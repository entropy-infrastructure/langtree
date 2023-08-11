import unittest
from langtree.core import Operator
from langtree.operators import Sequential, Parallel, chainable

class TestOperators(unittest.TestCase):

    # Test basic Operator functionality
    def test_basic_operator(self):
        op = Operator()
        result = op(a=5, b=10)
        self.assertEqual(result, {'a': 5, 'b': 10})

    # Test freezing of Operator arguments
    def test_operator_freeze(self):
        op = Operator()
        op.freeze_call(a=5)
        result = op(b=10)
        self.assertEqual(result, {'a': 5, 'b': 10})

    # Test chainable decorator
    @chainable
    def add(a, b):
        return a + b

    def test_chainable(self):
        op = self.add(a=5, b=3)
        result = op()
        self.assertEqual(result, 8)

    # Test Parallel and Sequential classes
    def test_parallel(self):
        op1 = Operator(call=lambda x: x + 1)
        op2 = Operator(call=lambda x: x * 2)
        parallel = Parallel([op1, op2])
        result = parallel(5)
        self.assertEqual(result, [6, 10])

    def test_sequential(self):
        op1 = Operator(call=lambda x: x + 1)
        op2 = Operator(call=lambda x: x * 2)
        sequential = Sequential([op1, op2])
        result = sequential(5)
        self.assertEqual(result, 12)

    # Test combining operators in Parallel and Sequential classes
    def test_combining(self):
        op1 = Operator(call=lambda x: x + 1)
        op2 = Operator(call=lambda x: x * 2)
        sequential = Sequential([op1])
        parallel = Parallel([op2])
        combined = sequential + parallel
        result = combined(5)
        self.assertEqual(result, [12])

    # Test edge cases
    def test_invalid_add_to_parallel(self):
        with self.assertRaises(ValueError):
            parallel = Parallel([])
            parallel += "invalid"

    def test_invalid_add_to_sequential(self):
        with self.assertRaises(ValueError):
            sequential = Sequential([])
            sequential += "invalid"


class TestEdgeCases(unittest.TestCase):

    # 1. Empty Operations
    def test_empty_parallel(self):
        parallel = Parallel([])
        result = parallel(5)
        self.assertEqual(result, [])

    def test_empty_sequential(self):
        sequential = Sequential([])
        result = sequential(5)
        self.assertEqual(result, (5,))

    # 2. Non-callable Operations
    def test_non_callable_parallel(self):
        with self.assertRaises(ValueError):
            parallel = Parallel([5])

    def test_non_callable_sequential(self):
        with self.assertRaises(ValueError):
            sequential = Sequential([5])

    # 3. Multiple Arguments
    op1 = Operator(call=lambda x, y: x + y)
    op2 = Operator(call=lambda x, y: x * y)
    op3 = Operator(call=lambda x: x + 1)
    op4 = Operator(call=lambda x, y: x * 2)

    def test_parallel_multiple_args(self):
        parallel = Parallel([self.op1, self.op2])
        result = parallel(5, 3)
        self.assertEqual(result, [8, 15])

    def test_sequential_multiple_args(self):
        sequential = Sequential([self.op1, self.op3])
        result = sequential(5, 3)
        self.assertEqual(result, 9)

    # 4. Nested Combinations
    def test_nested_combinations(self):

        inner_sequential = Sequential([self.op1, self.op3])
        outer_parallel = Parallel([inner_sequential, self.op4])

        result = outer_parallel(5, 3)
        self.assertEqual(result, [9, 10])

    # 5. Return Types
    def test_parallel_return_type(self):
        parallel = Parallel([self.op1])
        result = parallel(5, 3)
        self.assertIsInstance(result, list)

    def test_sequential_return_type(self):
        sequential = Sequential([self.op1])
        result = sequential(5, 3)
        self.assertNotIsInstance(result, list)
        self.assertNotIsInstance(result, tuple)


if __name__ == '__main__':
    unittest.main()
