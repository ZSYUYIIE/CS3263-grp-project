# CS3263 Project: LLM vs Solver for NUS Degree Plans

We compare a frontier LLM answering NUS degree-planning requests directly against the
same LLM translating each request into a spec for a constraint solver (CP-SAT). We also
measure where each approach breaks, including when no valid plan exists.
Scope: BComp (CS) Hons, NUSMods AY2026/27 data.

| Role | Owns | Lives in |
|---|---|---|
| **M1** (leader) | Data pipeline: prerequisite and exclusion parsing, coordination | `m1_data/`, `data/` (**done, see below**) |
| M2 | CP-SAT model, own CSP solver | `solver/`, `experiments/` (**done, see below**) |
| M3 | Instance generators, pipelines A and B, independent checker and grader | `instances/`, `pipelines/`, `eval/` (**done, see below**) |

Key dates: data parsed and spot-checked by **Thu 29 Oct**, feasible T2 results by
**Wed 4 Nov** (fallback point), presentation in the **week of 9 Nov** (15 min + 5 min Q&A,
possibly a recorded video), report **Fri 13 Nov**.

**New here? Read [`docs/CODE_GUIDE.md`](docs/CODE_GUIDE.md) first.** It explains in about 15 minutes
how the code fits together and follows one request through it step by step.
**Presenting or writing the report?** [`docs/FORMULATION.md`](docs/FORMULATION.md) has the whole problem
formulation (data + solver) on one page.

## Data pipeline (M1)

The NUSMods API gives prerequisites as rule strings with programme, cohort and A-level
conditions mixed in. Preclusions come as free text plus a rule string. The pipeline turns
both into **course-only logic trees** for a BComp CS Hons student, writes them as JSON for
code and Markdown for people, and checks the result.

```
NUSMods API ──fetch──▶ data/raw/AY2026-2027/modules/*.json      (verbatim, minus timetables)
                │
              build      parse rule strings ─▶ resolve for student_context ─▶ simplify
                │        cross-check against NUSMods' own prereqTree
                ▼
data/processed/AY2026-2027/
    catalog.json        ◀── load this (one record per course)
    COURSES.md          ◀── read this (one block per course)
    diagrams/index.html ◀── look at this (one dependency diagram per course)
    graph.json  course_graph.graphml  edges.csv  PARSE_REPORT.md  rules_literal.json
```

### Use the data

The processed data is committed, so you don't need to run anything to use it.

```python
from m1_data.catalog import Catalog
cat = Catalog.load()

cat["CS3263"]["prereq"]["text"]
# '(CS2109S or CS2109HS) and (CS2040 or CS2040S or ...) and (MA2001 or MA1522 or ...) and (...)'

cat.can_take("CS3263", {"CS2040S", "MA1521", "MA1522", "ST2334"})
# (False, ['missing prerequisite: CS2109S or CS2109HS'])

cat.reachable("CS3263", {"CS3244", "CS2040S", "MA1521", "MA1522", "ST2334"})
# (False, 'CS3263: every option fails: CS2109S is ruled out by completed CS3244 |
#          CS2109HS unavailable (not open to PROGRAMS 0300CSHON)')
```

Without Python, open `data/processed/AY2026-2027/COURSES.md` and search for `### CS3263`.

### See it as a graph

![Why completing CS3244 makes CS3263 impossible](docs/diagrams/exclusion-trap.svg)

All diagrams come as `.svg` images, which GitHub and VS Code show directly, and as clickable `.html` pages:

| Diagram | Image (GitHub / IDE) | For the report or slides |
|---|---|---|
| Every course: what it needs, what needs it, what it excludes | [`diagrams/` gallery](data/processed/AY2026-2027/diagrams/README.md) | – |
| BComp CS core chain (year 1 → CS3263) | [svg](docs/diagrams/cs-core-chain.svg) | [png](docs/diagrams/cs-core-chain.png) |
| The CS3244 trap (shown above) | [svg](docs/diagrams/exclusion-trap.svg) | [png](docs/diagrams/exclusion-trap.png) |
| How the solver answers a spec | [svg](docs/diagrams/solver-flow.svg) | [png](docs/diagrams/solver-flow.png) |

**Clickable version (one-time setup):** repo **Settings → Pages → Deploy from a branch → `main` / root → Save**.
After a minute, the course explorer is at
`https://zsyuyiie.github.io/cs3263-project/data/processed/AY2026-2027/diagrams/index.html`.
Opening `index.html` from a local clone in a browser also works.

