from abc import ABC, abstractmethod
import datetime


class StorageStrategySelector(ABC):
    """
    Selects and creates an instance of the appropriate StorageStrategy subclass based on the given booleans.
    """

    def __init__(self, *args, multirun=False, incremental=False, **kwargs):
        self.multirun = multirun
        self.incremental = incremental
        self.strategy_mapping = self.get_strategies()

        try:
            strategy_class = self.strategy_mapping[(self.multirun, self.incremental)]
        except KeyError:
            raise ValueError(f"No Storage strategy implemented for multirun={self.multirun}, incremental={self.incremental}")

        self.strategy = strategy_class(*args, **kwargs)

    @abstractmethod
    def get_strategies(self):
        pass

    def preprocess(self, chain):
        return self.strategy.preprocess(chain)

    def read(self, chain_name=None):
        return self.strategy.read(chain_name=chain_name)

    def write(self, chain):
        return self.strategy.write(chain)

    def generate_run_id(self, *args, **kwargs):
        return self.strategy.generate_run_id(*args, **kwargs)


class StorageStrategy(ABC):
    """
    Abstract base class for all Storage strategies.
    """

    @abstractmethod
    def preprocess(self, chain):
        """
        Prepares the state of the chain for writing.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def read(self, chain_name):
        """
        Reads the state of the chain with the given name.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def write(self, chain):
        """
        Writes the state of the chain.
        Must be implemented by subclasses.
        """
        pass

    def generate_run_id(self, *args, **kwargs):
        """
        Generates a new run_id.
        Can be overridden by subclasses.
        """
        # By default, generate a run_id based on the current time
        return datetime.datetime.now().isoformat()

