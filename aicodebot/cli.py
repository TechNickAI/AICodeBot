from aicodebot import version as aicodebot_version
from aicodebot.agents import SidekickAgent
from aicodebot.coder import CREATIVE_TEMPERATURE, DEFAULT_MAX_TOKENS, Coder
from aicodebot.config import get_config_file, get_local_data_dir, read_config
from aicodebot.helpers import create_and_write_file, exec_and_get_output, logger
from aicodebot.input import SidekickCompleter
from aicodebot.learn import load_documents_from_repo, store_documents
from aicodebot.output import OurMarkdown as Markdown, RichLiveCallbackHandler
from aicodebot.prompts import DEFAULT_PERSONALITY, PERSONALITIES, generate_files_context, get_prompt
from langchain.chains import LLMChain
from langchain.memory import ConversationTokenBufferMemory
from openai.api_resources import engine
from pathlib import Path
from prompt_toolkit import prompt as input_prompt
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.live import Live
from rich.style import Style
import click, humanize, json, langchain, openai, os, shutil, subprocess, sys, tempfile, webbrowser, yaml

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
@click.option("-d", "--debug", is_flag=True, help="Enable langchain debug output")
def cli(debug):
    # Turn on langchain debug output if requested
    langchain.debug = debug


# ---------------------------------------------------------------------------- #
#                                   Commands                                   #
# ---------------------------------------------------------------------------- #

# Commands are defined as functions with the @click decorator.
# The function name is the command name, and the docstring is the help text.
# Keep the commands in alphabetical order.


@cli.command()
@click.option("-t", "--response-token-size", type=int, default=350)
@click.option("-v", "--verbose", count=True)
def alignment(response_token_size, verbose):
    """A message from AICodeBot about AI Alignment ❤ + 🤖."""
    setup_cli()

    # Load the prompt
    prompt = get_prompt("alignment")
    logger.trace(f"Prompt: {prompt}")

    # Set up the language model
    model_name = Coder.get_llm_model_name(Coder.get_token_length(prompt.template) + response_token_size)

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
@click.option(
    "--skip-pre-commit",
    is_flag=True,
    help="Skip running pre-commit (otherwise run it if it is found).",
)
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def commit(verbose, response_token_size, yes, skip_pre_commit, files):  # noqa: PLR0915
    """Generate a commit message based on your changes."""
    setup_cli(verify_git_repo=True)

    # If files are specified, only consider those files
    if files:
        staged_files = [f for f in Coder.git_staged_files() if f in files]
        unstaged_files = [f for f in Coder.git_unstaged_files() if f in files]
    else:
        # Otherwise use git
        staged_files = Coder.git_staged_files()
        unstaged_files = Coder.git_unstaged_files()

    if not staged_files:
        # If no files are staged, they probably want to commit all changed files, confirm.
        if not files and not yes:
            confirm = click.confirm(
                "Since there are no git staged files, all of the modified files will be committed:\n\t"
                + "\n\t".join(unstaged_files)
                + "\nDoes that look correct?",
                default=True,
            )
            if not confirm:
                console.print("Aborting commit.")
                return

        files = unstaged_files
    else:
        # The list of files to be committed is the same as the list of staged files
        console.print("The following staged files will be committed:\n\t" + "\n\t".join(staged_files))

        files = staged_files

    diff_context = Coder.git_diff_context()
    languages = ",".join(Coder.identify_languages(files))
    if not diff_context:
        console.print("No changes to commit. 🤷")
        return

    # Check if pre-commit is installed and .pre-commit-config.yaml exists
    if not skip_pre_commit and Path(".pre-commit-config.yaml").exists():
        if not shutil.which("pre-commit"):
            console.print(
                "This project uses pre-commit, but it is not installed. Skipping pre-commit checks.",
                style=warning_style,
            )
        else:
            console.print("Running pre-commit checks...")
            result = subprocess.run(["pre-commit", "run", "--files"] + files)
            if result.returncode != 0:
                console.print("🛑 Pre-commit checks failed. Please fix the issues and try again.")
                return

    if not staged_files:
        # Stage the files that we are committing
        exec_and_get_output(["git", "add"] + list(files))

    # Load the prompt
    prompt = get_prompt("commit")
    logger.trace(f"Prompt: {prompt}")

    # Check the size of the diff context and adjust accordingly
    request_token_size = Coder.get_token_length(diff_context) + Coder.get_token_length(prompt.template)
    model_name = Coder.get_llm_model_name(request_token_size + response_token_size)
    if model_name is None:
        raise click.ClickException(
            f"The diff is too large to generate a commit message ({request_token_size} tokens). 😢"
        )

    console.print("Examining the diff and generating the commit message")
    with Live(Markdown(""), auto_refresh=True) as live:
        llm = Coder.get_llm(
            model_name,
            verbose,
            350,
            streaming=True,
            callbacks=[RichLiveCallbackHandler(live, bot_style)],
        )

        # Set up the chain
        chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)
        response = chain.run({"diff_context": diff_context, "languages": languages})

    commit_message_approved = not console.is_terminal or click.confirm(
        "Do you want to use this commit message (type n to edit)?", default=True
    )

    # Write the commit message to a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
        # For some reason the response often contains quotes around the summary, even if I tell it not to
        # So we strip them here
        commit_message = str(response).replace('"', "").strip()

        temp.write(commit_message)
        temp_file_name = temp.name

    if not commit_message_approved:
        # Open the temporary file in the user's editor
        editor = os.getenv("EDITOR", "vim")
        subprocess.call([editor, temp_file_name])  # noqa: S603

    # Ask the user if they want to commit the changes
    confirm = yes or not console.is_terminal or click.confirm("Are you ready to commit the changes?", default=True)
    if confirm:
        # Commit the changes using the temporary file for the commit message
        exec_and_get_output(["git", "commit", "-F", temp_file_name])
        console.print(f"✅ {len(files)} file(s) committed.")
    else:
        console.print("Aborting commit.")

    # Delete the temporary file
    Path(temp_file_name).unlink()


