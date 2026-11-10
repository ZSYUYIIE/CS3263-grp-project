# Data coverage: which courses we answer for

Short note for the team (10 Nov 2026). It explains the catalogue change in PR #2 and what to say
about it in the report. Field-level details are in [`DATA_SCHEMA.md`](DATA_SCHEMA.md#stubs).

## The rule: coverage by dependency

The catalogue has **full records** for:

1. every School of Computing course (prefixes CS, CSA, IS, ISC, ISD, ISE, ISY, IFS, BT, IT, CP)
   at levels 1000-4999, and
2. every course that any of those courses' rules depends on, followed all the way down
   (prerequisites of prerequisites, plus courses named in preclusions and corequisites and their
   prerequisites).

That gives 393 full records for AY2026/27 (before PR #2: 306). Config: `data/config/scope.json`
(`seed_prefixes`, `expand_all_refs`). Rebuild with `python -m m1_data fetch` then `build`.

We include a course because **a rule we care about depends on it**, not because CS students
often take it. So BT2101 is in (BT4240, BT4221 and IS4303 need it), while MA2101 is out (no SoC
rule mentions it), even though a CS student is more likely to take MA2101 as a UE. Every MA/ST
course that a CS or SoC rule names (MA1521, MA1522, MA2116, ST2131, ST2132, ST2334, ...) has full
details. We tried also seeding all of MA and ST. It changed no CS answer, so we dropped it to keep
the rule to one sentence.

## What the system answers for each kind of course

| Course | Example | Answer |
|---|---|---|
| Full record | CS3263, BT4240, ST2131 | normal answer (ELIGIBLE / NOT_ELIGIBLE / PLAN / NO_PLAN) |
| Real AY2026/27 course, known only by name (stub) | MA2101, NM2101 | **OUT_OF_SCOPE**: "a real AY course, but its details are not in the catalogue (outside our data coverage)" |
| Not in the catalogue at all | CM1102, GEC1015 | **OUT_OF_SCOPE**: "not in the catalogue" |
| Retired (no AY2026/27 page) | CS1010, MA1101R | can't be taken or planned; still counts if it is on a transcript |
| Full record whose only route runs through a stub | NM4259 (needs "any NM course") | NOT_ELIGIBLE / NO_PLAN with `data_limited: true`; Q1 says `can_still_become_eligible: "unknown"`, never "impossible" |

A stub on a transcript still counts: taking MA2101 correctly blocks MA1301, which MA2101 precludes.

## OUT_OF_SCOPE has two causes

1. **Student scope**: not BComp CS Hons single major (DDP, second major, minor, other programme,
   other AY). The rules differ, so any answer would be wrong.
2. **Course coverage**: a real course we did not model. The student may well be able to take it.
   We decline rather than guess.

Both mean "we don't model this, check NUSMods or an advisor", never "you can't". The reason
text says which cause applies. Grading compares only the status, so nothing changes for the experiments.

## Why this changed (the bug)

On `main`, 12 courses that are in the catalogue were answered "never eligible" only because one of
their prerequisites had not been fetched (e.g. BT4240 needs BT2101, which was a stub). The affected
courses were BT4221, BT4240, DBA3701, EC3303, EE4212, EE4704, EE5731, NM4259, NM4260, TCE2407, TCX3222 and TEE4204.
**No CS course was affected**, so no CS result or instance changes. PR #2 fixes it in two ways:
it fetches the missing prerequisites, and a reason that rests on missing data is tagged `[data gap]`,
so it reads as "unknown", not "impossible".

## Effect on experiments

- `instances/instances.json` was regenerated once in PR #2. It had been stale since the Q2
  `light_sems` / `balance_load` removal (c229e61). Q1 instances are unchanged; 85 of 115 Q2 /
  infeasible / missing-info / out-of-scope instances changed because the generator's random stream
  shifted. **Re-run any Route A or Route B results produced on the old file.** Later commits in the
  PR left the file byte-for-byte unchanged.
- Route A's record text now describes a name-only course as "a real AY2026/27 course, but its
  details are not in the records" (it used to say "old or retired", which was wrong).

## Suggested report wording

> Our catalogue covers all School of Computing courses for AY2026/27 and every course their rules
> depend on (393 courses with full records). Coverage is defined by dependency rather than
> popularity, so it is reproducible. A course outside it, e.g. MA2101 taken as an unrestricted
> elective, is declined as OUT_OF_SCOPE rather than guessed. Missing data is never reported as
> academic impossibility: a conclusion that rests on an unfetched record is labelled data-limited.
> Extending coverage is a data change, not a model change.

## Known assumptions (worth one line each in the report)

- A course with no semester listed in AY2026/27 (71 courses, e.g. CS3226) is treated as not
  offered in every future semester too: we assume offerings repeat yearly.
- Every student is resolved as cohort 2024 with a fixed set of A-level subjects
  (`data/config/student_context.json`). An A-level alternative the student lacks resolves to false
  (e.g. LSM2241's A-level Biology route, so it needs LSM1301; CS3242's A-level route, which still
  leaves the PC1201 route).
- Unknown GPA or units-completed conditions are assumed met.
