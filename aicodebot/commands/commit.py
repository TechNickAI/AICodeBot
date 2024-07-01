from aicodebot.coder import Coder
from aicodebot.helpers import exec_and_get_output, logger
from aicodebot.lm import LanguageModelManager
from aicodebot.output import OurMarkdown, RichLiveCallbackHandler, get_console
from aicodebot.prompts import get_prompt
from pathlib import Path
from rich.live import Live
import click, os, shutil, subprocess, sys, tempfile


@click.command()
@click.option("-t", "--response-token-size", type=int, default=250)
@click.option("-y", "--yes", is_flag=True, default=False, help="Don't ask for confirmation before committing.")
@click.option("--skip-pre-commit", is_flag=True, help="Skip running pre-commit.")
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def commit(response_token_size, yes, skip_pre_commit, files):  # noqa: PLR0915
    """Generate a commit message based on your changes."""
    console = get_console()
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
        console.print(
            "The following files have been staged and are ready for commit:\n\t" + "\n\t".join(staged_files)
        )

        files = staged_files

    # Don't look at files that were deleted/moved
    files = [f for f in files if Path(f).exists()]

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
            result = subprocess.run(["pre-commit", "run", "--files"] + files, check=False)
            if result.returncode != 0:
                console.print("🛑 Pre-commit checks failed. Please fix the issues and try again.")
                return

    if not staged_files:
        # Stage the files that we are committing
        exec_and_get_output(["git", "add"] + list(files))

    # Load the prompt
    prompt = get_prompt("commit")
    logger.trace(f"Prompt: {prompt}")
    lmm = LanguageModelManager()

    console.print("Analyzing the differences and generating a commit message")
    with Live(OurMarkdown(f"Talking to {lmm.model_name} via {lmm.provider}"), auto_refresh=True) as live:
        llm = lmm.model_factory(
            response_token_size=response_token_size,
            streaming=True,
            callbacks=[RichLiveCallbackHandler(live, console.bot_style)],
        )
        chain = prompt | llm
        response = chain.invoke({"diff_context": diff_context, "languages": languages})
        live.update(OurMarkdown(str(response)))

    commit_message_approved = not console.is_terminal or click.confirm(
        "Would you like to use this generated commit message? Type 'n' to edit it.", default=True
    )

    # Write the commit message to a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
        # For some reason the response often contains quotes around the summary, even if I tell it not to
        # So we strip them here
        commit_message = str(response.content).replace('"', "").strip()

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
