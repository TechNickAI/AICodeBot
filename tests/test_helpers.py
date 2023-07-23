from aicodebot.helpers import create_and_write_file, exec_and_get_output
from pathlib import Path
import pytest


def test_create_and_write_file(tmp_path):
    # Test creating a file that does not exist
    filename = tmp_path / "test.txt"
    text = "This is a test file."
    create_and_write_file(filename, text)
    assert Path(filename).exists()
    assert Path(filename).read_text() == text

    # Test creating a file that already exists with overwrite=True
    text = "This is a new test file."
    create_and_write_file(filename, text, overwrite=True)
    assert Path(filename).exists()
    assert Path(filename).read_text() == text

    # Test creating a file that already exists with overwrite=False
    with pytest.raises(ValueError):
        create_and_write_file(filename, text, overwrite=False)


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
