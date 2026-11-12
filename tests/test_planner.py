"""Offline sessions exercise translation boundaries and real solver integration."""
import copy
import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

from eval.checker import check_plan
from pipelines import config
from pipelines.run_b import PROMPT
from planner import cli
from planner.formatting import HEADLINES, format_answer, semester_label, summary
from solver.run import prepare, run

ROOT = Path(__file__).resolve().parent.parent
Q1 = {"query": "eligible", "target": "CS1101S", "completed": []}
Q2 = {"query": "plan", "current_sem": 1, "completed": [], "must_take": ["CS1101S"]}
ROWS = json.loads((ROOT / "instances/instances.json").read_text())


def flat(text):
    """Answers are word-wrapped for the terminal; compare text with whitespace collapsed."""
    return " ".join(text.split())


def headline(status):
    return HEADLINES[status].split("{")[0].strip()


@pytest.fixture(scope="module")
def catalog():
    return cli.Catalog.load()


def session(inputs, replies, catalog):
    """Fail on unexpected prompts instead of letting EOF hide a broken flow."""
    pending = iter(inputs)
    output = []
    translator = Mock(side_effect=copy.deepcopy(replies))

    def read(prompt):
        output.append(prompt)
        try:
            return next(pending)
        except StopIteration:
            pytest.fail(f"Unexpected prompt: {prompt}")

    cli.run_session(translator, catalog, read=read, write=output.append)
    assert list(pending) == []
    return flat("\n".join(output)), translator


def test_q1_session_preserves_optional_semester_and_solver_input(catalog, monkeypatch):
    spy = Mock(wraps=run)
    monkeypatch.setattr(cli, "run", spy)
    output, translator = session(["1", "Can I take CS1101S? I completed no courses.", "", "3"], [Q1], catalog)
    assert headline("ELIGIBLE") in output
    assert "Not specified; see offering notes" in output
    assert "Notes - no semester given" in output
    spy.assert_called_once_with(Q1, catalog)
    assert ("NUS course planner for BComp (CS) Hons AY" + catalog.data["acad_year"].replace("-", "/")) in output
    assert "Does this match" not in output
    assert "Student profile:" not in translator.call_args.args[0]
    assert "confirmed at startup" not in output
    assert "Selected task: check whether I can take a course" in translator.call_args.args[0]


def test_plan_session_sends_unchanged_constraints_to_real_solver(catalog, monkeypatch):
    spec = json.loads((ROOT / "examples/q2_plan.json").read_text())
    spec.update(unsupported=["no 8am classes"], mc_min=4, late=["CS2106"])
    spy = Mock(wraps=run)
    monkeypatch.setattr(cli, "run", spy)
    output, _ = session(["2", "Plan these courses with my constraints.", "", "3"], [spec], catalog)
    spy.assert_called_once_with(spec, catalog)
    answer = run(spec, catalog)
    assert answer["status"] == "PLAN"
    assert check_plan(spec, answer["plan"]) == []
    assert headline("PLAN") in output
    assert "Year 3 Semester 2 (semester 6): 0 (blocked)" in output
    assert "Must: CS2100 before CS2106" in output
    assert "Prefer: CS3230 in Year 3 Semester 1" in output
    assert "Minimum MC in each nonempty semester: 4" in output
    assert "Wishes I could not apply - no 8am classes" in output
    assert "does not check your full graduation requirements" in output


def test_followups_update_only_missing_fields_and_do_not_call_llm_again(catalog, monkeypatch):
    original = {"query": "plan", "mc_max": 12, "unsupported": ["light last semester"]}
    spy = Mock(wraps=run)
    monkeypatch.setattr(cli, "run", spy)
    output, translator = session(
        ["2", "Plan my courses.", "", "nothing", "none", "wrong", "Y1S1", "cs1101s", "", "3"],
        [original], catalog)
    translator.assert_called_once()
    spy.assert_called_once_with({**original, "completed": [], "current_sem": 1, "must_take": ["CS1101S"]}, catalog)
    assert headline("PLAN") in output
    assert "Maximum MC per semester: 12" in output
    assert "Wishes I could not apply - light last semester" in output


