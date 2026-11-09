"""Compare discovered SoCLaaS chat models on one shared Route A pilot.

python -m experiments.compare_route_a_models --instances results/model_selection/instances.json
Answers use the normal results/A/<model>/<id>.json format and can be reused in the full run.
This is an exploratory pilot, not evidence of general model superiority.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from statistics import median

from eval.grade import grade_one
from pipelines.prompt_a import build_messages
from pipelines.run_a import ROOT, SOCLAAS_BASE_URL, call_api, discover_model, parse_reply


def diagnostic_record(inst, rec):
    """Remove a known extra wrapper for a separate diagnostic, never the official grade."""
    answer = rec.get("answer") if rec else None
    branch = "plan" if inst["gold_spec"]["query"] == "plan" else "eligibility"
    if isinstance(answer, dict) and "status" not in answer and isinstance(answer.get(branch), dict):
        return dict(rec, answer=answer[branch]), True
    return rec, False


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--instances", required=True)
    ap.add_argument("--models", nargs="+", default=["qwen3.8:27b", "x-test-1", "x-test-2", "x-test-4"])
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--max-tokens", type=int, default=8192)
    ap.add_argument("--report-only", action="store_true", help="regrade saved responses without any API calls")
    a = ap.parse_args()
    key = os.environ.get("SOCLAAS_API_KEY")
    if not key and not a.report_only:
        raise SystemExit("set SOCLAAS_API_KEY")
    instances = json.loads(Path(a.instances).read_text(encoding="utf-8"))
    out = ROOT / "results/model_selection"
    saved = json.loads((out / "config.json").read_text(encoding="utf-8")) if a.report_only else None
    discovered, paths, model_info = [], {}, {}
    for requested in saved["models"] if saved else a.models:
        if saved:
            model, models = requested, list(saved["models"].values())
        else:
            model, models = discover_model(SOCLAAS_BASE_URL, key, requested)
        discovered.append(model)
        paths[model] = ROOT / "results/A" / re.sub(r"[^\w.-]", "_", model)
        paths[model].mkdir(parents=True, exist_ok=True)
        model_info[model] = next(m for m in models if m["id"] == model)
        if not a.report_only:
            (paths[model] / "models.json").write_text(json.dumps({
                "base_url": SOCLAAS_BASE_URL, "selected_model": model, "data": models}, indent=2), encoding="utf-8")
        label = "Loaded saved metadata for" if a.report_only else "Discovered"
        print(f"{label} {model}: {model_info[model]['soclaas']['display_name']}", flush=True)
    out.mkdir(parents=True, exist_ok=True)
    config = {"models": model_info, "instances": [i["id"] for i in instances],
              "max_tokens": a.max_tokens, "temperature": 0, "reasoning_effort": "provider default",
              "workers": a.workers, "note": "Exploratory shared pilot; one response per model and instance."}
    if not a.report_only:
        (out / "config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")

    def one(model, inst):
        path = paths[model] / f"{inst['id']}.json"
        if path.exists():
            return
        started = time.monotonic()
        text, usage = call_api(build_messages(inst), model, SOCLAAS_BASE_URL, key, a.max_tokens)
        parsed, fenced, error = parse_reply(text)
        rec = {"id": inst["id"], "pipeline": "A", "model": model,
               "seconds": round(time.monotonic() - started, 2), "usage": usage,
               "raw": text, "answer": parsed, "fenced": fenced, "parse_error": error}
        path.write_text(json.dumps(rec, indent=1), encoding="utf-8")

    grades_path = out / "grades.json"
    errors = (json.loads(grades_path.read_text(encoding="utf-8")).get("errors", {})
              if a.report_only and grades_path.exists() else {})
    with ThreadPoolExecutor(max_workers=a.workers) as executor:
        futures = {executor.submit(one, model, inst): (model, inst["id"])
                   for inst in ([] if a.report_only else instances) for model in discovered}
        for future in as_completed(futures):
            model, iid = futures[future]
            try:
                future.result()
                print(f"{model} {iid}: saved", flush=True)
            except RuntimeError as exc:
                errors[f"{model}/{iid}"] = str(exc)
                print(f"{model} {iid}: {exc}", flush=True)

    lines = ["# Route A model-selection pilot", "",
             f"Same {len(instances)} cases, prompts, catalogue records and token cap; "
             "provider-default reasoning effort.",
             "One response per case. This small, exploratory sample does not establish general superiority.",
             "Latency includes shared-service queueing and retries; costs use the discovery API's listed rates.", "",
             "Strict scores use the untouched response. Diagnostic scores remove only an extra `plan` or",
             "`eligibility` wrapper to distinguish format errors from reasoning errors; the task type comes",
             "from the gold spec for this offline diagnostic only. Stored responses and official grades are unchanged.",
             "Recorded-reply cost excludes failed calls without final text, which may also be charged.", "",
             "| Exact model ID | Answered | Strict status | Wrappers | Diagnostic status |"
             " Diagnostic valid plans | Diagnostic optimal plans | Median seconds | Recorded-reply USD |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    all_grades = {}
    feasible = sum(i["gold_answer"]["status"] == "PLAN" for i in instances)
    for model in discovered:
        records = [json.loads((paths[model] / f"{i['id']}.json").read_text(encoding="utf-8"))
                   if (paths[model] / f"{i['id']}.json").exists() else None for i in instances]
        grades = [grade_one(i, r) for i, r in zip(instances, records)]
        diagnostic = [diagnostic_record(i, r) for i, r in zip(instances, records)]
        diagnostic_grades = [grade_one(i, r) for i, (r, _) in zip(instances, diagnostic)]
        all_grades[model] = {"strict": grades, "diagnostic": diagnostic_grades}
        valid = sum(g["gold_status"] == "PLAN" and g["status"] == "PLAN" and not g["violations"]
                    for g in diagnostic_grades)
        optimal = sum(g["class"] == "optimal" for g in diagnostic_grades)
        seconds = [r["seconds"] for r in records if r]
        rates = model_info[model]["soclaas"]
        cost = sum((r.get("usage", {}).get("prompt_tokens", 0)
                    * rates["input_microdollars_per_million_tokens"]
                    + r.get("usage", {}).get("completion_tokens", 0)
                    * rates["output_microdollars_per_million_tokens"]) / 1e12 for r in records if r)
        latency = f"{median(seconds):.1f}" if seconds else "-"
        lines.append(f"| `{model}` | {len(seconds)}/{len(instances)} |"
                     f" {sum(g['status_correct'] for g in grades)}/{len(instances)} |"
                     f" {sum(w for _, w in diagnostic)} |"
                     f" {sum(g['status_correct'] for g in diagnostic_grades)}/{len(instances)} |"
                     f" {valid}/{feasible} | {optimal}/{feasible} | {latency} | ${cost:.4f} |")
    if saved and saved.get("stopping_note"):
        lines += ["", saved["stopping_note"],
                  "Missing responses are coverage gaps, not evidence that the model reasoned incorrectly."]
    (out / "grades.json").write_text(json.dumps({"grades": all_grades, "errors": errors}, indent=2), encoding="utf-8")
    (out / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
