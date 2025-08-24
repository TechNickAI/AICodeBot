import tiktoken
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from aicodebot.config import read_config
from aicodebot.helpers import logger

DEFAULT_RESPONSE_TOKENS = 1_000
DEFAULT_MEMORY_TOKENS = DEFAULT_RESPONSE_TOKENS * 2
DEFAULT_CONTEXT_TOKENS = DEFAULT_RESPONSE_TOKENS * 4
PRECISE_TEMPERATURE = 0.05
CREATIVE_TEMPERATURE = 0.6


class LanguageModelManager:
    """A class for interacting with language models."""

    provider = model_name = None

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    PROVIDERS = [OPENAI, ANTHROPIC]
    DEFAULT_MODEL = "gpt-5"
    DEFAULT_PROVIDER = OPENAI

    def __init__(self, model_name=None, provider=None):
        self.model_name = model_name
        self.provider = provider
        if not self.model_name:
            self.read_model_config()

    # --------------------------------- Factories -------------------------------- #

    def model_factory(
        self,
        response_token_size=DEFAULT_RESPONSE_TOKENS,
        temperature=PRECISE_TEMPERATURE,
        streaming=False,
        callbacks=None,
    ):
        """Get a model object for the specified model name."""

        provider, model_name = self.read_model_config()

        if provider == self.OPENAI:
            api_key = self.get_api_key("OPENAI_API_KEY")

            return ChatOpenAI(
                openai_api_key=api_key,
                model=model_name,
                max_tokens=response_token_size,
                temperature=temperature,
                streaming=streaming,
                callbacks=callbacks,
            )
        elif provider == self.ANTHROPIC:
            api_key = self.get_api_key("ANTHROPIC_API_KEY")
            return ChatAnthropic(
                api_key=api_key,
                model=model_name,
                max_tokens=response_token_size,
                temperature=temperature,
                streaming=streaming,
                callbacks=callbacks,
            )
        else:  # pragma: no cover
            raise ValueError(f"Provider {provider} is not one of: {self.PROVIDERS}")

    def get_api_key(self, key_name):
        # Read the API key from the config file only (environment variables only used during initial setup)
        config = read_config() or {}
        key_name_upper = key_name.upper()
        key_name_lower = key_name.lower()

        # Try provider-specific keys first (new format)
        if key_name_upper == "OPENAI_API_KEY":
            return config.get("openai_api_key") or config.get("OPENAI_API_KEY") or config.get(key_name_lower)
        elif key_name_upper == "ANTHROPIC_API_KEY":
            return config.get("anthropic_api_key") or config.get("ANTHROPIC_API_KEY") or config.get(key_name_lower)
        else:
            # Legacy fallback
            return config.get(key_name_lower) or config.get(key_name_upper)

    def get_model_token_limit(self, model_name):
        model_token_limits = {
            "claude-3": 200_000,
            "gpt-4": 8192,
            "gpt-4-32k": 32768,
            "gpt-3.5-turbo-16k": 16384,
        }
        if model_name in model_token_limits:
            return model_token_limits[model_name]
        else:
            raise ValueError(f"Model {model_name} not found")

    def get_token_size(self, text):
        """Get the number of tokens in a string using the tiktoken library."""
        encoding = tiktoken.encoding_for_model(self.tiktoken_model_name)
        tokens = encoding.encode(text)
        return len(tokens)

    def read_model_config(self):
        # Figure out which model to use, based on the configuration file or environment variables
        config = read_config() or {}

        # Check for new config format first (v1.3+)
        if config.get("version", 0) >= 1.3 and "provider" in config and "model" in config:
            # Use the new dynamic configuration
            self.provider = config["provider"].lower()
            self.model_name = config["model"]
            logger.debug(f"Using configured provider: {self.provider}, model: {self.model_name}")

        else:
            # Legacy config fallback (no environment variable detection)
            logger.debug("Using legacy configuration")
            self.provider = config.get("language_model_provider", self.DEFAULT_PROVIDER)

            # Set default models for legacy configs
            if self.provider == self.OPENAI:
                self.model_name = config.get("language_model", "gpt-4o")
            elif self.provider == self.ANTHROPIC:
                self.model_name = config.get("language_model", "claude-3-5-sonnet-20241022")
            else:
                self.model_name = config.get("language_model", self.DEFAULT_MODEL)

        # --------------------------- API key verification --------------------------- #
        if self.provider == self.OPENAI:
            key_name = "OPENAI_API_KEY"
        elif self.provider == self.ANTHROPIC:
            key_name = "ANTHROPIC_API_KEY"
        else:
            valid_providers = [self.OPENAI, self.ANTHROPIC]
            raise ValueError(f"Unrecognized provider: {self.provider}. Valid options are: {valid_providers}")

        if not self.get_api_key(key_name):
            raise ValueError(
                f"In order to use {self.provider}, you must set the API key in your config file.\n"
                f"Run 'aicodebot configure' to set up your configuration."
            )

        return self.provider, self.model_name

    @property
    def tiktoken_model_name(self):
        # This seems to work for both OpenAI and Anthropic
        return "gpt-4o"

    def use_appropriate_sized_model(self, chain, token_size):
        current_model = self.model_name
        gpt_4_limit = self.get_model_token_limit("gpt-4") * 0.9
        gpt_4_32k_limit = self.get_model_token_limit("gpt-4-32k") * 0.9
        if current_model in ["gpt-4", "gpt-4-32k"]:
            if token_size > gpt_4_32k_limit:
                raise ValueError("Token limit exceeded for GPT4, try using less context (files)")
            elif token_size > gpt_4_limit:
                self.model_name = "gpt-4-32k"
            else:
                self.model_name = "gpt-4"

        elif current_model in ["gpt-3.5-turbo", "gpt-3.5-turbo-16k"]:
            gpt_3_limit = self.get_model_token_limit("gpt-3.5-turbo") * 0.9
            gpt_3_16k_limit = self.get_model_token_limit("gpt-3.5-turbo-16k") * 0.9
            if token_size > gpt_3_16k_limit:
                raise ValueError("Token limit exceeded for GPT3.5, try using less context (files)")
            elif token_size > gpt_3_limit:
                self.model_name = "gp-3.5-turbo-16k"
            else:
                self.model_name = "gpt-3.5-turbo"

        if current_model != self.model_name:
            logger.trace(f"Switching from {current_model} to {self.model_name} to handle the context size.")
            chain.llm.model_name = self.model_name

        return current_model, self.model_name


def token_size(text):
    # Shortcut
    return LanguageModelManager().get_token_size(text)
