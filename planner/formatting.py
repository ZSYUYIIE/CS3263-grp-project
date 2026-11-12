"""Readable views of solver data; no rules, LLM calls or mutations live here.

Every explanation the solver gives (reasons, notes, warnings, preferences, wishes not applied) is
printed verbatim, so nothing the solver says is lost or reworded into a different claim.
"""

import textwrap

WIDTH = 64

OBJECTIVES = {
    "none": "No particular goal",
    "earliest_graduation": "Finish the requested courses as early as possible",
    "min_total_mc": "Take as few total MC as possible",
}

HEADLINES = {
    "ELIGIBLE": "Yes, you can take {target}",
    "NOT_ELIGIBLE": "No, you cannot take {target} yet",
    "NEVER_ELIGIBLE": "No, you cannot take {target}",
    "PLAN": "Here is your plan",
    "NO_PLAN": "No plan fits your request",
    "OUT_OF_SCOPE": "I can't help with this request",
    "INVALID_SPEC": "I couldn't read that request",
    "MISSING_INFO": "I need more information",
}

DISCLAIMER = ("This schedules only the courses you asked for and the prerequisites they need. "
              "It does not check your full graduation requirements.")


def heading(text, char="="):
    rule = char * WIDTH
    return f"\n{rule}\n  {text}\n{rule}"


def wrap(text, first="  ", rest=None):
    """Wrap at word boundaries only, so codes and phrases stay whole."""
    return textwrap.fill(str(text), WIDTH + 4, initial_indent=first, subsequent_indent=rest or first,
                         break_long_words=False, break_on_hyphens=False)


def section(lines, title, items, bullet="-"):
    """A titled list; left out entirely when there is nothing to show."""
    items = list(items)
    if items:
        lines += ["", f"  {title}"] + [wrap(item, f"    {bullet} ", "      ") for item in items]


def semester_label(semester):
    return f"Year {(semester - 1) // 2 + 1} Semester {(semester - 1) % 2 + 1} (semester {semester})"


def courses(codes):
    return ", ".join(codes) if codes else "None"


def field(label, value):
    return f"  {label + ':':<22}{value}"


def summary(spec, cleaned, warnings):
    """Show all effective inputs, including defaults and ignored-field warnings."""
    eligible = cleaned["query"] == "eligible"
    lines = [heading("Here is how I understood your request", "-"),
             field("Task", "Check whether you can take a course" if eligible else "Plan your remaining courses")]
    if "programme" in cleaned:
        lines.append(field("Programme", cleaned["programme"]))
    lines.append(field("Completed courses", courses(cleaned["completed"])))
    if eligible:
        lines.append(field("Course to check", cleaned["target"]))
        label = (semester_label(cleaned["current_sem"]) if "current_sem" in cleaned
                 else "Not specified; see offering notes")
        lines.append(field("Semester to check", label))
    else:
        default = " (default)" if spec.get("objective") is None else ""
        lines += [field("Starting semester", semester_label(cleaned["current_sem"])),
                  field("Courses to take", courses(cleaned["must_take"])),
                  field("Goal", OBJECTIVES[cleaned["objective"]] + default)]
        default = " (default)" if spec.get("mc_max") is None else ""
        limits = [f"Maximum MC per semester: {cleaned['mc_max']}{default}"]
        if "mc_min" in cleaned:
            limits.append(f"Minimum MC in each nonempty semester: {cleaned['mc_min']}")
        for sem, cap in sorted(cleaned["sem_caps"].items()):
            limits.append(f"{semester_label(sem)}: {cap}" + (" (blocked)" if cap == 0 else " MC at most"))
        if "atap_sems" in cleaned:
            limits.append("ATAP allowed in: " + "; ".join(semester_label(s) for s in cleaned["atap_sems"]))
        section(lines, "Limits", limits)
        rules = []
        for rule in cleaned["rules"]:
            if rule["type"] == "in_sem":
                label = f"{rule['course']} in {semester_label(rule['sem'])}"
            else:
                relation = {"before": "before", "apart": "in a different semester from",
                            "same_sem": "in the same semester as"}[rule["type"]]
                label = f"{rule['a']} {relation} {rule['b']}"
            rules.append(f"{'Must' if rule['strength'] == 'must' else 'Prefer'}: {label}")
        if cleaned["early"]:
            rules.append(f"Prefer earlier: {courses(cleaned['early'])}")
        if cleaned["late"]:
            rules.append(f"Prefer later: {courses(cleaned['late'])}")
        section(lines, "Rules and preferences", rules)
    section(lines, "Wishes the solver cannot apply", cleaned["unsupported"])
    section(lines, "Warnings", warnings)
    return "\n".join(lines)


