from aicodebot import version as aicodebot_version
from aicodebot.coder import DEFAULT_MAX_TOKENS, Coder
from aicodebot.commands import alignment, commit, configure, debug, learn, sidekick, sidekick_agent
from aicodebot.config import read_config
from aicodebot.helpers import logger
from aicodebot.output import OurMarkdown as Markdown, RichLiveCallbackHandler, get_console
from aicodebot.prompts import get_prompt
from langchain.chains import LLMChain
from rich.live import Live
import click, json, langchain, os, sys

# -------------------------- Top level command group ------------------------- #

console = get_console()


@click.group()
@click.version_option(aicodebot_version, "--version", "-V")
@click.help_option("--help", "-h")
@click.option("-d", "--debug-output", is_flag=True, help="Enable debug output")
@click.pass_context
def cli(ctx, debug_output):
    ctx.ensure_object(dict)
    ctx.obj["config"] = existing_config = read_config()
    if not existing_config:
        if ctx.invoked_subcommand != "configure":
            console.print("Welcome to AICodeBot 🤖. Let's set up your config file.\n", style=console.bot_style)
            configure.callback(openai_api_key=os.getenv("OPENAI_API_KEY"), verbose=0)
            sys.exit(0)
    else:
        os.environ["OPENAI_API_KEY"] = existing_config["openai_api_key"]

    # Turn on langchain debug output if requested
    langchain.debug = debug_output


# -------------------------- Subcommands ------------------------- #

cli.add_command(alignment)
cli.add_command(configure)
cli.add_command(commit)
cli.add_command(debug)
cli.add_command(sidekick)
if os.getenv("AICODEBOT_ENABLE_EXPERIMENTAL_FEATURES"):
    cli.add_command(learn)
    cli.add_command(sidekick_agent)


@cli.command
@click.option("-c", "--commit", help="The commit hash to review (otherwise look at [un]staged changes).")
@click.option("-v", "--verbose", count=True)
@click.option("--output-format", default="text", type=click.Choice(["text", "json"], case_sensitive=False))
@click.option("-t", "--response-token-size", type=int, default=DEFAULT_MAX_TOKENS * 2)
@click.argument("files", nargs=-1)
def review(commit, verbose, output_format, response_token_size, files):
    """Do a code review, with [un]staged changes, or a specified commit."""
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

    # Check the size of the diff context and adjust accordingly
    request_token_size = Coder.get_token_length(diff_context) + Coder.get_token_length(prompt.template)
    model_name = Coder.get_llm_model_name(request_token_size + response_token_size)
    if model_name is None:
        raise click.ClickException(f"The diff is too large to review ({request_token_size} tokens). 😢")

    llm = Coder.get_llm(model_name, verbose, response_token_size, streaming=True)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)

    if output_format == "json":
        with console.status("Examining the diff and generating the review", spinner=console.DEFAULT_SPINNER):
            response = chain.run({"diff_context": diff_context, "languages": languages})

        parsed_response = prompt.output_parser.parse(response)
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
        console.print(
            "Examining the diff and generating the review for the following files:\n\t" + "\n\t".join(files)
        )
        with Live(Markdown(""), auto_refresh=True) as live:
            llm.streaming = True
            llm.callbacks = [RichLiveCallbackHandler(live, console.bot_style)]

            chain.run({"diff_context": diff_context, "languages": languages})


if __name__ == "__main__":  # pragma: no cover
    cli()
