from aicodebot.coder import Coder
from pathlib import Path
from prompt_toolkit.completion import Completer, Completion
import click, humanize, subprocess


class Chat:
    console = files = None

    CONTINUE = 1  # Continue to the next iteration of the while loop
    BREAK = -1  # Break out of the while loop (quit)

    def __init__(self, console, files):
        self.console = console
        self.files = set(files)

    def parse_human_input(self, human_input):  # noqa: PLR0911
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
                    self.console.print(f"{cmd} requires a file name", style=self.console.error_style)
                    return self.CONTINUE

                # If the file doesn't exist, or we can't open it, let them know
                for filename in filenames:
                    if cmd == "/add":
                        try:
                            # Test opening the file
                            with Path(filename).open("r"):
                                self.files.add(filename)
                                self.console.print(f"✅ Added '{filename}' to the list of files.")
                        except OSError as e:
                            self.console.print(
                                f"Unable to open '{filename}': {e.strerror}", style=self.console.error_style
                            )
                            return self.CONTINUE

                    elif cmd == "/drop":
                        # Drop the file from the list
                        self.files.discard(filename)
                        self.console.print(f"✅ Dropped '{filename}' from the list of files.")

                self.show_file_context()
                return self.CONTINUE

            elif cmd == "/edit":
                return click.edit()
            elif cmd == "/files":
                self.show_file_context()
                return self.CONTINUE

            elif cmd == "/sh":
                # Strip off the /sh and any leading/trailing whitespace
                shell_command = human_input[3:].strip()

                if not shell_command:
                    return self.CONTINUE

                # Execute the shell command and let the output go directly to the console
                subprocess.run(shell_command, shell=True)  # noqa: S602
                return self.CONTINUE

            elif cmd == "/quit":
                return self.BREAK

        if human_input.lower()[-2:] == r"\e":
            # If the text ends wit then we want to edit it
            return click.edit(human_input[:-2])

        # No magic found, pass to the LLM
        return human_input

    def show_file_context(self):
        if not self.files:
            return

        self.console.print("Files loaded in this session:")
        for file in self.files:
            token_length = Coder.get_token_length(Path(file).read_text())
            self.console.print(f"\t{file} ({humanize.intcomma(token_length)} tokens)")


class SidekickCompleter(Completer):
    """A custom prompt_toolkit completer for sidekick.
    Handles the autocomplete for the sidekick commands and file names.
    """

    files = []  # List of files that we have loaded in the current context
    project_files = Coder.filtered_file_list(".", use_gitignore=True, ignore_patterns=[".git"])
    commands = {
        "/edit": "Use your editor for multi line input",
        "/add": "Add a file to the context for the LLM",
        "/drop": "Remove a file from the context for the LLM",
        "/review": "Do a code review on your [un]staged changes",
        "/commit": "Generate a commit message based on your [un]staged changes",
        "/sh": "Execute a shell command",
        "/files": "Show the list of files currently loaded in the context",
        "/quit": "👋 Say Goodbye!",
    }

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
