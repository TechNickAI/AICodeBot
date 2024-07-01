from aicodebot.lm import LanguageModelManager, token_size
from pathlib import Path
import os, pytest


def test_token_size(monkeypatch):
    monkeypatch.setenv("AICODEBOT_CONFIG_FILE", str(Path(__file__).parent / "test_config.yaml"))
    assert token_size("") == 0

    text = "Code with heart, align AI with humanity. ❤️🤖"
    assert LanguageModelManager().get_token_size(text) == 12
    assert token_size(text) == 12


@pytest.mark.parametrize(
    "provider,model_name",
    [
        (LanguageModelManager.OPENAI, "gpt-4"),
        (LanguageModelManager.OPENAI, "gpt-3.5-turbo"),
        (LanguageModelManager.ANTHROPIC, "claude-3-5-sonnet-20240620"),
    ],
)
def test_model_factory(provider, model_name, monkeypatch):
    monkeypatch.setenv("AICODEBOT_MODEL_PROVIDER", provider)
    monkeypatch.setenv("AICODEBOT_MODEL", model_name)
    monkeypatch.setenv("OPENROUTER_API_KEY", "dummy")
    monkeypatch.setenv("OPENAI_API_KEY", "dummy")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "dummy")

    lmm = LanguageModelManager()
    assert os.getenv("OPENROUTER_API_KEY") == "dummy"
    assert lmm.get_api_key("OPENROUTER_API_KEY") == "dummy"

    llm = lmm.model_factory()
    if hasattr(llm, "model"):
        assert llm.model == model_name
    else:
        assert llm.model_name == model_name
