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
