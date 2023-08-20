# Name: Minyi Huang
# OSU Email: huanminy@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 3
# Due Date: May 8th, 2023
# Description: Assignment 3 - Singly Linked List


from SLNode import *


class SLLException(Exception):
    """
    Custom exception class to be used by Singly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class LinkedList:
    def __init__(self, start_list=None) -> None:
        """
        Initialize new linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = SLNode(None)

        # populate SLL with initial values (if provided)
        # before using this feature, implement insert_back() method
        if start_list is not None:
            for value in start_list:
                self.insert_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'SLL ['
        node = self._head.next
        while node:
            out += str(node.value)
            if node.next:
                out += ' -> '
            node = node.next
        out += ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        length = 0
        node = self._head.next
        while node:
            length += 1
            node = node.next
        return length

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return not self._head.next

    # ------------------------------------------------------------------ #

    def insert_front(self, value: object) -> None:
        """
        This method adds a new node at the beginning of the list, right after the front sentinel;
        Implementing with O(1) runtime complexity
        """
        cur = self._head.next
        self._head.next = SLNode(value)
        self._head.next.next = cur

    def insert_back(self, value: object) -> None:
        """
        This method adds a new node at the end of the list, implemented with O(N) time complexity
        """
        cur = self._head
        while cur.next:
            cur = cur.next
        cur.next = SLNode(value)

    def insert_at_index(self, index: int, value: object) -> None:
        """
        This method inserts a new value at the specified index, implemented with O(N) time complexity
        """
        if index > self.length() or index < 0:
            raise SLLException

        count = 0
        cur = self._head

        while count < index:
            cur = cur.next
            count += 1

        temp_holder = cur.next
        cur.next = SLNode(value)
        cur.next.next = temp_holder

    def remove_at_index(self, index: int) -> None:
        """
        This method removes the node at the specified index position from the linked list,
        implemented with O(N) time complexity
        """
        if index < 0 or index >= self.length():
            raise SLLException

        count = 0
        cur = self._head

        while count < index:
            cur = cur.next
            count += 1

        temp_holder = cur.next.next
        cur.next = temp_holder

    def remove(self, value: object) -> bool:
        """
        This method returns True if a node that matches the provided value object was removed,
        implemented with O(N) time complexity
        """
        cur = self._head

        while cur.next:
            if cur.next.value == value:
                temp_holder = cur.next.next
                cur.next = temp_holder
                return True

            cur = cur.next

        return False

    def count(self, value: object) -> int:
        """
        This method counts and returns the number of elements in the list that match the provided “value” object,
        implemented with O(N) time complexity
        """
        count = 0
        cur = self._head

        while cur.next:
            if cur.next.value == value:
                count += 1

            cur = cur.next

        return count

    def find(self, value: object) -> bool:
        """
        This method returns a Boolean value based on whether the provided “value” object exists in the list,
        implemented with O(N) time complexity
        """
        cur = self._head

        while cur.next:
            if cur.next.value == value:
                return True

            cur = cur.next

        return False

    def slice(self, start_index: int, size: int) -> "LinkedList":
        """
        This method returns a new LinkedList object that contains the requested number of nodes from the original list,
        starting with the node located at the requested start index.

        Runtime complexity: O(N)
        """
        # 1. Check for invalid index
        if start_index < 0 or start_index >= self.length():
            raise SLLException

        # 2. Check for invalid size
        if size < 0 or (size + start_index) > self.length():
            raise SLLException

        position = 0
        cur = self._head
        newll = LinkedList()

        while position < start_index:
            position += 1
            cur = cur.next

        # break the while loop when found the targeted index

        position = 0
        new_cur = newll._head

        while position < size:
            position += 1
            value = cur.next.value
            new_cur.next = SLNode(value)   # add node to the new linked list object, whose value comes from the cur.next
            cur = cur.next
            new_cur = new_cur.next

        return newll


if __name__ == "__main__":

    print("\n# insert_front example 1")
    test_case = ["A", "B", "C"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_front(case)
        print(lst)

    print("\n# insert_back example 1")
    test_case = ["C", "B", "A"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_back(case)
        print(lst)

    print("\n# insert_at_index example 1")
    lst = LinkedList()
    test_cases = [(0, "A"), (0, "B"), (1, "C"), (3, "D"), (-1, "E"), (5, "F")]
    for index, value in test_cases:
        print("Inserted", value, "at index", index, ": ", end="")
        try:
            lst.insert_at_index(index, value)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove_at_index example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6])
    print(f"Initial LinkedList : {lst}")
    for index in [0, 2, 0, 2, 2, -2]:
        print("Removed at index", index, ": ", end="")
        try:
            lst.remove_at_index(index)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [7, 3, 3, 3, 3]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# remove example 2")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [1, 2, 3, 1, 2, 3, 3, 2, 1]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# count example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 2])
    print(lst, lst.count(1), lst.count(2), lst.count(3), lst.count(4))

    print("\n# find example 1")
    lst = LinkedList(["Waldo", "Clark Kent", "Homer", "Santa Claus"])
    print(lst)
    print(lst.find("Waldo"))
    print(lst.find("Superman"))
    print(lst.find("Santa Claus"))

    print("\n# slice example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ll_slice = lst.slice(1, 3)
    print("Source:", lst)
    print("Start: 1 Size: 3 :", ll_slice)
    ll_slice.remove_at_index(0)
    print("Removed at index 0 :", ll_slice)

    print("\n# slice example 2")
    lst = LinkedList([10, 11, 12, 13, 14, 15, 16])
    print("Source:", lst)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1)]
    for index, size in slices:
        print("Start:", index, "Size:", size, end="")
        try:
            print(" :", lst.slice(index, size))
        except:
            print(" : exception occurred.")
