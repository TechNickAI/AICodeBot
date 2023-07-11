from aicodebot.cli import cli
from aicodebot.helpers import create_and_write_file
from git import Repo
import os, pytest


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Skipping live tests without an API key.")
def test_commit_command(cli_runner, temp_git_repo):
    with cli_runner.isolated_filesystem():
        os.chdir(temp_git_repo.working_dir)  # change to the temporary repo directory
        create_and_write_file("test.txt", "This is a test file.")
        result = cli_runner.invoke(cli, ["commit", "-y"])
        assert result.exit_code == 0
        assert "The following files will be committed:\ntest.txt" in result.output

        # Check the last commit message in the repository
        repo = Repo(temp_git_repo.working_dir)
        last_commit_message = repo.head.commit.message
        assert len(last_commit_message) > 10


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Skipping live tests without an API key.")
def test_review(cli_runner, temp_git_repo):
    with cli_runner.isolated_filesystem():
        os.chdir(temp_git_repo.working_dir)  # change to the temporary repo directory

        # Add a new file
        create_and_write_file("test.txt", "Adding a new line.")

        repo = Repo(temp_git_repo.working_dir)
        # Stage the new file
        repo.git.add("test.txt")

        # Run the review command
        result = cli_runner.invoke(cli, ["review"])

        # Check that the review command ran successfully
        assert result.exit_code == 0
        assert len(result.output) > 20
