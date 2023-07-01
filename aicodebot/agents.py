""" LangChain Agent Setup """
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.agents.agent_toolkits import FileManagementToolkit

SIDEKICK_PROMPT_PREFIX = """
You are a programming assistant named AICodeBot, acting as a sidekick to a human developer.
You are running in the local repository, so you can interact with the files in the repository
to get more information about the code. If you aren't sure what to do, you can ask the human.

If asking the human for more clarification would produce better results, you can ask the human for more information.

Important: When you respond calling a tool, you should make sure your response is properly json formatted, ie escape
quotes and newlines.

Before writing any local files, you should ALWAYS check with the human developer first, explaining what you are doing.
"""


def get_agent(name, llm, verbose):
    """Get the agent by name"""
    if name == "sidekick":
        # Set up the tools. Basic local file management first
        tools = FileManagementToolkit(selected_tools=["read_file", "write_file", "list_directory"]).get_tools()
        tools += load_tools(["human"])  # Human input

        # Set up the agent
        return initialize_agent(
            tools,
            llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=verbose,
            return_intermediate_steps=True,
            agent_kwargs={"prefix": SIDEKICK_PROMPT_PREFIX, "verbose": verbose},
        )
    else:
        raise ValueError(f"Agent {name} not found")
