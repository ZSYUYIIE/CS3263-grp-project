"""Exhaustive check of the gold answers on small instances, written from docs/SOLVER_GUIDE.md sections 4 to 6.

Imports nothing from solver/ or m1_data/. For each gold PLAN or NO_PLAN instance whose search space is at most --max-space
assignments, it enumerates every assignment of courses to semesters, keeps the plans that pass eval/checker.py, and ranks
them by the guide's order (objective, fewest added courses, most preferences). A gold PLAN is confirmed when it is
optimal on all three; a gold NO_PLAN is confirmed when no valid plan exists.

    python -m eval.verify_gold_exhaustive --instances instances/q2_900.json
    python -m eval.verify_gold_exhaustive --instances instances/q2_900.json --max-space 100000 --out results/verify/exhaustive_q2.csv
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import time
from collections import Counter
from math import prod
from pathlib import Path

from eval.checker import ATAP, C, ROOT, check_plan, holds, measures, must_rule_courses, normalise_plan, rule_holds


def plannable(code, done):
    x = C.get(code)
    if not x or not x["exists_in_ay"] or not x["available"] or x.get("details") == "stub":
        return False
    blocked = x["preclusion"].get("blocked_if")
    return not (blocked is not None and holds(blocked, done))


def find_candidates(spec):
    done = set(spec.get("completed") or [])
    required = (set(spec.get("must_take") or []) | must_rule_courses(spec)) - done
    if spec.get("atap_sems"):
        required.add(ATAP)
    if any(not plannable(c, done) for c in required):
        return None, required
    seen, queue, found = set(), sorted(required), []
    while queue:
        code = queue.pop(0)
        if code in seen or code in done:
            continue
        seen.add(code)
        if not plannable(code, done):
            continue
        found.append(code)
        x = C[code]
        queue += sorted((x["prereq"].get("courses") or []) + (x["coreq"].get("courses") or []))
    return found, required


def semester_cap(spec, s):
    return {int(k): v for k, v in (spec.get("sem_caps") or {}).items()}.get(s, spec.get("mc_max", 20))


def domains(spec, candidates, required):
    k = spec["current_sem"]
    out = []
    for code in candidates:
        sems = [s for s in range(k, 9) if semester_cap(spec, s) > 0 and (1 if s % 2 else 2) in C[code]["offered"]]
        if code == ATAP and spec.get("atap_sems"):
            sems = [s for s in sems if s in spec["atap_sems"]]
        out.append(sems if code in required else [0] + sems)
    return out


def objective_value(spec, plan):
    m = measures(spec, plan)
    kind = spec.get("objective", "none")
    if kind == "earliest_graduation":
        return m["last_semester"] if m["last_semester"] is not None else spec["current_sem"] - 1
    if kind == "min_total_mc":
        return m["total_mc"]
    return 0


def preference_count(spec, plan, targets):
    plan = normalise_plan(plan)
    sem_of = {c: s for s, codes in plan.items() for c in codes}
    done = set(spec.get("completed") or [])
    k = spec["current_sem"]
    met = 0
    for r in spec.get("rules") or []:
        if r.get("strength") == "prefer":
            met += rule_holds(r, sem_of, done) and not (r["type"] == "in_sem" and r["course"] in done)
    for c in spec.get("early") or []:
        met += c in done or sem_of.get(c) == targets["early"].get(c)
    for c in spec.get("late") or []:
        met += c in done or sem_of.get(c) == targets["late"].get(c)
    return met


def verify(inst, max_space):
    spec, gold = inst["gold_spec"], inst["gold_answer"]
    if spec.get("light_sems") or spec.get("balance_load"):
        return {"id": inst["id"], "kind": inst["kind"], "gold_status": gold["status"], "candidates": "", "space": "",
                "valid_plans": "", "result": "skipped (light_sems or balance_load is not checked)", "detail": ""}
    candidates, required = find_candidates(spec)
    row = {"id": inst["id"], "kind": inst["kind"], "gold_status": gold["status"], "candidates": "", "space": "",
           "valid_plans": "", "result": "", "detail": ""}
    if candidates is None:
        row.update(candidates=0, space=0, valid_plans=0)
        valid = []
    else:
        doms = domains(spec, candidates, required)
        space = prod(len(d) for d in doms)
        row.update(candidates=len(candidates), space=space)
        if space > max_space:
            row["result"] = "skipped (space above limit)"
            return row
        valid = []
        for values in itertools.product(*doms):
            plan = {}
            for code, s in zip(candidates, values):
                if s:
                    plan.setdefault(s, []).append(code)
            if not check_plan(spec, plan):
                valid.append(plan)
        row["valid_plans"] = len(valid)
    if gold["status"] == "NO_PLAN":
        row["result"] = "confirmed" if not valid else "MISMATCH"
        row["detail"] = "" if not valid else f"{len(valid)} valid plans exist, for example {json.dumps(valid[0])}"
        return row
    if not valid:
        row.update(result="MISMATCH", detail="gold is PLAN but no valid plan was found")
        return row
    best = min(objective_value(spec, p) for p in valid)
    tied = [p for p in valid if objective_value(spec, p) == best]
    fewest = min(len(measures(spec, p)["added"]) for p in tied)
    tied = [p for p in tied if len(measures(spec, p)["added"]) == fewest]
    targets = {"early": {}, "late": {}}
    for c in set(spec.get("early") or []) | set(spec.get("late") or []):
        sems = [s for p in tied for s, codes in p.items() if c in codes]
        if sems:
            targets["early"][c], targets["late"][c] = min(sems), max(sems)
    most = max(preference_count(spec, p, targets) for p in tied)
    gold_plan = normalise_plan(gold["plan"])
    problems = []
    if objective_value(spec, gold_plan) != best:
        problems.append(f"objective {objective_value(spec, gold_plan)} but the best is {best}")
    elif len(measures(spec, gold_plan)["added"]) != fewest:
        problems.append(f"{len(measures(spec, gold_plan)['added'])} added courses but the fewest is {fewest}")
    elif preference_count(spec, gold_plan, targets) != most:
        problems.append(f"{preference_count(spec, gold_plan, targets)} preferences met but the most is {most}")
    if not problems and preference_count(spec, gold_plan, targets) != len(gold.get("preferences_met", [])):
        problems.append(f"the solver reports {len(gold.get('preferences_met', []))} preferences met, this check counts "
                        f"{preference_count(spec, gold_plan, targets)}")
    row["result"] = "MISMATCH" if problems else "confirmed"
    row["detail"] = "; ".join(problems)
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instances", default=str(ROOT / "instances/instances.json"))
    ap.add_argument("--max-space", type=int, default=100000)
    ap.add_argument("--out", default=str(ROOT / "results/verify/exhaustive.csv"))
    a = ap.parse_args()
    rows, started = [], time.time()
    insts = [i for i in json.loads(Path(a.instances).read_text()) if i["gold_answer"]["status"] in ("PLAN", "NO_PLAN")]
    for n, inst in enumerate(insts, 1):
        rows.append(verify(inst, a.max_space))
        if n % 50 == 0:
            print(f"[{n}/{len(insts)}] {time.time() - started:.0f}s", flush=True)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    ran = [r for r in rows if not r["result"].startswith("skipped")]
    print(f"\n{len(insts)} gold PLAN or NO_PLAN instances; {len(ran)} within {a.max_space} assignments "
          f"({100 * len(ran) / len(insts):.1f}%), {len(insts) - len(ran)} skipped; {time.time() - started:.0f}s")
    for status in ("PLAN", "NO_PLAN"):
        print(f"gold {status}: {dict(Counter(r['result'] for r in ran if r['gold_status'] == status))}")
    for r in rows:
        if r["result"] == "MISMATCH":
            print("MISMATCH", r["id"], r["kind"], r["detail"])
    print(f"written to {out}")


if __name__ == "__main__":
    main()
