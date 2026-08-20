import logging
import os
import time
from dataclasses import dataclass

from dotenv import load_dotenv
from litellm import completion

from prompt_layer import SYSTEM_PROMPT

# Load GROQ_API_KEY / MODEL_NAME from a local .env file when present.
# This is a no-op (and harmless) when the file doesn't exist, e.g. on
# Streamlit Cloud where secrets are injected as environment variables.
load_dotenv()

logger = logging.getLogger(__name__)

MAX_RETRIES = 2
RETRY_BACKOFF_SECONDS = 1.5


@dataclass
class LLMResult:
    content: str
    latency_ms: float
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None


def _resolve_config() -> str:
    """Resolve the model name and API key.

    Environment variables (populated via .env locally, or Streamlit Cloud
    secrets in production) are the single source of truth. This keeps
    this module importable and testable outside of a running Streamlit
    app, unlike reading st.secrets at import time.
    """
    model_name = os.getenv("MODEL_NAME")
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not model_name or not groq_api_key:
        try:
            import streamlit as st

            model_name = model_name or st.secrets.get("MODEL_NAME")
            groq_api_key = groq_api_key or st.secrets.get("GROQ_API_KEY")
        except Exception:
            pass

    if not groq_api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to a local .env file "
            "(see .env.example) or to Streamlit secrets."
        )
    if not model_name:
        raise RuntimeError(
            "MODEL_NAME is not set. Add it to a local .env file "
            "(see .env.example) or to Streamlit secrets, "
            "e.g. groq/llama-3.1-8b-instant."
        )

    os.environ["GROQ_API_KEY"] = groq_api_key
    return model_name


def call_llm(prompt: str) -> LLMResult:
    """Call the LLM, retrying on transient failures (rate limits, timeouts,
    flaky network) with a short linear backoff before giving up.
    """
    model_name = _resolve_config()

    last_error: Exception | None = None
    for attempt in range(MAX_RETRIES + 1):
        start = time.perf_counter()
        try:
            response = completion(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
                max_tokens=700,
            )
        except Exception as exc:  # noqa: BLE001 - retry any transient API error
            last_error = exc
            logger.warning(
                "LLM call attempt %d/%d failed: %s", attempt + 1, MAX_RETRIES + 1, exc
            )
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF_SECONDS * (attempt + 1))
            continue

        latency_ms = (time.perf_counter() - start) * 1000
        usage = getattr(response, "usage", None)
        return LLMResult(
            content=response["choices"][0]["message"]["content"],
            latency_ms=latency_ms,
            prompt_tokens=getattr(usage, "prompt_tokens", None),
            completion_tokens=getattr(usage, "completion_tokens", None),
            total_tokens=getattr(usage, "total_tokens", None),
        )

    logger.error("LLM call failed after %d attempt(s): %s", MAX_RETRIES + 1, last_error)
    raise RuntimeError(
        f"LLM call failed after {MAX_RETRIES + 1} attempt(s): {last_error}"
    ) from last_error
