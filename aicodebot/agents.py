from aicodebot.coder import Coder
from aicodebot.learn import load_learned_repo
from aicodebot.prompts import get_personality_prompt
from langchain.agents import AgentExecutor, StructuredChatAgent, Tool
from langchain.agents.agent_toolkits import FileManagementToolkit
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA

SIDEKICK_AGENT_PREFIX = """
You are an AI coding assistant that helps developers write code. You are working in a local repo.
Respond to the human as helpfully and accurately as possible.
For the Final Answer, respond in markdown format.
You have access to the following tools:
"""
SIDEKICK_AGENT_SUFFIX = (
    get_personality_prompt()
    + """Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary.
    Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation:.
Thought:"""
)


class SidekickAgent(StructuredChatAgent):
    """Our agent that will be used to run the sidekick command

    It implements the following langchain features:
    [ ] Memory for chat history
    [X] Agentic actions (planned multi-step actions to achieve a goal)
    * Tools to gain additional information
        * Vector store retrieval
        [x] Read local files
        [ ] Git interaction
        [ ] Execute shell commands
        [ ] Browse the web
        * Interact with apis
            [ ] Github
            [ ] Sentry/Honeybadger
    * Tools to make changes
        [ ] Patch local files
        [ ] Shell commands
        [ ] Interact with the github api
    [ ] Displaying intermediate steps
    [ ] Handle parsing errors
    [ ] Streamed output
    """

    @classmethod
    def get_agent_executor(cls, learned_repos=None):
        model_name = Coder.get_llm_model_name(5_000)
        llm = Coder.get_llm(model_name, streaming=True, callbacks=[StreamingStdOutCallbackHandler()])
        tools = cls.get_sidekick_tools(llm, learned_repos)
        agent = cls.from_llm_and_tools(
            llm=llm,
            prefix=SIDEKICK_AGENT_PREFIX,
            suffix=SIDEKICK_AGENT_SUFFIX,
            tools=tools,
        )
        return AgentExecutor.from_agent_and_tools(agent=agent, tools=tools)

    @classmethod
    def get_sidekick_tools(cls, llm, learned_repos=None):
        tools = FileManagementToolkit(selected_tools=["read_file"]).get_tools()
        if learned_repos is not None:
            for repo_name in learned_repos:
                vector_store = load_learned_repo(repo_name)

                retrieval_chain = RetrievalQA.from_chain_type(
                    llm=llm, chain_type="stuff", retriever=vector_store.as_retriever()
                )
                tools.append(
                    Tool(
                        name=f"{repo_name}_vectorstore",
                        func=retrieval_chain.run,
                        description=f"Useful for when you need to answer questions about the {repo_name} repo. "
                        "Use a question as input.",
                    )
                )

        return tools
