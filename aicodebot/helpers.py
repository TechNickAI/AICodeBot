from loguru import logger
from pathlib import Path
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


def exec_and_get_output(command):
    """Execute a command and return its output as a string."""
    logger.debug(f"Executing command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True, check=False)  # noqa: S603
    if result.returncode != 0:
        raise Exception(f"Command '{' '.join(command)}' failed with error:\n{result.stderr}")  # noqa: TRY002
    return result.stdout
