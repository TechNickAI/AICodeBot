from aicodebot.helpers import exec_and_get_output
import pytest


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
