# Name: Minyi Huang
# OSU Email: huanminy@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 1
# Due Date: April 23rd, 2023
# Description: Assignment 1


import random
from static_array import *


# ------------------- PROBLEM 1 - MIN_MAX -----------------------------------

def min_max(arr: StaticArray) -> (int, int):
    """
    Returns the minimum and the maximum value in an array as tuple (min, max)
    """

    minimum = maximum = arr[0]

    for i in range(arr.length() - 1):
        if minimum >= arr[i + 1]:
            minimum = arr[i + 1]

        elif maximum <= arr[i + 1]:
            maximum = arr[i + 1]

    return (minimum, maximum)


# ------------------- PROBLEM 2 - FIZZ_BUZZ ---------------------------------

def fizz_buzz(arr: StaticArray) -> StaticArray:
    """
    Returns a new StaticArray object according to the rules below:
        1. If the number is divisible by 3, the corresponding new-array element will be "fizz";
        2. If the number is divisible by 5, the corresponding new-array element will be "buzz";
        3. If the number is divisible by 3 and 5, the corresponding new-array element will be "fizzbuzz";
        4. In other cases, the element will not be modified
    """
    new_array = StaticArray(arr.length())

    for i in range(arr.length()):
        if abs(arr[i]) % 15 == 0:
            new_array.set(i, "fizzbuzz")

        elif abs(arr[i]) % 3 == 0:
            new_array.set(i, "fizz")

        elif abs(arr[i]) % 5 == 0:
            new_array.set(i, "buzz")

        else:
            new_array.set(i, arr[i])

    return new_array

# ------------------- PROBLEM 3 - REVERSE -----------------------------------

def reverse(arr: StaticArray) -> None:
    """
    Returns the reversed original array
    """
    size = arr.length() - 1

    i = 0
    mid = size // 2
    while i < mid:
        temp = arr[i]
        arr[i] = arr[size - i]
        arr[size - i] = temp
        i += 1

    return arr


# ------------------- PROBLEM 4 - ROTATE ------------------------------------

