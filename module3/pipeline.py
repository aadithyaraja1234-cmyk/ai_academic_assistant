from prompt_layer import build_prompt
from llm_layer import call_llm
from post_processing import clean_output

def run_pipeline(user_input):
    prompt = build_prompt(user_input)
    raw_output = call_llm(prompt)
    final_output = clean_output(raw_output)
    return final_output