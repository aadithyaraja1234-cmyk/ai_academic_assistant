SYSTEM_PROMPT = """" 
Your are an AI Academic Assistant
Provide structured and concise answers
Avoid hallucinations
"""
def build_prompt(user_input):
    return f"""
Answer the question clearly.

QUestion;
{user_input}

Provide:
-Clear explanation
-Example
-key insights
"""