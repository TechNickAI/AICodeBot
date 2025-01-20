from aicodebot.helpers import logger
from functools import cache
from langchain_core.callbacks import BaseCallbackHandler
from rich.console import Console
from rich.markdown import CodeBlock, Markdown
from rich.panel import Panel
from rich.style import Style
from rich.syntax import Syntax


class RichLiveCallbackHandler(BaseCallbackHandler):
    """Our specialized output handler that does streaming, and prints out rich.Markdown, with a few other goodies"""

    def __init__(self, live, style):
        self.buffer = []
        self.live = live
        self.style = style

    def on_llm_start(self, serialized, *args, **kwargs):
        """Initially print a message that we are sending to the LM"""
        model_name = serialized["kwargs"].get("model_name")
        if model_name:
            message = f"Sending request to *{model_name}*..."
        else:
            message = "Sending request to the language model..."
        self.live.update(Panel(OurMarkdown(message)), refresh=True)

    def on_llm_new_token(self, token, **kwargs):
        """Print out Markdown when we get a new token, using rich.live so it updates the whole terminal"""
        self.buffer.append(token)
        self.live.update(OurMarkdown("".join(self.buffer), style=self.style), refresh=True)

    def on_llm_end(self, *args, **kwargs):
        self.buffer = []
        self.live.stop()

    def on_llm_error(self, error, **kwargs):
        """Run when LM errors."""
        logger.exception(error)
        self.buffer = []
        self.live.stop()

    def on_retry(self, error, **kwargs):
        console = get_console()
        console.print(f"Error communicating with the Language Model API: {error}", style=console.error_style)


class OurCodeBlock(CodeBlock):
    """Overwrite the default CodeBlock, which puts a leading space in front of the code,
    which is annoying for copying/pasting code"""

    def __rich_console__(self, console, options):
        code = str(self.text)
        # Set the padding to 0 (default is 1)
        syntax = Syntax(code, self.lexer_name, theme=self.theme, word_wrap=True, padding=0)
        yield syntax


class OurMarkdown(Markdown):
    """Extended Markdown class that implements OurCodeBlock and adds functionality for parsing output"""

    # Extend the default elements to include OurCodeBlock for processing code blocks in markdown
    elements = {**Markdown.elements, "fence": OurCodeBlock, "code_block": OurCodeBlock}

    def pull_code_blocks(self):
        # Look at the parsed markdown for code blocks, ie:
        # ```python
        # Used for /copy in sidekick (copy to clipboard)
        out = []
        for token in self.parsed:
            if token.tag == "code" and token.info != "diff":
                out.append(token.content)
        return out

    def pull_diff_blocks(self):
        # Look at the parsed markdown for code blocks, ie:
        # ```diff
        # Used for /apply in sidekick (apply the patch with Patch.apply)
        out = []
        for token in self.parsed:
            if token.tag == "code" and token.info == "diff":
                out.append(token.content)
        return out


@cache
def get_console(*args, **kwargs):
    """Get a console object, with cache so that we reuse the same console object."""
    console = Console(*args, **kwargs)
    console.DEFAULT_SPINNER = "point"
    console.bot_style = Style(color="#30D5C8")
    console.error_style = Style(color="#FF0000")
    console.warning_style = Style(color="#FFA500")
    return console
