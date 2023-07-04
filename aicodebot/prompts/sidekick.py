from langchain import PromptTemplate
from pathlib import Path

SIDEKICK_TEMPLATE = """You are a pair programming assistant named AICodeBot, acting as a sidekick to a human developer.
If you aren't sure what to do, you can ask the human for more clarification.

Relevant chat history:
{chat_history}
End chat history
{context}

Conversation with the human developer:
Human: {task}
AICodeBot:
"""


def generate_files_context(files):
    """Generate the files context for the sidekick prompt."""
    files_context = "Here are the relevant files we are working with in this session:\n"
    for file_name in files:
        contents = Path(file_name).read_text()
        files_context += f"--- START OF FILE: {file_name} ---\n"
        files_context += contents
        files_context += f"\n--- END OF FILE: {file_name} ---\n\n"
    return files_context


def generate_sidekick_prompt(task, files=None):
    """Generates a prompt for the sidekick workflow."""
    return PromptTemplate(template=SIDEKICK_TEMPLATE, input_variables=["chat_history", "task", "context"])
