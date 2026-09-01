from unittest.mock import patch

from post_processing import clean_output


def test_parses_clean_json():
    raw = '{"explanation": "e", "example": "ex", "key_insights": ["a", "b"]}'
    answer = clean_output(raw)

    assert answer.is_structured is True
    assert answer.explanation == "e"
    assert answer.example == "ex"
    assert answer.key_insights == ["a", "b"]
    assert answer.is_complete is True


def test_strips_markdown_code_fence_around_json():
    raw = '```json\n{"explanation": "e", "example": "ex", "key_insights": ["a"]}\n```'
    answer = clean_output(raw)

    assert answer.is_structured is True
    assert answer.explanation == "e"


def test_extracts_json_object_from_surrounding_prose():
    raw = 'Sure, here is the answer:\n{"explanation": "e", "example": "", "key_insights": []}\nHope that helps!'
    answer = clean_output(raw)

    assert answer.is_structured is True
    assert answer.explanation == "e"


def test_falls_back_to_raw_text_when_not_valid_json():
    raw = "This is just plain prose, not JSON at all."
    answer = clean_output(raw)

    assert answer.is_structured is False
    assert answer.explanation == raw
    assert answer.example == ""
    assert answer.key_insights == []


def test_falls_back_to_raw_text_when_json_is_not_an_object():
    # Valid JSON, but a bare array rather than the expected {...} object.
    raw = '["explanation", "example"]'
    answer = clean_output(raw)

    assert answer.is_structured is False
    assert answer.explanation == raw


def test_recovers_unescaped_quotes_inside_a_string_value_via_json_repair():
    # Regression test: a live model response quoted example dialogue with
    # literal, unescaped `"` characters inside a JSON string value, which
    # strict json.loads correctly rejects as invalid.
    raw = (
        '{"explanation": "e", '
        '"example": "User: "who r u" -> Assistant: "I am an AI."", '
        '"key_insights": ["a"]}'
    )
    answer = clean_output(raw)

    assert answer.is_structured is True
    assert answer.explanation == "e"
    assert "who r u" in answer.example


def test_recovers_missing_closing_bracket_via_json_repair():
    # Regression test: a live model response was truncated/malformed with
    # a smart quote in place of the closing string quote and a missing
    # closing `]` for key_insights, right before the final `}`.
    raw = (
        '{"explanation": "e", "example": "ex", '
        '"key_insights": ["a", "b”}'
    )
    answer = clean_output(raw)

    assert answer.is_structured is True
    assert answer.explanation == "e"
    assert answer.example == "ex"
    assert len(answer.key_insights) >= 1


def test_falls_back_to_raw_text_when_json_repair_itself_raises():
    # Defensive path: json_repair is a third-party best-effort tool, so a
    # crash inside it must not take the app down with it.
    raw = "Some prose { not real json at all"
    with patch("post_processing.repair_json", side_effect=RuntimeError("boom")):
        answer = clean_output(raw)

    assert answer.is_structured is False
    assert answer.explanation == raw


def test_falls_back_to_raw_text_when_json_repair_yields_no_usable_dict():
    # Has a stray brace (so it reaches the json_repair tier), but repair
    # can only recover a bare list from it, not our expected object shape.
    raw = "Some prose { not real json at all"
    answer = clean_output(raw)

    assert answer.is_structured is False
    assert answer.explanation == raw
