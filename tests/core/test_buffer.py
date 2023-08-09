import unittest
from langtree.core.buffer import Buffer


class TestBuffer(unittest.TestCase):

    def test_init(self):
        buffer = Buffer(5)
        self.assertEqual(len(buffer.memory), 0)

    def test_append_within_length(self):
        buffer = Buffer(5)
        buffer.append(1)
        self.assertEqual(buffer.memory, [1])

    def test_append_exceeding_length(self):
        buffer = Buffer(3)
        buffer.append(1)
        buffer.append(2)
        buffer.append(3)
        buffer.append(4)
        self.assertEqual(buffer.memory, [2, 3, 4])

    def test_extend_within_length(self):
        buffer = Buffer(5)
        buffer.extend([1, 2, 3])
        self.assertEqual(buffer.memory, [1, 2, 3])

    def test_extend_exceeding_length(self):
        buffer = Buffer(3)
        buffer.extend([1, 2, 3, 4, 5])
        self.assertEqual(buffer.memory, [3, 4, 5])

    def test_add_with_item(self):
        buffer = Buffer(5)
        buffer + 5
        self.assertEqual(buffer.memory, [5])

    def test_add_with_list(self):
        buffer = Buffer(5)
        buffer + [1, 2, 3]
        self.assertEqual(buffer.memory, [1, 2, 3])

    def test_iadd_with_item(self):
        buffer = Buffer(5)
        buffer += 5
        self.assertEqual(buffer.memory, [5])

    def test_iadd_with_list(self):
        buffer = Buffer(5)
        buffer += [1, 2, 3]
        self.assertEqual(buffer.memory, [1, 2, 3])

    def test_repr(self):
        buffer = Buffer(5)
        buffer.extend([1, 2, 3])
        self.assertEqual(repr(buffer), "[1, 2, 3]")

if __name__ == "__main__":
    unittest.main()
