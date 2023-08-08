from aicodebot.coder import Coder
from aicodebot.lm import token_size
from pathlib import Path
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
from rich.panel import Panel
from rich.table import Table
import click, humanize, pyperclip, subprocess


class Chat:
    console = files = code_blocks = diff_blocks = raw_response = None

    CONTINUE = 1  # Continue to the next iteration of the while loop
    BREAK = -1  # Break out of the while loop (quit)

    def __init__(self, console, files):
        self.console = console
        self.files = set(files)

    def parse_human_input(self, human_input):  # noqa: PLR0911, PLR0915
        human_input = human_input.strip()

        if not human_input:
            return self.CONTINUE

        if human_input.startswith("/"):
            cmd = human_input.lower().split()[0]

            # ------------------------------ Handle commands ----------------------------- #
            if cmd in ["/add", "/drop"]:
                # Get the filename
                # If they didn't specify a file, then ignore
                try:
                    filenames = human_input.split()[1:]
                except IndexError:
                    self.console.print(Panel(f"{cmd} requires a file name", style=self.console.error_style))
                    return self.CONTINUE

                # If the file doesn't exist, or we can't open it, let them know
                for filename in filenames:
                    if cmd == "/add":
                        try:
                            # Test opening the file
                            with Path(filename).open("r"):
                                self.files.add(filename)
                                self.console.print(Panel(f"✅ Added '{filename}' to the list of files."))
                        except OSError as e:
                            self.console.print(
                                f"Unable to open '{filename}': {e.strerror}", style=self.console.error_style
                            )
                            return self.CONTINUE

                    elif cmd == "/drop":
                        # Drop the file from the list
                        self.files.discard(filename)
                        self.console.print(Panel(f"✅ Dropped '{filename}' from the list of files."))

                self.show_file_context()
                return self.CONTINUE

            elif cmd == "/apply":
                if not self.diff_blocks:
                    self.console.print("No diff blocks to apply.", style=self.console.error_style)
                else:
                    count = 0
                    for diff_block in self.diff_blocks:
                        # Apply the diff with git apply
                        count += 1
                        if Coder.apply_patch(diff_block):
                            self.console.print(Panel(f"✅ change {count} applied."))
                return self.CONTINUE

            elif cmd == "/copy":
                if not self.code_blocks:
                    self.console.print("No code blocks to copy.", style=self.console.error_style)
                else:
                    to_copy = "\n".join(self.code_blocks)
                    pyperclip.copy(to_copy)
                    self.console.print(Panel("✅ Copied the code block(s) to the clipboard."))
                return self.CONTINUE

            elif cmd == "/edit":
                return click.edit()

            elif cmd == "/files":
                self.show_file_context()
                return self.CONTINUE

            elif cmd == "/help":
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Command")
                table.add_column("Description")
                for command, description in SidekickCompleter.commands.items():
                    table.add_row(command, description)
                self.console.print(table)
                return self.CONTINUE

            elif cmd == "/sh":
                # Strip off the /sh and any leading/trailing whitespace
                shell_command = human_input[3:].strip()

                if not shell_command:
                    return self.CONTINUE

                # Execute the shell command and let the output go directly to the console
                subprocess.run(shell_command, shell=True)  # noqa: S602
                return self.CONTINUE

            elif cmd == "/raw":
                # Print the raw response from the LM without any formatting
                print(self.raw_response)  # noqa: T201
                return self.CONTINUE

            elif cmd == "/quit":
                return self.BREAK

        if human_input.lower()[-2:] == r"\e":
            # If the text ends wit then we want to edit it
            return click.edit(human_input[:-2])

        # No magic found, pass to the LM
        return human_input

    def show_file_context(self):
        if not self.files:
            return

        self.console.print("Files loaded in this session:")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("File")
        table.add_column("Token Size")
        for file in self.files:
            tokens = token_size(Path(file).read_text())
            table.add_row(file, humanize.intcomma(tokens))
        self.console.print(table)


class SidekickCompleter(Completer):
    """A custom prompt_toolkit completer for sidekick.
    Handles the autocomplete for the sidekick commands and file names.
    """

    files = []  # List of files that we have loaded in the current context
    _project_files = None
    commands = {
        "/help": "Print this help message",
        "/edit": "Use your editor for multi line input",
        "/add": "Add a file to the context for the LM",
        "/drop": "Remove a file from the context for the LM",
        "/apply": "Apply (patch) the recommended diff blocks to the files",
        "/copy": "Copy the code blocks from the response to the clipboard",
        "/review": "Do a code review on your [un]staged changes",
        "/commit": "Generate a commit message based on your [un]staged changes",
        "/sh": "Execute a shell command",
        "/files": "Show the list of files currently loaded in the context",
        "/quit": "👋 Say Goodbye!",
    }

    @property
    def project_files(self):
        if self._project_files is None:
            # If we are in a git repo, then use the gitignore file to filter the list of files
            if Coder.is_inside_git_repo():
                self._project_files = Coder.filtered_file_list(".", use_gitignore=True, ignore_patterns=[".git"])
            else:
                # We don't want to walk through a ginormous directory tree, so no auto complete if not in a repo
                self._project_files = []

        return self._project_files

    def get_completions(self, document, complete_event):
        # Get the text before the cursor
        text = document.text_before_cursor

        # If the text starts with a slash, it's a command
        if text.startswith("/"):
            for command, description in self.commands.items():
                if command.startswith(text):
                    yield Completion(command, start_position=-len(text), display_meta=description)

        if text.startswith("/add "):
            # For /add autocomplete the file name from the project file listing
            # Get the list of files in the current directory, filtered by the .gitignore file
            for file in self.project_files:
                if str(file).startswith(text.split()[-1]):
                    yield Completion(str(file), start_position=-len(text.split()[-1]))

        elif text.startswith("/drop "):
            # For /drop, use the current context files for autocomplete
            for file in self.files:
                if file.startswith(text.split()[-1]):
                    yield Completion(file, start_position=-len(text.split()[-1]))

        elif text.startswith(("/review ", "/commit ")):
            # For /review and /commit, use the staged/unstaged files for autocomplete
            changed_files = Coder.git_staged_files() + Coder.git_unstaged_files()
            for file in changed_files:
                if file.startswith(text.split()[-1]):
                    yield Completion(file, start_position=-len(text.split()[-1]))


def generate_prompt_session():
    history_file = Path.home() / ".aicodebot_request_history"
    return PromptSession(
        history=FileHistory(history_file),
        completer=SidekickCompleter(),
        auto_suggest=AutoSuggestFromHistory(),
        message=[("class:prompt", "🤖 ➤ ")],
    )
