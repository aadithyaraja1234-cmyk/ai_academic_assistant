from pydantic import BaseModel, Field


class StructuredAnswer(BaseModel):
    """A parsed, validated answer from the LLM.

    ``is_structured`` is False when the model didn't return valid JSON and
    the app fell back to showing the raw text as ``explanation`` instead of
    crashing. ``is_complete`` reports whether every section was actually
    filled in, which is a stricter, independent signal used by the eval
    harness (a response can be valid JSON but still leave a section empty).
    """

    explanation: str = ""
    example: str = ""
    key_insights: list[str] = Field(default_factory=list)
    is_structured: bool = True

    @property
    def is_complete(self) -> bool:
        return bool(self.explanation and self.example and self.key_insights)
