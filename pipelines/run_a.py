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


DEFAULT_MAX_TOKENS = 24576   # ceiling, not a target: 2 x the largest pilot reply (11,820 tokens), rounded up to a multiple of 1,024
ALLOWED_STATUS = {"ELIGIBLE", "NOT_ELIGIBLE", "PLAN", "NO_PLAN", "MISSING_INFO", "OUT_OF_SCOPE"}
_DEC = json.JSONDecoder(strict=False)


def call_api(messages, model, base_url, key, max_tokens, timeout=600, retries=4):
    body = json.dumps({"model": model, "messages": messages, "temperature": 0, "max_tokens": max_tokens}).encode()
    req = urllib.request.Request(base_url.rstrip("/") + "/chat/completions", data=body,
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
    for attempt in range(retries + 1):
        try:
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read())
            choice = data["choices"][0]
            usage = dict(data.get("usage") or {})
            usage["finish_reason"] = choice.get("finish_reason")
            usage["request_seconds"] = round(time.time() - t0, 2)
            usage["attempts"] = attempt + 1
            return choice["message"].get("content") or "", usage
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ConnectionError, KeyError, json.JSONDecodeError) as e:
            code = getattr(e, "code", None)
            if attempt == retries or code in (400, 401, 403, 404):
                detail = e.read().decode()[:500] if hasattr(e, "read") else str(e)
                raise RuntimeError(f"API error {code}: {detail}") from e
            time.sleep(2 ** (attempt + 1))


def _objects(s: str):
    """Every complete JSON object in the text, in order."""
    found, i = [], 0
    while True:
        j = s.find("{", i)
        if j < 0:
            return found
        try:
            obj, end = _DEC.raw_decode(s, j)
        except json.JSONDecodeError:
            i = j + 1
            continue
        found.append(obj)
        i = end


def _unwrap(obj, key):
    """{"eligibility": {"status": ...}} -> the inner object."""
    if isinstance(obj, dict) and key not in obj:
        inner = [v for v in obj.values() if isinstance(v, dict) and key in v]
        if len(inner) == 1:
            return inner[0]
    return obj


def _usable(obj, key):
    return isinstance(obj, dict) and key in obj and (key != "status" or obj["status"] in ALLOWED_STATUS)


def parse_reply_how(text: str, key: str = "status"):
    """Return (object, how, error). `how` says what had to be repaired, so format slips are counted, not hidden:
    clean | control_chars | fence | unwrapped | extra_text | last_of_several | cut_reasons.
    key is "status" for pipeline A answers and "query" for pipeline B specs."""
    s = (text or "").strip()
    if not s:
        return None, None, "empty reply"
    try:
        obj = json.loads(s)
        if _usable(obj, key):
            return obj, "clean", None
        if _usable(_unwrap(obj, key), key):
            return _unwrap(obj, key), "unwrapped", None
    except json.JSONDecodeError:
        pass
    unfenced = re.sub(r"^```(?:json)?\s*|\s*```$", "", s)
    for body, how in ((s, "control_chars"), (unfenced, "fence")):
        try:
            obj = _unwrap(_DEC.decode(body), key)
            if _usable(obj, key):
                return obj, how, None
        except json.JSONDecodeError:
            pass
    objs = [o for o in (_unwrap(o, key) for o in _objects(s) if isinstance(o, dict)) if _usable(o, key)]
    if objs:
        return objs[-1], "extra_text" if len(objs) == 1 else "last_of_several", None
    if key == "status":    # the reply broke inside "reasons"; status and plan come before it and are complete
        m = re.search(r'"status"\s*:\s*"([A-Z_]+)"', s)
        if m and m.group(1) in ALLOWED_STATUS:
            ans = {"status": m.group(1)}
            if ans["status"] != "PLAN":
                return ans, "cut_reasons", None
            p = re.search(r'"plan"\s*:\s*', s)
            if p and s[p.end():p.end() + 1] == "{":
                try:
                    plan, _ = _DEC.raw_decode(s, p.end())
                    ans["plan"] = plan
                    return ans, "cut_reasons", None
                except json.JSONDecodeError:
                    pass
    return None, None, "no usable JSON object in reply"


def parse_reply(text: str, key: str = "status"):
    """(object, repaired, error): repaired is True when the reply was not a clean single JSON object."""
    obj, how, err = parse_reply_how(text, key)
    return obj, how not in (None, "clean"), err


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instances", default=str(ROOT / "instances/instances.json"))
    ap.add_argument("--only", help="run only instances whose kind starts with this")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--tag", help="write to results/A_<tag>/<model> instead of results/A/<model> (for example a timing run)")
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
    out_dir = ROOT / "results" / ("A_" + a.tag if a.tag else "A") / re.sub(r"[^\w.-]", "_", model)
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
               "repair": how, "parse_error": err, "max_tokens": a.max_tokens, "workers": 1 if a.mock else a.workers}
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
