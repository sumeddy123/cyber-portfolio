import unittest
from bst import BinarySearchTree


class TreeTests(unittest.TestCase):
    def test_empty_and_missing(self):
        tree = BinarySearchTree()
        self.assertEqual(list(tree.inorder()), [])
        self.assertFalse(tree.contains(0))

    def test_duplicates_and_ordering(self):
        tree = BinarySearchTree()
        for value in [8, 3, -1, 10, 6, 3]:
            tree.insert(value)
        self.assertEqual(list(tree.inorder()), [-1, 3, 6, 8, 10])
        self.assertEqual(tree.size, 5)
        self.assertFalse(tree.insert(8))
        self.assertTrue(tree.contains(6))
        self.assertFalse(tree.contains(7))

    def test_skewed_tree_without_recursion_limit(self):
        tree = BinarySearchTree()
        for value in range(1100):
            tree.insert(value)
        self.assertEqual(list(tree.inorder()), list(range(1100)))
        self.assertTrue(tree.contains(1099))

    def test_rejects_non_integer_keys(self):
        for value in ['1', True, 1.5, None]:
            with self.assertRaises(TypeError):
                BinarySearchTree().insert(value)
