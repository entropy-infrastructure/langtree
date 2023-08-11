
import backoff


def default_call(*args, **kwargs):
    """Default call function that returns the provided keyword arguments.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        dict: The provided keyword arguments.
    """
    return kwargs


def default_parse(output):
    """Default parse function that returns the provided output without modifications.

    Args:
        output: The output to parse.

    Returns:
        The unmodified output.
    """
    return output


def freeze(function, **top_kwargs):
    """Return a function with specific arguments frozen.

    Args:
        function (callable): The function to freeze arguments for.
        **top_kwargs: Keyword arguments to freeze.

    Returns:
        callable: The function with specific arguments frozen.
    """
    def frozen(*args, **kwargs):
        return function(*args, **{**top_kwargs, **kwargs})
    return frozen


class Operator(object):
    """A class to represent and process custom call and parse operations."""

    def __init__(self, call=default_call, parse=default_parse):
        """Initialize the Operator with custom call and parse functions.

        Args:
            call (callable, optional): The custom call function. Defaults to default_call.
            parse (callable, optional): The custom parse function. Defaults to default_parse.
        """
        self.call = call
        self.parse = parse

    def __call__(self, *args, **kwargs):
        """Call the Operator's call function and parse its result.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The parsed result of the call function.
        """
        res = self.call(*args, **kwargs)
        if self.parse is not None:
            res = self.parse(res)
        return res

    def freeze_call(self, **kwargs):
        """Freeze specific arguments for the Operator's call function.

        Args:
            **kwargs: Keyword arguments to freeze.
        """
        self.call = freeze(self.call, **kwargs)

    def freeze_parse(self, **kwargs):
        """Freeze specific arguments for the Operator's parse function.

        Args:
            **kwargs: Keyword arguments to freeze.
        """
        self.parse = freeze(self.parse, **kwargs)
