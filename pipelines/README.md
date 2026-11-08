# Pipeline A: the LLM answers directly

1. Set the model (any OpenAI-compatible API; the key stays in your shell, never in the repo):

   ```bash
   export LLM_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1   # Qwen; GLM: https://open.bigmodel.cn/api/paas/v4
   export LLM_API_KEY=...
   export LLM_MODEL=qwen3-max                                                   # or glm-4.6
   ```
   (PowerShell: `$env:LLM_API_KEY="..."`.)

2. Try 5 instances first, then run everything (it resumes if stopped):

   ```bash
   python -m pipelines.run_a --limit 5
   python -m pipelines.run_a
   ```

3. Grade:

   ```bash
   python -m eval.grade results/A/qwen3-max
   ```
   This writes `graded.csv` (one row per instance, with the broken rules) and `SUMMARY.md` (tables for the slides).

`python -m pipelines.run_a --mock gold` runs the whole harness without an API (every answer is the gold answer,
so the grade must come out 100%).

What the model sees is built by `pipelines/prompt_a.py`: fixed instructions (the same rules and optimisation
order as the solver), the course records chosen by the rule in that file's docstring, and the request text.
It never sees the gold spec or the gold answer. One fresh call per instance, temperature 0.

Pipeline B produces solver specs instead; grade its final answers with the same `eval.grade` once its results
are saved in the same format (`results/B/<model>/<id>.json` with an `answer` field).
