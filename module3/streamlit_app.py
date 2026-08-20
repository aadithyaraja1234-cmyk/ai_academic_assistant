import streamlit as st

from pdf_export import build_pdf
from pipeline import run_pipeline
from prompt_layer import MAX_QUESTION_LENGTH

st.set_page_config(
    page_title="AI Academic Assistant",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 AI Academic Assistant")
st.markdown("Ask academic questions and receive structured answers.")

user_input = st.text_area(
    "Enter your question:",
    height=150,
    max_chars=MAX_QUESTION_LENGTH,
)

if st.button("Generate Answer"):
    if not user_input.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating response..."):
            try:
                result = run_pipeline(user_input)
            except Exception as e:
                st.error(f"Error: {e}")
            else:
                st.success("Response generated!")
                st.markdown("---")

                answer = result.answer
                if not answer.is_structured:
                    st.info(
                        "The model didn't return structured JSON this time; "
                        "showing the raw answer below."
                    )

                st.subheader("Explanation")
                st.markdown(answer.explanation or "_No explanation returned._")

                if answer.example:
                    st.subheader("Example")
                    st.markdown(answer.example)

                if answer.key_insights:
                    st.subheader("Key Insights")
                    for insight in answer.key_insights:
                        st.markdown(f"- {insight}")

                with st.expander("Response metadata"):
                    st.write(
                        {
                            "latency_ms": round(result.latency_ms, 1),
                            "prompt_tokens": result.prompt_tokens,
                            "completion_tokens": result.completion_tokens,
                            "total_tokens": result.total_tokens,
                        }
                    )

                st.download_button(
                    "Download as PDF",
                    data=build_pdf(user_input, answer),
                    file_name="academic_answer.pdf",
                    mime="application/pdf",
                )

st.markdown("---")
with st.expander("Privacy & data handling"):
    st.markdown(
        "Your question is sent to Groq's LLM API to generate a response and "
        "is not stored by this app or logged anywhere. No accounts, cookies, "
        "or personal data are collected. See Groq's own "
        "[privacy policy](https://groq.com/privacy-policy/) for how they "
        "handle API requests."
    )
st.caption(
    "Built by Aadithya Raja Anil · "
    "[Source on GitHub](https://github.com/aadithyaraja1234-cmyk/ai_academic_assistant)"
)
