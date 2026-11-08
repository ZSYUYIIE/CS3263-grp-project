"""Independent plan checker.

Implements the hard rules of docs/SOLVER_GUIDE.md section 4 straight from catalog.json, without importing
m1_data.catalog, m1_data.resolve or the solver (AGENTS.md rule 4), so a bug on either side shows up as a
disagreement instead of being shared.

    check_plan(spec, plan)            -> list of violated rules (empty = valid)
    measures(spec, plan)              -> last semester, total MC, added courses
    preferences_met(spec, plan, gold) -> number of soft wishes met
"""
from __future__ import annotations

import json
from pathlib import Path

from pipelines.output import plan_shape_errors

ROOT = Path(__file__).resolve().parent.parent
C = json.loads((ROOT / "data/processed/AY2026-2027/catalog.json").read_text())["courses"]
ATAP = "CP3880"


def holds(tree, done: set) -> bool:
    """Evaluate a logic tree (course / and / or / n_of; None = no requirement; False = never)."""
    if tree is None or tree is True:
        return True
    if tree is False:
        return False
    op = tree["op"]
    if op == "course":
        return tree["code"] in done
    args = tree["args"]
    if op == "and":
        return all(holds(t, done) for t in args)
    if op == "or":
        return any(holds(t, done) for t in args)
    if op == "n_of":
        return sum(holds(t, done) for t in args) >= tree["n"]
    raise ValueError(f"unknown node {op}")


def normalise_plan(plan) -> dict[int, list[str]]:
    out: dict[int, list[str]] = {}
    for s, codes in (plan or {}).items():
        out[int(s)] = [str(c).strip().upper().replace(" ", "") for c in (codes or [])]
    return out


def must_rule_courses(spec) -> set[str]:
    out = set()
    for r in spec.get("rules") or []:
        if r.get("strength") == "must":
            out |= {r[k] for k in ("a", "b", "course") if k in r}
    return out


def check_plan(spec: dict, plan) -> list[str]:
    shape = plan_shape_errors(plan)
    if shape:
        return ["FORMAT " + error for error in shape]
    v: list[str] = []
    plan = normalise_plan(plan)
    k = spec["current_sem"]
    done = set(spec.get("completed") or [])
    must = set(spec.get("must_take") or [])
    sem_of: dict[str, int] = {}
    for s, codes in plan.items():
        if codes and not (k <= s <= 8):
            v.append(f"R1 semester {s} is outside {k}..8")
        for c in codes:
            if c in sem_of:
                v.append(f"R1 {c} planned twice")
            sem_of[c] = s
    for c in sorted(must - done):
        if c not in sem_of:
            v.append(f"R1 must-take {c} missing")
    for c, s in sorted(sem_of.items()):
        x = C.get(c)
        if x is None:
            v.append(f"R2 {c} is not a real course in the data")
            continue
        if not x["exists_in_ay"] or not x["available"] or x.get("details") == "stub":
            v.append(f"R2 {c} cannot be planned (not offered or not open to CS Hons)")
            continue
        if c in done:
            v.append(f"R1 {c} is already completed")
        if holds(x["preclusion"].get("blocked_if"), done) and x["preclusion"].get("blocked_if") is not None:
            v.append(f"R2 {c} is blocked by a completed course")
        inverse = set(x["preclusion"].get("mutually_exclusive_with") or []) & done
        if inverse:
            v.append(f"R6 {c} excludes completed {', '.join(sorted(inverse))}")
        term = 1 if s % 2 else 2
        if term not in x["offered"]:
            v.append(f"R3 {c} not offered in Sem {term} (semester {s})")
        earlier = done | {d for d, t in sem_of.items() if t < s}
        if not holds(x["prereq"].get("logic"), earlier):
            v.append(f"R4 {c} in semester {s}: prerequisite not met ({x['prereq']['text']})")
        same = earlier | {d for d, t in sem_of.items() if t == s}
        if not holds(x["coreq"].get("logic"), same):
            v.append(f"R5 {c} in semester {s}: corequisite not met")
        for d in x["preclusion"].get("mutually_exclusive_with") or []:
            if d in sem_of and c < d:
                v.append(f"R6 {c} and {d} exclude each other")
    cap = spec.get("mc_max", 20)
    caps = {int(s): c for s, c in (spec.get("sem_caps") or {}).items()}
    for s, codes in plan.items():
        mc = sum(C[c]["mc"] or 0 for c in codes if c in C and c != ATAP)
        limit = caps.get(s, cap)
        if mc > limit or (limit == 0 and codes):
            v.append(f"R7 semester {s} has {mc} MC, limit {limit}")
        if spec.get("mc_min") and codes and mc + (12 if ATAP in codes else 0) < spec["mc_min"]:
            v.append(f"R8 semester {s} has {mc} MC, minimum {spec['mc_min']}")
    for r in spec.get("rules") or []:
        if r.get("strength") != "must":
            continue
        if not rule_holds(r, sem_of, done):
            v.append(f"R9 must rule not met: {describe(r)}")
    required = must | must_rule_courses(spec)
    for c, s in sem_of.items():
        if c in required or c not in C:
            continue
        needed = any(c in (C[d]["prereq"].get("courses") or []) and t > s
                     or c in (C[d]["coreq"].get("courses") or []) and t >= s
                     for d, t in sem_of.items() if d in C and d != c)
        if not needed:
            v.append(f"R10 {c} was added but no later planned course needs it")
    return v


