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
    "ALREADY_COMPLETED": "You have already completed {target}",
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


def format_answer(answer, catalog=None, completed=()):
    """Lead with a plain-language headline, then every solver explanation verbatim.

    `completed` is the student's cleaned transcript; it only picks the headline for a course already taken."""
    status = answer["status"]
    target = answer.get("target", "")
    if status == "NOT_ELIGIBLE" and target in completed:
        title_status = "ALREADY_COMPLETED"
    elif answer.get("can_still_become_eligible") is False:
        title_status = "NEVER_ELIGIBLE"
    else:
        title_status = status
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
        lines += ["", wrap("You could still take it later, once the reasons above no longer apply.")]
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


# ---- chances of getting the courses (the bidding MDP, solver/mdp.py) --------------------------------

LOW, HIGH = "round1", "all_rounds"          # the two probability scenarios, lower and higher
HARD = 0.95                                 # a course below this chance (lower scenario) is listed as hard to get
SHOWN_HARD = 5
SHOWN_OUTCOMES = 5
TINY = 1e-9                                 # stands for a chance the answer rounded to 0.0 but did list

LAST_SEMESTER = 8
BIDDING_INTRO = ("A CourseReg bid can fail when a course is full. These chances are rough estimates from the "
                 "AY2024/25 and AY2025/26 CourseReg reports, not a forecast. Each is a range from bidding in "
                 "round 1 only (lower) to bidding again in rounds 2 and 3 (higher).")


def pct(p):
    """A probability as a whole percentage; never rounds a small chance to 0% or a near-certain one to 100%."""
    if p <= 0:
        return "0%"
    if p >= 1:
        return "100%"
    if p < 0.005:
        return "under 1%"
    if p >= 0.995:
        return "over 99%"
    return f"{round(p * 100)}%"


def chance(a, b):
    """The range of two scenario probabilities, or one value when they look the same."""
    low, high = (pct(p) for p in sorted((a, b)))
    if low == high:
        return low
    if (low, high) == ("over 99%", "100%"):
        return low
    if (low, high) == ("0%", "under 1%"):
        return high
    return f"{low} to {high}"


def listed(distribution, key):
    """A probability from a finish distribution, which the answer rounds to three decimals. A key is
    present only when its probability is above 0, so 0.0 means a tiny chance; and 1.0 next to other
    keys means almost certain, not certain."""
    value = distribution.get(key)
    if value is None:
        return 0.0
    if value <= 0:
        return TINY
    if value >= 1 and len(distribution) > 1:
        return 1 - TINY
    return value


def year_semester(semester):
    return f"Year {(semester - 1) // 2 + 1} Semester {(semester - 1) % 2 + 1}"


def done_by(distribution, semester):
    """Chance of finishing by `semester`, from a finish distribution rounded to three decimals."""
    return sum(listed(distribution, key) for key in distribution if key != "late" and int(key) <= semester)


def figure(label, value, indent=2, width=42):
    return f"{' ' * indent}{label:<{width}}{value}"


def course_name(code, catalog):
    """Code and title, in the same columns as the plan (`course_line`)."""
    record = catalog[code] if catalog is not None and code in catalog else {}
    return f"{code:<9}  {record.get('title', '')}".rstrip()


def course_item(code, catalog):
    """A bulleted course; a long title wraps under itself."""
    return wrap(f"- {course_name(code, catalog)}", "    ", " " * 17)


def joined(codes):
    return " and ".join(codes) if len(codes) < 3 else ", ".join(codes[:-1]) + " and " + codes[-1]


def hard_courses(low, high, catalog):
    """Courses whose chance in some term is below HARD under the lower scenario, hardest first."""
    rows = []
    for code, by_term in low["admission"].items():
        if code in low["model"]["no_data"] or min(by_term.values()) >= HARD:
            continue
        other = high["admission"].get(code, {})
        terms = [f"Semester {term}: {chance(p, other.get(term, 1.0))}" for term, p in sorted(by_term.items())]
        rows.append((min(by_term.values()), code, terms))
    lines, indent = [], " " * 17                                       # under the title
    for _, code, terms in sorted(rows)[:SHOWN_HARD]:
        lines.append(course_item(code, catalog))
        one_line = indent + "   ".join(terms)
        lines += [one_line] if len(one_line) <= WIDTH + 4 else [indent + term for term in terms]
    if len(rows) > SHOWN_HARD:
        lines.append(f"    ...and {len(rows) - SHOWN_HARD} more below {pct(HARD)}")
    return lines


