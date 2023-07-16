from aicodebot.helpers import logger
from pathlib import Path
import os, yaml


def get_config_file():
    return Path(os.getenv("AICODEBOT_CONFIG_FILE", str(Path.home() / ".aicodebot.yaml")))


def read_config():
    """Read the config file and return its contents as a dictionary."""
    config_file = get_config_file()
    logger.debug(f"Using config file {config_file}")
    if config_file.exists():
        logger.debug(f"Config file {config_file} exists")
        with Path(config_file).open("r") as f:
            return yaml.safe_load(f)
    else:
        logger.debug(f"Config file {config_file} does not exist")
        return None
