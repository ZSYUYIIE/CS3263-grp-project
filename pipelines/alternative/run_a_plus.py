"""Pipeline A+: pipeline A with checker feedback (alternative approach, not part of the A versus B comparison).

Round 0 is the saved pipeline A reply (results/A/<model>), which was produced with the unchanged A prompt. When that reply
is a PLAN that breaks hard rules, the checker's messages are sent back (pipelines/alternative/prompt_a_plus.py) and the model
answers again, for at most --k rounds. Nothing in results/A is changed.

    python -m pipelines.alternative.run_a_plus --instances instances/q2_900.json
    python -m pipelines.alternative.run_a_plus --instances instances/q2_900.json --k 3 --workers 4
    python -m pipelines.alternative.run_a_plus --instances instances/q2_900.json --mock gold --a-dir results/A/some_model

Results: results/alternative/a_plus/<model>/<instance id>.json (all rounds). The same folder also gets round_0 ... round_k,
each holding every instance with the answer it had after that many feedback rounds, so each can be graded with
    python -m eval.grade results/alternative/a_plus/<model>/round_1 --instances instances/q2_900.json
Re-running continues where it stopped.
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

from eval.checker import check_plan, normalise_plan
from pipelines.alternative.prompt_a_plus import feedback_message
from pipelines.prompt_a import build_messages
from pipelines.run_a import DEFAULT_MAX_TOKENS, ROOT, call_api, parse_reply_how


def add_usage(total, usage):
    for key, value in (usage or {}).items():
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)) and key not in ("attempts", "request_seconds"):
            total[key] = total.get(key, 0) + value
        elif key == "request_seconds":
            total[key] = round(total.get(key, 0) + value, 2)
        elif key == "attempts":
            total[key] = max(total.get(key, 1), value)
        elif key == "finish_reason":
            total[key] = value
        elif isinstance(value, dict):
            inner = total.setdefault(key, {})
            for k2, v2 in value.items():
                if isinstance(v2, (int, float)) and not isinstance(v2, bool):
                    inner[k2] = inner.get(k2, 0) + v2
    return total


def plan_violations(spec, answer):
    if isinstance(answer, dict) and answer.get("status") == "PLAN":
        return check_plan(spec, answer.get("plan"))
    return None


def mock_reply(kind, inst, previous_raw):
    return json.dumps(inst["gold_answer"]) if kind == "gold" else previous_raw


def run_instance(inst, a_rec, a):
    spec = inst["gold_spec"]
    first = {"round": 0, "raw": a_rec.get("raw"), "answer": a_rec.get("answer"), "repair": a_rec.get("repair"),
             "parse_error": a_rec.get("parse_error"), "usage": a_rec.get("usage") or {}, "seconds": a_rec.get("seconds")}
    checkable = inst["gold_answer"]["status"] in ("PLAN", "NO_PLAN")
    viol = plan_violations(spec, first["answer"]) if checkable else None
    first["violations"] = viol
    rounds, end = [first], None
    if not checkable:
        end = "no checker spec"
    elif first["answer"] is None:
        end = "unparseable"
    elif viol is None:
        end = "not a plan"
    elif not viol:
        end = "valid"
    messages = build_messages(inst)
    while end is None:
        prev = rounds[-1]
        if len(rounds) > a.k:
            end = "cap"
            break
        msgs = messages + [{"role": "assistant", "content": prev["raw"]}, feedback_message(prev["violations"])]
        t = time.time()
        if a.mock:
            text, usage = mock_reply(a.mock, inst, prev["raw"]), {}
        else:
            text, usage = call_api(msgs, a.model, a.base, a.key, a.max_tokens)
        parsed, how, err = parse_reply_how(text)
        viol = plan_violations(spec, parsed)
        rnd = {"round": len(rounds), "raw": text, "answer": parsed, "repair": how, "parse_error": err, "usage": usage,
               "seconds": round(time.time() - t, 2), "violations": viol}
        rounds.append(rnd)
        if parsed is None:
            end = "unparseable"
        elif viol is None:
            end = "switched to " + parsed["status"]
        elif not viol:
            end = "valid"
        elif normalise_plan(parsed.get("plan")) == normalise_plan(prev["answer"].get("plan")):
            end = "repeated plan"
    return rounds, end


def cumulative(rounds, upto):
    use, secs = {}, 0
    for r in rounds[: upto + 1]:
        add_usage(use, r["usage"])
        secs += r["seconds"] or 0
    last = rounds[min(upto, len(rounds) - 1)]
    return last, use, round(secs, 2)


def record(inst, rounds, upto, end, model, a):
    last, use, secs = cumulative(rounds, upto)
    return {"id": inst["id"], "pipeline": "A+", "model": model, "round": upto, "rounds_used": len(rounds) - 1,
            "end": end, "seconds": secs, "usage": use, "raw": last["raw"], "answer": last["answer"],
            "fenced": last["repair"] not in (None, "clean"), "repair": last["repair"], "parse_error": last["parse_error"],
            "max_tokens": a.max_tokens, "k": a.k}


def write_round_folders(out_dir, insts, model, a):
    for r in range(a.k + 1):
        d = out_dir / f"round_{r}"
        d.mkdir(exist_ok=True)
        for inst in insts:
            f = out_dir / f"{inst['id']}.json"
            if f.exists():
                full = json.loads(f.read_text())
                (d / f"{inst['id']}.json").write_text(json.dumps(record(inst, full["rounds"], r, full["end"], model, a), indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instances", default=str(ROOT / "instances/instances.json"))
    ap.add_argument("--a-dir", help="saved pipeline A results (default results/A/<model>)")
    ap.add_argument("--k", type=int, default=3, help="maximum number of feedback rounds")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    ap.add_argument("--mock", choices=["gold", "repeat"], help="answer feedback without an API, for testing the harness")
    a = ap.parse_args()

    a.model = "mock-gold" if a.mock else os.environ.get("LLM_MODEL")
    a.base, a.key = os.environ.get("LLM_BASE_URL"), os.environ.get("LLM_API_KEY")
    if not a.mock and not (a.model and a.base and a.key):
        sys.exit("set LLM_BASE_URL, LLM_API_KEY and LLM_MODEL (or use --mock gold)")
    name = re.sub(r"[^\w.-]", "_", a.model)
    a_dir = Path(a.a_dir) if a.a_dir else ROOT / "results" / "A" / name
    out_dir = ROOT / "results" / "alternative" / "a_plus" / name
    out_dir.mkdir(parents=True, exist_ok=True)
    insts = [r for r in json.loads(Path(a.instances).read_text()) if (a_dir / f"{r['id']}.json").exists()]
    todo = [r for r in insts if not (out_dir / f"{r['id']}.json").exists()]
    print(f"{len(insts)} instances with a pipeline A reply in {a_dir}; {len(insts) - len(todo)} done already, {len(todo)} to run -> {out_dir}")

    def one(inst):
        a_rec = json.loads((a_dir / f"{inst['id']}.json").read_text())
        try:
            rounds, end = run_instance(inst, a_rec, a)
        except RuntimeError as e:
            return inst["id"], "API_ERROR", str(e)[:200]
        full = record(inst, rounds, len(rounds) - 1, end, name, a)
        full["rounds"] = rounds
        (out_dir / f"{inst['id']}.json").write_text(json.dumps(full, indent=1))
        trail = " -> ".join("valid" if r["violations"] == [] else "no plan" if r["violations"] is None else f"{len(r['violations'])} broken"
                            for r in rounds)
        return inst["id"], f"{trail} [{end}]", ""

    ex = ThreadPoolExecutor(max_workers=1 if a.mock else a.workers)
    ends = {}
    try:
        for i, (iid, status, note) in enumerate(ex.map(one, todo), 1):
            tag = status.split("[")[-1].rstrip("]")
            ends[tag] = ends.get(tag, 0) + 1
            print(f"[{i}/{len(todo)}] {iid}: {status}" + (f"  {note}" if note else ""), flush=True)
    except KeyboardInterrupt:
        print("stopped; finished instances are saved, run again to continue", flush=True)
        os._exit(1)
    write_round_folders(out_dir, insts, name, a)
    print(f"done: {ends}; round folders written to {out_dir}; instances with API_ERROR were not saved, run the same command again to retry them")


if __name__ == "__main__":
    main()
