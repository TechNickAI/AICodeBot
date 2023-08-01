from aicodebot import version as aicodebot_version
from aicodebot.coder import DEFAULT_MAX_TOKENS, Coder
from aicodebot.commands import alignment, configure, debug, learn, sidekick, sidekick_agent
from aicodebot.config import read_config
from aicodebot.helpers import exec_and_get_output, logger
from aicodebot.output import OurMarkdown as Markdown, RichLiveCallbackHandler, get_console
from aicodebot.prompts import get_prompt
from langchain.chains import LLMChain
from pathlib import Path
from rich.live import Live
import click, json, langchain, os, shutil, subprocess, sys, tempfile

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
            console.print("Welcome to AICodeBot 🤖. Let's set up your config file.\n", style=console.bot_style)
            configure.callback(openai_api_key=os.getenv("OPENAI_API_KEY"), verbose=0)
            sys.exit(0)
    else:
        os.environ["OPENAI_API_KEY"] = existing_config["openai_api_key"]

    # Turn on langchain debug output if requested
    langchain.debug = debug_output


cli.add_command(alignment)
cli.add_command(configure)
cli.add_command(debug)
cli.add_command(sidekick)
if os.getenv("AICODEBOT_ENABLE_EXPERIMENTAL_FEATURES"):
    cli.add_command(learn)
    cli.add_command(sidekick_agent)

# ---------------------------------------------------------------------------- #
#                                   Commands                                   #
# ---------------------------------------------------------------------------- #

# Commands are defined as functions with the @click decorator.
# The function name is the command name, and the docstring is the help text.
# Keep the commands in alphabetical order.


@cli.command()
@click.option("-v", "--verbose", count=True)
@click.option("-t", "--response-token-size", type=int, default=250)
@click.option("-y", "--yes", is_flag=True, default=False, help="Don't ask for confirmation before committing.")
@click.option("--skip-pre-commit", is_flag=True, help="Skip running pre-commit.")
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def commit(verbose, response_token_size, yes, skip_pre_commit, files):  # noqa: PLR0915
    """Generate a commit message based on your changes."""
    if not Coder.is_inside_git_repo():
        console.print("🛑 This command must be run from within a git repository.", style=console.error_style)
        sys.exit(1)

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
                style=console.warning_style,
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
            callbacks=[RichLiveCallbackHandler(live, console.bot_style)],
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


@cli.command
@click.option("-c", "--commit", help="The commit hash to review (otherwise look at [un]staged changes).")
@click.option("-v", "--verbose", count=True)
@click.option("--output-format", default="text", type=click.Choice(["text", "json"], case_sensitive=False))
@click.option("-t", "--response-token-size", type=int, default=DEFAULT_MAX_TOKENS * 2)
@click.argument("files", nargs=-1)
def review(commit, verbose, output_format, response_token_size, files):
    """Do a code review, with [un]staged changes, or a specified commit."""
    if not Coder.is_inside_git_repo():
        console.print("🛑 This command must be run from within a git repository.", style=console.error_style)
        sys.exit(1)

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
        with console.status("Examining the diff and generating the review", spinner=console.DEFAULT_SPINNER):
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
            llm.callbacks = [RichLiveCallbackHandler(live, console.bot_style)]

            chain.run({"diff_context": diff_context, "languages": languages})


if __name__ == "__main__":  # pragma: no cover
    cli()
