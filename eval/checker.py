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
    v: list[str] = []
    plan = normalise_plan(plan)
    done = set(spec.get("completed") or [])
    must = set(spec.get("must_take") or [])
    k = spec["current_sem"]
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


def preferences_met(spec, plan, gold_plan) -> int:
    """Soft wishes met, by SOLVER_GUIDE section 5. early / late are relative to the best
    value among tied plans, which only the solver knows; the gold plan stands in for it (met if at least as
    good as the gold plan). This can only under-count the LLM when the gold plan itself missed the wish."""
    plan_n, gold_n = normalise_plan(plan), normalise_plan(gold_plan)
    sem_of = {c: s for s, cs in plan_n.items() for c in cs}
    gsem = {c: s for s, cs in gold_n.items() for c in cs}
    done = set(spec.get("completed") or [])
    met = 0
    for r in spec.get("rules") or []:
        if r.get("strength") == "prefer":
            if r["type"] == "in_sem" and r["course"] in done:
                continue
            met += rule_holds(r, sem_of, done)
    for c in spec.get("early") or []:
        met += c in done or (c in sem_of and c in gsem and sem_of[c] <= gsem[c])
    for c in spec.get("late") or []:
        met += c in done or (c in sem_of and c in gsem and sem_of[c] >= gsem[c])
    return met
