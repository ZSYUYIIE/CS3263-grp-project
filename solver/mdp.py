"""Bidding under uncertainty: a finite-horizon MDP on top of a Q2 spec.

The CSP of `model.py` assumes the student gets every course in the plan. Here a bid for a course
succeeds only with a probability (`solver/admission.py`), so the answer is a policy: what to bid for
in each semester, given the courses obtained so far. Formulation, data and limits: docs/MDP_GUIDE.md.

    state       (semester s, set of courses obtained so far)
    action      a set of courses to bid for in s (offered, prerequisites done, within the MC cap)
    transition  each course in the bid is obtained independently with probability p(course, term of s)
    cost        1 per semester until every must_take course is obtained;
                `overrun` more if that has not happened by semester 8
    solution    backward induction over the reachable states (the horizon is at most 8 semesters)

CP-SAT decides which courses are needed (the must_take courses and the prerequisites it adds); the
MDP decides when to bid for them. With every probability equal to 1 the MDP is the CSP again: its
value is the CP-SAT last semester. This module only reads the other solver modules, and
`solver.run.run` does not call it.

    from solver.mdp import solve
    answer = solve(spec)                                   # probabilities from the reports
    answer = solve(spec, admission=Admission.from_dict({"CS4248": 0.6}))
CLI: `python -m solver.mdp path/to/spec.json [--estimator round1] [--p CS4248=0.6]`.
"""
from __future__ import annotations

import argparse
import json

from m1_data.catalog import Catalog, satisfied
from solver import q2
from solver.admission import DEFAULT_ESTIMATOR, ESTIMATORS, Admission
from solver.common import LAST_SEM, term_of
from solver.run import prepare

OVERRUN_SEMESTERS = 2        # cost of not finishing by semester 8: one more academic year
MAX_STATES = 200_000         # the search stops with TOO_LARGE beyond this many states
LATE = "late"                # key of the finish distribution for "not done by semester 8"
EPS = 1e-12


class TooLarge(Exception):
    pass


