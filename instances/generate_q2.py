"""Q2 instance set (900 requests).

    python -m instances.generate_q2
    python -m instances.generate_q2 --seed 3263 --out instances/q2_900.json
"""
from __future__ import annotations

import argparse
import copy
import json
import math
import pickle
import random
import time
from collections import Counter
from pathlib import Path

from ortools.sat.python import cp_model

from eval.checker import check_plan
from m1_data.catalog import Catalog
from solver import objectives
from solver.backtrack import Search, solve_with_stats
from solver.common import ATAP_CODE, term_of
from solver.run import prepare, run

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
C = json.loads((ROOT / "data/processed/AY2026-2027/catalog.json").read_text())["courses"]

ROADMAP = {
    1: ["CS1101S", "CS1231S", "MA1521", "ES2660"],
    2: ["CS2030S", "CS2040S", "MA1522", "IS1108"],
    3: ["CS2100", "CS2101", "CS2103T", "ST2334"],
    4: ["CS2106", "CS2109S", "CS3230"],
    5: ["CS2105", "CS3219"],
    6: ["CS2102"],
}
CORE = [c for s in sorted(ROADMAP) for c in ROADMAP[s]]
LEAVES = ["ES2660", "IS1108", "CS2101", "ST2334", "CS3230", "CS2105", "CS2102"]
BANDS = {"1-2": (1, 2), "3-4": (3, 4), "5-6": (5, 6), "7-8": (7, 8)}
CELLS = [(b, m) for b in ("1-2", "3-4") for m in (2, 4, 6, 8, 10, 12)] + \
        [("5-6", m) for m in (2, 4, 6, 8, 10)] + [("7-8", m) for m in (2, 4)]
OBJECTIVES = ["none", "earliest_graduation", "min_total_mc"]
NO_PLAN_KINDS = ["capacity", "exclusion", "parity", "chain", "rule_conflict", "hidden"]
VISIBLE = {"capacity": "lookup", "exclusion": "lookup", "parity": "lookup",
           "chain": "search", "rule_conflict": "search", "hidden": "search"}
RHO_BINS = [(0.4, 0.6), (0.6, 0.8), (0.8, 1.0)]

UNSUPPORTED = {
    "lighter final semester": ["I'd like my final semester to be lighter than the others.",
                               "Can the last semester be a lighter one?"],
    "even workload across semesters": ["Please keep my workload roughly the same every semester.",
                                       "I don't want one semester much heavier than another."],
    "no Friday classes": ["I'd rather not have classes on Fridays.", "Keep my Fridays free if you can."],
    "at most two exam modules per semester": ["I want at most two modules with final exams in a semester."],
    "avoid heavy group projects": ["I'd like to avoid modules with heavy group projects."],
    "take modules with a friend": ["My friend and I want to take our modules together where possible."],
    "S/U a module": ["I may S/U one of my modules."],
    "may retake a failed module": ["There's a chance I fail one module this semester and have to retake it."],
    "waiver request": ["I'm also applying to have one module waived."],
    "prefers a specific lecturer": ["I'd like modules taught by my favourite lecturer when possible."],
}
OTHER_PROGRAMMES = [("Business Analytics", "I am a Business Analytics student."),
                    ("Information Systems", "I'm in the Information Systems programme."),
                    ("Computer Engineering", "I study Computer Engineering."),
                    ("Information Security", "I am an Information Security student."),
                    ("Data Science and Analytics", "My programme is Data Science and Analytics.")]
SECOND_MAJORS = ["Mathematics", "Statistics", "Economics", "Physics", "Psychology"]
MINORS = ["Economics", "Mathematics", "Management", "Philosophy", "Statistics"]
NOT_IN_CATALOGUE = ["CS5340", "CS5242", "CS5228", "CS5331", "LAJ1201"]


class GenError(Exception):
    pass


STATUSES: list = []
_solve = objectives.solve


def _recording_solve(pm, expr=None, maximize=False):
    status, solver = _solve(pm, expr, maximize)
    STATUSES.append(status)
    return status, solver


objectives.solve = _recording_solve
objectives.TIME_LIMIT_SECONDS = 20


def sem_words(r, n):
    y, s = (n + 1) // 2, 2 - n % 2
    return r.choice([f"Y{y}S{s}", f"year {y} semester {s}", f"semester {n}"])


def listing(codes):
    codes = list(codes)
    if len(codes) == 1:
        return codes[0]
    return ", ".join(codes[:-1]) + " and " + codes[-1]


def mods(mc):
    return f"{mc // 4} module{'s' if mc // 4 != 1 else ''}"


def cap_of(spec, s):
    return (spec.get("sem_caps") or {}).get(str(s), spec.get("mc_max", 20))


def rules_of(spec, strength):
    return [x for x in spec.get("rules", []) if x["strength"] == strength]


def n_prefs(spec):
    return len(rules_of(spec, "prefer")) + len(spec.get("early", [])) + len(spec.get("late", []))


