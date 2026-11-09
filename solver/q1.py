"""Q1, "can I take X?": eligibility from the catalogue.

Uses `Catalog.can_take` (prerequisites, exclusions, offering term, availability) and, when the
answer is no, `Catalog.reachable` to say whether the student could ever become eligible.
"""
from __future__ import annotations

from m1_data.catalog import data_limited
from solver.common import term_of


def answer(spec: dict, catalog) -> dict:
    """Q1 answer for a cleaned spec: ELIGIBLE or NOT_ELIGIBLE with reasons."""
    semester = spec.get("current_sem")
    if semester is None:
        return answer_without_semester(spec, catalog)
    ok, reasons = catalog.can_take(spec["target"], spec["completed"], semester=term_of(semester))
    result = {
        "status": "ELIGIBLE" if ok else "NOT_ELIGIBLE",
        "target": spec["target"],
        "semester": semester,
        "reasons": reasons,
    }
    add_reachability(result, spec, catalog, ok)
    return result


def add_reachability(result: dict, spec: dict, catalog, ok: bool) -> None:
    if not ok and spec["target"] not in spec["completed"]:
        reachable, note = catalog.reachable(spec["target"], spec["completed"])
        if not reachable and data_limited([note]):
            # Missing data, not a rule: don't claim the student can never take it.
            result["can_still_become_eligible"] = "unknown"
            result["unknown_because"] = note
        else:
            result["can_still_become_eligible"] = reachable
            if not reachable:
                result["never_eligible_because"] = note
    if data_limited(result.get("reasons")) or data_limited([result.get("unknown_because")]):
        result["data_limited"] = True
    if spec["unsupported"]:
        result["not_applied"] = list(spec["unsupported"])


def answer_without_semester(spec: dict, catalog) -> dict:
    target = spec["target"]
    ok, reasons = catalog.can_take(target, spec["completed"])
    offered_in = [term for term in catalog[target]["offered"] if term in (1, 2)]
    if ok and not offered_in:
        ok = False
        reasons = ["not offered in Semester 1 or Semester 2"]
    result = {
        "status": "ELIGIBLE" if ok else "NOT_ELIGIBLE",
        "target": target,
        "reasons": reasons,
    }
    if ok:
        result["offered_in"] = offered_in
        if len(offered_in) == 2:
            result["notes"] = ["no semester given; the course is offered in both Semester 1 and Semester 2, "
                               "so the term does not matter"]
        else:
            result["notes"] = [f"no semester given; the course is offered in Semester {offered_in[0]} only, "
                               "so it can only be taken in that term"]
    add_reachability(result, spec, catalog, ok)
    return result
