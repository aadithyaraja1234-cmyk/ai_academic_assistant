import os
from dotenv import load_dotenv
from litellm import completion
from prompt_layer import SYSTEM_PROMPT

import streamlit as st

MODEL_NAME = st.secrets["MODEL_NAME"]
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

def call_llm(prompt):
    response = completion(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=700
    )


    return response["choices"][0]["message"]["content"]
