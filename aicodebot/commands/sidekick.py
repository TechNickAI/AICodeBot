from aicodebot import AICODEBOT
from aicodebot.coder import Coder
from aicodebot.config import Session
from aicodebot.helpers import logger
from aicodebot.input import Chat, generate_prompt_session
from aicodebot.lm import DEFAULT_CONTEXT_TOKENS, LanguageModelManager
from aicodebot.output import OurMarkdown, RichLiveCallbackHandler, get_console
from aicodebot.prompts import generate_files_context, get_prompt
from rich.live import Live
from rich.panel import Panel
import click, sys


@click.command()
@click.option("-a", "--apply", is_flag=True, help="Automatically apply changes")
@click.option("-r", "--request", help="What to ask your sidekick to do")
@click.option("-n", "--no-files", is_flag=True, help="Don't automatically load any files for context")
@click.option("-m", "--max-file-tokens", type=int, default=10_000, help="Don't load files larger than this")
@click.argument("files", nargs=-1, type=click.Path(exists=True, readable=True))
def sidekick(apply, request, no_files, max_file_tokens, files):  # noqa: PLR0915
    """
    Coding help from your AI sidekick coding assistant
    FILES: List of files to be used as context for the session
    """
    console = get_console()
    if not Coder.is_inside_git_repo():
        console.print("🛑 This command must be run from within a git repository.", style=console.error_style)
        sys.exit(1)

    console.print(
        Panel(OurMarkdown("This is an *experimental* feature. We love bug reports 😉", style=console.warning_style))
    )

    # ----------------- Determine which files to use for context ----------------- #

    if files:  # User supplied list of files
        context = generate_files_context(files)
    elif not no_files:
        # Determine which files to use for context automagically, with git
        session_data = Session.read()
        if session_data.get("files"):
            console.print("Using files from the last session for context.", style="dim")
            files = session_data["files"]
        else:
            console.print("Using recent git commits and current changes for context.", style="dim")
            files = Coder.auto_file_context(DEFAULT_CONTEXT_TOKENS, max_file_tokens)

        context = generate_files_context(files)
    else:
        context = generate_files_context([])

    # Convert it from a list or a tuple to a set to remove duplicates
    files = set(files)

    # ---------------------- Set up the chat loop and prompt --------------------- #
    chat = Chat(console, files)
    chat.show_file_context()
    languages = ",".join(Coder.identify_languages(files))

    console.print(
        f"Enter a request for your {AICODEBOT} sidekick. Type /help to see available commands.\n",
        style=console.bot_style,
    )
    our_input_session = generate_prompt_session()

    lmm = LanguageModelManager()
    prompt = get_prompt("sidekick")

    while True:  # continuous loop for multiple questions
        if request:
            human_input = request
        else:
            human_input = our_input_session.prompt()

        parsed_human_input = chat.parse_human_input(human_input)
        if parsed_human_input == chat.BREAK:
            break

        # Update the context for the new list of files
        context = generate_files_context(chat.file_context)
        languages = ",".join(Coder.identify_languages(chat.file_context))
        our_input_session.completer.file_context = chat.file_context

        # Save the files for the next session
        session_data = Session.read()
        session_data["files"] = list(chat.file_context)
        Session.write(session_data)

        if parsed_human_input == chat.CONTINUE:
            continue

        # If we got this far, it's a string that we are going to pass to the LM

        # --------------- Process the input and stream it to the human --------------- #
        if parsed_human_input != human_input:
            # If the user edited the input, then we want to print it out so they
            # have a record of what they asked for on their terminal
            console.print(parsed_human_input)
        try:
            with Live(OurMarkdown(f"Sending task to {lmm.model_name} via {lmm.provider}"), auto_refresh=False) as live:
                llm = lmm.model_factory(
                    streaming=True,
                    callbacks=[RichLiveCallbackHandler(live, console.bot_style)],
                )
                chain = prompt | llm

                chat.raw_response = chain.invoke(
                    {"task": parsed_human_input, "context": context, "languages": languages}
                )

                # One last "live" update with the full response
                markdown = OurMarkdown(str(chat.raw_response))
                live.update(markdown)

                # ------------------------- Post process the markdown ------------------------ #

                code_blocks = markdown.pull_code_blocks()
                if code_blocks:
                    logger.debug(f"Found code blocks: {code_blocks}")
                    code_block_message = f"{len(code_blocks)} code block(s) found, **/copy** to copy to your clipboard."
                    console.print(Panel(OurMarkdown(code_block_message)))
                    chat.code_blocks = markdown.pull_code_blocks()

                chat.diff_blocks = markdown.pull_diff_blocks()
                if chat.diff_blocks:
                    if apply:
                        chat.apply()
                    else:
                        patch_message = f"{len(chat.diff_blocks)} patches found, **/apply** to apply them."
                        console.print(Panel(OurMarkdown(patch_message)))

        except KeyboardInterrupt:
            console.print("\n\nOk, I'll stop talking. Hit Ctrl-C again to quit.", style=console.bot_style)
            continue

        if request:
            # If we were given a request, then we only want to run once
            break
