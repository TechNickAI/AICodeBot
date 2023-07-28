from aicodebot.helpers import create_and_write_file
from aicodebot.input import Chat
from tests.conftest import in_temp_directory
import pytest


class MockConsole:
    def __init__(self):
        self.output = []

    def print(self, message, style=None):  # noqa: A003
        self.output.append(message)


@pytest.fixture
def chat():
    console = MockConsole()
    files = ()  # Initial argument from click is a tuple
    return Chat(console, files)


def test_parse_human_input(chat):
    # Test with a normal input
    input_data = "Hello, world!"
    assert chat.parse_human_input(input_data) == input_data

    # Test with an empty input
    input_data = ""
    assert chat.parse_human_input(input_data) == chat.CONTINUE


def test_parse_human_input_files(chat, tmp_path):
    with in_temp_directory(tmp_path):
        create_and_write_file(tmp_path / "file.txt", "text")

        assert chat.parse_human_input("/add file.txt") == chat.CONTINUE
        assert chat.files == set(["file.txt"])
        assert "✅ Added 'file.txt' to the list of files." in chat.console.output

        assert chat.parse_human_input("/files") == chat.CONTINUE
        assert "file.txt" in "".join(chat.console.output)

        assert chat.parse_human_input("/drop file.txt") == chat.CONTINUE
        assert chat.files == set()


def test_parse_human_input_commands(chat):
    # Test /sh command
    assert chat.parse_human_input("/sh ls") == chat.CONTINUE

    # Test /quit command
    assert chat.parse_human_input("/quit") == chat.BREAK
