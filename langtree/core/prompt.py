
import re

def render_prompt(template, **kwargs):
    """Render a template string by substituting placeholders with provided keyword arguments.

    Args:
        template (str): The template string containing placeholders.
        **kwargs: Keyword arguments representing placeholder-value pairs.

    Returns:
        str: The rendered string after substitutions.
    """
    if template is None:
        return

    for key, value in kwargs.items():
        template = re.sub(r"\{\{" + re.escape(key) + r"\}\}", value, template)
    return template


class Prompt:
    """A class to represent and process prompt templates."""

    def __init__(self, template):
        """Initialize the Prompt object with a template string.

        Args:
            template (str): The template string for the prompt.
        """
        self.template = template

    def __call__(self, **kwargs):
        """Render the prompt using the provided keyword arguments.

        Args:
            **kwargs: Keyword arguments for rendering the prompt.

        Returns:
            str: The rendered prompt.
        """
        return render_prompt(self.template, **kwargs)

    def __add__(self, other):
        """Handle concatenation of two Prompt objects or a Prompt object with a string.

        Args:
            other (Prompt, str): Another Prompt object or a string to concatenate with.

        Returns:
            Prompt: A new Prompt object with concatenated templates.

        Raises:
            TypeError: If the other object is neither a Prompt nor a string.
        """
        # If the other object is a Prompt, concatenate templates
        if isinstance(other, Prompt):
            return Prompt(self.template + other.template)

        # If the other object is a str (or can be represented as one), concatenate
        elif isinstance(other, str):
            return Prompt(self.template + other)

        # If the other object is not a string or Prompt, raise a TypeError
        else:
            raise TypeError(f"Cannot concatenate 'Prompt' with '{type(other).__name__}'")
