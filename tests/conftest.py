from aicodebot.helpers import create_and_write_file
from click.testing import CliRunner
from git import Repo
import pytest


@pytest.fixture
def cli_runner():
    # Create a Click CLI runner that can be used to invoke the CLI
    return CliRunner()


@pytest.fixture
def temp_git_repo(tmp_path):
    # Create a temporary git repository that can be used for testing
    repo = Repo.init(tmp_path)
    with repo.config_writer() as git_config:
        git_config.set_value("user", "name", "AICodeBot Test")
        git_config.set_value("user", "email", "test@aicodebot.dev")

    create_and_write_file(tmp_path / "initial_commit.txt", "This is a test file.")
    repo.index.add(["initial_commit.txt"])
    repo.index.commit("Initial commit")

    return repo
