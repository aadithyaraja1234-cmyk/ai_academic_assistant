from unittest.mock import MagicMock, patch

import pytest

import llm_layer


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.setenv("MODEL_NAME", "groq/llama-3.1-8b-instant")


def _fake_response(content: str = "ok"):
    response = MagicMock()
    response.__getitem__.side_effect = lambda k: {
        "choices": [{"message": {"content": content}}]
    }[k]
    response.usage = MagicMock(prompt_tokens=5, completion_tokens=7, total_tokens=12)
    return response


def test_call_llm_returns_content_and_usage_on_first_try():
    with patch("llm_layer.completion", return_value=_fake_response("hello")) as mock_completion:
        result = llm_layer.call_llm("some prompt")

    mock_completion.assert_called_once()
    assert result.content == "hello"
    assert result.prompt_tokens == 5
    assert result.completion_tokens == 7
    assert result.total_tokens == 12
    assert result.latency_ms >= 0


def test_call_llm_retries_on_transient_error_then_succeeds():
    with patch(
        "llm_layer.completion",
        side_effect=[RuntimeError("rate limited"), _fake_response("ok after retry")],
    ) as mock_completion, patch("llm_layer.time.sleep"):
        result = llm_layer.call_llm("some prompt")

    assert mock_completion.call_count == 2
    assert result.content == "ok after retry"


def test_call_llm_raises_after_exhausting_retries():
    with (
        patch("llm_layer.completion", side_effect=RuntimeError("still failing")) as mock_completion,
        patch("llm_layer.time.sleep"),
        pytest.raises(RuntimeError, match="LLM call failed"),
    ):
        llm_layer.call_llm("some prompt")

    assert mock_completion.call_count == llm_layer.MAX_RETRIES + 1


def test_resolve_config_raises_clear_error_when_key_missing(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="GROQ_API_KEY"):
        llm_layer._resolve_config()
