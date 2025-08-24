import os
from contextlib import contextmanager
from pathlib import Path

import pytest
from click.testing import CliRunner
from git import Repo

from aicodebot.helpers import create_and_write_file


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


@contextmanager
def in_temp_directory(tmp_path):
    old_dir = Path.cwd()
    os.chdir(tmp_path)
    try:
        yield
    finally:
        os.chdir(old_dir)


@pytest.fixture(autouse=True)
def vcr_config():
    # Strip out the authorization header from the VCR cassettes, so we don't check in our API key
    return {"filter_headers": ["authorization", "openai-organization"]}
