"""The committed instance set matches its kinds: every gold answer has the status its kind promises."""
import json
from pathlib import Path

EXPECTED = {"q1/eligible": "ELIGIBLE", "q2": "PLAN", "q2_infeasible": "NO_PLAN",
            "missing_info": "MISSING_INFO", "out_of_scope": "OUT_OF_SCOPE"}

ROWS = json.loads((Path(__file__).resolve().parent.parent / "instances" / "instances.json").read_text())


def expected_status(kind: str) -> str:
    if kind.startswith("q1/"):
        return "ELIGIBLE" if kind == "q1/eligible" else "NOT_ELIGIBLE"
    return EXPECTED[kind.split("/")[0]]


def test_ids_unique():
    assert len({r["id"] for r in ROWS}) == len(ROWS)


def test_gold_status_matches_kind():
    for r in ROWS:
        assert r["gold_answer"]["status"] == expected_status(r["kind"]), r["id"]


def test_request_mentions_every_must_take_course_and_target():
    for r in ROWS:
        spec = r["gold_spec"]
        for code in spec.get("must_take", []) + ([spec["target"]] if "target" in spec else []):
            assert code in r["request"], (r["id"], code)
        for code in spec.get("completed", []):
            assert code in r["request"], (r["id"], code)
