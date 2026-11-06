"""Instance generator: natural-language requests with gold specs and gold answers.

Every instance is built from a gold spec first; the request text is then rendered from that spec, so
the text states exactly what the spec contains (and nothing else). The gold answer is the solver's
answer to the gold spec, and each instance is kept only if that answer matches the kind it was
built to be (for example an "infeasible / capacity" instance must get NO_PLAN).

    python -m instances.generate                   # writes instances/instances.json + SUMMARY.md
    python -m instances.generate --seed 7 --out x.json

Kinds (see SUMMARY.md for counts):
  q1/eligible, q1/missing_prereq, q1/wrong_term, q1/precluded, q1/already_done, q1/closed
  q2/loose, q2/tight                         (feasible; tight = one module less per semester breaks it)
  q2_infeasible/{exclusion, chain, capacity, parity, rule_conflict, hidden}
  missing_info/{q1, q2}
  out_of_scope/{programme, course}

Request wording follows docs/TRANSLATION_GUIDE.md sections 2 and 4, so a correct translation of the
text is the gold spec (after cleaning).
"""
from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from pathlib import Path

from m1_data.catalog import Catalog
from solver.run import run

HERE = Path(__file__).resolve().parent

# A typical BComp CS Hons roadmap, by the semester in which each course is usually taken.
ROADMAP = {
    1: ["CS1101S", "CS1231S", "MA1521", "ES2660"],
    2: ["CS2030S", "CS2040S", "MA1522", "IS1108"],
    3: ["CS2100", "CS2101", "CS2103T", "ST2334"],
    4: ["CS2106", "CS2109S", "CS3230"],
    5: ["CS2105", "CS3219"],
    6: ["CS2102"],
}
CORE = [c for s in sorted(ROADMAP) for c in ROADMAP[s]]
# Core courses no other core course depends on, so they can be "not yet done" without breaking the transcript.
LEAVES = ["ES2660", "IS1108", "CS2101", "ST2334", "CS3230", "CS2105", "CS2102"]

UNSUPPORTED = ["no 8am classes", "S/U option for CS2100", "might fail CS2106", "wants a waiver for CS2030S",
               "prefers modules with no final exam"]
UNSUPPORTED_TEXT = {
    "no 8am classes": "I don't want any 8am classes.",
    "S/U option for CS2100": "I may want to S/U CS2100.",
    "might fail CS2106": "I might fail CS2106, so keep that in mind.",
    "wants a waiver for CS2030S": "I'm also hoping to get a waiver for CS2030S.",
    "prefers modules with no final exam": "I'd prefer modules with no final exam.",
}
OTHER_PROGRAMMES = ["Business Analytics", "Information Systems", "Computer Engineering",
                    "BComp CS Hons with a second major in Mathematics", "BComp CS Hons with a minor in Economics",
                    "BComp CS and Business Administration double degree"]
NOT_IN_CATALOGUE = ["CS5340", "LAJ1201", "GEC1015", "CS4344", "CS5242"]


