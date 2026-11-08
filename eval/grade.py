"""Grade one pipeline's answers against the gold answers and write result tables.

    python -m eval.grade results/A/qwen3-max          # writes graded.csv and SUMMARY.md in that folder

Per instance: status correct?  For gold PLAN: valid?  optimality class (invalid / objective gap / extra
courses / preference gap / optimal, SOLVER_GUIDE section 6).  For gold NO_PLAN: invented plan?
For gold PLAN answered NO_PLAN: over-refusal.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from eval.checker import check_plan, measures, preference_bounds

ROOT = Path(__file__).resolve().parent.parent


def grade_one(inst, rec):
    gold = inst["gold_answer"]
    spec = inst["gold_spec"]
    ans = rec.get("answer") if rec else None
    status = (ans or {}).get("status", "UNPARSEABLE") if isinstance(ans, dict) else "UNPARSEABLE"
    row = {"id": inst["id"], "kind": inst["kind"], "group": inst["kind"].split("/")[0],
           "gold_status": gold["status"], "status": status, "status_correct": status == gold["status"],
           "fenced": bool(rec and rec.get("fenced")), "violations": "", "class": "",
           "api_error": rec.get("api_error", "") if rec else "", "unverified_preferences": ""}
    if gold["status"] == "PLAN":
        if status == "PLAN":
            v = check_plan(spec, ans.get("plan"))
            row["violations"] = " | ".join(v)
            if v:
                row["class"] = "invalid"
            else:
                m, g = measures(spec, ans.get("plan")), measures(spec, gold["plan"])
                obj = spec.get("objective", "none")
                worse = (obj == "earliest_graduation" and m["last_semester"] > g["last_semester"]) or \
                        (obj == "min_total_mc" and m["total_mc"] > g["total_mc"])
                better = (obj == "earliest_graduation" and m["last_semester"] < g["last_semester"]) or \
                         (obj == "min_total_mc" and m["total_mc"] < g["total_mc"])
                p, upper, unknown = preference_bounds(spec, ans.get("plan"), gold)
                row["unverified_preferences"] = " | ".join(unknown)
                gp = len(gold.get("preferences_met", []))
                row["class"] = ("BEATS GOLD: check" if better else "objective gap" if worse
                                else "extra courses" if len(m["added"]) > len(g["added"])
                                else "preference gap" if upper < gp
                                else "preference unverified" if p < gp else "optimal")
        elif status == "NO_PLAN":
            row["class"] = "over-refusal"
        else:
            row["class"] = "wrong status"
    elif gold["status"] == "NO_PLAN":
        row["class"] = "invented plan" if status == "PLAN" else "correct refusal" if status == "NO_PLAN" \
            else "wrong status"
    return row


def pct(n, d):
    return f"{100 * n / d:.0f}% ({n}/{d})" if d else "-"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results_dir")
    ap.add_argument("--instances", default=str(ROOT / "instances/instances.json"))
    a = ap.parse_args()
    out = Path(a.results_dir)
    insts = json.loads(Path(a.instances).read_text())
    rows, usage = [], Counter()
    for inst in insts:
        f = out / f"{inst['id']}.json"
        if not f.exists():
            continue
        rec = json.loads(f.read_text())
        for k_, v_ in (rec.get("usage") or {}).items():
            if isinstance(v_, int):
                usage[k_] += v_
        rows.append(grade_one(inst, rec))
    if not rows:
        raise SystemExit(f"no answers in {out}")
    with open(out / "graded.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    by = defaultdict(list)
    for r in rows:
        by[r["group"]].append(r)
    L = [f"# Results: {out}", "", f"{len(rows)} of {len(insts)} instances recorded.", "",
         "## Status accuracy by group", "", "| Group | Correct status |", "|---|---|"]
    L += [f"| {g} | {pct(sum(r['status_correct'] for r in rs), len(rs))} |" for g, rs in sorted(by.items())]
    L += [f"| **all** | {pct(sum(r['status_correct'] for r in rows), len(rows))} |"]
    feas = [r for r in rows if r["gold_status"] == "PLAN"]
    L += ["", "## Feasible plan requests (gold = PLAN)", "", "| Class | Count |", "|---|---|"]
    L += [f"| {c} | {pct(n, len(feas))} |" for c, n in Counter(r["class"] for r in feas).most_common()]
    for sub in ("q2/loose", "q2/tight"):
        rs = [r for r in feas if r["kind"] == sub]
        valid = sum(r["class"] not in ("invalid", "over-refusal", "wrong status") for r in rs)
        L += [f"\n{sub}: valid {pct(valid, len(rs))}, optimal {pct(sum(r['class'] == 'optimal' for r in rs), len(rs))}"]
    rules = Counter(v.split()[0] for r in feas for v in r["violations"].split(" | ") if v)
    if rules:
        L += ["", "Hard rules broken in invalid plans (R numbers = SOLVER_GUIDE section 4):", ""]
        L += [f"- {k}: {n}" for k, n in rules.most_common()]
    inf = [r for r in rows if r["gold_status"] == "NO_PLAN"]
    L += ["", "## Impossible requests (gold = NO_PLAN)", "",
          "| Kind | Correct refusal | Invented plan |", "|---|---|---|"]
    for kind in sorted({r["kind"] for r in inf}):
        rs = [r for r in inf if r["kind"] == kind]
        L += [f"| {kind} | {pct(sum(r['class'] == 'correct refusal' for r in rs), len(rs))} |"
              f" {pct(sum(r['class'] == 'invented plan' for r in rs), len(rs))} |"]
    L += ["", "## Format", "", f"- unparseable replies: {sum(r['status'] == 'UNPARSEABLE' for r in rows)}",
          f"- API/completion errors without an answer: {sum(bool(r['api_error']) for r in rows)}",
          f"- replies wrapped in fences or extra text: {sum(r['fenced'] for r in rows)}"]
    if usage:
        L += [f"- token usage: {dict(usage)}"]
    (out / "SUMMARY.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