def test_target_and_explicit_empty_must_take_followups(catalog):
    output, _ = session(["1", "Check eligibility.", "CS1101S, CS1231S", "cs1101s", "", "3"],
                        [{"query": "eligible", "completed": []}], catalog)
    assert "Enter one course code" in output
    assert headline("ELIGIBLE") in output
    output, _ = session(["2", "I have nothing left to schedule.", "none", "", "3"],
                        [{"query": "plan", "current_sem": 1, "completed": []}], catalog)
    assert "no remaining courses to schedule" in output


@pytest.mark.parametrize("action", ["s", "r", "b"])
def test_query_mismatch_requires_explicit_choice(catalog, monkeypatch, action):
    spy = Mock(wraps=run)
    monkeypatch.setattr(cli, "run", spy)
    inputs, replies = ["1", "Plan my courses.", action], [Q2]
    if action == "s":
        inputs += ["", "3"]
    elif action == "r":
        inputs += ["Can I take CS1101S?", "", "3"]
        replies.append(Q1)
    else:
        inputs += ["3"]
    output, _ = session(inputs, replies, catalog)
    assert "Your request was interpreted as: plan my remaining courses" in output
    assert spy.call_count == (0 if action == "b" else 1)
    if action != "b":
        assert spy.call_args.args[0] == (Q2 if action == "s" else Q1)


def test_replacement_and_new_query_have_no_stale_fields(catalog, monkeypatch):
    spy = Mock(wraps=run)
    monkeypatch.setattr(cli, "run", spy)
    old = {**Q2, "mc_max": 4, "unsupported": ["old wish"]}
    output, translator = session(
        ["2", "Old request.", "r", "Replacement request.", "", "1", "New question.", "", "3"],
        [old, Q2, Q1], catalog)
    assert [call.args[0] for call in spy.call_args_list] == [Q2, Q1]
    assert "Maximum MC per semester: 20 (default)" in output
    assert output.count("NUS course planner for BComp (CS) Hons") == 1
    assert "Old request" not in translator.call_args_list[1].args[0]
    assert "Replacement request" not in translator.call_args_list[2].args[0]


@pytest.mark.parametrize("programme", [
    "Business Analytics", "BComp CS Hons with a minor in Mathematics",
    "BComp CS Hons with a second major in Mathematics",
    "BComp CS Hons double degree", "BComp CS Hons concurrent degree",
])
def test_out_of_scope_request_never_calls_solver(catalog, monkeypatch, programme):
    spy = Mock()
    monkeypatch.setattr(cli, "run", spy)
    request = f"I am in {programme}. Plan my courses."
    output, translator = session(["2", request, "b", "3"], [{**Q2, "programme": programme}], catalog)
    assert headline("OUT_OF_SCOPE") in output
    translator.assert_called_once()
    assert request in translator.call_args.args[0]
    spy.assert_not_called()


@pytest.mark.parametrize("spec,status", [
    ({**Q1, "colour": "blue"}, "INVALID_SPEC"),
    ({**Q1, "programme": "BComp CS Hons with minor in Mathematics"}, "OUT_OF_SCOPE"),
    ({**Q1, "target": "UNKNOWN9999"}, "OUT_OF_SCOPE"),
    ({**Q2, "current_sem": 9}, "OUT_OF_SCOPE"),
])
def test_preflight_refusals_do_not_reach_solver(catalog, monkeypatch, spec, status):
    spy = Mock()
    monkeypatch.setattr(cli, "run", spy)
    output, _ = session(["1" if spec["query"] == "eligible" else "2", "My request.", "b", "3"],
                        [spec], catalog)
    assert headline(status) in output
    spy.assert_not_called()


