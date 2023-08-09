from langtree.models.openai import OpenAIChatCompletion
from langtree.core import Buffer, Prompt
from langtree.utils.data import Data

def openai_chat_completion_example():
    model = "gpt-3.5-turbo"

    history = Buffer(3)
    chat = OpenAIChatCompletion(model=model)

    system_prompt = Prompt("You are a helpful assistant")
    user_prompt = Prompt("{{banana}}.{{dev}} is cool")

    sys_content = system_prompt()
    user_content = user_prompt(banana="openai", dev="com")
    sys_message = Data({"role": "system", "content": None})
    user_message = Data(role="user", content=None)

    s = sys_message(content=sys_content)
    u = user_message(content=user_content)

    history += s
    history += u


    for i in range(3):
        response = chat(messages=history.memory)
        history += user_message(content=response.content)
        print(response)

if __name__ == "__main__":
    openai_chat_completion_example()