from aicodebot import AICODEBOT, version as aicodebot_version
from aicodebot.commands import alignment, commit, configure, debug, learn, review, sidekick, sidekick_agent
from aicodebot.config import read_config
from aicodebot.lm import LanguageModelManager
from aicodebot.output import get_console
import click, langchain, os, sys

# -------------------------- Top level command group ------------------------- #

console = get_console()


@click.group()
@click.version_option(aicodebot_version, "--version", "-V")
@click.help_option("--help", "-h")
@click.option("-d", "--debug-output", is_flag=True, help="Enable debug output")
@click.pass_context
def cli(ctx, debug_output):
    ctx.ensure_object(dict)
    ctx.obj["config"] = existing_config = read_config()
    if not existing_config:
        if ctx.invoked_subcommand != "configure":
            console.print(f"Welcome to {AICODEBOT}. Let's set up your config file.\n", style=console.bot_style)
            configure.callback(openai_api_key=os.getenv("OPENAI_API_KEY"), verbose=0)
            sys.exit(0)
    else:
        match LanguageModelManager.CURRENT_PROVIDER:
            case LanguageModelManager.OPENAI:
                os.environ["OPENAI_API_KEY"] = existing_config["openai_api_key"]
            case LanguageModelManager.OLLAMA:
                os.environ["OLLAMA_LOCAL"] = existing_config["ollama_local"]
            case LanguageModelManager.OPENROUTER:
                os.environ["OPENROUTER_API_KEY"] = existing_config["openrouter_api_key"]
            case _:
                raise ValueError(f"Model {LanguageModelManager.CURRENT_PROVIDER} not found. Exiting.")
    # Turn on langchain debug output if requested
    langchain.debug = debug_output


# -------------------------- Subcommands ------------------------- #

cli.add_command(alignment)
cli.add_command(configure)
cli.add_command(commit)
cli.add_command(debug)
cli.add_command(review)
cli.add_command(sidekick)
if os.getenv("AICODEBOT_ENABLE_EXPERIMENTAL_FEATURES"):
    cli.add_command(learn)
    cli.add_command(sidekick_agent)


if __name__ == "__main__":  # pragma: no cover
    cli()
