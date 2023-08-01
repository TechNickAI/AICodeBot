from aicodebot.coder import CREATIVE_TEMPERATURE, Coder
from aicodebot.helpers import logger
from aicodebot.output import OurMarkdown, RichLiveCallbackHandler, get_console
from aicodebot.prompts import get_prompt
from langchain.chains import LLMChain
from rich.live import Live
import click


@click.command()
@click.option("-t", "--response-token-size", type=int, default=350)
@click.option("-v", "--verbose", count=True)
def alignment(response_token_size, verbose):
    """A message from AICodeBot about AI Alignment ❤ + 🤖."""
    console = get_console()

    # Load the prompt
    prompt = get_prompt("alignment")
    logger.trace(f"Prompt: {prompt}")

    # Set up the language model
    model_name = Coder.get_llm_model_name(Coder.get_token_length(prompt.template) + response_token_size)

    with Live(OurMarkdown(""), auto_refresh=True) as live:
        llm = Coder.get_llm(
            model_name,
            verbose,
            response_token_size,
            temperature=CREATIVE_TEMPERATURE,
            streaming=True,
            callbacks=[RichLiveCallbackHandler(live, console.bot_style)],
        )

        # Set up the chain
        chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)

        chain.run({})
