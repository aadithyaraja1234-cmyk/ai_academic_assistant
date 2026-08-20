from unittest.mock import patch

from llm_layer import LLMResult
from pipeline import run_pipeline


def _fake_llm_result(content: str) -> LLMResult:
    return LLMResult(
        content=content,
        latency_ms=42.0,
        prompt_tokens=10,
        completion_tokens=20,
        total_tokens=30,
    )


def test_run_pipeline_wires_prompt_llm_and_post_processing():
    raw = '{"explanation": "raw answer", "example": "ex", "key_insights": ["a"]}'
    with patch("pipeline.call_llm", return_value=_fake_llm_result(raw)) as mock_call_llm:
        result = run_pipeline("What is gravity?")

    mock_call_llm.assert_called_once()
    (sent_prompt,), _ = mock_call_llm.call_args
    assert "What is gravity?" in sent_prompt

    assert result.answer.explanation == "raw answer"
    assert result.answer.is_structured is True


def test_run_pipeline_forwards_latency_and_token_metadata():
    raw = '{"explanation": "e", "example": "", "key_insights": []}'
    with patch("pipeline.call_llm", return_value=_fake_llm_result(raw)):
        result = run_pipeline("What is gravity?")

    assert result.latency_ms == 42.0
    assert result.prompt_tokens == 10
    assert result.completion_tokens == 20
    assert result.total_tokens == 30
