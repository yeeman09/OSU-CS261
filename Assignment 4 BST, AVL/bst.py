# Name: Minyi Huang
# OSU Email: huanminy@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: May 22nd, 2023
# Description: Binary Search Tree


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        This method adds a new value to the tree.
        Duplicate values are allowed and will be added to the right subtree of that node.
        O(N) runtime complexity.
        """
        if self._root is None:
            self._root = BSTNode(value)

        else:
            curr_node = self._root

            while curr_node:
                if value >= curr_node.value and curr_node.right:
                    curr_node = curr_node.right

                elif value >= curr_node.value and not curr_node.right:
                    curr_node.right = BSTNode(value)
                    return

                elif value < curr_node.value and curr_node.left:
                    curr_node = curr_node.left

                elif value < curr_node.value and not curr_node.left:
                    curr_node.left = BSTNode(value)
                    return

    def remove(self, value: object) -> bool:
        """
        This method removes a value from the tree. The method returns True if the value is removed.
        Otherwise, it returns False.
            1. When removing a node with two subtrees, replace it with the leftmost child of the right subtree
            2. If the deleted node only has one subtree (either right or left),
                replace the deleted node with the root node of that subtree.

        O(N) runtime complexity.
        """
        if not self._root:
            return False

        cur = self._root
        parent_node = self._root
        while cur.value != value:                          # O(N)
            if value > cur.value and cur.right:
                parent_node = cur
                cur = cur.right

            elif value > cur.value and not cur.right:
                return False

            elif value < cur.value and cur.left:
                parent_node = cur
                cur = cur.left

            elif value < cur.value and not cur.left:
                return False

        if not cur.left and not cur.right:
            self._remove_no_subtrees(parent_node, cur)      # O(1)

        elif cur.left and cur.right:
            self._remove_two_subtrees(parent_node, cur)     # O(N)

        elif not cur.left or not cur.right:
            self._remove_one_subtree(parent_node, cur)      # O(1)

        return True

    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        A helper method that helps the remove method to remove a node
        that does not have subtrees
        O(1)
        """
        if remove_node == self._root:
            self._root = None

        elif remove_parent.left == remove_node:
            remove_parent.left = None

        else:
            remove_parent.right = None

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        A helper method that helps the remove method to remove a node
        that has a left or right subtree (only)
        O(1)
        """
        if remove_node == self._root:
            if remove_node.left:
                self._root = remove_node.left

            else:
                self._root = remove_node.right

        elif remove_node == remove_parent.left:
            if remove_node.left:
                remove_parent.left = remove_node.left

            else:
                remove_parent.left = remove_node.right

        elif remove_node == remove_parent.right:
            if remove_node.left:
                remove_parent.right = remove_node.left

            else:
                remove_parent.right = remove_node.right

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        A helper method that helps the remove method to remove a node
        that has two subtrees and replace it with the leftmost child of the right subtree
        O(N)
        """

        # 1. Preserve the left & right subtree first
        left_tree = remove_node.left
        right_tree = remove_node.right
        if not remove_node.right.left:
            right_tree = remove_node.right.right

        # 2. Find the inorder successor and its parent for later use
        result = self._inorder_successor_parent(remove_parent, remove_node)         # O(N)
        leftmost_parent = result[0]
        leftmost_child = result[1]

        # 3. Update leftmost parent and Attach the right & left subtree to this leftmost child
        leftmost_parent.left = leftmost_child.right
        leftmost_child.right = None

        leftmost_child.left = left_tree
        leftmost_child.right = right_tree

        # 4. Update remove parent's pointer
        if remove_node != self._root:
            if remove_node == remove_parent.left:
                remove_parent.left = leftmost_child

            else:
                remove_parent.right = leftmost_child

        else:
            self._root = leftmost_child

    def _inorder_successor_parent(self, remove_parent: BSTNode, remove_node: BSTNode) -> (BSTNode, BSTNode):
        """
        A helper method that finds a node's inorder successor and the successor's parent
        O(N)
        """
        curr_node = remove_node.right
        parent_node = remove_node
        while curr_node.left:
            parent_node = curr_node
            curr_node = curr_node.left

        inorder_successor = curr_node

        return parent_node, inorder_successor

    def contains(self, value: object) -> bool:
        """
        This method returns True if the value is in the tree. Otherwise, it returns False.
        If the tree is empty, the method should return False.
        O(N) runtime complexity.
        """
        if not self._root:
            return False

        cur = self._root

        while cur.value != value:
            if value > cur.value and cur.right:
                cur = cur.right

            elif value > cur.value and not cur.right:
                return False

            elif value < cur.value and cur.left:
                cur = cur.left

            elif value < cur.value and not cur.left:
                return False

        return True

    def inorder_traversal(self) -> Queue:
        """
        This method will perform an inorder traversal of the tree and
        return a Queue object that contains the values of the visited nodes, in the order they were visited.
        If the tree is empty, the method returns an empty Queue.
        O(N) runtime complexity.
        """
        bst_inorder = Queue()

        if self.is_empty():
            return bst_inorder

        self.rec_inorder(self._root, bst_inorder)

        return bst_inorder

    def rec_inorder(self, node: BSTNode, bst_queue: Queue) -> None:
        """
        A recursion helper method that helps inorder traversal
        """

        curr_node = node
        if not curr_node:
            return

        self.rec_inorder(curr_node.left, bst_queue)
        bst_queue.enqueue(curr_node.value)
        self.rec_inorder(curr_node.right, bst_queue)

    def find_min(self) -> object:
        """
        This method returns the lowest value in the tree.
        If the tree is empty, the method should return None.
        O(N) runtime complexity.
        """
        if self.is_empty():
            return None

        cur = self._root
        while cur.left:
            cur = cur.left

        return cur.value

    def find_max(self) -> object:
        """
        This method returns the highest value in the tree.
        If the tree is empty, the method should return None.
        O(N) runtime complexity.
        """
        if self.is_empty():
            return None

        cur = self._root
        while cur.right:
            cur = cur.right

        return cur.value

    def is_empty(self) -> bool:
        """
        This method returns True if the tree is empty. Otherwise, it returns False.
        O(1) runtime complexity.
        """
        if not self._root:
            return True

        else:
            return False

    def make_empty(self) -> None:
        """
        This method removes all the nodes from the tree.
        O(1) runtime complexity
        """
        self._root = None


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    case = (-31, 36, -27, -90, 7, -56, 83, -40, -8, 89)
    tree = BST(case)
    for _ in case:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method remove() example 6")
    print("-------------------------------")
    case = (96, 97, -55, 12, -48, 49, -46, -76, 21, -37)
    tree = BST(case)
    root_value = tree.get_root()
    print('INPUT  :', tree, root_value)
    tree.remove(96)
    if not tree.is_valid_bst():
        raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('RESULT :', tree)
    tree.remove(-55)
    if not tree.is_valid_bst():
        raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
