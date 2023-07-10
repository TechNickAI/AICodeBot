from loguru import logger
from openai.api_resources import engine
from pathlib import Path
import fnmatch, openai, os, subprocess, sys, tiktoken, yaml

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


def generate_directory_structure(path, ignore_patterns=None, use_gitignore=True, indent=0):
    """Generate a text representation of the directory structure of a path."""
    ignore_patterns = ignore_patterns.copy() if ignore_patterns else []

    base_path = Path(path)

    if use_gitignore:
        # Note: .gitignore files can exist in sub directories as well, such as * in __pycache__ directories
        gitignore_file = base_path / ".gitignore"
        if gitignore_file.exists():
            with gitignore_file.open() as f:
                ignore_patterns.extend(line.strip() for line in f if line.strip() and not line.startswith("#"))

    structure = ""
    if base_path.is_dir():
        if not any(fnmatch.fnmatch(base_path.name, pattern) for pattern in ignore_patterns):
            structure += "  " * indent + f"- [Directory] {base_path.name}\n"
            for item in base_path.iterdir():
                structure += generate_directory_structure(item, ignore_patterns, use_gitignore, indent + 1)
    elif not any(fnmatch.fnmatch(base_path.name, pattern) for pattern in ignore_patterns):
        structure += "  " * indent + f"- [File] {base_path.name}\n"

    return structure


def get_llm_model(token_size=0):
    model_options = {
        "gpt-4": 8192,
        "gpt-4-32k": 32768,
        "gpt-3.5-turbo": 4096,
        "gpt-3.5-turbo-16k": 16384,
    }

    config = read_config()
    openai.api_key = config["openai_api_key"]
    engines = engine.Engine.list()
    logger.trace(f"Engines: {engines}")

    # For some unknown reason, tiktoken often underestimates the token size by ~10%, so let's buffer
    token_size = int(token_size * 1.1)

    # Try to use GPT-4 if it is supported and the token size is small enough
    if "gpt-4" in [engine.id for engine in engines.data] and token_size <= model_options["gpt-4"]:
        logger.info(f"Using GPT-4 for token size {token_size}")
        return "gpt-4"
    elif "gpt-4-32k" in [engine.id for engine in engines.data] and token_size <= model_options["gpt-4-32k"]:
        logger.info(f"Using GPT-4-32k for token size {token_size}")
        return "gpt-4-32k"
    elif token_size <= model_options["gpt-3.5-turbo"]:
        logger.info(f"Using GPT-3.5-turbo for token size {token_size}")
        return "gpt-3.5-turbo"
    elif token_size <= model_options["gpt-3.5-turbo-16k"]:
        logger.info(f"Using GPT-3.5-turbo-16k for token size {token_size}")
        return "gpt-3.5-turbo-16k"
    else:
        logger.critical(
            f"🛑 The context is too large ({token_size})"
            "for the any of the models supported by your Open AI API key. 😞"
        )
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


def get_config_file():
    if "AICODEBOT_CONFIG_FILE" in os.environ:
        config_file = Path(os.getenv("AICODEBOT_CONFIG_FILE"))
    else:
        config_file = Path(Path.home() / ".aicodebot.yaml")
    logger.debug(f"Using config file {config_file}")
    return config_file


def read_config():
    """Read the config file and return its contents as a dictionary."""
    config_file = get_config_file()
    if config_file.exists():
        logger.debug(f"Config file {config_file} exists")
        with Path(config_file).open("r") as f:
            return yaml.safe_load(f)
    else:
        logger.debug(f"Config file {config_file} does not exist")
        return None
