from aicodebot.helpers import logger
from aicodebot.lm import CREATIVE_TEMPERATURE, LanguageModelManager, get_token_size
from aicodebot.output import OurMarkdown, RichLiveCallbackHandler, get_console
from aicodebot.prompts import get_prompt
from rich.live import Live
import click


@click.command()
@click.option("-t", "--response-token-size", type=int, default=350)
def alignment(response_token_size):
    """A message from 🤖 AICodeBot about AI Alignment ❤"""
    console = get_console()

    # Load the prompt
    prompt = get_prompt("alignment")
    logger.trace(f"Prompt: {prompt}")

    # Set up the language model
    lmm = LanguageModelManager()
    model_name = lmm.choose_model(get_token_size(prompt.template) + response_token_size)

    with Live(OurMarkdown(""), auto_refresh=True) as live:
        llm = lmm.get_langchain_model(
            model_name,
            response_token_size,
            temperature=CREATIVE_TEMPERATURE,
            streaming=True,
            callbacks=[RichLiveCallbackHandler(live, console.bot_style)],
        )

        # Set up the chain
        chain = lmm.get_langchain_chain(llm=llm, prompt=prompt)

        chain.run({})
