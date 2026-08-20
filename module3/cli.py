"""Command-line entry point for the AI Academic Assistant.

Runs the same prompt -> LLM -> post-processing pipeline used by the
Streamlit UI, without requiring Streamlit. Useful for local testing and
for demonstrating that the pipeline is decoupled from the UI layer.

Usage:
    python cli.py
"""
from input_layer import get_user_input
from pipeline import PipelineResult, run_pipeline


def render(result: PipelineResult) -> str:
    answer = result.answer
    lines = [f"Explanation:\n{answer.explanation or '-'}"]

    if answer.example:
        lines.append(f"\nExample:\n{answer.example}")

    if answer.key_insights:
        bullets = "\n".join(f"- {insight}" for insight in answer.key_insights)
        lines.append(f"\nKey Insights:\n{bullets}")

    if not answer.is_structured:
        lines.append("\n[Note: model did not return structured JSON; showing raw text.]")

    lines.append(f"\n[latency: {result.latency_ms:.0f} ms]")
    return "\n".join(lines)


def main() -> None:
    question = get_user_input()
    if not question.strip():
        print("No question provided.")
        return

    try:
        result = run_pipeline(question)
    except ValueError as exc:
        print(f"Invalid input: {exc}")
        return
    except RuntimeError as exc:
        print(f"Request failed: {exc}")
        return

    print(render(result))


if __name__ == "__main__":
    main()
