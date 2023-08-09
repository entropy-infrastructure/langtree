import re


def render_prompt(template, **kwargs):
    if template is None:
        return

    for key, value in kwargs.items():
        template = re.sub(r"\{\{" + re.escape(key) + r"\}\}", value, template)
    return template


class Prompt:

    def __init__(self, template):
        self.template = template

    def __call__(self, **kwargs):
        return render_prompt(self.template, **kwargs)

    def __add__(self, other):
        # If the other object is a Prompt, concatenate templates
        if isinstance(other, Prompt):
            return Prompt(self.template + other.template)

        # If the other object is a str (or can be represented as one), concatenate
        elif isinstance(other, str):
            return Prompt(self.template + other)

        # If the other object is not a string or Prompt, raise a TypeError
        else:
            raise TypeError(f"Cannot concatenate 'Prompt' with '{type(other).__name__}'")
