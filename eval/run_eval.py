"""Run the assistant against a fixed question set (questions.json) and
score structural compliance, completeness, latency, and token cost.

This makes real, billed calls to the Groq API - it requires a valid
GROQ_API_KEY (see ../.env.example / ../module3/.env). It is intentionally
kept separate from the pytest suite, which mocks the LLM call so it can
run for free in CI.

Usage:
    python eval/run_eval.py
"""
import json
import statistics
import sys
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EVAL_DIR.parent / "module3"))

from pipeline import run_pipeline  # noqa: E402

QUESTIONS_PATH = EVAL_DIR / "questions.json"
RESULTS_PATH = EVAL_DIR / "results.json"
REPORT_PATH = EVAL_DIR / "REPORT.md"


def evaluate_question(q: dict) -> dict:
    row = {
        "id": q["id"],
        "subject": q["subject"],
        "difficulty": q["difficulty"],
        "question": q["question"],
        "is_structured": False,
        "is_complete": False,
        "latency_ms": None,
        "prompt_tokens": None,
        "completion_tokens": None,
        "total_tokens": None,
        "error": None,
    }
    try:
        result = run_pipeline(q["question"])
    except Exception as exc:  # noqa: BLE001 - record and keep going
        row["error"] = str(exc)
        return row

    answer = result.answer
    row.update(
        is_structured=answer.is_structured,
        is_complete=answer.is_complete,
        latency_ms=result.latency_ms,
        prompt_tokens=result.prompt_tokens,
        completion_tokens=result.completion_tokens,
        total_tokens=result.total_tokens,
    )
    return row


def summarize(rows: list[dict]) -> dict:
    n = len(rows)
    ok = [r for r in rows if r["error"] is None]
    latencies = [r["latency_ms"] for r in ok if r["latency_ms"] is not None]
    tokens = [r["total_tokens"] for r in ok if r["total_tokens"] is not None]

    return {
        "n_questions": n,
        "n_errors": n - len(ok),
        "structured_rate_pct": round(sum(r["is_structured"] for r in ok) / n * 100, 1) if n else 0.0,
        "complete_rate_pct": round(sum(r["is_complete"] for r in ok) / n * 100, 1) if n else 0.0,
        "median_latency_ms": round(statistics.median(latencies), 0) if latencies else None,
        "max_latency_ms": round(max(latencies), 0) if latencies else None,
        "median_total_tokens": round(statistics.median(tokens), 0) if tokens else None,
    }


def write_report(rows: list[dict], summary: dict) -> None:
    lines = [
        "# Evaluation Report",
        "",
        f"- Questions evaluated: {summary['n_questions']}",
        f"- Failed calls: {summary['n_errors']}",
        f"- Valid JSON / structured-output rate: {summary['structured_rate_pct']}%",
        f"- Fully complete (explanation + example + insights) rate: {summary['complete_rate_pct']}%",
        f"- Median latency: {summary['median_latency_ms']} ms",
        f"- Max latency: {summary['max_latency_ms']} ms",
        f"- Median total tokens/response: {summary['median_total_tokens']}",
        "",
        "| ID | Subject | Difficulty | Structured | Complete | Latency (ms) | Tokens |",
        "|---|---|---|---|---|---|---|",
    ]

    for r in rows:
        latency = f"{r['latency_ms']:.0f}" if r["latency_ms"] is not None else "-"
        tokens = r["total_tokens"] if r["total_tokens"] is not None else "-"
        structured = "yes" if r["is_structured"] else "no"
        complete = "yes" if r["is_complete"] else "no"
        lines.append(
            f"| {r['id']} | {r['subject']} | {r['difficulty']} | "
            f"{structured} | {complete} | {latency} | {tokens} |"
        )
        if r["error"]:
            lines.append(f"|  |  |  | ERROR: {r['error']} |  |  |  |")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    questions = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))

    rows = []
    for q in questions:
        print(f"[{q['id']}] {q['question'][:70]}")
        rows.append(evaluate_question(q))

    summary = summarize(rows)
    RESULTS_PATH.write_text(json.dumps({"summary": summary, "rows": rows}, indent=2), encoding="utf-8")
    write_report(rows, summary)

    print("\n--- Summary ---")
    for key, value in summary.items():
        print(f"{key}: {value}")
    print(f"\nWrote {RESULTS_PATH} and {REPORT_PATH}")


if __name__ == "__main__":
    main()
