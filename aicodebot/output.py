from aicodebot.helpers import logger
from functools import cache
from langchain.callbacks.base import BaseCallbackHandler
from rich.console import Console
from rich.markdown import CodeBlock, Markdown
from rich.style import Style
from rich.syntax import Syntax


class RichLiveCallbackHandler(BaseCallbackHandler):
    def __init__(self, live, style):
        self.buffer = []
        self.live = live
        self.style = style

    def on_llm_start(self, *args, **kwargs):
        self.live.update(Markdown("**Thinking...**"))

    def on_llm_new_token(self, token, **kwargs):
        self.buffer.append(token)
        self.live.update(OurMarkdown("".join(self.buffer), style=self.style), refresh=True)

    def on_llm_end(self, *args, **kwargs):
        self.buffer = []
        self.live.stop()

    def on_llm_error(self, error, **kwargs):
        """Run when LLM errors."""
        logger.exception(error)
        self.buffer = []
        self.live.stop()


class OurCodeBlock(CodeBlock):
    # The default Code block puts a leading space in front of the code, which is annoying for copying/pasting code

    def __rich_console__(self, console, options):
        code = str(self.text)
        # set dedent=True to remove leading spaces and turn off padding
        syntax = Syntax(code, self.lexer_name, theme=self.theme, word_wrap=True, padding=0)
        yield syntax


class OurMarkdown(Markdown):
    elements = {**Markdown.elements, "fence": OurCodeBlock, "code_block": OurCodeBlock}


@cache
def get_console():
    """Get a console object, with cache so that we reuse the same console object."""
    console = Console()
    console.DEFAULT_SPINNER = "point"
    console.bot_style = Style(color="#30D5C8")
    console.error_style = Style(color="#FF0000")
    console.warning_style = Style(color="#FFA500")
    return console
