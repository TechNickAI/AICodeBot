from aicodebot import AICODEBOT, version as aicodebot_version
from aicodebot.commands import alignment, commit, configure, debug, review, sidekick
from aicodebot.config import read_config
from aicodebot.output import get_console
import click, langchain_core, os, sys

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
        os.environ["OPENAI_API_KEY"] = existing_config["openai_api_key"]

    # Turn on langchain debug output if requested
    langchain_core.debug = debug_output


# -------------------------- Subcommands ------------------------- #

cli.add_command(alignment)
cli.add_command(configure)
cli.add_command(commit)
cli.add_command(debug)
cli.add_command(review)
cli.add_command(sidekick)


if __name__ == "__main__":  # pragma: no cover
    cli()
