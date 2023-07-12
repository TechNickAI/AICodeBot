from aicodebot import version as aicodebot_version
from aicodebot.coder import CREATIVE_TEMPERATURE, DEFAULT_MAX_TOKENS, Coder
from aicodebot.config import get_config_file, read_config
from aicodebot.helpers import RichLiveCallbackHandler, exec_and_get_output, logger
from aicodebot.prompts import DEFAULT_PERSONALITY, PERSONALITIES, generate_files_context, get_prompt
from langchain.chains import LLMChain
from langchain.memory import ConversationTokenBufferMemory
from openai.api_resources import engine
from pathlib import Path
from prompt_toolkit import prompt as input_prompt
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.style import Style
import click, datetime, openai, os, random, subprocess, sys, tempfile, webbrowser, yaml

# ----------------------------- Default settings ----------------------------- #

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
    setup_config()

    # Load the prompt
    prompt = get_prompt("alignment")
    logger.trace(f"Prompt: {prompt}")

    # Set up the language model
    model_name = Coder.get_llm_model_name(Coder.get_token_length(prompt.template))

    with Live(Markdown(""), auto_refresh=True) as live:
        llm = Coder.get_llm(
            model_name,
            verbose,
            response_token_size,
            temperature=CREATIVE_TEMPERATURE,
            streaming=True,
            callbacks=[RichLiveCallbackHandler(live, bot_style)],
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
    setup_config()

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

    diff_context = Coder.git_diff_context()

    if not diff_context:
        console.print("No changes to commit. 🤷")
        sys.exit(0)

    # Check the size of the diff context and adjust accordingly
    request_token_size = Coder.get_token_length(diff_context) + Coder.get_token_length(prompt.template)
    model_name = Coder.get_llm_model_name(request_token_size)
    if model_name is None:
        raise click.ClickException(
            f"The diff is too large to generate a commit message ({request_token_size} tokens). 😢"
        )

    llm = Coder.get_llm(model_name, verbose, 350)

    # Set up the chain
    chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)

    console.print("The following files will be committed:\n" + files)
    with console.status("Examining the diff and generating the commit message", spinner=DEFAULT_SPINNER):
        response = chain.run(diff_context)

    # Write the commit message to a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
        # For some reason the response often contains quotes around the summary, even if I tell it not to
        # So we strip them here
        commit_message = str(response).replace('"', "").strip()

        temp.write(commit_message)
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


@cli.command()
@click.option("-v", "--verbose", count=True)
@click.option("--openai-api-key", envvar="OPENAI_API_KEY", help="Your OpenAI API key")
def configure(verbose, openai_api_key):
    """Create or update the config file"""

    # --------------- Check for an existing key or set up defaults --------------- #

    config_data_defaults = {
        "version": 1.1,
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
            {"openai_api_key": existing_config["openai_api_key"], "personality": existing_config["personality"]}
        )

    config_data = config_data_defaults.copy()

    def write_config_file(config_data):
        with Path.open(config_file, "w") as f:
            yaml.dump(config_data, f)
            console.print(f"✅ Created config file at {config_file}")

    is_terminal = sys.stdout.isatty()
    if not is_terminal:
        if config_data["openai_api_key"] is None:
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
            "An OpenAI API key is required to use AICodeBot. You can get one for free on the OpenAI website.\n"
        )
        openai_api_key_url = "https://platform.openai.com/account/api-keys"
        if click.confirm("Open the OpenAI API keys page for you in a browser?", default=False):
            webbrowser.open(openai_api_key_url)

        config_data["openai_api_key"] = input_prompt("Please enter your OpenAI API key")

    # Validate the API key
    try:
        openai.api_key = config_data["openai_api_key"]
        click.echo("Validating the OpenAI API key")
        engine.Engine.list()
    except Exception as e:
        raise click.ClickException(f"Failed to validate the API key: {str(e)}") from e
    click.echo("✅ The API key is valid.")

    # ---------------------- Collect the personality choice ---------------------- #

    # Pull the choices from the name from each of the PERSONALITIES
    personality_choices = "\nHow would you like your AI to act? You can choose from the following personalities:\n"
    for key, personality in PERSONALITIES.items():
        personality_choices += f"\t{key} - {personality.description}\n"
    console.print(personality_choices)

    config_data["personality"] = click.prompt(
        "Please choose a personality",
        type=click.Choice(PERSONALITIES.keys(), case_sensitive=False),
        default=DEFAULT_PERSONALITY.name,
    )

    write_config_file(config_data)
    console.print("✅ Configuration complete, you're ready to run aicodebot!\n")

    # After writing the config file, print the usage for the top-level group
    ctx = click.get_current_context()
    while ctx.parent is not None:
        ctx = ctx.parent
    console.print(ctx.get_help())

    console.print("\nDon't know where to start? Try running `aicodebot alignment`.")


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("command", nargs=-1)
@click.option("-v", "--verbose", count=True)
def debug(command, verbose):
    """Run a command and debug the output."""
    setup_config()

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
    request_token_size = Coder.get_token_length(error_output) + Coder.get_token_length(prompt.template)
    model_name = Coder.get_llm_model_name(request_token_size)
    if model_name is None:
        raise click.ClickException(f"The output is too large to debug ({request_token_size} tokens). 😢")

    with Live(Markdown(""), auto_refresh=True) as live:
        llm = Coder.get_llm(
            model_name,
            verbose,
            streaming=True,
            callbacks=[RichLiveCallbackHandler(live, bot_style)],
        )

        # Set up the chain
        chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)
        chain.run(error_output)

    sys.exit(process.returncode)


