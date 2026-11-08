"""Run pipeline A over the instance set with any OpenAI-compatible chat API (Qwen, GLM, SoC-hosted models, ...).

Settings come from environment variables, so no key is ever written to the repo:
    LLM_BASE_URL   e.g. https://dashscope-intl.aliyuncs.com/compatible-mode/v1   (Qwen)
                        https://open.bigmodel.cn/api/paas/v4                       (GLM)
    LLM_API_KEY    your key
    LLM_MODEL      e.g. qwen3-max, glm-4.6

    python -m pipelines.run_a                      # all instances, skips ones already answered
    python -m pipelines.run_a --only q2_infeasible --limit 5
    python -m pipelines.run_a --mock gold          # no API: answers with the gold answer (tests the harness)

Each instance gets one fresh call (no shared history), temperature 0. The raw reply, the parsed JSON and the
token usage are saved to results/A/<model>/<instance id>.json. Re-running continues where it stopped.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pipelines.prompt_a import build_messages

ROOT = Path(__file__).resolve().parent.parent


def call_api(messages, model, base_url, key, max_tokens, timeout=300, retries=4):
    body = json.dumps({"model": model, "messages": messages, "temperature": 0, "max_tokens": max_tokens}).encode()
    req = urllib.request.Request(base_url.rstrip("/") + "/chat/completions", data=body,
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"], data.get("usage", {})
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            code = getattr(e, "code", None)
            if attempt == retries or code in (400, 401, 403, 404):
                detail = e.read().decode()[:500] if hasattr(e, "read") else str(e)
                raise RuntimeError(f"API error {code}: {detail}") from e
            time.sleep(2 ** (attempt + 1))


def parse_reply(text: str):
    """The JSON object in the reply. Fences are stripped, and counted as a format slip by the grader."""
    s = text.strip()
    fenced = s.startswith("```")
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s)
    try:
        return json.loads(s), fenced, None
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", s, re.S)
        if m:
            try:
                return json.loads(m.group(0)), True, None
            except json.JSONDecodeError as e:
                return None, fenced, str(e)
        return None, fenced, "no JSON object in reply"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instances", default=str(ROOT / "instances/instances.json"))
    ap.add_argument("--only", help="run only instances whose kind starts with this")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--max-tokens", type=int, default=4000)
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
    out_dir = ROOT / "results" / "A" / re.sub(r"[^\w.-]", "_", model)
    out_dir.mkdir(parents=True, exist_ok=True)
    todo = [r for r in rows if not (out_dir / f"{r['id']}.json").exists()]
    print(f"{len(rows) - len(todo)} done already, {len(todo)} to run -> {out_dir}")

    def one(r):
        messages = build_messages(r)
        t = time.time()
        if a.mock:
            text, usage = json.dumps(r["gold_answer"]), {}
        else:
            text, usage = call_api(messages, model, base, key, a.max_tokens)
        parsed, fenced, err = parse_reply(text)
        rec = {"id": r["id"], "pipeline": "A", "model": model, "seconds": round(time.time() - t, 2),
               "usage": usage, "raw": text, "answer": parsed, "fenced": fenced, "parse_error": err}
        (out_dir / f"{r['id']}.json").write_text(json.dumps(rec, indent=1))
        return r["id"], parsed["status"] if parsed else "UNPARSEABLE"

    with ThreadPoolExecutor(max_workers=1 if a.mock else a.workers) as ex:
        for i, (iid, status) in enumerate(ex.map(one, todo), 1):
            print(f"[{i}/{len(todo)}] {iid}: {status}", flush=True)


if __name__ == "__main__":
    main()
