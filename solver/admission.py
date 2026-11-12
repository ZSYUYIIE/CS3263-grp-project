"""Chance of getting a course you bid for, estimated from CourseReg allocation reports.

`Admission.load()` reads `data/demand/allocation.csv` (one row per report line; written by
`experiments/extract_demand.py`) and gives `p(code, semester)`: the probability that a student who
bids for `code` in that semester ends up with it. docs/MDP_GUIDE.md section 3 explains the estimate
and its limits.

In one registration round, for one course in one academic year (summed over its classes):
    contested = main + quota         students who were allocated or were turned away for lack of places
    unmet     = max(0, quota - reserve)
`quota` counts students turned away from a class because it was full, and `reserve` counts students
given a place from their reserve list. When a course has several classes, a student turned away
from a full class is usually given a place in another class through the reserve list, so only the
difference is counted as failing to get the course. The failure rate of a round is the pooled
`unmet / contested` over the academic years in the file.

Two estimators, used as a pessimistic and an optimistic bound:
    round1      p = 1 - failure rate of round 1 (the student does not try again)
    all_rounds  p = 1 - product of the failure rates of rounds 1 to 3 (the student tries again in
                every round, and the rounds are treated as independent)
A course and term with no rows gets p = 1 (`known()` is False). Probabilities are rounded to three
decimals, so a course with fewer than 1 failure in 2000 is treated as certain.
"""
from __future__ import annotations

import csv
from pathlib import Path

from solver.common import term_of

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "data/demand/allocation.csv"
ESTIMATORS = ("all_rounds", "round1")
DEFAULT_ESTIMATOR = "all_rounds"


def read_rows(path: str | Path | None = None) -> list[dict]:
    with open(path or DEFAULT_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def failure_rates(rows: list[dict]) -> dict[tuple[str, int], dict[int, tuple[int, int]]]:
    """(code, term) -> {round: (unmet, contested)}, pooled over academic years."""
    per_year: dict[tuple, list[int]] = {}
    for row in rows:
        key = (row["code"], int(row["semester"]), int(row["round"]), row["acad_year"])
        total = per_year.setdefault(key, [0, 0, 0])
        total[0] += int(row["main"])
        total[1] += int(row["quota"])
        total[2] += int(row["reserve"])
    pooled: dict[tuple[str, int], dict[int, tuple[int, int]]] = {}
    for (code, term, round_no, _year), (main, quota, reserve) in sorted(per_year.items()):
        rounds = pooled.setdefault((code, term), {})
        unmet, contested = rounds.get(round_no, (0, 0))
        rounds[round_no] = (unmet + max(0, quota - reserve), contested + main + quota)
    return pooled


def estimate(rounds: dict[int, tuple[int, int]], estimator: str) -> float | None:
    """Probability of getting the course from its per-round (unmet, contested); None = no evidence."""
    used = [1] if estimator == "round1" else sorted(rounds)
    fail, seen = 1.0, False
    for round_no in used:
        unmet, contested = rounds.get(round_no, (0, 0))
        if contested:
            fail *= unmet / contested
            seen = True
    return round(1.0 - fail, 3) if seen else None


class Admission:
    """Table of success probabilities by (course, term). Courses not in the table are certain."""

    def __init__(self, table: dict[tuple[str, int], float] | None = None, estimator: str = "given"):
        self.table = dict(table or {})
        self.estimator = estimator

    @classmethod
    def load(cls, estimator: str = DEFAULT_ESTIMATOR, path: str | Path | None = None) -> Admission:
        if estimator not in ESTIMATORS:
            raise ValueError(f"estimator must be one of {list(ESTIMATORS)}, got {estimator!r}")
        table = {}
        for key, rounds in failure_rates(read_rows(path)).items():
            p = estimate(rounds, estimator)
            if p is not None:
                table[key] = p
        return cls(table, estimator)

    @classmethod
    def certain(cls) -> Admission:
        """Every bid succeeds: the assumption the CSP makes."""
        return cls({}, "certain")

    @classmethod
    def from_dict(cls, given: dict) -> Admission:
        """`{"CS4248": 0.6}` (both terms) or `{"CS4248": {"1": 0.7, "2": 0.6}}` (by term)."""
        table = {}
        for code, value in given.items():
            by_term = value if isinstance(value, dict) else {1: value, 2: value}
            for term, p in by_term.items():
                if not 0.0 <= float(p) <= 1.0:
                    raise ValueError(f"probability for {code} must be between 0 and 1, got {p!r}")
                table[(code.strip().upper(), int(term))] = float(p)
        return cls(table)

    def known(self, code: str, semester: int) -> bool:
        return (code, term_of(semester)) in self.table

    def p(self, code: str, semester: int) -> float:
        return self.table.get((code, term_of(semester)), 1.0)
