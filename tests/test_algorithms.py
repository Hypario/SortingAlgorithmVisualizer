import itertools
import unittest

from src.algorithms import (
    bubble_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)


class SortingAlgorithmTests(unittest.TestCase):
    algorithms = (
        bubble_sort,
        insertion_sort,
        selection_sort,
        quick_sort,
        merge_sort,
        heap_sort,
    )

    def test_algorithms_sort_edge_cases_and_duplicates(self):
        cases = [
            [],
            [1],
            [1, 2, 3, 4],
            [4, 3, 2, 1],
            [3, 1, 2, 1, 3, 2],
            [5, 5, 5, 5],
        ]

        for algorithm in self.algorithms:
            for values in cases:
                with self.subTest(algorithm=algorithm.__name__, values=values):
                    result = values.copy()
                    list(algorithm(result))
                    self.assertEqual(result, sorted(values))

    def test_quick_sort_handles_many_equal_values(self):
        values = [2] * 1_500
        list(quick_sort(values))
        self.assertEqual(values, [2] * 1_500)

    def test_quick_sort_handles_ordered_inputs(self):
        for values in (list(range(2_000)), list(range(2_000, 0, -1))):
            with self.subTest(first=values[0]):
                result = values.copy()
                list(quick_sort(result))
                self.assertEqual(result, sorted(values))

    def test_algorithms_sort_short_sequences_exhaustively(self):
        for algorithm in self.algorithms:
            for size in range(6):
                for values in itertools.product(range(3), repeat=size):
                    with self.subTest(algorithm=algorithm.__name__, values=values):
                        result = list(values)
                        list(algorithm(result))
                        self.assertEqual(result, sorted(values))


if __name__ == "__main__":
    unittest.main()