def rotate(arr: StaticArray, steps: int) -> StaticArray:
    """
    Returns a new Static Array in which the positions of the elements in the original array
    has shifted either right or left steps

    If steps is a positive integer, then the elements will be rotated to the right;
    otherwise, to the left
    """
    size = arr.length()
    new_array = StaticArray(size)

    if size > steps >= 0:
        valid_steps = steps

    if steps > size:
        valid_steps = steps - size * (steps // size)

    if -size <= steps < 0:
        valid_steps = size - abs(steps)

    if steps <= -size:
        valid_steps = size - (abs(steps) - size * (abs(steps) // size))

    for i in range(size):
        if i < valid_steps:
            new_array.set(i, arr[size - valid_steps + i])
        else:
            new_array.set(i, arr[i - valid_steps])

    return new_array


# ------------------- PROBLEM 5 - SA_RANGE ----------------------------------

def sa_range(start: int, end: int) -> StaticArray:
    """
    Returns a StaticArray that contains all the consecutive integers
    between starting integer and the ending integer (inclusive)
    """
    size = abs(end - start) + 1
    new_array = StaticArray(size)

    if start <= end:
        for i in range(size):
            new_array.set(i, start)
            start += 1

    else:
        for i in range(size):
            new_array.set(i, start)
            start -= 1

    return new_array


# ------------------- PROBLEM 6 - IS_SORTED ---------------------------------

def is_sorted(arr: StaticArray) -> int:
    """
    Returns an integer that describes whether the array is sorted:
        1   if the array is sorted in strictly ascending order
        -1  if the array is sorted in strictly descending order
        0   otherwise
    """
    size = arr.length()

    if size == 1:
        return 1

    # Check if the array is sorted strictly in ascending order or descending order
    if arr[0] == arr [1]:
        return 0

    if arr[0] < arr[1]:
        for i in range(1, size - 1):
            if arr[i] < arr[i + 1]:
                continue
            else:                       # Not in strictly ascending order
                return 0
        return 1

    else:
        for i in range(1, size - 1):
            if arr[i] > arr [i + 1]:
                continue
            else:                       # Not in strictly ascending order
                return 0
        return -1


# ------------------- PROBLEM 7 - FIND_MODE -----------------------------------

def find_mode(arr: StaticArray) -> (int, int):
    """
    Returns the mode of the array and its frequency.
    If there is more than one value that has the highest frequency, select the one
    that occurs the first in the array
    """
    size = arr.length()
    final_frequency = init_frequency = 1
    final_mode = init_mode = arr[0]

    for i in range(size - 1):
        if arr[i] == arr[i + 1] and i + 1 != size - 1:
            init_frequency += 1
            continue

        if arr[i] == arr[i + 1] and i + 1 == size - 1:
            if init_frequency <= final_frequency:
                init_frequency += 1

            else:
                init_frequency += 1
                final_frequency = init_frequency
                final_mode = arr[i]
            continue

        if arr[i] != arr[i + 1] and init_frequency <= final_frequency:
            init_frequency = 1
            continue

        if arr[i] != arr[i + 1] and init_frequency > final_frequency:
            final_frequency = init_frequency
            final_mode = arr[i]
            init_frequency = 1

    return final_mode, final_frequency

# ------------------- PROBLEM 8 - REMOVE_DUPLICATES -------------------------

def remove_duplicates(arr: StaticArray) -> StaticArray:
    """
    Returns a new StaticArray with all duplicate values in the original array removed
    """
    size = arr.length()
    new_size = 1

    for i in range(1, size):
        if arr[i - 1] == arr[i]:
            continue

        else:
            new_size += 1

    new_array = StaticArray(new_size)
    new_array.set(0, arr[0])
    new_index = 1

    for i in range(1, size):
        if arr[i - 1] == arr[i]:
            continue

        else:
            new_array.set(new_index, arr[i])
            new_index += 1

    return new_array


# ------------------- PROBLEM 9 - COUNT_SORT --------------------------------

def count_sort(arr: StaticArray) -> StaticArray:
    """
    Returns a new StaticArray with the same content in the original array in
    non-ascending order, using the count sort algorithm
    """
    max_and_min = min_max(arr)
    max = max_and_min[1]
    min = max_and_min[0]
    array_length = arr.length()
    array_range = max - min

    # 1. Create a count array with its size based on the integer range in the original array
    count_SA = StaticArray(array_range + 1)
    count = 0

    # 1.1 Set all the initial elements in the count array as 0
    for i in range(array_range + 1):
        count_SA.set(i, count)

    # 1.2 Count the integer instance in the original array
    for j in range(array_length):
        index = abs(arr[j] - max)
        count_SA[index] += 1

    # 2. Create a new array to store the sorted elements
    new_array = StaticArray(array_length)
    count_index = 0
    new_index = 0

    while new_index < array_length:
        if count_SA[count_index] == 0:    # if the integer's count is 0, then this integer is not in the original array
            count_index += 1              # move on to the next element in the Count Array
            continue

        if count_SA[count_index] != 0:    # if the integer's count > 0, then this integer is in the original array
            new_array[new_index] = max - count_index
            new_index += 1
            count_SA[count_index] -= 1

    return new_array

# ------------------- PROBLEM 10 - TRANSFORM_STRING ---------------------------

def transform_string(source: str, s1: str, s2: str) -> str:
    """
    Returns a modified string that is the same length as the source string;
    The output string will be constructed according to the following rules:
        1. If the character from source string is present in s1, it should be replaced by the character
            at the sanem index in s2;
        2. If the character is:
            a. An uppercase letter, replace it with " ", a space
            b. A lowercase letter, replace it with "#"
            c. A digit, replace it with "!"
            d. Anything else, replace it with "="
    """
    s_len = len(source)
    new_string = ""

    for i in range(s_len):
        # 1. Check if the character is in string 1
        if source[i] in s1:
            index = s1.find(source[i])
            new_string += s2[index]
            continue

        # 2. Check if the character is an uppercase letter
        if source[i].isupper():
            new_string += " "

        elif source[i].islower():
            new_string += "#"

        elif source[i].isdigit():
            new_string += "!"

        else:
            new_string += "="

    return new_string

# ------------------- BASIC TESTING -----------------------------------------

if __name__ == "__main__":

    print('\n# min_max example 1')
    arr = StaticArray(5)
    for i, value in enumerate([7, 8, 6, -5, 4]):
        arr[i] = value
    print(arr)
    result = min_max(arr)
    if result:
        print(f"Min: {result[0]: 3}, Max: {result[1]}")
    else:
        print("min_max() not yet implemented")

    print('\n# min_max example 2')
    arr = StaticArray(1)
    arr[0] = 100
    print(arr)
    result = min_max(arr)
    if result:
        print(f"Min: {result[0]}, Max: {result[1]}")
    else:
        print("min_max() not yet implemented")

    print('\n# min_max example 3')
    test_cases = (
        [3, 3, 3],
        [-10, -30, -5, 0, -10],
        [25, 50, 0, 10],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        result = min_max(arr)
        if result:
            print(f"Min: {result[0]: 3}, Max: {result[1]}")
        else:
            print("min_max() not yet implemented")

    print('\n# fizz_buzz example 1')
    source = [_ for _ in range(-5, 20, 4)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(fizz_buzz(arr))
    print(arr)

    print('\n# fizz_buzz example 2')
    source = [-25, -45, 50, 90, -105, 123]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(fizz_buzz(arr))
    print(arr)

    print('\n# reverse example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    reverse(arr)
    print(arr)
    reverse(arr)
    print(arr)

    print('\n# reverse example 2')
    source = [3, 4, 5, 6, 9]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    reverse(arr)
    print(arr)
    reverse(arr)
    print(arr)

    print('\n# rotate example 0')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    for steps in [28]:
        space = " " if steps >= 0 else ""
        print(f"{rotate(arr, steps)} {space}{steps}")
    print(arr)

    print('\n# rotate example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    for steps in [1, 2, 0, -1, -2, 28, -100, 2 ** 28, -2 ** 31]:
        space = " " if steps >= 0 else ""
        print(f"{rotate(arr, steps)} {space}{steps}")
    print(arr)

    print('\n# rotate example 2')
    array_size = 1_000_000
    source = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(f'Started rotating large array of {array_size} elements')
    rotate(arr, 3 ** 14)
    rotate(arr, -3 ** 15)
    print(f'Finished rotating large array of {array_size} elements')

    print('\n# sa_range example 1')
    cases = [
        (1, 3), (-1, 2), (0, 0), (0, -3),
        (-95, -89), (-89, -95)]
    for start, end in cases:
        print(f"Start: {start: 4}, End: {end: 4}, {sa_range(start, end)}")

    print('\n# is_sorted example 1')
    test_cases = (
        [-100, -8, 0, 2, 3, 10, 20, 100],
        ['A', 'B', 'Z', 'a', 'z'],
        ['Z', 'T', 'K', 'A', '5'],
        [1, 3, -10, 20, -30, 0],
        [-10, 0, 0, 10, 20, 30],
        [100, 90, 0, -90, -200],
        ['apple']
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        result = is_sorted(arr)
        space = "  " if result and result >= 0 else " "
        print(f"Result:{space}{result}, {arr}")

    print('\n# find_mode example 0')
    test_cases = (
        ["zebra", "sloth", "otter", "otter", "moose", "koala"],
        [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5],
        ["amy", "amy", "bob", "chris", "chris", "david", "david"]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        result = find_mode(arr)
        if result:
            print(f"{arr}\nMode: {result[0]}, Frequency: {result[1]}\n")
        else:
            print("find_mode() not yet implemented\n")

    print('\n# find_mode example 1')
    test_cases = (
        [1, 20, 30, 40, 500, 500, 500],
        [2, 2, 2, 2, 1, 1, 1, 1],
        ["zebra", "sloth", "otter", "otter", "moose", "koala"],
        ["Albania", "Belgium", "Chile", "Denmark", "Egypt", "Fiji"]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        result = find_mode(arr)
        if result:
            print(f"{arr}\nMode: {result[0]}, Frequency: {result[1]}\n")
        else:
            print("find_mode() not yet implemented\n")

    print('# remove_duplicates example 1')
    test_cases = (
        [1], [1, 2], [1, 1, 2], [1, 20, 30, 40, 500, 500, 500],
        [5, 5, 5, 4, 4, 3, 2, 1, 1], [1, 1, 1, 1, 2, 2, 2, 2]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        print(remove_duplicates(arr))
    print(arr)

    print('\n# count_sort example 1')
    test_cases = (
        [1, 2, 4, 3, 5], [5, 4, 3, 2, 1], [0, -5, -3, -4, -2, -1, 0],
        [-3, -2, -1, 0, 1, 2, 3], [1, 2, 3, 4, 3, 2, 1, 5, 5, 2, 3, 1],
        [10100, 10721, 10320, 10998], [-100320, -100450, -100999, -100001],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        before = arr if len(case) < 50 else 'Started sorting large array'
        print(f"Before: {before}")
        result = count_sort(arr)
        after = result if len(case) < 50 else 'Finished sorting large array'
        print(f"After : {after}")

    print('\n# count_sort example 2')
    array_size = 5_000_000
    min_val = random.randint(-1_000_000_000, 1_000_000_000 - 998)
    max_val = min_val + 998
    case = [random.randint(min_val, max_val) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(case):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = count_sort(arr)
    print(f'Finished sorting large array of {array_size} elements')

    print('\n# transform_string example 1\n')
    original = (
        '#     #  =====  !      =====  =====  #     #  =====',
        '#  #  #  !      !      !      !   !  ##   ##  !    ',
        '# # # #  !===   !      !      !   !  # # # #  !=== ',
        '##   ##  !      !      !      !   !  #  #  #  !    ',
        '#     #  =====  =====  =====  =====  #     #  =====',
        '                                                   ',
        '         TTTTT OOOOO      22222   66666    1       ',
        '           T   O   O          2   6       11       ',
        '           T   O   O       222    66666    1       ',
        '           T   O   O      2       6   6    1       ',
        '           T   OOOOO      22222   66666   111      ',
    )
    test_cases = ('eMKCPVkRI%~}+$GW9EOQNMI!_%{#ED}#=-~WJbFNWSQqDO-..@}',
                  'dGAqJLcNC0YFJQEB5JJKETQ0QOODKF8EYX7BGdzAACmrSL0PVKC',
                  'aLiAnVhSV9}_+QOD3YSIYPR4MCKYUF9QUV9TVvNdFuGqVU4$/%D',
                  'zmRJWfoKC5RDKVYO3PWMATC7BEIIVX9LJR7FKtDXxXLpFG7PESX',
                  'hFKGVErCS$**!<OS<_/.>NR*)<<+IR!,=%?OAiPQJILzMI_#[+}',
                  'EOQUQJLBQLDLAVQSWERAGGAOKUUKOPUWLQSKJNECCPRRXGAUABN',
                  'WGBKTQSGVHHHHHTZZZZZMQKBLC66666NNR11111OKUN2KTGYUIB',
                  'YFOWAOYLWGQHJQXZAUPZPNUCEJABRR6MYR1JASNOTF22MAAGTVA',
                  'GNLXFPEPMYGHQQGZGEPZXGJVEYE666UKNE11111WGNW2NVLCIOK',
                  'VTABNCKEFTJHXATZTYGZVLXLAB6JVGRATY1GEY1PGCO2QFPRUAP',
                  'UTCKYKGJBWMHPYGZZZZZWOKQTM66666GLA11111CPF222RUPCJT')

    for case in test_cases:
        print(transform_string(case, '612HZ', '261TO'))
