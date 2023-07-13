from aicodebot.helpers import logger
from pathlib import Path
import os, yaml


def get_config_file():
    if "AICODEBOT_CONFIG_FILE" in os.environ:
        config_file = Path(os.getenv("AICODEBOT_CONFIG_FILE"))
    else:
        config_file = Path(Path.home() / ".aicodebot.yaml")
    return config_file


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