def test_unknown_completed_warning_is_visible_without_changing_solver_policy(catalog):
    spec = {**Q1, "completed": ["UNKNOWN9999"], "must_take": ["CS1231S"]}
    output, _ = session(["1", "Check the course.", "", "3"], [spec], catalog)
    assert "completed course UNKNOWN9999 is not in the catalogue and was ignored" in output
    assert "belongs to query 'plan'" in output
    assert headline("ELIGIBLE") in output


@pytest.mark.parametrize("status,menu", [("NOT_ELIGIBLE", "1"), ("NO_PLAN", "2")])
def test_solver_refusals_preserve_reasons_in_interactive_session(catalog, status, menu):
    spec = next(row["gold_spec"] for row in ROWS if row["gold_answer"]["status"] == status)
    answer = run(spec, catalog)
    output, _ = session([menu, "Check my request.", "", "3"], [spec], catalog)
    assert headline(status) in output
    assert all(reason in output for reason in answer["reasons"])


def test_out_of_range_followup_is_rejected_by_existing_scope_rules(catalog, monkeypatch):
    spy = Mock()
    monkeypatch.setattr(cli, "run", spy)
    output, _ = session(["2", "Plan my courses.", "Y5S1", "b", "3"],
                        [{"query": "plan", "completed": [], "must_take": []}], catalog)
    assert headline("OUT_OF_SCOPE") in output
    assert "current_sem is 9" in output
    spy.assert_not_called()


def test_api_retry_keeps_request_and_recovers(catalog):
    output, translator = session(["1", "Check the course.", "t", "", "3"],
                                 [RuntimeError("API unavailable"), Q1], catalog)
    assert "API unavailable" in output and headline("ELIGIBLE") in output
    assert translator.call_args_list[0] == translator.call_args_list[1]


@pytest.mark.parametrize("action", ["r", "b"])
def test_api_failure_can_replace_or_leave(catalog, action):
    inputs = ["1", "Old request.", action]
    replies = [RuntimeError("Translation failed")]
    if action == "r":
        inputs += ["New request.", "", "3"]
        replies.append(Q1)
    else:
        inputs.append("3")
    output, translator = session(inputs, replies, catalog)
    assert translator.call_count == (2 if action == "r" else 1)
    assert "Goodbye" in output


def test_global_navigation_and_blank_menu(catalog):
    output, _ = session(["", "1", "/back", "2", "Plan my courses.", "/back", "1", "/quit"],
                        [{"query": "plan"}], catalog)
    assert "Please choose 1, 2, 3" in output
    assert not any(headline(status) in output for status in HEADLINES)
    assert "Session ended" in output


@pytest.mark.parametrize("error", [EOFError, KeyboardInterrupt])
def test_interruption_exits_cleanly(catalog, error):
    output = []
    cli.run_session(Mock(), catalog, read=Mock(side_effect=error), write=output.append)
    assert output[-2:] == ["\nSession ended.", "Goodbye."]


def test_unchanged_prompt_and_interactive_api_limits(monkeypatch):
    fake = Mock(return_value=(json.dumps(Q1), {}))
    monkeypatch.setattr(cli, "call_api", fake)
    assert cli.translate_request("Student request", model="model",
                                 base_url="https://example.invalid/v1", key="key") == Q1
    args, kwargs = fake.call_args
    assert args[0][0] == {"role": "system", "content": PROMPT}
    assert args[0][1]["content"] == "Request: Student request\nJSON:"
    assert kwargs == {"timeout": 60, "retries": 1}


@pytest.mark.parametrize("text,usage,message", [
    ("", {}, "empty reply"), ("not json", {}, "no usable JSON"),
    (json.dumps(Q1), {"finish_reason": "length"}, "cut short"),
    (json.dumps(Q1) + "\n" + json.dumps(Q2), {}, "several possible requests"),
])
def test_bad_translation_is_not_sent_to_solver(monkeypatch, text, usage, message):
    monkeypatch.setattr(cli, "call_api", Mock(return_value=(text, usage)))
    with pytest.raises(RuntimeError, match=message):
        cli.translate_request("Request", model="model", base_url="url", key="key")


