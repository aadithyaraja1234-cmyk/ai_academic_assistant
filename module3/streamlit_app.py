import streamlit as st
from pipeline import run_pipeline

st.set_page_config(
    page_title="AI Academic Assistant",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Academic Assistant")
st.markdown("Ask academic questions and receive structured answers.")

user_input = st.text_area("Enter your question:", height=150)

if st.button("Generate Answer"):

    if not user_input.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating response..."):
            try:
                response = run_pipeline(user_input)
                st.success("Response Generated!")
                st.markdown("---")
                st.markdown(response)
            except Exception as e:
                st.error(f"Error: {str(e)}")