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
