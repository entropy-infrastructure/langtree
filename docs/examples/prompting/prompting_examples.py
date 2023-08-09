from langtree.core import Prompt
from langtree.prompting import UserMessage, SystemMessage


"""
Here we are defining two prompts. These aren't assigned to roles at first.

To assign these to message roles, we can use the message types as showm below.
"""


def Basics():
    system_prompt = Prompt("You are a helpful assistant")
    user_prompt = Prompt("{{banana}}.{{dev}} is cool")

    #Render the prompt
    sys_content = system_prompt()
    sys_msg = SystemMessage(content=sys_content)

    #Render the prompt with the variables
    usr_content = user_prompt(banana="open", dev="ai")
    usr_msg = UserMessage(content=usr_content)

    print(sys_msg)
    print(usr_msg)


"""
Now that we know how prompting works, we can do arithmetic on prompts!

This is great for few shot prompting since you can iteratively add and configure your prompts.

WARNING: THERE CAN ONLY BE ONE OF EACH PROMPT KEYWORD, make sure you name your prompt vars accordingly.
"""
def Basics_part_2():
    system_prompt = Prompt("You are a helpful assistant")
    user_prompt = Prompt("{{banana}}.{{dev}} is cool")
    prompt = user_prompt + system_prompt

    #Render the prompt with the variables
    content = prompt(banana="open", dev="ai")
    msg = UserMessage(content=content)

    print(msg)

"""
We are currently working on adding function calling and function message support
"""