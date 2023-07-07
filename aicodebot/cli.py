from aicodebot import version as aicodebot_version
from aicodebot.helpers import (
    exec_and_get_output,
    get_config_file,
    get_llm_model,
    get_token_length,
    git_diff_context,
    logger,
    read_config,
)
from aicodebot.prompts import PERSONALITIES, generate_files_context, get_prompt
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationTokenBufferMemory
from openai.api_resources import engine
from pathlib import Path
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.style import Style
import click, datetime, openai, os, random, subprocess, sys, tempfile, webbrowser, yaml

# ----------------------------- Default settings ----------------------------- #

DEFAULT_MAX_TOKENS = 512
PRECISE_TEMPERATURE = 0.1
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
@click.option("-t", "--response-token-size", type=int, default=350)
def alignment(response_token_size, verbose):
    """Get a message about Heart-Centered AI Alignment ❤ + 🤖."""
    config = setup_config()

    # Load the prompt
    prompt = get_prompt("alignment")
    logger.trace(f"Prompt: {prompt}")

    # Set up the language model
    model = get_llm_model(get_token_length(prompt.template))

    with Live(Markdown(""), auto_refresh=True) as live:
        llm = ChatOpenAI(
            model=model,
            temperature=CREATIVE_TEMPERATURE,
            openai_api_key=config["OPENAI_API_KEY"],
            max_tokens=response_token_size,
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
    config = setup_config()

    # Check if pre-commit is installed and .pre-commit-config.yaml exists
    if not skip_pre_commit and Path(".pre-commit-config.yaml").exists():
        console.print("Running pre-commit checks...")
        result = subprocess.run(["pre-commit", "run", "--all-files"])
        if result.returncode != 0:
            console.print("🛑 Pre-commit checks failed. Please fix the issues and try again.")
            return

    # Load the prompt
    prompt = get_prompt("commit")
    logger.trace(f"Prompt: {prompt}")

    # Get the changes from git
    staged_files = exec_and_get_output(["git", "diff", "--name-only", "--cached"])
    if not staged_files:
        # If no files are staged, Assume they want to commit all changed files
        logger.info("No files staged, assuming we want to commit all changed files, running git add -A")
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
    if model is None:
        raise click.ClickException(
            f"The diff is too large to generate a commit message ({request_token_size} tokens). 😢"
        )

    # Set up the language model
    llm = ChatOpenAI(
        model=model,
        openai_api_key=config["OPENAI_API_KEY"],
        temperature=PRECISE_TEMPERATURE,
        max_tokens=DEFAULT_MAX_TOKENS,
        verbose=verbose,
    )

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
    config = setup_config()

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
    prompt = get_prompt("debug")
    logger.trace(f"Prompt: {prompt}")

    # Set up the language model
    request_token_size = get_token_length(error_output) + get_token_length(prompt.template)
    model = get_llm_model(request_token_size)
    if model is None:
        raise click.ClickException(f"The output is too large to debug ({request_token_size} tokens). 😢")

    with Live(Markdown(""), auto_refresh=True) as live:
        llm = ChatOpenAI(
            model=model,
            temperature=PRECISE_TEMPERATURE,
            openai_api_key=config["OPENAI_API_KEY"],
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
@click.option("-t", "--response-token-size", type=int, default=350)
def fun_fact(verbose, response_token_size):
    """Get a fun fact about programming and artificial intelligence."""
    config = setup_config()

    # Load the prompt
    prompt = get_prompt("fun_fact")
    logger.trace(f"Prompt: {prompt}")

    # Set up the language model
    model = get_llm_model(get_token_length(prompt.template))

    with Live(Markdown(""), auto_refresh=True) as live:
        llm = ChatOpenAI(
            model=model,
            temperature=PRECISE_TEMPERATURE,
            max_tokens=response_token_size,
            openai_api_key=config["OPENAI_API_KEY"],
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
    config = setup_config()

    diff_context = git_diff_context(commit)
    if not diff_context:
        console.print("No changes detected for review. 🤷")
        sys.exit(0)

    # Load the prompt
    prompt = get_prompt("review")
    logger.trace(f"Prompt: {prompt}")

    # Check the size of the diff context and adjust accordingly
    response_token_size = DEFAULT_MAX_TOKENS
    request_token_size = get_token_length(diff_context) + get_token_length(prompt.template)
    model = get_llm_model(request_token_size)
    if model is None:
        raise click.ClickException(f"The diff is too large to review ({request_token_size} tokens). 😢")

    with Live(Markdown(""), auto_refresh=True) as live:
        llm = ChatOpenAI(
            model=model,
            temperature=PRECISE_TEMPERATURE,
            openai_api_key=config["OPENAI_API_KEY"],
            max_tokens=response_token_size,
            verbose=verbose,
            streaming=True,
            callbacks=[RichLiveCallbackHandler(live)],
        )

        # Set up the chain
        chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)

        chain.run(diff_context)


@cli.command()
@click.option("--openai-api-key", "-k", help="Your OpenAI API key")
@click.option("--gpt-4-supported", "-4", help="Whether you have access to GPT-4", is_flag=True)
def setup(openai_api_key, gpt_4_supported):
    """Set up the configuration file with your OpenAI API key
    If the config file already exists, it will ask you if you want to remove it and recreate it.
    """
    config_file = get_config_file()
    if config_file.exists():
        if not click.confirm(
            f"The config file already exists at {config_file}. Do you want to remove it and recreate it?"
        ):
            console.print("Setup cancelled. 🚫")
            sys.exit(1)

        # Remove the existing config file
        config_file.unlink()

    # Call the setup_config function with the provided arguments
    setup_config(openai_api_key, gpt_4_supported)


@cli.command
@click.option("--request", "-r", help="What to ask your sidekick to do")
@click.option("-v", "--verbose", count=True)
@click.option("-t", "--response-token-size", type=int, default=DEFAULT_MAX_TOKENS * 2)
@click.argument("files", nargs=-1)
def sidekick(request, verbose, response_token_size, files):
    """
    EXPERIMENTAL: Coding help from your AI sidekick\n
    FILES: List of files to be used as context for the session
    """

    console.print("This is an experimental feature. Play with it, but don't count on it.", style=warning_style)

    config = setup_config()

    # Pull in context. Right now it's just the contents of files that we passed in.
    # Soon, we could add vector embeddings of:
    # imported code / modules / libraries
    # Style guides/reference code
    # git history
    context = generate_files_context(files)

    # Generate the prompt and set up the model
    prompt = get_prompt("sidekick")
    request_token_size = get_token_length(prompt.template) + get_token_length(context)
    model = get_llm_model(request_token_size)
    if model is None:
        raise click.ClickException(
            f"The file context you supplied is too large ({request_token_size} tokens). 😢 Try again with less files."
        )

    llm = ChatOpenAI(
        model=model,
        openai_api_key=config["OPENAI_API_KEY"],
        temperature=PRECISE_TEMPERATURE,
        max_tokens=response_token_size,
        verbose=verbose,
        streaming=True,
    )

    # Open the temporary file in the user's editor
    editor = Path(os.getenv("EDITOR", "/usr/bin/vim")).name

    # Set up the chain
    memory = ConversationTokenBufferMemory(
        memory_key="chat_history", input_key="task", llm=llm, max_token_limit=DEFAULT_MAX_TOKENS
    )
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory, verbose=verbose)

    while True:  # continuous loop for multiple questions
        if request:
            human_input = request
        else:
            human_input = click.prompt(
                f"Enter a question OR (q) quit, OR (e) to edit using {editor}\n>>>",
                prompt_suffix="",
            )
            if len(human_input) == 1:
                if human_input.lower() == "q":
                    break
                elif human_input.lower() == "e":
                    human_input = click.edit()
            elif human_input.lower()[-2:] == r"\e":
                # If the text ends with \e then we want to edit it
                human_input = click.edit(human_input[:-2])

        with Live(Markdown(""), auto_refresh=True) as live:
            callback = RichLiveCallbackHandler(live)
            callback.buffer = []
            llm.callbacks = [callback]
            chain.run({"task": human_input, "context": context})

        if request:
            # If we were given a request, then we only want to run once
            break


# ---------------------------------------------------------------------------- #
#                               Helper functions                               #
# ---------------------------------------------------------------------------- #


def setup_config(openai_api_key=None, gpt_4_supported=None):
    config = read_config()
    openai.api_key = openai_api_key
    if config:
        openai.api_key = config["OPENAI_API_KEY"]
        logger.success(f"Using OpenAI API key from {get_config_file()}")
        return config
    elif os.getenv("OPENAI_API_KEY"):
        logger.info("Using OPENAI_API_KEY environment variable")
        openai.api_key = os.getenv("OPENAI_API_KEY")

    config_file = get_config_file()
    console.print(f"[bold red]The config file does not exist.[/bold red]\nLet's set that up for you at {config_file}\n")

    if not openai.api_key:
        openai_api_key_url = "https://platform.openai.com/account/api-keys"

        console.print(
            "First, an OpenAI API key is required to use AICodeBot. You can get one for free on the OpenAI website.\n"
        )

        if click.confirm("Open the OpenAI API keys page for you in a browser?"):
            webbrowser.open(openai_api_key_url)

        openai.api_key = click.prompt("Please enter your OpenAI API key")

    # Validate the API key and check if it supports GPT-4
    if gpt_4_supported is None:
        try:
            click.echo("Validating the API key, and checking if GPT-4 is supported...")
            engines = engine.Engine.list()
            logger.trace(f"Engines: {engines}")
            gpt_4_supported = "gpt-4" in [engine.id for engine in engines.data]
            if gpt_4_supported:
                click.echo("✅ The API key is valid and supports GPT-4.")
            else:
                click.echo("✅ The API key is valid, but does not support GPT-4. GPT-3.5 will be used instead.")
        except Exception as e:
            raise click.ClickException(f"Failed to validate the API key: {str(e)}") from e

    # Pull the choices from the name from each of the PERSONALITIES
    personality_choices = "\nHow would you like your AI to act? You can choose from the following personalities:\n"
    for key, personality in PERSONALITIES.items():
        personality_choices += f"\t{key} - {personality.description}\n"
    console.print(personality_choices)

    personality = click.prompt(
        "Please choose a personality",
        type=click.Choice(PERSONALITIES.keys(), case_sensitive=False),
        default=list(PERSONALITIES.keys())[0],
    )

    config_data = {
        "config_version": 1,
        "OPENAI_API_KEY": openai.api_key,
        "gpt_4_supported": gpt_4_supported,
        "personality": personality,
    }

    with Path.open(config_file, "w") as f:
        yaml.dump(config_data, f)

    console.print(
        f"[bold green]Created {config_file} with your OpenAI API key.[/bold green] "
        "Now, please re-run aicodebot and let's get started!"
    )
    sys.exit(0)


class RichLiveCallbackHandler(BaseCallbackHandler):
    buffer = []

    def __init__(self, live):
        self.live = live

    def on_llm_new_token(self, token, **kwargs):
        self.buffer.append(token)
        self.live.update(Markdown("".join(self.buffer), style=bot_style))


if __name__ == "__main__":
    cli()
