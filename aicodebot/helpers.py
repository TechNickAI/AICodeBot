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
            status_parts = status.split("\t")
            status_code = status_parts[0][0]  # Get the first character of the status code
            if status_code == "A":
                # If the file is new, include the entire file content
                file_name = status_parts[1]
                contents = Path(file_name).read_text()
                diffs.append(f"## New file added: {file_name}")
                diffs.append(contents)
            elif status_code == "R":
                # If the file is renamed, get the diff and note the old and new names
                old_file_name, new_file_name = status_parts[1], status_parts[2]
                diffs.append(f"## File renamed: {old_file_name} -> {new_file_name}")
                diffs.append(exec_and_get_output(base_git_diff + [diff_type, "--", new_file_name]))
            elif status_code == "D":
                # If the file is deleted, note the deletion
                file_name = status_parts[1]
                diffs.append(f"## File deleted: {file_name}")
            else:
                # If the file is not new, renamed, or deleted, get the diff
                file_name = status_parts[1]
                diffs.append(f"## File changed: {file_name}")
                diffs.append(exec_and_get_output(base_git_diff + [diff_type, "--", file_name]))

        return "\n".join(diffs)


def exec_and_get_output(command):
    """Execute a command and return its output as a string."""
    result = subprocess.run(command, capture_output=True, text=True)  # noqa: S603
    if result.returncode != 0:
        raise Exception(f"Command '{' '.join(command)}' failed with error:\n{result.stderr}")  # noqa: TRY002
    return result.stdout
