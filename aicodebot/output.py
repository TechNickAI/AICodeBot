from aicodebot.helpers import logger
from langchain.callbacks.base import BaseCallbackHandler
from rich.markdown import CodeBlock, Markdown
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
