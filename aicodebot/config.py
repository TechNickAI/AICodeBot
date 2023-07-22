from aicodebot.helpers import logger
from pathlib import Path
import os, sys, yaml


def get_local_data_dir():
    data_dir = Path(os.getenv("AICODEBOT_LOCAL_DATA_DIR", str(Path.home() / ".aicodebot_data")))
    # Make the directory if it doesn't exist
    if not data_dir.exists():
        logger.debug(f"Creating local data directory {data_dir}")
        data_dir.mkdir()
        # Create the subdirectories
        (data_dir / "repos").mkdir()
        (data_dir / "vector_stores").mkdir()

    return data_dir


def get_config_file():
    return Path(os.getenv("AICODEBOT_CONFIG_FILE", str(Path.home() / ".aicodebot.yaml")))


def read_config():
    """Read the config file and return its contents as a dictionary."""
    config_file = get_config_file()
    logger.debug(f"Using config file {config_file}")
    if config_file.exists():
        logger.debug(f"Config file {config_file} exists")
        with Path(config_file).open("r") as f:
            out = yaml.safe_load(f)

            # If the tests are running, don't use openrouter, call open ai directly
            if "pytest" in sys.modules and "openrouter_api_key" in out:
                del out["openrouter_api_key"]

            return out
    else:
        logger.debug(f"Config file {config_file} does not exist")
        return None
