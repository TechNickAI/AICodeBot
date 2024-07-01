from aicodebot.helpers import logger
from aicodebot.lm import LanguageModelManager
from aicodebot.output import OurMarkdown, RichLiveCallbackHandler, get_console
from aicodebot.prompts import get_prompt
from rich.live import Live
import click, subprocess, sys


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("command", nargs=-1)
@click.pass_context
def debug(ctx, command):
    """Run a command and debug the output."""
    console = get_console()

    # Run the command and capture its output
    command_str = " ".join(command)
    console.print(f"Executing the command:\n{command_str}", highlight=False)
    process = subprocess.run(command_str, shell=True, capture_output=True, text=True, check=False)  # noqa: S602

    # Print the output of the command
    output = f"Standard Output:\n{process.stdout}\nStandard Error:\n{process.stderr}"
    console.print(output, highlight=False)

    # If it succeeded, exit
    if process.returncode == 0:
        console.print("✅ The command completed successfully.")
        return

    # If the command failed, send its output to ChatGPT for analysis
    console.print(f"The command exited with status {process.returncode}.")

    # Load the prompt
    prompt = get_prompt("debug")
    logger.trace(f"Prompt: {prompt}")
    lmm = LanguageModelManager()

    with Live(OurMarkdown(f"Talking to {lmm.model_name} via {lmm.provider}"), auto_refresh=True) as live:
        llm = lmm.model_factory(
            streaming=True,
            callbacks=[RichLiveCallbackHandler(live, console.bot_style)],
        )
        chain = prompt | llm
        response = chain.invoke({"command_output": output, "languages": ["unix", "bash", "shell"]})
        live.update(OurMarkdown(response))

    sys.exit(process.returncode)