class BiddingMDP:
    """The MDP of one cleaned Q2 spec over a fixed set of candidate courses."""

    def __init__(self, spec: dict, catalog, candidates, admission: Admission,
                 overrun: float = OVERRUN_SEMESTERS, all_bids: bool = False):
        self.catalog = catalog
        self.admission = admission
        self.overrun = overrun
        self.all_bids = all_bids
        self.start = spec["current_sem"]
        self.done0 = frozenset(spec["completed"])
        self.required = frozenset(spec["must_take"]) - self.done0
        self.candidates = sorted(set(candidates) - self.done0)
        self.caps = {s: spec["sem_caps"].get(s, spec["mc_max"]) for s in range(self.start, LAST_SEM + 1)}
        self.values: dict[tuple, float] = {}
        self.choices: dict[tuple, tuple] = {}
        self.bid_cache: dict[tuple, list[tuple]] = {}

    # ---- the rules of one semester -------------------------------------------------------------

    def mc(self, code: str) -> int:
        return int(self.catalog[code]["mc"])

    def finished(self, got: frozenset) -> bool:
        return self.required <= got

    def legal(self, code: str, semester: int, got: frozenset) -> bool:
        """May `code` be bid for in `semester`, leaving its corequisites aside?"""
        record = self.catalog.courses.get(code)
        if record is None or not (record["exists_in_ay"] and record["available"]):
            return False
        done = self.done0 | got
        if code in done or term_of(semester) not in record["offered"]:
            return False
        if self.catalog.blocked_by(code, done):
            return False
        return satisfied(record["prereq"]["logic"], done)

    def coreq_ok(self, code: str, held) -> bool:
        return satisfied(self.catalog[code]["coreq"]["logic"], held)

    def bid_error(self, semester: int, got: frozenset, bid) -> str | None:
        """Why `bid` is not allowed in this state, or None. Checks a policy given from outside."""
        done = self.done0 | got
        if len(set(bid)) != len(bid):
            return "a course is listed twice"
        for code in bid:
            if not self.legal(code, semester, got):
                return f"{code} cannot be taken in semester {semester}"
            if not self.coreq_ok(code, done | set(bid)):
                return f"{code} lacks its corequisite"
            if self.catalog.blocked_by(code, set(bid) - {code}):
                return f"{code} excludes another course in the bid"
        if sum(self.mc(c) for c in bid) > self.caps[semester]:
            return f"more than {self.caps[semester]} MC"
        return None

    def bids(self, semester: int, got: frozenset) -> list[tuple]:
        """The bids considered in a state. Bidding costs nothing and an extra course never hurts,
        so a bid that still has room for another course is never better than the larger one; unless
        `all_bids` is set, only the bids that cannot be extended are returned."""
        key = (semester, got)
        if key in self.bid_cache:
            return self.bid_cache[key]
        cap = self.caps[semester]
        done = self.done0 | got
        open_now = [c for c in self.candidates if c not in got and self.legal(c, semester, got)]
        found: list[tuple] = []

        def extend(index: int, chosen: list[str], load: int) -> None:
            if index == len(open_now):
                held = done | set(chosen)
                if all(self.coreq_ok(c, held) for c in chosen):
                    found.append(tuple(chosen))
                return
            code = open_now[index]
            fits = load + self.mc(code) <= cap
            if fits and not self.catalog.blocked_by(code, set(chosen)):
                extend(index + 1, [*chosen, code], load + self.mc(code))
            extend(index + 1, chosen, load)

        extend(0, [], 0)
        if not self.all_bids:
            as_sets = [set(b) for b in found]
            found = [b for b, s in zip(found, as_sets) if not any(s < other for other in as_sets)]
        self.bid_cache[key] = found
        return found

    def outcomes(self, semester: int, got: frozenset, bid) -> list[tuple[float, frozenset]]:
        """(probability, courses obtained after the semester) for every result of a bid. A course
        obtained without its corequisite is given up."""
        risky = [c for c in bid if self.admission.p(c, semester) < 1.0]
        sure = [c for c in bid if c not in risky]
        done = self.done0 | got
        results: dict[frozenset, float] = {}
        for mask in range(1 << len(risky)):
            probability = 1.0
            won = set(sure)
            for i, code in enumerate(risky):
                p = self.admission.p(code, semester)
                if mask >> i & 1:
                    won.add(code)
                    probability *= p
                else:
                    probability *= 1.0 - p
            if probability == 0.0:
                continue
            while True:
                dropped = {c for c in won if not self.coreq_ok(c, done | won)}
                if not dropped:
                    break
                won -= dropped
            after = got | won
            results[after] = results.get(after, 0.0) + probability
        return [(p, after) for after, p in sorted(results.items(), key=lambda item: sorted(item[0]))]

    # ---- backward induction --------------------------------------------------------------------

    def q(self, semester: int, got: frozenset, bid) -> float:
        """Expected cost of bidding `bid` now and acting optimally afterwards."""
        return 1.0 + sum(p * self.value(semester + 1, after) for p, after in self.outcomes(semester, got, bid))

    def value(self, semester: int, got: frozenset) -> float:
        """Least expected cost from a state (the Bellman equation, memoised)."""
        if self.finished(got):
            return 0.0
        if semester > LAST_SEM:
            return float(self.overrun)
        key = (semester, got)
        if key not in self.values:
            if len(self.values) >= MAX_STATES:
                raise TooLarge
            best_cost, best_bid = None, ()
            for bid in self.bids(semester, got):
                cost = self.q(semester, got, bid)
                if best_cost is None or cost < best_cost - EPS:
                    best_cost, best_bid = cost, bid
            self.values[key] = best_cost
            self.choices[key] = best_bid
        return self.values[key]

    def policy(self, semester: int, got: frozenset) -> tuple:
        """The optimal bid in a state (the first one found among equally good bids)."""
        if self.finished(got) or semester > LAST_SEM:
            return ()
        self.value(semester, got)
        return self.choices[(semester, got)]

    # ---- evaluating any policy exactly ---------------------------------------------------------

    def evaluate(self, policy=None) -> dict:
        """Distribution of the finishing semester under `policy(semester, got) -> bid`, computed by
        pushing probability forward through the semesters (no sampling). Keys are semesters and
        `LATE`. Default: the optimal policy. A bid that breaks a rule raises ValueError."""
        policy = policy or self.policy
        finish: dict = {}
        if self.finished(frozenset()):
            return {self.start - 1: 1.0}
        front = {frozenset(): 1.0}
        for semester in range(self.start, LAST_SEM + 1):
            following: dict[frozenset, float] = {}
            for got, mass in sorted(front.items(), key=lambda item: sorted(item[0])):
                bid = tuple(policy(semester, got))
                error = self.bid_error(semester, got, bid)
                if error:
                    raise ValueError(f"semester {semester}, bid {list(bid)}: {error}")
                for p, after in self.outcomes(semester, got, bid):
                    if self.finished(after):
                        finish[semester] = finish.get(semester, 0.0) + mass * p
                    else:
                        following[after] = following.get(after, 0.0) + mass * p
            front = following
        late = sum(front.values())
        if late > 0.0:
            finish[LATE] = late
        return finish

    def expected_cost(self, finish: dict) -> float:
        """Expected cost of a finish distribution, in the units of `value`."""
        total = 0.0
        for when, mass in finish.items():
            semesters = LAST_SEM - self.start + 1 + self.overrun if when == LATE else when - self.start + 1
            total += mass * semesters
        return total


