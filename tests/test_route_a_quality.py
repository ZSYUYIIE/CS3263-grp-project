"""Regressions for truncated completions, factual claims and malformed plans."""
import copy
import csv
import json
import sys

import pytest

from eval.checker import C, check_plan, eligibility_checks, infeasibility_certificates, preference_bounds
from eval.grade import grade_one
from eval.quality import audit_one
from eval.quality import main as quality_main
from pipelines.output import validate_answer
from pipelines.run_a import ROOT, answer_record, main

INSTANCES = json.loads((ROOT / "instances/instances.json").read_text())


def test_budget_retry_keeps_both_attempts_and_never_changes_messages(monkeypatch):
    calls = []

    def fake(messages, model, base, key, cap, timeout):
        calls.append((copy.deepcopy(messages), cap))
        if len(calls) == 1:
            return {"raw": None, "usage": {"prompt_tokens": 50, "completion_tokens": 100}, "finish_reason": "length"}
        return {"raw": '{"status":"NO_PLAN","reasons":["Conflicting requirements."]}',
                "usage": {"prompt_tokens": 50, "completion_tokens": 180}, "finish_reason": "stop"}

    monkeypatch.setattr("pipelines.run_a.completion", fake)
    rec = answer_record(INSTANCES[0], "test-model", "test-url", "test-secret", 100, retry_max_tokens=200)
    assert [cap for _, cap in calls] == [100, 200]
    assert calls[0][0] == calls[1][0]
    assert len(rec["attempts"]) == 2 and rec["budget_retried"]
    assert rec["usage"] == {"prompt_tokens": 100, "completion_tokens": 280}
    assert rec["attempts"][0]["raw"] is None and rec["answer"]["status"] == "NO_PLAN"


def test_wrong_or_malformed_answer_is_not_retried_to_improve_its_grade(monkeypatch):
    calls = []

    def fake(*args):
        calls.append(args)
        return {"raw": '{"answer":{"status":"NO_PLAN"}}', "usage": {}, "finish_reason": "stop"}

    monkeypatch.setattr("pipelines.run_a.completion", fake)
    rec = answer_record(INSTANCES[0], "test-model", "test-url", "test-secret", 100, retry_max_tokens=200)
    assert len(calls) == 1 and not rec["format_valid"]


def test_budget_exhaustion_has_only_one_escalation(monkeypatch):
    caps = []

    def fake(messages, model, base, key, cap, timeout):
        caps.append(cap)
        return {"raw": None, "usage": {"completion_tokens": cap}, "finish_reason": "length"}

    monkeypatch.setattr("pipelines.run_a.completion", fake)
    rec = answer_record(INSTANCES[0], "test-model", "test-url", "test-secret", 100, retry_max_tokens=200)
    assert caps == [100, 200]
    assert rec["budget_exhausted"] and rec["api_error"] and rec["answer"] is None
    assert rec["usage"]["completion_tokens"] == 300


def test_eligibility_is_independent_of_gold_and_matches_all_q1_references():
    for inst in INSTANCES:
        if inst["gold_answer"]["status"] in ("ELIGIBLE", "NOT_ELIGIBLE"):
            expected = "ELIGIBLE" if all(eligibility_checks(inst["gold_spec"]).values()) else "NOT_ELIGIBLE"
            assert expected == inst["gold_answer"]["status"], inst["id"]


def test_correct_status_with_false_supporting_claim_fails_quality():
    inst = next(i for i in INSTANCES if i["id"] == "q1-eligible-01")
    checks = eligibility_checks(inst["gold_spec"])
    checks["prerequisites_met"] = False
    record = {"prompt_version": "route-a-v2", "answer": {
        "status": "ELIGIBLE", "reasons": ["Prerequisites are not met."], "eligibility_checks": checks}}
    audit = audit_one(inst, record)
    assert audit["status_correct"] and audit["quality_errors"]
    assert not audit["eligibility_claims_verified"]


@pytest.mark.parametrize("plan", [None, [], {"5": {"status": "PLAN"}}, {"5": "CS1101S"}, {"Y2S1": []}])
def test_malformed_plan_is_a_failure_instead_of_a_checker_crash(plan):
    assert check_plan({"current_sem": 3, "completed": [], "must_take": []}, plan)


def test_completed_inverse_preclusion_is_checked(monkeypatch):
    course = copy.deepcopy(C["CS2109S"])
    course["prereq"]["logic"] = None
    course["preclusion"]["blocked_if"] = None
    course["preclusion"]["mutually_exclusive_with"] = ["CS3244"]
    monkeypatch.setitem(C, "TEST1000", course)
    spec = {"current_sem": 5, "completed": ["CS3244"], "must_take": ["TEST1000"]}
    assert any("R6 TEST1000 excludes completed CS3244" in error for error in check_plan(spec, {"5": ["TEST1000"]}))


