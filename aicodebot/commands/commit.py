import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import click
from pydantic import BaseModel, Field
from rich.panel import Panel

from aicodebot.coder import Coder
from aicodebot.helpers import exec_and_get_output, logger
from aicodebot.lm import LanguageModelManager
from aicodebot.output import OurMarkdown, get_console
from aicodebot.prompts import get_prompt


class CommitMessage(BaseModel):
    # Note we get better results if the message_detail is first.
    git_message_detail: str | None = Field(
        description="An optional detailed explanation of the changes made in this commit,"
        " if the summary doesn't provide enough context",
    )

    git_message_summary: str = Field(description="A brief summary of the commit message (max 72 characters)")


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
        console.print("The following files have been staged and are ready for commit:\n\t" + "\n\t".join(staged_files))

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
    with console.status(f"Generating commit message with {lmm.model_name} via {lmm.provider}", spinner="dots"):
        llm = lmm.model_factory(response_token_size=response_token_size)
        # Using Langchain Expression Language (LCEL) for structured output. So chic! 😉
        chain = prompt | llm.with_structured_output(CommitMessage)
        logger.debug(f"Chain input: {{'diff_context': {diff_context}, 'languages': {languages}}}")
        response = chain.invoke({"diff_context": diff_context, "languages": languages})
        logger.debug(f"Chain response: {response}")

    # Handle both object and dict responses,
    # The structured output sometimes returns a dict and sometimes returns an object?!
    def get_attr_or_item(obj, key):
        return obj[key] if isinstance(obj, dict) else getattr(obj, key, None)

    git_message_summary = get_attr_or_item(response, "git_message_summary")
    git_message_detail = get_attr_or_item(response, "git_message_detail")

    commit_message = git_message_summary or "No summary provided"
    if git_message_detail:
        commit_message += f"\n\n{git_message_detail}"

    console.print(Panel(OurMarkdown(commit_message)))

    commit_message_approved = not console.is_terminal or click.confirm(
        "Would you like to use this generated commit message? Type 'n' to edit it.", default=True
    )

    # Write the commit message to a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
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
