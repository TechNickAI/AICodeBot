from loguru import logger
from pathlib import Path
import os, subprocess, sys, tiktoken

# ---------------------------------------------------------------------------- #
#                    Global logging configuration for loguru                   #
# ---------------------------------------------------------------------------- #


logger.remove()
logger_format = (
    "<level>{time}</level> {message} | <level>{level}</level> "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"
)
logger.add(sys.stderr, catch=True, format=logger_format, level=os.getenv("LOG_LEVEL", "WARNING"))
logger = logger.opt(colors=True)

# ---------------------------------------------------------------------------- #
#                                Misc functions                                #
# ---------------------------------------------------------------------------- #


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
            logger.info(f"Using GPT-4 for token size {token_size}")
            return "gpt-4"
        elif token_size <= model_options["gpt-4-32k"]:
            logger.info(f"Using GPT-4-32k for token size {token_size}")
            return "gpt-4-32k"
        else:
            logger.critical("🛑 The context is too large to for the Model. 😞")
            return None
    else:
        if token_size <= model_options["gpt-3.5-turbo"]:  # noqa: PLR5501
            logger.info(f"Using GPT-3.5-turbo for token size {token_size}")
            return "gpt-3.5-turbo"
        elif token_size <= model_options["gpt-3.5-turbo-16k"]:
            logger.info(f"Using GPT-3.5-turbo-16k for token size {token_size}")
            return "gpt-3.5-turbo-16k"
        else:
            logger.critical("🛑 The context is too large to for the Model. 😞")
            return None


def get_token_length(text, model="gpt-3.5-turbo"):
    """Get the number of tokens in a string using the tiktoken library."""
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    token_length = len(tokens)
    logger.debug(f"Token length for text {text[0:10]}...: {token_length}")
    return token_length


def git_diff_context(commit=None):
    """Get a text representation of the git diff for the current commit or staged files, including new files"""
    base_git_diff = ["git", "diff", "-U10"]  # Tell diff to provide 10 lines of context

    if commit:
        # If a commit is provided, just get the diff for that commit
        logger.debug(f"Getting diff for commit {commit}")
        return exec_and_get_output(["git", "show", commit])
    else:
        # Otherwise, get the diff for the staged files, or if there are none, the diff for the unstaged files
        staged_files = exec_and_get_output(["git", "diff", "--cached", "--name-only"]).splitlines()
        if staged_files:
            logger.debug(f"Getting diff for staged files: {staged_files}")
            diff_type = "--cached"
        else:
            logger.debug(f"Getting diff for unstaged files: {staged_files}")
            diff_type = "HEAD"

        file_status = exec_and_get_output(["git", "diff", diff_type, "--name-status"]).splitlines()

        diffs = []
        for status in file_status:
            status_parts = status.split("\t")
            status_code = status_parts[0][0]  # Get the first character of the status code
            if status_code == "A":
                # If the file is new, include the entire file content
                file_name = status_parts[1]
                contents = Path(file_name).read_text()
                diffs.append(f"## New file added: {file_name}")
                diffs.append(contents)
            elif status_code == "R":
                # If the file is renamed, get the diff and note the old and new names
                old_file_name, new_file_name = status_parts[1], status_parts[2]
                diffs.append(f"## File renamed: {old_file_name} -> {new_file_name}")
                diffs.append(exec_and_get_output(base_git_diff + [diff_type, "--", new_file_name]))
            elif status_code == "D":
                # If the file is deleted, note the deletion
                file_name = status_parts[1]
                diffs.append(f"## File deleted: {file_name}")
            else:
                # If the file is not new, renamed, or deleted, get the diff
                file_name = status_parts[1]
                diffs.append(f"## File changed: {file_name}")
                diffs.append(exec_and_get_output(base_git_diff + [diff_type, "--", file_name]))

        return "\n".join(diffs)


def exec_and_get_output(command):
    """Execute a command and return its output as a string."""
    logger.debug(f"Executing command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)  # noqa: S603
    if result.returncode != 0:
        raise Exception(f"Command '{' '.join(command)}' failed with error:\n{result.stderr}")  # noqa: TRY002
    return result.stdout
