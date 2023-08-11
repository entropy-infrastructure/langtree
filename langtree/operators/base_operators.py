import copy

from langtree.core.operator import Operator

"""
    Before someone asks why these operators do not inherit from Operator, the answer is twofold:
        1) Explicitly different classes are nice for the conditional blocks
        2) Implementing the freezing present in Operator is not a great idea on a vector OP (way too much mental overhead for a developer, i.e. me)
"""


def chainable(func):
    """Decorator that makes a function chainable with its arguments.

    Args:
        func (callable): The function to make chainable.

    Returns:
        callable: The chainable function.
    """
    def wrapper(*args, **kws):
        op = Operator(func)
        op.freeze_call(**kws)
        return op

    return wrapper


class Parallel:
    def __init__(self, operations):

        self.operations = []
        for operation in operations:
            self.add(operation)

    def __iadd__(self, other):
        return self.add(other)

    def __add__(self, other):
        operations = self.operations

        if isinstance(other, Sequential):
            return Parallel(operations + [other])
        elif isinstance(other, Parallel):
            return Parallel(self.operations + other.operations)
        elif isinstance(other, Operator):
            return Parallel(operations + [other])
        else:
            raise ValueError(
                f"{type(other)} is not usable with type:{type(self)}. This class can only add Operators (SequentialOperator, ParallelOperator, Operator)")

    def add(self, other):
        if isinstance(other, Sequential):
            self.operations.append(other)
        elif isinstance(other, Parallel):
            self.operations.extend(other.operations)
        elif isinstance(other, Operator):
            self.operations.append(other)
        else:
            raise ValueError(
                f"{type(other)} is not usable with type:{type(self)}. This class can only add Operators (SequentialOperator, ParallelOperator, Operator)")

        return self

    def __call__(self, *args, **kwargs):

        output = []
        for operation in self.operations:
            output.append(operation(*copy.deepcopy(args), **copy.deepcopy(kwargs)))

        return output


class Sequential:
    def __init__(self, operations):

        self.operations = []
        for operation in operations:
            self.add(operation)

    def __iadd__(self, other):
        return self.add(other)

    def __add__(self, other):
        operations = self.operations

        if isinstance(other, Sequential):
            return Sequential(operations + other.operations)
        elif isinstance(other, Parallel):
            return Sequential(operations + [other])
        elif isinstance(other, Operator):
            return Sequential(operations + [other])
        else:
            raise ValueError(
                f"{type(other)} is not usable with type:{type(self)}. This class can only add Operators (SequentialOperator, ParallelOperator, Operator)")

    def __call__(self, *args, **kwargs):

        output = args
        for i, operation in enumerate(self.operations):

            if not isinstance(output, tuple):
                output = tuple([output])

            if i == 0:
                output = operation(*output, **kwargs)
            else:
                output = operation(*output)

        return output

    def add(self, other):
        if isinstance(other, Sequential):
            self.operations.extend(other.operations)
        elif isinstance(other, Parallel):
            self.operations.append(other)
        elif isinstance(other, Operator):
            self.operations.append(other)
        else:
            raise ValueError(f"{type(other)} is not usable with type:{type(self)}. This class can only add Operators (SequentialOperator, ParallelOperator, Operator)")

        return self
