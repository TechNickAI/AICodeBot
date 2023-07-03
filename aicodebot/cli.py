from aicodebot import version as aicodebot_version
from aicodebot.agents import get_agent
from aicodebot.helpers import exec_and_get_output, get_token_length, git_diff_context
from dotenv import load_dotenv
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import load_prompt
from openai.api_resources import engine
from pathlib import Path
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.style import Style
import click, datetime, openai, os, random, subprocess, sys, tempfile, webbrowser

# ----------------------------- Default settings ----------------------------- #

DEFAULT_MAX_TOKENS = 512
PRECISE_TEMPERATURE = 0
CREATIVE_TEMPERATURE = 0.7
DEFAULT_SPINNER = "point"

# ----------------------- Setup for rich console output ---------------------- #

console = Console()
bot_style = Style(color="#30D5C8")
error_style = Style(color="#FF0000")
warning_style = Style(color="#FFA500")

# -------------------------- Top level command group ------------------------- #


@click.group()
@click.version_option(aicodebot_version, "--version", "-V")
@click.help_option("--help", "-h")
def cli():
    pass


# ---------------------------------------------------------------------------- #
#                                   Commands                                   #
# ---------------------------------------------------------------------------- #

# Commands are defined as functions with the @click decorator.
# The function name is the command name, and the docstring is the help text.
# Keep the commands in alphabetical order.


@cli.command()
@click.option("-v", "--verbose", count=True)
def alignment(verbose):
    """Get a message about Heart-Centered AI Alignment ❤ + 🤖."""
    setup_environment()

    # Load the prompt
    prompt = load_prompt(Path(__file__).parent / "prompts" / "alignment.yaml")

    # Set up the language model
    model = get_llm_model(get_token_length(prompt.template))

    with Live(Markdown(""), auto_refresh=True) as live:
        llm = ChatOpenAI(
            model=model,
            temperature=CREATIVE_TEMPERATURE,
            max_tokens=DEFAULT_MAX_TOKENS,
            verbose=verbose,
            streaming=True,
            callbacks=[RichLiveCallbackHandler(live)],
        )

        # Set up the chain
        chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)

        chain.run({})


@cli.command()
@click.option("-v", "--verbose", count=True)
@click.option("-t", "--response-token-size", type=int, default=250)
@click.option("-y", "--yes", is_flag=True, default=False, help="Don't ask for confirmation before committing.")
@click.option("--skip-pre-commit", is_flag=True, help="Skip running pre-commit (otherwise run it if it is found).")
def commit(verbose, response_token_size, yes, skip_pre_commit):
    """Generate a commit message based on your changes."""
    setup_environment()

    # Check if pre-commit is installed and .pre-commit-config.yaml exists
    if not skip_pre_commit and Path(".pre-commit-config.yaml").exists():
        console.print("Running pre-commit checks...")
        result = subprocess.run(["pre-commit", "run", "--all-files"])
        if result.returncode != 0:
            console.print("🛑 Pre-commit checks failed. Please fix the issues and try again.")
            return

    # Load the prompt
    prompt = load_prompt(Path(__file__).parent / "prompts" / "commit_message.yaml")

    # Get the changes from git
    staged_files = exec_and_get_output(["git", "diff", "--name-only", "--cached"])
    if not staged_files:
        # If no files are staged, Assume they want to commit all changed files
        exec_and_get_output(["git", "add", "-A"])
        # Get the list of files to be committed
        files = exec_and_get_output(["git", "diff", "--name-only", "--cached"])
    else:
        # The list of files to be committed is the same as the list of staged files
        files = staged_files

    diff_context = git_diff_context()

    if not diff_context:
        console.print("No changes to commit. 🤷")
        sys.exit(0)

    # Check the size of the diff context and adjust accordingly
    request_token_size = get_token_length(diff_context) + get_token_length(prompt.template)
    model = get_llm_model(request_token_size)
    if verbose:
        console.print(f"Diff context token size: {request_token_size}, using model: {model}")

    # Set up the language model
    llm = ChatOpenAI(model=model, temperature=PRECISE_TEMPERATURE, max_tokens=DEFAULT_MAX_TOKENS, verbose=verbose)

    # Set up the chain
    chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)

    console.print("The following files will be committed:\n" + files)
    with console.status("Examining the diff and generating the commit message", spinner=DEFAULT_SPINNER):
        response = chain.run(diff_context)

    # Write the commit message to a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
        temp.write(str(response).strip())
        temp_file_name = temp.name

    # Open the temporary file in the user's editor
    editor = os.getenv("EDITOR", "vim")
    subprocess.call([editor, temp_file_name])  # noqa: S603

    # Ask the user if they want to commit the changes
    if yes or click.confirm("Are you ready to commit the changes?"):
        # Commit the changes using the temporary file for the commit message
        exec_and_get_output(["git", "commit", "-F", temp_file_name])
        console.print(f"✅ {len(files.splitlines())} files committed.")

    # Delete the temporary file
    Path.unlink(temp_file_name)


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("command", nargs=-1)
@click.option("-v", "--verbose", count=True)
def debug(command, verbose):
    """Run a command and debug the output."""
    setup_environment()

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
        sys.exit(0)

    # If the command failed, send its output to ChatGPT for analysis
    error_output = process.stderr

    console.print(f"The command exited with status {process.returncode}.")

    # Load the prompt
    prompt = load_prompt(Path(__file__).parent / "prompts" / "debug.yaml")

    # Set up the language model
    model = get_llm_model(get_token_length(error_output) + get_token_length(prompt.template))

    with Live(Markdown(""), auto_refresh=True) as live:
        llm = ChatOpenAI(
            model=model,
            temperature=PRECISE_TEMPERATURE,
            max_tokens=DEFAULT_MAX_TOKENS,
            verbose=verbose,
            streaming=True,
            callbacks=[RichLiveCallbackHandler(live)],
        )

        # Set up the chain
        chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)
        chain.run(error_output)

    sys.exit(process.returncode)