class Q2Gen:
    def __init__(self, seed):
        self.r = random.Random(seed)
        self.cat = Catalog.load()
        self.pool = sorted(c for c, x in C.items()
                           if c[:3] in ("CS3", "CS4") and x["exists_in_ay"] and x["available"]
                           and x.get("details") != "stub" and x["mc"] == 4 and not c.endswith("R"))
        self.deep_pool = [c for c in self.pool if self.depth(c) >= 4]
        self.one_term = [c for c in self.pool if len([t for t in C[c]["offered"] if t in (1, 2)]) == 1]
        self.solves = 0
        self.cache = {}
        self.budget_end = None

    def depth(self, c, seen=()):
        if c in seen or c not in C:
            return 0
        ds = [d for d in (C[c]["prereq"].get("courses") or []) if d in C
              and C[d]["exists_in_ay"] and C[d].get("details") != "stub"]
        return 1 + max([self.depth(d, seen + (c,)) for d in ds] or [0])

    def unmet_depth(self, c, done, seen=()):
        if c in done or c in seen or c not in C:
            return 0
        ds = [d for d in (C[c]["prereq"].get("courses") or []) if d in C and C[d]["exists_in_ay"]
              and C[d].get("details") != "stub"]
        if not ds or self.cat.can_take(c, set(done))[0]:
            return 0
        best = min((self.unmet_depth(d, done, seen + (c,)) for d in ds if self.reachable(d, done)), default=0)
        return 1 + best

    def offered(self, c, s):
        return term_of(s) in C[c]["offered"]

    # ---------- solving ----------
    def gold(self, spec):
        if self.budget_end and time.time() > self.budget_end:
            raise GenError("budget")
        STATUSES.clear()
        self.solves += 1
        ans = run(copy.deepcopy(spec), self.cat)
        ok = True
        if ans["status"] == "PLAN":
            ok = bool(STATUSES) and all(s == cp_model.OPTIMAL for s in STATUSES) and not check_plan(spec, ans["plan"])
        elif ans["status"] == "NO_PLAN":
            ok = not any("ran out of time" in x for x in ans.get("reasons", []))
        return ans, ok

    def cached(self, spec):
        key = json.dumps(spec, sort_keys=True)
        if key not in self.cache:
            self.cache[key] = self.gold(spec)
        return self.cache[key]

    def plan_ok(self, spec):
        ans, ok = self.cached(spec)
        return copy.deepcopy(ans) if ok and ans["status"] == "PLAN" else None

    def no_plan_ok(self, spec):
        ans, ok = self.cached(spec)
        return copy.deepcopy(ans) if ok and ans["status"] == "NO_PLAN" else None

    def measure(self, spec):
        early, cleaned, _ = prepare(copy.deepcopy(spec), self.cat)
        if early is not None:
            return {}
        s = Search(cleaned, self.cat, "mac", time.time() + 60)
        needed = sum(C[c]["mc"] or 0 for c in s.required if c != ATAP_CODE and c in C)
        room = sum(s.cap(x) for x in s.sems)
        out = {"rho": round(needed / room, 3) if room else None, "n_sems": len(s.sems),
               "n_cand": len(s.candidates), "needed_mc": needed, "room_mc": room}
        if not s.reasons and hasattr(s, "initial"):
            out["log10_omega"] = round(sum(math.log10(len(v)) for v in s.initial.values() if v), 2)
        return out

    def needed_room(self, spec):
        m = self.measure(spec)
        return m.get("needed_mc", 0), m.get("room_mc", 0)

    # ---------- transcripts and must-take lists ----------
    def sim(self, k):
        done = [c for s in ROADMAP if s < k for c in ROADMAP[s]]
        for c in self.r.sample(LEAVES, self.r.randint(0, 2)):
            if c in done:
                done.remove(c)
        for s in range(4, k):
            if self.r.random() < 0.6:
                ok = [c for c in self.pool if c not in done and self.cat.can_take(c, set(done), term_of(s))[0]
                      and self.depth(c) <= 5]
                if ok:
                    done.append(self.r.choice(ok))
        return done

    def reachable(self, c, done):
        return (c not in done and c in C and C[c]["exists_in_ay"] and C[c]["available"]
                and not self.cat.blocked_by(c, set(done)) and self.cat.reachable(c, set(done))[0])

    def must_list(self, done, m, k):
        r = self.r
        rem = [c for c in CORE if c not in done]
        deep = [c for c in self.deep_pool if self.reachable(c, done) and not self.cat.can_take(c, set(done))[0]]
        el = [c for c in self.pool if self.reachable(c, done)]
        n_deep = min(len(deep), r.randint(0, max(1, m // 3)) if k <= 6 else r.randint(0, 1))
        n_core = min(len(rem), r.randint(m // 3, m - n_deep))
        must = r.sample(rem, n_core) + r.sample(deep, n_deep)
        rest = [c for c in el if c not in must]
        r.shuffle(rest)
        for c in rest:
            if len(must) >= m:
                break
            if not any(c in (C[x]["preclusion"].get("mutually_exclusive_with") or []) for x in must):
                must.append(c)
        if len(must) != m:
            raise GenError("must list")
        r.shuffle(must)
        return must

    def base(self, k, m, caps=True):
        r = self.r
        done = self.sim(k)
        spec = {"query": "plan", "current_sem": k, "completed": done, "must_take": self.must_list(done, m, k)}
        if r.random() < 0.3:
            spec["programme"] = "BComp CS Hons"
        if caps:
            x = r.random()
            if x < 0.25:
                spec["mc_max"] = 16
            elif x < 0.45:
                spec["mc_max"] = 12
            if k <= 7 and r.random() < 0.3:
                spec["sem_caps"] = {str(r.randint(k + 1, 8)): 0}
        return spec

    def placed(self, ans):
        return {c: int(s) for s, cs in ans["plan"].items() for c in cs}

    def usable(self, spec):
        return [s for s in range(spec["current_sem"], 9) if cap_of(spec, s) > 0]

    # ---------- rules and preferences ----------
    def make_rules(self, spec, where, n, strength, bind_p=0.5, extra_p=0.0, taken=None):
        r = self.r
        must = spec["must_take"]
        done = set(spec["completed"])
        taken = set(taken or ())
        for x in spec.get("rules", []):
            taken.add(self.rule_key(x))
        out = []
        for _ in range(400):
            if len(out) == n:
                return out
            t = r.choices(["before", "apart", "same_sem", "in_sem"], weights=[35, 20, 20, 25])[0]
            bind = r.random() < bind_p
            if t == "in_sem":
                c = None
                if extra_p and r.random() < extra_p:
                    opts = [x for x in self.pool if self.reachable(x, done) and x not in must
                            and x not in where and self.unmet_depth(x, done) <= 3]
                    c = r.choice(opts) if opts else None
                c = c or r.choice(must)
                sems = [s for s in self.usable(spec) if self.offered(c, s)]
                if c not in where:
                    sems = [s for s in sems if s >= spec["current_sem"] + self.unmet_depth(c, done)]
                if c in where and bind:
                    sems = [s for s in sems if s != where[c] and s >= where[c] - 1]
                elif c in where:
                    sems = [where[c]] if where[c] in sems else []
                if not sems:
                    continue
                rule = {"type": "in_sem", "course": c, "sem": r.choice(sems), "strength": strength}
            else:
                if len(must) < 2:
                    continue
                a, b = r.sample(must, 2)
                pa, pb = where.get(a), where.get(b)
                if pa is None or pb is None:
                    continue
                if t == "before":
                    holds = pa < pb
                    if holds == bind:
                        if pa == pb:
                            continue
                        a, b = b, a
                else:
                    holds = (pa != pb) if t == "apart" else (pa == pb)
                    if holds == bind:
                        continue
                rule = {"type": t, "a": a, "b": b, "strength": strength}
            key = self.rule_key(rule)
            if key in taken or (rule["type"] != "in_sem" and ("pair", frozenset((rule["a"], rule["b"]))) in taken):
                continue
            taken.add(key)
            if rule["type"] != "in_sem":
                taken.add(("pair", frozenset((rule["a"], rule["b"]))))
            out.append(rule)
        raise GenError("rules")

    def rule_key(self, x):
        if x["type"] == "in_sem":
            return ("in", x["course"])
        return ("pair", frozenset((x["a"], x["b"])))

    def make_prefs(self, spec, where, n):
        r = self.r
        must = [c for c in required_courses(spec) if c in where]
        used = {c for x in spec.get("rules", []) if x["type"] == "in_sem" for c in [x["course"]]}
        timed = set(spec.get("early", [])) | set(spec.get("late", []))
        out = []
        for _ in range(120):
            if len(out) == n:
                return out
            kind = r.choices(["rule", "early", "late"], weights=[55, 25, 20])[0]
            if kind == "rule":
                try:
                    got = self.make_rules({**spec, "must_take": must,
                                           "rules": spec.get("rules", []) + [x for k_, x in out if k_ == "rule"]},
                                          where, 1, "prefer", bind_p=0.6)
                except GenError:
                    continue
                out.append(("rule", got[0]))
                continue
            opts = [c for c in must if c not in timed and c not in used]
            if not opts:
                continue
            c = r.choice(opts)
            timed.add(c)
            out.append((kind, c))
        raise GenError("prefs")

    def with_prefs(self, spec, prefs):
        s = copy.deepcopy(spec)
        for kind, x in prefs:
            if kind == "rule":
                s.setdefault("rules", []).append(x)
            else:
                s.setdefault(kind, []).append(x)
        return s

    def with_rules(self, spec, rules):
        s = copy.deepcopy(spec)
        if rules:
            s["rules"] = list(rules) + s.get("rules", [])
        return s

    def set_objective(self, spec, objective):
        s = copy.deepcopy(spec)
        s.pop("objective", None)
        if objective != "none":
            s["objective"] = objective
        return s

    # ---------- feasible plans ----------
    def build_plan(self, k, m, n_rules, n_p, objective, tries=60):
        for _ in range(tries):
            try:
                spec = self.set_objective(self.base(k, m), objective)
                a0 = self.plan_ok(spec)
                if not a0:
                    continue
                for _ in range(6):
                    rules = self.make_rules(spec, self.placed(a0), n_rules, "must", extra_p=0.6 if m <= 3 else 0.15)
                    s1 = self.with_rules(spec, rules)
                    a1 = self.plan_ok(s1)
                    if a1:
                        break
                else:
                    continue
                for _ in range(6):
                    prefs = self.make_prefs(s1, self.placed(a1), n_p)
                    s2 = self.with_prefs(s1, prefs)
                    a2 = self.plan_ok(s2)
                    if a2:
                        return {"spec": s2, "answer": a2, "core": spec, "rules": rules, "prefs": prefs,
                                "objective": objective}
            except GenError:
                continue
        raise GenError(f"plan k={k} m={m}")


# ---------- rendering ----------
def sem_sentence(r, k):
    return r.choice([f"I am in {sem_words(r, k)} now.", f"I am currently in {sem_words(r, k)}.",
                     f"This semester is {sem_words(r, k)} for me.", f"I'm starting {sem_words(r, k)}."])


def done_sentence(r, done):
    done = list(done)
    r.shuffle(done)
    if not done:
        return "I have not completed any module yet."
    return r.choice([f"I have completed {listing(done)}.", f"I've finished {listing(done)}.",
                     f"So far I have passed {listing(done)}.", f"My completed modules are {listing(done)}."])


def must_sentence(r, must):
    must = list(must)
    r.shuffle(must)
    return r.choice(["I still have to take ", "I need to take ", "I must take ",
                     "My remaining required modules are "]) + listing(must) + "."


def rule_sentence(r, x):
    mw = x["strength"] == "must"
    t = x["type"]
    if t == "in_sem":
        c, s = x["course"], x["sem"]
        return (r.choice([f"{c} has to be in semester {s}.", f"I must take {c} in {sem_words(r, s)}."]) if mw
                else r.choice([f"If possible, I would like {c} in semester {s}.", f"Ideally {c} would be in {sem_words(r, s)}."]))
    a, b = x["a"], x["b"]
    if t == "before":
        return (r.choice([f"{a} must come before {b}.", f"I need to finish {a} before I start {b}."]) if mw
                else r.choice([f"Ideally I'd take {a} before {b}.", f"I'd rather do {a} before {b}."]))
    if t == "apart":
        return (r.choice([f"{a} and {b} must not be in the same semester.", f"I definitely can't have {a} and {b} together."]) if mw
                else r.choice([f"I'd prefer {a} and {b} in different semesters.", f"If possible, keep {a} and {b} apart."]))
    return (r.choice([f"{a} and {b} must be in the same semester.", f"I have to take {a} and {b} together in one semester."]) if mw
            else r.choice([f"I would like {a} and {b} together in one semester.", f"Ideally {a} and {b} go in the same semester."]))


def fact_sentences(r, spec):
    facts = []
    k = spec.get("current_sem")
    if "mc_max" in spec:
        m = spec["mc_max"]
        facts.append(("mc_max", r.choice([f"I can take at most {m} MC per semester.", f"At most {mods(m)} per semester.",
                                          f"My limit is {m} MC each semester."])))
    caps = dict(spec.get("sem_caps", {}))
    atap = spec.get("atap_sems")
    if atap:
        if len(atap) == 1:
            s_ = atap[0]
            if caps.get(str(s_)) == 1:
                facts.append(("atap", f"Semester {s_} is my ATAP semester and I do not want any other module in it."))
                caps.pop(str(s_))
            else:
                facts.append(("atap", r.choice([f"I will do ATAP in semester {s_}.", f"My ATAP internship is in {sem_words(r, s_)}."])))
        elif k is not None and atap == list(range(k, 9)):
            facts.append(("atap", r.choice(["I will also do ATAP, in whichever semester fits.",
                                            "I plan to do ATAP at some point, no particular semester."])))
        else:
            facts.append(("atap", "I will do ATAP in " + " or ".join(f"semester {s_}" for s_ in atap) + "."))
    for s_, cap in sorted(caps.items(), key=lambda x: int(x[0])):
        if cap == 0:
            facts.append(("caps", r.choice([f"Semester {s_} is my exchange semester.", f"I will do NOC in semester {s_}.",
                                            f"I will be away on exchange in {sem_words(r, int(s_))}, so no modules then.",
                                            f"I'm taking a leave of absence in semester {s_}."])))
        else:
            facts.append(("caps", f"In semester {s_} I can only take {mods(cap) if cap % 4 == 0 else str(cap) + ' MC'}."))
    if "mc_min" in spec:
        m = spec["mc_min"]
        facts.append(("mc_min", r.choice([f"In any semester where I take modules, I want at least {m} MC.",
                                          f"Whenever I study in a semester it should be at least {mods(m)}; a semester with no modules is fine."])))
    obj = spec.get("objective")
    if obj == "earliest_graduation":
        facts.append(("objective", r.choice(["I want to graduate as early as possible.", "Please use the fewest semesters.",
                                             "Finishing as soon as possible matters most to me."])))
    elif obj == "min_total_mc":
        facts.append(("objective", r.choice(["I want the fewest total credits.", "Please keep my total MC as low as possible."])))
    for x in rules_of(spec, "must"):
        facts.append(("must_rule", rule_sentence(r, x)))
    for x in rules_of(spec, "prefer"):
        facts.append(("pref", rule_sentence(r, x)))
    for c in spec.get("early", []):
        facts.append(("pref", r.choice([f"I would like {c} as early as possible.", f"{c} as early as possible, please."])))
    for c in spec.get("late", []):
        facts.append(("pref", r.choice([f"I would like {c} as late as possible.", f"If you can, put {c} as late as possible."])))
    return facts


CLOSINGS = ["Please plan my remaining semesters.", "Can you plan the rest of my degree?",
            "What should my plan look like?", "How should I arrange my remaining semesters?"]


def programme_sentence(r, spec, text=None):
    p = spec.get("programme")
    if not p:
        return None
    if text:
        return text
    return r.choice(["I am a Computer Science (BComp CS Hons) student.", "I'm a BComp Computer Science Honours student."])


def render(spec, wording, r, extra_course=None, programme_text=None, sem_text=None):
    head = [programme_sentence(r, spec, programme_text)]
    if "completed" in spec:
        head.append(done_sentence(r, spec["completed"]))
    if sem_text:
        head.append(sem_text)
    elif "current_sem" in spec:
        head.append(sem_sentence(r, spec["current_sem"]))
    head = [x for x in head if x]
    facts = fact_sentences(r, spec)
    must = spec.get("must_take")
    correction = ""
    if wording != "scattered":
        parts = head + ([must_sentence(r, must)] if must else []) + [t for _, t in facts]
        if wording == "unsupported":
            for u in spec.get("unsupported", []):
                parts.insert(r.randint(min(len(head) + 1, len(parts)), len(parts)), r.choice(UNSUPPORTED[u]))
        return " ".join(parts + [r.choice(CLOSINGS)]), correction
    pieces = []
    body = []
    follow = []
    done = list(spec.get("completed", []))
    r.shuffle(done)
    if "completed" in spec and len(done) >= 3:
        cut = r.randint(1, len(done) - 1)
        first = f"I've done {listing(done[:cut])}."
        pieces.append(first)
        body.append(r.choice([f"Oh, I forgot to say I also completed {listing(done[cut:])}.",
                              f"Also already done: {listing(done[cut:])}."]))
    elif "completed" in spec:
        pieces.append(done_sentence(r, done))
    if spec.get("programme"):
        body.append(programme_sentence(r, spec, programme_text))
    options = []
    if "current_sem" in spec and 1 <= spec["current_sem"] <= 8:
        options.append("semester")
    if "mc_max" in spec and spec["mc_max"] <= 16:
        options.append("mc_max")
    if must and extra_course:
        options.append("drop_course")
    if any(x["type"] == "before" for x in rules_of(spec, "must")):
        options.append("rule_flip")
    correction = r.choice(options) if options else ""
    if sem_text:
        body.append(sem_text)
    elif "current_sem" in spec:
        k = spec["current_sem"]
        if correction == "semester":
            wrong = k + 1 if k < 8 and (k == 1 or r.random() < 0.5) else k - 1
            body.append(f"I'm in {sem_words(r, wrong)} now. Wait, sorry, I'm actually in {sem_words(r, k)}.")
        else:
            body.append(sem_sentence(r, k))
    if must:
        ms = list(must)
        r.shuffle(ms)
        cut = r.randint(1, len(ms) - 1) if len(ms) >= 2 else len(ms)
        first, second = ms[:cut], ms[cut:]
        if correction == "drop_course":
            first = first + [extra_course]
        anchor = r.choice(["Modules I still need: ", "I need to take "]) + listing(first) + "."
        body.append(anchor)
        if second:
            follow.append((anchor, r.choice([f"Oh, and {listing(second)} too.",
                                             f"I almost forgot {listing(second)}, I need {'that' if len(second) == 1 else 'those'} as well."])))
        if correction == "drop_course":
            follow.append((anchor, f"Actually, scratch {extra_course}, I've decided not to take it."))
    flip = next((i for i, x in enumerate(rules_of(spec, "must")) if x["type"] == "before"), None)
    j = 0
    for kind, text in facts:
        if kind == "mc_max" and correction == "mc_max":
            m = spec["mc_max"]
            text = f"I can take at most {m + 4} MC per semester. No wait, make that {m} MC."
        if kind == "must_rule":
            if correction == "rule_flip" and j == flip:
                x = rules_of(spec, "must")[j]
                text = f"{x['b']} must come before {x['a']}. Sorry, other way round: {x['a']} must come before {x['b']}."
            j += 1
        body.append(text)
    r.shuffle(body)
    for anchor, text in follow:
        body.insert(r.randint(body.index(anchor) + 1, len(body)), text)
    return " ".join(pieces + body + [r.choice(CLOSINGS)]), correction


# ---------- derived sets ----------
def with_caps(spec, mc_max, caps):
    s = copy.deepcopy(spec)
    s.pop("sem_caps", None)
    s.pop("mc_max", None)
    if mc_max != 20:
        s["mc_max"] = mc_max
    if caps:
        s["sem_caps"] = {str(k): v for k, v in sorted(caps.items())}
    return s


def fixed_sems(spec):
    return {x["sem"] for x in rules_of(spec, "must") if x["type"] == "in_sem"} | set(spec.get("atap_sems", []))


def tighten(g, spec, lo, hi):
    r = g.r
    k = spec["current_sem"]
    need, _ = g.needed_room(spec)
    sems = list(range(k, 9))
    free = [s for s in sems if s not in fixed_sems(spec)]
    seen, options = set(), []
    for _ in range(600):
        m = r.choice([4, 8, 12, 16, 20])
        blocked = set(r.sample(free, r.randint(0, max(0, len(free) - 1))))
        caps = {s: 0 for s in blocked}
        rest = [s for s in sems if s not in blocked]
        if rest and r.random() < 0.4:
            caps[r.choice(rest)] = r.choice([4, 8, 12])
        room = sum(caps.get(s, m) for s in sems)
        if not room:
            continue
        rho = need / room
        key = (m, tuple(sorted(caps.items())))
        if lo <= rho < hi or (hi == 1.0 and rho == 1.0):
            if key not in seen:
                seen.add(key)
                options.append((len(blocked), r.random(), m, caps))
    options.sort(key=lambda x: (x[0], x[1]))
    for _, _, m, caps in options[:25]:
        s = with_caps(spec, m, caps)
        ans = g.plan_ok(s)
        if ans:
            return s, ans
    raise GenError("tighten")


def atap_option(g, spec):
    r = g.r
    k = spec["current_sem"]
    singles = [s for s in range(k, 8) if cap_of(spec, s) > 0]
    opts = []
    for s in r.sample(singles, len(singles)):
        opts.append({"atap_sems": [s]})
        opts.append({"atap_sems": [s], "cap1": s})
    if k <= 7:
        opts.insert(r.randint(0, len(opts)), {"atap_sems": list(range(k, 9))})
    return opts


def add_atap(spec, opt):
    s = copy.deepcopy(spec)
    s["atap_sems"] = list(opt["atap_sems"])
    if "cap1" in opt:
        s.setdefault("sem_caps", {})[str(opt["cap1"])] = 1
        s["sem_caps"] = dict(sorted(s["sem_caps"].items(), key=lambda x: int(x[0])))
    return s


def add_mcmin(spec, v):
    s = copy.deepcopy(spec)
    s["mc_min"] = v
    return s


def mcmin_values(spec):
    return [v for v in (12, 8) if v <= spec.get("mc_max", 20)]


def derive(g, rec, group):
    out = []
    spec, core, rules, prefs, obj = rec["spec"], rec["core"], rec["rules"], rec["prefs"], rec["objective"]
    for lo, hi in RHO_BINS:
        s, a = tighten(g, spec, lo, hi)
        out.append(("S2", f"rho {lo}-{hi}", "", "", s, a))
    a0 = g.plan_ok(g.with_prefs(g.set_objective(core, obj), prefs))
    if not a0:
        raise GenError("ladder base")
    where = g.placed(a0)
    pref_spec = g.with_prefs(g.set_objective(core, obj), prefs)
    rules3 = g.make_rules(pref_spec, where, 3, "must", extra_p=0.15)
    prefs3 = g.make_prefs(g.with_rules(g.set_objective(core, obj), rules), g.placed(rec["answer"]), 3)
    group_opts = [None]
    if group == "atap":
        group_opts = atap_option(g, spec)
    elif group == "mcmin":
        group_opts = mcmin_values(spec)
    for opt in group_opts:
        def extra(s):
            if group == "atap":
                return add_atap(s, opt)
            if group == "mcmin":
                return add_mcmin(s, opt)
            return s
        lad = []
        ok = True
        for j in range(4):
            s = extra(g.with_rules(pref_spec, rules3[:j]))
            a = g.plan_ok(s)
            if not a:
                ok = False
                break
            lad.append(("S3", "rule ladder", "rule", j, s, a))
        if not ok:
            continue
        for j in range(4):
            s = extra(g.with_prefs(g.with_rules(g.set_objective(core, obj), rules), prefs3[:j]))
            a = g.plan_ok(s)
            if not a:
                ok = False
                break
            lad.append(("S3", "preference ladder", "preference", j, s, a))
        if ok:
            out += lad
            break
    else:
        raise GenError("ladders")
    for o in OBJECTIVES:
        s = g.set_objective(spec, o)
        a = g.plan_ok(s)
        if not a:
            raise GenError("objective ladder")
        out.append(("S3", "objective ladder", "objective", o, s, a))
    for opt in atap_option(g, spec):
        s = add_atap(spec, opt)
        a = g.plan_ok(s)
        if a:
            out.append(("S3", "atap twin", "", "", s, a))
            break
    else:
        raise GenError("atap twin")
    best = None
    for v in mcmin_values(spec):
        s = add_mcmin(spec, v)
        a = g.plan_ok(s)
        if a and (best is None or a["plan"] != rec["answer"]["plan"]):
            best = (s, a)
            if a["plan"] != rec["answer"]["plan"]:
                break
    if not best:
        raise GenError("mcmin twin")
    out.append(("S3", "min-MC twin", "", "", best[0], best[1]))
    return out


# ---------- impossible requests ----------
def required_courses(spec):
    req = [c for c in spec.get("must_take", []) if c not in spec.get("completed", [])]
    for x in rules_of(spec, "must"):
        for c in ([x["course"]] if x["type"] == "in_sem" else [x["a"], x["b"]]):
            if c not in req and c not in spec.get("completed", []):
                req.append(c)
    return req


def no_parity(spec):
    use = [s for s in range(spec["current_sem"], 9) if cap_of(spec, s) > 0]
    return all(c in C and any(term_of(s) in C[c]["offered"] for s in use) for c in required_courses(spec))


def under_capacity(g, spec):
    need, room = g.needed_room(spec)
    return room > 0 and need <= room


def build_noplan(g, kind, k, n_rules, n_p, objective, need_twin):
    r = g.r
    for _ in range(40):
        try:
            if kind == "capacity":
                left = 9 - k
                rec = g.build_plan(k, max(2, min(12, left + r.randint(1, 3))), n_rules, n_p, objective, tries=8)
                f = rec["spec"]
                need, _ = g.needed_room(f)
                bad = None
                for m in (16, 12, 8, 4):
                    if m >= f.get("mc_max", 20):
                        continue
                    s = with_caps(f, m, {int(a): b for a, b in f.get("sem_caps", {}).items()})
                    n2, room = g.needed_room(s)
                    if room and n2 > room:
                        bad = (m, s)
                        break
                if not bad:
                    continue
                m, s = bad
                if not g.no_plan_ok(s):
                    continue
                twin = None
                for m2 in range(m + 4, 24, 4):
                    t = with_caps(f, m2, {int(a): b for a, b in f.get("sem_caps", {}).items()})
                    if g.plan_ok(t):
                        twin = t
                        break
                if not twin:
                    continue
                return s, twin
            rec = g.build_plan(k, r.randint(3, 7) if k <= 6 else r.randint(2, 4), n_rules, n_p, objective, tries=8)
            f, fa = rec["spec"], rec["answer"]
            done = set(f["completed"])
            if kind == "exclusion":
                plaus = set(g.pool) | set(CORE)
                pairs = [(t, b) for t in g.pool + CORE if t not in done and t not in f["must_take"]
                         and g.reachable(t, done)
                         for b in (C[t]["preclusion"].get("courses") or [])
                         if b in plaus and b not in done and b not in f["must_take"] and b in C
                         and C[b]["exists_in_ay"] and C[b]["available"]]
                if not pairs:
                    continue
                t, b = r.choice(pairs)
                if k >= 2 and r.random() < 0.5 and g.cat.can_take(b, done)[0]:
                    twin = copy.deepcopy(f)
                    twin["completed"] = f["completed"] + [b]
                    s = copy.deepcopy(twin)
                    s["must_take"] = f["must_take"] + [t]
                else:
                    twin = copy.deepcopy(f)
                    twin["must_take"] = f["must_take"] + [t]
                    s = copy.deepcopy(twin)
                    s["must_take"] = twin["must_take"] + [b]
            elif kind == "parity":
                cands = [c for c in g.one_term if g.reachable(c, done) and c not in f["must_take"]
                         and g.cat.can_take(c, done)[0]]
                if not cands:
                    continue
                x = r.choice(cands)
                tt = [t for t in C[x]["offered"] if t in (1, 2)][0]
                tsems = [s_ for s_ in range(k, 9) if term_of(s_) == tt]
                if any(s_ in fixed_sems(f) for s_ in tsems):
                    continue
                if len(tsems) > 2:
                    continue
                twin = copy.deepcopy(f)
                twin["must_take"] = f["must_take"] + [x]
                caps = {int(a): b for a, b in f.get("sem_caps", {}).items()}
                if tsems:
                    keep = tsems[-1]
                    for s_ in tsems:
                        if s_ != keep:
                            caps[s_] = 0
                    twin = with_caps(twin, twin.get("mc_max", 20), caps)
                    caps[keep] = 0
                s = with_caps(twin, twin.get("mc_max", 20), caps)
                if not tsems:
                    twin = None
            elif kind == "chain":
                deep = [c for c in g.deep_pool if g.reachable(c, done) and not g.cat.can_take(c, done)[0]
                        and c not in f["must_take"]]
                if not deep:
                    continue
                d = r.choice(deep)
                cur = copy.deepcopy(f)
                cur["must_take"] = f["must_take"] + [d]
                if not g.plan_ok(cur):
                    if k < 7:
                        continue
                    s, twin = cur, None
                else:
                    s = twin = None
                    caps = {int(a): b for a, b in cur.get("sem_caps", {}).items()}
                    free = [s_ for s_ in range(k, 9) if s_ not in fixed_sems(cur) and caps.get(s_) != 0]
                    r.shuffle(free)
                    prev = cur
                    for s_ in free[:-1]:
                        caps[s_] = 0
                        nxt = with_caps(cur, cur.get("mc_max", 20), caps)
                        if not g.plan_ok(nxt):
                            s, twin = nxt, prev
                            break
                        prev = nxt
                    if s is None:
                        continue
                if not no_parity(s) or not under_capacity(g, s):
                    continue
                without = copy.deepcopy(s)
                without["must_take"] = [c for c in s["must_take"] if c != d]
                if not g.plan_ok(without):
                    continue
            elif kind == "rule_conflict":
                s, twin = conflict(g, f, fa, n_rules)
                if s is None:
                    continue
            elif kind == "hidden":
                s, twin = hidden(g, f, fa, n_rules)
                if s is None:
                    continue
            if kind != "capacity" and not under_capacity(g, s):
                continue
            if kind not in ("parity",) and not no_parity(s):
                continue
            if not g.no_plan_ok(s):
                continue
            if need_twin and twin is None:
                continue
            if twin is not None and not g.plan_ok(twin):
                continue
            return s, twin
        except GenError:
            continue
    raise GenError(f"no plan {kind} k={k}")


def conflict(g, f, fa, n_total):
    r = g.r
    where = g.placed(fa)
    must = [c for c in f["must_take"] if c in where]
    pats = ["cycle", "pair", "same_apart", "insem_same", "before_insem"]
    r.shuffle(pats)
    use = g.usable(f)
    for p in pats:
        size = {"cycle": 3, "pair": 2, "same_apart": 2, "insem_same": 3, "before_insem": 3}[p]
        n_normal = n_total - size
        if n_normal < 0 or len(must) < 3:
            continue
        a, b, c = r.sample(must, 3)
        if p == "cycle":
            cr = [{"type": "before", "a": a, "b": b}, {"type": "before", "a": b, "b": c}, {"type": "before", "a": c, "b": a}]
        elif p == "pair":
            cr = [{"type": "before", "a": a, "b": b}, {"type": "before", "a": b, "b": a}]
        elif p == "same_apart":
            cr = [{"type": "same_sem", "a": a, "b": b}, {"type": "apart", "a": a, "b": b}]
        else:
            sa = [s for s in use if g.offered(a, s)]
            sb = [s for s in use if g.offered(b, s)]
            if p == "insem_same":
                combos = [(x, y) for x in sa for y in sb if x != y]
                if not combos:
                    continue
                x, y = r.choice(combos)
                cr = [{"type": "in_sem", "course": a, "sem": x}, {"type": "in_sem", "course": b, "sem": y},
                      {"type": "same_sem", "a": a, "b": b}]
            else:
                combos = [(x, y) for x in sa for y in sb if y <= x]
                if not combos:
                    continue
                x, y = r.choice(combos)
                cr = [{"type": "before", "a": a, "b": b}, {"type": "in_sem", "course": a, "sem": x},
                      {"type": "in_sem", "course": b, "sem": y}]
        for x in cr:
            x["strength"] = "must"
        involved = {a, b, c}
        old = [x for x in rules_of(f, "must")
               if not involved & ({x["course"]} if x["type"] == "in_sem" else {x["a"], x["b"]})][:n_normal]
        if len(old) < n_normal:
            try:
                extra = g.make_rules({**f, "rules": old + cr}, where, n_normal - len(old), "must")
            except GenError:
                continue
            old = old + extra
        base_rules = old + rules_of(f, "prefer")
        s = copy.deepcopy(f)
        s["rules"] = old + cr + rules_of(f, "prefer")
        twin = copy.deepcopy(f)
        twin["rules"] = old + cr[:-1] + rules_of(f, "prefer")
        relaxed = copy.deepcopy(f)
        relaxed["rules"] = base_rules
        if g.plan_ok(relaxed):
            return s, twin
    return None, None


def hidden(g, f, fa, n_total):
    r = g.r
    done = set(f["completed"])
    where = g.placed(fa)
    n_normal = n_total - 1
    normal = rules_of(f, "must")[:n_normal]
    if len(normal) < n_normal:
        return None, None
    used = {c for x in normal for c in ([x["course"]] if x["type"] == "in_sem" else [x["a"], x["b"]])}
    pats = ["insem", "before", "same"]
    r.shuffle(pats)
    for p in pats:
        if p == "insem":
            cands = [c for c in f["must_take"] if c in where and c not in used and not g.cat.can_take(c, done)[0]]
            r.shuffle(cands)
            for c in cands[:3]:
                sems = [s for s in g.usable(f) if g.offered(c, s) and s < where[c]]
                for s_ in sems:
                    rule = {"type": "in_sem", "course": c, "sem": s_, "strength": "must"}
                    s = copy.deepcopy(f)
                    s["rules"] = normal + [rule] + rules_of(f, "prefer")
                    if not g.no_plan_ok(s):
                        continue
                    later = [t for t in g.usable(f) if g.offered(c, t) and t > s_]
                    for t in later:
                        twin = copy.deepcopy(s)
                        twin["rules"] = normal + [{**rule, "sem": t}] + rules_of(f, "prefer")
                        if g.plan_ok(twin):
                            return s, twin
            continue
        pairs = [(a, b) for a in f["must_take"] for b in f["must_take"] if a != b and a in where and b in where
                 and b in (C[a]["prereq"].get("courses") or []) and not ({a, b} & used)]
        if not pairs:
            continue
        a, b = r.choice(pairs)
        t = "before" if p == "before" else "same_sem"
        s = copy.deepcopy(f)
        s["rules"] = normal + [{"type": t, "a": a, "b": b, "strength": "must"}] + rules_of(f, "prefer")
        twin = copy.deepcopy(f)
        twin["rules"] = normal + [{"type": "before", "a": b, "b": a, "strength": "must"}] + rules_of(f, "prefer")
        if g.no_plan_ok(s) and g.plan_ok(twin):
            return s, twin
    return None, None


# ---------- missing information and out of scope ----------
def build_missing(g, field, cell, i):
    band, m = cell
    k = BANDS[band][i % 2] if band != "7-8" else 7
    rec = g.build_plan(k, m, 2 + i % 3, 2 + (i + 1) % 3, OBJECTIVES[i % 3])
    s = copy.deepcopy(rec["spec"])
    s.pop(field)
    if field == "must_take":
        s["rules"] = rules_of(s, "prefer")
        s = {k_: v for k_, v in s.items() if k_ not in ("early", "late", "rules")}
    ans, ok = g.gold(s)
    if ans["status"] != "MISSING_INFO":
        raise GenError("missing")
    return s, ans, None, None


def build_oos(g, sub, cell, i):
    r = g.r
    band, m = cell
    k = 8 if sub == "semester above 8" else (BANDS[band][i % 2] if band != "7-8" else 7)
    if sub == "semester 0":
        k = 1
    rec = g.build_plan(k, min(m, 4) if k == 8 else m, 2 + i % 3, 2 + (i + 1) % 3, OBJECTIVES[i % 3])
    s = copy.deepcopy(rec["spec"])
    text, sem_text = None, None
    if sub == "other programme":
        name, text = OTHER_PROGRAMMES[i % len(OTHER_PROGRAMMES)]
        s["programme"] = name
    elif sub == "second major":
        x = SECOND_MAJORS[i % len(SECOND_MAJORS)]
        s["programme"] = f"BComp CS Hons with a second major in {x}"
        text = r.choice([f"I'm a Computer Science student doing a second major in {x}.",
                         f"I study CS and I also have a second major in {x}."])
    elif sub == "minor":
        x = MINORS[i % len(MINORS)]
        s["programme"] = f"BComp CS Hons with a minor in {x}"
        text = r.choice([f"I'm in Computer Science with a minor in {x}.", f"I'm a CS student taking a minor in {x}."])
    elif sub == "course not in catalogue":
        s["must_take"] = s["must_take"] + [NOT_IN_CATALOGUE[i % len(NOT_IN_CATALOGUE)]]
    elif sub == "semester above 8":
        k2 = 9 + i % 2
        s["current_sem"] = k2
        s = {k_: v for k_, v in s.items() if k_ not in ("rules", "sem_caps", "atap_sems", "early", "late")}
        y, t = (k2 + 1) // 2, 2 - k2 % 2
        sem_text = r.choice([f"I am in Y{y}S{t} now, my fifth year.", f"I'm currently in semester {k2}."])
    elif sub == "semester 0":
        s["current_sem"] = 0
        s["completed"] = []
        s = {k_: v for k_, v in s.items() if k_ not in ("rules", "sem_caps", "atap_sems", "early", "late")}
        sem_text = r.choice(["I haven't started university yet, so I'm in semester 0.",
                             "I am in semester 0 right now, before my first semester."])
    ans, ok = g.gold(s)
    if ans["status"] != "OUT_OF_SCOPE":
        raise GenError("oos")
    return s, ans, text, sem_text


# ---------- assembly ----------
def log(msg, t0):
    print(f"[{time.time() - t0:7.0f}s] {msg}", flush=True)


def attempt(fn, n=6):
    for _ in range(n):
        try:
            return fn()
        except GenError:
            continue
    raise GenError("gave up")


def meta_of(g, spec, ans):
    m = g.measure(spec) if spec.get("query") == "plan" and 1 <= spec.get("current_sem", 0) <= 8 and "must_take" in spec \
        and "completed" in spec else {}
    return {
        "log10_omega": m.get("log10_omega", ""), "rho": m.get("rho", ""), "n_cand": m.get("n_cand", ""),
        "n_sems": m.get("n_sems", ""), "needed_mc": m.get("needed_mc", ""), "room_mc": m.get("room_mc", ""),
        "added": len(ans.get("added_prerequisites", [])) if ans["status"] == "PLAN" else "",
        "n_prefs": n_prefs(spec), "n_must_rules": len(rules_of(spec, "must")),
        "objective": spec.get("objective", "none"), "atap": "atap_sems" in spec, "mc_min": "mc_min" in spec,
        "M": len(spec.get("must_take", [])) if "must_take" in spec else "",
        "cur_sem": spec.get("current_sem", ""),
    }


def band_of(k):
    if k == "" or k is None:
        return "not given"
    if not 1 <= k <= 8:
        return "outside 1-8"
    return next(b for b, (lo, hi) in BANDS.items() if lo <= k <= hi)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=3263)
    ap.add_argument("--out", default=str(HERE / "q2_900.json"))
    a = ap.parse_args()
    t0 = time.time()
    g = Q2Gen(a.seed)
    items = []

    def add(set_, kind, spec, ans, **meta):
        items.append({"set": set_, "kind": kind, "spec": spec, "answer": ans, "meta": meta})
        return len(items) - 1

    s1 = []
    cache_file = Path(a.out).with_suffix(".s1.pkl")
    if cache_file.exists():
        items, s1 = pickle.load(open(cache_file, "rb"))
        log(f"S1 loaded from {cache_file.name} ({len(items)} items)", t0)
    for band, m in ([] if s1 else CELLS):
        lo, hi = BANDS[band]
        for i in range(9):
            obj, nr, npf = OBJECTIVES[i % 3], 2 + i // 3, 2 + (i + i // 3) % 3
            ks = [7] if band == "7-8" else ([lo, hi] if i % 2 == 0 else [hi, lo])
            rec = None
            for k in ks:
                try:
                    rec = g.build_plan(k, m, nr, npf, obj)
                    break
                except GenError:
                    continue
            if rec is None:
                rec = attempt(lambda: g.build_plan(ks[0], m, nr, npf, obj, tries=200), 3)
            idx = add("S1", "q2/S1", rec["spec"], rec["answer"], cell=f"{band}/M{m}", twin="")
            s1.append((idx, rec, band))
        log(f"S1 cell {band}/M{m} done ({len(items)} items, {g.solves} solves)", t0)

    if not cache_file.exists():
        pickle.dump((items, s1), open(cache_file, "wb"))
    quota_band = {"1-2": 6, "3-4": 7, "5-6": 6, "7-8": 2}
    quota_rules = {2: 7, 3: 7, 4: 7}
    bases = []
    order = list(s1)
    g.r.shuffle(order)
    order.sort(key=lambda x: (4 * len(x[1]["answer"].get("added_prerequisites", [])) / max(1, g.needed_room(x[1]["spec"])[0]) > 0.25,
                              x[2] == "1-2" and int(items[x[0]]["meta"]["cell"].split("M")[1]) > 8))
    for strict in (True, False):
        for idx, rec, band in order:
            if len(bases) == 21:
                break
            if any(b[0] == idx for b in bases):
                continue
            nr = len(rules_of(rec["spec"], "must"))
            need0 = g.needed_room(rec["spec"])[0]
            if strict and 4 * len(rec["answer"].get("added_prerequisites", [])) > 0.3 * need0:
                continue
            if quota_rules.get(nr, 0) == 0 or (strict and quota_band[band] == 0):
                continue
            group = "atap" if len(bases) < 7 else "mcmin" if len(bases) < 14 else "none"
            g.budget_end = time.time() + 60
            try:
                derived = derive(g, rec, group)
            except GenError:
                continue
            finally:
                g.budget_end = None
            quota_rules[nr] -= 1
            quota_band[band] -= 1
            bases.append((idx, rec, derived, group))
            log(f"base {len(bases)}/21 from {items[idx]['meta']['cell']} ({g.solves} solves)", t0)
    if len(bases) != 21:
        raise SystemExit("could not find 21 bases")
    for bi, (idx, rec, derived, group) in enumerate(bases):
        items[idx]["meta"].update(base_id=f"B{bi:02d}", twin="base", base_group=group)
        for set_, label, ladder, level, spec, ans in derived:
            twin = {"S2": label, "atap twin": "atap", "min-MC twin": "mc_min"}.get(set_ if set_ == "S2" else label, "")
            add(set_, f"q2/{set_}", spec, ans, base_id=f"B{bi:02d}", twin=twin, ladder=ladder, level=level,
                base_group=group, derived_from=idx)

    s4 = []
    k_lists = {"capacity": [3, 4, 5, 6, 7, 8], "exclusion": list(range(1, 9)), "parity": [5, 6, 7, 8],
               "chain": [4, 5, 6, 7, 8], "rule_conflict": list(range(1, 8)), "hidden": list(range(1, 8))}
    pair_n = 0
    for kind in NO_PLAN_KINDS:
        for i in range(40):
            nr = {"rule_conflict": 3 + i % 2, "hidden": 2 + i % 2}.get(kind, 1 + i % 4)
            npf, obj = 2 + (i // 4) % 3, OBJECTIVES[(i + i // 3) % 3]
            want = i % 10 in (0, 3, 6)
            ks = k_lists[kind]
            k = ks[i % len(ks)]
            res = None
            for kk in [k] + [x for x in ks if x != k]:
                try:
                    res = build_noplan(g, kind, kk, nr, npf, obj, want)
                    break
                except GenError:
                    continue
            if res is None:
                raise SystemExit(f"S4 {kind} {i} failed")
            s, twin = res
            ans = g.no_plan_ok(s)
            pid = ""
            if want:
                pair_n += 1
                pid = f"P{pair_n:02d}"
            idx = add("S4", f"q2_infeasible/{kind}", s, ans, nokind=kind, visible=VISIBLE[kind], pair_id=pid,
                      twin="impossible" if want else "")
            s4.append(idx)
            if want:
                add("S4", f"q2/near_miss_{kind}", twin, g.plan_ok(twin), nokind=kind, visible=VISIBLE[kind],
                    pair_id=pid, twin="near_miss", partner=idx)
        log(f"S4 {kind} done ({len(items)} items, {g.solves} solves)", t0)

    s5_cells = CELLS[::3]
    for bi, cell in enumerate(s5_cells):
        band, m = cell
        k = BANDS[band][bi % 2] if band != "7-8" else 7
        rec = attempt(lambda: g.build_plan(k, m, 2 + bi % 3, 2 + (bi + 1) % 3, OBJECTIVES[bi % 3]))
        for w in ("plain", "scattered", "unsupported"):
            add("S5", "q2/S5", copy.deepcopy(rec["spec"]), copy.deepcopy(rec["answer"]), base_id=f"W{bi}",
                twin="base" if w == "plain" else w, wording_fixed=w, cell=f"{band}/M{m}")
    log(f"S5 done ({len(items)} items)", t0)

    small = [c for c in CELLS if c[1] <= 8]
    for fi, field in enumerate(["current_sem", "must_take", "completed"]):
        for i in range(10):
            cell = small[(fi * 10 + i) % len(small)]
            s, ans, _, _ = attempt(lambda: build_missing(g, field, cell, i))
            add("S6", f"missing_info/{field}", s, ans, missing=field)
    for si, sub in enumerate(["other programme", "second major", "minor", "course not in catalogue",
                              "semester above 8", "semester 0"]):
        for i in range(5):
            cell = small[(si * 5 + i) % len(small)]
            s, ans, text, sem_text = attempt(lambda: build_oos(g, sub, cell, i))
            add("S6", f"out_of_scope/{sub}", s, ans, oos=sub, programme_text=text, sem_text=sem_text)
    log(f"S6 done ({len(items)} items)", t0)

    assign_wording(g, items, bases, s1, s4)
    rows = finish(g, items)
    Path(a.out).write_text(json.dumps(rows, indent=1))
    (Path(a.out).parent / "Q2_SUMMARY.md").write_text(summary(rows, a.seed, Path(a.out).name))
    log(f"wrote {len(rows)} instances to {a.out} ({g.solves} solves)", t0)


def assign_wording(g, items, bases, s1, s4):
    r = g.r
    for it in items:
        it["meta"]["wording"] = it["meta"].get("wording_fixed", "plain")
    base_w = {0: "scattered", 10: "scattered", 5: "unsupported", 15: "unsupported"}
    base_idx = {b[0]: bi for bi, b in enumerate(bases)}
    for bi, w in base_w.items():
        items[bases[bi][0]]["meta"]["wording"] = w
    for it in items:
        d = it["meta"].get("derived_from")
        if d is not None and d in base_idx:
            it["meta"]["wording"] = items[d]["meta"]["wording"]
    by_cell = {}
    for idx, _, _ in s1:
        if idx not in base_idx:
            by_cell.setdefault(items[idx]["meta"]["cell"], []).append(idx)
    cells = list(by_cell)
    for w, offset in (("scattered", 0), ("unsupported", 3)):
        n = 0
        j = offset
        while n < 16:
            cell = cells[j % len(cells)]
            free = [x for x in by_cell[cell] if items[x]["meta"]["wording"] == "plain"]
            if free:
                items[r.choice(free)]["meta"]["wording"] = w
                n += 1
            j += 1
    twinned = [i for i in s4 if items[i]["meta"]["pair_id"]]
    single = [i for i in s4 if not items[i]["meta"]["pair_id"]]

    def spread(pool, w, n):
        by_kind = {}
        for i in pool:
            if items[i]["meta"]["wording"] == "plain":
                by_kind.setdefault(items[i]["meta"]["nokind"], []).append(i)
        kinds = sorted(by_kind)
        r.shuffle(kinds)
        j = 0
        while n:
            lst = by_kind[kinds[j % len(kinds)]]
            if lst:
                items[lst.pop(r.randrange(len(lst)))]["meta"]["wording"] = w
                n -= 1
            j += 1

    spread(twinned, "scattered", 8)
    spread(twinned, "unsupported", 8)
    spread(single, "scattered", 20)
    spread(single, "unsupported", 20)
    for it in items:
        p = it["meta"].get("partner")
        if p is not None:
            it["meta"]["wording"] = items[p]["meta"]["wording"]
    miss = [i for i, it in enumerate(items) if it["set"] == "S6" and it["kind"].startswith("missing")]
    oos = [i for i, it in enumerate(items) if it["set"] == "S6" and it["kind"].startswith("out_of_scope")]
    for pool, ns, nu in ((miss, 4, 3), (oos, 3, 4)):
        pick = r.sample(pool, ns + nu)
        for i in pick[:ns]:
            items[i]["meta"]["wording"] = "scattered"
        for i in pick[ns:]:
            items[i]["meta"]["wording"] = "unsupported"
    wishes = {}
    for idx, it in enumerate(items):
        if it["meta"]["wording"] != "unsupported":
            continue
        src = it["meta"].get("derived_from", it["meta"].get("partner"))
        if it["set"] == "S5":
            src = ("S5", it["meta"]["base_id"])
        if src is not None and src in wishes:
            keys = wishes[src]
        else:
            keys = r.sample(sorted(UNSUPPORTED), r.choice([1, 1, 2]))
            wishes[src if src is not None else idx] = keys
        wishes[idx] = keys
        it["spec"]["unsupported"] = list(keys)
        if it["answer"]["status"] in ("PLAN", "NO_PLAN"):
            it["answer"]["not_applied"] = list(keys)
        else:
            ans, _ = g.gold(it["spec"])
            it["answer"] = ans


def extra_course(g, spec):
    used = set(spec.get("completed", [])) | set(spec.get("must_take", [])) | set(required_courses(spec))
    opts = [c for c in g.pool if c not in used]
    return g.r.choice(opts)


def finish(g, items):
    rows = []
    count = Counter()
    for it in items:
        spec, ans, meta = it["spec"], it["answer"], it["meta"]
        set_ = it["set"]
        count[set_] += 1
        iid = f"q2-{set_}-{count[set_]:03d}"
        meta["id_index"] = iid
    for it in items:
        spec, ans, meta = it["spec"], it["answer"], it["meta"]
        text, corr = render(spec, meta["wording"], g.r, extra_course(g, spec),
                            meta.get("programme_text"), meta.get("sem_text"))
        m = meta_of(g, spec, ans)
        out_meta = {"set": it["set"], "answer_type": ans["status"], "wording": meta["wording"],
                    "correction_kind": corr, "twin": meta.get("twin", ""), "ladder": meta.get("ladder", ""),
                    "level": meta.get("level", ""), "base_id": meta.get("base_id", ""),
                    "pair_id": meta.get("pair_id", ""), "nokind": meta.get("nokind", ""),
                    "visible": meta.get("visible", ""), "cell": meta.get("cell", ""),
                    "base_group": meta.get("base_group", ""), "band": band_of(spec.get("current_sem", "")),
                    "missing": meta.get("missing", ""), "oos": meta.get("oos", "")}
        if "derived_from" in meta:
            out_meta["base_instance"] = items[meta["derived_from"]]["meta"]["id_index"]
        if "partner" in meta:
            out_meta["partner"] = items[meta["partner"]]["meta"]["id_index"]
        out_meta.update(m)
        rows.append({"id": meta["id_index"], "kind": it["kind"], "request": text,
                     "gold_spec": spec, "gold_answer": ans, "meta": out_meta})
    return rows


def summary(rows, seed, name):
    def table(title, key, order=None):
        c = Counter(key(r) for r in rows)
        keys = order or sorted(c, key=str)
        out = [f"### {title}", "", "| Value | Count |", "|---|---|"]
        out += [f"| {k} | {c.get(k, 0)} |" for k in keys] + [f"| total | {sum(c.values())} |", ""]
        return out

    L = [f"# Q2 instance set (seed {seed})", "", f"{len(rows)} instances in `{name}`. "
         f"Regenerate with `python -m instances.generate_q2 --seed {seed}`.", ""]
    L += table("Set", lambda r: r["meta"]["set"])
    L += table("Kind", lambda r: r["kind"])
    L += table("Answer type", lambda r: r["meta"]["answer_type"])
    L += table("Current semester band", lambda r: r["meta"]["band"],
               ["1-2", "3-4", "5-6", "7-8", "not given", "outside 1-8"])
    L += table("Must-take count M", lambda r: "not given" if r["meta"]["M"] == "" else
               "2-4" if r["meta"]["M"] <= 4 else "6-8" if r["meta"]["M"] <= 8 else "10-12" if r["meta"]["M"] <= 12 else "13+")
    L += table("Objective", lambda r: r["meta"]["objective"] if r["gold_spec"].get("query") else "")
    L += table("Number of preferences", lambda r: r["meta"]["n_prefs"])
    L += table("Number of must rules", lambda r: r["meta"]["n_must_rules"])
    L += table("ATAP", lambda r: r["meta"]["atap"])
    L += table("Minimum MC", lambda r: r["meta"]["mc_min"])
    L += table("Wording", lambda r: r["meta"]["wording"], ["plain", "scattered", "unsupported"])
    L += table("NO_PLAN kind", lambda r: r["meta"]["nokind"] if r["meta"]["answer_type"] == "NO_PLAN" else "-")
    L += table("NO_PLAN found by", lambda r: r["meta"]["visible"] if r["meta"]["answer_type"] == "NO_PLAN" else "-")
    s1 = [r for r in rows if r["meta"]["set"] == "S1"]
    L += ["### log10 |Omega| on S1", "", "| Bin | Count |", "|---|---|"]
    edges = [(-1, 3, "below 3"), (3, 6, "3 to below 6"), (6, 10, "6 to below 10"), (10, 24, "10 to below 24"),
             (24, 1e9, "24 and above")]
    for lo, hi, lab in edges:
        L.append(f"| {lab} | {sum(lo <= r['meta']['log10_omega'] < hi for r in s1)} |")
    L += ["", "### Added courses in the gold plan on S1", "", "| Value | Count |", "|---|---|"]
    c = Counter(min(r["meta"]["added"], 3) for r in s1)
    L += [f"| {'3+' if k == 3 else k} | {c[k]} |" for k in sorted(c)] + [""]
    pop = [r for r in rows if r["meta"]["set"] in ("S1", "S2") or r["meta"]["nokind"] == "capacity"
           and r["meta"]["answer_type"] == "NO_PLAN"]
    L += ["### Capacity ratio rho (S1, S2, capacity impossible)", "", "| Bin | Count |", "|---|---|"]
    for lo, hi, lab in [(0, 0.4, "below 0.4"), (0.4, 0.6, "0.4 to below 0.6"), (0.6, 0.8, "0.6 to below 0.8"), (0.8, 1.0001, "0.8 to 1.0"),
                        (1.0001, 99, "above 1")]:
        L.append(f"| {lab} | {sum(lo <= r['meta']['rho'] < hi for r in pop)} |")
    L += ["", "## Examples", ""]
    seen = set()
    for r in rows:
        k = (r["kind"], r["meta"]["wording"])
        if k in seen:
            continue
        seen.add(k)
        L.append(f"- **{r['id']}** ({r['kind']}, {r['meta']['wording']}, gold `{r['gold_answer']['status']}`): {r['request']}")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()
