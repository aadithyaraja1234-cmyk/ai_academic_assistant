from dataclasses import dataclass

from llm_layer import call_llm
from post_processing import clean_output
from prompt_layer import build_prompt
from schemas import StructuredAnswer


@dataclass
class PipelineResult:
    answer: StructuredAnswer
    latency_ms: float
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None


def run_pipeline(user_input: str) -> PipelineResult:
    prompt = build_prompt(user_input)
    llm_result = call_llm(prompt)
    answer = clean_output(llm_result.content)
    return PipelineResult(
        answer=answer,
        latency_ms=llm_result.latency_ms,
        prompt_tokens=llm_result.prompt_tokens,
        completion_tokens=llm_result.completion_tokens,
        total_tokens=llm_result.total_tokens,
    )