@cli.command()
@click.option("-v", "--verbose", count=True)
def fun_fact(verbose):
    """Get a fun fact about programming and artificial intelligence."""
    setup_environment()

    # Load the prompt
    prompt = load_prompt(Path(__file__).parent / "prompts" / "fun_fact.yaml")

    # Set up the language model
    model = get_llm_model(get_token_length(prompt.template))

    with Live(Markdown(""), auto_refresh=True) as live:
        llm = ChatOpenAI(
            model=model,
            temperature=PRECISE_TEMPERATURE,
            max_tokens=DEFAULT_MAX_TOKENS / 2,
            verbose=verbose,
            streaming=True,
            callbacks=[RichLiveCallbackHandler(live)],
        )

        # Set up the chain
        chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)

        year = random.randint(1942, datetime.datetime.utcnow().year)
        chain.run(f"programming and artificial intelligence in the year {year}")


@cli.command
@click.option("-c", "--commit", help="The commit hash to review (otherwise look at [un]staged changes).")
@click.option("-v", "--verbose", count=True)
def review(commit, verbose):
    """Do a code review, with [un]staged changes, or a specified commit."""
    setup_environment()

    diff_context = git_diff_context(commit)
    if not diff_context:
        console.print("No changes detected for review. 🤷")
        sys.exit(0)

    # Load the prompt
    prompt = load_prompt(Path(__file__).parent / "prompts" / "review.yaml")

    # Check the size of the diff context and adjust accordingly
    response_token_size = DEFAULT_MAX_TOKENS / 2
    request_token_size = get_token_length(diff_context) + get_token_length(prompt.template)
    model = get_llm_model(request_token_size)
    if verbose:
        console.print(f"Diff context token size: {request_token_size}, using model: {model}")

    with Live(Markdown(""), auto_refresh=True) as live:
        llm = ChatOpenAI(
            model=model,
            temperature=PRECISE_TEMPERATURE,
            max_tokens=response_token_size,
            verbose=verbose,
            streaming=True,
            callbacks=[RichLiveCallbackHandler(live)],
        )

        # Set up the chain
        chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)

        chain.run(diff_context)


@cli.command
@click.option("--task", "-t", help="The task you want to perform - a description of what you want to do.")
@click.option("-v", "--verbose", count=True)
def sidekick(task, verbose):
    """ALPHA/EXPERIMENTAL: Get coding help from your AI sidekick."""
    console.print(
        "⚠️ WARNING: The 'sidekick' feature is currently experimental and, frankly, it sucks right now. "
        "Due to the token limitations with large language models, the amount of context "
        "that can be sent back and forth is limited, and slow. This means that sidekick will struggle with "
        "complex tasks and will take longer than a human for simpler tasks.\n"
        "Play with it, but don't expect too much. Do you feel like contributing? 😃\n"
        "See docs/sidekick.md for more information.",
        style=warning_style,
    )

    setup_environment()

    model = get_llm_model()
    llm = ChatOpenAI(model=model, temperature=PRECISE_TEMPERATURE, max_tokens=2000, verbose=verbose)

    agent = get_agent("sidekick", llm, verbose)

    with console.status("Thinking", spinner=DEFAULT_SPINNER):
        response = agent({"input": task})
        console.print("")
        console.print(response["output"], style=bot_style)


