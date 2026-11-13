"""Grade one pipeline's answers against the gold answers and write result tables.

    python -m eval.grade results/A/qwen3-max
    python -m eval.grade results/A/qwen3-max results/B/qwen3-max      # also writes COMPARE.md, one column per folder

Per instance: status correct?  For gold PLAN: valid?  optimality class (invalid / objective gap / extra
courses / preference gap / optimal, SOLVER_GUIDE section 6).  For gold NO_PLAN: invented plan?
For gold PLAN answered NO_PLAN: over-refusal.

The two agreed metrics:
  valid-answer accuracy   the status equals the gold status and, for PLAN, the plan breaks no hard rule.
                          Denominator: every instance in the group.
  optimal-plan accuracy   a gold PLAN instance answered with an optimal plan.
                          Denominator: the gold PLAN instances in the group only.
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
from decimal import ROUND_HALF_UP, Decimal
from math import comb, sqrt
from statistics import NormalDist
from collections import Counter, defaultdict
from pathlib import Path

from eval.checker import check_plan, measures, preferences_met

ROOT = Path(__file__).resolve().parent.parent

Q1_META = ("reason", "level", "style", "role", "base_id", "pair_id", "term_form", "missing_course_takeable_now",
           "correction_kind", "retraction_flips_answer")
Q2_META = ("set", "twin", "answer_type", "visible", "wording", "log10_omega", "rho", "n_cand", "n_sems", "added",
           "nokind", "ladder", "band", "oos", "missing")
SIZE_EDGES = ((-1, 3, "below 3"), (3, 6, "3 to below 6"), (6, 10, "6 to below 10"), (10, 24, "10 to below 24"),
              (24, 1e9, "24 and above"))
BAND_ORDER = ("1-2", "3-4", "5-6", "7-8", "not given", "outside 1-8")
NOKIND_ORDER = ("capacity", "exclusion", "parity", "chain", "rule_conflict", "hidden")
CLASSES = ("optimal", "preference gap", "extra courses", "objective gap", "invalid", "over-refusal", "wrong status",
           "BEATS GOLD: check")
RHO_ORDER = ("below 0.4", "0.4 to below 0.6", "0.6 to below 0.8", "0.8 to 1.0", "above 1")
OBJECTIVE_ORDER = ("none", "earliest_graduation", "min_total_mc")
SPEC_FIELDS = ("query", "current_sem", "completed", "must_take", "mc_max", "mc_min", "sem_caps", "atap_sems",
               "objective", "early", "late", "rules", "unsupported", "programme")


def decision_size(inst, catalog):
    """k = number of distinct course codes in the target's prerequisite, preclusion and mutual-exclusion lists."""
    course = catalog.courses.get(inst["gold_spec"].get("target"))
    if not course:
        return ""
    codes = set(course["prereq"].get("courses") or [])
    codes |= set(course["preclusion"].get("courses") or []) | set(course["preclusion"].get("mutually_exclusive_with") or [])
    return len(codes)


