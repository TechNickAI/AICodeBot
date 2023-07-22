from aicodebot.coder import Coder
from aicodebot.helpers import create_and_write_file
import os, pytest


def test_generate_directory_structure(tmp_path):
    # Create a file, a hidden file, another file, a .gitignore file, and a subdirectory in the temporary directory
    create_and_write_file(tmp_path / "file.txt", "This is a test file")
    create_and_write_file(tmp_path / ".hidden_file", "This is a hidden test file")
    create_and_write_file(tmp_path / "test_file", "This is another test file")
    create_and_write_file(tmp_path / ".gitignore", "*.txt\n")
    sub_dir = tmp_path / "sub_dir"
    sub_dir.mkdir()
    create_and_write_file(sub_dir / "sub_file", "This is a test file in a subdirectory")
    create_and_write_file(sub_dir / ".gitignore", "sub_file")

    # Call the function with the temporary directory and an ignore pattern
    directory_structure = Coder.generate_directory_structure(tmp_path, ignore_patterns=["*.txt"])

    # Check that the returned string is not empty
    assert directory_structure

    # Check that the returned string contains the name of the created subdirectory
    assert "- [Directory] sub_dir" in directory_structure

    # Check that the returned string does not contain the names of the ignored files
    assert "- [File] file.txt" not in directory_structure

    # Check that the returned string contains the name of the hidden file and the other file
    assert "- [File] .hidden_file" in directory_structure
    assert "- [File] test_file" in directory_structure

    # Check that the function respects .gitignore
    directory_structure_gitignore = Coder.generate_directory_structure(tmp_path)
    assert "- [File] file.txt" not in directory_structure_gitignore
    assert "- [File] sub_file" not in directory_structure_gitignore

    # Check that the function works correctly when use_gitignore is False
    directory_structure_no_gitignore = Coder.generate_directory_structure(tmp_path, use_gitignore=False)
    assert "- [File] file.txt" in directory_structure_no_gitignore
    assert "- [File] sub_file" in directory_structure_no_gitignore

    file_list = Coder.filtered_file_list(".", use_gitignore=True, ignore_patterns=[".git"])
    assert len(file_list) > 10


def test_get_token_length():
    text = ""
    assert Coder.get_token_length(text) == 0

    text = "Code with heart, align AI with humanity. ❤️🤖"
    assert Coder.get_token_length(text) == 14


def test_git_diff_context(temp_git_repo):
    os.chdir(temp_git_repo.working_dir)

    # Test empty repo (no commits, no staged files, no unstaged changes)
    diff = Coder.git_diff_context()
    assert not diff

    # Add a new file but don't stage it
    create_and_write_file("newfile.txt", "This is a new file.")
    diff = Coder.git_diff_context()
    assert not diff, "New file should not be included in diff until it is staged"

    # Stage the new file
    temp_git_repo.git.add("newfile.txt")
    diff = Coder.git_diff_context()
    assert "## New file added: newfile.txt" in diff
    assert "This is a new file." in diff

    # Commit the new file
    temp_git_repo.git.commit("-m", "Add newfile.txt")
    diff = Coder.git_diff_context()
    assert not diff

    # Test diff for a specific commit
    commit = temp_git_repo.head.commit.hexsha
    diff = Coder.git_diff_context(commit)
    assert "This is a new file." in diff

    # Modify the file but don't stage it
    create_and_write_file("newfile.txt", "This is a modified file.", overwrite=True)
    diff = Coder.git_diff_context()
    assert "## File changed: newfile.txt" in diff
    assert "This is a modified file." in diff

    # Stage the modified file
    temp_git_repo.git.add("newfile.txt")
    diff = Coder.git_diff_context()
    assert "## File changed: newfile.txt" in diff
    assert "This is a modified file." in diff

    # Commit the modified file
    temp_git_repo.git.commit("-m", "Modify newfile.txt")
    diff = Coder.git_diff_context()
    assert not diff

    # Rename the file but don't stage it
    temp_git_repo.git.mv("newfile.txt", "renamedfile.txt")
    diff = Coder.git_diff_context()
    assert "## File renamed: newfile.txt -> renamedfile.txt" in diff

    # Stage the renamed file
    temp_git_repo.git.add("renamedfile.txt")
    diff = Coder.git_diff_context()
    assert "## File renamed: newfile.txt -> renamedfile.txt" in diff

    # Commit the renamed file
    temp_git_repo.git.commit("-m", "Rename newfile.txt to renamedfile.txt")
    diff = Coder.git_diff_context()
    assert not diff

    # Test diff for a specific commit
    commit = temp_git_repo.head.commit.hexsha
    diff = Coder.git_diff_context(commit)
    assert "renamedfile.txt" in diff


def test_parse_github_url():
    # Test with https URL
    owner, repo = Coder.parse_github_url("https://github.com/owner/repo.git")
    assert owner == "owner"
    assert repo == "repo"

    # Test with git URL
    owner, repo = Coder.parse_github_url("git@github.com:owner/repo.git")
    assert owner == "owner"
    assert repo == "repo"

    # Test with invalid URL
    with pytest.raises(ValueError):
        Coder.parse_github_url("not a valid url")
