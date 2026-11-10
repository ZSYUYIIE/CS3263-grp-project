"""Run pipeline A with the Q1 ablation 1 prompt (pipelines/ablation/prompt_a_ablation1.py).

Same call, reply parsing and resume behaviour as run_a.py (the functions are imported from it), same options except
--tag and --set. Results go to results/q1_ablation1/A/<model>. Grade with
    python -m eval.grade results/q1_ablation1/A/<model> --instances instances/q1_400.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pipelines.ablation.prompt_a_ablation1 import build_messages
from pipelines.run_a import DEFAULT_MAX_TOKENS, ROOT, call_api, parse_reply_how


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instances", default=str(ROOT / "instances/instances.json"))
    ap.add_argument("--only", help="run only instances whose kind starts with this")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    ap.add_argument("--mock", choices=["gold"], help="answer without an API, for testing the harness")
    a = ap.parse_args()

    model = "mock-gold" if a.mock else os.environ.get("LLM_MODEL")
    base, key = os.environ.get("LLM_BASE_URL"), os.environ.get("LLM_API_KEY")
    if not a.mock and not (model and base and key):
        sys.exit("set LLM_BASE_URL, LLM_API_KEY and LLM_MODEL (or use --mock gold)")
    rows = json.loads(Path(a.instances).read_text())
    if a.only:
        rows = [r for r in rows if r["kind"].startswith(a.only)]
    rows = rows[: a.limit] if a.limit else rows
    out_dir = ROOT / "results" / "q1_ablation1" / "A" / re.sub(r"[^\w.-]", "_", model)
    out_dir.mkdir(parents=True, exist_ok=True)
    todo = [r for r in rows if not (out_dir / f"{r['id']}.json").exists()]
    print(f"{len(rows) - len(todo)} done already, {len(todo)} to run -> {out_dir}")

    def one(r):
        messages = build_messages(r)
        t = time.time()
        if a.mock:
            text, usage = json.dumps(r["gold_answer"]), {}
        else:
            try:
                text, usage = call_api(messages, model, base, key, a.max_tokens)
            except RuntimeError as e:      # not saved, so the next run retries this instance
                return r["id"], "API_ERROR", str(e)[:200]
        parsed, how, err = parse_reply_how(text)
        rec = {"id": r["id"], "pipeline": "A", "model": model, "seconds": round(time.time() - t, 2),
               "usage": usage, "raw": text, "answer": parsed, "fenced": how not in (None, "clean"),
               "repair": how, "parse_error": err, "max_tokens": a.max_tokens, "workers": 1 if a.mock else a.workers, "ablation": 1}
        (out_dir / f"{r['id']}.json").write_text(json.dumps(rec, indent=1))
        return r["id"], (parsed["status"] if parsed else "UNPARSEABLE") + (f" [{how}]" if how not in (None, "clean") else ""), \
            ("hit max_tokens" if usage.get("finish_reason") == "length" else "")

    ex = ThreadPoolExecutor(max_workers=1 if a.mock else a.workers)
    stats = {"api_error": 0, "unparseable": 0, "truncated": 0, "repaired": 0}
    try:
        for i, (iid, status, note) in enumerate(ex.map(one, todo), 1):
            stats["api_error"] += status == "API_ERROR"
            stats["unparseable"] += status.startswith("UNPARSEABLE")
            stats["truncated"] += note == "hit max_tokens"
            stats["repaired"] += "[" in status
            print(f"[{i}/{len(todo)}] {iid}: {status}" + (f"  ({note})" if note else ""), flush=True)
    except KeyboardInterrupt:
        print("stopped; finished instances are saved, run again to continue", flush=True)
        os._exit(1)
    print(f"done: {stats}; instances with API_ERROR were not saved, run the same command again to retry them")

if __name__ == "__main__":
    main()
