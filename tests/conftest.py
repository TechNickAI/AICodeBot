from click.testing import CliRunner
from git import Repo
from pathlib import Path
import pytest


@pytest.fixture
def cli_runner():
    # Create a Click CLI runner that can be used to invoke the CLI
    return CliRunner()


def create_and_write_file(filename, text):
    with Path(filename).open("w") as f:
        f.write(text)


@pytest.fixture
def temp_git_repo(tmp_path):
    # Create a temporary git repository that can be used for testing
    repo = Repo.init(tmp_path)
    with repo.config_writer() as git_config:
        git_config.set_value("user", "name", "AICodeBot Test")
        git_config.set_value("user", "email", "test@aicodebot.dev")

    with Path.open(tmp_path / "initial_commit.txt", "w") as f:
        f.write("This is a test file.")
    repo.index.add(["initial_commit.txt"])
    repo.index.commit("Initial commit")

    return repo
