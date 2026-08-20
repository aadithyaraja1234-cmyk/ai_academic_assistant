from schemas import StructuredAnswer


def test_defaults_are_empty_and_structured():
    answer = StructuredAnswer()
    assert answer.explanation == ""
    assert answer.example == ""
    assert answer.key_insights == []
    assert answer.is_structured is True
    assert answer.is_complete is False


def test_is_complete_requires_every_section_filled():
    partial = StructuredAnswer(explanation="x", example="", key_insights=["a"])
    assert partial.is_complete is False

    full = StructuredAnswer(explanation="x", example="y", key_insights=["a"])
    assert full.is_complete is True
