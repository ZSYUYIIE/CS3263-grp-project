"""Readable views of solver data; no rules, LLM calls or mutations live here."""

OBJECTIVES = {
    "none": "No primary objective",
    "earliest_graduation": "Finish the requested courses as early as possible",
    "min_total_mc": "Minimise total MC",
}


def semester_label(semester):
    return f"Year {(semester - 1) // 2 + 1} Semester {(semester - 1) % 2 + 1} (semester {semester})"


def courses(codes):
    return ", ".join(codes) if codes else "None"


def summary(spec, cleaned, warnings):
    """Show all effective inputs, including defaults and ignored-field warnings."""
    lines = ["\nYour request:"]
    if "programme" in cleaned:
        lines.append(f"Programme: {cleaned['programme']}")
    lines.append(f"Completed courses: {courses(cleaned['completed'])}")
    if cleaned["query"] == "eligible":
        lines.append(f"Check eligibility for: {cleaned['target']}")
        label = (semester_label(cleaned["current_sem"]) if "current_sem" in cleaned
                 else "Not specified; see offering notes")
        lines.append(f"Semester to check: {label}")
    else:
        lines += [f"Starting semester: {semester_label(cleaned['current_sem'])}",
                  f"Required courses: {courses(cleaned['must_take'])}"]
        default = " (default)" if spec.get("mc_max") is None else ""
        lines.append(f"Maximum MC per semester: {cleaned['mc_max']}{default}")
        if "mc_min" in cleaned:
            lines.append(f"Minimum MC in each nonempty semester: {cleaned['mc_min']}")
        for sem, cap in sorted(cleaned["sem_caps"].items()):
            lines.append(f"MC limit in {semester_label(sem)}: {cap}" + (" (blocked)" if cap == 0 else ""))
        if "atap_sems" in cleaned:
            lines.append("ATAP allowed in: " + "; ".join(semester_label(s) for s in cleaned["atap_sems"]))
        default = " (default)" if spec.get("objective") is None else ""
        lines.append(f"Objective: {OBJECTIVES[cleaned['objective']]}{default}")
        lines += [f"Prefer earlier: {courses(cleaned['early'])}", f"Prefer later: {courses(cleaned['late'])}"]
        for rule in cleaned["rules"]:
            if rule["type"] == "in_sem":
                label = f"{rule['course']} in {semester_label(rule['sem'])}"
            else:
                relation = {"before": "before", "apart": "in a different semester from",
                            "same_sem": "in the same semester as"}[rule["type"]]
                label = f"{rule['a']} {relation} {rule['b']}"
            lines.append(f"{'Must' if rule['strength'] == 'must' else 'Prefer'}: {label}")
    for wish in cleaned["unsupported"]:
        lines.append(f"Wish the solver cannot apply: {wish}")
    for warning in warnings:
        lines.append(f"Warning: {warning}")
    return "\n".join(lines)


def format_answer(answer):
    """Keep the status and every solver explanation visible, including timeouts."""
    status = answer["status"]
    lines = [f"\nResult: {status}"]
    if "message" in answer:
        lines.append(answer["message"])
    if status in ("ELIGIBLE", "NOT_ELIGIBLE"):
        lines.append(f"Course: {answer['target']}")
        if "semester" in answer:
            lines.append(f"Semester: {semester_label(answer['semester'])}")
        if "offered_in" in answer:
            lines.append("Offered in: " + ", ".join(f"Semester {s}" for s in answer["offered_in"]))
        if "can_still_become_eligible" in answer:
            lines.append("Can still become eligible: " + ("Yes" if answer["can_still_become_eligible"] else "No"))
        if "never_eligible_because" in answer:
            lines.append(answer["never_eligible_because"])
    if status == "PLAN":
        lines.append("\nSemester                         | Courses | MC")
        for sem, codes in sorted(answer["plan"].items(), key=lambda item: int(item[0])):
            lines.append(f"{semester_label(int(sem)):<32} | {courses(codes)} | {answer['mc_per_semester'][sem]}")
        if not answer["plan"]:
            lines.append("No remaining courses to schedule.")
        if answer.get("last_semester") is not None:
            lines.append(f"Requested courses finish by: {semester_label(answer['last_semester'])}")
        if answer.get("added_prerequisites"):
            lines.append(f"Added prerequisites: {courses(answer['added_prerequisites'])}")
        lines.append("This schedules the requested courses and prerequisites; "
                     "it does not verify all graduation requirements.")
    for key, label in (("reasons", "Reason"), ("errors", "Error"), ("notes", "Note"), ("warnings", "Warning"),
                       ("not_applied", "Wish not applied"), ("preferences_met", "Preference met"),
                       ("preferences_not_met", "Preference not met")):
        for item in answer.get(key, []):
            lines.append(f"{label}: {item}")
    return "\n".join(lines)