# ---------------------------------------------------------------------------- #
#                               Helper functions                               #
# ---------------------------------------------------------------------------- #


def setup_environment():
    # Load environment variables from the config file
    config_file = Path(Path.home() / ".aicodebot")
    load_dotenv(config_file)

    if os.getenv("OPENAI_API_KEY"):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        return True

    openai_api_key_url = "https://platform.openai.com/account/api-keys"

    console.print(
        "[bold red]The OPENAI_API_KEY environment variable is not set.[/bold red]\n"
        f"The OpenAI API key is required to use aicodebot. You can get one for free on the OpenAI website.\n"
        f"Let's create a config file for you at {config_file}"
    )

    if click.confirm("Open the OpenAI API keys page for you in a browser?"):
        webbrowser.open(openai_api_key_url)

    if click.confirm(f"Create the {config_file} file for you?"):
        api_key = click.prompt("Please enter your OpenAI API key")

        # Validate the API key and check if it supports GPT-4
        openai.api_key = api_key
        try:
            click.echo("Validating the API key, and checking if GPT-4 is supported...")
            engines = engine.Engine.list()
            gpt_4_supported = "true" if "gpt-4" in [engine.id for engine in engines.data] else "false"
            if gpt_4_supported == "true":
                click.echo("✅ The API key is valid and supports GPT-4.")
            else:
                click.echo("✅ The API key is valid, but does not support GPT-4. GPT-3.5 will be used instead.")
        except Exception as e:
            raise click.ClickException(f"Failed to validate the API key: {str(e)}") from e

        # Copy .env.template to .env and insert the API key and gpt_4_supported
        template_file = Path(__file__).parent / ".aicodebot.template"
        with Path.open(template_file, "r") as template, Path.open(config_file, "w") as env:
            for line in template:
                if line.startswith("OPENAI_API_KEY="):
                    env.write(f"OPENAI_API_KEY={api_key}\n")
                elif line.startswith("GPT_4_SUPPORTED="):
                    env.write(f"GPT_4_SUPPORTED={gpt_4_supported}\n")
                else:
                    env.write(line)

        console.print(
            f"[bold green]Created {config_file} with your OpenAI API key and GPT-4 support status.[/bold green] "
            "Now, please re-run aicodebot and let's get started!"
        )
        sys.exit(0)

    raise click.ClickException(
        "🛑 Please set an API key in the OPENAI_API_KEY environment variable or in a .aicodebot file."
    )


def get_llm_model(token_size=0):
    # https://platform.openai.com/docs/models/gpt-3-5
    # We want to use GPT-4, if it is available for this OPENAI_API_KEY, otherwise GPT-3.5
    # We also want to use the largest model that supports the token size we need
    model_options = {
        "gpt-4": 8192,
        "gpt-4-32k": 32768,
        "gpt-3.5-turbo": 4096,
        "gpt-3.5-turbo-16k": 16384,
    }
    gpt_4_supported = os.getenv("GPT_4_SUPPORTED") == "true"

    # For some unknown reason, tiktoken often underestimates the token size by ~10%, so let's buffer
    token_size = int(token_size * 1.1)

    if gpt_4_supported:
        if token_size <= model_options["gpt-4"]:
            return "gpt-4"
        elif token_size <= model_options["gpt-4-32k"]:
            return "gpt-4-32k"
        else:
            raise click.ClickException("🛑 The context is too large to for the Model. 😞")
    else:
        if token_size <= model_options["gpt-3.5-turbo"]:  # noqa: PLR5501
            return "gpt-3.5-turbo"
        elif token_size <= model_options["gpt-3.5-turbo-16k"]:
            return "gpt-3.5-turbo-16k"
        else:
            raise click.ClickException("🛑 The context is too large to for the Model. 😞")


class RichLiveCallbackHandler(BaseCallbackHandler):
    buffer = []

    def __init__(self, live):
        self.live = live

    def on_llm_new_token(self, token, **kwargs):
        self.buffer.append(token)
        self.live.update(Markdown("".join(self.buffer)))


if __name__ == "__main__":
    cli()
