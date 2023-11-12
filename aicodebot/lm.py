from aicodebot import AICODEBOT_NO_EMOJI
from aicodebot.config import read_config
from aicodebot.helpers import logger
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import Ollama
from langchain.memory import ConversationTokenBufferMemory
from openai.api_resources import engine
import functools, openai, os, tiktoken

DEFAULT_RESPONSE_TOKENS = 512
DEFAULT_MEMORY_TOKENS = DEFAULT_RESPONSE_TOKENS * 2
DEFAULT_CONTEXT_TOKENS = DEFAULT_RESPONSE_TOKENS * 4
PRECISE_TEMPERATURE = 0.05
CREATIVE_TEMPERATURE = 0.6


class LanguageModelManager:
    """A class for interacting with language models."""

    provider = model_name = _memory = None

    OPENAI = "OpenAI"
    OPENROUTER = "OpenRouter"
    OLLAMA = "Ollama"
    PROVIDERS = [OPENAI, OPENROUTER, OLLAMA]
    DEFAULT_MODEL = "gpt-4"
    DEFAULT_PROVIDER = OPENAI
    CURRENT_PROVIDER = DEFAULT_PROVIDER
    # NOTE: CURRENT_PROVIDER needs to be manually set.
    #       This will change when the configure command is implemented and CURRENT_PROVIDER can be changed at will.

    def __init__(self, model_name=None, provider=None):
        self.model_name = model_name
        self.provider = provider
        if not self.model_name:
            self.read_model_config()

    # --------------------------------- Factories -------------------------------- #

    def chain_factory(
        self,
        prompt,
        response_token_size=None,
        temperature=PRECISE_TEMPERATURE,
        streaming=False,
        callbacks=None,
        chat_history=False,
    ):
        language_model = self.model_factory(response_token_size, temperature, streaming, callbacks)
        if chat_history:
            memory = self.get_memory(language_model)
        else:
            memory = None
        return LLMChain(llm=language_model, prompt=prompt, memory=memory)

    def model_factory(
        self,
        response_token_size=None,
        temperature=PRECISE_TEMPERATURE,
        streaming=False,
        callbacks=None,
    ):
        """Get a model object for the specified model name."""

        # We support multiple approaches for using language models:
        # 1. OpenAI API
        # 2. Open Router API
        # 3. FUTURE - Local models

        provider, model_name = self.read_model_config()

        if provider == self.OPENAI:
            return self.get_openai_model(
                model_name,
                response_token_size=response_token_size,
                temperature=temperature,
                streaming=streaming,
                callbacks=callbacks,
            )
        elif provider == self.OPENROUTER:
            return self.get_openrouter_model(
                model_name,
                response_token_size=response_token_size,
                temperature=temperature,
                streaming=streaming,
                callbacks=callbacks,
            )
        # NOTE: Ollama does not have a streaming parameter, this is handled by callbacks instead.
        #       This may result in slight changes elsewhere in the codebase when Ollama is used.
        # TODO: Create a wrapper for Ollama models, enabling them to use the streaming parameter.
        elif provider == self.OLLAMA:
            return self.get_ollama_model(
                model_name,
                response_token_size=response_token_size,
                temperature=temperature,
                callbacks=callbacks,
            )
        else:  # pragma: no cover
            raise ValueError(f"Provider {provider} is not one of: {self.PROVIDERS}")

    def get_memory(self, llm, token_limit=DEFAULT_MEMORY_TOKENS, memory_key="chat_history", input_key="task"):
        """Initializes a memory object with the specified parameters."""
        if not self._memory:  # Re-use the same memory object
            self._memory = ConversationTokenBufferMemory(
                memory_key=memory_key,
                input_key=input_key,
                llm=llm,
                max_token_limit=token_limit,
                human_prefix="Software Engineer",
                ai_prefix=AICODEBOT_NO_EMOJI,
            )
        return self._memory

    def get_ollama_model(
        self,
        model_name,
        response_token_size=None,
        temperature=PRECISE_TEMPERATURE,
        callbacks=None,
    ):
        return Ollama(
            model=model_name,
            num_ctx=response_token_size,
            temperature=temperature,
            callbacks=callbacks,
        )

    def get_openai_model(
        self,
        model_name,
        response_token_size=None,
        temperature=PRECISE_TEMPERATURE,
        streaming=False,
        callbacks=None,
    ):
        """Get an OpenAI model object for the specified model name."""
        api_key = self.get_key("OPENAI_API_KEY")

        return ChatOpenAI(
            openai_api_key=api_key,
            model=model_name,
            max_tokens=response_token_size,
            temperature=temperature,
            streaming=streaming,
            callbacks=callbacks,
        )

    def get_key(self, key_name):
        # Read the api key from either the environment or the config file
        key_name_upper = key_name.upper()
        key = os.getenv(key_name_upper)
        if key:
            return key
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

    def get_openrouter_model(
        self,
        model_name,
        response_token_size=None,
        temperature=PRECISE_TEMPERATURE,
        streaming=False,
        callbacks=None,
    ):
        api_key = self.get_key("OPENROUTER_API_KEY")

        # Set the API base to the Open Router API, and set special headers that are required
        api_base = "https://openrouter.ai/api/v1"
        headers = {"HTTP-Referer": "https://aicodebot.dev", "X-Title": AICODEBOT_NO_EMOJI}

        return ChatOpenAI(
            openai_api_key=api_key,
            openai_api_base=api_base,
            model=model_name,
            max_tokens=response_token_size,
            temperature=temperature,
            streaming=streaming,
            callbacks=callbacks,
            # In order to get ConversationBufferMemory to work, we need to set the tiktoken model name
            tiktoken_model_name=self.tiktoken_model_name,
            model_kwargs={"headers": headers},
        )

    def get_model_token_limit(self, model_name):
        model_token_limits = {
            "openai/gpt-4": 8192,
            "openai/gpt-4-32k": 32768,
            "anthropic/claude-2": 100_000,
            "gpt-4": 8192,
            "gpt-4-32k": 32768,
            "gpt-3.5-turbo": 4096,
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
        # Figure out which model to use, based on the config file or environment variables
        config = read_config() or {}
        self.provider = os.getenv(
            "AICODEBOT_MODEL_PROVIDER", config.get("language_model_provider", self.CURRENT_PROVIDER)
        )
        self.model_name = os.getenv("AICODEBOT_MODEL", config.get("language_model", self.DEFAULT_MODEL))

        # --------------------------- API key verification --------------------------- #
        if self.provider == self.OPENAI:
            key_name = "OPENAI_API_KEY"
        elif self.provider == self.OPENROUTER:
            key_name = "OPENROUTER_API_KEY"
        elif self.provider == self.OLLAMA:
            key_name = "OLLAMA_LOCAL"
        else:
            raise ValueError(f"Unrecognized provider: {self.provider}")
        model = self.get_key(key_name)
        if not model:
            raise ValueError(
                f"In order to use {self.provider}, you must set the {key_name} in your environment or config file"
            )
        # NOTE: This code doesnt do anything except set the name Ollama.
        #       When configure is implemented this will dynamically organize which model is being used.
        match self.provider:
            case self.OLLAMA:
                self.model_name = model
            case self.OPENAI:
                self.model_name = "gpt-4"
            case self.OPENROUTER:
                self.model_name = "openrouter"

        return self.provider, self.model_name

    @property
    def tiktoken_model_name(self):
        if "/" in self.model_name:
            if self.model_name.startswith("openai/"):
                # For OpenAI models, this is as simple as stripping the prefix "openai/" from the model name
                return self.model_name.replace("openai/", "")
            else:
                # For non-OpenAI models, we set the model name to "gpt-4" for now. Seems to work.
                # Tested with anthropic/claude2
                return self.DEFAULT_MODEL
        else:
            return self.model_name

    def use_appropriate_sized_model(self, chain, token_size):
        current_model = self.model_name
        gpt_4_limit = self.get_model_token_limit("gpt-4") * 0.9
        gpt_4_32k_limit = self.get_model_token_limit("gpt-4-32k") * 0.9
        if current_model in ["gpt-4", "gpt-4-32k"]:
            if token_size > gpt_4_32k_limit:
                raise ValueError("Token limit exceeded for GPT4, try using less context (files)")
            elif token_size > gpt_4_limit:
                if "gpt-4-32k" in openai_supported_engines():
                    self.model_name = "gpt-4-32k"
                else:
                    raise ValueError(
                        "Your request is too large for gpt-4, and you don't have access to gpt-4-32k.\n"
                        "Hint: Try using openrouter.ai which has access to lots of models. See the README for details."
                    )
            else:
                self.model_name = "gpt-4"

        elif current_model in ["openai/gpt-4", "openai/gpt-4-32k"]:
            if token_size > gpt_4_32k_limit:
                raise ValueError(
                    "Token limit exceeded for GPT4, try using less context (files)\n"
                    "Hint: try anthropic/claude-2 (100k token limit)"
                )
            elif token_size > gpt_4_limit:
                self.model_name = "openai/gpt-4-32k"
            else:
                self.model_name = "openai/gpt-4"

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
    # NOTE: This sets the token size to default value for Ollama.
    #       TikToken doesn't seem to support Ollama-based models.
    #       Local models will not work as intended without dynamically setting the token size.
    # TODO: Dynamically set token size for Ollama-based models.
    if LanguageModelManager.CURRENT_PROVIDER == LanguageModelManager.OLLAMA:
        return 2048
    return LanguageModelManager().get_token_size(text)


# This is outside the class because functools.lru_cache doesn't work with class methods
# in Python <= 3.9
@functools.lru_cache(maxsize=1)
def openai_supported_engines():
    """Get a list of the models supported by the OpenAI API key."""
    config = read_config()
    openai.api_key = config["openai_api_key"]
    engines = engine.Engine.list()
    out = [engine.id for engine in engines.data]
    logger.trace(f"OpenAI supported engines: {out}")
    return out
