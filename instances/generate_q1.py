"""Q1-only instance generator: 400 "can I take X?" requests built to the agreed plan.

    python -m instances.generate_q1                 # writes q1_400.json, q1_gating.json, Q1_SUMMARY.md
    python -m instances.generate_q1 --seed 7 --outdir /tmp/q1

It does not touch instances.json or generate.py. Every instance is built from a gold spec first; the
request text is rendered from the spec, and the gold answer is the solver's answer to that spec. A case is
kept only if the solver answer matches the reason it was designed for (a "missing prerequisite" case must
fail on the prerequisite alone, an "exclusion" case on the exclusion alone, and so on).

The 400 (see Q1_SUMMARY.md for the checked counts):
  150 base cases x 2 renderings (plain, harder)          300
    reasons (base cases): ELIGIBLE 54, missing prerequisite 54 (each a near-miss of an ELIGIBLE base),
    exclusion 15, wrong offering term 12, closed 9, already completed 6.
    complexity: 50 base cases at each of levels 1, 2, 3 (level of the target's prerequisite formula).
  term twins   42  (30 ELIGIBLE one-term targets + the 12 wrong-term cases, term given as "next semester")
  exclusion twins 18 (an ELIGIBLE base plus one completed course that excludes the target)
  MISSING_INFO 20  (14 true, 6 decoys with the semester left out)
  OUT_OF_SCOPE 20  (programme, course not in catalogue, other-faculty course, semester outside 1-8)

Semester model: `current_sem` k is the semester in which the student wants to take the target, so the
student has finished f = k-1 semesters. A transcript must fit f (chain depth, course level, 2-4 modules per
finished semester), and a student is never "in Y1S1 now" with courses completed.
"""
from __future__ import annotations

import argparse
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

from instances.generate import CORE, ROADMAP, OTHER_PROGRAMMES
from m1_data.catalog import Catalog, satisfied
from solver.common import term_of
from solver.run import run

HERE = Path(__file__).resolve().parent
CODE_RE = re.compile(r"\b[A-Z]{2,4}\d{4}[A-Z]{0,2}\b")
ROAD_SEM = {c: s for s, cs in ROADMAP.items() for c in cs}

LEVELS = (1, 2, 3)
PER_LEVEL = {"eligible": 18, "missing_prereq": 18, "precluded": 5, "wrong_term": 4, "closed": 3, "already_done": 2}
ELIG_TYPES = {"term": 10, "excl": 6, "plain": 2}         # per level, of the 18 ELIGIBLE bases
OOS_PROGRAMMES = OTHER_PROGRAMMES[:5]
OOS_NOT_IN_CATALOGUE = ["CS5340", "CS5242", "CS6101", "CS4344", "CS5228"]
OOS_OTHER_FACULTY = ["LAJ1201", "GEC1015", "GEA1000", "ACC1701", "LAJ1202"]


# ---------------------------------------------------------------- wording helpers
def sem_abs(r, n):
    y, s = (n + 1) // 2, 2 - n % 2
    return r.choice([f"Y{y}S{s}", f"year {y} semester {s}", f"semester {n}", f"Year {y}, Semester {s}", f"Y{y} Sem {s}"])


