from aicodebot.coder import Coder
from aicodebot.helpers import logger
from aicodebot.lm import DEFAULT_RESPONSE_TOKENS, LanguageModelManager
from aicodebot.output import OurMarkdown, RichLiveCallbackHandler, get_console
from aicodebot.prompts import get_prompt
from rich.live import Live
import click, json, sys


@click.command()
@click.option("-c", "--commit", help="The commit hash to review (otherwise look at [un]staged changes).")
@click.option("--output-format", default="text", type=click.Choice(["text", "json"], case_sensitive=False))
@click.option("-t", "--response-token-size", type=int, default=DEFAULT_RESPONSE_TOKENS * 2)
@click.argument("files", nargs=-1)
def review(commit, output_format, response_token_size, files):
    """Do a code review, with [un]staged changes, or a specified commit."""
    console = get_console()
    if not Coder.is_inside_git_repo():
        console.print("🛑 This command must be run from within a git repository.", style=console.error_style)
        sys.exit(1)

    # If files are specified, only consider those files
    # Otherwise, use git to get the list of files
    if not files:
        files = Coder.git_staged_files()
        if not files:
            files = Coder.git_unstaged_files()

    diff_context = Coder.git_diff_context(commit, files)
    if not diff_context:
        console.print("No changes detected for review. 🤷")
        return
    languages = ",".join(Coder.identify_languages(files))

    # Load the prompt
    prompt = get_prompt("review", structured_output=output_format == "json")
    logger.trace(f"Prompt: {prompt}")

    lmm = LanguageModelManager()

    if output_format == "json":
        llm = lmm.model_factory(response_token_size=response_token_size, streaming=True)
        chain = prompt | llm
        response = chain.invoke({"diff_context": diff_context, "languages": languages})

        parsed_response = prompt.output_parser.parse(response.content)
        data = {
            "review_status": parsed_response.review_status,
            "review_comments": parsed_response.review_comments,
        }
        if commit:
            data["commit"] = commit
        json_response = json.dumps(data, indent=4)
        print(json_response)  # noqa: T201

    else:
        # Stream live
        console.print("Examining the diff and generating the review for the following files:\n\t" + "\n\t".join(files))
        with Live(OurMarkdown(f"Talking to {lmm.model_name} via {lmm.provider}"), auto_refresh=True) as live:
            model = lmm.model_factory(
                response_token_size=response_token_size,
                streaming=True,
                callbacks=[RichLiveCallbackHandler(live, console.bot_style)],
            )

            chain = prompt | model

            response = chain.invoke({"diff_context": diff_context, "languages": languages})
            live.update(OurMarkdown(str(response.content)))