@cli.command()
@click.option("-v", "--verbose", count=True)
@click.option("-t", "--response-token-size", type=int, default=250)
def fun_fact(verbose, response_token_size):
    """Get a fun fact about programming and artificial intelligence."""
    setup_config()

    # Load the prompt
    prompt = get_prompt("fun_fact")
    logger.trace(f"Prompt: {prompt}")

    # Set up the language model
    model_name = Coder.get_llm_model_name(Coder.get_token_length(prompt.template))

    with Live(Markdown(""), auto_refresh=True) as live:
        llm = Coder.get_llm(
            model_name,
            verbose,
            response_token_size=response_token_size,
            temperature=CREATIVE_TEMPERATURE,
            streaming=True,
            callbacks=[RichLiveCallbackHandler(live, bot_style)],
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
    setup_config()

    diff_context = Coder.git_diff_context(commit)
    if not diff_context:
        console.print("No changes detected for review. 🤷")
        sys.exit(0)

    # Load the prompt
    prompt = get_prompt("review")
    logger.trace(f"Prompt: {prompt}")

    # Check the size of the diff context and adjust accordingly
    response_token_size = DEFAULT_MAX_TOKENS * 2
    request_token_size = Coder.get_token_length(diff_context) + Coder.get_token_length(prompt.template)
    model_name = Coder.get_llm_model_name(request_token_size)
    if model_name is None:
        raise click.ClickException(f"The diff is too large to review ({request_token_size} tokens). 😢")

    with Live(Markdown(""), auto_refresh=True) as live:
        llm = Coder.get_llm(
            model_name,
            verbose,
            response_token_size=response_token_size,
            streaming=True,
            callbacks=[RichLiveCallbackHandler(live, bot_style)],
        )

        # Set up the chain
        chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)

        chain.run(diff_context)


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

    setup_config()

    # Pull in context. Right now it's just the contents of files that we passed in.
    # Soon, we could add vector embeddings of:
    # imported code / modules / libraries
    # Style guides/reference code
    # git history
    context = generate_files_context(files)

    # Generate the prompt and set up the model
    prompt = get_prompt("sidekick")
    request_token_size = Coder.get_token_length(prompt.template) + Coder.get_token_length(context)
    model_name = Coder.get_llm_model_name(request_token_size)
    if model_name is None:
        raise click.ClickException(
            f"The file context you supplied is too large ({request_token_size} tokens). 😢 Try again with less files."
        )

    llm = Coder.get_llm(model_name, verbose, response_token_size, streaming=True)

    # Open the temporary file in the user's editor
    editor = Path(os.getenv("EDITOR", "/usr/bin/vim")).name

    # Set up the chain
    memory = ConversationTokenBufferMemory(
        memory_key="chat_history", input_key="task", llm=llm, max_token_limit=DEFAULT_MAX_TOKENS
    )
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory, verbose=verbose)
    history_file = Path.home() / ".aicodebot_request_history"

    while True:  # continuous loop for multiple questions
        if request:
            human_input = request
        else:
            console.print(f"Enter a request OR (q) quit, OR (e) to edit using {editor}")
            human_input = input_prompt("➤ ", history=FileHistory(history_file))
            if len(human_input) == 1:
                if human_input.lower() == "q":
                    break
                elif human_input.lower() == "e":
                    human_input = click.edit()
            elif human_input.lower()[-2:] == r"\e":
                # If the text ends with \e then we want to edit it
                human_input = click.edit(human_input[:-2])

        with Live(Markdown(""), auto_refresh=True) as live:
            callback = RichLiveCallbackHandler(live, bot_style)
            llm.callbacks = [callback]  # a fresh callback handler for each question
            chain.run({"task": human_input, "context": context})

        if request:
            # If we were given a request, then we only want to run once
            break


# ---------------------------------------------------------------------------- #
#                               Helper functions                               #
# ---------------------------------------------------------------------------- #


def setup_config():
    existing_config = read_config()
    if not existing_config:
        console.print("No config file found. Running configure...\n")
        configure.callback(openai_api_key=None, verbose=0)
        sys.exit()
    else:
        return existing_config


if __name__ == "__main__":
    cli()
