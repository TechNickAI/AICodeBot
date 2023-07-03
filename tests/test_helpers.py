from aicodebot.helpers import exec_and_get_output, get_token_length, git_diff_context
from pathlib import Path
import os, pytest


def test_get_token_length():
    text = ""
    assert get_token_length(text) == 0

    text = "Code with heart, align AI with humanity. ❤️🤖"
    assert get_token_length(text) == 14


def create_and_write_file(filename, text):
    with Path(filename).open("w") as f:
        f.write(text)


def test_git_diff_context(temp_git_repo):
    os.chdir(temp_git_repo.working_dir)

    # Test empty repo (no commits, no staged files, no unstaged changes)
    diff = git_diff_context()
    assert diff == ""

    # Add a new file but don't stage it
    create_and_write_file("newfile.txt", "This is a new file.")
    diff = git_diff_context()
    assert diff == "", "New file should not be included in diff until it is staged"

    # Stage the new file
    temp_git_repo.git.add("newfile.txt")
    diff = git_diff_context()
    assert "## New file added: newfile.txt" in diff
    assert "This is a new file." in diff

    # Commit the new file
    temp_git_repo.git.commit("-m", "Add newfile.txt")
    diff = git_diff_context()
    assert diff == ""

    # Test diff for a specific commit
    commit = temp_git_repo.head.commit.hexsha
    diff = git_diff_context(commit)
    assert "This is a new file." in diff

    # Modify the file but don't stage it
    create_and_write_file("newfile.txt", "This is a modified file.")
    diff = git_diff_context()
    assert "## File changed: newfile.txt" in diff
    assert "This is a modified file." in diff

    # Stage the modified file
    temp_git_repo.git.add("newfile.txt")
    diff = git_diff_context()
    assert "## File changed: newfile.txt" in diff
    assert "This is a modified file." in diff

    # Commit the modified file
    temp_git_repo.git.commit("-m", "Modify newfile.txt")
    diff = git_diff_context()
    assert diff == ""

    # Rename the file but don't stage it
    temp_git_repo.git.mv("newfile.txt", "renamedfile.txt")
    diff = git_diff_context()
    assert "## File renamed: newfile.txt -> renamedfile.txt" in diff

    # Stage the renamed file
    temp_git_repo.git.add("renamedfile.txt")
    diff = git_diff_context()
    assert "## File renamed: newfile.txt -> renamedfile.txt" in diff

    # Commit the renamed file
    temp_git_repo.git.commit("-m", "Rename newfile.txt to renamedfile.txt")
    diff = git_diff_context()
    assert diff == ""

    # Test diff for a specific commit
    commit = temp_git_repo.head.commit.hexsha
    diff = git_diff_context(commit)
    assert "renamedfile.txt" in diff


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
