from math import floor


def binary_search(array, array_length, target):
    """
    Search algorithm that finds the position of a target value within a sorted array.
    Worst case = O(log(n))
    Average case = O(log(n))
    Best case = O(1)
    Worst case space = O(1)
    """
    # Both ends of the array
    left_index = 0
    right_index = array_length - 1
    
    # Ensure left index is always less than the right index
    while left_index <= right_index:
        # New middle of the half
        middle_index = floor((left_index + right_index) / 2)
        
        # Find which half of the array the target is within
        current = array[middle_index]
        if current < target:
            left_index = middle_index + 1
        elif current > target:
            right_index = middle_index - 1
        else:
            return middle_index
    return None


if __name__ == "__main__":
    def print_binary_search(target):
        target_index = binary_search(example_array, len(example_array), target)
        if target_index is not None:
            print("Target at index:", target_index)
        else:
            print("Target not found")

    example_array = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Target found at index: index
    for index in range(11):
        print_binary_search(index)

    # Target not found
    print_binary_search(-1)
    print_binary_search(11)