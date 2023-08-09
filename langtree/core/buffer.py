class Buffer:

    def __init__(self, length):
        self._len = length
        self._memory = []

    def append(self, item):
        self._memory.append(item)
        self._shrink()

    def extend(self, item_list):
        self._memory.extend(item_list)
        self._shrink()

    def _shrink(self):
        while self._len < len(self._memory):
            self._memory.pop(0)

    def __add__(self, item):
        if type(item) == list:
            self.extend(item)
        else:
            self.append(item)

    def __iadd__(self, item):
        if type(item) == list:
            self.extend(item)
        else:
            self.append(item)

        return self

    def __repr__(self):
        return self._memory.__repr__()

    @property
    def memory(self):
        return self._memory
