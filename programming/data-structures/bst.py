"""Integer binary search tree with iterative operations and unique keys."""
from dataclasses import dataclass


@dataclass
class Node:
    value: int
    left: 'Node | None' = None
    right: 'Node | None' = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.size = 0

    @staticmethod
    def _validate(value):
        if type(value) is not int:
            raise TypeError('keys must be integers')

    def insert(self, value):
        """Return True for a new key; False when the key already exists."""
        self._validate(value)
        if self.root is None:
            self.root = Node(value)
            self.size = 1
            return True
        node = self.root
        while True:
            if value == node.value:
                return False
            side = 'left' if value < node.value else 'right'
            child = getattr(node, side)
            if child is None:
                setattr(node, side, Node(value))
                self.size += 1
                return True
            node = child

    def contains(self, value):
        self._validate(value)
        node = self.root
        while node:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False

    def inorder(self):
        stack, node = [], self.root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            yield node.value
            node = node.right


if __name__ == '__main__':
    tree = BinarySearchTree()
    for key in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
        tree.insert(key)
    print('Sorted keys:', list(tree.inorder()))
    print('Contains 6:', tree.contains(6))
    print('Contains 99:', tree.contains(99))
