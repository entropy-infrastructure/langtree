from langtree.models.openai import OpenAIChatCompletion
from langtree.core import Buffer, Prompt, Operator
from langtree.utils.data import Data
from langtree.operators import Parallel, Sequential, chainable
from langtree.replay_engine import ChainRecorder


@chainable
def callit(history, operator=None):
    res = operator(messages=history.memory)
    return res, history


@chainable
def storeresult(res, history, message=None):
    history.append(message(content=res.content))
    return history

def pick_one(histories):
    return histories[-1]

def openai_chat_completion_parallel_example():
    model = "gpt-3.5-turbo"
    c = ChainRecorder("test")

    history = Buffer(3)
    chatgpt = OpenAIChatCompletion(model=model)
    chatgpt4 = OpenAIChatCompletion(model="gpt-4")

    system_prompt = Prompt("You are a helpful assistant")
    user_prompt = Prompt("{{banana}}.{{dev}} is cool")
    user_prompt2 = Prompt("{{banana2}}.{{dev2}} is cool")
    p3 = user_prompt2 + user_prompt

    sys_content = system_prompt()
    user_content = p3(banana="openai", dev="com", banana2="founders", dev2="inc")
    sys_message = Data({"role": "system", "content": None})
    user_message = Data(role="user", content=None)

    s = sys_message(content=sys_content)
    u = user_message(content=user_content)

    history += s
    history += u

    """
    This is a sequential example. First we create a list of functions that are our sequential chain
    Then we add GPT4 as an extension to the sequence.
    
    These two do the same thing.
    """
    chat = Sequential([callit(operator=chatgpt), storeresult(message=user_message)] * 3)
    chat += Operator(call=callit(operator=chatgpt4))

    chat = Sequential([callit(operator=chatgpt), storeresult(message=user_message)] * 3)
    chat.add(Operator(call=callit(operator=chatgpt4)))

    """
       This is a parallel example. First we create a list of functions that are our parallel chain
       Then we add GPT4 as an extension to the sequence.

       These two also do the same thing as each other.
       """

    chat = Parallel([callit(operator=chatgpt)] * 3)
    chat += Operator(call=callit(operator=chatgpt4))

    chat = Parallel([callit(operator=chatgpt)] * 3)
    chat.add(Operator(call=callit(operator=chatgpt4)))

    """
        This is a combined example. First we create two lists of functions that are our sequential chains
        Then we add them in parallel. Then we add another gpt4 example in parallel
        
        THEN we pick the result we want from the 3 chains
   """

    chat = Sequential([callit(operator=chatgpt), storeresult(message=user_message)] * 3)
    chat2 = Sequential([callit(operator=chatgpt4), storeresult(message=user_message)] * 3)

    chat3 = Sequential([])
    chat3 += Operator(call=callit(operator=chatgpt4))

    chat4 = Parallel([chat, chat2])

    chat4 += chat3
    res = chat4(history)

    chat5 = Sequential([pick_one])
    res = chat5(res)

    print(res)

if __name__ == "__main__":
    openai_chat_completion_parallel_example()