def eligibility_checks(spec):
    """Independent Q1 facts, read directly from the catalogue; never used during generation."""
    code = spec["target"]
    course = C[code]
    done = set(spec["completed"])
    preclusion = course["preclusion"]
    blocked = preclusion.get("blocked_if")
    inverse = set(preclusion.get("mutually_exclusive_with") or []) - set(preclusion.get("courses") or [])
    semester = spec.get("current_sem")
    offered = (1 if semester % 2 else 2) in course["offered"] if semester is not None else bool(
        {1, 2} & set(course["offered"]))
    return {"not_completed": code not in done, "open_to_programme": bool(course["available"]),
            "prerequisites_met": holds(course["prereq"].get("logic"), done),
            "no_preclusions": not ((blocked is not None and holds(blocked, done)) or inverse & done),
            "offered_in_term": offered}


def infeasibility_certificates(spec):
    """Sufficient, independently checked conflicts; not a general planning solver."""
    done = set(spec.get("completed") or [])
    required = set(spec.get("must_take") or []) - done
    first = spec["current_sem"]
    cap = spec.get("mc_max", 20)
    caps = {int(s): value for s, value in (spec.get("sem_caps") or {}).items()}
    active = [s for s in range(first, 9) if caps.get(s, cap) > 0]
    proofs = []
    for course in sorted(required & C.keys()):
        record = C[course]
        if not record["available"] or record.get("details") == "stub":
            proofs.append(f"{course} is unavailable to this programme in the catalogue")
        blockers = set(record["preclusion"].get("mutually_exclusive_with") or []) & done
        if blockers:
            proofs.append(f"{course} excludes completed {', '.join(sorted(blockers))}")
        for other in sorted(required & set(record["preclusion"].get("mutually_exclusive_with") or [])):
            if course < other:
                proofs.append(f"required {course} and {other} are mutually exclusive")
        if not any((1 if s % 2 else 2) in record["offered"] for s in active):
            proofs.append(f"{course} has no offering in a remaining nonblocked semester")
        if first == 8 and not holds(record["prereq"].get("logic"), done):
            proofs.append(f"{course} has an unmet prerequisite and no strictly earlier semester remains")
    required_mc = sum(C[c]["mc"] or 0 for c in required if c in C and c != ATAP)
    capacity = sum(caps.get(s, cap) for s in range(first, 9))
    if required_mc > capacity:
        proofs.append(f"required ordinary courses need {required_mc} MC but remaining capacity is {capacity} MC")
    hard = [r for r in spec.get("rules") or [] if r.get("strength") == "must"]
    before = {(r["a"], r["b"]) for r in hard if r["type"] == "before" and
              r["a"] not in done and r["b"] not in done}
    if any((b, a) in before for a, b in before):
        proofs.append("mandatory before rules contain a directed two-course cycle")
    fixed = {}
    for rule in hard:
        if rule["type"] != "in_sem":
            continue
        course, semester = rule["course"], rule["sem"]
        if course not in C:
            continue
        fixed.setdefault(semester, set()).add(course)
        record = C[course]
        if (1 if semester % 2 else 2) not in record["offered"]:
            proofs.append(f"fixed {course} in semester {semester} conflicts with its offering")
        if semester == first and not holds(record["prereq"].get("logic"), done):
            proofs.append(f"fixed {course} in the starting semester has an unmet strict prerequisite")
    for semester, courses in fixed.items():
        credits = sum(C[c]["mc"] or 0 for c in courses if c != ATAP)
        if credits > caps.get(semester, cap):
            proofs.append(f"courses fixed to semester {semester} need {credits} MC above its cap")
    return proofs


def describe(r):
    if r["type"] == "in_sem":
        return f"{r['course']} in semester {r['sem']}"
    return f"{r['type']} {r['a']} {r['b']}"


def rule_holds(r, sem_of, done) -> bool:
    t = r["type"]
    if t == "in_sem":
        return sem_of.get(r["course"]) == r["sem"]
    a, b = r["a"], r["b"]
    if a in done or b in done:          # fixed rules for completed courses (SOLVER_GUIDE section 5)
        return {"before": a in done and b not in done, "apart": True,
                "same_sem": a in done and b in done}[t]
    if a not in sem_of or b not in sem_of:
        return False
    return {"before": sem_of[a] < sem_of[b], "apart": sem_of[a] != sem_of[b],
            "same_sem": sem_of[a] == sem_of[b]}[t]


