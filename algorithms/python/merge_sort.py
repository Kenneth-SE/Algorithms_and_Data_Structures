"""
Sorting algorithm using Divide and Conquer paradigm to output a sorted array.
Recursively calls merge_sort for both halves of the array at every level.
Worst case = O(n*log(n))
Average case = O(n*log(n))
Best case = O(n*log(n))
Worst case space = O(n)
"""

def merge_sort(array):
    def merge(t_array, t_left_array, t_right_array):
        """
        Merges the two halves together, sorting the full array.
        """
        # Counters for left_array, right_array, full array respectively
        i = j = k = 0

        # While a 'half array' can be iterated over
        left_array_length = len(t_left_array)
        right_array_length = len(t_right_array)
        while i < left_array_length and j < right_array_length:

            # Compare the left elements of both halves
            if t_left_array[i] < t_right_array[j]:
                t_array[k] = t_left_array[i]
                i += 1
            else:
                t_array[k] = t_right_array[j]
                j += 1

            # One sorted item is always assigned each loop
            k += 1
        
        # Append the rest of the left side to the array
        while i < left_array_length:
            array[k] = t_left_array[i]
            i += 1
            k += 1
        
        # Append the rest of the right side to the array
        while j < right_array_length:
            array[k] = t_right_array[j]
            j += 1
            k += 1

    """
    At every level, split the array in half and sort both halves then merge.
    """
    n = len(array)
    # Array of size one is already sorted
    if n > 1:
        # Divide the array into two halves by finding the middle index
        middle_index = n // 2

        # Call merge_sort for the first half
        left_array = array[:middle_index]
        merge_sort(left_array)

        # Call merge_sort for the second half
        right_array = array[middle_index:]
        merge_sort(right_array)

        # Once both halves are sorted merge the two.
        merge(array, left_array, right_array)


if __name__ == "__main__":
    example_array = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    solution_array = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    print("Before:", example_array)
    merge_sort(example_array)
    print("After:", example_array)

    if example_array == solution_array:
        print("Sorted!")
    else:
        print("Error. Still unsorted.")