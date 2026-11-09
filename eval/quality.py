"""Offline Route A quality audit: facts and plans are checked independently of generation.

python -m eval.quality RESULTS_DIR
No model calls, answer repair, or solver imports. Free-text explanations need separate review.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from eval.checker import C, eligibility_checks, infeasibility_certificates, measures, preference_bounds
from eval.grade import ROOT, grade_one
from pipelines.output import validate_answer


def higher_grade_clauses(node):
    if not isinstance(node, dict):
        return []
    if node.get("op") == "course":
        grade = node.get("min_grade", "D")
        return [f"{node['code']} >= {grade}"] if grade != "D" else []
    return [clause for child in node.get("args", []) for clause in higher_grade_clauses(child)]


def audit_one(instance, record, witnesses=()):
    grade = grade_one(instance, record)
    answer = record.get("answer")
    spec = instance["gold_spec"]
    errors = [] if grade["status_correct"] else [f"status {grade['status']} differs from {grade['gold_status']}"]
    expected_checks = None
    expected_missing = None
    checks_verified = False
    certificates = []
    shape = validate_answer(answer, require_evidence=record.get("prompt_version") == "route-a-v2")
    if isinstance(answer, dict):
        if answer.get("status") == "NO_PLAN" and spec.get("query") == "plan" and "current_sem" in spec:
            certificates = infeasibility_certificates(spec)
            if certificates and grade["gold_status"] == "PLAN":
                errors.append("REFERENCE_DISAGREEMENT: an independent infeasibility certificate contradicts gold")
        if grade["gold_status"] in ("ELIGIBLE", "NOT_ELIGIBLE") and spec.get("target") in C:
            expected_checks = eligibility_checks(spec)
            independently_eligible = all(expected_checks.values())
            expected_status = "ELIGIBLE" if independently_eligible else "NOT_ELIGIBLE"
            if instance["gold_answer"]["status"] != expected_status:
                errors.append("REFERENCE_DISAGREEMENT: independent Q1 check differs from gold")
            claimed = answer.get("eligibility_checks")
            if isinstance(claimed, dict):
                claim_errors = []
                for key, expected in expected_checks.items():
                    if type(claimed.get(key)) is not bool or claimed[key] != expected:
                        claim_errors.append(f"eligibility_checks.{key}: expected {expected}, got {claimed.get(key)!r}")
                errors.extend(claim_errors)
                checks_verified = not claim_errors
            elif record.get("prompt_version") == "route-a-v2":
                errors.append("missing verifiable eligibility_checks")
        if grade["gold_status"] == "MISSING_INFO":
            mandatory = ("completed", "target") if spec["query"] == "eligible" else (
                "completed", "current_sem", "must_take")
            expected_missing = [f for f in mandatory if f not in spec]
            claimed = answer.get("missing_fields")
            if (not isinstance(claimed, list) or any(not isinstance(f, str) for f in claimed) or
                    set(claimed) != set(expected_missing)):
                errors.append(f"missing_fields: expected {expected_missing!r}, got {claimed!r}")
    if grade["violations"]:
        errors.extend(grade["violations"].split(" | "))
    facts = None
    grade_warnings = []
    if grade["gold_status"] == "PLAN" and isinstance(answer, dict) and answer.get("status") == "PLAN":
        if not grade["violations"]:
            facts = measures(spec, answer["plan"])
            lower, upper, unknown = preference_bounds(spec, answer["plan"], instance["gold_answer"], witnesses)
            if upper < len(instance["gold_answer"].get("preferences_met", [])):
                errors.append("verified preference gap: an independently valid witness disproves a relative optimum")
    courses = set(facts["added"]) if facts else set()
    if facts:
        courses |= {c for codes in answer["plan"].values() for c in codes}
    if expected_checks is not None:
        courses.add(spec["target"])
    for code in sorted(courses):
        clauses = higher_grade_clauses(C[code]["prereq"].get("logic"))
        if clauses:
            grade_warnings.append(f"{code}: higher-grade clauses are not checked by the completion-only benchmark: "
                                  + "; ".join(clauses))
    return dict(grade, format_valid=not shape and not record.get("fenced") and not record.get("budget_exhausted"),
                schema_errors=shape, quality_errors=errors, eligibility_expected=expected_checks,
                eligibility_claims_verified=checks_verified, missing_fields_expected=expected_missing,
                plan_measures=facts, scope_warnings=grade_warnings,
                infeasibility_certificates=certificates,
                budget_exhausted=bool(record.get("budget_exhausted")),
                budget_retried=bool(record.get("budget_retried")),
                explanation_review="pending: automated facts do not verify every prose assertion")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("results_dir", type=Path)
    ap.add_argument("--instances", type=Path, default=ROOT / "instances/instances.json")
    args = ap.parse_args()
    rows, review = [], []
    witness_path = args.results_dir / "preference_witnesses.json"
    witnesses = json.loads(witness_path.read_text()) if witness_path.exists() else {}
    for instance in json.loads(args.instances.read_text(encoding="utf-8")):
        path = args.results_dir / f"{instance['id']}.json"
        if not path.exists():
            continue
        record = json.loads(path.read_text(encoding="utf-8"))
        row = audit_one(instance, record, [w["plan"] for w in witnesses.get(instance["id"], [])])
        rows.append(row)
        review.append({"id": instance["id"], "kind": instance["kind"], "request": instance["request"],
                       "answer": json.dumps(record.get("answer"), ensure_ascii=False),
                       "reference": json.dumps(instance["gold_answer"], ensure_ascii=False),
                       "quality_errors": " | ".join(row["quality_errors"]),
                       "explanation_review": "pending", "review_notes": ""})
    if not rows:
        raise SystemExit("no recorded cases to audit")
    summary = {"recorded": len(rows), "status_correct": sum(r["status_correct"] for r in rows),
               "format_valid": sum(r["format_valid"] for r in rows),
               "api_errors": sum(bool(r["api_error"]) for r in rows),
               "budget_exhausted": sum(r["budget_exhausted"] for r in rows),
               "budget_retried": sum(r["budget_retried"] for r in rows),
               "eligibility_cases": sum(r["gold_status"] in ("ELIGIBLE", "NOT_ELIGIBLE") for r in rows),
               "eligibility_claims_verified": sum(r["eligibility_claims_verified"] for r in rows),
               "quality_errors": sum(bool(r["quality_errors"]) for r in rows),
               "cases_with_unverified_grade_clauses": sum(bool(r["scope_warnings"]) for r in rows),
               "optimal_plans": sum(r["class"] == "optimal" for r in rows),
               "witness_verified_preference_gaps": sum(any("verified preference gap" in e
                                                           for e in r["quality_errors"]) for r in rows),
               "invalid_plans": sum(r["class"] == "invalid" for r in rows)}
    summary["independently_certified_refusals"] = sum(bool(r["infeasibility_certificates"]) for r in rows)
    review_path = args.results_dir / "explanation_review.csv"
    existing = {}
    if review_path.exists():
        with review_path.open(encoding="utf-8", newline="") as stream:
            existing = {r["id"]: r for r in csv.DictReader(stream)}
    for entry in review:
        if entry["id"] in existing and existing[entry["id"]].get("answer") == entry["answer"]:
            for field in ("explanation_review", "review_notes"):
                entry[field] = existing[entry["id"]].get(field, entry[field])
    with review_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(review[0]))
        writer.writeheader()
        writer.writerows(review)
    reviewed = {r["id"]: r for r in review}
    for row in rows:
        row["explanation_review"] = reviewed[row["id"]]["explanation_review"]
        row["review_notes"] = reviewed[row["id"]]["review_notes"]
    summary.update({"assistant_review_pass": sum(r["explanation_review"] == "assistant_pass" for r in review),
                    "assistant_review_issues": sum(r["explanation_review"] == "assistant_issue" for r in review),
                    "assistant_review_notes": sum(r["explanation_review"] == "assistant_note" for r in review),
                    "explanations_pending_review": sum(r["explanation_review"] == "pending" for r in review)})
    (args.results_dir / "quality.json").write_text(json.dumps({"summary": summary, "cases": rows}, indent=2))
    lines = ["# Route A answer quality", "", "| Check | Count |", "|---|---:|"]
    lines += [f"| {name.replace('_', ' ')} | {count} |" for name, count in summary.items()]
    lines += ["", "Modelled plan constraints and Q1 boolean claims are checked from AY2026/27 catalogue data.",
              "Optimality is measured against the saved gold reference; this audit does not call a solver.",
              "A relative preference is not certified from a reference plan that itself missed that preference.",
              "Independently valid offline witness plans can disprove a preference claim; they never enter generation.",
              "Higher-than-pass grade clauses are reported as scope warnings: transcripts contain no grades,",
              "and the benchmark's completion-only semantics do not establish real-world grade eligibility.",
              "Correct refusal statuses do not by themselves prove that the written explanation is sound.",
              "Free-text claims need separate review in explanation_review.csv. Existing review entries are preserved."]
    issues = [r for r in rows if r["explanation_review"] == "assistant_issue"]
    if issues:
        lines += ["", "## Assisted review: issues needing attention", "",
                  "These notes preserve the original LLM replies. Status scores are not prose-correctness scores.", ""]
        lines += [f"- **{r['id']}**: {r['review_notes']}" for r in issues]
    notes = [r for r in rows if r["explanation_review"] == "assistant_note"]
    if notes:
        lines += ["", "## Optional wording notes", "",
                  "These are not incorrect decisions or scope-recognition failures.", ""]
        lines += [f"- **{r['id']}**: {r['review_notes']}" for r in notes]
    warnings = [r["id"] for r in rows if r["scope_warnings"]]
    if warnings:
        lines += ["", "## Completion-only modelling limit", "",
                  "Higher-than-pass grade clauses remain unverified in: " + ", ".join(warnings) + ".",
                  "These cases involve CS3233's A- prerequisites. Validity here is conditional on the benchmark's",
                  "completion-only simplification; it does not certify those grades for a real student."]
    (args.results_dir / "QUALITY.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