def measures(spec, plan) -> dict:
    plan = normalise_plan(plan)
    used = [s for s, codes in plan.items() if codes]
    codes = [c for cs in plan.values() for c in cs]
    required = set(spec.get("must_take") or []) | must_rule_courses(spec) | set(spec.get("completed") or [])
    return {"last_semester": max(used) if used else None,
            "total_mc": sum((C[c]["mc"] or 0) for c in codes if c in C),
            "added": sorted(c for c in codes if c not in required)}


def loads(plan, k, last):
    plan = normalise_plan(plan)
    return {s: sum(C[c]["mc"] or 0 for c in plan.get(s, []) if c in C and c != ATAP) for s in range(k, last + 1)}


def preferences_met(spec, plan, gold_plan) -> int:
    """Soft wishes met, by SOLVER_GUIDE section 5. early / late / balance_load are relative to the best
    value among tied plans, which only the solver knows; the gold plan stands in for it (met if at least as
    good as the gold plan). This legacy proxy may over-count when the gold plan missed a relative wish.
    Certified grading uses preference_bounds instead."""
    plan_n, gold_n = normalise_plan(plan), normalise_plan(gold_plan)
    sem_of = {c: s for s, cs in plan_n.items() for c in cs}
    gsem = {c: s for s, cs in gold_n.items() for c in cs}
    done = set(spec.get("completed") or [])
    k = spec["current_sem"]
    met = 0
    for r in spec.get("rules") or []:
        if r.get("strength") == "prefer":
            if r["type"] == "in_sem" and r["course"] in done:
                continue
            met += rule_holds(r, sem_of, done)
    used = [s for s, cs in plan_n.items() if cs]
    if used:
        last = max(used) if spec.get("objective", "none") != "none" else 8
        ld = loads(plan, k, max(last, max(used)))
        window = loads(plan, k, last)
        avg = sum(window.values()) / len(window)
        for s in spec.get("light_sems") or []:
            s = max(used) if s == "last" else s
            if s >= k and ld.get(s, 0) < avg:
                met += 1
        if spec.get("balance_load") and gold_n:
            met += max(ld.values()) <= max(loads(gold_plan, k, max(int(x) for x in gold_n)).values())
    for c in spec.get("early") or []:
        met += c in done or (c in sem_of and c in gsem and sem_of[c] <= gsem[c])
    for c in spec.get("late") or []:
        met += c in done or (c in sem_of and c in gsem and sem_of[c] >= gsem[c])
    return met


def preference_bounds(spec, plan, gold_answer, witnesses=()):
    """Certify preference counts without treating a missed gold wish as its optimal bound.

    A gold plan that missed 'balance load' cannot establish the minimum achievable peak.
    Offline, independently valid witness plans can disprove a claimed relative optimum.
    """
    gold_plan = gold_answer["plan"]
    exact = {k: v for k, v in spec.items() if k not in ("balance_load", "early", "late")}
    lower = preferences_met(exact, plan, gold_plan)
    unknown = []
    normalized = normalise_plan(plan)
    semesters = {c: s for s, codes in normalized.items() for c in codes}
    gold_semesters = {c: s for s, codes in normalise_plan(gold_plan).items() for c in codes}
    done = set(spec.get("completed") or [])
    met_labels = set(gold_answer.get("preferences_met", []))
    gold_measures = measures(spec, gold_plan)
    comparable = []
    for witness in witnesses:
        if check_plan(spec, witness):
            continue
        m = measures(spec, witness)
        objective = spec.get("objective", "none")
        same_primary = (objective == "none" or
                        objective == "earliest_graduation" and m["last_semester"] == gold_measures["last_semester"] or
                        objective == "min_total_mc" and m["total_mc"] == gold_measures["total_mc"])
        if same_primary and len(m["added"]) == len(gold_measures["added"]):
            comparable.append(normalise_plan(witness))

    def peak(candidate):
        last = max(candidate, default=spec["current_sem"])
        return max(loads(candidate, spec["current_sem"], last).values(), default=0)

    if spec.get("balance_load"):
        label = "largest semester load is as small as possible"
        if any(peak(w) < peak(normalized) for w in comparable):
            pass  # A feasible plan with a smaller peak disproves this preference.
        elif label in met_labels:
            lower += peak(normalized) <= peak(normalise_plan(gold_plan))
        else:
            unknown.append(label)
    for key, wording in (("early", "as early as possible"), ("late", "as late as possible")):
        for course in spec.get(key) or []:
            label = f"{course} {wording}"
            if course in done:
                lower += 1
            elif course not in semesters:
                continue
            else:
                better_witness = any(course in {c for cs in w.values() for c in cs} and
                                     ((semesters[course] > s) if key == "early" else (semesters[course] < s))
                                     for w in comparable for s, cs in w.items() if course in cs)
                if better_witness:
                    continue
                if label in met_labels and course in gold_semesters:
                    lower += ((semesters[course] <= gold_semesters[course]) if key == "early"
                              else (semesters[course] >= gold_semesters[course]))
                else:
                    unknown.append(label)
    return int(lower), int(lower) + len(unknown), unknown
