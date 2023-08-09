import unittest
import os
from langtree.replay_engine.chain import ChainRecorder
from langtree.replay_engine.adapters.json import JSONStore


# Define some functions to use in testing
@ChainRecorder.record()
def add(x, y):
    return x + y

@ChainRecorder.record("test")
def multiply(x, y):
    return x * y

@ChainRecorder.record()
def subtract(x, y):
    return x - y

class TestChainRecorderPersistence(unittest.TestCase):
    def setUp(self):
        self.file_path = "test_data.json"
        self.data_storage = JSONStore(self.file_path)

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_single_run_absolute_persistence(self):
        """
        Tests persistence for a single run absolute strategy.
        """


        with ChainRecorder("c1", persistence_strategy=self.data_storage):
            add(3, 4)
            multiply(5, 6)

        data_storage = JSONStore(self.file_path)
        data = data_storage.read()
        self.assertIsNotNone(data)
        self.assertIn('c1', data)
        self.assertEqual(len(data['c1']), 2)

    def test_single_run_absolute_persistence(self):
        """
        Tests persistence for a single run absolute strategy.
        """


        with ChainRecorder("default", persistence_strategy=self.data_storage):
            add(3, 4)
            multiply(5, 6)

        data_storage = JSONStore(self.file_path)
        data = data_storage.read()
        self.assertIsNotNone(data)
        self.assertIn('default', data)
        self.assertEqual(len(data['default']), 2)

    def test_single_run_incremental_persistence(self):
        """
        Tests persistence for a single run incremental strategy.
        """

        data_storage = JSONStore(self.file_path, incremental=True)

        with ChainRecorder("c2", persistence_strategy=data_storage):
            add(3, 4)
            multiply(5, 6)

        with ChainRecorder() as another_unnamed_ChainRecorder:
            add(1, 2)

        data_storage = JSONStore(self.file_path, incremental=True)
        data = data_storage.read()
        self.assertIsNotNone(data)
        self.assertIn('c2', data)
        self.assertEqual(len(data['c2']), 2)

    def test_multi_run_absolute_persistence(self):
        """
        Tests persistence for a multi-run absolute strategy.
        """

        data_storage = JSONStore(self.file_path, multirun=True)

        with ChainRecorder("test", persistence_strategy=data_storage) as test_ChainRecorder:
            add(3, 4)
            multiply(5, 6)

        with ChainRecorder("test", persistence_strategy=data_storage) as another_test_ChainRecorder:
            add(1, 2)

        data_storage = JSONStore(self.file_path)
        data = data_storage.read()
        self.assertIsNotNone(data)
        self.assertIn('test', data)
        self.assertEqual(len(data['test']), 2)
        self.assertEqual(sum(len(run) for run in data['test']), 3)

    def test_multi_run_incremental_persistence(self):
        """
        Tests persistence for a multi-run incremental strategy.
        """

        data_storage = JSONStore(self.file_path, multirun=True, incremental=True)

        with ChainRecorder("test", persistence_strategy=data_storage) as test_ChainRecorder:
            add(3, 4)
            multiply(5, 6)

        with ChainRecorder("test", persistence_strategy=data_storage) as another_test_ChainRecorder:
            add(1, 2)

        with ChainRecorder("test", persistence_strategy=data_storage) as third_test_ChainRecorder:
            multiply(2, 3)

        data_storage = JSONStore(self.file_path, multirun=True, incremental=True)
        data = data_storage.read()
        self.assertIsNotNone(data)
        self.assertIn('test', data)
        self.assertEqual(len(data['test']), 3)

if __name__ == "__main__":
    unittest.main()