**For code:** `graph.json` is a node-link graph that keeps the and/or structure; `course_graph.graphml`
opens in yEd, Gephi or Cytoscape. The diagrams follow the diagram-design skill and pass its
`self_check.py` and `verify-geometry.py`.

**Scope:** BComp (CS) Hons, single major, AY2026/27. Requests about DDPs, second majors,
minors or other programmes are answered `OUT_OF_SCOPE` with a reason (`m1_data/scope.py`).

**Field reference and every interpretation decision: [`docs/DATA_SCHEMA.md`](docs/DATA_SCHEMA.md).**

### Rebuild the data

Python 3.10+ and the standard library only. Run from the repo root:

```bash
python -m m1_data fetch    # download from NUSMods (internet; about 1 min)
python -m m1_data build    # parse + write data/processed + run checks
python -m m1_data check    # checks only
python -m pytest -q        # tests
ruff check .               # lint (style and likely bugs)
```

Change which courses are fetched in `data/config/scope.json`, and the student that
conditions are resolved for in `data/config/student_context.json`. Hand fixes go in
`data/manual/overrides.json`, and every fix needs a reason.

### Status

| | |
|---|---|
| Courses with full data | 306 (all CS 1000–4999 + prerequisite closure + referenced) |
| Rule strings parsed | 918 / 918, 0 errors |
| Cross-check with NUSMods prereqTree | 198 match, 31 differ (all explained in `PARSE_REPORT.md`) |
| Invariant checks | pass |
| Hand spot-check | **to do:** `data/manual/SPOT_CHECK.md` (before generating instances) |

## Solver (M2)

### Interactive planner

To ask a question without creating a JSON file, run from the repo root:

```bash
python -m pip install -r requirements-dev.txt
cp .env.example .env    # first-time setup only; keep your existing .env if you have one
# Fill in LLM_BASE_URL, LLM_API_KEY and LLM_MODEL in .env.
python -m planner
```

The startup title shows the supported programme and academic year. Choose **1. Check whether I can take a course**
or **2. Plan my remaining courses** to go straight to the natural-language prompt. Describe your request in one line.
For example:

> I have completed no courses. I am in Y1S1. Plan CS1101S and CS1231S with at most 20 MC per semester.

The planner uses Pipeline B to translate your words, asks for any missing required information, and shows
its interpretation before solving. Check that summary, then press Enter to solve, choose `R` to replace
the request, or `B` to return to the menu. Replacing a request starts a fresh translation. Missing course
lists accept comma-separated codes or an explicit `none`, and a course to check or take that is not in the
catalogue is asked for again; semesters accept numbers or forms like `Y2S1`.
Enter `/back` or `/quit` at any prompt to leave a request or exit. On macOS and Linux, arrow keys move the
cursor and Up/Down recall earlier entries from the session. Q1 does not require a semester; when it is
omitted, the answer includes the solver's offering notes.

This covers BComp (CS) Hons, single major, no second major, minor, double or concurrent degree, under AY2026/27
rules. Q2 schedules the courses you request and their necessary prerequisites; it does not check all graduation
requirements. Each answer opens with a plain-language headline (for example "Yes, you can take CS3263" or
"Here is your plan"); a plan is listed semester by semester with each course's title and MC, marking the
prerequisites the solver added. Warnings, unsupported wishes, unmet preferences and refusal reasons are displayed
with the answer, in the solver's own words.

The command loads the project-root `.env`, preserving existing environment variables. It keeps requests in memory
and does not write experiment results. It uses the existing Pipeline B prompt and solver; the JSON CLI below still
works. See `python -m planner --help` for API timeout, retry and token limits (defaults: 60 seconds per attempt,
one retry, 24576 reply tokens). Translation requires your configured LLM service.

### JSON interface

The solver answers two kinds of request, each given as a JSON **spec**:

- **Q1** (`"query": "eligible"`): can the student take one course now, and if not, why not.
- **Q2** (`"query": "plan"`): plan the remaining semesters (1 to 8) so that every course in
  `must_take` is completed, and optimise the stated objective and preferences.

It needs Python 3.10+ and the `ortools` package (CP-SAT). Run from the repo root:

```bash
python -m pip install -r requirements-dev.txt    # pytest and ortools
python -m solver.run spec.json                   # answer one spec as JSON
python -m pytest -q                              # all tests
```

```python
import json
from m1_data.catalog import Catalog
from solver.run import run

answer = run(json.load(open("spec.json")), Catalog.load())
```

