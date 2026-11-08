"""Structural output contract; contains no course facts or solved answers."""
import re

STATUSES = {"ELIGIBLE", "NOT_ELIGIBLE", "PLAN", "NO_PLAN", "MISSING_INFO", "OUT_OF_SCOPE"}
CHECKS = {"not_completed", "open_to_programme", "prerequisites_met", "no_preclusions", "offered_in_term"}
FIELDS = {"status", "reasons", "plan", "eligibility_checks", "missing_fields", "not_applied"}
MANDATORY_FIELDS = {"completed", "target", "current_sem", "must_take"}


def plan_shape_errors(plan):
    if not isinstance(plan, dict):
        return ["plan must be an object mapping semesters to course lists"]
    errors = []
    for semester, courses in plan.items():
        if not isinstance(semester, str) or semester not in {str(n) for n in range(1, 9)}:
            errors.append(f"invalid semester key: {semester!r}")
        if not isinstance(courses, list) or any(not isinstance(c, str) or
                                               not re.fullmatch(r"[A-Z]{2,4}\d{4}[A-Z]{0,3}", c)
                                               for c in courses):
            errors.append(f"semester {semester}: expected a list of course codes")
    return errors


def validate_answer(answer, require_evidence=True):
    if not isinstance(answer, dict):
        return ["answer must be a top-level JSON object"]
    errors = []
    status = answer.get("status")
    if not isinstance(status, str) or status not in STATUSES:
        errors.append("missing or invalid top-level status")
    reasons = answer.get("reasons")
    if not isinstance(reasons, list) or not reasons or any(not isinstance(r, str) or not r.strip() for r in reasons):
        errors.append("reasons must be a nonempty list of nonempty strings")
    if set(answer) - FIELDS:
        errors.append("unexpected top-level fields: " + ", ".join(sorted(set(answer) - FIELDS)))
    if status == "PLAN":
        errors.extend(plan_shape_errors(answer.get("plan")))
    elif "plan" in answer:
        errors.append("plan is allowed only with status PLAN")
    if status in ("ELIGIBLE", "NOT_ELIGIBLE"):
        checks = answer.get("eligibility_checks")
        if require_evidence or checks is not None:
            if (not isinstance(checks, dict) or set(checks) != CHECKS or
                    any(type(v) is not bool for v in checks.values())):
                errors.append("eligibility_checks must contain exactly the five named boolean checks")
    elif "eligibility_checks" in answer:
        errors.append("eligibility_checks is allowed only for eligibility decisions")
    if status == "MISSING_INFO":
        missing = answer.get("missing_fields")
        if require_evidence or missing is not None:
            if not isinstance(missing, list) or not missing or any(
                not isinstance(f, str) or f not in MANDATORY_FIELDS for f in missing
            ):
                errors.append("missing_fields must list missing mandatory field names")
    elif "missing_fields" in answer:
        errors.append("missing_fields is allowed only with status MISSING_INFO")
    if "not_applied" in answer and (not isinstance(answer["not_applied"], list) or
                                    any(not isinstance(x, str) for x in answer["not_applied"])):
        errors.append("not_applied must be a list of strings")
    return errors
