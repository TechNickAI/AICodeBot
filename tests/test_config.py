import pytest
import yaml

from aicodebot.config import (
    Session,
    detect_api_keys,
    fetch_anthropic_models,
    fetch_models_for_provider,
    fetch_openai_models,
    read_config,
)


def test_session_read_write(tmp_path, monkeypatch):
    monkeypatch.setenv("AICODEBOT_SESSION_FILE", str(tmp_path / "session.yaml"))

    assert not Session.get_config_file().exists()

    # Test write
    test_data = {"key": "value"}
    Session.write(test_data)

    # Check that the file was written correctly
    assert Session.get_config_file().exists()

    # Test read
    read_data = Session.read()
    assert read_data == test_data


def test_detect_api_keys_with_valid_keys(monkeypatch):
    """Test detecting valid API keys from environment variables."""
    # Set up environment variables
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test123")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test456")

    detected = detect_api_keys()

    assert "openai" in detected
    assert detected["openai"]["key"] == "sk-test123"
    assert detected["openai"]["source"] == "environment"

    assert "anthropic" in detected
    assert detected["anthropic"]["key"] == "sk-ant-test456"
    assert detected["anthropic"]["source"] == "environment"


def test_detect_api_keys_with_invalid_keys(monkeypatch):
    """Test that invalid API key formats are not detected."""
    # Set up invalid API keys
    monkeypatch.setenv("OPENAI_API_KEY", "invalid-key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "also-invalid")

    detected = detect_api_keys()

    # Should be empty since keys don't match expected formats
    assert detected == {}


def test_detect_api_keys_no_keys(monkeypatch):
    """Test detecting when no API keys are set."""
    # Remove any existing API keys
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    detected = detect_api_keys()

    assert detected == {}


def test_detect_api_keys_partial(monkeypatch):
    """Test detecting when only one API key is set."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test123")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    detected = detect_api_keys()

    assert "openai" in detected
    assert "anthropic" not in detected


@pytest.mark.asyncio
async def test_fetch_openai_models():
    """Test that OpenAI models are returned correctly."""
    models = await fetch_openai_models("dummy-key")

    # Should return the hardcoded list
    assert len(models) == 4
    assert any(model["id"] == "gpt-5" for model in models)
    assert any(model["id"] == "o3-pro" for model in models)

    # Check structure
    for model in models:
        assert "id" in model
        assert "name" in model
        assert "description" in model


@pytest.mark.asyncio
async def test_fetch_anthropic_models():
    """Test that Anthropic models are returned correctly."""
    models = await fetch_anthropic_models("dummy-key")

    # Should return the hardcoded list
    assert len(models) == 4
    assert any(model["id"] == "claude-opus-4-1" for model in models)
    assert any(model["id"] == "claude-sonnet-4-0" for model in models)

    # Check structure
    for model in models:
        assert "id" in model
        assert "name" in model
        assert "description" in model


@pytest.mark.asyncio
async def test_fetch_models_for_provider_openai():
    """Test fetching models for OpenAI provider."""
    models = await fetch_models_for_provider("openai", "dummy-key")

    assert len(models) > 0
    assert any(model["id"] == "gpt-5" for model in models)


@pytest.mark.asyncio
async def test_fetch_models_for_provider_anthropic():
    """Test fetching models for Anthropic provider."""
    models = await fetch_models_for_provider("anthropic", "dummy-key")

    assert len(models) > 0
    assert any(model["id"] == "claude-opus-4-1" for model in models)


@pytest.mark.asyncio
async def test_fetch_models_for_provider_case_insensitive():
    """Test that provider names are case insensitive."""
    openai_models = await fetch_models_for_provider("OpenAI", "dummy-key")
    anthropic_models = await fetch_models_for_provider("ANTHROPIC", "dummy-key")

    assert len(openai_models) > 0
    assert len(anthropic_models) > 0


@pytest.mark.asyncio
async def test_fetch_models_for_provider_invalid():
    """Test error handling for invalid provider."""
    with pytest.raises(ValueError, match="Unknown provider"):
        await fetch_models_for_provider("invalid", "dummy-key")


def test_read_config_new_format(tmp_path, monkeypatch):
    """Test reading config file with new v1.3 format."""
    config_file = tmp_path / "config.yaml"
    config_data = {
        "version": 1.3,
        "provider": "openai",
        "model": "gpt-5",
        "personality": "Einstein",
        "openai_api_key": "sk-test123",
    }

    # Write config file
    with config_file.open("w") as f:
        yaml.dump(config_data, f)

    # Mock the config file path
    monkeypatch.setenv("AICODEBOT_CONFIG_FILE", str(config_file))
    monkeypatch.setenv("AICODEBOT_SESSION_FILE", str(tmp_path / "session.yaml"))

    config = read_config()

    assert config["version"] == 1.3
    assert config["provider"] == "openai"
    assert config["model"] == "gpt-5"
    assert config["personality"] == "Einstein"
    assert config["openai_api_key"] == "sk-test123"
    assert "session" in config  # Session data should be loaded


def test_read_config_nonexistent(tmp_path, monkeypatch):
    """Test reading config file that doesn't exist."""
    nonexistent_file = tmp_path / "nonexistent.yaml"
    monkeypatch.setenv("AICODEBOT_CONFIG_FILE", str(nonexistent_file))

    config = read_config()

    assert config is None


def test_read_config_legacy_format(tmp_path, monkeypatch):
    """Test reading config file with legacy format."""
    config_file = tmp_path / "config.yaml"
    config_data = {"language_model_provider": "OpenAI", "language_model": "gpt-4", "openai_api_key": "sk-legacy123"}

    # Write config file
    with config_file.open("w") as f:
        yaml.dump(config_data, f)

    # Mock the config file path
    monkeypatch.setenv("AICODEBOT_CONFIG_FILE", str(config_file))
    monkeypatch.setenv("AICODEBOT_SESSION_FILE", str(tmp_path / "session.yaml"))

    config = read_config()

    assert config["language_model_provider"] == "OpenAI"
    assert config["language_model"] == "gpt-4"
    assert config["openai_api_key"] == "sk-legacy123"
    assert "session" in config  # Session data should be loaded