Solver reference (inputs, outputs, rules, optimality, variants): [`docs/SOLVER_GUIDE.md`](docs/SOLVER_GUIDE.md)
Pipeline B translation guide and prompt: [`docs/TRANSLATION_GUIDE.md`](docs/TRANSLATION_GUIDE.md)

### Spec fields

| Field | Used by | Meaning |
|---|---|---|
| `query` | both | `"eligible"` or `"plan"` |
| `current_sem` | both | first semester still to plan (odd semester = Sem 1, even = Sem 2); optional in Q1 |
| `completed` | both | courses already passed (`[]` if none) |
| `programme` | both | copied from the student; checked by `m1_data/scope.py` |
| `unsupported` | both | wishes the solver cannot model; echoed back as `not_applied` |
| `target` | Q1 | the course asked about |
| `must_take` | Q2 | courses the plan must contain (`[]` if none) |
| `mc_max`, `mc_min` | Q2 | MC limit per semester (default 20); minimum MC in every semester that has courses |
| `sem_caps` | Q2 | per-semester limit overriding `mc_max`; `0` blocks the semester |
| `atap_sems` | Q2 | semesters where ATAP (`CP3880`, 12 MC) may be planned; giving the field asks for ATAP |
| `rules` | Q2 | list of `{"type": before / in_sem / apart / same_sem, "strength": must / prefer, ...}` |
| `objective` | Q2 | `earliest_graduation`, `min_total_mc` or `none` |
| `early`, `late` | Q2 | preferences: earlier or later courses |

A field the student did not state is left out of the spec. `null`, `""` and `[]` are never used as placeholders;
`[]` is written only when the student says there are none. Field values of the wrong type or unknown fields give
`INVALID_SPEC`.

### Answer statuses

| Query | Statuses |
|---|---|
| Q1 | `ELIGIBLE`, `NOT_ELIGIBLE`, `MISSING_INFO`, `INVALID_SPEC`, `OUT_OF_SCOPE` |
| Q2 | `PLAN`, `NO_PLAN`, `MISSING_INFO`, `INVALID_SPEC`, `OUT_OF_SCOPE` |

The check order is `INVALID_SPEC`, then `OUT_OF_SCOPE`, then `MISSING_INFO`. `MISSING_INFO` lists the mandatory
fields that were not given (Q1: `completed`, `target`; Q2: `completed`, `current_sem`, `must_take`).
`NO_PLAN` carries a `reasons` list; when the rules conflict, `solver/explain.py` names a minimal set of
conflicting rules.

### Rules the model enforces

- Prerequisites in a strictly earlier semester, corequisites in the same or an earlier one.
- A course only in semesters of a term it is offered in; preclusions and mutual exclusions respected.
- MC per semester at most `mc_max` (or the `sem_caps` value); `mc_min` for semesters that have courses.
- A course the student did not list is added only when a planned course in a later semester needs it
  (reported as `added_prerequisites`).
- ATAP only in `atap_sems`, never the last semester used, and the other courses in that semester total at most
  min(8, the semester cap) MC; ATAP's own 12 MC is not counted against the cap.
- A `must` rule is hard; a `prefer` rule only counts towards the preference tie-break.

### Optimisation order (Q2)

1. Hard rules. No solution gives `NO_PLAN`.
2. The objective (`earliest_graduation` minimises the last semester, `min_total_mc` minimises total MC); fixed.
3. Fewest added courses; fixed.
4. Preferences: the number met among `prefer` rules, `early` and `late`; fixed.
5. Earliest last semester (only when the objective is not `earliest_graduation`; a presentation tie-break).

### Files

| File | Role |
|---|---|
| `solver/spec.py` | validates and cleans a spec |
| `solver/run.py` | entry point: `run(spec, catalog)`; shared `prepare()` front half |
| `solver/q1.py` | Q1 eligibility answer |
| `solver/model.py` | CP-SAT model (variables and hard rules) |
| `solver/q2.py` | Q2 staged optimisation and answer building |
| `solver/explain.py` | minimal conflicting rules for a `NO_PLAN` |
| `solver/backtrack.py` | own backtracking solver with four variants (below); independent of `model.py` and `q2.py` |
| `experiments/run_ablation.py` | ablation runner (CP-SAT against the four variants) |
| `solver/mdp.py`, `solver/admission.py` | MDP extension: bidding policy when a bid can fail; probabilities from the allocation reports |
| `experiments/run_mdp.py`, `extract_demand.py` | bidding experiment (plan, replan, policy); extraction of the report rows |
| `tests/test_solver.py`, `test_q2.py`, `test_explain.py`, `test_backtrack.py`, `test_ablation.py`, `test_mdp.py` | tests |

