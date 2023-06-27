from pathlib import Path
import subprocess, tiktoken


def get_token_length(text, model="gpt-3.5-turbo"):
    """Get the number of tokens in a string using the tiktoken library."""
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)


def git_diff_context(commit=None):
    """Get a text representation of the git diff for the current commit or staged files, including new files"""
    base_git_diff = ["git", "diff", "-U10"]  # Tell diff to provide 10 lines of context

    if commit:
        # If a commit is provided, just get the diff for that commit
        return exec_and_get_output(["git", "show", commit])
    else:
        # Otherwise, get the diff for the staged files, or if there are none, the diff for the unstaged files
        staged_files = exec_and_get_output(["git", "diff", "--cached", "--name-only"]).splitlines()
        if staged_files:
            # If there are staged files, get the diff for those files
            diff_type = "--cached"
        else:
            diff_type = "HEAD"

        file_status = exec_and_get_output(["git", "diff", diff_type, "--name-status"]).splitlines()

        diffs = []
        for status in file_status:
            status_code, file_name = status.split("\t")
            if status_code == "A":
                # If the file is new, include the entire file content
                contents = Path.read_text(file_name)
                diffs.append(f"## New file added: {file_name}")
                diffs.append(contents)
            else:
                # If the file is not new, get the diff
                diffs.append(f"## File changed: {file_name}")
                diffs.append(exec_and_get_output(base_git_diff + [diff_type, "--", file_name]))

        return "\n".join(diffs)


def exec_and_get_output(command):
    """Execute a command and return its output as a string."""
    result = subprocess.run(command, capture_output=True, text=True)  # noqa: S603
    if result.returncode != 0:
        raise Exception(f"Command '{' '.join(command)}' failed with error:\n{result.stderr}")  # noqa: TRY002
    return result.stdout
