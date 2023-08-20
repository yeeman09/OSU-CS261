# Name: Minyi Huang
# OSU Email: huanminy@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 5
# Due Date: May 30th, 2023
# Description: Min Heap


from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return 'HEAP ' + str(heap_data)

    def add(self, node: object) -> None:
        """
        This method adds a new object to the MinHeap while maintaining heap property.
        O(log N)
        """
        self._heap.append(node)

        if self._heap.length() == 1:
            return

        child_index = self._heap.length() - 1
        parent_index = (child_index - 1) // 2

        # While the newly add node is smaller than its parent node, swap
        while self._heap[child_index] < self._heap[parent_index]:
            placeholder = self._heap[parent_index]
            self._heap[parent_index] = self._heap[child_index]
            self._heap[child_index] = placeholder

            child_index = parent_index
            parent_index = (child_index - 1) // 2

            # if the newly add node already becomes the root value, return
            if child_index == 0:
                return

    def is_empty(self) -> bool:
        """
        This method returns True if the heap is empty; otherwise, it returns False.
        O(1)
        """
        if self._heap.length() == 0:
            return True

        return False

    def get_min(self) -> object:
        """
        This method returns an object with the minimum key, without removing it from the heap.
        If the heap is empty, the method raises a MinHeapException.
        O(1).
        """
        if self._heap.is_empty():
            raise MinHeapException

        return self._heap[0]

    def remove_min(self) -> object:
        """
        This method returns an object with the minimum key, and removes it from the heap.
        If the heap is empty, the method raises a MinHeapException.

        For the downward percolation of the replacement node:
            if both children of the node have the same value (and are both smaller than the node),
            swap with the left child.

        O(log N).
        """

        if self.size() == 0:
            raise MinHeapException

        min_node = self.get_min()
        self._heap[0] = self._heap[self._heap.length() - 1]
        self._heap.pop()

        # TIME TO CHECK NEW ROOT AND ITS CHILD NODES！
        _percolate_down(self._heap, 0, self._heap.length())         # O(log N)

        return min_node

    def build_heap(self, da: DynamicArray) -> None:
        """
        This method receives a DynamicArray with objects in any order, and builds a proper MinHeap from them.
        The current content of the MinHeap is overwritten.
        O(N).
        """
        if da.is_empty():
            self.clear()
            return

        # empty the original heap, copy the values of the passed-in DA into the heap
        self.clear()
        for i in range(da.length()):
            self._heap.append(da[i])

        # build heap:
        # 1. check if the parent node is greater than any of the child nodes
        # 2. if so, exchange, then percolate down from the newly exchanged child node
        starting_index = (self._heap.length() - 2) // 2
        for i in range(starting_index, -1, -1):
            if (2 * i + 2) < self._heap.length():
                if self._heap[i] > self._heap[2*i + 1] or self._heap[i] > self._heap[2*i + 2]:
                    if self._heap[2*i + 1] <= self._heap[2*i + 2]:
                        placeholder = self._heap[i]
                        self._heap[i] = self._heap[2*i+1]
                        self._heap[2*i+1] = placeholder
                        _percolate_down(self._heap, 2*i + 1, self._heap.length())

                    else:
                        placeholder = self._heap[i]
                        self._heap[i] = self._heap[2*i+2]
                        self._heap[2*i+2] = placeholder
                        _percolate_down(self._heap, 2*i + 2, self._heap.length())

            # edge case for the last parent node: it only has left child node
            else:
                if self._heap[i] > self._heap[2 * i + 1]:
                    placeholder = self._heap[i]
                    self._heap[i] = self._heap[2 * i + 1]
                    self._heap[2 * i + 1] = placeholder
                    _percolate_down(self._heap, 2 * i + 1, self._heap.length())

    def size(self) -> int:
        """
        This method returns the number of items currently stored in the heap.
        O(1).
        """
        return self._heap.length()

    def clear(self) -> None:
        """
        This method clears the contents of the heap.
        O(1).
        """
        self._heap = DynamicArray()


def heapsort(da: DynamicArray) -> None:
    """
    This function sorts DA's content in non-ascending order, using the Heapsort algorithm.
    O(N logN).
    """
    starting_index = (da.length() - 2)//2
    for i in range(starting_index, -1, -1):         # O(N)
        _percolate_down(da, i, da.length())

    new_len = da.length() - 1
    for j in range(da.length() - 1):                # O(N*log(N))
        placeholder = da[0]
        da[0] = da[new_len]
        da[new_len] = placeholder
        new_len -= 1

        if new_len != 0:
            _percolate_down(da, 0, new_len + 1)


def _percolate_down(da: DynamicArray, parent: int, da_length: int) -> None:
    """
    This is a helper function that helps remove the minimum in the DA and resorts the original dynamic array.
    O(log(n))
    """

    # left_child index = 2 * parent + 1
    # right_child index = 2 * parent + 2

    while (2 * parent + 1) < da_length:

        # if there is no right child node and parent is not smaller than the left child
        if (2 * parent + 2) > da_length - 1 and da[parent] >= da[2 * parent + 1]:
            placeholder = da[parent]
            da[parent] = da[2 * parent + 1]
            da[2 * parent + 1] = placeholder
            parent = 2 * parent + 1

        # if there is no right child node and parent is smaller than the left child
        elif (2 * parent + 2) > da_length - 1 and da[parent] < da[2 * parent + 1]:
            return

        # there are both left and right child node and the parent node is not smaller than both of them
        elif da[parent] >= da[2 * parent + 1] or da[parent] >= da[2 * parent + 2]:
            if da[2 * parent + 1] <= da[2 * parent + 2]:
                placeholder = da[parent]
                da[parent] = da[2 * parent + 1]
                da[2 * parent + 1] = placeholder
                parent = 2 * parent + 1

            else:
                placeholder = da[parent]
                da[parent] = da[2 * parent + 2]
                da[2 * parent + 2] = placeholder
                parent = 2 * parent + 2

        # there are both left and right child node and the parent node is smaller than both
        elif da[parent] < da[2 * parent + 1] and da[parent] < da[2 * parent + 2]:
            return


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - remove_min example 2")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    h.add(15)
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)

    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)

    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 3")
    print("------------------------")
    da = DynamicArray([100, 45, 24, -90, -50, -300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)