def ranks(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    out = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        for t in range(i, j + 1):
            out[order[t]] = (i + j) / 2 + 1
        i = j + 1
    return out


def spearman(xs, ys):
    """Spearman rank correlation and a two-sided p from the normal approximation (n of a few hundred)."""
    n = len(xs)
    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    sxx, syy = sum((a - mx) ** 2 for a in rx), sum((b - my) ** 2 for b in ry)
    if not sxx or not syy:
        return None, None
    rho = sxy / sqrt(sxx * syy)
    z = rho * sqrt(n - 1)
    return rho, 2 * (1 - NormalDist().cdf(abs(z)))


def k_bins(entries, parts=4):
    """entries: (k, payload). Equal-size bins by rank of k; returns (low k, high k, payloads)."""
    entries = sorted(entries, key=lambda e: e[0])
    n = len(entries)
    out = []
    for i in range(parts):
        part = entries[i * n // parts:(i + 1) * n // parts]
        if part:
            out.append((part[0][0], part[-1][0], [e[1] for e in part]))
    return out


def valid_ok(r):
    return r["status_correct"] and r["class"] != "invalid"


def optimal_ok(r):
    return r["gold_status"] == "PLAN" and r["class"] == "optimal"


def grade_one(inst, rec):
    gold = inst["gold_answer"]
    spec = inst["gold_spec"]
    ans = rec.get("answer") if rec else None
    status = (ans or {}).get("status", "UNPARSEABLE") if isinstance(ans, dict) else "UNPARSEABLE"
    row = {"id": inst["id"], "kind": inst["kind"], "group": inst["kind"].split("/")[0],
           "gold_status": gold["status"], "status": status, "status_correct": status == gold["status"],
           "fenced": bool(rec and rec.get("fenced")), "violations": "", "class": ""}
    meta = inst.get("meta") or {}
    for key in Q1_META + Q2_META:
        row[key] = meta.get(key, "")
    row["meta_group"] = meta.get("group", "")
    row["k"] = ""
    usage = (rec or {}).get("usage") or {}
    for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
        row[key] = usage.get(key, "")
    row.update({"objective": "", "n_must_rules": "", "n_prefs": "", "must_take": "", "cur_sem": "", "atap": "",
                "mc_min": ""})
    if spec.get("query") == "plan":
        rules = spec.get("rules") or []
        n_prefs = meta.get("n_prefs")
        if n_prefs is None:
            n_prefs = len(gold.get("preferences_met", [])) + len(gold.get("preferences_not_met", []))
        row.update({"objective": spec.get("objective", "none"),
                    "n_must_rules": sum(x.get("strength") == "must" for x in rules),
                    "n_prefs": n_prefs, "must_take": len(spec.get("must_take") or []),
                    "cur_sem": spec.get("current_sem", ""), "atap": "atap_sems" in spec, "mc_min": "mc_min" in spec})
    if gold["status"] == "PLAN":
        if status == "PLAN":
            v = check_plan(spec, ans.get("plan"))
            row["violations"] = " | ".join(v)
            if v:
                row["class"] = "invalid"
            else:
                m, g = measures(spec, ans.get("plan")), measures(spec, gold["plan"])
                obj = spec.get("objective", "none")
                worse = (obj == "earliest_graduation" and m["last_semester"] > g["last_semester"]) or \
                        (obj == "min_total_mc" and m["total_mc"] > g["total_mc"])
                better = (obj == "earliest_graduation" and m["last_semester"] < g["last_semester"]) or \
                         (obj == "min_total_mc" and m["total_mc"] < g["total_mc"])
                p = preferences_met(spec, ans.get("plan"), gold["plan"])
                gp = len(gold.get("preferences_met", []))
                row["class"] = ("BEATS GOLD: check" if better else "objective gap" if worse
                                else "extra courses" if len(m["added"]) > len(g["added"])
                                else "preference gap" if p < gp else "optimal")
        elif status == "NO_PLAN":
            row["class"] = "over-refusal"
        else:
            row["class"] = "wrong status"
    elif gold["status"] == "NO_PLAN":
        row["class"] = "invented plan" if status == "PLAN" else "correct refusal" if status == "NO_PLAN" \
            else "wrong status"
    return row


def pct(n, d):
    if not d:
        return "-"
    value = (Decimal(100 * n) / Decimal(d)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return f"{value}% ({n}/{d})"


def _pct(vals, q):
    v = sorted(vals)
    return v[int(q * (len(v) - 1))] if v else None


def _stats(vals):
    vals = [x for x in vals if x is not None and x != ""]
    if not vals:
        return "-", "-", "-"
    return f"{statistics.median(vals):g}", f"{_pct(vals, 0.95):g}", f"{max(vals):g}"


def fisher_p(a, b, c, d):
    """Two-sided Fisher exact p for the table [[a, b], [c, d]] (a, b = correct, wrong in group 1)."""
    n1, n2, k = a + b, c + d, a + c
    tot = n1 + n2
    if tot == 0:
        return None
    probs = {x: comb(n1, x) * comb(n2, k - x) / comb(tot, k) for x in range(max(0, k - n2), min(n1, k) + 1)}
    p0 = probs[a]
    return min(1.0, sum(v for v in probs.values() if v <= p0 * (1 + 1e-9)))


def mcnemar_p(b, c):
    """Exact two-sided McNemar p from the discordant pairs (b = first right/second wrong, c = reverse)."""
    n = b + c
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(comb(n, i) for i in range(min(b, c) + 1)) / 2 ** n)


def fmt_p(p):
    return "-" if p is None else f"{p:.3f}"


def paired(rows, first, second, key="base_id"):
    """Pairs of rows sharing `key`: first(r) selects one side, second(r) the other. Returns (n, both, only1, only2, neither)."""
    a = {r[key]: r for r in rows if first(r)}
    b = {r[key]: r for r in rows if second(r)}
    ids = sorted(set(a) & set(b))
    both = sum(a[i]["status_correct"] and b[i]["status_correct"] for i in ids)
    o1 = sum(a[i]["status_correct"] and not b[i]["status_correct"] for i in ids)
    o2 = sum(b[i]["status_correct"] and not a[i]["status_correct"] for i in ids)
    return len(ids), both, o1, o2, len(ids) - both - o1 - o2


def q1_section(rows):
    """Tables for the Q1 set built by instances/generate_q1.py (rows carry its metadata)."""
    q = [r for r in rows if r["role"]]
    if not q:
        return []
    base = [r for r in q if r["role"] == "base_plain"]
    L = ["", "## Q1 factors (instances/generate_q1.py)", ""]

    classes = defaultdict(list)
    for r in q:
        classes[r["gold_status"]].append(r["status_correct"])
    rec = {k: sum(v) / len(v) for k, v in classes.items()}
    L += [f"Balanced accuracy (mean of the {len(rec)} per-class accuracies above): {(Decimal(100 * sum(rec.values())) / len(rec)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)}%", ""]

    def table(title, key, rs, order=None):
        groups = defaultdict(list)
        for r in rs:
            groups[str(r[key])].append(r["status_correct"])
        names = order or sorted(groups)
        out = [f"**{title}**", "", "| Value | Correct |", "|---|---|"]
        out += [f"| {n} | {pct(sum(groups[n]), len(groups[n]))} |" for n in names if n in groups]
        return out + [""]
    L += table("By reason (base cases, plain wording)", "reason", base)
    L += table("By formula complexity level (base cases, plain wording)", "level", base)
    L += table("By wording style (all Q1 base-case renderings)", "style", [r for r in q if r["role"] in ("base_plain", "base_harder")])
    lv = {l: [r["status_correct"] for r in base if str(r["level"]) == l] for l in ("1", "2", "3")}
    if lv["1"] and lv["3"]:
        L += [f"Level 1 against level 3: Fisher exact p = "
              f"{fmt_p(fisher_p(sum(lv['1']), len(lv['1']) - sum(lv['1']), sum(lv['3']), len(lv['3']) - sum(lv['3'])))}", ""]

    L += ["**Paired comparisons** (same base case, two versions; exact McNemar on the discordant pairs)", "",
          "| Comparison | Pairs | Both right | Only first right | Only second right | p |", "|---|---|---|---|---|---|"]

    def add(name, first, second, key="base_id"):
        n, both, o1, o2, _ = paired(q, first, second, key)
        L.append(f"| {name} | {n} | {both} | {o1} | {o2} | {fmt_p(mcnemar_p(o1, o2)) if n else '-'} |")
    add("plain vs scattered wording", lambda r: r["role"] == "base_plain", lambda r: r["role"] == "base_harder" and r["style"] == "scattered")
    add("plain vs correction wording", lambda r: r["role"] == "base_plain", lambda r: r["role"] == "base_harder" and r["style"] == "correction")
    add("term absolute vs 'next semester'", lambda r: r["role"] == "base_plain", lambda r: r["role"] == "term_twin")
    add("ELIGIBLE base vs with excluding course", lambda r: r["role"] == "base_plain" and r["gold_status"] == "ELIGIBLE",
        lambda r: r["role"] == "exclusion_twin")
    add("ELIGIBLE base vs its missing-prerequisite near-miss", lambda r: r["role"] == "base_plain" and r["reason"] == "eligible",
        lambda r: r["role"] == "base_plain" and r["reason"] == "missing_prereq", key="pair_id")
    L.append("")

    ks = [r for r in q if r["k"] != ""]
    if ks:
        L += ["**By decision size k** (course codes in the target's prerequisite, preclusion and exclusion lists; "
              "state space 2^k; equal-size bins by rank of k, all Q1 instances whose target is in the catalogue)", "",
              "| k | Instances | Correct |", "|---|---|---|"]
        for lo, hi, rs in k_bins([(r["k"], r) for r in ks]):
            L.append(f"| {lo}-{hi} | {len(rs)} | {pct(sum(r['status_correct'] for r in rs), len(rs))} |")
        rho, p = spearman([r["k"] for r in ks], [int(r["status_correct"]) for r in ks])
        if rho is not None:
            L += ["", f"Spearman correlation of k with a correct status: rho = {rho:.2f}, p = {fmt_p(p)} (normal approximation)", ""]

    mp = [r for r in base if r["reason"] == "missing_prereq"]
    now = [r["status_correct"] for r in mp if r["missing_course_takeable_now"] is True]
    later = [r["status_correct"] for r in mp if r["missing_course_takeable_now"] is False]
    if now and later:
        L += [f"Missing-prerequisite cases, missing course could be taken now: {pct(sum(now), len(now))}; "
              f"could not: {pct(sum(later), len(later))}; Fisher exact p = "
              f"{fmt_p(fisher_p(sum(now), len(now) - sum(now), sum(later), len(later) - sum(later)))}", ""]
    cor = [r for r in q if r["role"] == "base_harder" and r["style"] == "correction" and r["correction_kind"] == "drop"]
    if cor:
        fl = [r["status_correct"] for r in cor if r["retraction_flips_answer"] is True]
        L += [f"Correction wording where the retracted course would change the answer: {pct(sum(fl), len(fl))}", ""]
    info = [r for r in q if r["role"] == "info"]
    if info:
        L += ["**Descriptive groups**", "", "| Group | Correct |", "|---|---|"]
        for g in sorted({r["meta_group"] for r in info}):
            rs = [r for r in info if r["meta_group"] == g]
            L.append(f"| {g} | {pct(sum(r['status_correct'] for r in rs), len(rs))} |")
        L.append("")
    return L


def capped(value, top=3):
    value = int(value)
    return f"{top}+" if value >= top else str(value)


def rho_bin(value):
    if value > 1:
        return "above 1"
    for edge, name in ((0.4, "below 0.4"), (0.6, "0.4 to below 0.6"), (0.8, "0.6 to below 0.8")):
        if value < edge:
            return name
    return "0.8 to 1.0"


def semester_band(value):
    low = (int(value) - 1) // 2 * 2 + 1
    return f"{low}-{low + 1}"


def level_groups(rows, key, order=None):
    groups = defaultdict(list)
    for r in rows:
        value = key(r)
        if value is not None:
            groups[value].append(r)
    names = order or sorted(groups)
    return [(str(name), groups[name]) for name in names if name in groups]


def yes_no(value):
    return "yes" if value else "no"


def size_bin(value):
    return next(name for lo, hi, name in SIZE_EDGES if lo <= value < hi)


def m_group(r):
    if r["must_take"] == "" or r["answer_type"] == "MISSING_INFO" and r["missing"] == "must_take":
        return "not given"
    m = int(r["must_take"])
    return "2-4" if m <= 4 else "6-8" if m <= 8 else "10-12"


def rho_population(q):
    return [r for r in q if r["rho"] != "" and (r["set"] in ("S1", "S2") or (r["set"] == "S4" and r["nokind"] == "capacity"
            and r["gold_status"] == "NO_PLAN"))]


def q2_tables(q):
    plan = [r for r in q if r["gold_status"] == "PLAN"]
    s1 = [r for r in plan if r["set"] == "S1"]
    size = [r for r in s1 if r["log10_omega"] != ""]
    rule_ladder = [r for r in plan if r["ladder"] == "rule"]
    pref_ladder = [r for r in plan if r["ladder"] == "preference"]
    obj_ladder = [r for r in plan if r["ladder"] == "objective"]
    twins = [r for r in plan if r["twin"] in ("base", "atap", "mc_min")]
    wording = [r for r in plan if r["set"] == "S5"]
    return [
        ("By set", level_groups(q, lambda r: r["set"])),
        ("By answer type (gold status)", level_groups(q, lambda r: r["answer_type"] or None)),
        ("Current semester band (all instances)", level_groups(q, lambda r: r["band"], BAND_ORDER)),
        ("Must-take courses M (all instances)", level_groups(q, m_group, ("2-4", "6-8", "10-12", "not given"))),
        ("Objective (all instances with a plan request)", level_groups([r for r in q if r["objective"] != ""],
                                                                       lambda r: r["objective"], OBJECTIVE_ORDER)),
        ("Number of preferences (all instances with a plan request)",
         level_groups([r for r in q if r["n_prefs"] != ""], lambda r: capped(r["n_prefs"], 4))),
        ("Number of must rules (all instances with a plan request)",
         level_groups([r for r in q if r["n_must_rules"] != ""], lambda r: capped(r["n_must_rules"], 4))),
        ("ATAP in the request (all instances with a plan request)",
         level_groups([r for r in q if r["atap"] != ""], lambda r: yes_no(r["atap"]))),
        ("Minimum MC in the request (all instances with a plan request)",
         level_groups([r for r in q if r["mc_min"] != ""], lambda r: yes_no(r["mc_min"]))),
        ("Wording (all instances)", level_groups(q, lambda r: r["wording"] or "plain", ("plain", "scattered", "unsupported"))),
        ("State space size, log10 of |Omega| (S1, gold PLAN, fixed bins)",
         level_groups(size, lambda r: size_bin(float(r["log10_omega"])), [n for _, _, n in SIZE_EDGES])),
        ("Usable semesters |S| (S1, gold PLAN)", level_groups([r for r in s1 if r["n_sems"] != ""], lambda r: int(r["n_sems"]))),
        ("Added courses in the gold plan (S1, gold PLAN)", level_groups([r for r in s1 if r["added"] != ""], lambda r: capped(r["added"]))),
        ("Capacity ratio rho (S1, S2 and capacity-impossible requests)",
         level_groups(rho_population(q), lambda r: rho_bin(float(r["rho"])), RHO_ORDER)),
        ("Must-rule ladder (same students, 0 to 3 must rules added)", level_groups(rule_ladder, lambda r: str(r["n_must_rules"]))),
        ("Preference ladder (same students, 0 to 3 preferences added)", level_groups(pref_ladder, lambda r: str(r["n_prefs"]))),
        ("Objective ladder (same students, objective changed)", level_groups(obj_ladder, lambda r: r["objective"], OBJECTIVE_ORDER)),
        ("ATAP and minimum-MC twins and their bases", level_groups(twins, lambda r: {"base": "base", "atap": "with ATAP", "mc_min": "with minimum MC"}[r["twin"]],
                                                                    ("base", "with ATAP", "with minimum MC"))),
        ("Wording twins (S5, same student in three wordings)", level_groups(wording, lambda r: r["wording"] or "plain",
                                                                           ("plain", "scattered", "unsupported"))),
    ]


def level_cells(rs):
    plan = [r for r in rs if r["gold_status"] == "PLAN"]
    total = [r["total_tokens"] for r in plan if r["total_tokens"] != ""]
    optimal = sum(optimal_ok(r) for r in plan)
    per_optimal = f"{sum(total) / optimal:.0f}" if total and optimal else "-"
    return [str(len(rs)), pct(sum(valid_ok(r) for r in rs), len(rs)), pct(optimal, len(plan)),
            _stats([r["completion_tokens"] for r in rs])[0], _stats([r["total_tokens"] for r in rs])[0], per_optimal]


def render_tables(tables):
    L = []
    for title, groups in tables:
        if not groups:
            continue
        L += [f"**{title}**", "",
              "| Level | Instances | Valid-answer accuracy | Optimal-plan accuracy (gold PLAN) | Median completion tokens | "
              "Median total tokens | Tokens per optimal plan |", "|---|---|---|---|---|---|---|"]
        L += [f"| {name} | " + " | ".join(level_cells(rs)) + " |" for name, rs in groups]
        L.append("")
    return L


def trend_lines(q):
    plan = [r for r in q if r["gold_status"] == "PLAN"]
    sized = [r for r in plan if r["set"] == "S1" and r["log10_omega"] != ""]
    tight = [r for r in plan if r["set"] in ("S1", "S2") and r["rho"] != ""]
    L = []
    for label, rs, key in (("log10 |Omega| (S1, gold PLAN)", sized, "log10_omega"),
                           ("capacity ratio rho (S1 and S2, gold PLAN)", tight, "rho")):
        for name, field in (("a valid answer", None), ("an optimal plan", None),
                            ("completion tokens", "completion_tokens"), ("total tokens", "total_tokens")):
            if name == "a valid answer":
                pairs = [(float(r[key]), int(valid_ok(r))) for r in rs]
            elif name == "an optimal plan":
                pairs = [(float(r[key]), int(optimal_ok(r))) for r in rs]
            else:
                pairs = [(float(r[key]), r[field]) for r in rs if r[field] != ""]
            if len(pairs) < 3:
                continue
            rho, p = spearman([x for x, _ in pairs], [y for _, y in pairs])
            if rho is not None:
                L.append(f"- {label} with {name}: rho = {rho:.2f}, p = {fmt_p(p)}, n = {len(pairs)} (normal approximation)")
    return (["**Rank correlations**", ""] + L + [""]) if L else []


def objective_class_table(q):
    plan = [r for r in q if r["gold_status"] == "PLAN"]
    groups = level_groups(plan, lambda r: r["objective"], OBJECTIVE_ORDER)
    if not groups:
        return []
    L = ["**Answer class by objective (all Q2 gold PLAN instances)**", "",
         "| Objective | Instances | " + " | ".join(CLASSES) + " |", "|---|---|" + "---|" * len(CLASSES)]
    for name, rs in groups:
        L.append(f"| {name} | {len(rs)} | " + " | ".join(pct(sum(r["class"] == c for r in rs), len(rs)) for c in CLASSES) + " |")
    return L + [""]


def no_plan_table(q):
    nop = [r for r in q if r["gold_status"] == "NO_PLAN" and r["visible"] != ""]
    if not nop:
        return []
    L = ["**Impossible requests by how the conflict is found**", "",
         "| Found by | Instances | Correct refusal | Invented plan | Wrong status |", "|---|---|---|---|---|"]
    for name, rs in level_groups(nop, lambda r: r["visible"]):
        L.append(f"| {name} | {len(rs)} | {pct(sum(r['class'] == 'correct refusal' for r in rs), len(rs))} | "
                 f"{pct(sum(r['class'] == 'invented plan' for r in rs), len(rs))} | "
                 f"{pct(sum(r['class'] == 'wrong status' for r in rs), len(rs))} |")
    L += ["", "**Impossible requests by kind**", "",
          "| Kind | Instances | Correct refusal | Invented plan | Wrong status |", "|---|---|---|---|---|"]
    for name, rs in level_groups(nop, lambda r: r["nokind"], NOKIND_ORDER):
        L.append(f"| {name} | {len(rs)} | {pct(sum(r['class'] == 'correct refusal' for r in rs), len(rs))} | "
                 f"{pct(sum(r['class'] == 'invented plan' for r in rs), len(rs))} | "
                 f"{pct(sum(r['class'] == 'wrong status' for r in rs), len(rs))} |")
    return L + [""]


def pair_counts(first, second, ok, key="base_id"):
    a = {r[key]: r for r in first}
    b = {r[key]: r for r in second}
    ids = sorted(set(a) & set(b))
    both = sum(ok(a[i]) and ok(b[i]) for i in ids)
    only_first = sum(ok(a[i]) and not ok(b[i]) for i in ids)
    only_second = sum(ok(b[i]) and not ok(a[i]) for i in ids)
    return len(ids), both, only_first, only_second


def pair_row(name, counts):
    n, both, only_first, only_second = counts
    return f"| {name} | {n} | {both} | {only_first} | {only_second} | {fmt_p(mcnemar_p(only_first, only_second))} |"


def paired_lines(q):
    labels = sorted({r["twin"] for r in q if r["twin"] not in ("", "base")})
    plan = [r for r in q if r["gold_status"] == "PLAN"]
    header = ["| Twin | Pairs | Both right | Only base right | Only twin right | p |", "|---|---|---|---|---|---|"]
    L = []
    for title, ok, population in (("Valid-answer", valid_ok, q), ("Optimal-plan", optimal_ok, plan)):
        rows = []
        for label in labels:
            counts = pair_counts([r for r in population if r["twin"] == "base"],
                                 [r for r in population if r["twin"] == label], ok)
            if counts[0]:
                rows.append(pair_row(label, counts))
        if rows:
            L += [f"**Paired twins, {title.lower()} outcome** (same student, one factor changed; exact McNemar on the "
                  f"discordant pairs)", ""] + header + rows + [""]
    near = [r for r in q if r["set"] == "S4" and r["pair_id"] != ""]
    kinds = [k for k in NOKIND_ORDER if k in {r["nokind"] for r in near}]
    rows = []
    for kind in kinds:
        counts = pair_counts([r for r in near if r["gold_status"] == "NO_PLAN" and r["nokind"] == kind],
                             [r for r in near if r["gold_status"] == "PLAN"], valid_ok, key="pair_id")
        if counts[0]:
            rows.append(pair_row(kind, counts))
    if rows:
        counts = pair_counts([r for r in near if r["gold_status"] == "NO_PLAN"],
                             [r for r in near if r["gold_status"] == "PLAN"], valid_ok, key="pair_id")
        rows.append(pair_row("all kinds", counts))
        L += ["**Impossible request against its near-miss twin, valid-answer outcome**", "",
              "| Kind | Pairs | Both right | Only impossible version right | Only near-miss right | p |",
              "|---|---|---|---|---|---|"] + rows + [""]
    return L


def as_list(value):
    return value if isinstance(value, list) else []


def code_set(value):
    return sorted({str(x).strip().upper() for x in as_list(value)})


def normal_spec(spec):
    rules = {repr(sorted((str(k), str(v).strip().upper()) for k, v in x.items()))
             for x in as_list(spec.get("rules")) if isinstance(x, dict)}
    caps = spec.get("sem_caps")
    return {
        "query": spec.get("query"),
        "current_sem": spec.get("current_sem"),
        "completed": code_set(spec.get("completed")),
        "must_take": code_set(spec.get("must_take")),
        "mc_max": spec.get("mc_max", 20),
        "mc_min": spec.get("mc_min"),
        "sem_caps": {str(k): v for k, v in caps.items()} if isinstance(caps, dict) else {},
        "atap_sems": sorted(str(x) for x in as_list(spec.get("atap_sems"))) if "atap_sems" in spec else None,
        "objective": spec.get("objective", "none"),
        "early": code_set(spec.get("early")),
        "late": code_set(spec.get("late")),
        "rules": sorted(rules),
        "unsupported": bool(as_list(spec.get("unsupported"))),
        "programme": spec.get("programme"),
    }


def b_section(items):
    b = [(inst, rec, row) for inst, rec, row in items
         if row["set"] and rec and "spec" in rec]
    if not b:
        return []

    def right(row):
        return optimal_ok(row) if row["gold_status"] == "PLAN" else valid_ok(row)

    no_json = [x for x in b if x[1].get("parse_error")]
    rejected = [x for x in b if not x[1].get("parse_error") and x[2]["status"] == "INVALID_SPEC"]
    differing = []
    field_counts, field_right = Counter(), Counter()
    exact = 0
    dropped = 0
    for inst, rec, row in b:
        if not isinstance(rec.get("spec"), dict):
            continue
        gold, model = normal_spec(inst["gold_spec"]), normal_spec(rec["spec"])
        diff = [f for f in SPEC_FIELDS if gold[f] != model[f]]
        exact += not diff
        if diff:
            differing.append(right(row))
        for f in diff:
            field_counts[f] += 1
            field_right[f] += right(row)
        dropped += gold["unsupported"] and not model["unsupported"]
    false_missing = sum(x[2]["status"] == "MISSING_INFO" and x[2]["gold_status"] != "MISSING_INFO" for x in b)
    missed_missing = sum(x[2]["gold_status"] == "MISSING_INFO" and x[2]["status"] != "MISSING_INFO" for x in b)
    false_scope = sum(x[2]["status"] == "OUT_OF_SCOPE" and x[2]["gold_status"] != "OUT_OF_SCOPE" for x in b)
    L = ["**Pipeline B: what happened to the spec (Q2 instances)**", "", "| Event | Instances |", "|---|---|",
         f"| reply has no usable JSON | {pct(len(no_json), len(b))} |",
         f"| spec rejected by the schema (INVALID_SPEC) | {pct(len(rejected), len(b))} |",
         f"| spec equals the gold spec in every compared field | {pct(exact, len(b))} |",
         f"| spec differs from the gold spec in at least one field | {pct(len(differing), len(b))} |",
         f"| of these, the final answer is still right | {pct(sum(differing), len(differing))} |",
         f"| false MISSING_INFO (gold is not MISSING_INFO) | {pct(false_missing, len(b))} |",
         f"| MISSING_INFO not given (gold is MISSING_INFO) | {pct(missed_missing, len(b))} |",
         f"| false OUT_OF_SCOPE (gold is not OUT_OF_SCOPE) | {pct(false_scope, len(b))} |",
         f"| unsupported wish dropped from the spec | {pct(dropped, len(b))} |", ""]
    if field_counts:
        L += ["| Field that differs from gold | Specs | Final answer still right |", "|---|---|---|"]
        for f, n in field_counts.most_common():
            L.append(f"| {f} | {n} | {pct(field_right[f], n)} |")
        L.append("")
    return L


def q2_section(rows, items):
    q = [r for r in rows if r["set"]]
    if not q:
        return []
    L = ["", "## Q2 factors", "",
         "Valid-answer accuracy: every instance in the level. Optimal-plan accuracy: the gold PLAN instances in the level "
         "only. Tokens are medians over the instances in the level; tokens per optimal plan is the total tokens of the "
         "level's gold PLAN instances divided by its optimal plans.", ""]
    L += render_tables(q2_tables(q))
    L += trend_lines(q)
    L += objective_class_table(q)
    L += no_plan_table(q)
    L += paired_lines(q)
    L += b_section(items)
    return L


def metric_lines(rows):
    plan = [r for r in rows if r["gold_status"] == "PLAN"]
    nop = [r for r in rows if r["gold_status"] == "NO_PLAN"]
    valid_plans = sum(valid_ok(r) for r in plan)
    optimal = sum(optimal_ok(r) for r in plan)
    L = [f"- valid-answer accuracy (status equals gold; for PLAN, no hard rule broken), all instances: "
         f"{pct(sum(valid_ok(r) for r in rows), len(rows))}"]
    if plan:
        L += [f"- valid-answer accuracy, gold PLAN instances: {pct(valid_plans, len(plan))}",
              f"- optimal-plan accuracy (objective, then fewest added courses, then most preferences), gold PLAN instances: "
              f"{pct(optimal, len(plan))}",
              f"- valid plans that are not optimal: {pct(valid_plans - optimal, valid_plans)}",
              f"- over-refusal (gold PLAN answered NO_PLAN): {pct(sum(r['class'] == 'over-refusal' for r in plan), len(plan))}"]
        beats = sum(r["class"] == "BEATS GOLD: check" for r in plan)
        if beats:
            L.append(f"- plans better than the gold plan (check the gold answer): {beats}")
    if nop:
        L += [f"- correct refusal, gold NO_PLAN instances: {pct(sum(r['class'] == 'correct refusal' for r in nop), len(nop))}",
              f"- invented plan, gold NO_PLAN instances: {pct(sum(r['class'] == 'invented plan' for r in nop), len(nop))}"]
    return L


def valid_cell(rs):
    return pct(sum(valid_ok(r) for r in rs), len(rs))


def optimal_cell(rs):
    plan = [r for r in rs if r["gold_status"] == "PLAN"]
    return pct(sum(optimal_ok(r) for r in plan), len(plan))


def class_cell(status, cls):
    def cell(rs):
        group = [r for r in rs if r["gold_status"] == status]
        return pct(sum(r["class"] == cls for r in group), len(group))
    return cell


HEADLINE = (
    ("Instances", lambda rs: str(len(rs))),
    ("Valid-answer accuracy, all instances", valid_cell),
    ("Valid-answer accuracy, gold PLAN", lambda rs: valid_cell([r for r in rs if r["gold_status"] == "PLAN"])),
    ("Optimal-plan accuracy, gold PLAN", optimal_cell),
    ("Correct refusal, gold NO_PLAN", class_cell("NO_PLAN", "correct refusal")),
    ("Invented plan, gold NO_PLAN", class_cell("NO_PLAN", "invented plan")),
    ("Over-refusal, gold PLAN", class_cell("PLAN", "over-refusal")),
    ("Median completion tokens", lambda rs: _stats([r["completion_tokens"] for r in rs])[0]),
    ("Median total tokens", lambda rs: _stats([r["total_tokens"] for r in rs])[0]),
)


def compare_text(names, all_rows):
    cols = " | ".join(names)
    sep = "|---|" + "---|" * len(names)
    L = ["# Comparison", "", "## Headline", "", f"| | {cols} |", sep]
    for label, fn in HEADLINE:
        L.append(f"| {label} | " + " | ".join(fn(rs) for rs in all_rows) + " |")
    per_dir = [q2_tables([r for r in rs if r["set"]]) for rs in all_rows]
    if any(r["set"] for rs in all_rows for r in rs):
        L += ["", "## Q2 factors", ""]
        for i, (title, _) in enumerate(per_dir[0]):
            levels = []
            for tables in per_dir:
                levels += [name for name, _ in tables[i][1] if name not in levels]
            if not levels:
                continue
            for metric, cell in (("valid-answer accuracy", valid_cell), ("optimal-plan accuracy (gold PLAN)", optimal_cell)):
                L += [f"**{title}: {metric}**", "", f"| Level | {cols} |", sep]
                for level in levels:
                    L.append(f"| {level} | " + " | ".join(cell(dict(tables[i][1]).get(level, [])) for tables in per_dir) + " |")
                L.append("")
    return "\n".join(L) + "\n"


def write_resources(out, items):
    """RESOURCES.md: token and time figures from the saved records. Written to a file only, never printed."""
    n = len(items)
    use = [(rec.get("usage") or {}) for _, rec, _ in items]
    tot = [u.get("total_tokens") for u in use]
    L = [f"# Resources: {out}", "", f"{n} instances. Token counts are as reported by the API. Seconds are wall-clock under the "
         f"worker count saved in each record, on a shared server: indicative only.", "",
         "| Quantity | Median | 95th percentile | Max |", "|---|---|---|---|"]
    for name, vals in (("prompt tokens", [u.get("prompt_tokens") for u in use]),
                       ("completion tokens", [u.get("completion_tokens") for u in use]),
                       ("total tokens", tot),
                       ("reasoning tokens (when the API reports them)",
                        [(u.get("completion_tokens_details") or {}).get("reasoning_tokens") for u in use]),
                       ("seconds per instance (whole)", [rec.get("seconds") for _, rec, _ in items]),
                       ("seconds of the successful request", [u.get("request_seconds") for u in use]),
                       ("solver seconds (pipeline B)", [rec.get("solver_seconds") for _, rec, _ in items])):
        L.append(f"| {name} | " + " | ".join(_stats(vals)) + " |")
    known = [t for t in tot if t is not None]
    cut = sum(u.get("finish_reason") == "length" for u in use)
    retried = sum((u.get("attempts") or 1) > 1 for u in use)
    rows = [r for _, _, r in items]
    plan_tokens = [(rec.get("usage") or {}).get("total_tokens") for _, rec, r in items if r["gold_status"] == "PLAN"]
    plan_tokens = [t for t in plan_tokens if t is not None]
    valid = sum(valid_ok(r) for r in rows)
    optimal = sum(optimal_ok(r) for r in rows)
    L += ["", f"- instances with a reply cut off at max_tokens: {cut} ({(Decimal(100 * cut) / n).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)}%)",
          f"- instances that needed more than one API attempt: {retried}",
          f"- total tokens over all instances: {sum(known)}"] + metric_lines(rows)
    if known:
        L.append(f"- tokens per valid answer (all instances): {sum(known) / valid:.0f}" if valid
                 else "- tokens per valid answer: none valid")
    if plan_tokens:
        L.append(f"- tokens per optimal plan (total tokens of the gold PLAN instances / optimal plans): {sum(plan_tokens) / optimal:.0f}"
                 if optimal else "- tokens per optimal plan: none optimal")
    kitems = [(r["k"], (rec, r)) for _, rec, r in items if r["k"] != ""]
    if kitems:
        L += ["", "## Tokens and seconds by decision size k (Q1 requests whose target is in the catalogue)", "",
              "Equal-size bins by rank of k; medians. Seconds are indicative only (shared server).", "",
              "| k | Instances | Median prompt tokens | Median completion tokens | Median total tokens | Median seconds |",
              "|---|---|---|---|---|---|"]
        for lo, hi, sub in k_bins(kitems):
            def med(f):
                return _stats([f(rec) for rec, _ in sub])[0]
            L.append(f"| {lo}-{hi} | {len(sub)} | {med(lambda x: (x.get('usage') or {}).get('prompt_tokens'))} | "
                     f"{med(lambda x: (x.get('usage') or {}).get('completion_tokens'))} | "
                     f"{med(lambda x: (x.get('usage') or {}).get('total_tokens'))} | {med(lambda x: x.get('seconds'))} |")
        pairs = [(k, (rec.get("usage") or {}).get("total_tokens")) for k, (rec, _) in kitems]
        pairs = [(k, t) for k, t in pairs if t is not None]
        rho, p = spearman([k for k, _ in pairs], [t for _, t in pairs]) if len(pairs) > 2 else (None, None)
        if rho is not None:
            L += ["", f"Spearman correlation of k with total tokens: rho = {rho:.2f}, p = {fmt_p(p)} (normal approximation)"]
    (out / "RESOURCES.md").write_text("\n".join(L) + "\n")


def grade_dir(out, insts, catalog):
    rows, usage, repairs, cut, items = [], Counter(), Counter(), 0, []
    for inst in insts:
        f = out / f"{inst['id']}.json"
        if not f.exists():
            continue
        rec = json.loads(f.read_text())
        for k_, v_ in (rec.get("usage") or {}).items():
            if isinstance(v_, int):
                usage[k_] += v_
        repairs[rec.get("repair") or ("none" if rec.get("answer") or rec.get("spec") else "unparseable")] += 1
        cut += (rec.get("usage") or {}).get("finish_reason") == "length"
        rows.append(grade_one(inst, rec))
        if catalog and (inst.get("meta") or {}).get("role"):
            rows[-1]["k"] = decision_size(inst, catalog)
        items.append((inst, rec, rows[-1]))
    if not rows:
        raise SystemExit(f"no answers in {out}")
    with open(out / "graded.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    if any(r["role"] for r in rows):
        names = {"ELIGIBLE": "eligible", "NOT_ELIGIBLE": "not eligible", "MISSING_INFO": "missing info",
                 "OUT_OF_SCOPE": "out of scope"}
    elif any(r["set"] for r in rows):
        names = {"PLAN": "plan", "NO_PLAN": "no plan", "MISSING_INFO": "missing info", "OUT_OF_SCOPE": "out of scope"}
    else:
        names = None
    if names:
        groups = [(names[k], [r for r in rows if r["gold_status"] == k]) for k in names]
        title = "## Status accuracy by gold answer"
    else:
        by = defaultdict(list)
        for r in rows:
            by[r["group"]].append(r)
        groups = sorted(by.items())
        title = "## Status accuracy by group"
    L = [f"# Results: {out}", "", f"{len(rows)} of {len(insts)} instances answered.", "",
         title, "", "| Group | Correct status |", "|---|---|"]
    L += [f"| {g} | {pct(sum(r['status_correct'] for r in rs), len(rs))} |" for g, rs in groups if rs]
    L += [f"| **all** | {pct(sum(r['status_correct'] for r in rows), len(rows))} |"]
    feas = [r for r in rows if r["gold_status"] == "PLAN"]
    if feas:
        L += ["", "## Agreed metrics", ""] + metric_lines(rows)
    L += ["", "## Feasible plan requests (gold = PLAN)", "", "| Class | Count |", "|---|---|"]
    L += [f"| {c} | {pct(n, len(feas))} |" for c, n in Counter(r["class"] for r in feas).most_common()]
    for sub in ("q2/loose", "q2/tight"):
        rs = [r for r in feas if r["kind"] == sub]
        if rs:
            valid = sum(valid_ok(r) for r in rs)
            L += [f"\n{sub}: valid {pct(valid, len(rs))}, optimal {pct(sum(r['class'] == 'optimal' for r in rs), len(rs))}"]
    rules = Counter(v.split()[0] for r in feas for v in r["violations"].split(" | ") if v)
    if rules:
        L += ["", "Hard rules broken in invalid plans (R numbers = SOLVER_GUIDE section 4):", ""]
        L += [f"- {k}: {n}" for k, n in rules.most_common()]
    inf = [r for r in rows if r["gold_status"] == "NO_PLAN"]
    L += ["", "## Impossible requests (gold = NO_PLAN)", "",
          "| Kind | Correct refusal | Invented plan |", "|---|---|---|"]
    for kind in sorted({r["kind"] for r in inf}):
        rs = [r for r in inf if r["kind"] == kind]
        L += [f"| {kind} | {pct(sum(r['class'] == 'correct refusal' for r in rs), len(rs))} |"
              f" {pct(sum(r['class'] == 'invented plan' for r in rs), len(rs))} |"]
    L += ["", "## Format", "", f"- unparseable replies: {sum(r['status'] == 'UNPARSEABLE' for r in rows)}",
          f"- replies that needed repair before parsing: {sum(r['fenced'] for r in rows)}",
          f"- repair kinds (clean = none needed): {dict(repairs)}",
          f"- replies cut off at max_tokens: {cut}"]
    clean = [r for r in rows if not r["fenced"] and r["status"] != "UNPARSEABLE"]
    rep = [r for r in rows if r["fenced"]]
    cc, rc = sum(r["status_correct"] for r in clean), sum(r["status_correct"] for r in rep)
    L += [f"- accuracy counting repaired replies by their answer: {pct(sum(r['status_correct'] for r in rows), len(rows))}",
          f"- strict accuracy (clean replies only count): {pct(cc, len(rows))}",
          f"- clean replies right: {pct(cc, len(clean))}; repaired replies right: {pct(rc, len(rep))}"
          + (f"; Fisher exact p = {fmt_p(fisher_p(cc, len(clean) - cc, rc, len(rep) - rc))}" if clean and rep else "")]
    if feas:
        for name, ok, pool in (("valid-answer", valid_ok, rows), ("optimal-plan", optimal_ok, feas)):
            pool_clean = [r for r in pool if not r["fenced"] and r["status"] != "UNPARSEABLE"]
            pool_rep = [r for r in pool if r["fenced"]]
            c, p = sum(ok(r) for r in pool_clean), sum(ok(r) for r in pool_rep)
            L += [f"- {name} accuracy, clean replies: {pct(c, len(pool_clean))}; repaired replies: {pct(p, len(pool_rep))}"
                  + (f"; Fisher exact p = {fmt_p(fisher_p(c, len(pool_clean) - c, p, len(pool_rep) - p))}" if pool_clean and pool_rep else ""),
                  f"- {name} accuracy counting only clean replies as right (strict): {pct(c, len(pool))}"]
    L += q1_section(rows)
    L += q2_section(rows, items)
    if usage:
        L += [f"- token usage: {dict(usage)}"]
    (out / "SUMMARY.md").write_text("\n".join(L) + "\n")
    write_resources(out, items)
    return L, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results_dirs", nargs="+")
    ap.add_argument("--instances", default=str(ROOT / "instances/instances.json"))
    ap.add_argument("--compare-out", default="COMPARE.md")
    a = ap.parse_args()
    insts = json.loads(Path(a.instances).read_text())
    catalog = None
    if any((i.get("meta") or {}).get("role") for i in insts):
        from m1_data.catalog import Catalog
        catalog = Catalog.load()
    graded = []
    for d in a.results_dirs:
        out = Path(d)
        L, rows = grade_dir(out, insts, catalog)
        graded.append(("/".join(out.parts[-2:]), rows))
        if len(a.results_dirs) == 1:
            print("\n".join(L))
            print(f"\nresource figures written to {out / 'RESOURCES.md'}")
        else:
            print(f"{out}: {len(rows)} of {len(insts)} instances graded, tables in {out / 'SUMMARY.md'}")
    if len(graded) > 1:
        Path(a.compare_out).write_text(compare_text([n for n, _ in graded], [r for _, r in graded]))
        print(f"side-by-side tables written to {a.compare_out}")


if __name__ == "__main__":
    main()
