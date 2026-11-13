# Guide for AI agents

You are working in the CS3263 project repo (LLM vs constraint solver for NUS degree
planning). Read `README.md` for the project, `docs/CODE_GUIDE.md` for how the code fits together,
and `docs/DATA_SCHEMA.md` for the data contract.
This file covers what you need to avoid mistakes.

## Ground rules

1. **Course facts come from the data, never from memory.** Prerequisites and preclusions change
   every year. Your training data is likely an older AY. Look the course up in
   `data/processed/AY2026-2027/catalog.json` (or `COURSES.md`) and cite the AY.
2. **Do not edit `data/processed/`, `data/raw/` or `docs/diagrams/`.** They are generated. To change an output,
   fix the parser in `m1_data/` or add an entry with a `reason` to `data/manual/overrides.json`,
   then run `python -m m1_data build`.
3. **After any change, run `ruff check .` and `python -m pytest -q`; after a change to `m1_data/`,
   also `python -m m1_data build`.** All must pass before pushing.
4. **Keep the evaluation checker independent.** Code under `eval/` must not import
   `m1_data.catalog` or `m1_data.resolve`. It implements the rules from `docs/DATA_SCHEMA.md`
   itself, so a bug in one side shows up as a disagreement.
5. **Never put the answer in the prompt.** Pipeline A gives the LLM course records, chosen by the
   rule written in the report. Don't add fields like `available` or `reachable` that do the
   reasoning for the model unless that is the condition being tested.

6. **Out-of-scope students get OUT_OF_SCOPE, never a plan.** The data covers BComp (CS) Hons,
   single major, AY2026/27 only. DDP, second majors, minors and other programmes are declined
   with a reason (`m1_data/scope.py`, `docs/DATA_SCHEMA.md#scope`). Never answer "the CS part
   anyway".

7. **The instance files are generated; never edit them by hand.** `instances/instances.json` comes from
   `python -m instances.generate`, and `q1_400.json` / `q1_gating.json` from `python -m instances.generate_q1`.
   Their gold answers are the solver's answers at generation time, so after any change to the spec format
   (`solver/spec.py`) or to the solver's rules, regenerate them and run the tests. Regenerating can change the
   request texts: results in `results/` made from an older file must be rerun, not mixed with new ones.
8. **A change to a hard rule is made in three places:** `solver/model.py`, `solver/backtrack.py` and
   `eval/checker.py` implement the rules independently on purpose. Do not make one import another. Update the
   two prompts (`pipelines/prompt_a.py`, `pipelines/prompt_b.txt`) and the guides in the same change.
9. **Only pipelines A and B exist.** A: the LLM answers directly. B: the LLM writes a spec and the solver
   answers it. Do not describe other pipelines in the docs unless they are added to `pipelines/`.

10. **The MDP extension is an add-on, not a pipeline.** `solver/mdp.py` and `solver/admission.py` answer "what
    should I bid for when a bid can fail" for a Q2 spec (`docs/MDP_GUIDE.md`). `solver/run.py`, the pipelines, the
    instance generators and `eval/` must not import them, and the spec format does not change for them. The
    interactive planner may: it offers the check after a plan (`planner/cli.py` `offer_bidding`, text in
    `planner/formatting.py` `format_bidding`), so a change to the `POLICY` answer fields must keep that view and
    `tests/test_planner.py` working.
    `BiddingMDP.legal` and `bids` restate the offering, prerequisite, corequisite, exclusion and MC-cap rules for
    one semester, so a change to those rules (rule 8) is made there too; `tests/test_mdp.py` fails if the MDP
    with every probability equal to 1 stops agreeing with CP-SAT and the checker.
11. **`data/demand/allocation.csv` is generated; never edit it by hand.** It comes from
    `python -m experiments.extract_demand <folder>` run on `pdftotext -layout` output of the CourseReg demand and
    allocation reports (`data/demand/README.md`). The numbers in `docs/MDP_GUIDE.md` and the README come from
    `python -m experiments.run_mdp`; rerun it and update them after changing that file, the estimators in
    `solver/admission.py`, the MDP or the instance set.

## LLM configuration

All four pipeline CLI runners call `pipelines.config.load_env()` before reading settings.
It loads only the project-root `.env` using `python-dotenv`, preserving existing environment
variables. Keep `.env` Git-ignored and use `.env.example` for placeholder configuration.
Update both `pyproject.toml` and `requirements-dev.txt` when adding runtime dependencies.

## Finding things fast

| Need | Where |
|---|---|
| One course, readable | `grep -n -A 12 "^### CS3263" data/processed/AY2026-2027/COURSES.md` |
| One course, structured | `catalog.json → courses → "CS3263"` or `Catalog.load()["CS3263"]` |
| Entry point for one spec | `solver/run.py` → `run(spec, catalog)`; Q1 in `solver/q1.py`, Q2 in `solver/q2.py` (model in `solver/model.py`) |
| The instance sets | `instances/instances.json` (115 mixed), `q1_400.json`, `q1_gating.json`; counts in `instances/SUMMARY.md`, `Q1_SUMMARY.md` |
| Run or grade a pipeline | `pipelines/README.md` |
| Bidding policy when a bid can fail | `python -m solver.mdp spec.json`; `docs/MDP_GUIDE.md` |
| Chance of getting a course | `Admission.load("all_rounds" or "round1", missing="mean").p(code, semester)` in `solver/admission.py` |
| Is X allowed now? (T1) | `Catalog.can_take(code, completed, semester)` |
| Is X ruled out forever? | `Catalog.reachable(code, completed)` |
| Courses that need X | `courses[X]["unlocks"]` |
| All relations as a table | `edges.csv` |
| Traverse the graph (and/or kept) | `graph.json` (nodes `course` / `all` / `any` / `n_of`; edges `prereq` / `arg` / `excludes`) |
| Show a person a course | `data/processed/AY2026-2027/diagrams/<CODE>.html` |
| Why a rule was read a certain way | `courses[X]["assumptions"]`, `["warnings"]`, and `docs/DATA_SCHEMA.md#interpretation-decisions` |
| Raw NUSMods text | `courses[X]["prereq"]["source_text"]`, `["source"]["prerequisiteRule"]` |

## Logic tree semantics, in one breath

Nodes are `course` (completed), `and`, `or`, and `n_of` (≥ n args). `prereq.logic = null`
means no requirement, and `false` means never satisfiable. `preclusion.blocked_if` is the
condition under which the student may NOT take the course. `mutually_exclusive_with` is
the symmetric "never both" list to use in a planner. Stub records (`details: "stub"`) can
satisfy a tree when they appear in a transcript, but can't be planned.

## Things that look like bugs but are intended

- `CS2109HS`, `CS2040HS` and `CS2030HS` are `available: false`, because they are closed to BComp CS Hons.
- `MA1521` and similar have no prerequisite. The "A-level H2 Maths or MA1301" alternative is
  resolved by the student context, which holds H2 Maths.
- `CS2309` follows NUSMods' bracket reading, not normal precedence (see its `warnings`).
- 95 codes have `exists_in_ay: false`. They are old courses that are still named in preclusions.
- In the MDP a course-term with no CourseReg report rows is not certain: it gets `Admission.missing` (by default the
  mean of the estimates) and is listed in `model.no_data` of the answer. Don't default it back to 1 silently, and
  call the two estimators approximate scenarios, not bounds.
- The MDP's default `overrun` is 10, not 2, on purpose: lower values trade a large chance of a late finish for an
  earlier one (`docs/MDP_GUIDE.md` section 2).