class Gen:
    def __init__(self, seed: int):
        self.r = random.Random(seed)
        self.cat = Catalog.load()
        self.C = json.load(open(HERE.parent / "data/processed/AY2026-2027/catalog.json"))["courses"]
        self.pool = [c for c, x in self.C.items()
                     if c[:3] in ("CS3", "CS4") and x["exists_in_ay"] and x["available"]
                     and x.get("details") != "stub" and x["mc"] == 4 and not c.endswith("R")]
        # Courses a student could realistically have completed: core plus undergraduate CS electives.
        self.plausible = set(self.pool) | set(CORE)
        self.t1_only = [c for c in self.pool if self.C[c]["offered"] == [1]]
        self.t2_only = [c for c in self.pool if self.C[c]["offered"] == [2]]

    # ---------- building blocks ----------
    def transcript(self, k: int, drop_max: int = 2) -> list[str]:
        done = [c for s in ROADMAP if s < k for c in ROADMAP[s]]
        for c in self.r.sample(LEAVES, self.r.randint(0, drop_max)):
            if c in done:
                done.remove(c)
        return done

    def remaining_core(self, done: list[str]) -> list[str]:
        return [c for c in CORE if c not in done]

    def electives(self, done, n):
        ok = [c for c in self.pool if c not in done and not self.cat.blocked_by(c, set(done))]
        return self.r.sample(ok, n)

    def solve(self, spec):
        return run(json.loads(json.dumps(spec)), self.cat)

    # ---------- Q1 ----------
    def q1(self, sub):
        for _ in range(500):
            k = self.r.randint(2, 8)
            done = self.transcript(k)
            target = None
            if sub == "precluded":
                cands = [(t, b) for t in self.pool + CORE if t not in done
                         for b in (self.C[t]["preclusion"].get("courses") or [])
                         if b in self.plausible
                         and b not in done and self.cat.can_take(b, set(done))[0]]
                if not cands:
                    continue
                target, b = self.r.choice(cands)
                done = done + [b]
            elif sub == "already_done":
                target = self.r.choice(done) if done else None
            elif sub == "closed":
                target = self.r.choice(["CS2109HS", "CS2040HS", "CS2030HS", "CS2100HS"])
            elif sub == "wrong_term":
                target = self.r.choice(self.t1_only if k % 2 == 0 else self.t2_only)
            else:
                target = self.r.choice(self.remaining_core(done) + self.electives(done, 3))
            if not target:
                continue
            spec = {"query": "eligible", "target": target, "current_sem": k, "completed": done}
            ans = self.solve(spec)
            reasons = " ".join(ans.get("reasons", []))
            want = {
                "eligible": ans["status"] == "ELIGIBLE",
                "missing_prereq": ans["status"] == "NOT_ELIGIBLE" and "missing prerequisite" in reasons
                and "not offered" not in reasons,
                "wrong_term": ans["status"] == "NOT_ELIGIBLE" and "not offered" in reasons
                and "missing" not in reasons,
                "precluded": ans["status"] == "NOT_ELIGIBLE" and "precluded" in reasons,
                "already_done": ans["status"] == "NOT_ELIGIBLE" and "already completed" in reasons,
                "closed": ans["status"] == "NOT_ELIGIBLE" and "unavailable" in reasons,
            }[sub]
            if want:
                return spec
        raise RuntimeError(f"could not build q1/{sub}")

    # ---------- Q2 feasible ----------
    def add_wishes(self, spec):
        r = self.r
        must = spec["must_take"]
        if r.random() < 0.5:
            spec["objective"] = r.choice(["earliest_graduation", "earliest_graduation", "min_total_mc"])
        if r.random() < 0.3:
            spec["early"] = [r.choice(must)]
        if r.random() < 0.2:
            spec["late"] = [r.choice([c for c in must if c not in spec.get("early", [])] or must)]
        if r.random() < 0.25:
            spec["light_sems"] = ["last"]
        if r.random() < 0.2:
            spec["balance_load"] = True
        rules = []
        if r.random() < 0.35 and len(must) >= 2:
            a, b = r.sample(must, 2)
            rules.append({"type": r.choice(["apart", "same_sem", "before"]), "a": a, "b": b, "strength": "prefer"})
        if r.random() < 0.25:
            rules.append({"type": "in_sem", "course": r.choice(must),
                          "sem": r.randint(spec["current_sem"], 8), "strength": "prefer"})
        if rules:
            spec["rules"] = rules
        if r.random() < 0.25:
            spec["unsupported"] = [r.choice(UNSUPPORTED)]
        if r.random() < 0.3:
            spec["programme"] = "BComp CS Hons"
        return spec

    def q2_base(self, k_lo=3, k_hi=7):
        k = self.r.randint(k_lo, k_hi)
        done = self.transcript(k)
        rem = self.remaining_core(done)
        must = self.r.sample(rem, self.r.randint(len(rem) // 2, len(rem))) if rem else []
        must += self.electives(done + must, self.r.randint(1, 4))
        return {"query": "plan", "current_sem": k, "completed": done, "must_take": must}

    def q2(self, sub):
        for _ in range(300):
            spec = self.q2_base()
            if self.r.random() < 0.25:
                spec["sem_caps"] = {str(self.r.randint(spec["current_sem"] + 1, 8)): 0}
            if sub == "loose":
                if self.r.random() < 0.6:
                    spec["mc_max"] = self.r.choice([16, 20])
                self.add_wishes(spec)
                if self.solve(spec)["status"] == "PLAN":
                    return spec
            else:  # tight: smallest per-semester module count that still has a plan
                self.add_wishes(spec)
                for mc in (4, 8, 12, 16, 20):
                    spec["mc_max"] = mc
                    if self.solve(spec)["status"] == "PLAN":
                        break
                else:
                    continue
                if mc == 4 or self.solve({**spec, "mc_max": mc - 4})["status"] == "NO_PLAN":
                    return spec
        raise RuntimeError(f"could not build q2/{sub}")

    # ---------- Q2 infeasible ----------
    def infeasible(self, sub):
        r = self.r
        for _ in range(500):
            if sub == "exclusion":
                spec = self.q2_base(3, 6)
                done = set(spec["completed"])
                cands = [(t, b) for t in self.pool if t not in done
                         for b in (self.C[t]["preclusion"].get("courses") or [])
                         if b in self.plausible
                         and b not in done and self.cat.can_take(b, done)[0]]
                if not cands:
                    continue
                t, b = r.choice(cands)
                if r.random() < 0.5:   # completed course rules the target out
                    spec["completed"] = spec["completed"] + [b]
                    spec["must_take"] = [c for c in spec["must_take"] if c != b] + [t]
                else:                  # two must-take courses exclude each other
                    spec["must_take"] = [c for c in spec["must_take"] if c not in (t, b)] + [t, b]
            elif sub == "chain":
                k = r.choice([7, 8])
                # A final-year student who never took CS2109S (or CS2106) and now needs a course built on it.
                done = [c for c in self.transcript(k, drop_max=0) if c not in ("CS2109S", "CS2106")]
                spec = {"query": "plan", "current_sem": k, "completed": done,
                        "must_take": r.sample(["CS3263", "CS4248", "CS3264", "CS4243", "CS3210", "CS4218"], 2)}
            elif sub == "capacity":
                spec = self.q2_base(5, 7)
                left = 9 - spec["current_sem"]
                spec["mc_max"] = r.choice([4, 8])
                need_courses = left * spec["mc_max"] // 4 + r.randint(1, 2)
                extra = self.electives(spec["completed"] + spec["must_take"], 6)
                spec["must_take"] = (spec["must_take"] + extra)[:max(need_courses, len(spec["must_take"]))]
            elif sub == "parity":
                k = r.choice([7, 8])
                done = self.transcript(7, drop_max=0)
                spec = {"query": "plan", "current_sem": k, "completed": done}
                if k == 7:
                    spec["sem_caps"] = {"8": 0}
                    course = r.choice(self.t2_only)
                else:
                    course = r.choice(self.t1_only)
                spec["must_take"] = self.electives(done + [course], 1) + [course]
            elif sub == "rule_conflict":
                spec = self.q2_base(4, 6)
                spec["mc_max"] = 8
                if len(spec["must_take"]) < 3:
                    continue
                a, b, c = r.sample(spec["must_take"], 3)
                s = r.randint(spec["current_sem"], 8)
                if r.random() < 0.5:
                    spec["rules"] = [{"type": "in_sem", "course": x, "sem": s, "strength": "must"} for x in (a, b, c)]
                else:
                    spec["rules"] = [{"type": "before", "a": a, "b": b, "strength": "must"},
                                     {"type": "before", "a": b, "b": a, "strength": "must"}]
            elif sub == "hidden":
                spec = self.q2_base(3, 6)
                done = set(spec["completed"])
                cands = [c for c in spec["must_take"] if not self.cat.can_take(c, done)[0]]
                if not cands:
                    continue
                spec["rules"] = [{"type": "in_sem", "course": r.choice(cands),
                                  "sem": spec["current_sem"], "strength": "must"}]
            if r.random() < 0.3:
                spec["objective"] = "earliest_graduation"
            ans = self.solve(spec)
            if ans["status"] != "NO_PLAN":
                continue
            # The relaxed spec (perturbation removed) must have a plan, so the perturbation is the cause.
            relaxed = self.relax(spec, sub)
            if relaxed is not None and self.solve(relaxed)["status"] != "PLAN":
                continue
            return spec
        raise RuntimeError(f"could not build infeasible/{sub}")

    def relax(self, spec, sub):
        s = json.loads(json.dumps(spec))
        if sub in ("rule_conflict", "hidden"):
            s.pop("rules", None)
        elif sub == "capacity":
            s["mc_max"] = 20
        elif sub == "parity":
            s.pop("sem_caps", None)
            s["current_sem"] = 7
        elif sub == "chain":
            s["current_sem"] = 5
        elif sub == "exclusion":
            return None
        return s

    # ---------- missing info / out of scope ----------
    def missing(self, sub):
        spec = self.q1("missing_prereq") if sub == "q1" else self.q2("loose")
        drop = (["completed"] if sub == "q1" else [self.r.choice(["completed", "current_sem"])])
        for f in drop:
            spec.pop(f)
        return spec

    def oos(self, sub):
        spec = self.q2("loose") if self.r.random() < 0.6 else self.q1("eligible")
        if sub == "programme":
            spec["programme"] = self.r.choice(OTHER_PROGRAMMES)
        else:
            code = self.r.choice(NOT_IN_CATALOGUE)
            assert code not in self.C
            if spec["query"] == "plan":
                spec["must_take"] = spec["must_take"] + [code]
            else:
                spec["target"] = code
        return spec


# ---------- rendering ----------
def sem_words(r, n):
    y, s = (n + 1) // 2, 2 - n % 2
    return r.choice([f"Y{y}S{s}", f"year {y} semester {s}", f"semester {n}"])


def listing(codes):
    codes = list(codes)
    if len(codes) == 1:
        return codes[0]
    return ", ".join(codes[:-1]) + " and " + codes[-1]


def render(spec, r) -> str:
    out = []
    prog = spec.get("programme")
    if prog:
        out.append("I am a Computer Science (BComp CS Hons) student." if prog == "BComp CS Hons"
                   else f"I am doing {prog}." if "degree" in prog or "with" in prog
                   else f"I am a {prog} student.")
    if "completed" in spec:
        done = list(spec["completed"])
        r.shuffle(done)
        out.append("I have not completed any module yet." if not done
                   else r.choice(["I have completed ", "I've finished ", "So far I have passed "])
                   + listing(done) + ".")
    if spec["query"] == "eligible":
        k = spec.get("current_sem")
        t = spec["target"]
        if k is None:
            out.append(f"Can I take {t} next semester?")
        elif k >= 2 and r.random() < 0.5:
            out.append(f"I am in {sem_words(r, k - 1)} now. Can I take {t} next semester?")
        else:
            out.append(f"Can I take {t} in {sem_words(r, k)}?")
    else:
        if "current_sem" in spec:
            out.append(r.choice(["I am in {} now.", "I am currently in {}.", "I'm starting {}."])
                       .format(sem_words(r, spec["current_sem"])))
        must = list(spec["must_take"])
        r.shuffle(must)
        out.append(r.choice(["I still have to take ", "I need to take ", "I must take "]) + listing(must) + "."
                   if must else "I have no more modules that I must take.")
        if "mc_max" in spec:
            m = spec["mc_max"]
            out.append(r.choice([f"I can take at most {m} MC per semester.",
                                 f"At most {m // 4} module{'s' if m > 4 else ''} per semester."]))
        if "mc_min" in spec:
            out.append(f"I want at least {spec['mc_min']} MC in every semester I study.")
        for s, cap in sorted(spec.get("sem_caps", {}).items()):
            out.append(r.choice([f"Semester {s} is my exchange semester.", f"I will do NOC in semester {s}."])
                       if cap == 0 else f"At most {cap} MC in semester {s}.")
        obj = spec.get("objective")
        if obj == "earliest_graduation":
            out.append(r.choice(["I want to graduate as early as possible.", "Please use the fewest semesters."]))
        elif obj == "min_total_mc":
            out.append("I want the fewest total credits.")
        if spec.get("light_sems") == ["last"]:
            out.append("I'd like a light last semester.")
        if spec.get("balance_load"):
            out.append("Please spread the workload evenly.")
        for c in spec.get("early", []):
            out.append(f"I would like {c} as early as possible.")
        for c in spec.get("late", []):
            out.append(f"I would like {c} as late as possible.")
        for ru in spec.get("rules", []):
            must_word = ru["strength"] == "must"
            t = ru["type"]
            if t == "in_sem":
                out.append(f"{ru['course']} has to be in semester {ru['sem']}." if must_word
                           else f"If possible, I would like {ru['course']} in semester {ru['sem']}.")
            elif t == "before":
                out.append(f"{ru['a']} must come before {ru['b']}." if must_word
                           else f"Ideally I'd take {ru['a']} before {ru['b']}.")
            elif t == "apart":
                out.append(f"{ru['a']} and {ru['b']} must not be in the same semester." if must_word
                           else f"I'd prefer {ru['a']} and {ru['b']} in different semesters.")
            elif t == "same_sem":
                out.append(f"{ru['a']} and {ru['b']} must be in the same semester." if must_word
                           else f"I would like {ru['a']} and {ru['b']} together in one semester.")
        out.append(r.choice(["Please plan my remaining semesters.", "Can you plan the rest of my degree?",
                             "What should my plan look like?"]))
    for u in spec.get("unsupported", []):
        out.append(UNSUPPORTED_TEXT[u])
    return " ".join(out)


PLAN = [("q1", s, n) for s, n in [("eligible", 12), ("missing_prereq", 8), ("wrong_term", 4),
                                    ("precluded", 3), ("already_done", 2), ("closed", 1)]] + \
       [("q2", "loose", 25), ("q2", "tight", 20)] + \
       [("q2_infeasible", s, 4) for s in ["exclusion", "chain", "capacity", "parity", "rule_conflict", "hidden"]] + \
       [("missing_info", "q1", 3), ("missing_info", "q2", 4), ("out_of_scope", "programme", 6),
        ("out_of_scope", "course", 3)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=3263)
    ap.add_argument("--out", default=str(HERE / "instances.json"))
    a = ap.parse_args()
    g = Gen(a.seed)
    rows = []
    for group, sub, n in PLAN:
        for _ in range(n):
            build = {"q1": g.q1, "q2": g.q2, "q2_infeasible": g.infeasible,
                     "missing_info": g.missing, "out_of_scope": g.oos}[group]
            spec = build(sub)
            ans = g.solve(spec)
            iid = f"{group}-{sub}-{sum(1 for x in rows if x['kind'] == f'{group}/{sub}') + 1:02d}"
            rows.append({"id": iid, "kind": f"{group}/{sub}", "request": render(spec, g.r),
                         "gold_spec": spec, "gold_answer": ans})
    Path(a.out).write_text(json.dumps(rows, indent=1))
    kinds = Counter(x["kind"] for x in rows)
    status = Counter((x["kind"].split("/")[0], x["gold_answer"]["status"]) for x in rows)
    lines = [f"# Instance set (seed {a.seed})", "", f"{len(rows)} instances. Regenerate with "
             f"`python -m instances.generate --seed {a.seed}`.", "", "| Kind | Count |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in kinds.items()]
    lines += ["", "| Group | Gold status | Count |", "|---|---|---|"]
    lines += [f"| {g_} | {s} | {v} |" for (g_, s), v in sorted(status.items())]
    lines += ["", "## Examples", ""]
    seen = set()
    for x in rows:
        if x["kind"] in seen:
            continue
        seen.add(x["kind"])
        lines += [f"**{x['id']}**: {x['request']}", "",
                  f"Gold status: `{x['gold_answer']['status']}`", ""]
    (Path(a.out).parent / "SUMMARY.md").write_text("\n".join(lines))
    print(f"wrote {len(rows)} instances to {a.out}")
    print(dict(kinds))


if __name__ == "__main__":
    main()
