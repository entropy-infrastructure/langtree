from langtree.models.openai import OpenAICompletion
from langtree.core import Prompt


def openai_completion_example():
    model = "text-davinci-003"

    chat = OpenAICompletion(model=model)

    user_prompt = Prompt("{{banana}}.{{dev}} is cool what do you think?")

    response = chat(prompt=user_prompt(banana="openai", dev="com"), max_tokens=200)

    print(response)

if __name__ == "__main__":
    openai_completion_example()
