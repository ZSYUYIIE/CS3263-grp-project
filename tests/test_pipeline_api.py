"""Client contract tests: discovery, non-streaming requests, retries and safe failures."""
import io
import json
from urllib.error import HTTPError

import pytest

from eval.grade import grade_one
from experiments.compare_route_a_models import diagnostic_record
from pipelines.run_a import SOCLAAS_BASE_URL, answer_record, call_api, discover_model, request_json


def response(data):
    return io.BytesIO(json.dumps(data).encode())


def test_discovery_precedes_chat_and_preserves_history(monkeypatch):
    requests = []
    messages = [{"role": "system", "content": "instructions"},
                {"role": "user", "content": "first"},
                {"role": "assistant", "content": "answer"},
                {"role": "user", "content": "follow-up"}]

    def open_request(req, timeout):
        requests.append(req)
        assert req.get_header("Authorization") == "Bearer test-secret"
        if req.get_method() == "GET":
            return response({"data": [{"id": "qwen3.8:27b", "soclaas": {"capabilities": ["chat"]}}]})
        return response({"choices": [{"message": {"content": '{"status":"PLAN"}'}}],
                         "usage": {"total_tokens": 42}})

    monkeypatch.setattr("urllib.request.urlopen", open_request)
    model, _ = discover_model(SOCLAAS_BASE_URL, "test-secret")
    text, usage = call_api(messages, model, SOCLAAS_BASE_URL, "test-secret", 8192)
    assert [r.full_url for r in requests] == [SOCLAAS_BASE_URL + "/models",
                                             SOCLAAS_BASE_URL + "/chat/completions"]
    payload = json.loads(requests[1].data)
    assert payload["model"] == "qwen3.8:27b"
    assert payload["stream"] is False
    assert payload["messages"] == messages
    assert text == '{"status":"PLAN"}' and usage == {"total_tokens": 42}


def test_discovery_rejects_embeddings_and_unknown_ids(monkeypatch):
    monkeypatch.setattr("pipelines.run_a.request_json", lambda *args: {"data": [
        {"id": "bge-m3", "soclaas": {"capabilities": ["embeddings"]}}]})
    for model in ("bge-m3", "invented-model", None):
        with pytest.raises(ValueError):
            discover_model(SOCLAAS_BASE_URL, "test-secret", model)


@pytest.mark.parametrize("status", [429, 500, 502, 503, 504])
def test_temporary_http_errors_have_bounded_retries(monkeypatch, status):
    calls, sleeps = [], []

    def fail(req, timeout):
        calls.append(req)
        raise HTTPError(req.full_url, status, "temporary failure", {}, io.BytesIO(b"retry later"))

    monkeypatch.setattr("urllib.request.urlopen", fail)
    monkeypatch.setattr("time.sleep", sleeps.append)
    with pytest.raises(RuntimeError, match=f"API error {status}"):
        request_json("/models", SOCLAAS_BASE_URL, "test-secret")
    assert len(calls) == 5
    assert sleeps == [2, 4, 8, 16]


@pytest.mark.parametrize("status", [400, 401, 403, 404, 422])
def test_permanent_http_errors_fail_without_retry_and_redact_key(monkeypatch, status):
    def fail(req, timeout):
        raise HTTPError(req.full_url, status, "invalid request", {}, io.BytesIO(b"echo test-secret"))

    monkeypatch.setattr("urllib.request.urlopen", fail)
    monkeypatch.setattr("time.sleep", lambda _: pytest.fail("permanent failure must not retry"))
    with pytest.raises(RuntimeError) as exc:
        request_json("/models", SOCLAAS_BASE_URL, "test-secret")
    assert "test-secret" not in str(exc.value)
    assert "[REDACTED]" in str(exc.value)


def test_reasoning_only_response_is_not_recorded_as_answer(monkeypatch):
    monkeypatch.setattr("pipelines.run_a.request_json", lambda *args: {
        "choices": [{"message": {"content": None, "reasoning_content": "unfinished"}}]})
    with pytest.raises(RuntimeError, match="non-text content"):
        call_api([], "qwen3.8:27b", SOCLAAS_BASE_URL, "test-secret", 1)


def test_wrapper_diagnostic_does_not_change_official_grade_or_record():
    inst = {"id": "format-case", "kind": "q1/precluded", "gold_spec": {"query": "eligible"},
            "gold_answer": {"status": "NOT_ELIGIBLE"}}
    rec = {"answer": {"eligibility": {"status": "NOT_ELIGIBLE", "reasons": []}}}
    before = json.dumps(rec)
    diagnostic, wrapped = diagnostic_record(inst, rec)
    assert wrapped
    assert grade_one(inst, diagnostic)["status_correct"]
    assert not grade_one(inst, rec)["status_correct"]
    assert json.dumps(rec) == before


def test_missing_final_text_is_recorded_with_usage_and_without_a_fabricated_answer(monkeypatch):
    monkeypatch.setattr("pipelines.run_a.request_json", lambda *args: {
        "choices": [{"message": {"content": None}}], "usage": {"completion_tokens": 8192}})
    inst = {"id": "budget-case", "request": "Can I take CS3263?", "gold_spec": {}}
    rec = answer_record(inst, "x-test-2", SOCLAAS_BASE_URL, "test-secret", 8192)
    assert rec["raw"] is None and rec["answer"] is None
    assert rec["usage"] == {"completion_tokens": 8192}
    assert "non-text content" in rec["api_error"]
