from aicodebot import version as aicodebot_version
from aicodebot.helpers import exec_and_get_output
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import load_prompt
from pathlib import Path
from rich.console import Console
from rich.style import Style
import click, datetime, openai, os, random, subprocess, sys, tempfile, webbrowser

# Create a Console object
console = Console()
bot_style = Style(color="#30D5C8")
DEFAULT_MAX_TOKENS = 1024


def setup_environment():
    # Load environment variables from the config file
    config_file = Path(Path.home() / ".aicodebot")
    load_dotenv(config_file)

    if os.getenv("OPENAI_API_KEY"):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        return True

    openai_api_key_url = "https://platform.openai.com/account/api-keys"

    console.print(
        "[bold red]The OPENAI_API_KEY environment variable is not set.[/bold red]\n"
        f"Let's fix that for you by creating a config file at {config_file}"
    )

    if click.confirm("Do you want me to open the OpenAI API keys page for you in a browser?"):
        webbrowser.open(openai_api_key_url)

    if click.confirm(f"Do you want me to create the {config_file} file for you?"):
        api_key = click.prompt("Please enter your OpenAI API key")

        # Copy .env.template to .env and insert the API key
        template_file = Path(__file__).parent / ".aicodebot.template"
        with Path.open(template_file, "r") as template, Path.open(config_file, "w") as env:
            for line in template:
                if line.startswith("OPENAI_API_KEY="):
                    env.write(f"OPENAI_API_KEY={api_key}\n")
                else:
                    env.write(line)

        console.print(f"[bold green]Created {config_file} with your OpenAI API key. You're all set![/bold green]")
        sys.exit(0)

    raise click.ClickException("Please set an API key in the OPENAI_API_KEY environment variable or in a .env file.")


@click.group()
@click.version_option(aicodebot_version, "--version", "-V")
@click.help_option("--help", "-h")
def cli():
    pass


@cli.command()
@click.option("-v", "--verbose", count=True)
def alignment(verbose):
    """Get a message about Heart-Centered AI Alignment ❤ + 🤖."""
    setup_environment()

    # Load the prompt
    prompt = load_prompt(Path(__file__).parent / "prompts" / "alignment.yaml")

    # Set up the language model
    llm = OpenAI(temperature=1, max_tokens=DEFAULT_MAX_TOKENS)

    # Set up the chain
    chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)

    name = exec_and_get_output(["git", "config", "--get", "user.name"])

    with console.status("Thinking", spinner="point"):
        response = chain.run(name)
        console.print(response, style=bot_style)


@cli.command()
@click.option("-v", "--verbose", count=True)
@click.option("-t", "--max-tokens", type=int, default=250)
@click.option("-y", "--yes", is_flag=True, default=False, help="Don't ask for confirmation before committing.")
def commit(verbose, max_tokens, yes):
    """Generate a git commit message and commit changes after you approve."""
    setup_environment()

    # Load the prompt
    prompt = load_prompt(Path(__file__).parent / "prompts" / "commit_message.yaml")

    # Set up the language model
    llm = OpenAI(temperature=0.1, max_tokens=max_tokens)

    # Set up the chain
    chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)

    # Get the changes from git
    staged_files = exec_and_get_output(["git", "diff", "--name-only", "--cached"])
    base_git_diff = ["git", "diff", "-U10"]  # Tell diff to provide 10 lines of context
    if not staged_files:
        # If no files are staged, stage all changed files
        exec_and_get_output(["git", "add", "-A"])
        # Get the diff for all changes since the last commit
        diff = exec_and_get_output(base_git_diff + ["HEAD"])
        # Get the list of files to be committed
        files = exec_and_get_output(["git", "diff", "--name-only", "--cached"])
    else:
        # If some files are staged, get the diff for those files
        diff = exec_and_get_output(base_git_diff + ["--cached"])
        # The list of files to be committed is the same as the list of staged files
        files = staged_files

    if not diff:
        console.print("No changes to commit.")
        sys.exit(0)

    console.print("The following files will be committed:\n" + files)

    with console.status("Thinking", spinner="point"):
        response = chain.run(diff)

    # Write the commit message to a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
        temp.write(str(response).strip())
        temp_file_name = temp.name

    # Open the temporary file in the user's editor
    editor = os.getenv("EDITOR", "vim")
    subprocess.call([editor, temp_file_name])  # noqa: S603

    # Ask the user if they want to commit the changes
    if yes or click.confirm("Do you want to commit the changes?"):
        # Commit the changes using the temporary file for the commit message
        exec_and_get_output(["git", "commit", "-F", temp_file_name])
        console.print(f"✅ {len(files.splitlines())} files committed.")

    # Delete the temporary file
    Path.unlink(temp_file_name)


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("command", nargs=-1)
@click.option("-v", "--verbose", count=True)
def debug(command, verbose):
    """Run a command and get debugging advice if it fails."""
    setup_environment()

    # Load the prompt
    prompt = load_prompt(Path(__file__).parent / "prompts" / "debug.yaml")

    # Set up the language model
    llm = OpenAI(temperature=0.1, max_tokens=DEFAULT_MAX_TOKENS)

    # Set up the chain
    chat_chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)
    command_str = " ".join(command)

    # Run the command and capture its output
    console.print(f"Running:\n{command_str}")
    process = subprocess.run(command_str, shell=True, capture_output=True, text=True)  # noqa: S602

    # Print the output of the command
    output = f"Standard Output:\n{process.stdout}\nStandard Error:\n{process.stderr}"
    console.print(f"Output:\n{output}")

    # Print a message about the exit status
    if process.returncode == 0:
        console.print("The command completed successfully.")
    else:
        console.print(f"The command exited with status {process.returncode}.")

    # If the command failed, send its output to ChatGPT for analysis
    if process.returncode != 0:
        error_output = process.stderr
        with console.status("Thinking", spinner="point"):
            response = chat_chain.run(error_output)
            console.print(response, style=bot_style)


@cli.command()
@click.option("-v", "--verbose", count=True)
def fun_fact(verbose):
    """Tell me something interesting about programming or AI."""
    setup_environment()

    # Load the prompt
    prompt = load_prompt(Path(__file__).parent / "prompts" / "fun_fact.yaml")

    # Set up the language model
    llm = ChatOpenAI(temperature=1, max_tokens=DEFAULT_MAX_TOKENS)

    # Set up the chain
    chat_chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)

    with console.status("Thinking", spinner="point"):
        # Select a random year so that we get a different answer each time
        year = random.randint(1942, datetime.datetime.utcnow().year)
        response = chat_chain.run(f"programming and artificial intelligence in the year {year}")
        console.print(response, style=bot_style)


@cli.command()
def version():
    """Print the version number."""
    console.print(f"AICodeBot version {aicodebot_version}")


if __name__ == "__main__":
    cli()
