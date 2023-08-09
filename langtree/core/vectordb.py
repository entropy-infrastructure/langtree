from abc import ABC, abstractmethod
from typing import Any, List


class VectorDatabase(ABC):
    @abstractmethod
    def insert(self, vector: List[float], metadata: Any, **kwargs) -> None:
        """
        Inserts a vector into the database, with optional metadata and additional parameters.
        """
        pass

    @abstractmethod
    def query(self, vector: List[float], top_k: int, **kwargs) -> List[Any]:
        """
        Queries the database for the 'top_k' closest vectors to the provided vector.
        Returns a list of matched vectors' metadata. Accepts additional parameters.
        """
        pass

    def __getattr__(self, name):
        """
        Override Python's default behavior when an attribute isn't found.
        We can use this to 'forward' method calls to the underlying database object.
        """
        def method(*args, **kwargs):
            if hasattr(self.db, name):
                func = getattr(self.db, name)
                if callable(func):
                    return func(*args, **kwargs)
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

        return method