@cli.command()
@click.option("-v", "--verbose", count=True)
@click.option("--openai-api-key", envvar="OPENAI_API_KEY", help="Your OpenAI API key")
def configure(verbose, openai_api_key):
    """Create or update the configuration file"""

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
            "You need an OpenAI API Key for AICodeBot. You can get one on the OpenAI website.",
            style=bot_style,
        )
        openai_api_key_url = "https://platform.openai.com/account/api-keys"
        if click.confirm("Open the api keys page in a browser?", default=False):
            webbrowser.open(openai_api_key_url)

        config_data["openai_api_key"] = click.prompt("Please enter your OpenAI API key").strip()

    # Validate the API key
    try:
        openai.api_key = config_data["openai_api_key"]
        with console.status("Validating the OpenAI API key", spinner=DEFAULT_SPINNER):
            engine.Engine.list()
    except Exception as e:
        raise click.ClickException(f"Failed to validate the API key: {str(e)}") from e
    console.print("✅ The API key is valid.")

    # ---------------------- Collect the personality choice ---------------------- #

    # Pull the choices from the name from each of the PERSONALITIES
    console.print(
        "\nHow would you like your AI to act? You can choose from the following personalities:\n",
        style=bot_style,
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
    console.print("✅ Configuration complete, you're ready to run aicodebot!\n")


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("command", nargs=-1)
@click.option("-v", "--verbose", count=True)
def debug(command, verbose):
    """Run a command and debug the output."""
    setup_cli()

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

    with Live(Markdown(""), auto_refresh=True) as live:
        llm = Coder.get_llm(
            model_name,
            verbose,
            streaming=True,
            callbacks=[RichLiveCallbackHandler(live, bot_style)],
        )

        # Set up the chain
        chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)
        chain.run({"command_output": output, "languages": ["unix", "bash", "shell"]})

    sys.exit(process.returncode)


