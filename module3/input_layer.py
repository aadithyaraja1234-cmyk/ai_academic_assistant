def get_user_input() -> str:
    """Prompt the user for a question on stdin.

    Used by cli.py so the pipeline can be exercised without Streamlit.
    """
    return input("Ask your question: ")
