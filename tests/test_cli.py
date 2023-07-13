from aicodebot import version as aicodebot_version
from aicodebot.cli import cli
from aicodebot.config import read_config
from aicodebot.helpers import create_and_write_file
from aicodebot.prompts import DEFAULT_PERSONALITY
from git import Repo
from pathlib import Path
import json, os, pytest


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Skipping live tests without an API key.")
def test_alignment(cli_runner):
    result = cli_runner.invoke(cli, ["alignment", "-t", "50"])
    assert result.exit_code == 0, f"Output: {result.output}"


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="skipping live tests without an api key.")
def test_configure(cli_runner, tmp_path, monkeypatch):
    key = os.getenv("OPENAI_API_KEY")

    temp_config_file = Path(tmp_path / ".aicodebot.test.yaml")
    # set aicodebot_config_file to the temp config file
    monkeypatch.setenv("AICODEBOT_CONFIG_FILE", str(temp_config_file))

    assert read_config() is None

    # run the setup command, should work with the env var set
    result = cli_runner.invoke(cli, ["configure"])

    # check if the command was successful
    assert result.exit_code == 0, f"output: {result.output}"
    # check if the config file was created
    assert Path(temp_config_file).exists()

    # load the config file
    config_data = read_config()
    # check if the config file contains the correct data
    assert config_data["openai_api_key"] == key
    assert config_data["personality"] == DEFAULT_PERSONALITY.name

    # remove the config file
    Path.unlink(temp_config_file)
    assert read_config() is None

    # now unset the env var and run the command again with it passed as a flag
    monkeypatch.setenv("OPENAI_API_KEY", "")
    assert not os.getenv("OPENAI_API_KEY")

    result = cli_runner.invoke(cli, ["configure", "--openai-api-key", key])
    assert result.exit_code == 0, f"output: {result.output}"

    # load the config file
    config_data = read_config()
    # check if the config file contains the correct data
    assert config_data["openai_api_key"] == key
    assert config_data["personality"] == DEFAULT_PERSONALITY.name


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Skipping live tests without an API key.")
def test_debug_success(cli_runner):
    result = cli_runner.invoke(cli, ["debug", "echo", "Hello, world!"])
    assert result.exit_code == 0, f"Output: {result.output}"
    assert "echo Hello, world!" in result.output
    assert "The command completed successfully." in result.output


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Skipping live tests without an API key.")
def test_debug_failure(cli_runner):
    result = cli_runner.invoke(cli, ["debug", "ls", "-9"])
    assert result.exit_code > 0, f"Output: {result.output}"
    assert "ls -9" in result.output


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Skipping live tests without an API key.")
def test_fun_fact(cli_runner):
    result = cli_runner.invoke(cli, ["fun-fact", "-t", "50"])
    assert result.exit_code == 0, f"Output: {result.output}"


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Skipping live tests without an API key.")
def test_commit(cli_runner, temp_git_repo):
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
        result = cli_runner.invoke(cli, ["review", "-t", "100"])

        # Check that the review command ran successfully
        assert result.exit_code == 0
        assert len(result.output) > 20

        # Again with json output
        result = cli_runner.invoke(cli, ["review", "-t", "100", "--output-format", "json"])

        assert result.exit_code == 0
        # Check if it's valid json
        parsed = json.loads(result.output)
        assert parsed["review_status"] in ["PASSED", "COMMENTS"]


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Skipping live tests without an API key.")
def test_sidekick(cli_runner):
    # Define a mock request and file context
    mock_request = "What is 3 + 2? Just give me the answer, nothing else. Use a number, not text"
    mock_files = [".gitignore"]

    # Invoke the sidekick command
    result = cli_runner.invoke(cli, ["sidekick", "-t", "100", "--request", mock_request] + mock_files)

    assert result.exit_code == 0, f"Output: {result.output}"
    assert "5" in result.output


def test_version(cli_runner):
    result = cli_runner.invoke(cli, ["-V"])
    assert result.exit_code == 0, f"output: {result.output}"
    assert aicodebot_version in result.output
