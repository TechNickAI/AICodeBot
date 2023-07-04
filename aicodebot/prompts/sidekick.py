from langchain import PromptTemplate

SIDEKICK_PREFIX = """You are a pair programming assistant named AICodeBot, acting as a sidekick to a human developer.
If you aren't sure what to do, you can ask the human for more clarification.

Relevant history:
{history}
End History

Conversation with the human developer:
Human: {task}
AICodeBot:
"""


def generate_sidekick_prompt(task, files=None):
    """Generates a prompt for the sidekick workflow."""
    return PromptTemplate(template=SIDEKICK_PREFIX, input_variables=["history", "task"])
