# Pipelines A and B

Two pipelines answer the same instances, and `eval.grade` grades both:

- A (`run_a.py`): the LLM answers the request itself, given the planning rules and the course records.
- B (`run_b.py`): the LLM translates the request into a spec, and the solver answers the spec.

`python -m planner` is the eligibility checker and planner, an interactive tool built on pipeline B (configure `.env` as below). It uses the same
translation prompt and API helpers, with its own timeout and retry options, and writes nothing to `results/`. Its
follow-up questions and revisions are outside the experiment's one-call-per-instance protocol. Usage is in
[`docs/CHECKER_PLANNER_GUIDE.md`](../docs/CHECKER_PLANNER_GUIDE.md).

## Pipeline A: the LLM answers directly

1. Install dependencies and create your local configuration from the project root:

   ```bash
   python -m pip install -r requirements-dev.txt
   cp .env.example .env
   ```

   Edit `.env` to set `LLM_BASE_URL`, `LLM_API_KEY` and `LLM_MODEL` for your
   OpenAI-compatible provider. All four runners (A, B and both ablations) load this
   project-root file on startup, so no `source` command is needed. Restart the command
   after editing it. `.env` is Git-ignored and must not be committed.

   Variables already set in the environment take priority over `.env`, so shell exports
   and CI configuration still work. Without a `.env`, the runners read the environment
   only. Mock runs need no API credentials.

2. Try 5 instances first, then run everything (it resumes if stopped):

   ```bash
   python -m pipelines.run_a --limit 5
   python -m pipelines.run_a
   ```

3. Grade:

   ```bash
   python -m eval.grade results/A/qwen3-max
   ```
   This writes `graded.csv` (one row per instance, with the broken rules) and `SUMMARY.md` (result tables).

`python -m pipelines.run_a --mock gold` runs the whole harness without an API (every answer is the gold answer,
so the grade must come out 100%).

What the model sees is built by `pipelines/prompt_a.py`: fixed instructions (the same rules and optimisation
order as the solver), the course records chosen by the rule in that file's docstring, and the request text.
It never sees the gold spec or the gold answer. One fresh call per instance, temperature 0.

## Pipeline B: the LLM writes a spec, the solver answers

Same environment variables, options and resume behaviour as pipeline A:

```bash
python -m pipelines.run_b --limit 5
python -m pipelines.run_b
python -m eval.grade results/B/qwen3-max
```

The system prompt is `pipelines/prompt_b.txt` (the translation rules of `docs/TRANSLATION_GUIDE.md`). The model sees
that prompt and the request text only: no course records, because the solver has the course data. Its reply is
parsed as one JSON spec, checked with `solver.spec.validate` and answered with `solver.run`. A reply that is not
usable JSON is recorded as `INVALID_SPEC`. Each `results/B/<model>/<id>.json` holds the raw reply, the parsed `spec`,
its `schema_errors`, the solver's `answer` and `solver_seconds`.

`python -m pipelines.run_b --mock gold` uses the gold spec as the model's reply, so it tests the solver and the
grader only. The grade must come out 100%.

## Comparing the two

```bash
python -m eval.grade results/A/qwen3-max results/B/qwen3-max
```

writes `SUMMARY.md` and `graded.csv` in each folder and one `COMPARE.md` with a column per folder. For pipeline B the
summary also compares each spec with the gold spec, field by field.

## Other instance sets and options

- `--instances instances/q1_400.json` (or `q1_gating.json`) on `run_a`, `run_b` and `eval.grade` uses another set.
  Pass the same file to the runner and to the grader.
- `--only q2_infeasible` runs the instances whose kind starts with that text, and `--limit N` the first N.
- `--tag NAME` writes to `results/A_NAME/<model>` (or `B_NAME`), for example for a timing run.
- `--workers N` (default 4) and `--max-tokens N` (default 24576).

## Prompt ablation 1

`pipelines/ablation/` holds a second version of both prompts in which the semester numbering (Y1S1 = 1, ...,
odd = Semester 1) is not explained, with its own runners:

```bash
python -m pipelines.ablation.run_a_ablation1 --instances instances/q1_400.json
python -m pipelines.ablation.run_b_ablation1 --instances instances/q1_400.json
python -m eval.grade results/q1_ablation1/A/<model> --instances instances/q1_400.json
```

Results go to `results/q1_ablation1/A/<model>` and `results/q1_ablation1/B/<model>`. The ablation prompts also differ
from the main prompts in a few other lines (ATAP, minimum MC, the light-semester and even-workload wishes), so keep
this ablation to Q1 instances, which those lines do not affect.
