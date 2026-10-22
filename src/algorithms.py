from collections.abc import Iterator, MutableSequence


# Each yielded tuple contains the bar indices involved in one visualizer step.
SortStep = tuple[int, ...]


def bubble_sort(array: MutableSequence[int]) -> Iterator[SortStep]:
    """Sort in place by swapping adjacent out-of-order values."""
    for i in range(len(array) - 1):
        # After each pass, the largest remaining value is in its final position.
        for j in range(len(array) - 1 - i):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                yield j, j + 1


def insertion_sort(array: MutableSequence[int]) -> Iterator[SortStep]:
    """Build a sorted prefix by inserting each next value into its correct place."""
    for i in range(1, len(array)):
        current = array[i]
        # Shift larger values right to make room for the value being inserted.
        while i > 0 and array[i - 1] > current:
            array[i] = array[i - 1]
            i -= 1
            array[i] = current
            yield i, i + 1


def selection_sort(array: MutableSequence[int]) -> Iterator[SortStep]:
    """Repeatedly find the smallest value in the unsorted suffix and move it left."""
    for i in range(len(array)):
        minimum = i
        for j in range(i + 1, len(array)):
            if array[j] < array[minimum]:
                minimum = j
        if minimum != i:
            array[minimum], array[i] = array[i], array[minimum]
            yield minimum, i


def _median_of_three_index(array: MutableSequence[int], low: int, high: int) -> int:
    """Choose the median of the first, middle, and last values as the pivot."""
    middle = (low + high) // 2
    return sorted((low, middle, high), key=array.__getitem__)[1]


def quick_sort(
    array: MutableSequence[int], low: int = 0, high: int | None = None
) -> Iterator[SortStep]:
    """Sort in place using median-of-three quick sort and a three-way partition."""
    if high is None:
        high = len(array) - 1
    if low >= high:
        return

    pivot = array[_median_of_three_index(array, low, high)]
    # Partition into values below, equal to, and above the pivot.
    less = low
    current = low
    greater = high

    while current <= greater:
        if array[current] < pivot:
            if current != less:
                array[less], array[current] = array[current], array[less]
            yield less, current
            less += 1
            current += 1
        elif array[current] > pivot:
            if current != greater:
                array[current], array[greater] = array[greater], array[current]
            yield current, greater
            greater -= 1
        else:
            yield current,
            current += 1

    # The equal-to-pivot range is already sorted; recurse on the outer ranges.
    yield from quick_sort(array, low, less - 1)
    yield from quick_sort(array, greater + 1, high)


def merge_sort(
    array: MutableSequence[int], low: int = 0, high: int | None = None
) -> Iterator[SortStep]:
    """Sort in place by recursively sorting halves and merging them in order."""
    if high is None:
        high = len(array) - 1
    if low >= high:
        return

    middle = (low + high) // 2
    yield from merge_sort(array, low, middle)
    yield from merge_sort(array, middle + 1, high)

    # Copy each sorted half so values can be safely merged back into the array.
    left = array[low : middle + 1]
    right = array[middle + 1 : high + 1]
    left_index = 0
    right_index = 0
    write_index = low

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            array[write_index] = left[left_index]
            left_index += 1
        else:
            array[write_index] = right[right_index]
            right_index += 1
        yield write_index,
        write_index += 1

    while left_index < len(left):
        array[write_index] = left[left_index]
        left_index += 1
        yield write_index,
        write_index += 1

    while right_index < len(right):
        array[write_index] = right[right_index]
        right_index += 1
        yield write_index,
        write_index += 1


def heap_sort(array: MutableSequence[int]) -> Iterator[SortStep]:
    """Sort in place by building a max heap, then moving its maximum to the end."""
    def sift_down(root: int, end: int) -> Iterator[SortStep]:
        # Restore the max-heap property by moving the root toward its larger child.
        while (child := 2 * root + 1) < end:
            if child + 1 < end and array[child] < array[child + 1]:
                child += 1
            if array[root] >= array[child]:
                return
            array[root], array[child] = array[child], array[root]
            yield root, child
            root = child

    size = len(array)
    # Turn the array into a max heap, starting at the last parent node.
    for root in range(size // 2 - 1, -1, -1):
        yield from sift_down(root, size)

    # Move the heap maximum to the sorted suffix and rebuild the smaller heap.
    for end in range(size - 1, 0, -1):
        array[0], array[end] = array[end], array[0]
        yield 0, end
        yield from sift_down(0, end)
