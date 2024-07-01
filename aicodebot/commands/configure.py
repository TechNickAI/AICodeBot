from aicodebot import AICODEBOT
from aicodebot.config import get_config_file, read_config
from aicodebot.helpers import create_and_write_file
from aicodebot.output import get_console
from aicodebot.prompts import DEFAULT_PERSONALITY, PERSONALITIES
import click, os, sys, webbrowser, yaml


@click.command()
@click.option("-v", "--verbose", count=True)
@click.option("--openai-api-key", envvar="OPENAI_API_KEY", help="Your OpenAI API key")
def configure(verbose, openai_api_key):
    """Create or update the configuration file"""
    console = get_console()

    # --------------- Check for an existing key or set up defaults --------------- #

    config_data_defaults = {
        "version": 1.2,
        "openai_api_key": openai_api_key,
        "personality": DEFAULT_PERSONALITY.name,
    }

    config_data = config_data_defaults.copy()
    config_file = get_config_file()

    existing_config = read_config()
    if existing_config:
        console.print(f"Config file already exists at {get_config_file()}.")
        click.confirm("Do you want to rerun configure and overwrite it?", default=False, abort=True)
        config_data.update(
            {
                "openai_api_key": existing_config["openai_api_key"],
                "personality": existing_config["personality"],
            }
        )

    config_data = config_data_defaults.copy()

    def write_config_file(config_data):
        create_and_write_file(config_file, yaml.dump(config_data))
        console.print(f"✅ Created config file at {config_file}")

    is_terminal = sys.stdout.isatty()
    openai_api_key = openai_api_key or config_data["openai_api_key"] or os.getenv("OPENAI_API_KEY")
    if not is_terminal:
        if openai_api_key is None:
            raise click.ClickException(
                "🛑 No OpenAI API key found.\n"
                "Please set the OPENAI_API_KEY environment variable or call configure with --openai-api-key set."
            )
        else:
            # If we are not in a terminal, then we can't ask for input, so just use the defaults and write the file
            write_config_file(config_data)
            return

    # ---------------- Collect the OPENAI_API_KEY and validate it ---------------- #

    if config_data["openai_api_key"] is None:
        console.print(
            f"You need an OpenAI API Key for {AICODEBOT}. You can get one on the OpenAI website.",
            style=console.bot_style,
        )
        openai_api_key_url = "https://platform.openai.com/account/api-keys"
        if click.confirm("Open the api keys page in a browser?", default=False):
            webbrowser.open(openai_api_key_url)

        config_data["openai_api_key"] = click.prompt("Please enter your OpenAI API key").strip()

    # ---------------------- Collect the personality choice ---------------------- #

    # Pull the choices from the name from each of the PERSONALITIES
    console.print(
        "\nHow would you like your AI to act? You can choose from the following personalities:\n",
        style=console.bot_style,
    )
    personality_choices = ""
    for key, personality in PERSONALITIES.items():
        personality_choices += f"\t[b]{key}[/b] - {personality.description}\n"
    console.print(personality_choices)

    config_data["personality"] = click.prompt(
        "Please choose a personality",
        type=click.Choice(PERSONALITIES.keys(), case_sensitive=False),
        default=DEFAULT_PERSONALITY.name,
    )

    write_config_file(config_data)
    console.print(f"✅ Configuration complete, you're ready to run {AICODEBOT}!\n")
