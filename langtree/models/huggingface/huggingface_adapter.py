from easyllm.clients import huggingface
from tinychain.core import Adapter
from tinychain.core.utils import get_chat_content


class HuggingfaceChatCompletion(Adapter):

    def __init__(self, call=None, parse=None, **kwargs):
        super().__init__(
            call=huggingface.ChatCompletion.create if call is None else call,
            parse=get_chat_content if parse is None else parse
        )
        self.freeze_call(**kwargs)


class HuggingfaceCompletion(Adapter):

    def __init__(self, call=None, parse=None, **kwargs):
        super().__init__(
            call=huggingface.Completion.create if call is None else call,
            parse=get_chat_content if parse is None else parse
        )
        self.freeze_call(**kwargs)


class HuggingfaceEmbedding(Adapter):

    def __init__(self, call=None, **kwargs):
        super().__init__(
            call=huggingface.Embedding.create if call is None else call
        )
        self.freeze_call(**kwargs)
