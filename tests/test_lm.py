from aicodebot.lm import LanguageModelManager, token_size
from aicodebot.prompts import get_prompt
import pytest


def test_token_size():
    assert token_size("") == 0

    text = "Code with heart, align AI with humanity. ❤️🤖"
    assert LanguageModelManager().get_token_size(text) == 14
    assert token_size(text) == 14


@pytest.mark.parametrize("provider,model_name", [("OpenAI", "gpt-4"), ("OpenRouter", "gpt-4")])
def test_chain_factory(provider, model_name, monkeypatch):
    monkeypatch.setenv("AICODEBOT_MODEL_PROVIDER", provider)
    monkeypatch.setenv("AICODEBOT_MODEL", model_name)
    monkeypatch.setenv("OPENROUTER_API_KEY", "dummy")
    monkeypatch.setenv("OPENAI_API_KEY", "dummy")
    llm = LanguageModelManager()
    prompt = get_prompt("alignment")
    chain = llm.chain_factory(prompt)
