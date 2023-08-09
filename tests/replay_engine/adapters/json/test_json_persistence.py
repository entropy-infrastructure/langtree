import unittest
import os
from tinychain.replay_engine import Chain
from tinychain.replay_engine.adapters.json import JSONStore
from tinychain.replay_engine.test_utils import flatten_records


@Chain.record()
def add(x, y):
    return x + y


@Chain.record("test", "test2")
def multiply(x, y):
    return x * y


class TestJSONStore(unittest.TestCase):
    def setUp(self):
        self.data_storage = JSONStore("test_data.json", multirun=True)

    def tearDown(self):
        if os.path.exists("test_data.json"):
            os.remove("test_data.json")

    def test_read_all_chains(self):
        """
        Tests reading all chains from the data storage.
        """
        with Chain("chain1", persistence_strategy=self.data_storage):
            add(1, 2)

        with Chain("chain2", persistence_strategy=self.data_storage):
            multiply(2, 3)

        all_data = self.data_storage.read()
        self.assertIsNotNone(all_data)
        self.assertEqual(len(all_data), 2)
        self.assertIn("chain1", all_data)
        self.assertIn("chain2", all_data)

    def test_read_specific_chain(self):
        """
        Tests reading a specific chain from the data storage.
        """
        with Chain("chain1", persistence_strategy=self.data_storage):
            add(1, 2)

        with Chain("chain2", persistence_strategy=self.data_storage):
            multiply(2, 3)

        chain1_data = self.data_storage.read("chain1")
        self.assertIsNotNone(chain1_data)
        self.assertEqual(len(flatten_records(chain1_data)), 1)  # 1 function call in chain1

        chain2_data = self.data_storage.read("chain2")
        self.assertIsNotNone(chain2_data)
        self.assertEqual(len(flatten_records(chain2_data)), 1)  # 1 function call in chain2

    def test_read_non_existent_chain(self):
        """
        Tests reading a non-existent chain from the data storage.
        """
        with Chain("chain1", persistence_strategy=self.data_storage):
            add(1, 2)

        non_existent_chain_data = self.data_storage.read("non_existent_chain")
        self.assertIsNone(non_existent_chain_data)
