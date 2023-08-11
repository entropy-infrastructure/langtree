
class Buffer:
    """A class to represent a buffer with a fixed length.

    This buffer allows appending and extending its content while ensuring 
    it never exceeds its defined length. If the buffer's content exceeds 
    its length, items are removed from the beginning.
    """

    def __init__(self, length):
        """Initialize the Buffer with a defined length.

        Args:
            length (int): The maximum length of the buffer.
        """
        self._len = length
        self._memory = []

    def append(self, item):
        """Append an item to the buffer and ensure the buffer does not exceed its length.

        Args:
            item: The item to append.
        """
        self._memory.append(item)
        self._shrink()

    def extend(self, item_list):
        """Extend the buffer with a list of items and ensure the buffer does not exceed its length.

        Args:
            item_list (list): The list of items to extend the buffer with.
        """
        self._memory.extend(item_list)
        self._shrink()

    def _shrink(self):
        """Private method to shrink the buffer to its defined length by removing items from the beginning."""
        while self._len < len(self._memory):
            self._memory.pop(0)

    def __add__(self, item):
        """Handle addition operations with the buffer. Allows for adding a single item or a list of items.

        Args:
            item: An item or a list of items to add.

        Returns:
            Buffer: The updated buffer.
        """
        if type(item) == list:
            self.extend(item)
        else:
            self.append(item)

    def __iadd__(self, item):
        """Handle in-place addition operations with the buffer. Allows for adding a single item or a list of items.

        Args:
            item: An item or a list of items to add.

        Returns:
            Buffer: The updated buffer.
        """
        if type(item) == list:
            self.extend(item)
        else:
            self.append(item)
        return self

    def __repr__(self):
        """Return a representation of the buffer's memory."""
        return self._memory.__repr__()

    @property
    def memory(self):
        """Provide access to the buffer's memory.

        Returns:
            list: The buffer's memory content.
        """
        return self._memory
