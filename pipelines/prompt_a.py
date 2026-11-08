"""Pipeline A prompt: the LLM answers the student's request itself, given the course records it needs.

Record selection rule (state this in the report):
  every course named in the request (completed, must-take, target, rule courses), plus the transitive
  closure of prerequisite and corequisite courses of the courses not yet completed, restricted to codes
  that exist in AY2026/27. Records are factual catalogue data only: no field that does the reasoning
  (no "reachable", no "eligible"). A course closed to BComp CS Hons says so, because that is a catalogue
  fact the student could look up.

The request text is the only part taken from the instance; the gold spec is used only to decide which
records to include (the same courses a student would look up), never shown to the model.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = json.loads((ROOT / "data/processed/AY2026-2027/catalog.json").read_text())["courses"]
CODE_RE = re.compile(r"\b[A-Z]{2,4}\d{4}[A-Z]{0,3}\b")
PROMPT_VERSION = "route-a-v2"

INSTRUCTIONS = """You are an academic planning assistant for NUS BComp (Computer Science) Honours students,
single major, under AY2026/27 rules. Answer the student's request using ONLY the course records given below. Work it out
yourself; there is no tool.

SEMESTERS
Semesters are numbered 1 to 8: Y1S1 = 1, Y1S2 = 2, Y2S1 = 3, Y2S2 = 4, Y3S1 = 5, Y3S2 = 6, Y4S1 = 7, Y4S2 = 8.
Odd semesters are Semester 1 of the academic year, even semesters are Semester 2. "Offered: Sem 1" means
the course can only be placed in odd semesters. Future years are assumed to offer courses as AY2026/27 does.

QUESTION TYPES
- "Can I take X (in semester N / next semester)?" -> eligibility. X is eligible when: X is open to BComp CS
  Hons, the student has not completed X, X's prerequisite is satisfied by the completed courses, X is not
  blocked by a completed course ("Cannot take if completed"), and X is offered in that semester's term.
  If the request gives no semester, judge eligibility for any term X is offered in.
- "Plan my remaining semesters" -> plan from the semester the student is in now (inclusive) to semester 8.

PLANNING RULES (all must hold)
1. Each course at most once. Every course the student must take (and has not completed) is in the plan.
2. Only courses open to BComp CS Hons, and none blocked by a completed course.
3. A course only in a semester of a term it is offered in.
4. Prerequisites must be completed or planned in a STRICTLY earlier semester. Corequisites in the same or an
   earlier semester.
5. Two courses that are mutually exclusive cannot both be planned (and a completed course rules out the
   courses it blocks).
6. MC per semester at most the student's limit (20 MC if none is stated). An exchange/NOC semester has 0 MC.
   "N modules" means N x 4 MC.
7. Every "must"/"has to" wish holds.
8. Add a course the student did not ask for ONLY when it is a prerequisite needed by a planned course.
   Never add courses to fill a semester.

WHAT TO OPTIMISE, in this order
1. If the student wants to graduate as early as possible: the smallest last semester used. If they want the
   fewest total credits: the smallest total MC. Otherwise no ranking here.
2. The fewest added courses.
3. The most of the student's soft wishes met ("prefer", "ideally", "if possible", "as early/late as possible",
   "light last semester", "spread evenly").
Never trade a better step 1 or 2 for more soft wishes.

WHEN TO REFUSE
- If no plan satisfies all the rules, say so: status "NO_PLAN", with the reason.
- If the student does not say which courses they have completed (and "none" was not said), or (for a plan)
  which semester they are in or which courses they must take, do not guess: status "MISSING_INFO".
- If the student is not a single-major BComp CS Hons student (another programme, second major, minor, double
  degree), or asks about a course that is not in the records and is not a real AY2026/27 course you were given,
  status "OUT_OF_SCOPE".
- Wishes you cannot act on (timetable, S/U, waivers, failing) do not change the answer.

OUTPUT
Return exactly ONE JSON object, starting with { and ending with }. No markdown fences or outside text.
The answer object ITSELF must have a top-level "status" string and "reasons" list.
Do NOT wrap the answer inside "eligibility", "answer", "result", or "plan".
Answer only the question the student asked. Do not produce separate eligibility and planning answers.
Choose ONE status: ELIGIBLE, NOT_ELIGIBLE, PLAN, NO_PLAN, MISSING_INFO, OUT_OF_SCOPE.
"reasons" must contain at least one short, specific final justification grounded in the request and records.
Give the final answer and concise supporting facts, not a transcript of your internal deliberation.

