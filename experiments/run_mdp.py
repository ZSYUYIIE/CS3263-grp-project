"""Bidding experiment: how does a CP-SAT plan fare when bids can fail, and does the MDP do better?

    python -m experiments.run_mdp                                   # instances/instances.json
    python -m experiments.run_mdp --out rows.csv --limit 10

For every request in the instance file that has a plan, and for both probability estimates
(`solver/admission.py`), three ways of acting are compared in the same model of failed bids:

    plan      follow the CP-SAT plan as written; it works only if every bid succeeds
    replan    bid for the first semester of the CP-SAT plan, then ask CP-SAT again with the courses
              actually obtained, every semester
    mdp       the optimal policy of `solver/mdp.py`

Every request is solved for earliest graduation and without its preferences, so that the three
aim at the same thing. Outcomes are computed exactly (`BiddingMDP.evaluate`), not sampled.
Writes one CSV row per (instance, estimator) and prints a summary. See docs/MDP_GUIDE.md section 6.
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
import time

from m1_data.catalog import Catalog
from solver.admission import ESTIMATORS, Admission
from solver.mdp import BiddingMDP, TooLarge, build, on_time, plan_success
from solver.run import run

COLUMNS = ["id", "estimator", "last_semester", "courses", "uncertain", "states", "mdp_seconds",
           "plan_success", "replan_on_time", "mdp_on_time", "replan_cost", "mdp_cost", "cpsat_calls"]
PREFERENCE_FIELDS = ("rules", "early", "late")
GAIN = 0.001      # a difference in on-time probability smaller than this counts as a tie


def for_graduation(spec: dict) -> dict:
    """The spec asked for earliest graduation, without preferences."""
    kept = {key: value for key, value in spec.items() if key not in PREFERENCE_FIELDS}
    kept["objective"] = "earliest_graduation"
    return kept


def replan_policy(spec: dict, mdp: BiddingMDP, catalog):
    """policy(semester, got): the first semester of a fresh CP-SAT plan from that state."""
    cache: dict[tuple, tuple] = {}

    def policy(semester: int, got: frozenset) -> tuple:
        key = (semester, got)
        if key not in cache:
            state = dict(spec)
            state["current_sem"] = semester
            # the original order first, so that the first call is the request itself and gives the same plan
            state["completed"] = list(spec["completed"]) + sorted(got)
            state["must_take"] = [code for code in spec["must_take"] if code not in got]
            answer = run(state, catalog)
            cache[key] = tuple(answer["plan"].get(str(semester), [])) if answer["status"] == "PLAN" else ()
        return cache[key]

    policy.cache = cache
    return policy


def row_of(instance: dict, estimator: str, admission: Admission, catalog) -> dict | None:
    spec = for_graduation(instance["gold_spec"])
    started = time.perf_counter()
    early, mdp, plan_answer, _warnings = build(spec, catalog, admission)
    if early is not None:
        return None
    try:
        finish = mdp.evaluate()
    except TooLarge:
        return None
    seconds = time.perf_counter() - started
    replan = replan_policy(spec, mdp, catalog)
    replan_finish = mdp.evaluate(replan)
    uncertain = [c for c in mdp.candidates
                 if any(admission.p(c, s) < 1.0 for s in (1, 2) if s in catalog[c]["offered"])]
    return {
        "id": instance["id"],
        "estimator": estimator,
        "last_semester": plan_answer["last_semester"],
        "courses": len(mdp.candidates),
        "uncertain": len(uncertain),
        "states": len(mdp.values),
        "mdp_seconds": round(seconds, 3),
        "plan_success": round(plan_success(mdp, plan_answer["plan"]), 4),
        "replan_on_time": round(on_time(replan_finish), 4),
        "mdp_on_time": round(on_time(finish), 4),
        "replan_cost": round(mdp.expected_cost(replan_finish), 4),
        "mdp_cost": round(mdp.expected_cost(finish), 4),
        "cpsat_calls": len(replan.cache),
    }


def summarise(rows: list[dict], estimator: str) -> None:
    mine = [r for r in rows if r["estimator"] == estimator]
    if not mine:
        return
    affected = [r for r in mine if r["uncertain"]]
    better = [r for r in mine if r["mdp_on_time"] - r["replan_on_time"] > GAIN]
    worse = [r for r in mine if r["replan_on_time"] - r["mdp_on_time"] > GAIN]

    def mean(key: str) -> float:
        return statistics.mean(r[key] for r in mine)

    print(f"\n{estimator}: {len(mine)} requests, {len(affected)} with at least one uncertain course")
    print(f"  mean probability the plan works as written   {mean('plan_success'):.3f}")
    print(f"  mean on-time probability, replan with CP-SAT {mean('replan_on_time'):.3f}")
    print(f"  mean on-time probability, MDP policy         {mean('mdp_on_time'):.3f}")
    print(f"  MDP better on {len(better)}, equal on {len(mine) - len(better) - len(worse)}, "
          f"worse on {len(worse)} (difference above {GAIN})")
    if better:
        top = max(better, key=lambda r: r["mdp_on_time"] - r["replan_on_time"])
        print(f"  largest gain: {top['id']} from {top['replan_on_time']:.3f} to {top['mdp_on_time']:.3f}")
    print(f"  states: median {statistics.median(r['states'] for r in mine):.0f}, "
          f"largest {max(r['states'] for r in mine)}; "
          f"slowest policy {max(r['mdp_seconds'] for r in mine):.2f} s")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("instances", nargs="?", default="instances/instances.json")
    parser.add_argument("--out", help="write the rows to this CSV file")
    parser.add_argument("--limit", type=int, help="use only the first N requests that have a plan")
    args = parser.parse_args()

    with open(args.instances, encoding="utf-8") as f:
        instances = [x for x in json.load(f)
                     if x["gold_spec"].get("query") == "plan" and x["gold_answer"].get("status") == "PLAN"]
    if args.limit:
        instances = instances[:args.limit]
    catalog = Catalog.load()
    rows, skipped = [], set()
    for estimator in ESTIMATORS:
        admission = Admission.load(estimator)
        for instance in instances:
            row = row_of(instance, estimator, admission, catalog)
            if row is None:
                skipped.add(instance["id"])
            else:
                rows.append(row)
    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
    print(f"{len(instances)} requests with a plan; {len(skipped)} not covered by the MDP "
          f"(must rules, ATAP, mc_min or too many states): {sorted(skipped)}")
    for estimator in ESTIMATORS:
        summarise(rows, estimator)


if __name__ == "__main__":
    main()