### Own CSP solver and ablation

`solver/backtrack.py` solves Q2 with its own backtracking search over partial assignments. The four variants are
cumulative:

- **plain**: static variable order; each value is checked only against the variables already assigned.
- **mrv**: plain plus MRV (minimum remaining values): next variable is the one with the fewest legal values
  given the current assignment, counted on demand.
- **fc**: MRV plus forward checking: after each assignment, values of unassigned variables that conflict with
  the assigned ones are deleted.
- **mac**: MRV plus forward checking plus domain propagation: the pruning is repeated, using the reduced domains,
  until no domain changes; an empty domain means backtrack.

Every complete plan gets a full validity check, so pruning only changes speed. The search is branch-and-bound over
the same stages as CP-SAT, so all four variants and CP-SAT reach the same optimum (status, last semester and number
of preferences met); several plans can tie, so the plans themselves may differ.

```python
from solver.backtrack import solve_with_stats
answer, stats = solve_with_stats(spec, variant="mac", time_limit=60)
# stats: nodes, backtracks, checks, seconds, timed_out
```

`nodes` counts assignment attempts over all stages and `backtracks` counts rejected assignments. A run that
reaches the time limit returns status `TIMED_OUT` and `timed_out=True` (CP-SAT has no such status).

Ablation over a JSON list of `{"id": ..., "spec": {...}}`. The instance files keep the spec under `gold_spec`, so
write such a list from them first (keep only the `"query": "plan"` rows and rename the key):

```bash
python -m experiments.run_ablation instances.json --limit 30 --out rows.csv --time-limit 60
```

It writes one CSV row per instance and engine (`id, engine, status, last_semester, preferences_met, seconds, nodes,
backtracks, checks, timed_out`) and prints, per engine, instances finished, median seconds, median nodes and
agreement with CP-SAT over the finished instances.

### Bidding under uncertainty (MDP extension)

The CP-SAT plan assumes the student gets every course in it. `solver/mdp.py` drops that assumption: a bid
succeeds with a probability estimated from two years of NUS CourseReg demand and allocation reports
(`data/demand/allocation.csv`, read by `solver/admission.py`), and the answer is a policy, not a fixed plan.
It is a finite-horizon MDP solved exactly by backward induction. CP-SAT chooses which courses are needed and
the MDP chooses when to bid for them; with every probability equal to 1 it gives the CP-SAT answer.

```bash
python -m solver.mdp examples/q2_bidding.json                     # policy for one Q2 spec
python -m solver.mdp examples/q2_bidding.json --estimator round1  # the lower probability scenario
python -m experiments.run_mdp --out rows.csv                      # plan vs replan vs policy on the instance set
```

It takes the same Q2 spec and is separate from `solver.run`, the pipelines, the instance files and the checker.
The policy minimises the expected finishing semester, with a late finish (after semester 8) counted as 10
more semesters. The probabilities are approximate scenarios, not forecasts, and a course-term with no report
rows gets a stated fallback (the mean of the others), not certainty.
On the 45 committed requests that have a plan, the mean probability of finishing by semester 8 is 0.947 for
the plan as written, 0.980 when replanning with CP-SAT every semester and 0.992 for the policy (`all_rounds`
scenario), and 0.690, 0.859 and 0.904 under the `round1` scenario.
Formulation, data, results and limits: [`docs/MDP_GUIDE.md`](docs/MDP_GUIDE.md).

## Instances, pipelines and evaluation (M3)

The experiment gives the same natural-language request to two pipelines and grades both answers against a gold
answer:

- **Pipeline A** (`pipelines/run_a.py`): the LLM answers the request itself. It is given the planning rules and the
  catalogue records of the courses involved, and no tool.
- **Pipeline B** (`pipelines/run_b.py`): the LLM only translates the request into a spec; the solver answers the spec.

Only these two pipelines exist in the repo.

### Instance sets

Every instance is built spec-first: the generator writes a gold spec, renders the request text from it, and stores
the solver's answer to that spec as the gold answer. An instance is kept only if the answer has the status its kind
was built to have.

| File | Instances | Made by | What it is for |
|---|---|---|---|
| `instances/instances.json` | 115 | `python -m instances.generate` | the mixed set: 30 Q1, 45 feasible Q2 (loose and tight), 24 infeasible Q2 in six kinds, 7 missing-info, 9 out-of-scope ([`SUMMARY.md`](instances/SUMMARY.md)) |
| `instances/q1_400.json` | 400 | `python -m instances.generate_q1` | Q1 in depth: three complexity levels, three wording styles and paired twins ([`Q1_SUMMARY.md`](instances/Q1_SUMMARY.md)) |
| `instances/q1_gating.json` | 80 | the same command | 40 pairs drawn from the 400, for a quick first run |