For PLAN, include a top-level "plan" object mapping semester strings directly to lists of course codes.
Its values must be lists, never another answer object. Example of SHAPE ONLY (not a solution):
{"status":"PLAN","plan":{"5":["COURSE_CODE"],"6":["ANOTHER_CODE"]},"reasons":["Concise justification."]}
Use real course codes from the records. Include only semesters from the current one to 8.
For every other status, OMIT "plan" completely.

For ELIGIBLE or NOT_ELIGIBLE, also include "eligibility_checks", with EXACTLY these five boolean fields:
"not_completed", "open_to_programme", "prerequisites_met", "no_preclusions", "offered_in_term".
Each boolean is YOUR assessment, which will be independently checked afterward.
With no semester specified, "offered_in_term" means offered in at least one regular term (Sem 1 or 2).
Explain the actual blocker(s) when NOT_ELIGIBLE. An eligible decision requires all five checks to be true.

For MISSING_INFO, also include "missing_fields": a list of the missing mandatory fields chosen from
"completed", "target", "current_sem", "must_take". Missing only a semester does not prevent eligibility advice.
For NO_PLAN, explain a concrete conflict among the stated requirements or course rules.
For OUT_OF_SCOPE, explain the scope mismatch and recommend checking with an academic advisor.
You may include "not_applied": a list of unsupported wishes from the student; never silently satisfy them.
Do not add any other top-level fields. Before responding, check the output shape and your answer against
the supplied rules. Do not invent missing information to avoid returning MISSING_INFO.
"""


def term_text(offered):
    names = {1: "Sem 1", 2: "Sem 2", 3: "Special Term I", 4: "Special Term II"}
    return ", ".join(names[t] for t in offered) if offered else "not offered"


def record_text(code: str) -> str:
    x = CATALOG[code]
    if not x["exists_in_ay"] or x.get("details") == "stub":
        return f"{code}: no AY2026/27 offering (old or retired course; can count as completed, cannot be planned)"
    lines = [f"{code} {x['title']} | {x['mc']} MC | offered: {term_text(x['offered'])}"]
    if not x["available"]:
        lines.append("  NOT open to BComp CS Hons students: " + "; ".join(x["unavailable_reasons"]))
    lines.append(f"  prerequisite: {x['prereq']['text']}")
    if x["coreq"].get("logic") is not None:
        lines.append(f"  corequisite: {x['coreq']['text']}")
    pre = x["preclusion"]
    if pre.get("blocked_if") is not None:
        lines.append(f"  cannot take if completed: {pre['text']}")
    if pre.get("mutually_exclusive_with"):
        lines.append("  mutually exclusive with: " + ", ".join(pre["mutually_exclusive_with"]))
    return "\n".join(lines)


def select_records(spec: dict, request: str) -> list[str]:
    done = set(spec.get("completed") or [])
    named = set(done) | set(spec.get("must_take") or [])
    if spec.get("target"):
        named.add(spec["target"])
    for ru in spec.get("rules") or []:
        named |= {ru[k] for k in ("a", "b", "course") if k in ru}
    named |= set(CODE_RE.findall(request))       # anything the student typed
    seen: set[str] = set()
    queue = [c for c in named if c in CATALOG and c not in done]
    while queue:
        c = queue.pop()
        if c in seen:
            continue
        seen.add(c)
        x = CATALOG[c]
        if x.get("details") == "stub":
            continue
        for d in (x["prereq"].get("courses") or []) + (x["coreq"].get("courses") or []):
            if d in CATALOG and CATALOG[d]["exists_in_ay"] and d not in seen:
                queue.append(d)
    return sorted((seen | named) & set(CATALOG))


def build_messages(instance: dict) -> list[dict]:
    codes = select_records(instance["gold_spec"], instance["request"])
    records = "\n".join(record_text(c) for c in codes)
    user = (f"COURSE RECORDS (NUSMods AY2026/27, {len(codes)} courses)\n{records}\n\n"
            f"STUDENT REQUEST\n{instance['request']}")
    return [{"role": "system", "content": INSTRUCTIONS}, {"role": "user", "content": user}]
