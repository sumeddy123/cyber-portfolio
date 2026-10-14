# Binary search tree

A dependency-free Python implementation with integer keys, duplicate suppression, iterative insertion and search, and an in-order generator.

```bash
python programming/data-structures/bst.py
python -m unittest discover -s programming/data-structures -v
```

Expected sorted keys: `[1, 3, 4, 6, 7, 8, 10, 13, 14]`. Search for 6 returns True; search for 99 returns False.

Insertion and search take O(h), where h is tree height. A balanced shape gives O(log n); sorted insertion can make this unbalanced tree O(n) per operation. Traversal takes O(n) time and O(h) auxiliary space. Iterative code avoids recursion depth errors, but does not solve the skewed-tree performance problem.

Tests cover empty trees, duplicates, negative keys, missing keys, invalid types, and a 1,100-node skewed tree. Booleans are deliberately rejected even though Python treats bool as an int subclass. Deletion and self-balancing are not implemented.

Next exercise: implement minimum/maximum lookup, then explain when a dictionary would be a better choice.
