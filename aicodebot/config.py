from aicodebot.helpers import create_and_write_file, logger
from pathlib import Path
import os, yaml


def get_local_data_dir():
    data_dir = Path(os.getenv("AICODEBOT_LOCAL_DATA_DIR", str(Path.home() / ".aicodebot")))
    # Make the directory if it doesn't exist
    if not data_dir.exists():
        logger.debug(f"Creating local data directory {data_dir}")
        data_dir.mkdir()
        # Create the subdirectories
        (data_dir / "repos").mkdir()
        (data_dir / "vector_stores").mkdir()

    return data_dir


def get_config_file():
    return Path(os.getenv("AICODEBOT_CONFIG_FILE", get_local_data_dir() / "config.yaml"))


def read_config():
    """Read the config file and return its contents as a dictionary."""
    config_file = get_config_file()
    logger.debug(f"Using config file {config_file}")
    if config_file.exists():
        logger.debug(f"Config file {config_file} exists")
        with Path(config_file).open("r") as f:
            out = yaml.safe_load(f)

            # Load the session data
            out["session"] = Session.read()
            return out
    else:
        logger.debug(f"Config file {config_file} does not exist")
        return None


class Session:
    """Read and write local session data"""

    @classmethod
    def get_config_file(cls):
        return Path(os.getenv("AICODEBOT_SESSION_FILE", str(get_local_data_dir() / "session.yaml")))

    @classmethod
    def read(cls):
        """Read the session file and return its contents as a dictionary."""
        session_file = cls.get_config_file()
        logger.debug(f"Using session file {session_file}")
        if session_file.exists():
            logger.debug(f"Session file {session_file} exists")
            with Path(session_file).open("r") as f:
                return yaml.safe_load(f)
        else:
            logger.debug(f"Session file {session_file} does not exist")
            return {}

    @classmethod
    def write(cls, session_data):
        session_file = cls.get_config_file()
        logger.debug(f"Writing session data to {session_file}")
        data = yaml.safe_dump(session_data)
        create_and_write_file(session_file, data, overwrite=True)
