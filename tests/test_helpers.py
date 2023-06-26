from aicodebot.helpers import exec_and_get_output, get_token_length, git_diff_context
from git import Repo
from pathlib import Path
import os, pytest


def test_get_token_length():
    text = ""
    assert get_token_length(text) == 0

    text = "Code with heart, align AI with humanity. ❤️🤖"
    assert get_token_length(text) == 14


def test_git_diff_context(cli_runner, temp_git_repo):
    with cli_runner.isolated_filesystem():
        os.chdir(temp_git_repo.working_dir)  # change to the temporary repo directory

        # Add a new file
        with Path.open("test.txt", "w") as f:
            f.write("Adding a new line.")

        # Get the diff for changes
        diff = git_diff_context()
        assert "Adding a new line." in diff

        repo = Repo(temp_git_repo.working_dir)

        # Stage the changes
        repo.git.add("test.txt")
        diff = git_diff_context()
        assert "Adding a new line." in diff

        # Commit the changes
        repo.git.commit("-m", "Add test.txt")

        # Get the diff for the commit
        commit = repo.head.commit.hexsha
        diff = git_diff_context(commit)
        assert "Adding a new line." in diff

        # Modify the file
        with Path.open("test.txt", "a") as f:
            f.write("Adding another line.")

        # Get the diff for changes
        diff = git_diff_context()
        assert "Adding another line." in diff

        # Commit the changes
        repo.git.add("test.txt")
        repo.git.commit("-m", "Modify test.txt")

        # Get the diff for the commit
        commit = repo.head.commit.hexsha
        diff = git_diff_context(commit)
        assert "Adding another line." in diff


def test_exec_and_get_output_success():
    # Test a command that should succeed
    command = ["echo", "Hello, World!"]
    output = exec_and_get_output(command)
    assert output.strip() == "Hello, World!"


def test_exec_and_get_output_failure():
    # Test a command that should fail
    command = ["ls", "/nonexistent_directory"]
    with pytest.raises(Exception) as excinfo:
        exec_and_get_output(command)
    assert "Command 'ls /nonexistent_directory' failed with error:" in str(excinfo.value)
