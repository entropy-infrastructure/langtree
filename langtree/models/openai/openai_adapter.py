from langtree.core import Operator
from langtree.core.utils import get_embedding_content
import openai

def get_chat_content(output):
    return output["choices"][0]["message"]

class OpenAIChatCompletion(Operator):

    def __init__(self, call=None, parse=None, **kwargs):
        super().__init__(
            call=openai.ChatCompletion.create if call is None else call,
            parse=get_chat_content if parse is None else parse
        )
        self.freeze_call(**kwargs)


class OpenAICompletion(Operator):

    def __init__(self, call=None, parse=None, **kwargs):
        super().__init__(
            call=openai.Completion.create if call is None else call,
            parse=None
        )
        self.freeze_call(**kwargs)

def make_open_ai_embedding_call(func):
    def embfn(docs, model=None):
        return [func(input=d, model=model)["data"][0]["embedding"] for d in docs]

    return embfn

class OpenAIEmbedding(Operator):

    def __init__(self, call=None, **kwargs):
        super().__init__(
            call=make_open_ai_embedding_call(openai.Embedding.create) if call is None else call,
            parse=get_embedding_content
        )
        self.freeze_call(**kwargs)
