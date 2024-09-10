from aicodebot import version as aicodebot_version
from aicodebot.cli import cli
from aicodebot.config import read_config
from aicodebot.helpers import create_and_write_file
from aicodebot.prompts import DEFAULT_PERSONALITY
from git import Repo
from pathlib import Path
from tests.conftest import in_temp_directory
import json, os, pytest

# smaller than the default size to speed up the tests
TEST_RESPONSE_TOKEN_SIZE = 150


@pytest.mark.vcr()
def test_alignment(cli_runner, monkeypatch):
    monkeypatch.setenv("AICODEBOT_CONFIG_FILE", str(Path(__file__).parent / "test_config.yaml"))
    result = cli_runner.invoke(cli, ["alignment", "-t", "50"])
    assert result.exit_code == 0, f"Output: {result.output}"


@pytest.mark.vcr()
def test_commit(cli_runner, temp_git_repo, monkeypatch):
    monkeypatch.setenv("AICODEBOT_CONFIG_FILE", str(Path(__file__).parent / "test_config.yaml"))
    with cli_runner.isolated_filesystem() and in_temp_directory(temp_git_repo.working_dir):
        # Scenario 1: Only unstaged changes
        create_and_write_file("test1.txt", "This is a test file.")
        repo = Repo(temp_git_repo.working_dir)
        repo.git.add("test1.txt")  # stage the new file
        result = cli_runner.invoke(cli, ["commit", "-y", "-t", 250, "test1.txt"])
        assert result.exit_code == 0, f"Output: {result.output}"
        # Check if the file was committed by looking in git
        assert "test1.txt" in repo.git.ls_files()

        # Scenario 2: Both staged and unstaged changes
        create_and_write_file("test2.txt", "This is another test file.")
        repo = Repo(temp_git_repo.working_dir)
        repo.git.add("test2.txt")  # stage the new file
        create_and_write_file("test3.txt", "This is yet another test file.")  # unstaged file
        result = cli_runner.invoke(cli, ["commit", "-y", "-t", 250])
        assert result.exit_code == 0, f"Output: {result.output}"
        assert "test2.txt" in repo.git.ls_files()

        # Scenario 3: No changes at all
        result = cli_runner.invoke(cli, ["commit", "-y", "-t", 250])
        assert result.exit_code == 0, f"Output: {result.output}"
        assert "No changes" in result.output


@pytest.mark.vcr()
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
    Path(temp_config_file).unlink()
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


def test_debug_success(cli_runner, monkeypatch):
    monkeypatch.setenv("AICODEBOT_CONFIG_FILE", str(Path(__file__).parent / "test_config.yaml"))
    result = cli_runner.invoke(cli, ["debug", "echo", "Hello, world!"])
    assert result.exit_code == 0, f"Output: {result.output}"
    assert "echo Hello, world!" in result.output
    assert "The command completed successfully." in result.output


@pytest.mark.vcr()
def test_debug_failure(cli_runner, monkeypatch):
    monkeypatch.setenv("AICODEBOT_CONFIG_FILE", str(Path(__file__).parent / "test_config.yaml"))
    result = cli_runner.invoke(cli, ["debug", "ls", "-9"])
    assert result.exit_code > 0, f"Output: {result.output}"
    assert "ls -9" in result.output


@pytest.mark.vcr()
def test_review(cli_runner, temp_git_repo, monkeypatch):
    monkeypatch.setenv("AICODEBOT_CONFIG_FILE", str(Path(__file__).parent / "test_config.yaml"))
    with cli_runner.isolated_filesystem() and in_temp_directory(temp_git_repo.working_dir):
        # Add a new file
        create_and_write_file("test.txt", "Adding a new line.")

        repo = Repo(temp_git_repo.working_dir)
        # Stage the new file
        repo.git.add("test.txt")

        # Run the review command
        result = cli_runner.invoke(cli, ["review", "-t", TEST_RESPONSE_TOKEN_SIZE, "test.txt"])

        # Check that the review command ran successfully
        assert result.exit_code == 0, f"Output: {result.output}"
        assert len(result.output) > 20

        # Again with json output
        result = cli_runner.invoke(
            # Larger test token size to make sure the response is valid json
            cli,
            ["review", "-t", TEST_RESPONSE_TOKEN_SIZE * 3, "--output-format", "json", "test.txt"],
        )

        assert result.exit_code == 0, f"Output: {result.output}"
        # Check if it's valid json
        parsed = json.loads(result.output)
        assert parsed["review_status"] in ["PASSED"]


@pytest.mark.vcr()
def test_sidekick(cli_runner, monkeypatch):
    monkeypatch.setenv("AICODEBOT_CONFIG_FILE", str(Path(__file__).parent / "test_config.yaml"))
    # Define a mock request and file context
    mock_request = "What is 3 + 2? Just give me the answer, nothing else. Use a number, not text"
    mock_files = [".gitignore"]

    # Invoke the sidekick command
    result = cli_runner.invoke(cli, ["sidekick", "--request", mock_request] + mock_files)

    assert result.exit_code == 0, f"Output: {result.output}"
    assert "5" in result.output


def test_version(cli_runner, monkeypatch):
    monkeypatch.setenv("AICODEBOT_CONFIG_FILE", str(Path(__file__).parent / "test_config.yaml"))
    result = cli_runner.invoke(cli, ["-V"])
    assert result.exit_code == 0, f"output: {result.output}"
    assert aicodebot_version in result.output
