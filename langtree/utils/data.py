class Data(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._allowed_keys = set(self.keys())

    def __call__(self, **kwargs):
        # Check if any of the keys in kwargs are not in the allowed keys
        if not set(kwargs.keys()).issubset(self._allowed_keys):
            raise KeyError("Attempting to update with a key that wasn't provided upon instantiation.")
        self.update(kwargs)
        return self.copy()
