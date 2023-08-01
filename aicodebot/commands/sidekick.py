from aicodebot.agents import SidekickAgent
from aicodebot.coder import Coder
from aicodebot.config import Session
from aicodebot.helpers import logger
from aicodebot.input import Chat, SidekickCompleter
from aicodebot.output import OurMarkdown, RichLiveCallbackHandler, get_console
from aicodebot.prompts import generate_files_context, get_prompt
from langchain.chains import LLMChain
from langchain.memory import ConversationTokenBufferMemory
from pathlib import Path
from prompt_toolkit import prompt as input_prompt
from prompt_toolkit.history import FileHistory
from rich.live import Live
import click, humanize, sys


@click.command
@click.option("-r", "--request", help="What to ask your sidekick to do")
@click.option("-n", "--no-files", is_flag=True, help="Don't automatically load any files for context")
@click.option("-m", "--max-file-tokens", type=int, default=10_000, help="Don't load files larger than this")
@click.option("-v", "--verbose", count=True)
@click.argument("files", nargs=-1, type=click.Path(exists=True, readable=True))
def sidekick(request, verbose, no_files, max_file_tokens, files):  # noqa: PLR0915
    """
    Coding help from your AI sidekick
    FILES: List of files to be used as context for the session
    """
    console = get_console()
    if not Coder.is_inside_git_repo():
        console.print("🛑 This command must be run from within a git repository.", style=console.error_style)
        sys.exit(1)

    console.print("This is an experimental feature. We love bug reports 😉", style=console.warning_style)

    # ----------------- Determine which files to use for context ----------------- #
    model_name = Coder.get_llm_model_name(-1, biggest_available=True)
    model_token_limit = Coder.get_model_token_limit(model_name)
    file_context_limit = model_token_limit * 0.75
    console.print(
        f"Using the [bold underline]{model_name}[/bold underline] model, "
        f"which has a {humanize.intcomma(model_token_limit)} token limit."
    )

    if files:  # User supplied list of files
        context = generate_files_context(files)
        file_token_size = Coder.get_token_length(context)
        if file_token_size > file_context_limit:
            raise click.ClickException(
                f"The file(s) you supplied are too large ({file_token_size} tokens). 😢 Try again with less files."
            )
    elif not no_files:
        # Determine which files to use for context automagically, with git
        session_data = Session.read()
        if session_data.get("files"):
            console.print("Using files from the last session for context.")
            files = session_data["files"]
        else:
            console.print("Using recent git commits and current changes for context.")
            files = Coder.auto_file_context(file_context_limit, max_file_tokens)

        context = generate_files_context(files)
        file_token_size = Coder.get_token_length(context)
    else:
        context = generate_files_context([])
        file_token_size = 0

    # Convert it from a list or a tuple to a set to remove duplicates
    files = set(files)
    # ----------------------------- Set up langchain ----------------------------- #

    # Generate the prompt and set up the model
    prompt = get_prompt("sidekick")
    memory_token_size = round(model_token_limit * 0.1)

    # Determine the max token size for the response
    def calc_response_token_size(files):
        file_token_size = 0
        for file in files:
            file_token_size += Coder.get_token_length(Path(file).read_text())
        prompt_token_size = Coder.get_token_length(prompt.template)
        logger.trace(
            f"File token size: {file_token_size}, memory token size: {memory_token_size}, "
            f"prompt token size: {prompt_token_size}, model token limit: {model_token_limit}"
        )
        out = model_token_limit - (memory_token_size + file_token_size + prompt_token_size)
        out = round(out * 0.95)  # Small buffer
        logger.debug(f"Response max token size: {out}")
        return out

    response_token_size = calc_response_token_size(files)

    llm = Coder.get_llm(model_name, verbose, response_token_size, streaming=True)
    memory = ConversationTokenBufferMemory(
        memory_key="chat_history", input_key="task", llm=llm, max_token_limit=memory_token_size
    )
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory, verbose=verbose)

    # ---------------------- Set up the chat loop and prompt --------------------- #
    chat = Chat(console, files)
    chat.show_file_context()
    languages = ",".join(Coder.identify_languages(files))

    console.print(
        "Enter a request for your AICodeBot sidekick. Type / to see available commands.\n",
        style=console.bot_style,
    )
    history_file = Path.home() / ".aicodebot_request_history"
    completer = SidekickCompleter()
    completer.files = files

    while True:  # continuous loop for multiple questions
        if request:
            human_input = request
        else:
            human_input = input_prompt("🤖 ➤ ", history=FileHistory(history_file), completer=completer)

        parsed_human_input = chat.parse_human_input(human_input)
        if parsed_human_input == chat.BREAK:
            break

        # Update the context for the new list of files
        context = generate_files_context(chat.files)
        languages = ",".join(Coder.identify_languages(chat.files))
        if completer.files != chat.files:
            completer.files = chat.files
            session_data = Session.read()
            session_data["files"] = list(chat.files)
            Session.write(session_data)

        if parsed_human_input == chat.CONTINUE:
            continue

        # If we got this far, it's a string that we are going to pass to the LLM

        # --------------- Process the input and stream it to the human --------------- #
        if parsed_human_input != human_input:
            # If the user edited the input, then we want to print it out so they
            # have a record of what they asked for on their terminal
            console.print(parsed_human_input)

        try:
            with Live(OurMarkdown(""), auto_refresh=True) as live:
                callback = RichLiveCallbackHandler(live, console.bot_style)
                llm.callbacks = [callback]  # a fresh callback handler for each question

                # Recalculate the response token size in case the files changed
                llm.max_tokens = calc_response_token_size(files)

                chain.run({"task": parsed_human_input, "context": context, "languages": languages})

        except KeyboardInterrupt:
            console.print("\n\nOk, I'll stop talking. Hit Ctrl-C again to quit.", style=console.bot_style)
            continue

        if request:
            # If we were given a request, then we only want to run once
            break


@click.command
@click.option("-l", "--learned-repos", multiple=True, help="The name of the repo to use for learned information")
def sidekick_agent(learned_repos):
    """
    EXPERIMENTAL: Coding help from your AI sidekick, made agentic with tools\n
    """
    console = get_console()
    if not Coder.is_inside_git_repo():
        console.print("🛑 This command must be run from within a git repository.", style=console.error_style)
        sys.exit(1)

    console.print("This is an experimental feature.", style=console.warning_style)

    agent = SidekickAgent.get_agent_executor(learned_repos)
    history_file = Path.home() / ".aicodebot_request_history"

    console.print("Enter a request for your AICodeBot sidekick", style=console.bot_style)

    edited_input = None
    while True:  # continuous loop for multiple questions
        human_input = input_prompt("🤖 ➤ ", history=FileHistory(history_file))
        human_input = human_input.strip()

        if not human_input:
            # Must have been spaces or blank line
            continue

        elif human_input.lower()[-2:] == r"\e":
            # If the text ends wit then we want to edit it
            human_input = edited_input = click.edit(human_input[:-2])

        if edited_input:
            # If the user edited the input, then we want to print it out so they
            # have a record of what they asked for on their terminal
            console.print(f"Request:\n{edited_input}")

        response = agent.run(human_input)
        # Remove everything after Action: (if it exists)
        response = response.split("Action:")[0]
        console.print(OurMarkdown(response))
