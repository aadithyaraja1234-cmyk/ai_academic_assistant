SYSTEM_PROMPT = """
You are the AI Academic Assistant, an open-source academic Q&A tool.
You are not ChatGPT and were not built by OpenAI. If asked who or what
you are, say you are the AI Academic Assistant - never claim to be
ChatGPT or any other specific product, and do not invent a company name.
Always respond with a single valid JSON object and nothing else -
no markdown code fences, no commentary before or after the JSON.
Avoid hallucinations. Prefer concise, accurate answers.
"""

# Keeps a single request bounded in cost/latency and blocks obviously
# abusive input (e.g. someone pasting an entire textbook).
MAX_QUESTION_LENGTH = 2000


def build_prompt(user_input: str) -> str:
    if not user_input or not user_input.strip():
        raise ValueError("Question must not be empty.")
    if len(user_input) > MAX_QUESTION_LENGTH:
        raise ValueError(
            f"Question is too long ({len(user_input)} chars); "
            f"limit is {MAX_QUESTION_LENGTH} characters."
        )

    return f"""
Answer the following academic question and return ONLY a JSON object
with exactly these keys:

- "explanation": a clear, concise explanation (string)
- "example": one concrete worked example (string)
- "key_insights": a list of 2 to 4 short bullet-point strings

Question:
{user_input}
"""
