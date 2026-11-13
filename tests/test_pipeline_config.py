"""File-based configuration must preserve shell settings and work in every runner."""
import importlib
import json
import os
import sys

import pytest

from pipelines import config

VARIABLES = ("LLM_BASE_URL", "LLM_API_KEY", "LLM_MODEL")
RUNNERS = (
    "pipelines.run_a",
    "pipelines.run_b",
    "pipelines.ablation.run_a_ablation1",
    "pipelines.ablation.run_b_ablation1",
)


@pytest.fixture
def env_root(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "ROOT", tmp_path)
    # Set then delete, so monkeypatch records each variable and restores it after the
    # test even though load_dotenv writes to os.environ directly.
    for name in (*VARIABLES, "PYTHON_DOTENV_DISABLED"):
        monkeypatch.setenv(name, "")
        monkeypatch.delenv(name)
    return tmp_path


def test_loads_project_file_from_other_directory(env_root, tmp_path, monkeypatch):
    (env_root / ".env").write_text('LLM_MODEL="file-model"\nLLM_API_KEY=test-key\n')
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    (elsewhere / ".env").write_text("LLM_MODEL=wrong-model\n")
    monkeypatch.chdir(elsewhere)
    config.load_env()
    assert os.environ["LLM_MODEL"] == "file-model"
    assert os.environ["LLM_API_KEY"] == "test-key"


def test_shell_takes_priority(env_root, monkeypatch):
    (env_root / ".env").write_text("LLM_MODEL=file-model\nLLM_API_KEY=test-key\n")
    monkeypatch.setenv("LLM_MODEL", "shell-model")
    config.load_env()
    assert os.environ["LLM_MODEL"] == "shell-model"
    assert os.environ["LLM_API_KEY"] == "test-key"


def test_missing_file_preserves_environment(env_root, monkeypatch):
    monkeypatch.setenv("LLM_MODEL", "shell-model")
    config.load_env()
    assert os.environ["LLM_MODEL"] == "shell-model"
    assert "LLM_API_KEY" not in os.environ


@pytest.mark.parametrize("module_name", RUNNERS)
@pytest.mark.parametrize("mock", [False, True])
def test_runner_configuration(env_root, monkeypatch, module_name, mock):
    runner = importlib.import_module(module_name)
    monkeypatch.setattr(runner, "ROOT", env_root)
    if not mock:
        (env_root / ".env").write_text(
            "LLM_BASE_URL=https://example.invalid/v1\nLLM_API_KEY=test-key\nLLM_MODEL=file-model\n"
        )
    spec = {"query": "eligible", "target": "CS1101S", "completed": []}
    instance = {"id": "config-check", "request": "Can I take CS1101S? I have completed no courses.",
                "kind": "q1/eligible", "gold_spec": spec, "gold_answer": {"status": "ELIGIBLE"}}
    instances = env_root / "instances.json"
    instances.write_text(json.dumps([instance]))
    calls = []

    def fake_api(messages, model, base, key, max_tokens):
        calls.append((model, base, key))
        reply = spec if "run_b" in module_name else instance["gold_answer"]
        return json.dumps(reply), {}

    monkeypatch.setattr(runner, "call_api", fake_api)
    if "run_a" in module_name:
        monkeypatch.setattr(runner, "build_messages", lambda inst: [{"role": "user", "content": inst["request"]}])
    args = [module_name, "--instances", str(instances), "--workers", "1"]
    if mock:
        args += ["--mock", "gold"]
    monkeypatch.setattr(sys, "argv", args)
    runner.main()
    assert calls == ([] if mock else [("file-model", "https://example.invalid/v1", "test-key")])
    records = list((env_root / "results").rglob("config-check.json"))
    assert len(records) == 1
    record = json.loads(records[0].read_text())
    assert record["model"] == ("mock-gold" if mock else "file-model")
    assert record["answer"]["status"] == "ELIGIBLE"
