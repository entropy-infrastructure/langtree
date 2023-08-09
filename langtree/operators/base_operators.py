import copy

from langtree.core.operator import Operator, freeze

"""
    Before someone asks why these operators do not inherit from Operator, the answer is twofold:
        1) Explicitly different classes are nice for the conditional blocks
        2) Implementing the freezing present in Operator is not a great idea on a vector OP (way too much mental overhead for a developer, i.e. me)
"""


def chainable(func):

    def wrapper(**kws):
        def wrapped(*args, **kwargs):
            res = func(*args, **{**kws, **kwargs})
            return res

        return wrapped

    return wrapper

class Parallel:
    def __init__(self, operations):
        self.operations = operations

    def __iadd__(self, other):
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

    def __add__(self, other):
        return self.add(other)

    def add(self, other):
        operations = self.operations

        if isinstance(other, Sequential):
            return Parallel(operations.append(other))
        elif isinstance(other, Parallel):
            return Parallel(self.operations.extend(other.operations))
        elif isinstance(other, Operator):
            return Parallel(operations.append(other))
        else:
            raise ValueError(
                f"{type(other)} is not usable with type:{type(self)}. This class can only add Operators (SequentialOperator, ParallelOperator, Operator)")

    def __call__(self, *args, **kwargs):

        output = []
        for operation in self.operations:
            output.append(operation(*copy.deepcopy(args), **copy.deepcopy(kwargs)))

        return output


class Sequential:
    def __init__(self, operations):
        self.operations = operations

    def __iadd__(self, other):
        if isinstance(other, Sequential):
            self.operations.extend(other.operations)
        elif isinstance(other, Parallel):
            self.operations.append(other)
        elif isinstance(other, Operator):
            self.operations.append(other)
        else:
            raise ValueError(f"{type(other)} is not usable with type:{type(self)}. This class can only add Operators (SequentialOperator, ParallelOperator, Operator)")

        return self

    def __add__(self, other):
        return self.add(other)

    def __call__(self, *args, **kwargs):

        output = self.operations[0](*args, **kwargs)
        for operation in self.operations[1:]:

            output = operation(*output)

            if not isinstance(output, tuple):
                output = tuple([output])

        return output

    def add(self, other):
        operations = self.operations

        if isinstance(other, Sequential):
            return Sequential(operations.extend(other.operations))
        elif isinstance(other, Parallel):
            return Sequential(operations.append(other))
        elif isinstance(other, Operator):
            return Sequential(operations.append(other))
        else:
            raise ValueError(
                f"{type(other)} is not usable with type:{type(self)}. This class can only add Operators (SequentialOperator, ParallelOperator, Operator)")
