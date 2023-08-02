from aicodebot.lm import LanguageModelManager, get_token_size


def test_choose_model():
    # Simple test for now. Upcoming commit will walk through a bunch of different model scenarios
    lmm = LanguageModelManager()
    model_name = lmm.choose_model(100)
    assert model_name in LanguageModelManager.openai_supported_engines()


def test_get_token_length():
    assert LanguageModelManager.get_token_length("") == 0

    text = "Code with heart, align AI with humanity. ❤️🤖"
    assert LanguageModelManager.get_token_length(text) == 14
    assert get_token_size(text) == 14
