"""Run pipeline B with the Q1 ablation 1 prompt (pipelines/ablation/prompt_b_ablation1.txt).

Same call, spec parsing, solver and resume behaviour as run_b.py (the functions are imported from it and from
run_a.py), same options except --tag and --set. Results go to results/q1_ablation1/B/<model>. Grade with
    python -m eval.grade results/q1_ablation1/B/<model> --instances instances/q1_400.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from m1_data.catalog import Catalog
from pipelines.run_a import DEFAULT_MAX_TOKENS, ROOT, call_api, parse_reply_how
from solver.run import run
from solver.spec import validate

PROMPT = (ROOT / "pipelines/ablation/prompt_b_ablation1.txt").read_text(encoding="utf-8")


def build_messages(inst):
    return [{"role": "system", "content": PROMPT}, {"role": "user", "content": f"Request: {inst['request']}\nJSON:"}]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instances", default=str(ROOT / "instances/instances.json"))
    ap.add_argument("--only", help="run only instances whose kind starts with this")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    ap.add_argument("--mock", choices=["gold"], help="use the gold spec instead of a model, to test the solver and the grader")
    a = ap.parse_args()

    model = "mock-gold" if a.mock else os.environ.get("LLM_MODEL")
    base, key = os.environ.get("LLM_BASE_URL"), os.environ.get("LLM_API_KEY")
    if not a.mock and not (model and base and key):
        sys.exit("set LLM_BASE_URL, LLM_API_KEY and LLM_MODEL (or use --mock gold)")
    rows = json.loads(Path(a.instances).read_text())
    if a.only:
        rows = [r for r in rows if r["kind"].startswith(a.only)]
    rows = rows[: a.limit] if a.limit else rows
    out_dir = ROOT / "results" / "q1_ablation1" / "B" / re.sub(r"[^\w.-]", "_", model)
    out_dir.mkdir(parents=True, exist_ok=True)
    todo = [r for r in rows if not (out_dir / f"{r['id']}.json").exists()]
    print(f"{len(rows) - len(todo)} done already, {len(todo)} to run -> {out_dir}")

    catalog = Catalog.load()
    lock = threading.Lock()

    def one(r):
        t = time.time()
        if a.mock:
            text, usage = json.dumps(r["gold_spec"]), {}
        else:
            try:
                text, usage = call_api(build_messages(r), model, base, key, a.max_tokens)
            except RuntimeError as e:      # not saved, so the next run retries this instance
                return r["id"], "API_ERROR", [str(e)[:200]]
        spec, how, err = parse_reply_how(text, "query")
        errors, solver_seconds = [], 0.0
        if err:
            answer = {"status": "INVALID_SPEC", "errors": [err]}
        else:
            with lock:
                t_solver = time.time()
                errors = validate(spec, catalog)[0]
                answer = run(spec, catalog)
                solver_seconds = round(time.time() - t_solver, 3)
        rec = {"id": r["id"], "pipeline": "B", "model": model, "seconds": round(time.time() - t, 2),
               "solver_seconds": solver_seconds, "max_tokens": a.max_tokens, "workers": 1 if a.mock else a.workers,
               "usage": usage, "ablation": 1, "raw": text, "spec": spec, "fenced": how not in (None, "clean"), "repair": how, "parse_error": err,
               "schema_errors": errors, "answer": answer}
        (out_dir / f"{r['id']}.json").write_text(json.dumps(rec, indent=1))
        return r["id"], answer.get("status", "NO_STATUS"), errors

    ex = ThreadPoolExecutor(max_workers=1 if a.mock else a.workers)
    api_errors = 0
    try:
        for i, (iid, status, errors) in enumerate(ex.map(one, todo), 1):
            api_errors += status == "API_ERROR"
            print(f"[{i}/{len(todo)}] {iid}: {status}" + (f"  schema: {'; '.join(errors)}" if errors else ""), flush=True)
    except KeyboardInterrupt:
        print("stopped; finished instances are saved, run again to continue", flush=True)
        os._exit(1)
    print(f"done: {api_errors} API errors (not saved); run the same command again to retry them")

if __name__ == "__main__":
    main()
