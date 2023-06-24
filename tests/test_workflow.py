from aicodebot.cli import cli
from git import Repo
from pathlib import Path
import os, pytest


@pytest.mark.skipif(os.getenv("OPENAI_API_KEY") is None, reason="Skipping live tests without an API key.")
def test_commit_command(cli_runner, temp_git_repo):
    with cli_runner.isolated_filesystem():
        os.chdir(temp_git_repo.working_dir)  # change to the temporary repo directory
        with Path.open("test.txt", "a") as f:
            f.write("Adding a new line.")
        result = cli_runner.invoke(cli, ["commit", "-y"])
        assert result.exit_code == 0
        assert "The following files will be committed:\ntest.txt" in result.output

        # Check the last commit message in the repository
        repo = Repo(temp_git_repo.working_dir)
        last_commit_message = repo.head.commit.message
        assert len(last_commit_message) > 10
