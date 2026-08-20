import json
import re

from schemas import StructuredAnswer

_JSON_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


def _extract_json(text: str) -> str:
    """Best-effort extraction of a JSON object from a raw LLM response.

    Small instruction-tuned models often wrap JSON in markdown code fences
    or add a stray sentence despite being told not to, so this strips
    fences and, failing that, slices out the outermost {...} block before
    giving up and returning the text unchanged.
    """
    text = _JSON_FENCE_RE.sub("", text.strip()).strip()

    if text.startswith("{") and text.endswith("}"):
        return text

    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]

    return text


def clean_output(raw_response: str) -> StructuredAnswer:
    """Parse the raw LLM response into a validated StructuredAnswer.

    Falls back to a best-effort unstructured answer (is_structured=False,
    the raw text as `explanation`) if the model didn't return valid JSON,
    so the app degrades gracefully instead of crashing.
    """
    candidate = _extract_json(raw_response)
    try:
        data = json.loads(candidate)
        if not isinstance(data, dict):
            raise ValueError("Expected a JSON object")
        return StructuredAnswer(
            explanation=str(data.get("explanation", "")),
            example=str(data.get("example", "")),
            key_insights=[str(item) for item in data.get("key_insights", [])],
            is_structured=True,
        )
    except (json.JSONDecodeError, TypeError, ValueError):
        return StructuredAnswer(
            explanation=raw_response.strip(),
            example="",
            key_insights=[],
            is_structured=False,
        )