def on_time(finish: dict) -> float:
    return 1.0 - finish.get(LATE, 0.0)


def expected_last(finish: dict) -> float | None:
    """Mean finishing semester among the outcomes that finish by semester 8."""
    mass = on_time(finish)
    if mass <= 0.0:
        return None
    return sum(when * p for when, p in finish.items() if when != LATE) / mass


def unsupported_reasons(cleaned: dict) -> list[str]:
    if cleaned["query"] != "plan":
        return ["only a plan request (query 'plan') can be turned into a bidding policy"]
    reasons = []
    if any(rule["strength"] == "must" for rule in cleaned["rules"]):
        reasons.append("must rules are not modelled under uncertainty")
    if "atap_sems" in cleaned:
        reasons.append("ATAP is not modelled under uncertainty")
    if "mc_min" in cleaned:
        reasons.append("a minimum load (mc_min) is not modelled under uncertainty")
    return reasons


def build(spec, catalog=None, admission: Admission | None = None,
          overrun: float = OVERRUN_SEMESTERS, all_bids: bool = False):
    """Front half shared with the experiment. Returns (early answer or None, mdp, CP-SAT answer,
    warnings). The early answer is the solver's own INVALID_SPEC / OUT_OF_SCOPE / MISSING_INFO /
    NO_PLAN, or UNSUPPORTED for a request the MDP does not cover."""
    catalog = catalog or Catalog.load()
    admission = admission if admission is not None else Admission.load()
    early, cleaned, warnings = prepare(spec, catalog)
    if early is not None:
        return early, None, None, warnings
    reasons = unsupported_reasons(cleaned)
    if reasons:
        return {"status": "UNSUPPORTED", "reasons": reasons}, None, None, warnings
    plan_answer = q2.answer(cleaned, catalog)
    if plan_answer["status"] != "PLAN":
        return plan_answer, None, None, warnings
    candidates = [code for courses in plan_answer["plan"].values() for code in courses]
    mdp = BiddingMDP(cleaned, catalog, candidates, admission, overrun, all_bids)
    return None, mdp, plan_answer, warnings


def _shown(value: float) -> float:
    return round(value, 4)


def _distribution(finish: dict) -> dict:
    numbered = sorted(k for k in finish if k != LATE)
    shown = {str(k): _shown(finish[k]) for k in numbered}
    if LATE in finish:
        shown[LATE] = _shown(finish[LATE])
    return shown


def plan_success(mdp: BiddingMDP, plan: dict) -> float:
    """Probability that every bid of a fixed plan succeeds in the semester the plan gives it."""
    probability = 1.0
    for semester, courses in plan.items():
        for code in courses:
            probability *= mdp.admission.p(code, int(semester))
    return probability


def solve(spec, catalog=None, admission: Admission | None = None,
          overrun: float = OVERRUN_SEMESTERS) -> dict:
    """Bidding policy for one Q2 spec: POLICY, or the answer that explains why there is none."""
    early, mdp, plan_answer, warnings = build(spec, catalog, admission, overrun)
    if early is not None:
        result = early
    else:
        try:
            result = _policy_answer(mdp, plan_answer)
        except TooLarge:
            result = {"status": "TOO_LARGE",
                      "reasons": [f"the policy needs more than {MAX_STATES} states "
                                  f"({len(mdp.candidates)} courses to schedule)"]}
    if warnings and "warnings" not in result:
        result["warnings"] = warnings
    return result


