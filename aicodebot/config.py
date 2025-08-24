import os
from pathlib import Path

import yaml

from aicodebot.helpers import create_and_write_file, logger


def get_local_data_dir():
    data_dir = Path(os.getenv("AICODEBOT_LOCAL_DATA_DIR", str(Path.home() / ".aicodebot")))
    # Make the directory if it doesn't exist
    if not data_dir.exists():
        logger.debug(f"Creating local data directory {data_dir}")
        data_dir.mkdir()
        # Create the subdirectories
        (data_dir / "repos").mkdir()
        (data_dir / "vector_stores").mkdir()

    return data_dir


def get_config_file():
    return Path(os.getenv("AICODEBOT_CONFIG_FILE", get_local_data_dir() / "config.yaml"))


def read_config():
    """Read the config file and return its contents as a dictionary."""
    config_file = get_config_file()
    logger.debug(f"Using config file {config_file}")
    if config_file.exists():
        logger.debug(f"Config file {config_file} exists")
        with Path(config_file).open("r") as f:
            out = yaml.safe_load(f)

            # Load the session data
            out["session"] = Session.read()
            return out
    else:
        logger.debug(f"Config file {config_file} does not exist")
        return None


def detect_api_keys():
    """Detect existing API keys from environment variables."""
    detected_keys = {}

    # Check for OpenAI API key
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and openai_key.startswith("sk-"):
        detected_keys["openai"] = {"key": openai_key, "source": "environment"}

    # Check for Anthropic API key
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key and anthropic_key.startswith("sk-ant-"):
        detected_keys["anthropic"] = {"key": anthropic_key, "source": "environment"}

    return detected_keys


async def fetch_openai_models(api_key):  # noqa: ARG001 - api_key needed for interface consistency
    """Return latest OpenAI models."""
    # Return the latest/upcoming OpenAI models (hardcoded list for cutting-edge access)
    return [
        {"id": "gpt-5", "name": "gpt-5", "description": "GPT-5 (Next-generation flagship model)"},
        {"id": "gpt-5-mini", "name": "gpt-5-mini", "description": "GPT-5 Mini (Fast and efficient next-gen)"},
        {"id": "gpt-oss-120b", "name": "gpt-oss-120b", "description": "GPT-OSS 120B (Open source model)"},
        {"id": "o3-pro", "name": "o3-pro", "description": "O3 Pro (Advanced reasoning model)"},
    ]


async def fetch_anthropic_models(api_key):  # noqa: ARG001 - api_key needed for interface consistency
    """Fetch available models from Anthropic API."""
    # Note: Anthropic doesn't have a public models API endpoint like OpenAI
    # Return the latest available models from official docs (January 2025)
    # Source: https://docs.anthropic.com/en/docs/about-claude/models/overview
    return [
        {
            "id": "claude-opus-4-1",
            "name": "claude-opus-4-1",
            "description": "Claude Opus 4.1 (Most capable and intelligent - Latest flagship)",
        },
        {
            "id": "claude-sonnet-4-0",
            "name": "claude-sonnet-4-0",
            "description": "Claude Sonnet 4 (High-performance with exceptional reasoning)",
        },
        {
            "id": "claude-3-7-sonnet-latest",
            "name": "claude-3-7-sonnet-latest",
            "description": "Claude Sonnet 3.7 (High-performance with extended thinking)",
        },
        {
            "id": "claude-3-5-haiku-latest",
            "name": "claude-3-5-haiku-latest",
            "description": "Claude Haiku 3.5 (Fastest model with intelligence)",
        },
    ]


async def fetch_models_for_provider(provider, api_key):
    """Fetch models for a specific provider."""
    if provider.lower() == "openai":
        return await fetch_openai_models(api_key)
    elif provider.lower() == "anthropic":
        return await fetch_anthropic_models(api_key)
    else:
        raise ValueError(f"Unknown provider: {provider}")


class Session:
    """Read and write local session data"""

    @classmethod
    def get_config_file(cls):
        return Path(os.getenv("AICODEBOT_SESSION_FILE", str(get_local_data_dir() / "session.yaml")))

    @classmethod
    def read(cls):
        """Read the session file and return its contents as a dictionary."""
        session_file = cls.get_config_file()
        logger.debug(f"Using session file {session_file}")
        if session_file.exists():
            logger.debug(f"Session file {session_file} exists")
            with Path(session_file).open("r") as f:
                return yaml.safe_load(f)
        else:
            logger.debug(f"Session file {session_file} does not exist")
            return {}

    @classmethod
    def write(cls, session_data):
        session_file = cls.get_config_file()
        logger.debug(f"Writing session data to {session_file}")
        data = yaml.safe_dump(session_data)
        create_and_write_file(session_file, data, overwrite=True)
