from aicodebot.config import read_config
from aicodebot.helpers import logger
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
import os, tiktoken

DEFAULT_RESPONSE_TOKENS = 1_000
DEFAULT_MEMORY_TOKENS = DEFAULT_RESPONSE_TOKENS * 2
DEFAULT_CONTEXT_TOKENS = DEFAULT_RESPONSE_TOKENS * 4
PRECISE_TEMPERATURE = 0.05
CREATIVE_TEMPERATURE = 0.6


class LanguageModelManager:
    """A class for interacting with language models."""

    provider = model_name = None

    OPENAI = "OpenAI"
    ANTHROPIC = "Anthropic"
    PROVIDERS = [OPENAI, ANTHROPIC]
    DEFAULT_MODEL = "gpt-4o"
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
        # Read the api key from either the environment or the config file
        key_name_upper = key_name.upper()
        api_key = os.getenv(key_name_upper)
        if api_key:
            return api_key
        else:
            config = read_config() or {}
            key_name_lower = key_name.lower()
            # Try both upper and lower case from the config file
            if key_name_lower in config:
                return config[key_name_lower]
            elif key_name_upper in config:
                return config[key_name_upper]
            else:
                return None

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
        # Figure out which model to use, based on the environment variables or config file
        config = read_config() or {}
        self.provider = (
            (os.getenv("ANTHROPIC_API_KEY") and self.ANTHROPIC)
            or (os.getenv("OPENAI_API_KEY") and self.OPENAI)
            or os.getenv("AICODEBOT_MODEL_PROVIDER", config.get("language_model_provider", self.DEFAULT_PROVIDER))
        )

        if self.provider == self.OPENAI:
            self.model_name = "gpt-4o"
        elif self.provider == self.ANTHROPIC:
            self.model_name = "claude-3-5-sonnet-latest"
        else:
            self.model_name = os.getenv("AICODEBOT_MODEL", config.get("language_model", self.DEFAULT_MODEL))

        # --------------------------- API key verification --------------------------- #
        if self.provider == self.OPENAI:
            key_name = "OPENAI_API_KEY"
        elif self.provider == self.ANTHROPIC:
            key_name = "ANTHROPIC_API_KEY"
        else:
            raise ValueError(f"Unrecognized provider: {self.provider}")

        if not self.get_api_key(key_name):
            raise ValueError(
                f"In order to use {self.provider}, you must set the {key_name} in your environment or config file"
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
