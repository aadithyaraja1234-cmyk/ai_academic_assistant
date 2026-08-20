from unittest.mock import patch

import cli
from pipeline import PipelineResult
from schemas import StructuredAnswer


def _result(**overrides) -> PipelineResult:
    defaults = dict(
        answer=StructuredAnswer(
            explanation="e", example="ex", key_insights=["a", "b"], is_structured=True
        ),
        latency_ms=123.0,
        prompt_tokens=1,
        completion_tokens=2,
        total_tokens=3,
    )
    defaults.update(overrides)
    return PipelineResult(**defaults)


def test_render_includes_every_section_and_latency():
    output = cli.render(_result())
    assert "Explanation:\ne" in output
    assert "Example:\nex" in output
    assert "- a" in output and "- b" in output
    assert "[latency: 123 ms]" in output


def test_render_flags_unstructured_fallback():
    answer = StructuredAnswer(explanation="raw text", is_structured=False)
    output = cli.render(_result(answer=answer))
    assert "did not return structured JSON" in output


def test_main_prints_message_for_blank_input(capsys):
    with patch("cli.get_user_input", return_value="   "):
        cli.main()
    assert "No question provided." in capsys.readouterr().out


def test_main_prints_friendly_message_on_invalid_input(capsys):
    with (
        patch("cli.get_user_input", return_value="a" * 5000),
        patch("cli.run_pipeline", side_effect=ValueError("too long")),
    ):
        cli.main()
    assert "Invalid input" in capsys.readouterr().out


def test_main_prints_friendly_message_on_request_failure(capsys):
    with (
        patch("cli.get_user_input", return_value="What is gravity?"),
        patch("cli.run_pipeline", side_effect=RuntimeError("API down")),
    ):
        cli.main()
    assert "Request failed" in capsys.readouterr().out


def test_main_prints_rendered_answer_on_success(capsys):
    with (
        patch("cli.get_user_input", return_value="What is gravity?"),
        patch("cli.run_pipeline", return_value=_result()),
    ):
        cli.main()
    assert "Explanation:\ne" in capsys.readouterr().out