def test_fenced_translation_can_be_reviewed(monkeypatch):
    monkeypatch.setattr(cli, "call_api", Mock(return_value=(f"```json\n{json.dumps(Q1)}\n```", {})))
    assert cli.translate_request("Request", model="model", base_url="url", key="key") == Q1


def test_formatting_preserves_all_gold_explanations_and_input(catalog):
    for row in ROWS:
        answer = copy.deepcopy(row["gold_answer"])
        before = copy.deepcopy(answer)
        output = flat(format_answer(answer, catalog))
        assert answer == before
        status = "NEVER_ELIGIBLE" if answer.get("can_still_become_eligible") is False else answer["status"]
        assert HEADLINES[status].format(target=answer.get("target", "")) in output
        assert "Result:" not in output
        for key in ("reasons", "errors", "warnings", "notes", "preferences_met", "preferences_not_met", "not_applied"):
            assert all(flat(item) in output for item in answer.get(key, [])), (row["id"], key)
        for key in ("message", "never_eligible_because"):
            if key in answer:
                assert flat(answer[key]) in output
        spec = copy.deepcopy(row["gold_spec"])
        early, cleaned, warnings = prepare(spec, catalog)
        if early is None:
            summary(spec, cleaned, warnings)
            assert spec == row["gold_spec"]


def test_timeout_reason_does_not_become_proven_infeasibility():
    answer = {"status": "NO_PLAN", "reasons": ["the solver ran out of time before finding a plan"]}
    output = format_answer(answer)
    assert answer["reasons"][0] in output
    assert "infeasible" not in output.lower()


def test_atap_and_all_rule_types_appear_in_summary(catalog):
    spec = {**Q2, "atap_sems": [2], "sem_caps": {"2": 1}, "early": ["CS1101S"], "late": ["CS1231S"],
            "rules": [{"type": kind, "a": "CS1101S", "b": "CS1231S", "strength": strength}
                      for kind, strength in (("before", "must"), ("apart", "prefer"), ("same_sem", "prefer"))]}
    early, cleaned, warnings = prepare(spec, catalog)
    assert early is None
    output = summary(spec, cleaned, warnings)
    for text in ("ATAP allowed in: Year 1 Semester 2", "Must: CS1101S before CS1231S",
                 "Prefer: CS1101S in a different semester from CS1231S",
                 "Prefer: CS1101S in the same semester as CS1231S", "Prefer earlier: CS1101S",
                 "Prefer later: CS1231S"):
        assert text in output


def test_main_loads_root_env_and_preserves_shell_settings(tmp_path, monkeypatch, catalog):
    monkeypatch.setattr(config, "ROOT", tmp_path)
    (tmp_path / ".env").write_text("LLM_BASE_URL=https://example.invalid/v1\nLLM_API_KEY=test-key\nLLM_MODEL=file-model\n")
    for name in ("LLM_BASE_URL", "LLM_API_KEY", "LLM_MODEL", "PYTHON_DOTENV_DISABLED"):
        monkeypatch.setenv(name, "")
        monkeypatch.delenv(name)
    monkeypatch.setenv("LLM_MODEL", "shell-model")
    fake = Mock(return_value=Q1)
    monkeypatch.setattr(cli, "translate_request", fake)

    def fake_session(translate, actual_catalog):
        assert actual_catalog.data["acad_year"] == catalog.data["acad_year"]
        assert translate("Request") == Q1

    monkeypatch.setattr(cli, "run_session", fake_session)
    assert cli.main(["--timeout", "15", "--retries", "0", "--max-tokens", "1024"]) == 0
    fake.assert_called_once_with("Request", model="shell-model", base_url="https://example.invalid/v1",
                                 key="test-key", max_tokens=1024, timeout=15, retries=0)


