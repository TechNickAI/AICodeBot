from aicodebot.helpers import logger
from aicodebot.lm import CREATIVE_TEMPERATURE, LanguageModelManager
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

    with Live(OurMarkdown(""), auto_refresh=True) as live:
        lmm = LanguageModelManager()
        chain = lmm.chain_factory(
            prompt=prompt,
            response_token_size=response_token_size,
            temperature=CREATIVE_TEMPERATURE,
            streaming=True,
            callbacks=[RichLiveCallbackHandler(live, console.bot_style)],
        )

        chain.run({})