ORD = {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth"}


def sem_indirect(r, n):
    y, s = (n + 1) // 2, 2 - n % 2
    return r.choice([f"my {ORD[n]} semester", f"the {ORD[s]} semester of my {ORD[y]} year"])


def listing(codes):
    codes = list(codes)
    if len(codes) == 1:
        return codes[0]
    return ", ".join(codes[:-1]) + " and " + codes[-1]


DONE = ["I have completed {L}.", "I've finished {L}.", "So far I have passed {L}.", "My completed modules are {L}.",
        "I already took {L}.", "I have cleared {L}.", "Modules I have done: {L}.", "Done so far: {L}.",
        "I have credit for {L}.", "My record shows {L} as completed.", "I've got {L} behind me.",
        "Completed so far: {L}.", "Here is what I have finished: {L}.", "Finished modules: {L}.",
        "Passed so far: {L}.", "On my transcript: {L}.", "Courses behind me: {L}.", "These are done: {L}.",
        "Modules cleared to date: {L}.", "Already completed: {L}.", "Out of the way: {L}."]
LEADS = ["Hi! ", "Hello! ", "Quick question: ", "Hey! ", "Question: ", "Hi there. ", "Excuse me. ", "Good day. ",
         "Thanks for helping. ", "Small query: "]


def lead(r, text):
    if r.random() >= 0.5:
        return text
    pre = r.choice(LEADS)
    if pre.endswith(": ") and (":" in text.split(" ")[0] or text.startswith("Planning ahead:")):
        return text
    return pre + text


QUESTION = ["Can I take {T}", "Am I eligible to take {T}", "Am I allowed to take {T}", "Is it possible for me to take {T}",
            "Would I be able to take {T}", "May I take {T}", "Do I qualify to take {T}", "Could I take {T}"]


def done_sentence(r, S):
    S = list(S)
    r.shuffle(S)
    return r.choice(DONE).format(L=listing(S))


def lower_first(s):
    return s[0].lower() + s[1:]


def render_plain(r, spec):
    S, T, k = spec["completed"], spec["target"], spec["current_sem"]
    sem, done, q = sem_abs(r, k), done_sentence(r, spec["completed"]), r.choice(QUESTION).format(T=spec["target"])
    forms = [f"{done} {q} in {sem}?", f"{q} in {sem}? {done}", f"I am planning my modules for {sem}. {done} {q}?",
             f"For {sem}, {lower_first(q)}? {done}", f"{done} I want to take {T} in {sem}. Am I eligible?",
             f"I would like to take {T} in {sem}. {done} Is that allowed?",
             f"{q} when I reach {sem}? {done}", f"Planning ahead: {done} {q} in {sem}?"]
    return lead(r, r.choice(forms)), {"sem_texts": [sem]}


def render_term_next(r, spec):
    k = spec["current_sem"]
    n = k - 1
    sem = sem_abs(r, n)
    variant = r.choice(["in_now", "just_finished", "just_ended"])
    pre = {"in_now": f"I am in {sem} now.", "just_finished": f"I have just finished {sem}.",
           "just_ended": f"{sem} just ended for me."}[variant]
    done = done_sentence(r, spec["completed"])
    q = r.choice(QUESTION).format(T=spec["target"]) + " next semester?"
    text = r.choice([f"{done} {pre} {q}", f"{pre} {done} {q}", f"{pre} {q} {done}"])
    return lead(r, text), {"sem_texts": [sem], "term_variant": variant}


CHUNK = ["Modules cleared: {L}.", "I also finished {L}.", "Besides those, I passed {L}.", "Also completed: {L}.",
         "On top of that I cleared {L}.", "Done as well: {L}."]
VERBS = ["take", "enrol in", "register for", "sign up for", "read"]


def render_scattered(r, spec):
    S = list(spec["completed"])
    r.shuffle(S)
    parts = 2 if len(S) < 6 else r.choice([2, 3])
    cut = sorted(r.sample(range(1, len(S)), parts - 1)) if len(S) > parts else []
    chunks = [S[i:j] for i, j in zip([0] + cut, cut + [len(S)]) if S[i:j]]
    first = "I have completed {L}.".format(L=listing(chunks[0]))
    rest = [t.format(L=listing(c)) for t, c in zip(r.sample(CHUNK, len(chunks) - 1), chunks[1:])]
    sem = sem_abs(r, spec["current_sem"])
    verb = r.choice(VERBS)
    q = r.choice([f"Is {spec['target']} something I can {verb} in {sem}?",
                  f"Would the prerequisites let me {verb} {spec['target']} in {sem}?",
                  f"I am wondering about {spec['target']}. Could I {verb} it in {sem}?",
                  f"Does my record allow me to {verb} {spec['target']} in {sem}?"])
    mid = r.randint(0, len(rest))
    skeleton = r.choice(["q_first", "q_middle", "q_last"])
    if skeleton == "q_first":
        text = " ".join([q, first] + rest)
    elif skeleton == "q_middle":
        text = " ".join([first] + rest[:mid] + [q] + rest[mid:])
    else:
        text = " ".join([first] + rest + [q])
    return lead(r, text), {"sem_texts": [sem]}


def render_correction(r, spec, ctx):
    """ctx: kind ('swap'|'drop'), decoy, swapped (course the decoy replaces), negated, wrong_sem."""
    S = list(spec["completed"])
    kind, decoy, negated = ctx["kind"], ctx["decoy"], ctx["negated"]
    if kind == "swap":
        z = ctx["swapped"]
        shown = [c for c in S if c != z] + [decoy]
        fix = r.choice([f"Sorry, not {decoy}, I meant {z}.", f"Correction: I never took {decoy}; it was {z}.",
                        f"Wait, {decoy} is wrong. I actually finished {z}."])
    else:
        shown = S + [decoy]
        fix = r.choice([f"Actually, scratch {decoy}, I have not taken it.", f"Sorry, I have not completed {decoy}.",
                        f"Wait, ignore {decoy}; I have not done that one."])
    r.shuffle(shown)
    parts = [f"I have completed {listing(shown)}.", fix]
    for x in negated:
        parts.append(r.choice([f"I have not taken {x}.", f"I haven't done {x} yet.", f"{x} is not on my record."]))
    k = spec["current_sem"]
    sem = sem_abs(r, k)
    sems = [sem]
    if ctx.get("wrong_sem"):
        w = sem_abs(r, ctx["wrong_sem"])
        q = f"I am looking at {w}. Sorry, I mean {sem}. {r.choice(QUESTION).format(T=spec['target'])}?"
        sems.append(w)
    else:
        q = f"{r.choice(QUESTION).format(T=spec['target'])} in {sem}?"
    if r.random() < 0.5:
        parts = [q] + parts
    else:
        parts = parts + [q]
    return lead(r, " ".join(parts)), {"sem_texts": sems}


def render_decoy(r, spec):
    done = done_sentence(r, spec["completed"])
    ind = sem_indirect(r, spec["current_sem"])
    q = r.choice(QUESTION).format(T=spec["target"])
    return r.choice([f"{done} I will be starting {ind}. {q} then?", f"{done} {q} in {ind}?",
                     f"{q} in {ind}? {done}"]), {"sem_texts": [ind]}


def render_missing(r, spec, which):
    T = spec.get("target")
    if which == "current_sem":
        done = done_sentence(r, spec["completed"])
        return r.choice([f"{done} {r.choice(QUESTION).format(T=T)} next semester?",
                         f"{r.choice(QUESTION).format(T=T)}? {done}",
                         f"{done} I want to take {T}. Am I eligible?"]), {}
    if which == "completed":
        sem = sem_abs(r, spec["current_sem"])
        return r.choice([f"{r.choice(QUESTION).format(T=T)} in {sem}?",
                         f"I am planning {sem}. {r.choice(QUESTION).format(T=T)}?",
                         f"I'd like to take {T} in {sem}. Am I eligible?"]), {"sem_texts": [sem]}
    sem = sem_abs(r, spec["current_sem"])
    done = done_sentence(r, spec["completed"])
    return r.choice([f"{done} I want to take one more module in {sem}. Am I eligible for it?",
                     f"{done} Can I take the module my friend recommended in {sem}?",
                     f"I am in {sem}. {done} Am I allowed to take the elective I picked?"]), {"sem_texts": [sem]}


def render_oos(r, spec, prog=None):
    text, info = render_plain(r, spec)
    if prog:
        pre = ("I am doing {}." if ("degree" in prog or "with" in prog) else "I am a {} student.").format(prog)
        text = pre + " " + text
    return text, info


# ---------------------------------------------------------------- generator
class Q1Gen:
    def __init__(self, seed):
        self.seed = seed
        self.r = random.Random(seed)
        self.cat = Catalog.load()
        self.C = self.cat.courses
        self.uses = Counter()          # families per target
        self.set_uses = Counter()      # base cases per completed set
        self.dead = Counter()
        usable = [c for c in self.C if self.usable(c)]
        self.filler = [c for c in usable if (c in CORE or c[:2] in ("CS", "MA", "ST", "IS", "ES")) and not c.endswith("R")
                       and (self.minf(c) <= 6)]
        self.pools = {}
        for L in LEVELS:
            elig = [c for c in usable if self.level(c)[0] == L and (self.C[c]["offered"] and set(self.C[c]["offered"]) & {1, 2})]
            self.pools[("elig", L)] = elig
            self.pools[("term", L)] = [c for c in elig if len(set(self.C[c]["offered"]) & {1, 2}) == 1]
            self.pools[("excl", L)] = [c for c in elig if self.excluders(c)]
            self.pools[("closed", L)] = [c for c, x in self.C.items() if x["exists_in_ay"] and not x["available"]
                                         and x.get("details") != "stub" and isinstance(x["prereq"]["logic"], dict)
                                         and self.level(c)[0] == L]

    # ---- catalogue helpers
    def usable(self, c):
        x = self.C.get(c)
        return bool(x and x["exists_in_ay"] and x["available"] and x.get("details") != "stub")

    def level(self, c):
        p = self.C[c]["prereq"]["logic"]
        if not isinstance(p, dict):
            return (0, 0, 0, 0)

        def flat(n):
            if n["op"] in ("and", "or"):
                out = []
                for a in n["args"]:
                    out += flat(a) if a["op"] == n["op"] else [a]
                return out
            return [n]
        groups = flat(p) if p["op"] == "and" else [p]
        simple = all(g["op"] == "course" or (g["op"] == "or" and all(a["op"] == "course" for a in flatten_or(g)))
                     for g in groups)
        h = sum(1 for g in groups if not (g["op"] == "course" or (g["op"] == "or" and all(a["op"] == "course" for a in flatten_or(g)))))
        g = len(groups)
        L = 1 if g == 1 and simple else 2 if g <= 3 and simple else 3
        m = len(set(self.C[c]["prereq"]["courses"]))
        return (L, g, h, m)

    def grade_gated(self, c):
        def walk(n):
            if not isinstance(n, dict):
                return False
            if n["op"] == "course":
                return n.get("min_grade") not in (None, "D")
            return any(walk(a) for a in n["args"])
        return walk(self.C[c]["prereq"]["logic"])

    def cap(self, c):
        return 2 if (c == "CS3233" or self.grade_gated(c)) else 4

    def excluders(self, T):
        x = self.C[T]["preclusion"]
        return sorted(b for b in set(x["courses"]) | set(x["mutually_exclusive_with"]) if b != T and self.usable(b))

    def minf(self, c):
        if c in ROAD_SEM:
            return ROAD_SEM[c]
        m = re.search(r"\d", c)
        return {1: 1, 2: 2, 3: 4, 4: 5}.get(int(m.group()) if m else 1, 6)

    def rank(self, c):
        return 0 if c in CORE else 1 if c[:2] == "CS" else 2

    def depth(self, S):
        memo, S = {}, set(S)

        def d(c, stack=()):
            if c in memo:
                return memo[c]
            if c in stack:
                return 1
            ps = [p for p in self.C[c]["prereq"]["courses"] if p in S and p != c]
            memo[c] = 1 + max([d(p, stack + (c,)) for p in ps] or [0])
            return memo[c]
        return max([d(c) for c in S] or [0])

    def fmin(self, S):
        return max([self.minf(c) for c in S] + [self.depth(S), 1 if S else 0])

    def lo_hi(self, f):
        return min(2 * f, 12), min(4 * f, 16)

    def fits(self, S, k):
        f = k - 1
        lo, hi = self.lo_hi(f)
        return (f == 0 and not S) or (f >= 1 and 1 <= len(S) <= min(5 * f, 18) and len(S) >= max(1, lo - 1)
                                       and self.fmin(S) <= f)

    # ---- transcript construction
    def sat(self, node, rng):
        if node is None or node is True:
            return set()
        if node is False:
            return None
        op = node["op"]
        if op == "course":
            return {node["code"]} if self.usable(node["code"]) else None
        if op == "and":
            out = set()
            for a in node["args"]:
                s = self.sat(a, rng)
                if s is None:
                    return None
                out |= s
            return out
        opts = [s for s in (self.sat(a, rng) for a in node["args"]) if s is not None]
        need = 1 if op == "or" else node["n"]
        if len(opts) < need:
            return None
        opts.sort(key=lambda s: sum(self.rank(c) for c in s) / max(len(s), 1) + rng.random() * 1.3)
        out = set()
        for s in opts[:need]:
            out |= s
        return out

    def closure(self, seed, rng):
        S, stack = set(seed), sorted(seed)
        while stack:
            c = stack.pop()
            p = self.C[c]["prereq"]["logic"]
            if p is False:
                return None
            if satisfied(p, S):
                continue
            s = self.sat(p, rng)
            if s is None:
                return None
            for d in sorted(s - S):
                S.add(d)
                stack.append(d)
        return S

    def conflicts(self, c, S):
        if self.cat.blocked_by(c, set(S)):
            return True
        x = self.C[c]["preclusion"]
        ex = set(x["courses"]) | set(x["mutually_exclusive_with"])
        for s in S:
            y = self.C[s]["preclusion"]
            if c in set(y["courses"]) | set(y["mutually_exclusive_with"]) or s in ex:
                return True
        return False

    def fill(self, S, T, f, n, rng, forbid=()):
        S = set(S)
        while len(S) < n:
            cands = []
            for c in self.filler:
                if c in S or c == T or c in forbid or self.minf(c) > f:
                    continue
                if not self.cat.can_take(c, S)[0] or self.conflicts(c, S) or self.cat.blocked_by(T, S | {c}):
                    continue
                if self.depth(S | {c}) > f:
                    continue
                cands.append(c)
            if not cands:
                break
            S.add(rng.choices(cands, weights=[3 if c in CORE else 1 for c in cands])[0])
        return S

    def base_transcript(self, T, rng, allowed=None, kmin=2, include_T=False):
        p = self.C[T]["prereq"]["logic"]
        seed = self.sat(p, rng)
        if seed is None:
            return None
        S0 = self.closure(seed | ({T} if include_T else set()), rng)
        if S0 is None:
            return None
        fm = self.fmin(S0)
        ks = [f + 1 for f in range(max(fm, kmin - 1, 1), 8) if allowed is None or term_of(f + 1) in allowed]
        rng.shuffle(ks)
        for k in ks:
            f = k - 1
            lo, hi = self.lo_hi(f)
            if len(S0) > max(hi, lo):
                continue
            n = rng.randint(max(lo, len(S0)), max(hi, len(S0)))
            S = self.fill(S0, T, f, n, rng)
            if self.fits(S, k):
                return sorted(S, key=lambda c: (self.minf(c), c)), k
        return None

    def solve(self, spec):
        return run(json.loads(json.dumps(spec)), self.cat)

    @staticmethod
    def spec(T, k, S):
        return {"query": "eligible", "target": T, "current_sem": k, "completed": list(S)}

    def reasons_of(self, spec):
        a = self.solve(spec)
        return a, " | ".join(a.get("reasons", []))

    # ---- builders
    def pick(self, pool, rng, cost=1):
        live = [t for t in pool if self.uses[t] + cost <= self.cap(t) and self.dead[t] < 12]
        if not live:
            raise RuntimeError("target pool exhausted")
        m = min(self.uses[t] for t in live)
        return rng.choice([t for t in live if self.uses[t] == m])

    def add_excluder(self, T, S, k, rng):
        bs = self.excluders(T)
        rng.shuffle(bs)
        for b in bs:
            if b in S:
                continue
            S2 = self.closure(set(S) | {b}, rng)
            if S2 is None or not self.fits(S2, k) or len(S2 - set(S)) > 3:
                continue
            spec = self.spec(T, k, sorted(S2, key=lambda c: (self.minf(c), c)))
            a, rs = self.reasons_of(spec)
            if a["status"] == "NOT_ELIGIBLE" and ("precluded" in rs or "mutually exclusive" in rs) \
                    and not any(w in rs for w in ("missing", "not offered", f"{T} already completed", "unavailable")):
                return spec, b
        return None

    def takeable_now(self, c, S, k):
        return self.cat.can_take(c, set(S), semester=term_of(k))[0]

    def removal(self, S, gone):
        R = set(gone)
        changed = True
        while changed:
            changed = False
            for s in S:
                if s in R:
                    continue
                p = self.C[s]["prereq"]["logic"]
                if isinstance(p, dict) and not satisfied(p, set(S) - R):
                    R.add(s)
                    changed = True
        return R

    def near_miss(self, T, S, k, want_now, rng):
        p = self.C[T]["prereq"]["logic"]
        Sset = set(S)
        crit = [c for c in S if not satisfied(p, Sset - {c})]
        rng.shuffle(crit)
        f = k - 1
        lo, _ = self.lo_hi(f)
        for c in crit:
            options = [{c}]
            for q in self.C[c]["prereq"]["courses"]:
                if q in Sset:
                    options.append({c, q})
            for gone in options:
                R = self.removal(Sset, gone)
                S2 = Sset - R
                now = self.takeable_now(c, S2, k)
                if now != want_now:
                    continue
                if len(S2) < max(1, lo - 1):
                    S2 = self.fill(S2, T, f, lo, rng, forbid=R)
                    if satisfied(p, S2):
                        continue
                if not self.fits(S2, k):
                    continue
                spec = self.spec(T, k, sorted(S2, key=lambda x: (self.minf(x), x)))
                a, rs = self.reasons_of(spec)
                if a["status"] == "NOT_ELIGIBLE" and "missing prerequisite" in rs and not any(
                        w in rs for w in ("not offered", "precluded", f"{T} already completed", "unavailable", "mutually")):
                    return spec, c, sorted(R)
        return None

    def eligible_family(self, L, ftype, want_now, rng):
        for _ in range(600):
            pool = self.pools[("term" if ftype == "term" else "excl" if ftype == "excl" else "elig", L)]
            T = self.pick(pool, rng, cost=2)
            allowed = set(self.C[T]["offered"]) & {1, 2}
            st = self.base_transcript(T, rng, allowed=allowed, kmin=3 if ftype == "term" else 2)
            if not st:
                self.dead[T] += 1
                continue
            S, k = st
            spec = self.spec(T, k, S)
            a, rs = self.reasons_of(spec)
            if a["status"] != "ELIGIBLE" or self.set_uses[frozenset(S)] >= 3:
                self.dead[T] += 1
                continue
            nm = self.near_miss(T, S, k, want_now, rng)
            if not nm:
                self.dead[T] += 0.5
                continue
            fam = {"E": spec, "M": nm[0], "missing_course": nm[1], "removed": nm[2], "missing_now": want_now,
                   "ftype": ftype, "T": T}
            if ftype == "excl":
                x = self.add_excluder(T, S, k, rng)
                if not x:
                    self.dead[T] += 0.5
                    continue
                fam["X"], fam["excluder"] = x
            self.uses[T] += 2     # the ELIGIBLE base and its near-miss are two base cases
            self.set_uses[frozenset(S)] += 1
            return fam
        raise RuntimeError(f"eligible family L{L} {ftype}")

    def simple_case(self, kind, L, rng):
        for _ in range(600):
            if kind == "wrong_term":
                T = self.pick(self.pools[("term", L)], rng)
                allowed = {1, 2} - set(self.C[T]["offered"])
                st = self.base_transcript(T, rng, allowed=allowed, kmin=3)
            elif kind == "closed":
                T = self.pick(self.pools[("closed", L)], rng)
                st = self.base_transcript(T, rng)
            elif kind == "already_done":
                T = self.pick(self.pools[("elig", L)], rng)
                st = self.base_transcript(T, rng, allowed=set(self.C[T]["offered"]) & {1, 2}, include_T=True)
            else:  # precluded
                T = self.pick(self.pools[("excl", L)], rng)
                st = self.base_transcript(T, rng, allowed=set(self.C[T]["offered"]) & {1, 2})
            if not st:
                self.dead[T] += 1
                continue
            S, k = st
            extra = {}
            if kind == "precluded":
                x = self.add_excluder(T, S, k, rng)
                if not x:
                    self.dead[T] += 1
                    continue
                spec, extra["excluder"] = x
            else:
                spec = self.spec(T, k, S)
            a, rs = self.reasons_of(spec)
            bad = ("missing", "precluded", "mutually", f"{T} already completed")
            ok = {"wrong_term": a["status"] == "NOT_ELIGIBLE" and "not offered" in rs and not any(w in rs for w in
                                                                                                    ("missing", "precluded", f"{T} already completed", "unavailable", "mutually")),
                  "closed": a["status"] == "NOT_ELIGIBLE" and "unavailable" in rs and not any(w in rs for w in bad),
                  "already_done": a["status"] == "NOT_ELIGIBLE" and rs == f"{T} already completed",
                  "precluded": a["status"] == "NOT_ELIGIBLE"}[kind]
            if not ok or self.set_uses[frozenset(spec["completed"])] >= 3:
                self.dead[T] += 1
                continue
            self.uses[T] += 1
            self.set_uses[frozenset(spec["completed"])] += 1
            return {"spec": spec, "T": T, **extra}
        raise RuntimeError(f"case {kind} L{L}")

    # ---- assembly
    def build(self):
        rng = self.r
        bases = []     # base cases, in order
        n = Counter()

        def new_id(code):
            n[code] += 1
            return f"q1-{code}-{n[code]:03d}"

        for L in LEVELS:
            plan = [t for t, c in ELIG_TYPES.items() for _ in range(c)]
            rng.shuffle(plan)
            # exactly half of the 18 near-misses have a missing course the student could take now
            flags = {"term": [True] * 5 + [False] * 5, "excl": [True] * 3 + [False] * 3, "plain": [True, False]}
            for v in flags.values():
                rng.shuffle(v)
            for ft in plan:
                fam = self.eligible_family(L, ft, flags[ft].pop(), rng)
                eid, mid = new_id("el"), new_id("mp")
                T = fam["T"]
                bases.append({"id": eid, "reason": "eligible", "L": L, "spec": fam["E"], "pair": eid,
                              "twin": "term" if ft == "term" else "excl" if ft == "excl" else None, "fam": fam})
                bases.append({"id": mid, "reason": "missing_prereq", "L": L, "spec": fam["M"], "pair": eid, "twin": None,
                              "fam": fam, "missing_course": fam["missing_course"], "removed": fam["removed"],
                              "missing_now": fam["missing_now"]})
                if ft == "excl":
                    bases[-2]["excl_twin_spec"] = fam["X"]
                    bases[-2]["excluder"] = fam["excluder"]
            for kind, code in (("precluded", "ex"), ("wrong_term", "wt"), ("closed", "cl"), ("already_done", "ad")):
                for _ in range(PER_LEVEL[kind]):
                    c = self.simple_case(kind, L, rng)
                    bases.append({"id": new_id(code), "reason": kind, "L": L, "spec": c["spec"], "pair": None,
                                  "twin": "term" if kind == "wrong_term" else None, "fam": None,
                                  "excluder": c.get("excluder")})

        # harder-wording style: E and M of one pair share a style; the rest alternate
        pairs = sorted({b["pair"] for b in bases if b["reason"] == "eligible"})
        styles = {}
        for i, pid in enumerate(rng.sample(pairs, len(pairs))):
            styles[pid] = "scattered" if i % 2 == 0 else "correction"
        others = [b for b in bases if b["reason"] not in ("eligible", "missing_prereq")]
        rng.shuffle(others)
        for i, b in enumerate(others):
            styles[b["id"]] = "scattered" if i % 2 == 0 else "correction"
        for b in bases:
            b["style"] = styles[b["pair"] if b["reason"] in ("eligible", "missing_prereq") else b["id"]]
        return bases

    def correction_ctx(self, b, rng):
        spec = b["spec"]
        S, T = spec["completed"], spec["target"]
        decoy = swapped = None
        kind = rng.choice(["drop", "swap"])
        gold = self.solve(spec)["status"]
        if kind == "drop":
            if b["reason"] == "missing_prereq":
                decoy = b["missing_course"]
            elif b["reason"] == "eligible" and self.excluders(T):
                decoy = rng.choice(self.excluders(T))
            else:
                kind = "swap"
        taken = set(S) | {T}
        if kind == "swap":
            swapped = rng.choice(S)
            cands = [c for c in self.filler if c not in taken and c not in self.excluders(T)]
            decoy = rng.choice(cands)
        negated = []
        for _ in range(rng.choice([1, 1, 2])):
            cands = [c for c in self.filler if c not in taken and c != decoy and c not in negated]
            negated.append(rng.choice(cands))
        k = spec["current_sem"]
        wrong = None
        if rng.random() < 0.5:
            wrong = rng.choice([x for x in (k - 1, k + 1) if 1 <= x <= 8])
        flips = None
        if kind == "drop":
            flips = self.solve({**spec, "completed": list(S) + [decoy]})["status"] != gold
        return {"kind": kind, "decoy": decoy, "swapped": swapped, "negated": negated, "wrong_sem": wrong,
                "retraction_flips_answer": flips}

    def instance(self, iid, kind, spec, text, info, meta):
        return {"id": iid, "kind": kind, "request": text, "gold_spec": spec, "gold_answer": self.solve(spec),
                "meta": {**meta, **info}}

    def rows(self, bases):
        rows, seed = [], self.seed

        def rr(iid):
            return random.Random(f"{seed}-{iid}")

        for b in bases:
            spec, T, L = b["spec"], b["spec"]["target"], b["L"]
            _, g, h, m = self.level(T)
            kind = f"q1/{b['reason']}"
            base_meta = {"reason": b["reason"], "level": L, "g": g, "h": h, "m": m, "target": T,
                         "base_id": b["id"], "pair_id": b["pair"], "finished_semesters": spec["current_sem"] - 1,
                         "n_completed": len(spec["completed"]), "group": "base"}
            if b["reason"] == "missing_prereq":
                base_meta.update(missing_course=b["missing_course"], missing_course_takeable_now=b["missing_now"])
            if b.get("excluder"):
                base_meta["excluder"] = b["excluder"]
            text, info = render_plain(rr(b["id"] + "-p"), spec)
            rows.append(self.instance(b["id"] + "-p", kind, spec, text, info, {**base_meta, "style": "plain", "role": "base_plain",
                                                                              "term_form": "absolute"}))
            r = rr(b["id"] + "-h")
            if b["style"] == "scattered":
                text, info = render_scattered(r, spec)
                extra = {}
            else:
                ctx = self.correction_ctx(b, r)
                text, info = render_correction(r, spec, ctx)
                extra = {"correction_kind": ctx["kind"], "retracted": [ctx["decoy"]], "negated": ctx["negated"],
                         "retraction_flips_answer": ctx["retraction_flips_answer"]}
                if ctx["wrong_sem"]:
                    extra["retracted_semester"] = ctx["wrong_sem"]
            rows.append(self.instance(b["id"] + "-h", kind, spec, text, {**info, **extra},
                                      {**base_meta, "style": b["style"], "role": "base_harder", "term_form": "absolute"}))
            if b["twin"] == "term":
                text, info = render_term_next(rr(b["id"] + "-t"), spec)
                rows.append(self.instance(b["id"] + "-t", kind, spec, text, info,
                                          {**base_meta, "style": "plain", "role": "term_twin", "term_form": "relative"}))
            if b["twin"] == "excl":
                xs = b["excl_twin_spec"]
                text, info = render_plain(rr(b["id"] + "-x"), xs)
                rows.append(self.instance(b["id"] + "-x", "q1/precluded", xs, text, info,
                                          {**base_meta, "reason": "precluded", "style": "plain", "role": "exclusion_twin",
                                           "excluder": b["excluder"], "n_completed": len(xs["completed"]),
                                           "term_form": "absolute"}))
        rows += self.info_groups()
        return rows

    def eligible_like(self, rng, status, both_terms=False):
        """A Q1 spec with the wanted gold status, for the MISSING_INFO, decoy and OUT_OF_SCOPE groups.
        both_terms: the target is offered in both semesters, so the semester would not change the answer."""
        for _ in range(300):
            L = rng.choice([1, 2])
            T = rng.choice(self.pools[("elig", L)])
            if both_terms and not {1, 2} <= set(self.C[T]["offered"]):
                continue
            allowed = set(self.C[T]["offered"]) & {1, 2}
            st = self.base_transcript(T, rng, allowed=allowed, kmin=3)
            if not st:
                continue
            spec = self.spec(T, st[1], st[0])
            if status == "NOT_ELIGIBLE":
                nm = self.near_miss(T, st[0], st[1], rng.random() < 0.5, rng)
                if not nm:
                    continue
                spec = nm[0]
            if self.solve(spec)["status"] == status:
                return spec
        raise RuntimeError("eligible_like")

    def info_groups(self):
        rows, rng, seed = [], random.Random(self.seed + 1), self.seed
        n = Counter()

        def rr(iid):
            return random.Random(f"{seed}-{iid}")

        def add(kind, code, spec, text, info, meta):
            n[code] += 1
            iid = f"q1-{code}-{n[code]:02d}"
            rows.append(self.instance(iid, kind, spec, text, info, {"level": None, "group": meta.pop("group"),
                                                                    "style": "plain", "role": "info", **meta}))
            return iid

        # true MISSING_INFO: 7 without the completed list, 7 without a target (a missing semester is NOT
        # MISSING_INFO for Q1: the solver answers when the term does not matter)
        for which, cnt in (("completed", 7), ("target", 7)):
            for _ in range(cnt):
                spec = self.eligible_like(rng, rng.choice(["ELIGIBLE", "NOT_ELIGIBLE"]))
                full = json.loads(json.dumps(spec))
                spec.pop(which)
                iid = f"q1-mi-{n['mi'] + 1:02d}"
                text, info = render_missing(rr(iid), full, which)
                add("missing_info/q1", "mi", spec, text, info, {"group": "missing_info", "missing": which,
                                                                "reason": "missing_info"})
        # decoys: the semester is left out but the answer does not depend on it (target offered in both terms)
        for status in ["ELIGIBLE"] * 3 + ["NOT_ELIGIBLE"] * 3:
            full = self.eligible_like(rng, status, both_terms=True)
            spec = json.loads(json.dumps(full))
            spec.pop("current_sem")
            iid = f"q1-dc-{n['dc'] + 1:02d}"
            text, info = render_missing(rr(iid), full, "current_sem")
            add("q1/decoy", "dc", spec, text, info, {"group": "missing_info_decoy", "reason": "decoy",
                                                     "target": spec["target"], "hidden_sem": full["current_sem"]})
        # OUT_OF_SCOPE: 5 programme, 5 not in catalogue, 5 other faculty, 5 semester outside 1-8
        for i in range(5):
            spec = self.eligible_like(rng, "ELIGIBLE")
            prog = OOS_PROGRAMMES[i]
            spec["programme"] = prog
            iid = f"q1-os-{n['os'] + 1:02d}"
            text, info = render_oos(rr(iid), spec, prog)
            add("out_of_scope/programme", "os", spec, text, info, {"group": "out_of_scope", "reason": "oos_programme",
                                                                   "programme": prog})
        for kind, codes in (("not_in_catalogue", OOS_NOT_IN_CATALOGUE), ("other_faculty", OOS_OTHER_FACULTY)):
            for code in codes:
                assert code not in self.C, code
                spec = self.eligible_like(rng, "ELIGIBLE")
                spec["target"] = code
                iid = f"q1-os-{n['os'] + 1:02d}"
                text, info = render_plain(rr(iid), spec)
                add("out_of_scope/course", "os", spec, text, info, {"group": "out_of_scope", "reason": f"oos_{kind}",
                                                                    "target": code})
        for k in (9, 10, 9, 11, 12):
            spec = self.eligible_like(rng, "ELIGIBLE")
            spec["current_sem"] = k
            iid = f"q1-os-{n['os'] + 1:02d}"
            text, info = render_plain(rr(iid), spec)
            add("out_of_scope/semester", "os", spec, text, info, {"group": "out_of_scope", "reason": "oos_semester",
                                                                  "semester": k})
        return rows


def flatten_or(g):
    out = []
    for a in g["args"]:
        out += flatten_or(a) if a["op"] == "or" else [a]
    return out


# ---------------------------------------------------------------- checks and output
WANT_STATUS = {"missing_info/q1": "MISSING_INFO", "out_of_scope/programme": "OUT_OF_SCOPE",
               "out_of_scope/course": "OUT_OF_SCOPE", "out_of_scope/semester": "OUT_OF_SCOPE"}


def check_text(x):
    """Every rendering must state exactly its gold spec: all completed codes and the target appear, every other
    code is a recorded retraction or negation, and the semester wording appears."""
    spec, m, t = x["gold_spec"], x["meta"], x["request"]
    codes = set(CODE_RE.findall(t))
    want = set(spec.get("completed", [])) | ({spec["target"]} if "target" in spec else set())
    allowed_extra = set(m.get("retracted", [])) | set(m.get("negated", []))
    assert want <= codes, (x["id"], want - codes)
    assert codes - want <= allowed_extra, (x["id"], codes - want - allowed_extra)
    for s in m.get("sem_texts", []):
        assert s in t, (x["id"], s)
    if x["meta"].get("role") == "term_twin":
        assert "next semester" in t, x["id"]


def verify(rows, g):
    assert len(rows) == 400, len(rows)
    ids = [x["id"] for x in rows]
    assert len(set(ids)) == 400
    for x in rows:
        check_text(x)
        st = x["gold_answer"]["status"]
        w = WANT_STATUS.get(x["kind"])
        if w:
            assert st == w, (x["id"], st)
        if x["meta"]["group"] in ("base", "missing_info_decoy"):
            sp = x["gold_spec"]
            k = sp.get("current_sem") or x["meta"]["hidden_sem"]
            assert g.fits(set(sp["completed"]), k), (x["id"], "transcript does not fit the semester")
    base = [x for x in rows if x["meta"]["role"] == "base_plain"]
    assert len(base) == 150, len(base)
    for L in LEVELS:
        assert sum(1 for x in base if x["meta"]["level"] == L) == 50
    exp = {"eligible": 54, "missing_prereq": 54, "precluded": 15, "wrong_term": 12, "closed": 9, "already_done": 6}
    assert Counter(x["meta"]["reason"] for x in base) == exp, Counter(x["meta"]["reason"] for x in base)
    role = Counter(x["meta"]["role"] for x in rows)
    assert role["base_harder"] == 150 and role["term_twin"] == 42 and role["exclusion_twin"] == 18 and role["info"] == 40, role
    sty = Counter(x["meta"]["style"] for x in rows)
    assert sty["scattered"] == 75 and sty["correction"] == 75 and sty["plain"] == 250, sty
    nm = [x for x in base if x["meta"]["reason"] == "missing_prereq"]
    assert sum(1 for x in nm if x["meta"]["missing_course_takeable_now"]) == 27
    stat = Counter(x["gold_answer"]["status"] for x in rows)
    assert stat == {"ELIGIBLE": 141, "NOT_ELIGIBLE": 225, "MISSING_INFO": 14, "OUT_OF_SCOPE": 20}, stat
    return stat


def gating(rows, rng):
    """80 instances: 10 term pairs, 10 exclusion pairs, 10 scattered pairs, 10 correction pairs (no instance twice)."""
    by = defaultdict(dict)
    for x in rows:
        if x["meta"].get("base_id"):
            by[x["meta"]["base_id"]][x["meta"]["role"]] = x
    used, out = set(), []

    def take(role_pair, cond, n, per_level=True):
        cands = [b for b, d in by.items() if role_pair in d and "base_plain" in d and cond(d) and b not in used]
        rng.shuffle(cands)
        got = []
        for L in LEVELS:
            pool = [b for b in cands if by[b]["base_plain"]["meta"]["level"] == L]
            got += pool[: n // 3 + (1 if L == 1 and n % 3 else 0)]
        for b in got:
            used.add(b)
            out.extend([by[b]["base_plain"], by[b][role_pair]])
        return len(got)
    take("term_twin", lambda d: True, 10)
    take("exclusion_twin", lambda d: True, 10)
    take("base_harder", lambda d: d["base_harder"]["meta"]["style"] == "scattered" and
         d["base_plain"]["meta"]["reason"] in ("eligible", "missing_prereq"), 10)
    take("base_harder", lambda d: d["base_harder"]["meta"]["style"] == "correction" and
         d["base_plain"]["meta"]["reason"] in ("eligible", "missing_prereq"), 10)
    return out


def summary(rows, g, stat, seed):
    L = [f"# Q1 instance set (seed {seed})", "", f"{len(rows)} instances. Regenerate with "
         f"`python -m instances.generate_q1 --seed {seed}`.", ""]

    def table(title, header, data):
        L.extend([f"## {title}", "", "| " + " | ".join(header) + " |", "|" + "---|" * len(header)])
        L.extend("| " + " | ".join(str(c) for c in row) + " |" for row in data)
        L.append("")
    table("By gold status", ["Status", "Instances"], sorted(stat.items()))
    base = [x for x in rows if x["meta"]["role"] == "base_plain"]
    table("Base cases by reason and level", ["Reason", "L1", "L2", "L3", "Base cases", "Instances"],
          [[r] + [sum(1 for x in base if x["meta"]["reason"] == r and x["meta"]["level"] == lv) for lv in LEVELS]
           + [sum(1 for x in base if x["meta"]["reason"] == r),
              sum(1 for x in rows if x["meta"]["reason"] == r and x["meta"]["group"] == "base")]
           for r in ["eligible", "missing_prereq", "precluded", "wrong_term", "closed", "already_done"]])
    table("Roles", ["Role", "Instances"], sorted(Counter(x["meta"]["role"] for x in rows).items()))
    table("Wording style", ["Style", "Instances"], sorted(Counter(x["meta"]["style"] for x in rows).items()))
    table("Complexity level of all instances", ["Level", "Instances"],
          sorted(Counter(str(x["meta"]["level"]) for x in rows).items()))
    tu = Counter(x["meta"]["target"] for x in base if x["meta"].get("target"))
    L += [f"Target use among base cases: max {max(tu.values())}, distinct targets {len(tu)}; "
          f"CS3233 base cases: {tu.get('CS3233', 0)}.", ""]
    su = Counter(tuple(sorted(x["gold_spec"]["completed"])) for x in base if x["meta"]["reason"] != "missing_prereq")
    L += [f"Completed-set reuse among non-missing base cases: max {max(su.values())}.", ""]
    opens = Counter(" ".join(x["request"].split()[:2]).lower() for x in rows)
    top = opens.most_common(5)
    L += ["Sentence openings (first two words), top 5: " + ", ".join(f"{w} {c / len(rows):.0%}" for w, c in top), ""]
    cs = [x for x in rows if x["meta"].get("correction_kind")]
    fl = sum(1 for x in cs if x["meta"].get("retraction_flips_answer"))
    L += [f"Correction renderings: {len(cs)}; retracted course would change the answer in {fl} of "
          f"{sum(1 for x in cs if x['meta']['correction_kind'] == 'drop')} 'drop' cases.", ""]
    L += ["## Examples", ""]
    seen = set()
    for x in rows:
        key = (x["kind"], x["meta"]["role"], x["meta"]["style"])
        if key in seen or len(seen) > 40:
            continue
        seen.add(key)
        L.append(f"- **{x['id']}** ({x['gold_answer']['status']}, {x['meta']['role']}, {x['meta']['style']}): {x['request']}")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=3263)
    ap.add_argument("--outdir", default=str(HERE))
    a = ap.parse_args()
    g = Q1Gen(a.seed)
    bases = g.build()
    rows = g.rows(bases)
    stat = verify(rows, g)
    gate = gating(rows, random.Random(a.seed + 2))
    out = Path(a.outdir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "q1_400.json").write_text(json.dumps(rows, indent=1))
    (out / "q1_gating.json").write_text(json.dumps(gate, indent=1))
    (out / "Q1_SUMMARY.md").write_text(summary(rows, g, stat, a.seed))
    print(f"wrote {len(rows)} instances ({len(gate)} gating) to {out}")
    print(dict(stat))


if __name__ == "__main__":
    main()