def test_missing_configuration_is_actionable_and_does_not_start_session(monkeypatch, capsys):
    monkeypatch.setattr(cli, "load_env", Mock())
    for name in ("LLM_BASE_URL", "LLM_API_KEY", "LLM_MODEL"):
        monkeypatch.delenv(name, raising=False)
    spy = Mock()
    monkeypatch.setattr(cli, "run_session", spy)
    assert cli.main([]) == 2
    assert ".env.example" in capsys.readouterr().out
    spy.assert_not_called()


@pytest.mark.parametrize("args", [["--timeout", "0"], ["--max-tokens", "-1"], ["--retries", "3"]])
def test_invalid_options_fail_before_configuration(monkeypatch, args):
    spy = Mock()
    monkeypatch.setattr(cli, "load_env", spy)
    with pytest.raises(SystemExit) as error:
        cli.main(args)
    assert error.value.code == 2
    spy.assert_not_called()


def test_module_entry_point_help_and_clean_exit():
    result = subprocess.run([sys.executable, "-m", "planner", "--help"], cwd=ROOT,
                            capture_output=True, text=True, check=True)
    assert "natural language" in result.stdout
    env = {**os.environ, "LLM_BASE_URL": "https://example.invalid/v1", "LLM_API_KEY": "test-key", "LLM_MODEL": "model"}
    result = subprocess.run([sys.executable, "-m", "planner"], cwd=ROOT, env=env, input="3\n",
                            capture_output=True, text=True, check=True)
    assert "Goodbye" in result.stdout
    assert result.stderr == ""


@pytest.mark.parametrize("error", [ValueError("unknown url type: 'localhost:8000/chat/completions'"),
                                   IndexError("list index out of range")])
def test_unexpected_api_errors_reach_the_retry_menu(monkeypatch, catalog, error):
    monkeypatch.setattr(cli, "call_api", Mock(side_effect=error))
    with pytest.raises(RuntimeError, match=type(error).__name__):
        cli.translate_request("Request", model="model", base_url="localhost:8000", key="key")

    def translate(request):
        return cli.translate_request(request, model="model", base_url="localhost:8000", key="key")
    output = []
    inputs = iter(["1", "Check the course.", "b", "3"])
    cli.run_session(translate, catalog, read=lambda prompt: next(inputs), write=output.append)
    assert any("API error" in line for line in output) and output[-1] == "Goodbye."


def test_null_fields_from_translation_are_labelled_default(catalog):
    spec = {**Q2, "mc_max": None, "objective": None}
    _, cleaned, warnings = prepare(spec, catalog)
    text = flat(summary(spec, cleaned, warnings))
    assert "Maximum MC per semester: 20 (default)" in text
    assert "Goal: No particular goal (default)" in text


def test_completed_followup_has_one_hint(catalog):
    output, _ = session(["2", "Plan CS1101S.", "none", "", "3"],
                        [{"query": "plan", "current_sem": 1, "must_take": ["CS1101S"]}], catalog)
    assert 'Please give the courses you have already completed (comma-separated codes, or "none"): ' in output
    assert "say so if there are none" not in output


def test_plan_lists_each_semester_with_titles_and_totals(catalog):
    answer = run({**Q2, "must_take": ["CS2040S"]}, catalog)
    assert answer["status"] == "PLAN" and answer.get("added_prerequisites")
    output = format_answer(answer, catalog)
    assert "Result:" not in output and "PLAN" not in output
    lines = output.splitlines()
    for sem, codes in answer["plan"].items():
        assert any(line.strip().startswith(semester_label(int(sem))) for line in lines)
        for code in codes:
            line = next(line for line in lines if line.strip().startswith(f"- {code} "))
            assert catalog[code]["title"] in line
            assert ("prerequisite" in line) == (code in answer["added_prerequisites"])
    assert f"Total: {sum(answer['mc_per_semester'].values())} MC" in output


def test_never_eligible_has_its_own_headline(catalog):
    row = next(r for r in ROWS if r["gold_answer"].get("can_still_become_eligible") is False)
    output = format_answer(run(row["gold_spec"], catalog), catalog)
    title = output.strip().splitlines()[1].strip()
    assert title == f"No, you cannot take {row['gold_answer']['target']}"
