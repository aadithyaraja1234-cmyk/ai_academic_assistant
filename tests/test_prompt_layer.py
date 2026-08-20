import pytest

from prompt_layer import MAX_QUESTION_LENGTH, SYSTEM_PROMPT, build_prompt


def test_system_prompt_has_no_stray_leading_quote():
    assert not SYSTEM_PROMPT.strip().startswith('"')


def test_build_prompt_includes_the_question():
    prompt = build_prompt("What is gravity?")
    assert "What is gravity?" in prompt


def test_build_prompt_requests_the_expected_json_keys():
    prompt = build_prompt("What is gravity?")
    assert '"explanation"' in prompt
    assert '"example"' in prompt
    assert '"key_insights"' in prompt


def test_build_prompt_rejects_empty_input():
    with pytest.raises(ValueError, match="empty"):
        build_prompt("   ")


def test_build_prompt_rejects_input_over_the_length_limit():
    too_long = "a" * (MAX_QUESTION_LENGTH + 1)
    with pytest.raises(ValueError, match="too long"):
        build_prompt(too_long)


def test_build_prompt_accepts_input_at_exactly_the_length_limit():
    at_limit = "a" * MAX_QUESTION_LENGTH
    assert build_prompt(at_limit)  # does not raise
