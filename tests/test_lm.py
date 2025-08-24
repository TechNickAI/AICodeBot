from pathlib import Path

from aicodebot.lm import LanguageModelManager, token_size


def test_token_size(monkeypatch):
    monkeypatch.setenv("AICODEBOT_CONFIG_FILE", str(Path(__file__).parent / "test_config.yaml"))
    assert token_size("") == 0

    text = "Code with heart, align AI with humanity. ❤️🤖"
    assert LanguageModelManager().get_token_size(text) == 12
    assert token_size(text) == 12
