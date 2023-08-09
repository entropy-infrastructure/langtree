import unittest
import os
from langtree.replay_engine.chain import ChainRecorder
from langtree.replay_engine.adapters.json import JSONStore
from langtree.replay_engine.test_utils import flatten_records


@ChainRecorder.record()
def add(x, y):
    return x + y


@ChainRecorder.record("test", "test2")
def multiply(x, y):
    return x * y


@ChainRecorder.record()
def subtract(x, y):
    return x - y


@ChainRecorder.record()
def calculate_area(length, width):
    """
    Function to calculate the area of a rectangle. Calls multiply() function internally.
    """
    return multiply(length, width)


@ChainRecorder.record()
def calculate_perimeter(length, width):
    """
    Function to calculate the perimeter of a rectangle. Calls add() function internally.
    """
    return multiply(add(length, width), 2)

class TestChain(unittest.TestCase):
    def test_unnamed_chain(self):
        """
        Tests unnamed Chain objects and checks that recorded function executions are logged.
        """
        with ChainRecorder() as unnamed_chain:
            result = add(3, 4)
            self.assertEqual(result, 7)
            self.assertEqual(unnamed_chain.last()['output'], 7)

    def test_named_chain(self):
        """
        Tests named Chain objects and checks that only executions of functions registered with the named chain are logged.
        """
        with ChainRecorder("test") as test_chain:
            result = multiply(3, 4)
            self.assertEqual(result, 12)
            self.assertEqual(test_chain.last()['output'], 12)

    def test_nested_calls(self):
        """
        Tests that nested calls are recorded in the correct order.
        """
        @ChainRecorder.record()
        def nested_function(x, y):
            subtract_result = subtract(x, y)
            add_result = add(x, y)
            return subtract_result, add_result

        with ChainRecorder() as nested_chain:
            result = nested_function(10, 5)
            self.assertEqual(result, (5, 15))
            self.assertEqual(nested_chain.last()['output'], (5, 15))

    def test_clear_records(self):
        """
        Tests that the clear_records function works correctly.
        """
        with ChainRecorder() as unnamed_chain:
            add(1, 2)
            unnamed_chain.clear()
            self.assertEqual(unnamed_chain.total(), 0)

    def test_checkpoint_restore(self):
        """
        Tests the checkpoint and restore functionality.
        """
        with ChainRecorder() as unnamed_chain:
            add(1, 2)
            unnamed_chain.checkpoint()
            add(3, 4)
            unnamed_chain.checkpoint()
            self.assertEqual(unnamed_chain.total(), 2)

            unnamed_chain.restore(0)
            self.assertEqual(unnamed_chain.total(), 1)


class TestFunctionNesting(unittest.TestCase):
    def setUp(self):
        self.data_storage = JSONStore("test_data.json")

    def tearDown(self):
        if os.path.exists("test_data.json"):
            os.remove("test_data.json")

    def test_single_nesting(self):
        """
        Tests a single level of function nesting.
        """
        with ChainRecorder("nested1", persistence_strategy=self.data_storage):
            multiply(add(3, 4), 2)  # should return 14

        chain_data = self.data_storage.read("nested1")
        self.assertIsNotNone(chain_data)
        records = flatten_records(chain_data['nested1'])
        self.assertEqual(len(records), 2)  # 2 function calls
        self.assertEqual(records[0]['function'], 'add')
        self.assertEqual(records[0]['output'], 7)
        self.assertEqual(records[1]['function'], 'multiply')
        self.assertEqual(records[1]['output'], 14)

    def test_double_nesting(self):
        """
        Tests two levels of function nesting.
        """
        with ChainRecorder("nested2", persistence_strategy=self.data_storage):
            multiply(add(multiply(2, 2), 1), 3)  # should return 15

        chain_data = self.data_storage.read("nested2")
        self.assertIsNotNone(chain_data)
        records = flatten_records(chain_data['nested2'])
        self.assertEqual(len(records), 3)  # 3 function calls
        self.assertEqual(records[0]['function'], 'multiply')
        self.assertEqual(records[0]['output'], 4)
        self.assertEqual(records[1]['function'], 'add')
        self.assertEqual(records[1]['output'], 5)
        self.assertEqual(records[2]['function'], 'multiply')
        self.assertEqual(records[2]['output'], 15)

class TestExternalFunction(unittest.TestCase):
    def setUp(self):
        self.data_storage = JSONStore("test_data.json")

    def tearDown(self):
        if os.path.exists("test_data.json"):
            os.remove("test_data.json")

    def test_external_function(self):
        """
        Tests an external function calling multiply() and add().
        """
        with ChainRecorder("external", persistence_strategy=self.data_storage):
            calculate_area(5, 4)  # should return 20
            calculate_perimeter(5, 4)  # should return 18

        chain_data = self.data_storage.read("external")
        self.assertIsNotNone(chain_data)
        records = flatten_records(chain_data['external'])
        self.assertEqual(len(records), 5)  # 5 function calls
        self.assertEqual(records[0]['function'], 'calculate_area')
        self.assertEqual(records[0]['output'], 20)
        self.assertEqual(records[1]['function'], 'multiply')
        self.assertEqual(records[1]['output'], 20)
        self.assertEqual(records[2]['function'], 'calculate_perimeter')
        self.assertEqual(records[2]['output'], 18)


if __name__ == "__main__":
    unittest.main()
