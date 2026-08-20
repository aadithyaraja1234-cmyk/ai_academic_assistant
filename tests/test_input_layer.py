from unittest.mock import patch

from input_layer import get_user_input


def test_get_user_input_returns_stdin_text():
    with patch("builtins.input", return_value="What is gravity?") as mock_input:
        result = get_user_input()

    mock_input.assert_called_once_with("Ask your question: ")
    assert result == "What is gravity?"