@cli.command
@click.option("-v", "--verbose", count=True)
@click.option("-r", "--repo-url", help="The URL of the repository to learn from")
def learn(repo_url, verbose):
    """NOT WORKING YET: Learn new skills and gain additional knowledge from a repository"""
    # Clone the supplied repo locally and walk through it, load it into a
    # local vector store, and pre-query this vector store for the LLM to use a
    # context for the prompt

    setup_cli()

    console.print("This is an experimental feature.", style=warning_style)

    owner, repo_name = Coder.parse_github_url(repo_url)

    local_data_dir = get_local_data_dir()

    Coder.clone_repo(repo_url, local_data_dir / "repos" / repo_name)
    console.print("✅ Repo cloned.")

    console.print("Loading documents from repo...")
    vector_store_dir = local_data_dir / "vector_stores" / repo_name
    documents = load_documents_from_repo(local_data_dir / "repos" / repo_name)

    num_documents = humanize.intcomma(len(documents))
    console.print(f"✅ {num_documents} documents loaded")

    console.print("Storking documents from into vector store...")
    store_documents(documents, vector_store_dir)
    console.print(
        f"✅ Repo loaded and indexed. You can now use it with the sidekick-agent command with -l {repo_name}"
    )


@cli.command
@click.option("-c", "--commit", help="The commit hash to review (otherwise look at [un]staged changes).")
@click.option("-v", "--verbose", count=True)
@click.option("--output-format", default="text", type=click.Choice(["text", "json"], case_sensitive=False))
@click.option("-t", "--response-token-size", type=int, default=DEFAULT_MAX_TOKENS * 2)
@click.argument("files", nargs=-1)
def review(commit, verbose, output_format, response_token_size, files):
    """Do a code review, with [un]staged changes, or a specified commit."""
    setup_cli(verify_git_repo=True)

    # If files are specified, only consider those files
    # Otherwise, use git to get the list of files
    if not files:
        files = Coder.git_staged_files()
        if not files:
            files = Coder.git_unstaged_files()

    diff_context = Coder.git_diff_context(commit, files)
    if not diff_context:
        console.print("No changes detected for review. 🤷")
        return
    languages = ",".join(Coder.identify_languages(files))

    # Load the prompt
    prompt = get_prompt("review", structured_output=output_format == "json")
    logger.trace(f"Prompt: {prompt}")

    # Check the size of the diff context and adjust accordingly
    request_token_size = Coder.get_token_length(diff_context) + Coder.get_token_length(prompt.template)
    model_name = Coder.get_llm_model_name(request_token_size + response_token_size)
    if model_name is None:
        raise click.ClickException(f"The diff is too large to review ({request_token_size} tokens). 😢")

    llm = Coder.get_llm(model_name, verbose, response_token_size, streaming=True)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)

    if output_format == "json":
        with console.status("Examining the diff and generating the review", spinner=DEFAULT_SPINNER):
            response = chain.run({"diff_context": diff_context, "languages": languages})

        parsed_response = prompt.output_parser.parse(response)
        data = {
            "review_status": parsed_response.review_status,
            "review_comments": parsed_response.review_comments,
        }
        if commit:
            data["commit"] = commit
        json_response = json.dumps(data, indent=4)
        print(json_response)  # noqa: T201

    else:
        # Stream live
        console.print(
            "Examining the diff and generating the review for the following files:\n\t" + "\n\t".join(files)
        )
        with Live(Markdown(""), auto_refresh=True) as live:
            llm.streaming = True
            llm.callbacks = [RichLiveCallbackHandler(live, bot_style)]

            chain.run({"diff_context": diff_context, "languages": languages})


