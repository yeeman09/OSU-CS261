# Name: Minyi Huang
# OSU Email: huanminy@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 2
# Due Date: May 1st, 2023
# Description: Assignment 2


from dynamic_array import *


class Bag:
    def __init__(self, start_bag=None):
        """
        Init new bag based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._da = DynamicArray()

        # populate bag with initial values (if provided)
        # before using this feature, implement add() method
        if start_bag is not None:
            for value in start_bag:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "BAG: " + str(self._da.length()) + " elements. ["
        out += ', '.join([str(self._da.get_at_index(_))
                          for _ in range(self._da.length())])
        return out + ']'

    def size(self) -> int:
        """
        Return total number of items currently in the bag
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.length()

    # -----------------------------------------------------------------------

    def add(self, value: object) -> None:
        """
        This method adds a new element to the bag, with O(1） amortized runtime complexity
        """
        self._da.append(value)

    def remove(self, value: object) -> bool:
        """
        This method removes any one element from the bag that matches the parameter value object.
        If removed, return True; otherwise, return False
        """
        index = None
        for i in range(self._da.length()):
            if self._da.get_at_index(i) == value:
                index = i
                break

        if index is None:
            return False

        else:
            self._da.remove_at_index(index)
            return True

    def count(self, value: object) -> int:
        """
        This method returns the number of elements in the bag that match the provided value object
        """
        number = 0
        for i in range(self._da.length()):
            if self._da.get_at_index(i) == value:
                number += 1

        return number

    def clear(self) -> None:
        """
        This method clears the contents of the bag
        """
        self._da = DynamicArray()

    def equal(self, second_bag: "Bag") -> bool:
        """
        The method returns True if the bags are equal (contain the same number of elements,
        and also contain the same elements without regard to the order of elements). Otherwise, it returns False.
        """

        if self._da.is_empty() and second_bag._da.is_empty():
            return True

        if self._da.length() == second_bag._da.length():       # if two bags are equal, they should have the same length
            for i in range(self._da.length()):
                instance = self._da.get_at_index(i)
                bag1_count = self.count(instance)              # see how many instances there are in bag 1
                bag2_count = second_bag.count(instance)        # see how many instances there are in bag 2
                if bag1_count == bag2_count:                   # if counts equal, then continue looping
                    continue

                else:                                          # else, directly break the loop by returning False
                    return False

            return True                                        # looped through two bags and all counts are equal

        else:                                                  # if two bags do not have the same length, then not equal
            return False

    def __iter__(self):
        """
        Create iterator for loop
        """
        self.index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        """
        try:
            value = self._da[self.index]
        except DynamicArrayException:
            raise StopIteration

        self.index += 1
        return value


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# add example 1")
    bag = Bag()
    print(bag)
    values = [10, 20, 30, 10, 20, 30]
    for value in values:
        bag.add(value)
    print(bag)

    print("\n# remove example 1")
    bag = Bag([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(bag)
    print(bag.remove(7), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)

    print("\n# count example 1")
    bag = Bag([1, 2, 3, 1, 2, 2])
    print(bag, bag.count(1), bag.count(2), bag.count(3), bag.count(4))

    print("\n# clear example 1")
    bag = Bag([1, 2, 3, 1, 2, 3])
    print(bag)
    bag.clear()
    print(bag)

    print("\n# equal example 1")
    bag1 = Bag([10, 20, 30, 40, 50, 60])
    bag2 = Bag([60, 50, 40, 30, 20, 10])
    bag3 = Bag([10, 20, 30, 40, 50])
    bag_empty = Bag()

    print(bag1, bag2, bag3, bag_empty, sep="\n")
    print(bag1.equal(bag2), bag2.equal(bag1))
    print(bag1.equal(bag3), bag3.equal(bag1))
    print(bag2.equal(bag3), bag3.equal(bag2))
    print(bag1.equal(bag_empty), bag_empty.equal(bag1))
    print(bag_empty.equal(bag_empty))
    print(bag1, bag2, bag3, bag_empty, sep="\n")

    bag1 = Bag([100, 200, 300, 200])
    bag2 = Bag([100, 200, 30, 100])
    print(bag1.equal(bag2))

    bag1 = Bag([1, 1, 2])
    bag2 = Bag([2, 1, 2])
    print(bag1.equal(bag2))
    print(bag2.equal(bag1))

    print("\n# __iter__(), __next__() example 1")
    bag = Bag([5, 4, -8, 7, 10])
    print(bag)
    for item in bag:
        print(item)

    print("\n# __iter__(), __next__() example 2")
    bag = Bag(["orange", "apple", "pizza", "ice cream"])
    print(bag)
    for item in bag:
        print(item)
