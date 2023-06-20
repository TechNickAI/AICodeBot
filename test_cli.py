from cli import joke, version
from click.testing import CliRunner
from setup import __version__


def test_version():
    runner = CliRunner()
    result = runner.invoke(version)
    assert result.exit_code == 0
    assert __version__ in result.output


def test_joke():
    runner = CliRunner()
    result = runner.invoke(joke)
    assert result.exit_code == 0
