from aicodebot import version as aicodebot_version
from aicodebot.cli import cli
import os, pytest


def test_version(cli_runner):
    result = cli_runner.invoke(cli, ["-V"])
    assert result.exit_code == 0
    assert aicodebot_version in result.output


@pytest.mark.skipif(os.getenv("OPENAI_API_KEY") is None, reason="Skipping live tests without an API key.")
def test_fun_fact(cli_runner):
    result = cli_runner.invoke(cli, ["fun-fact"])
    assert result.exit_code == 0


@pytest.mark.skipif(os.getenv("OPENAI_API_KEY") is None, reason="Skipping live tests without an API key.")
def test_alignment(cli_runner):
    result = cli_runner.invoke(cli, ["alignment"])
    assert result.exit_code == 0


def test_debug_success(cli_runner):
    result = cli_runner.invoke(cli, ["debug", "echo", "Hello, world!"])
    assert result.exit_code == 0
    assert "echo Hello, world!" in result.output
    assert "The command completed successfully." in result.output


@pytest.mark.skipif(os.getenv("OPENAI_API_KEY") is None, reason="Skipping live tests without an API key.")
def test_debug_failure(cli_runner):
    result = cli_runner.invoke(cli, ["debug", "ls", "-9"])
    assert result.exit_code > 0
    assert "ls -9" in result.output
