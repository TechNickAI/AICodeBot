from aicodebot import version as aicodebot_version
from aicodebot.cli import cli
from aicodebot.helpers import read_config
from pathlib import Path
import os, pytest


def test_version(cli_runner):
    result = cli_runner.invoke(cli, ["-V"])
    assert result.exit_code == 0, f"Output: {result.output}"
    assert aicodebot_version in result.output


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Skipping live tests without an API key.")
def test_fun_fact(cli_runner):
    result = cli_runner.invoke(cli, ["fun-fact", "-t", "50"])
    assert result.exit_code == 0, f"Output: {result.output}"


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Skipping live tests without an API key.")
def test_alignment(cli_runner):
    result = cli_runner.invoke(cli, ["alignment", "-t", "50"])
    assert result.exit_code == 0, f"Output: {result.output}"


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
def test_sidekick(cli_runner):
    # Define a mock request and file context
    mock_request = "What is 3 + 2? Just give me the answer, nothing else. Use a number, not text"
    mock_files = [".gitignore"]

    # Invoke the sidekick command
    result = cli_runner.invoke(cli, ["sidekick", "-t", "100", "--request", mock_request] + mock_files)

    assert result.exit_code == 0, f"Output: {result.output}"
    assert "5" in result.output


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Skipping live tests without an API key.")
def test_configure(cli_runner, tmp_path, monkeypatch):
    key = os.getenv("OPENAI_API_KEY")

    temp_config_file = Path(tmp_path / ".aicodebot.test.yaml")
    # set AICODEBOT_CONFIG_FILE to the temp config file
    monkeypatch.setenv("AICODEBOT_CONFIG_FILE", str(temp_config_file))

    assert read_config() is None

    # Run the setup command, should work with the env var set
    result = cli_runner.invoke(cli, ["configure"])

    # Check if the command was successful
    assert result.exit_code == 0, f"Output: {result.output}"
    # Check if the config file was created
    assert Path(temp_config_file).exists()

    # Load the config file
    config_data = read_config()
    # Check if the config file contains the correct data
    assert config_data["openai_api_key"] == key
    assert config_data["personality"] == "Her"

    # Remove the config file
    Path.unlink(temp_config_file)
    assert read_config() is None

    # Now unset the env var and run the command again with it passed as a flag
    monkeypatch.setenv("OPENAI_API_KEY", "")
    assert os.getenv("OPENAI_API_KEY") == ""

    result = cli_runner.invoke(cli, ["configure", "--openai-api-key", key])
    assert result.exit_code == 0, f"Output: {result.output}"

    # Load the config file
    config_data = read_config()
    # Check if the config file contains the correct data
    assert config_data["openai_api_key"] == key
    assert config_data["personality"] == "Her"