def test_schema_rejects_wrappers_and_false_missing_field_names():
    assert validate_answer({"plan": {"status": "PLAN", "plan": {}}})
    assert validate_answer({"status": "MISSING_INFO", "reasons": ["Unknown."], "missing_fields": ["made_up"]})


def test_resume_rejects_changed_prompt_or_budget_without_touching_results(tmp_path, monkeypatch):
    out = tmp_path / "results"
    args = ["run_a", "--mock", "gold", "--limit", "1", "--workers", "1", "--out", str(out),
            "--max-tokens", "100", "--retry-max-tokens", "200"]
    monkeypatch.setattr(sys, "argv", args)
    main()
    original = (out / (INSTANCES[0]["id"] + ".json")).read_bytes()
    monkeypatch.setattr(sys, "argv", args[:-3] + ["101", "--retry-max-tokens", "200"])
    with pytest.raises(SystemExit, match="configuration differs"):
        main()
    assert (out / (INSTANCES[0]["id"] + ".json")).read_bytes() == original


def test_quality_report_adds_new_cases_without_erasing_prose_review(tmp_path, monkeypatch):
    instances_path = tmp_path / "instances.json"
    instances_path.write_text(json.dumps(INSTANCES[:2]))
    first, second = INSTANCES[:2]
    (tmp_path / f"{first['id']}.json").write_text(json.dumps({"answer": first["gold_answer"]}))
    monkeypatch.setattr(sys, "argv", ["quality", str(tmp_path), "--instances", str(instances_path)])
    quality_main()
    path = tmp_path / "explanation_review.csv"
    with path.open(encoding="utf-8", newline="") as stream:
        entries = list(csv.DictReader(stream))
    entries[0].update(explanation_review="assistant_issue", review_notes="A separately reviewed factual issue.")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(entries[0]))
        writer.writeheader()
        writer.writerows(entries)
    (tmp_path / f"{second['id']}.json").write_text(json.dumps({"answer": second["gold_answer"]}))
    quality_main()
    with path.open(encoding="utf-8", newline="") as stream:
        entries = list(csv.DictReader(stream))
    assert len(entries) == 2
    assert entries[0]["explanation_review"] == "assistant_issue"
    assert entries[0]["review_notes"] == "A separately reviewed factual issue."
    assert entries[1]["explanation_review"] == "pending"
    entries[0].update(explanation_review="assistant_note", review_notes="Optional wording; the decision was correct.")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(entries[0]))
        writer.writeheader()
        writer.writerows(entries)
    quality_main()
    summary = json.loads((tmp_path / "quality.json").read_text())["summary"]
    assert summary["assistant_review_notes"] == 1
    assert summary["assistant_review_issues"] == 0
    assert summary["status_correct"] == 2


def test_infeasibility_certificates_cover_refusals_and_never_reject_gold_plans():
    for inst in INSTANCES:
        if inst["gold_answer"]["status"] == "NO_PLAN":
            assert infeasibility_certificates(inst["gold_spec"]), inst["id"]
        elif inst["gold_answer"]["status"] == "PLAN":
            assert not infeasibility_certificates(inst["gold_spec"]), inst["id"]


def test_missed_gold_preference_does_not_certify_a_bad_relative_bound():
    inst = next(i for i in INSTANCES if i["id"] == "q2-loose-25")
    plan = {"3": ["CS2102", "CS2107"], "4": ["CS2103DE", "CS3223"], "5": ["CS3219", "CS4236"],
            "6": ["ST2334", "CS2109S"], "7": ["CS3268", "CS2105", "CS2101"], "8": ["CS4221"]}
    assert not check_plan(inst["gold_spec"], plan)
    assert grade_one(inst, {"answer": {"status": "PLAN", "plan": plan}})["class"] == "preference unverified"
    witness = {"3": ["CS2103T", "CS2102"], "4": ["CS3219", "CS2107"], "5": ["CS3223", "CS4236"],
               "6": ["ST2334", "CS2109S"], "7": ["CS3268", "CS2105"], "8": ["CS4221", "CS2101"]}
    lower, upper, unknown = preference_bounds(inst["gold_spec"], plan, inst["gold_answer"], [witness])
    assert lower == upper == 1 and not unknown
    assert preference_bounds(inst["gold_spec"], plan, inst["gold_answer"], [{}])[2]


def test_higher_grade_conditions_remain_visible_as_unverified_scope():
    inst = next(i for i in INSTANCES if i["id"] == "q2-loose-03")
    audit = audit_one(inst, {"answer": inst["gold_answer"]})
    assert any("A-" in warning for warning in audit["scope_warnings"])
