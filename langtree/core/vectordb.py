
from abc import ABC, abstractmethod
from typing import Any, List

class VectorDatabase(ABC):
    @abstractmethod
    def insert(self, vector: List[float], metadata: Any, **kwargs) -> None:
        """Insert a vector into the database with optional metadata and additional parameters.

        Args:
            vector (List[float]): The vector to be inserted.
            metadata (Any): Optional metadata associated with the vector.
            **kwargs: Additional parameters for insertion.
        """
        pass

    @abstractmethod
    def query(self, vector: List[float], top_k: int, **kwargs) -> List[Any]:
        """Query the database for the 'top_k' closest vectors to the provided vector.

        Returns a list of matched vectors' metadata. Accepts additional parameters.

        Args:
            vector (List[float]): The vector used for querying.
            top_k (int): Number of closest vectors to return.
            **kwargs: Additional parameters for querying.

        Returns:
            List[Any]: List of matched vectors' metadata.
        """
        pass

    def __getattr__(self, name):
        """Override Python's default behavior when an attribute isn't found.

        This can be used to 'forward' method calls to the underlying database object.

        Args:
            name (str): The name of the attribute.

        Returns:
            callable: The method from the underlying database object.
        """
        def method(*args, **kwargs):
            if hasattr(self.db, name):
                func = getattr(self.db, name)
                if callable(func):
                    return func(*args, **kwargs)
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        return method
