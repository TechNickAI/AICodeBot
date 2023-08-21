from aicodebot.helpers import create_and_write_file
from aicodebot.input import Chat
from aicodebot.output import get_console
from io import StringIO
from pathlib import Path
from tests.conftest import in_temp_directory
import pyperclip, pytest, textwrap


class MockConsole:
    warning_style = error_style = bot_style = "none"

    def __init__(self):
        self.output = []
        self.console = get_console(file=StringIO(), force_terminal=True)  # we need to create a console object

    def print(self, message, style=None):  # noqa: A003
        self.console.print(message)
        self.output.append(self.console.file.getvalue())  # we get the value from the console
        self.console.file.truncate(0)  # we clear the console
        self.console.file.seek(0)  # we reset the cursor


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


def test_parse_human_input_files(chat, tmp_path, monkeypatch):
    monkeypatch.setenv("AICODEBOT_CONFIG_FILE", str(Path(__file__).parent / "test_config.yaml"))
    with in_temp_directory(tmp_path):
        create_and_write_file(tmp_path / "file.txt", "text")

        assert chat.parse_human_input("/add file.txt") == chat.CONTINUE
        assert chat.file_context == {"file.txt"}

        assert chat.parse_human_input("/files") == chat.CONTINUE

        assert chat.parse_human_input("/drop file.txt") == chat.CONTINUE
        assert chat.file_context == set()


def test_parse_human_input_commands(chat):
    # Test /sh command
    assert chat.parse_human_input("/sh ls") == chat.CONTINUE

    # Test /help command
    assert chat.parse_human_input("/help") == chat.CONTINUE

    # Test /quit command
    assert chat.parse_human_input("/quit") == chat.BREAK


def test_apply_subcommand(chat, temp_git_repo):
    with in_temp_directory(temp_git_repo.working_dir):
        # Create a file to be modified
        mod_file = Path("mod_file.txt")
        mod_file.write_text("AICodeBot is your coding sidekick.\nIt is here to make your coding life easier.\n")

        # Create a patch to modify the file
        mod_patch = textwrap.dedent(
            """
            --- a/mod_file.txt
            +++ b/mod_file.txt
            @@ -1,2 +1,3 @@
             AICodeBot is your coding sidekick.
             It is here to make your coding life easier.
            +It is now even better!
            """
        ).lstrip()
        # Add the patch to the chat (simulating it coming in from the LM response)
        chat.diff_blocks = [mod_patch]

        # Apply the patch using the /apply command
        assert chat.parse_human_input("/apply") == chat.CONTINUE

        # Check if the file was properly modified
        assert "It is now even better!" in mod_file.read_text()


def test_copy_subcommand(chat, temp_git_repo):
    try:
        pyperclip.copy("foo")
        assert pyperclip.paste() == "foo"
    except pyperclip.PyperclipException:
        pytest.skip("pyperclip not available on this operating system")

    with in_temp_directory(temp_git_repo.working_dir):
        # Add the patch to the chat (simulating it coming in from the LM response)
        chat.code_blocks = ["code block 1", "code block 2"]

        # Apply the patch using the /apply command
        assert chat.parse_human_input("/copy") == chat.CONTINUE

        assert pyperclip.paste() == "\n".join(chat.code_blocks)  # lint-ignore