def outcome_lines(answer, semester):
    """What to bid for next semester after each way the first bid can turn out (one scenario)."""
    rows = []
    for row in answer["if_then"][:SHOWN_OUTCOMES]:
        if row["missed"]:
            label = f"If you miss {joined(row['missed'])} ({pct(row['probability'])}):"
        else:
            label = f"If every bid succeeds ({pct(row['probability'])}):"
        rows.append((label, ", ".join(row["next_bid"]) if row["next_bid"] else "nothing more; you are done"))
    width = max(len(label) for label, _ in rows) + 2
    lines = ["", f"  Then, in {semester_label(semester)}, bid for"]
    if all(4 + width + len(bid) <= WIDTH + 4 for _, bid in rows):     # one aligned line per outcome
        lines += [f"    {label:<{width}}{bid}" for label, bid in rows]
    else:                                                               # the bid on its own line
        for label, bid in rows:
            lines += [f"    {label}", wrap(bid, "        ")]
    rest = answer["if_then"][SHOWN_OUTCOMES:]
    if rest:
        together = sum(row["probability"] for row in rest)
        lines.append(f"    ...and {len(rest)} less likely outcomes (together {pct(together)})")
    return lines


def format_bidding(answers, catalog=None):
    """The answers of `solver.mdp.solve` for the two scenarios ({"round1": ..., "all_rounds": ...}) as text.
    The advice (what to bid for) comes from the lower scenario, so it leaves time to bid again; every
    other chance is shown as a range."""
    low, high = answers[LOW], answers[HIGH]
    failed = next((a for a in (low, high) if a["status"] != "POLICY"), None)
    if failed is not None:
        lines = [heading("I can't work out your chances for this request")]
        section(lines, "Why", failed.get("reasons", []) or [failed["status"]])
        return "\n".join(lines)

    lines = [heading("Your chances of getting these courses"), "", wrap(BIDDING_INTRO), ""]
    lines.append(figure("Plan above works exactly as written",
                        chance(low["deterministic"]["success_probability"],
                               high["deterministic"]["success_probability"])))
    finish_low, finish_high = low["finish_distribution"], high["finish_distribution"]
    planned = low["deterministic"]["last_semester"]
    if planned is not None and planned < LAST_SEMESTER:      # otherwise the next line says the same
        lines.append(figure(f"Done by {year_semester(planned)}, as planned",
                            chance(done_by(finish_low, planned), done_by(finish_high, planned))))
    lines.append(figure(f"Done by {year_semester(LAST_SEMESTER)}",
                        chance(1 - listed(finish_low, "late"), 1 - listed(finish_high, "late"))))

    hard = hard_courses(low, high, catalog)
    if hard:
        lines += ["", "  Hardest courses to get"] + hard
    else:
        lines += ["", wrap(f"None of these courses is often full: every chance is {pct(HARD)} or more.")]

    first = low["first_bid"]
    if first["courses"]:
        lines += ["", f"  Bid for these now, in {semester_label(first['semester'])}"]
        lines += [course_item(code, catalog) for code in first["courses"]]
        planned = low["deterministic"]["plan"].get(str(first["semester"]), [])
        if set(planned) != set(first["courses"]):
            lines.append(wrap("Note: this differs from the first semester of the plan above.", "    "))
        if low["if_then"]:
            lines += outcome_lines(low, first["semester"] + 1)


    no_data = low["model"]["no_data"]
    if no_data:
        assumed = chance(low["model"]["no_data_p"], high["model"]["no_data_p"])
        items = [f"{code} (Semester {' and '.join(str(t) for t in terms)})" for code, terms in no_data.items()]
        lines += ["", wrap(f"No past CourseReg data for {joined(items)}. A chance of {assumed} was assumed.")]

    section(lines, "Notes", low.get("notes", []))
    section(lines, "Not taken into account", low.get("not_applied", []))
    return "\n".join(lines)
