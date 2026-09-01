import json
import logging
import re

from json_repair import repair_json

from schemas import StructuredAnswer

logger = logging.getLogger(__name__)

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


def _to_answer(data: dict) -> StructuredAnswer:
    return StructuredAnswer(
        explanation=str(data.get("explanation", "")),
        example=str(data.get("example", "")),
        key_insights=[str(item) for item in data.get("key_insights", [])],
        is_structured=True,
    )


def clean_output(raw_response: str) -> StructuredAnswer:
    """Parse the raw LLM response into a validated StructuredAnswer.

    Three-tier strategy, each stage only reached if the previous one fails:
    1. Strict `json.loads` - the fast, common path for well-formed JSON.
    2. `json_repair` - recovers real-world malformations seen in
       production, notably unescaped quotes inside string values (e.g. a
       model quoting example dialogue) and smart quotes/missing brackets
       from a truncated-looking response.
    3. Unstructured fallback (`is_structured=False`, raw text as
       `explanation`) - so the app degrades gracefully instead of
       crashing when the response isn't recoverable at all.
    """
    candidate = _extract_json(raw_response)

    try:
        data = json.loads(candidate)
        if not isinstance(data, dict):
            raise ValueError("Expected a JSON object")
        return _to_answer(data)
    except (json.JSONDecodeError, TypeError, ValueError):
        pass

    try:
        repaired = repair_json(candidate, return_objects=True)
        if isinstance(repaired, dict) and repaired.get("explanation"):
            logger.warning("Recovered malformed JSON from LLM response via json_repair")
            return _to_answer(repaired)
    except Exception as exc:  # noqa: BLE001 - repair is best-effort, never fatal
        logger.warning("json_repair failed on LLM response: %s", exc)

    return StructuredAnswer(
        explanation=raw_response.strip(),
        example="",
        key_insights=[],
        is_structured=False,
    )
