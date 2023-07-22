from langchain.callbacks.base import BaseCallbackHandler
from loguru import logger
from pathlib import Path
from prompt_toolkit.completion import Completer, Completion
from rich.markdown import Markdown
import os, subprocess, sys

# ---------------------------------------------------------------------------- #
#                    Global logging configuration for loguru                   #
# ---------------------------------------------------------------------------- #


logger.remove()
logger_format = (
    "<level>{time}</level> {message} | <level>{level}</level> "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"
)
logger.add(sys.stderr, catch=True, format=logger_format, level=os.getenv("LOG_LEVEL", "WARNING").upper())
logger = logger.opt(colors=True)

# ---------------------------------------------------------------------------- #
#                                Misc functions                                #
# ---------------------------------------------------------------------------- #


def create_and_write_file(filename, text, overwrite=False):
    """Create a file and write text to it."""
    if Path(filename).exists() and not overwrite:
        raise ValueError(f"File '{filename}' already exists and overwrite is False.")

    with Path(filename).open("w") as f:
        f.write(text)


class SidekickCompleter(Completer):
    """A custom prompt_toolkit completer for sidekick."""

    def get_completions(self, document, complete_event):
        # Get the text before the cursor
        text = document.text_before_cursor

        supported_commands = ["/add", "/drop", "/edit", "/files", "/quit"]

        # If the text starts with a slash, it's a command
        if text.startswith("/"):
            for command in supported_commands:
                if command.startswith(text):
                    yield Completion(command, start_position=-len(text))

        if text.startswith(("/add ", "/drop ")):
            # If the text starts with /add or /drop, it's a file
            files = Path().rglob("*")
            for file in files:
                if file.name.startswith(text.split()[-1]):
                    yield Completion(file.name, start_position=-len(text.split()[-1]))


def exec_and_get_output(command):
    """Execute a command and return its output as a string."""
    logger.debug(f"Executing command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)  # noqa: S603
    if result.returncode != 0:
        raise Exception(f"Command '{' '.join(command)}' failed with error:\n{result.stderr}")  # noqa: TRY002
    return result.stdout


class RichLiveCallbackHandler(BaseCallbackHandler):
    def __init__(self, live, style):
        self.buffer = []
        self.live = live
        self.style = style

    def on_llm_new_token(self, token, **kwargs):
        self.buffer.append(token)
        self.live.update(Markdown("".join(self.buffer), style=self.style))