The files are generated with seed 3263 and are reproducible: the same command writes the same bytes. **Do not edit
them by hand, and regenerate them after any change to the spec format or the solver's rules**, because the gold
answers are the solver's answers at the time of generation. Regenerating can change the request texts, so results
obtained from an older file cannot be mixed with results from a newer one.

### Run and grade

Both pipelines call any OpenAI-compatible chat API. Copy `.env.example` to `.env` and set
`LLM_BASE_URL`, `LLM_API_KEY` and `LLM_MODEL` there. The runners load the project-root `.env`
automatically, with existing environment variables taking priority. `.env` is Git-ignored.
One fresh call per instance, temperature 0; a stopped run resumes.

```bash
python -m pipelines.run_a --mock gold      # dry run without an API: every answer is the gold answer
python -m pipelines.run_b --mock gold      # dry run: every spec is the gold spec, so only the solver is tested
python -m pipelines.run_a                  # real run -> results/A/<model>/<instance id>.json
python -m pipelines.run_b                  # real run -> results/B/<model>/<instance id>.json
python -m eval.grade results/A/<model> results/B/<model>     # graded.csv, SUMMARY.md per folder, and COMPARE.md
```

Add `--instances instances/q1_400.json` to the three commands to use another set. Details, including the prompt
ablation: [`pipelines/README.md`](pipelines/README.md).

### How an answer is graded

`eval/checker.py` implements the hard rules (1 to 11) of [`docs/SOLVER_GUIDE.md`](docs/SOLVER_GUIDE.md) section 4 straight
from `catalog.json`. It does not import the solver or `m1_data.catalog`, so a bug on one side shows up as a
disagreement. A plan of the wrong shape (not `{semester: [codes]}`) is an invalid
answer, not an error.

`eval/grade.py` puts each answer in one class. For a request that has a plan: **invalid** (breaks a hard rule), then
**objective gap**, **extra courses**, **preference gap**, otherwise **optimal**; answering `NO_PLAN` is an
**over-refusal**. For a request with no plan: **correct refusal**, or **invented plan**. The two headline metrics are
valid-answer accuracy (over every instance) and optimal-plan accuracy (over the requests that have a plan).

### Files

| File | Role |
|---|---|
| `instances/generate.py`, `generate_q1.py` | instance generators (spec first, then text, then gold answer) |
| `pipelines/prompt_a.py`, `run_a.py` | pipeline A prompt (rules + selected course records) and runner |
| `pipelines/prompt_b.txt`, `run_b.py` | pipeline B translation prompt and runner |
| `pipelines/ablation/` | prompt ablation 1 for both pipelines (semester numbering not explained) |
| `eval/checker.py` | independent plan checker |
| `eval/grade.py` | classes, metrics, result tables and tests of significance |
| `tests/test_instances.py`, `test_checker.py` | the committed mixed set matches its kinds; every gold plan is valid and grades as optimal |

## Repository layout

```
m1_data/            data pipeline package (fetch, rules, resolve, build, check, catalog,
                    graph, diagrams, scope)
solver/             spec, run, q1, q2, model, explain, backtrack (M2); mdp, admission (MDP extension)
experiments/        run_ablation.py (M2); run_mdp.py, extract_demand.py (MDP extension)
instances/          instance generators and the generated instance sets (M3)
pipelines/          pipeline A and B prompts and runners, prompt ablation (M3)
eval/               independent checker and grader (M3)
results/            written by the pipeline runners: results/<pipeline>/<model>/
examples/           example spec JSON files
data/config/        scope.json, student_context.json
data/raw/           NUSMods responses, kept so results are reproducible (data drifts year to year)
data/processed/     generated outputs (do not edit)
data/manual/        overrides.json, SPOT_CHECK.md
data/demand/        allocation.csv: CourseReg demand and allocation report rows (generated; see its README)
docs/               CODE_GUIDE.md, FORMULATION.md, DATA_SCHEMA.md, SOLVER_GUIDE.md, TRANSLATION_GUIDE.md, MDP_GUIDE.md,
                    diagrams/ (hand-laid overviews)
tests/              pytest
AGENTS.md           orientation for AI coding agents working in this repo
```
