# Name: Minyi Huang
# OSU Email: huanminy@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: May 22nd, 2023
# Description: AVL Tree


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        This method adds a new value to the tree while maintaining its AVL property.
        If the value is already in the tree, the method will not change the tree.
        O(log N) runtime complexity.
        """

        if self.is_empty():
            self._root = AVLNode(value)
            return

        cur = self._root
        new_node = AVLNode(value)

        while cur:                                                       # O(height), height = logN
            if value == cur.value:
                return

            if value < cur.value and cur.left:
                cur = cur.left

            elif value < cur.value and not cur.left:
                cur.left = new_node
                new_node.parent = cur
                cur = None

            elif value > cur.value and cur.right:
                cur = cur.right

            elif value > cur.value and not cur.right:
                cur.right = new_node
                new_node.parent = cur
                cur = None

        parent = new_node.parent
        while parent:                                                      # O(height), height = logN
            self._update_height(parent)                                    # O(1)
            self._rebalance(parent)                                        # O(1)
            parent = parent.parent

    def remove(self, value: object) -> bool:
        """
        This method removes the value from the AVL tree.
        The method returns True if the value is removed. Otherwise, it returns False.
        O(log N) runtime complexity.
        """
        cur = self._root

        while cur.value != value:                                          # O(height), height = logN
            if value < cur.value and cur.left:
                cur = cur.left

            elif value < cur.value and not cur.left:
                return False

            elif value > cur.value and cur.right:
                cur = cur.right

            elif value > cur.value and not cur.right:
                return False

        parent = cur.parent

        if not cur.left and not cur.right:
            self._remove_no_subtrees(parent, cur)                           # O(1)

        elif cur.left and cur.right:
            if cur == self._root:
                parent = self._root
            parent = self._remove_two_subtrees(parent, cur)                 # O(height), height = logN

        elif not cur.left or not cur.right:
            left_tree = cur.left
            right_tree = cur.right
            self._remove_one_subtree(parent, cur)                           # O(1)
            if left_tree:
                left_tree.parent = parent

            elif right_tree:
                right_tree.parent = parent

        while parent:                                                       # O(height), height = logN
            self._update_height(parent)                                     # O(1)
            self._rebalance(parent)                                         # O(1)
            parent = parent.parent

        return True

    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        This method helps the remove method to remove a node with two subtrees,
        replacing it with the leftmost child of the right subtree (i.e. the inorder successor).
        O(height), height = log(n)
        """

        # 1. Preserve the left & right subtree of the node
        left_tree = remove_node.left
        right_tree = remove_node.right
        if not remove_node.right.left:
            right_tree = remove_node.right.right

        # 2. Find the inorder successor and its parent
        #    If there is not an inorder successor, leftmost_child = remove_node.right
        result = self._inorder_successor_parent(remove_parent, remove_node)         # O(height), height = log(n)
        leftmost_parent = result[0]
        leftmost_child = result[1]
        leftmost_child.parent = None

        # 3. Attach the left & right subtree to the leftmost_child,
        #    and Update the pointers respectively
        leftmost_parent.left = leftmost_child.right
        if leftmost_child.right:
            leftmost_child.right.parent = leftmost_parent

        leftmost_child.left = left_tree
        left_tree.parent = leftmost_child

        if right_tree:
            leftmost_child.right = right_tree
            right_tree.parent = leftmost_child

        # 4. Update pointers of the remove parent or reassign the root of the tree
        if leftmost_child == remove_node.right:
            if remove_node == self._root:
                self._root = leftmost_child

            elif remove_node == remove_parent.left:
                remove_parent.left = leftmost_child
                leftmost_child.parent = remove_parent

            else:
                remove_parent.right = leftmost_child
                leftmost_child.parent = remove_parent

            return leftmost_child  # see if the new root/subtree root breaks the balance

        else:
            if remove_node == self._root:
                self._root = leftmost_child

            else:
                if remove_node != self._root:
                    if remove_node == remove_parent.left:
                        remove_parent.left = leftmost_child

                    else:
                        remove_parent.right = leftmost_child

                    leftmost_child.parent = remove_parent

            return leftmost_parent  # see if the balance breaks after the leftmost child becomes the new (sub)tree root

    def _balance_factor(self, node: AVLNode) -> int:
        """
        This method returns the balance factor of an AVL node
        O(1)
        """
        right_height = 0
        left_height = 0

        if node.right:
            right_height = node.right.height

            if not node.left:
                balance_factor = right_height + 1
                return balance_factor

        if node.left:
            left_height = node.left.height

            if not node.right:
                balance_factor = - (left_height + 1)
                return balance_factor

        balance_factor = right_height - left_height

        return balance_factor

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        This method rotates a right-heavy subtree
        O(1)
        """
        new_subroot = node.right
        node.right = new_subroot.left
        if node.right:
            node.right.parent = node

        if node.parent and node == node.parent.left:
            node.parent.left = new_subroot

        elif node.parent and node == node.parent.right:
            node.parent.right = new_subroot

        new_subroot.left = node
        new_subroot.parent = node.parent
        node.parent = new_subroot

        self._update_height(node)
        self._update_height(new_subroot)

        return new_subroot

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        This method rotates a left-heavy subtree
        O(1)
        """
        new_subroot = node.left
        node.left = new_subroot.right
        if node.left:
            node.left.parent = node

        if node.parent and node == node.parent.left:
            node.parent.left = new_subroot

        elif node.parent and node == node.parent.right:
            node.parent.right = new_subroot

        new_subroot.right = node
        new_subroot.parent = node.parent
        node.parent = new_subroot
        self._update_height(node)
        self._update_height(new_subroot)

        return new_subroot

    def _update_height(self, node: AVLNode) -> None:
        """
        This method updates the height of a node after rotation(s)
        O(1)
        """
        right_height = 0
        left_height = 0

        if node.right:
            right_height = node.right.height

        if node.left:
            left_height = node.left.height

        if not node.left and not node.right:
            node.height = 0

        elif right_height > left_height:
            node.height = right_height + 1

        else:
            node.height = left_height + 1

    def _rebalance(self, node: AVLNode) -> None:
        """
        This method rebalances the tree whenever we do insert/remove
        O(1)
        """

        balance_factor = self._balance_factor(node)

        # left-heavy
        if balance_factor < -1:
            # subtree right heavy
            if self._balance_factor(node.left) > 0:
                node.left = self._rotate_left(node.left)
                node.left.parent = node

            new_subroot = self._rotate_right(node)
            if node == self._root:
                self._root = new_subroot

        # right heavy
        elif balance_factor > 1:
            # subtree left heavy
            if self._balance_factor(node.right) < 0:
                node.right = self._rotate_right(node.right)
                node.right.parent = node

            new_subroot = self._rotate_left(node)

            if node == self._root:
                self._root = new_subroot

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
