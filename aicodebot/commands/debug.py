from aicodebot.coder import DEFAULT_MAX_TOKENS, Coder
from aicodebot.helpers import logger
from aicodebot.output import OurMarkdown, RichLiveCallbackHandler, get_console
from aicodebot.prompts import get_prompt
from langchain.chains import LLMChain
from rich.live import Live
import click, subprocess, sys


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("command", nargs=-1)
@click.option("-v", "--verbose", count=True)
@click.pass_context
def debug(ctx, command, verbose):
    """Run a command and debug the output."""
    console = get_console()

    # Run the command and capture its output
    command_str = " ".join(command)
    console.print(f"Executing the command:\n{command_str}")
    process = subprocess.run(command_str, shell=True, capture_output=True, text=True)  # noqa: S602

    # Print the output of the command
    output = f"Standard Output:\n{process.stdout}\nStandard Error:\n{process.stderr}"
    console.print(output)

    # If it succeeded, exit
    if process.returncode == 0:
        console.print("✅ The command completed successfully.")
        return

    # If the command failed, send its output to ChatGPT for analysis
    console.print(f"The command exited with status {process.returncode}.")

    # Load the prompt
    prompt = get_prompt("debug")
    logger.trace(f"Prompt: {prompt}")

    # Set up the language model
    request_token_size = Coder.get_token_length(output) + Coder.get_token_length(prompt.template)
    model_name = Coder.get_llm_model_name(request_token_size + DEFAULT_MAX_TOKENS)
    if model_name is None:
        raise click.ClickException(f"The output is too large to debug ({request_token_size} tokens). 😢")

    with Live(OurMarkdown(""), auto_refresh=True) as live:
        llm = Coder.get_llm(
            model_name,
            verbose,
            streaming=True,
            callbacks=[RichLiveCallbackHandler(live, console.bot_style)],
        )

        # Set up the chain
        chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)
        chain.run({"command_output": output, "languages": ["unix", "bash", "shell"]})

    sys.exit(process.returncode)