def _policy_answer(mdp: BiddingMDP, plan_answer: dict) -> dict:
    start, nothing = mdp.start, frozenset()
    cost = mdp.value(start, nothing)
    nothing_to_take = mdp.finished(nothing)
    finish = {} if nothing_to_take else mdp.evaluate()
    first = mdp.policy(start, nothing)
    last = None if nothing_to_take else expected_last(finish)

    alternatives = []
    if not nothing_to_take:
        scored = sorted(((mdp.q(start, nothing, bid), bid) for bid in mdp.bids(start, nothing)),
                        key=lambda item: (round(item[0], 9), item[1]))
        alternatives = [{"courses": list(bid), "expected_cost": _shown(value)} for value, bid in scored[:5]]

    if_then = []
    if first and start < LAST_SEM:
        for p, after in mdp.outcomes(start, nothing, first):
            if _shown(p) == 0.0:
                continue
            if_then.append({
                "probability": _shown(p),
                "obtained": sorted(after),
                "missed": sorted(set(first) - after),
                "next_bid": list(mdp.policy(start + 1, after)),
            })
        if_then.sort(key=lambda row: -row["probability"])

    table, no_data = {}, []
    for code in mdp.candidates:
        terms = [t for t in mdp.catalog[code]["offered"] if t in (1, 2)]
        if any(mdp.admission.p(code, t) < 1.0 for t in terms):
            table[code] = {str(t): mdp.admission.p(code, t) for t in terms}
        if mdp.admission.from_reports and not any(mdp.admission.known(code, t) for t in terms):
            no_data.append(code)

    result = {
        "status": "POLICY",
        "estimator": mdp.admission.estimator,
        "first_bid": {"semester": start, "courses": list(first)},
        "if_then": if_then,
        "alternatives": alternatives,
        "expected_cost": _shown(cost),
        "on_time_probability": _shown(on_time(finish)),
        "expected_last_semester": None if last is None else _shown(last),
        "finish_distribution": _distribution(finish),
        "admission": table,
        "deterministic": {
            "last_semester": plan_answer["last_semester"],
            "plan": plan_answer["plan"],
            "success_probability": _shown(plan_success(mdp, plan_answer["plan"])),
        },
        "model": {
            "courses": len(mdp.candidates),
            "uncertain": sorted(table),
            "no_data": no_data,
            "states": len(mdp.values),
            "overrun": mdp.overrun,
        },
    }
    notes = list(plan_answer.get("notes", []))
    objective = plan_answer["objective"]
    if objective != "earliest_graduation":
        notes.append(f"objective '{objective}' only decided which courses are needed; "
                     "the policy minimises the expected finishing semester")
    if notes:
        result["notes"] = notes
    preferences = plan_answer["preferences_met"] + plan_answer["preferences_not_met"]
    not_applied = list(plan_answer.get("not_applied", [])) + [f"preference: {label}" for label in preferences]
    if not_applied:
        result["not_applied"] = not_applied
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Bidding policy for one Q2 spec (docs/MDP_GUIDE.md).")
    parser.add_argument("spec", help="path to a spec JSON file")
    parser.add_argument("--estimator", choices=ESTIMATORS, default=DEFAULT_ESTIMATOR)
    parser.add_argument("--overrun", type=float, default=OVERRUN_SEMESTERS,
                        help="cost, in semesters, of not finishing by semester 8")
    parser.add_argument("--p", action="append", default=[], metavar="CODE=PROB",
                        help="set one course's probability by hand (both terms); repeatable")
    args = parser.parse_args()

    admission = Admission.load(args.estimator)
    for item in args.p:
        code, _, value = item.partition("=")
        override = Admission.from_dict({code: float(value)})
        admission.table.update(override.table)
    if args.p:
        admission.estimator = f"{args.estimator} with {len(args.p)} set by hand"
    with open(args.spec, encoding="utf-8") as f:
        try:
            spec = json.load(f)
        except json.JSONDecodeError as error:
            print(json.dumps({"status": "INVALID_SPEC", "errors": [f"not valid JSON: {error}"]}, indent=2))
            return
    print(json.dumps(solve(spec, admission=admission, overrun=args.overrun), indent=2))


if __name__ == "__main__":
    main()