@cli.command
@click.option("-r", "--request", help="What to ask your sidekick to do")
@click.option("-n", "--no-files", is_flag=True, help="Don't automatically load any files for context")
@click.option("-m", "--max-file-tokens", type=int, default=10_000, help="Don't load files larger than this")
@click.option("-v", "--verbose", count=True)
@click.argument("files", nargs=-1, type=click.Path(exists=True, readable=True))
def sidekick(request, verbose, no_files, max_file_tokens, files):  # noqa: PLR0915
    """
    Coding help from your AI sidekick
    FILES: List of files to be used as context for the session
    """
    setup_cli(verify_git_repo=True)

    console.print("This is an experimental feature. We love bug reports 😉", style=warning_style)

    # ----------------- Determine which files to use for context ----------------- #
    model_name = Coder.get_llm_model_name(-1, biggest_available=True)
    model_token_limit = Coder.get_model_token_limit(model_name)
    file_context_limit = model_token_limit * 0.75
    console.print(
        f"Using the [bold underline]{model_name}[/bold underline] model, "
        f"which has a {humanize.intcomma(model_token_limit)} token limit."
    )

    if files:  # User supplied list of files
        context = generate_files_context(files)
        file_token_size = Coder.get_token_length(context)
        if file_token_size > file_context_limit:
            raise click.ClickException(
                f"The file(s) you supplied are too large ({file_token_size} tokens). 😢 Try again with less files."
            )
    elif not no_files:
        # Determine which files to use for context automagically, with git
        console.print("Using recent git commits and current changes for context.")
        files = Coder.auto_file_context(file_context_limit, max_file_tokens)
        context = generate_files_context(files)
        file_token_size = Coder.get_token_length(context)
    else:
        context = generate_files_context([])
        file_token_size = 0

    # Convert it from a list or a tuple to a set to remove duplicates
    files = set(files)
    # ----------------------------- Set up langchain ----------------------------- #

    # Generate the prompt and set up the model
    prompt = get_prompt("sidekick")
    memory_token_size = round(model_token_limit * 0.1)

    # Determine the max token size for the response
    def calc_response_token_size(files):
        file_token_size = 0
        for file in files:
            file_token_size += Coder.get_token_length(Path(file).read_text())
        prompt_token_size = Coder.get_token_length(prompt.template)
        logger.trace(
            f"File token size: {file_token_size}, memory token size: {memory_token_size}, "
            f"prompt token size: {prompt_token_size}, model token limit: {model_token_limit}"
        )
        out = model_token_limit - (memory_token_size + file_token_size + prompt_token_size)
        out = round(out * 0.95)  # Small buffer
        logger.debug(f"Response max token size: {out}")
        return out

    response_token_size = calc_response_token_size(files)

    llm = Coder.get_llm(model_name, verbose, response_token_size, streaming=True)
    memory = ConversationTokenBufferMemory(
        memory_key="chat_history", input_key="task", llm=llm, max_token_limit=memory_token_size
    )
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory, verbose=verbose)

    # ---------------------- Set up the chat loop and prompt --------------------- #
    show_file_context(files)
    languages = ",".join(Coder.identify_languages(files))

    console.print(
        "Enter a request for your AICodeBot sidekick. Type / to see available commands.\n",
        style=bot_style,
    )
    history_file = Path.home() / ".aicodebot_request_history"
    completer = SidekickCompleter()
    completer.files = files

    while True:  # continuous loop for multiple questions
        edited_input = None
        if request:
            human_input = request
        else:
            human_input = input_prompt("🤖 ➤ ", history=FileHistory(history_file), completer=completer)
            human_input = human_input.strip()

        if not human_input:
            # Must have been spaces or blank line
            continue

        if human_input.startswith("/"):
            cmd = human_input.lower().split()[0]

            # ------------------------------ Handle commands ----------------------------- #
            if cmd in ["/add", "/drop"]:
                # Get the filename
                # If they didn't specify a file, then ignore
                try:
                    filenames = human_input.split()[1:]
                except IndexError:
                    continue

                # If the file doesn't exist, or we can't open it, let them know
                for filename in filenames:
                    if cmd == "/add":
                        try:
                            # Test opening the file
                            with Path(filename).open("r"):
                                files.add(filename)
                                console.print(f"✅ Added '{filename}' to the list of files.")
                        except OSError as e:
                            console.print(f"Unable to open '{filename}': {e.strerror}", style=error_style)
                            continue

                    elif cmd == "/drop":
                        # Drop the file from the list
                        files.discard(filename)
                        console.print(f"✅ Dropped '{filename}' from the list of files.")

                # Update the context for the new list of files
                context = generate_files_context(files)
                completer.files = files
                languages = ",".join(Coder.identify_languages(files))
                show_file_context(files)
                continue

            elif cmd == "/commit":
                # Call the commit function with the parsed arguments
                args = human_input.split()[1:]
                ctx = click.get_current_context()
                ctx.invoke(commit, *args)
                continue
            elif cmd == "/edit":
                human_input = edited_input = click.edit()
            elif cmd == "/files":
                show_file_context(files)
                continue
            elif cmd == "/review":
                # Call the review function with the parsed arguments
                args = human_input.split()[1:]
                ctx = click.get_current_context()
                ctx.invoke(review, *args)
                continue
            elif cmd == "/sh":
                # Strip off the /sh and any leading/trailing whitespace
                shell_command = human_input[3:].strip()

                if not shell_command:
                    continue

                # Execute the shell command and let the output go directly to the console
                subprocess.run(shell_command, shell=True)  # noqa: S602
                continue

            elif cmd == "/quit":
                break

        elif human_input.lower()[-2:] == r"\e":
            # If the text ends wit then we want to edit it
            human_input = edited_input = click.edit(human_input[:-2])

        # --------------- Process the input and stream it to the human --------------- #
        if edited_input:
            # If the user edited the input, then we want to print it out so they
            # have a record of what they asked for on their terminal
            console.print(f"Request:\n{edited_input}")

        try:
            with Live(Markdown(""), auto_refresh=True) as live:
                callback = RichLiveCallbackHandler(live, bot_style)
                llm.callbacks = [callback]  # a fresh callback handler for each question
                # Recalculate the response token size in case the files changed
                llm.max_tokens = calc_response_token_size(files)

                chain.run({"task": human_input, "context": context, "languages": languages})
        except KeyboardInterrupt:
            console.print("\n\nOk, I'll stop talking. Hit Ctrl-C again to quit.", style=bot_style)
            continue

        if request:
            # If we were given a request, then we only want to run once
            break


