from langchain.callbacks.base import BaseCallbackHandler
from rich.markdown import Markdown


class RichLiveCallbackHandler(BaseCallbackHandler):
    def __init__(self, live, style):
        self.buffer = []
        self.live = live
        self.style = style

    def on_llm_new_token(self, token, **kwargs):
        self.buffer.append(token)
        self.live.update(Markdown("".join(self.buffer), style=self.style))
