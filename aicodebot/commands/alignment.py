from aicodebot.helpers import logger
from aicodebot.lm import CREATIVE_TEMPERATURE, LanguageModelManager
from aicodebot.output import OurMarkdown, RichLiveCallbackHandler, get_console
from aicodebot.prompts import get_prompt
from rich.live import Live
import click


@click.command()
@click.option("-t", "--response-token-size", type=int, default=500)
def alignment(response_token_size):
    """A message about AI Alignment 🤖 + ❤"""
    console = get_console()

    # Load the prompt
    prompt = get_prompt("alignment")
    logger.trace(f"Prompt: {prompt}")
    lmm = LanguageModelManager()

    with Live(OurMarkdown(f"Talking to {lmm.model_name} via {lmm.provider}"), auto_refresh=True) as live:
        llm = lmm.model_factory(
            response_token_size=response_token_size,
            temperature=CREATIVE_TEMPERATURE,
            streaming=True,
            callbacks=[RichLiveCallbackHandler(live, console.bot_style)],
        )
        chain = prompt | llm

        response = str(chain.invoke({}))
        live.update(OurMarkdown(response))
