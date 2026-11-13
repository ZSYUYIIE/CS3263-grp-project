"""Compare the gold answers with the independent backtracking solver (solver/backtrack.py, which is left unchanged).

For each gold PLAN or NO_PLAN instance, solves the gold spec with one backtracking variant and compares status,
the graded measures in order: the objective (last semester for earliest_graduation, total MC for min_total_mc), the number
of added courses and the number of preferences met (the last semester under the other objectives is only a tie-break, so it is noted in the detail column but is not a DIFF), as in docs/SOLVER_GUIDE.md section 6. A returned plan must also pass eval/checker.py. Instances that hit the time limit are counted separately.

    python -m eval.verify_gold_backtrack --instances instances/q2_900.json
    python -m eval.verify_gold_backtrack --instances instances/q2_900.json --time-limit 200 --max-log10 99 --retry-from results/verify/backtrack_mac_all_q2.csv --out results/verify/backtrack_mac_retry_q2.csv
    python -m eval.verify_gold_backtrack --instances instances/q2_900.json --variant mac --time-limit 40 --workers 4

Instances whose state space (meta log10_omega) is above --max-log10 are skipped, because the search cannot finish on them.
"""
from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from eval.checker import ROOT, check_plan, measures

_CATALOG = None


def compare(inst, variant, time_limit):
    global _CATALOG
    from m1_data.catalog import Catalog
    from solver.backtrack import solve_with_stats
    _CATALOG = _CATALOG or Catalog.load()
    spec, gold = inst["gold_spec"], inst["gold_answer"]
    answer, stats = solve_with_stats(spec, _CATALOG, variant, time_limit)
    row = {"id": inst["id"], "kind": inst["kind"], "gold_status": gold["status"], "backtrack_status": answer["status"],
           "seconds": round(stats["seconds"], 2), "nodes": stats["nodes"], "result": "", "detail": ""}
    if stats["timed_out"]:
        row["result"] = "timed out"
        return row
    problems = []
    if answer["status"] != gold["status"]:
        problems.append(f"status {answer['status']} but gold is {gold['status']}")
    elif gold["status"] == "PLAN":
        violations = check_plan(spec, answer["plan"])
        if violations:
            problems.append("its plan breaks " + " | ".join(violations))
        a, b = measures(spec, answer["plan"]), measures(spec, gold["plan"])
        compared = []
        if spec.get("objective") == "earliest_graduation":
            compared.append(("last semester", a["last_semester"], b["last_semester"]))
        elif a["last_semester"] != b["last_semester"]:
            row["detail"] = f"tie-break only: last semester {a['last_semester']} but gold has {b['last_semester']}"
        if spec.get("objective") == "min_total_mc":
            compared.append(("total MC", a["total_mc"], b["total_mc"]))
        compared += [("added courses", len(a["added"]), len(b["added"])),
                     ("preferences met", len(answer["preferences_met"]), len(gold["preferences_met"]))]
        for name, x, y in compared:
            if x != y:
                problems.append(f"{name} {x} but gold has {y}")
    row["result"] = "DIFF" if problems else "agree"
    if problems:
        row["detail"] = "; ".join(problems)
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instances", default=str(ROOT / "instances/instances.json"))
    ap.add_argument("--variant", default="mac", choices=["plain", "mrv", "fc", "mac"])
    ap.add_argument("--time-limit", type=float, default=40)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--max-log10", type=float, default=14, help="skip instances with log10 of the state space above this")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--retry-from", help="CSV of an earlier run: only the instances it marks as timed out are run again")
    ap.add_argument("--out", default=str(ROOT / "results/verify/backtrack.csv"))
    a = ap.parse_args()
    insts = [i for i in json.loads(Path(a.instances).read_text()) if i["gold_answer"]["status"] in ("PLAN", "NO_PLAN")]
    insts = insts[: a.limit] if a.limit else insts
    if a.retry_from:
        with open(a.retry_from, newline="") as fh:
            retry = {r["id"] for r in csv.DictReader(fh) if r["result"] == "timed out"}
        insts = [i for i in insts if i["id"] in retry]
    big = lambda i: i["meta"].get("log10_omega") not in ("", None) and i["meta"]["log10_omega"] > a.max_log10
    started = time.time()
    rows = [{"id": i["id"], "kind": i["kind"], "gold_status": i["gold_answer"]["status"], "backtrack_status": "",
             "seconds": "", "nodes": "", "result": "skipped (state space above limit)", "detail": ""} for i in insts if big(i)]
    insts = [i for i in insts if not big(i)]
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        for n, row in enumerate(ex.map(compare, insts, [a.variant] * len(insts), [a.time_limit] * len(insts)), 1):
            rows.append(row)
            if n % 25 == 0:
                print(f"[{n}/{len(insts)}] {time.time() - started:.0f}s", flush=True)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"\n{len(rows)} instances, variant {a.variant}, limit {a.time_limit}s, {time.time() - started:.0f}s")
    for status in ("PLAN", "NO_PLAN"):
        print(f"gold {status}: {dict(Counter(r['result'] for r in rows if r['gold_status'] == status))}")
    for r in rows:
        if r["result"] == "DIFF":
            print("DIFF", r["id"], r["kind"], r["detail"])
    print(f"written to {out}")


if __name__ == "__main__":
    main()
