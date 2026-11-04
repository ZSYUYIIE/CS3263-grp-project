"""Constants and small helpers shared by the solver modules.

Both solvers use these: the CP-SAT model (`model.py`, `objectives.py`) and the
hand-written backtracking search (`backtrack.py`). Sharing them here does not
couple the two searches, which stay independent of each other.
"""
from __future__ import annotations

from m1_data.catalog import satisfied

LAST_SEM = 8                 # semesters are numbered 1..8; odd = Sem 1, even = Sem 2
ATAP_CODE = "CP3880"         # ATAP internship, 12 MC
ATAP_OTHER_CAP = 8           # max MC of other courses in the ATAP semester

GENERIC_REASON = ("no plan satisfies all the rules together (prerequisite order, offering terms, "
                  "MC caps, exclusions and your must-rules conflict)")


def term_of(semester: int) -> int:
    """Teaching term of a semester number: odd -> 1 (Sem 1), even -> 2 (Sem 2)."""
    return 1 if semester % 2 == 1 else 2


def unmet_codes(node, done: set, found: set) -> None:
    """Add to `found` every course in `node` that still matters because the
    (sub)tree is not yet satisfied by the completed courses `done`."""
    if node is None or node is True or node is False:
        return
    if satisfied(node, done):
        return
    if node["op"] == "course":
        found.add(node["code"])
        return
    for arg in node["args"]:
        unmet_codes(arg, done, found)


def tree_leaves(node, found: set) -> None:
    """Add every course code that appears anywhere in a logic tree to `found`."""
    if node is None or node is True or node is False:
        return
    if node["op"] == "course":
        found.add(node["code"])
        return
    for arg in node["args"]:
        tree_leaves(arg, found)


def rule_courses(rule: dict) -> list[str]:
    """Courses a student rule talks about: one for `in_sem`, two otherwise."""
    if rule["type"] == "in_sem":
        return [rule["course"]]
    return [rule["a"], rule["b"]]
