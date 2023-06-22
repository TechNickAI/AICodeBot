from aicodebot import version as aicodebot_version
from aicodebot.cli import cli
from click.testing import CliRunner
import os, pytest


@pytest.fixture
def runner():
    return CliRunner()


def test_version(runner):
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert aicodebot_version in result.output


@pytest.mark.skipif(os.getenv("OPENAI_API_KEY") is None, reason="Skipping live tests without an API key.")
def test_funfact(runner):
    result = runner.invoke(cli, ["fun-fact"])
    assert result.exit_code == 0


@pytest.mark.skipif(os.getenv("OPENAI_API_KEY") is None, reason="Skipping live tests without an API key.")
def test_alignment(runner):
    result = runner.invoke(cli, ["alignment"])
    assert result.exit_code == 0


def test_debug_success(runner):
    result = runner.invoke(cli, ["debug", "echo", "Hello, world!"])
    assert result.exit_code == 0
    assert "Running:\necho Hello, world!" in result.output
    assert "The command completed successfully." in result.output


@pytest.mark.skipif(os.getenv("OPENAI_API_KEY") is None, reason="Skipping live tests without an API key.")
def test_debug_failure(runner):
    result = runner.invoke(cli, ["debug", "ls", "-9"])
    assert result.exit_code == 0  # the debug command itself should still succeed
    assert "Running:\nls -9" in result.output
    assert "The command exited with status 1." in result.output
    # You might also want to check that the output includes the expected error message,
    # and that it includes some advice from ChatGPT.
