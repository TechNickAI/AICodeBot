from aicodebot.llm import LLM


def test_get_token_length():
    text = ""
    assert LLM.get_token_length(text) == 0

    text = "Code with heart, align AI with humanity. ❤️🤖"
    assert LLM.get_token_length(text) == 14
