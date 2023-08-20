# Name: Minyi Huang
# OSU Email: huanminy@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: June 5th, 2023
# Description: Hash Map - Separate Chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key/value pair in the hash map.
        If the given key already exists in the hash map, its associated value will be replaced with the new value.
        If the given key is not in the hash map, a new key/value pair will be added.
        """
        if self.table_load() >= 1:
            new_cap = 2 * self._capacity
            self.resize_table(new_cap)

        index = self._hash_function(key) % self._capacity

        for i in self._buckets[index]:
            if i.key == key:
                i.value = value
                return

        self._buckets[index].insert(key, value)
        self._size += 1

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.
        """
        count = 0
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                count += 1

        return count

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.
        load = total number of elements stored in the table / the number of buckets
        """
        cap = self._capacity
        total_elements = self._size

        load_factor = total_elements / cap

        return load_factor

    def clear(self) -> None:
        """
        This method clears the contents of the hash map.
        It does not change the underlying hash table capacity.
        """
        self._buckets = DynamicArray()

        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table.
        All existing key/value pairs must remain in the new hash map, and all hash table links must be rehashed.
        """

        if new_capacity < 1:
            return

        old_cap = self._capacity
        old_buckets = self._buckets

        if new_capacity >= 1:
            if not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)

        self._capacity = new_capacity
        self.clear()                                # clear the old map for rehash

        for i in range(old_cap):
            if old_buckets[i].length() != 0:
                for j in (old_buckets[i]):
                    self.put(j.key, j.value)

    def get(self, key: str):
        """
        This method returns the value associated with the given key.
        If the key is not in the hash map, the method returns None.
        """

        index = self._hash_function(key) % self._capacity
        for i in self._buckets[index]:
            if i.key == key:
                return i.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False.
        An empty hash map does not contain any keys.
        """
        if self._size == 0:
            return False

        index = self._hash_function(key) % self._capacity
        for i in self._buckets[index]:
            if i.key == key:
                return True

        return False

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing (no exception needs to be raised).
        """

        index = self._hash_function(key) % self._capacity
        for i in self._buckets[index]:
            if i.key == key:
                self._buckets[index].remove(key)
                self._size -= 1
                return

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a DA where each index contains a tuple of a key/value pair stored in the hash map
        - Set up a size counter to keep track of the size
        - When the counter = the number of elements in the map, stop looping
        """
        result_da = DynamicArray()

        size_counter = 0
        for i in range(self._capacity):
            if self._buckets[i].length() != 0:
                for j in self._buckets[i]:
                    result_da.append((j.key, j.value))

                size_counter += self._buckets[i].length()
                if size_counter == self._size:
                    return result_da

        return result_da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    This function will return a tuple (DA - the mode value/s, an integer - the highest frequency)

    If there is more than one value with the highest frequency,
    all values at that frequency should be included in the array being returned (the order does not matter).

    If there is only one mode, the dynamic array will only contain that value.

    Time Complexity: O(N)
    """

    map = HashMap()

    for i in range(da.length()):
        if map.contains_key(da[i]):
            freq = map.get(da[i])
            freq += 1
            map.put(da[i], freq)

        else:
            freq = 1
            map.put(da[i], freq)

    highest_freq = 1
    key_value = map.get_keys_and_values()
    mode_da = DynamicArray()

    for j in range(key_value.length()):
        if key_value[j][1] > highest_freq:
            highest_freq = key_value[j][1]
            mode_da = DynamicArray()
            mode_da.append(key_value[j][0])

        elif key_value[j][1] == highest_freq:
            mode_da.append(key_value[j][0])

    return mode_da, highest_freq


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
