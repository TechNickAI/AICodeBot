from aicodebot.coder import Coder
from prompt_toolkit.completion import Completer, Completion


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
