import threading
from functools import wraps


class ChainRecorder:
    # Class-level variables
    context_chains = threading.local()
    context_chains.active_contexts = []
    context_chains.contexts = {}
    registered_functions = {}

    def __init__(self, name=None, persistence_strategy=None):
        self.name = name
        self.records = []
        self.records_history = []
        self.checkpoints = []
        self.persistence_strategy = persistence_strategy
        self._stack = []
        if name:
            ChainRecorder.context_chains.contexts[name] = self
        if not ChainRecorder.context_chains.contexts:
            ChainRecorder.context_chains.contexts['default'] = self

    def bind(self, name):
        func = ChainRecorder.registered_functions.get(name)
        if func is None:
            raise ValueError(f"No function registered under the name {name}")

        @wraps(func)
        def wrapper(*args, **kwargs):
            record = {
                'function': name,
                'input': {'args': args, 'kwargs': kwargs},
                'output': None,
                'children': [],
                'errors': []
            }

            if self._stack:
                self._stack[-1]['children'].append(record)
            else:
                self.records.append(record)

            self._stack.append(record)
            try:
                output = func(*args, **kwargs)
            except Exception as e:
                record['errors'].append(str(e))
                raise
            else:
                record['output'] = output
            finally:
                self._stack.pop()

            return output

        return wrapper

    @classmethod
    def record(cls, *context_names):
        def decorator(func):
            func_name = func.__name__
            cls.registered_functions[func_name] = func

            @wraps(func)
            def wrapper(*args, **kwargs):
                active_contexts = cls.context_chains.active_contexts
                named_contexts = [cls.context_chains.contexts.get(context_name) for context_name in context_names if
                                  context_name in cls.context_chains.contexts]

                all_contexts = active_contexts.copy()
                if len(named_contexts) > 0:
                    all_contexts.extend(named_contexts)

                output = None
                for context in set(all_contexts):
                    output = context.bind(func_name)(*args, **kwargs)
                return output

            return wrapper

        return decorator

    def checkpoint(self):
        """
        Create a checkpoint of the current state of the records.
        Also persist the checkpoint if a persistence object is provided.
        """
        self.checkpoints.append(len(self.records) - 1)
        if self.persistence_strategy:
            self.persistence_strategy.write(self)

    def restore(self, index):
        """
        Restore the state of all records to the specified checkpoint index.
        """
        if index >= len(self.checkpoints):
            raise IndexError(f"No checkpoint with index {index}")
        # Roll back to the checkpoint by removing all subsequent records
        self.records = self.records[:self.checkpoints[index] + 1]

    def __enter__(self):
        ChainRecorder.context_chains.active_contexts.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ChainRecorder.context_chains.active_contexts.remove(self)
        # Persist the records when the chain is no longer in use
        if self.persistence_strategy:
            self.persistence_strategy.write(self)

    def persist(self):
        if self.persistence_strategy:
            self.persistence_strategy.write(self)

    @classmethod
    def from_persisted(cls, chain_name, persistence_strategy):
        # Use the strategy to read the persisted chain
        persisted_data = persistence_strategy.read(chain_name)
        if persisted_data is not None:
            # Use the persisted data to create a new ChainRecorder instance
            chain = cls(name=chain_name, persistence_strategy=persistence_strategy)
            chain.records = persisted_data
            return chain
        else:
            return None

    @classmethod
    def get_history(cls, context_name=None):
        if context_name is None:
            return cls.context_chains.contexts['default'].records_history
        return cls.context_chains.contexts.get(context_name, []).records_history

    @classmethod
    def get_records(cls, context_name=None):
        if context_name is None:
            return cls.context_chains.contexts['default'].records
        return cls.context_chains.contexts.get(context_name, []).records

    @classmethod
    def remove_context(cls, context_name):
        if context_name in cls.context_chains.contexts:
            del cls.context_chains.contexts[context_name]

    @classmethod
    def restore_last(cls, context_name=None):
        if context_name is None:
            context = cls.context_chains.contexts['default']
        else:
            context = cls.context_chains.contexts.get(context_name)
        if context:
            context.restore(len(context.checkpoints) - 1)

    @classmethod
    def search_history(cls, function_name, context_name=None):
        if context_name is None:
            context = cls.context_chains.contexts['default']
        else:
            context = cls.context_chains.contexts.get(context_name)
        if context:
            return [record for record in context.records_history if record['function'] == function_name]
        else:
            return []

    @classmethod
    def last_executed(cls, context_name=None):
        if context_name is None:
            context = cls.context_chains.contexts['default']
        else:
            context = cls.context_chains.contexts.get(context_name)
        if context and context.records:
            return context.records[-1]
        else:
            return None

    @classmethod
    def total_executed(cls, context_name=None):
        if context_name is None:
            context = cls.context_chains.contexts['default']
        else:
            context = cls.context_chains.contexts.get(context_name)
        return len(context.records) if context else 0

    @classmethod
    def clear_records(cls, context_name=None):
        if context_name is None:
            context = cls.context_chains.contexts['default']
        else:
            context = cls.context_chains.contexts.get(context_name)
        if context:
            context.records = []

    def search(self, function_name):
        return [record for record in self.records_history if record['function'] == function_name]

    def last(self):
        return self.records[-1] if self.records else None

    def total(self):
        return len(self.records)

    def clear(self):
        self.records = []
