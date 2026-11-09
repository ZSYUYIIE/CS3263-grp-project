"""Run pipeline A over the instance set with any OpenAI-compatible chat API (Qwen, GLM, SoC-hosted models, ...).

NUS SoCLaaS: set SOCLAAS_API_KEY and use --provider soclaas. The runner discovers /models
before sending requests and selects an exact chat model ID (override with --model).
Other compatible APIs use --provider compatible and these environment variables:
    LLM_BASE_URL   e.g. https://dashscope-intl.aliyuncs.com/compatible-mode/v1   (Qwen)
                        https://open.bigmodel.cn/api/paas/v4                       (GLM)
    LLM_API_KEY    your key
    LLM_MODEL      e.g. qwen3-max, glm-4.6

    python -m pipelines.run_a                      # all instances, skips ones already answered
    python -m pipelines.run_a --only q2_infeasible --limit 5
    python -m pipelines.run_a --mock gold          # no API: answers with the gold answer (tests the harness)

Each attempt uses a fresh conversation, temperature 0. SoCLaaS defaults to 16384 completion tokens with one
exhaustion-only retry at 32768. Replies, finish reasons and usage from every attempt are retained under
results/A/<model>/<prompt version and budgets>/. A manifest guards resumption against mixed conditions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from pipelines.output import validate_answer
from pipelines.prompt_a import INSTRUCTIONS, PROMPT_VERSION, build_messages

ROOT = Path(__file__).resolve().parent.parent
SOCLAAS_BASE_URL = "https://soclaas-api.comp.nus.edu.sg/v1"
PREFERRED_MODELS = ("x-test-2", "qwen3.8:27b", "qwen3.6:35b", "gemma4:26b", "nemotron3.5:30b")


class APIResponseError(RuntimeError):
    """A completion without final text, retaining usage for experiment accounting."""

    def __init__(self, message, usage, finish_reason=None):
        super().__init__(message)
        self.usage = usage
        self.finish_reason = finish_reason


def request_json(path, base_url, key, payload=None, timeout=300, retries=4):
    """GET or POST JSON, retrying rate limits and temporary failures with bounded backoff."""
    body = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(base_url.rstrip("/") + path, data=body,
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read())
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            code = getattr(e, "code", None)
            if attempt == retries or (code is not None and code != 429 and not 500 <= code < 600):
                detail = e.read().decode(errors="replace") if hasattr(e, "read") else str(e)
                detail = detail.replace(key, "[REDACTED]")[:500]
                raise RuntimeError(f"API error {code}: {detail}") from None
            time.sleep(min(2 ** (attempt + 1), 16))


def discover_model(base_url, key, requested=None):
    """Choose only a chat-capable exact ID returned by SoCLaaS, never an alias."""
    models = request_json("/models", base_url, key)["data"]
    chat = {m["id"]: m for m in models if "chat" in m.get("soclaas", {}).get("capabilities", [])}
    if requested:
        if requested not in chat:
            raise ValueError(f"{requested!r} is not a chat model returned by GET /models")
        model = chat[requested].get("soclaas", {}).get("alias_of", requested)
        if model not in chat:
            raise ValueError(f"GET /models did not return alias target {model!r}")
    else:
        model = next((m for m in PREFERRED_MODELS if m in chat), None)
        if model is None:
            raise ValueError("no preferred chat model found; select an exact GET /models ID with --model")
    return model, models


def completion(messages, model, base_url, key, max_tokens, timeout=600, retries=4):
    payload = {"model": model, "messages": messages, "stream": False,
               "temperature": 0, "max_tokens": max_tokens}
    data = request_json("/chat/completions", base_url, key, payload, timeout, retries)
    try:
        choice = data["choices"][0]
        content = choice["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError("API response has no choices[0].message.content") from None
    return {"raw": content if isinstance(content, str) else None, "usage": data.get("usage") or {},
            "finish_reason": choice.get("finish_reason")}


def call_api(messages, model, base_url, key, max_tokens, timeout=300, retries=4):
    """Compatibility interface for the original model-selection experiment."""
    result = completion(messages, model, base_url, key, max_tokens, timeout, retries)
    if result["raw"] is None:
        raise APIResponseError("API returned non-text content; check the model and token budget",
                               result["usage"], result["finish_reason"])
    return result["raw"], result["usage"]


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


def sum_usage(items):
    """Include usage of exhausted attempts, including nested reasoning-token counters."""
    total = {}
    for usage in items:
        for name, value in usage.items():
            if type(value) is int:
                total[name] = total.get(name, 0) + value
            elif isinstance(value, dict):
                total[name] = sum_usage([total.get(name, {}), value])
    return total


def answer_record(instance, model, base, key, max_tokens, mock=False, retry_max_tokens=0, timeout=600):
    """Retry only output exhaustion, once, with identical messages and no checker feedback."""
    messages = build_messages(instance)
    started = time.monotonic()
    budgets = [max_tokens] + ([retry_max_tokens] if retry_max_tokens > max_tokens and not mock else [])
    attempts = []
    for budget in budgets:
        attempt_started = time.monotonic()
        try:
            result = ({"raw": json.dumps(instance["gold_answer"]), "usage": {}, "finish_reason": "mock"}
                      if mock else completion(messages, model, base, key, budget, timeout))
            text = result["raw"]
            parsed, fenced, error = parse_reply(text) if text else (None, False, "no final text")
            exhausted = result["finish_reason"] in ("length", "max_tokens") or (
                result["usage"].get("completion_tokens", 0) >= budget and (not text or error is not None))
            attempt = dict(result, max_tokens=budget, answer=parsed, fenced=fenced, parse_error=error,
                           budget_exhausted=exhausted)
            if not text:
                attempt["api_error"] = "API returned non-text content or no final text"
        except RuntimeError as exc:
            attempt = {"raw": None, "answer": None, "usage": getattr(exc, "usage", {}),
                       "finish_reason": getattr(exc, "finish_reason", None), "max_tokens": budget,
                       "fenced": False, "parse_error": None, "budget_exhausted": False, "api_error": str(exc)}
        attempt["seconds"] = round(time.monotonic() - attempt_started, 2)
        attempts.append(attempt)
        if not attempt["budget_exhausted"]:
            break
    final = attempts[-1]
    schema_errors = validate_answer(final["answer"])
    if final["fenced"]:
        schema_errors.append("JSON was surrounded by fences or extra text")
    rec = {"id": instance["id"], "pipeline": "A", "model": model,
           "prompt_version": PROMPT_VERSION,
           "messages_sha256": hashlib.sha256(json.dumps(messages, sort_keys=True).encode()).hexdigest(),
           "seconds": round(time.monotonic() - started, 2),
           "raw": final["raw"], "answer": final["answer"], "fenced": final["fenced"],
           "parse_error": final["parse_error"], "finish_reason": final["finish_reason"],
           "budget_exhausted": final["budget_exhausted"], "budget_retried": len(attempts) > 1,
           "schema_errors": schema_errors, "format_valid": not schema_errors, "attempts": attempts}
    rec["usage"] = sum_usage(a["usage"] for a in attempts)
    if final.get("api_error"):
        rec["api_error"] = final["api_error"]
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instances", default=str(ROOT / "instances/instances.json"))
    ap.add_argument("--only", help="run only instances whose kind starts with this")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--max-tokens", type=int, help="initial completion cap (SoCLaaS: 16384; compatible: 4000)")
    ap.add_argument("--retry-max-tokens", type=int, help="one exhaustion-only retry cap (SoCLaaS: 32768; 0 disables)")
    ap.add_argument("--timeout", type=int, default=600, help="per HTTP request timeout in seconds")
    ap.add_argument("--out", type=Path, help="exact results directory; defaults to a new v2 condition directory")
    ap.add_argument("--ids", nargs="+", help="selected instance IDs for a pilot; later resume without this flag")
    ap.add_argument("--provider", choices=["soclaas", "compatible"],
                    default="soclaas" if os.environ.get("SOCLAAS_API_KEY") else "compatible")
    ap.add_argument("--model", help="exact model ID; SoCLaaS validates it against GET /models")
    ap.add_argument("--mock", choices=["gold"], help="answer without an API, for testing the harness")
    a = ap.parse_args()
    if a.max_tokens is None:
        a.max_tokens = 16384 if a.provider == "soclaas" else 4000
    if a.retry_max_tokens is None:
        a.retry_max_tokens = 32768 if a.provider == "soclaas" else 0
    if a.max_tokens <= 0 or a.timeout <= 0 or a.workers <= 0 or a.retry_max_tokens < 0:
        ap.error("token caps, timeout and workers must be positive (retry cap may be zero)")
    if 0 < a.retry_max_tokens <= a.max_tokens:
        ap.error("retry cap must exceed the initial cap, or be zero to disable")

    models = None
    if a.mock:
        model, base, key = "mock-gold", None, None
    elif a.provider == "soclaas":
        base, key = SOCLAAS_BASE_URL, os.environ.get("SOCLAAS_API_KEY")
        if not key:
            sys.exit("set SOCLAAS_API_KEY (or use --mock gold)")
        model, models = discover_model(base, key, a.model or os.environ.get("SOCLAAS_MODEL"))
    else:
        model = a.model or os.environ.get("LLM_MODEL")
        base, key = os.environ.get("LLM_BASE_URL"), os.environ.get("LLM_API_KEY")
        if not (model and base and key):
            sys.exit("set LLM_BASE_URL, LLM_API_KEY and LLM_MODEL (or use --mock gold)")
    rows = json.loads(Path(a.instances).read_text())
    if a.only:
        rows = [r for r in rows if r["kind"].startswith(a.only)]
    if a.ids:
        unknown = set(a.ids) - {r["id"] for r in rows}
        if unknown:
            ap.error("unknown instance IDs: " + ", ".join(sorted(unknown)))
        rows = [r for r in rows if r["id"] in a.ids]
    rows = rows[: a.limit] if a.limit else rows
    condition = f"{PROMPT_VERSION}_{a.max_tokens}_{a.retry_max_tokens}"
    out_dir = a.out or ROOT / "results" / "A" / re.sub(r"[^\w.-]", "_", model) / condition
    catalog_hash = hashlib.sha256((ROOT / "data/processed/AY2026-2027/catalog.json").read_bytes()).hexdigest()
    config = {"prompt_version": PROMPT_VERSION, "model": model, "base_url": base,
              "max_tokens": a.max_tokens, "retry_max_tokens": a.retry_max_tokens,
              "timeout": a.timeout, "workers": a.workers, "temperature": 0, "stream": False,
              "prompt_sha256": hashlib.sha256(INSTRUCTIONS.encode()).hexdigest(),
              "catalog_sha256": catalog_hash,
              "instances_sha256": hashlib.sha256(Path(a.instances).read_bytes()).hexdigest(),
              "record_selection": "benchmark metadata selects factual records; no gold answer in prompts"}
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = out_dir / "run_manifest.json"
    if manifest.exists():
        if json.loads(manifest.read_text())["config"] != config:
            sys.exit("run configuration differs from saved results; choose a new --out directory")
    elif list(out_dir.glob("*.json")):
        sys.exit("existing results have no v2 manifest; choose a new --out directory")
    else:
        manifest.write_text(json.dumps({"created_at": datetime.now(timezone.utc).isoformat(),
                                        "config": config}, indent=2))
    if models is not None:
        (out_dir / "models.json").write_text(json.dumps({"base_url": base, "selected_model": model,
                                                       "data": models}, indent=2), encoding="utf-8")
    todo = [r for r in rows if not (out_dir / f"{r['id']}.json").exists()]
    print(f"{len(rows) - len(todo)} done already, {len(todo)} to run -> {out_dir}")

    def one(r):
        rec = answer_record(r, model, base, key, a.max_tokens, mock=bool(a.mock),
                            retry_max_tokens=a.retry_max_tokens, timeout=a.timeout)
        (out_dir / f"{r['id']}.json").write_text(json.dumps(rec, indent=1))
        parsed = rec["answer"]
        if rec.get("api_error"):
            return r["id"], "API_ERROR"
        return r["id"], parsed.get("status", "UNPARSEABLE") if isinstance(parsed, dict) else "UNPARSEABLE"

    with ThreadPoolExecutor(max_workers=1 if a.mock else a.workers) as ex:
        futures = [ex.submit(one, r) for r in todo]
        for i, future in enumerate(as_completed(futures), 1):
            iid, status = future.result()
            print(f"[{i}/{len(todo)}] {iid}: {status}", flush=True)


if __name__ == "__main__":
    main()
