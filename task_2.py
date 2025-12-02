from typing import List, Tuple, Optional


def binary_search_with_upper_bound(arr: List[float], target: float) -> Tuple[int, Optional[float]]:
    left = 0
    right = len(arr)
    iterations = 0

    while left < right:
        iterations += 1
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid

    if left < len(arr):
        upper_bound = arr[left]
    else:
        upper_bound = None

    return iterations, upper_bound


if __name__ == "__main__":
    data = [1.0, 2.5, 3.3, 4.7, 5.0, 7.2]

    print(binary_search_with_upper_bound(data, 3.0))
    print(binary_search_with_upper_bound(data, 4.7))
    print(binary_search_with_upper_bound(data, 8.0))