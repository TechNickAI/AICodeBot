from dotenv import find_dotenv, load_dotenv
from pathlib import Path
from setup import __version__
import click, os, webbrowser

# Load environment variables from .env file
load_dotenv(find_dotenv())


def setup_environment():
    if os.getenv("OPENAI_API_KEY"):
        return True

    openai_api_key_url = "https://platform.openai.com/account/api-keys"

    click.echo("The OPENAI_API_KEY environment variable is not set. Let's fix that for you by creating a .env file.")

    if click.confirm("Do you want me to open the OpenAI API keys page for you in a browser?"):
        webbrowser.open(openai_api_key_url)

    if click.confirm("Do you want me to create the .env file for you?"):
        api_key = click.prompt("Please enter your OpenAI API key")

        # Copy .env.template to .env and insert the API key
        with Path.open(".env.template", "r") as template, Path.open(".env", "w") as env:
            for line in template:
                if line.startswith("OPENAI_API_KEY="):
                    env.write(f"OPENAI_API_KEY={api_key}\n")
                else:
                    env.write(line)

        click.echo("Created .env file with your OpenAI API key. You're all set!")

        return True

    raise click.UsageError("Please set an API key in the OPENAI_API_KEY environment variable or in a .env file.")

    return False


@click.group()
@click.version_option(__version__, "--version", "-V")
@click.help_option("--help", "-h")
def cli():
    pass


@cli.command()
def version():
    """Print the version number."""
    click.echo(f"AICodeBot version {__version__}")


@cli.command()
@click.option("-v", "--verbose", count=True)
def joke(verbose):
    """Tell a [probably bad] programming joke."""
    setup_environment()
    api_key = os.getenv("OPENAI_API_KEY")
    if verbose:
        click.echo(f"Using API key: {api_key}")


if __name__ == "__main__":
    cli()