def course_line(code, catalog, added):
    record = catalog[code] if catalog is not None and code in catalog else {}
    details = [f"{record['mc']} MC"] if record.get("mc") is not None else []
    if added:
        details.append("prerequisite")
    title = f"  {record['title']}" if record.get("title") else ""
    return f"    - {code:<9}{title}" + (f"  ({', '.join(details)})" if details else "")


def plan_lines(answer, catalog):
    lines = []
    added = set(answer.get("added_prerequisites", []))
    plan = sorted(answer["plan"].items(), key=lambda item: int(item[0]))
    if not plan:
        return ["", "  You have no remaining courses to schedule."]
    for sem, codes in plan:
        mc = answer["mc_per_semester"][sem]
        lines += ["", f"  {semester_label(int(sem)):<{WIDTH - 10}}{mc:>4} MC"]
        lines += [course_line(code, catalog, code in added) for code in codes] or ["    (no courses)"]
    total = sum(answer["mc_per_semester"].values())
    busy = sum(1 for codes in answer["plan"].values() if codes)
    lines += ["", "  " + "-" * (WIDTH - 2),
              f"  Total: {total} MC over {busy} semester{'s' if busy != 1 else ''}"]
    if answer.get("last_semester") is not None:
        lines.append(f"  Requested courses finish by: {semester_label(answer['last_semester'])}")
    if added:
        lines.append(f"  Added prerequisites: {courses(answer['added_prerequisites'])}")
    return lines


def format_answer(answer, catalog=None):
    """Lead with a plain-language headline, then every solver explanation verbatim."""
    status = answer["status"]
    target = answer.get("target", "")
    title_status = "NEVER_ELIGIBLE" if answer.get("can_still_become_eligible") is False else status
    lines = [heading(HEADLINES.get(title_status, status).format(target=target))]
    if "message" in answer:
        lines += ["", wrap(answer["message"])]
    if status in ("ELIGIBLE", "NOT_ELIGIBLE"):
        record = catalog[target] if catalog is not None and target in catalog else {}
        name = f"{target} {record['title']}" if record.get("title") else target
        when = f" in {semester_label(answer['semester'])}" if "semester" in answer else ""
        lines += ["", field("Course", name)]
        if when:
            lines.append(field("Semester", semester_label(answer["semester"])))
        if "offered_in" in answer:
            lines.append(field("Offered in", " and ".join(f"Semester {s}" for s in answer["offered_in"])))
        if status == "ELIGIBLE":
            lines += ["", wrap(f"You meet the requirements to take {target}{when}.")]
    if status == "PLAN":
        lines += plan_lines(answer, catalog)
    reasons = answer.get("reasons", [])
    if all(reason in answer.get("message", "") for reason in reasons):
        reasons = []   # the refusal message already names them
    section(lines, "Why" if status != "ELIGIBLE" else "Details", reasons)
    section(lines, "Problems found", answer.get("errors", []))
    if answer.get("can_still_become_eligible") is True:
        lines += ["", "  You can still become eligible once you meet the requirements above."]
    if "never_eligible_because" in answer:
        lines += ["", wrap(f"You can never become eligible: {answer['never_eligible_because']}")]
    section(lines, "Preferences met", answer.get("preferences_met", []), "+")
    section(lines, "Preferences not met", answer.get("preferences_not_met", []), "x")
    section(lines, "Notes", answer.get("notes", []))
    section(lines, "Wishes I could not apply", answer.get("not_applied", []))
    section(lines, "Warnings", answer.get("warnings", []))
    if status == "PLAN":
        lines += ["", wrap(DISCLAIMER)]
    elif status == "NO_PLAN":
        lines += ["", "  Try changing a limit or rule and ask again."]
    elif status == "INVALID_SPEC":
        lines += ["", "  Try rephrasing your request."]
    return "\n".join(lines)
