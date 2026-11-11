"""The independent checker accepts every gold plan and catches basic rule breaks."""
import json
from pathlib import Path

from eval.checker import check_plan
from eval.grade import grade_one

ROWS = json.loads((Path(__file__).resolve().parent.parent / "instances" / "instances.json").read_text())
PLANS = [r for r in ROWS if r["gold_answer"]["status"] == "PLAN"]


def test_gold_plans_are_valid():
    for r in PLANS:
        assert check_plan(r["gold_spec"], r["gold_answer"]["plan"]) == [], r["id"]


def test_gold_answers_grade_as_optimal():
    for r in ROWS:
        row = grade_one(r, {"answer": r["gold_answer"]})
        assert row["status_correct"], r["id"]
        if r["gold_answer"]["status"] == "PLAN":
            assert row["class"] == "optimal", (r["id"], row)


def test_catches_prereq_offering_padding_and_missing():
    spec = {"query": "plan", "current_sem": 5, "completed": ["CS1101S", "CS1231S", "CS2030S", "CS2040S",
            "MA1521", "MA1522", "ST2334"], "must_take": ["CS3263", "CS3243"]}
    v = check_plan(spec, {"5": ["CS3263", "CS3243", "CS4248"]})
    text = " ".join(v)
    assert "R4 CS3263" in text          # CS2109S not done
    assert "R3 CS3243" in text          # Sem 2 only, semester 5 is Sem 1
    assert "R10 CS4248" in text         # padding
    assert "R6" in text                 # CS3263 and CS3243 exclude each other
    assert "R1 must-take" in " ".join(check_plan(spec, {"6": ["CS3243"]}))


def test_badly_shaped_plan_is_invalid_not_a_crash():
    """Whatever shape an LLM gives the plan, grading goes on: the answer is classed invalid."""
    inst = next(r for r in PLANS)
    for plan in ([["CS3219"]], {"Y3S1": ["CS3219"]}, {"5": "CS3219"}, {"5": {"courses": ["CS3219"]}}, {"5": [3219]},
                 "CS3219 in semester 5"):
        violations = check_plan(inst["gold_spec"], plan)
        assert len(violations) == 1 and violations[0].startswith("format: "), plan
        row = grade_one(inst, {"answer": {"status": "PLAN", "plan": plan}})
        assert row["class"] == "invalid", plan


ATAP_SPEC = {"query": "plan", "current_sem": 5, "must_take": ["CS3263", "CS2105"], "atap_sems": [6],
             "completed": ["CS1101S", "CS1231S", "CS2030S", "CS2040S", "MA1521", "MA1522", "ST2334", "CS2100",
                           "CS2103T", "CS2101", "CS2109S", "CS2106", "CS3230", "ES2660", "IS1108"]}


def test_solver_atap_plan_is_valid_and_grades_as_optimal():
    """ATAP asked for with atap_sems is not an "added" course (rule 10), so the solver's own plan must pass."""
    from solver.run import run
    gold = run(ATAP_SPEC)
    assert gold["status"] == "PLAN" and "CP3880" in gold["plan"]["6"]
    assert check_plan(ATAP_SPEC, gold["plan"]) == []
    inst = {"id": "atap", "kind": "q2/loose", "gold_spec": ATAP_SPEC, "gold_answer": gold}
    assert grade_one(inst, {"answer": gold})["class"] == "optimal"
    # asking through must_take instead of atap_sems was already accepted, and still is
    by_must_take = {**ATAP_SPEC, "must_take": ["CS3263", "CS2105", "CP3880"]}
    del by_must_take["atap_sems"]
    assert check_plan(by_must_take, {"5": ["CP3880"], "6": ["CS3263", "CS2105"]}) == []


def test_catches_each_atap_rule_break():
    def broken(plan, spec=ATAP_SPEC):
        return " | ".join(check_plan(spec, plan))
    assert "R11 ATAP (CP3880) was asked for but is not planned" in broken({"5": ["CS3263", "CS2105"]})
    assert "R11 CP3880 in semester 5, allowed semesters [6]" in broken({"5": ["CP3880"], "6": ["CS3263", "CS2105"]})
    assert "R11 CP3880 is in the last semester used" in broken({"5": ["CS3263", "CS2105"], "6": ["CP3880"]})
    three_beside = {**ATAP_SPEC, "must_take": ["CS3263", "CS2105", "CS2102"]}
    text = broken({"6": ["CP3880", "CS3263", "CS2105", "CS2102"], "7": []}, three_beside)
    assert "R11 semester 6 has 12 MC beside ATAP, limit 8" in text
    # ATAP nobody asked for is still an added course that nothing needs
    no_atap = {k: v for k, v in ATAP_SPEC.items() if k != "atap_sems"}
    assert "R10 CP3880" in broken({"5": ["CP3880"], "6": ["CS3263", "CS2105"]}, no_atap)