@cli.command
@click.option("-l", "--learned-repos", multiple=True, help="The name of the repo to use for learned information")
def sidekick_agent(learned_repos):
    """
    EXPREMENTAL: Coding help from your AI sidekick, made agentic with tools\n
    """
    setup_cli(verify_git_repo=True)

    console.print("This is an experimental feature.", style=warning_style)

    agent = SidekickAgent.get_agent_executor(learned_repos)
    history_file = Path.home() / ".aicodebot_request_history"

    console.print("Enter a request for your AICodeBot sidekick", style=bot_style)

    edited_input = None
    while True:  # continuous loop for multiple questions
        human_input = input_prompt("🤖 ➤ ", history=FileHistory(history_file))
        human_input = human_input.strip()

        if not human_input:
            # Must have been spaces or blank line
            continue

        elif human_input.lower()[-2:] == r"\e":
            # If the text ends wit then we want to edit it
            human_input = edited_input = click.edit(human_input[:-2])

        if edited_input:
            # If the user edited the input, then we want to print it out so they
            # have a record of what they asked for on their terminal
            console.print(f"Request:\n{edited_input}")

        response = agent.run(human_input)
        # Remove everything after Action: (if it exists)
        response = response.split("Action:")[0]
        console.print(Markdown(response))


# ---------------------------------------------------------------------------- #
#                               Helper functions                               #
# ---------------------------------------------------------------------------- #


def setup_cli(verify_git_repo=False):
    if verify_git_repo and not Coder.is_inside_git_repo():
        console.print("🛑 This command must be run from within a git repository.", style=error_style)
        sys.exit(1)

    existing_config = read_config()
    if not existing_config:
        console.print("Welcome to AICodeBot 🤖. Let's set up your config file.\n", style=bot_style)
        configure.callback(openai_api_key=os.getenv("OPENAI_API_KEY"), verbose=0)
        sys.exit(0)
    else:
        os.environ["OPENAI_API_KEY"] = existing_config["openai_api_key"]
        return existing_config


def show_file_context(files):
    if not files:
        return

    console.print("Files loaded in this session:")
    for file in files:
        token_length = Coder.get_token_length(Path(file).read_text())
        console.print(f"\t{file} ({humanize.intcomma(token_length)} tokens)")


if __name__ == "__main__":  # pragma: no cover
    cli()
