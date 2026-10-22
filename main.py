import numpy as np
import pygame

from collections.abc import Iterator

import src.display as display
from src.algorithms import (
    bubble_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort, SortStep,
)

# Global variables
n_elements = 10
min_value = 1
max_value = n_elements

numbers = []
rng: np.random.Generator = np.random.default_rng()

default_fps = 60
current_fps = default_fps
speed = 1.0
# MAX skips most intermediate states by processing many operations per redraw.
MAX_STEPS_PER_FRAME = 128

toggle_clock = False

sorting = False
list_sorted = False
colored = {}


def generate_starting_list(n: int, min_val: int, max_val: int) -> list[int]:
    if n > max_val - min_val + 1:
        raise ValueError("Cannot generate more unique elements than the range allows.")
    return rng.choice(
        np.arange(min_val, max_val + 1), size=n, replace=False
    ).tolist()


def verify(array: list[int]) -> Iterator[int]:
    if not array:
        return
    previous = array[0]
    yield 0
    for i in range(1, len(array)):
        if array[i] >= previous:
            yield i
        previous = array[i]


def reset():
    global numbers, colored, sorting, list_sorted, n_elements
    numbers = generate_starting_list(n_elements, min_value, max_value)
    sorting = False
    list_sorted = False
    colored = {}


def main():
    running = True
    clock = pygame.time.Clock()

    global toggle_clock, current_fps, speed, colored, sorting, list_sorted
    global numbers, n_elements, min_value, max_value

    numbers = generate_starting_list(n_elements, min_value, max_value)

    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble sort"
    sorting_algorithm_generator: Iterator[SortStep] | None = None

    verify_generator = None

    while running:
        if not toggle_clock:
            clock.tick(current_fps)

        display.draw_interface(numbers, sorting_algorithm_name, speed, toggle_clock, colored)
        steps_per_frame = MAX_STEPS_PER_FRAME if toggle_clock else 1

        if sorting:
            if sorting_algorithm_generator is None:
                raise RuntimeError("Sorting is active without an algorithm generator.")
            for _ in range(steps_per_frame):
                try:
                    step = next(sorting_algorithm_generator)
                    colored = {
                        index: display.GREEN if position == 0 else display.RED
                        for position, index in enumerate(step)
                    }
                except StopIteration:
                    sorting = False
                    verify_generator = verify(numbers)
                    list_sorted = True
                    break

        if verify_generator is not None:
            for _ in range(steps_per_frame):
                try:
                    colored[next(verify_generator)] = display.GREEN
                except StopIteration:
                    verify_generator = None
                    break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                reset()
                verify_generator = None
            elif event.key == pygame.K_SPACE and not (sorting or list_sorted):
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(numbers)
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "Insertion sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "Bubble sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algorithm_name = "Selection sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algorithm_name = "Quick sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algorithm_name = "Merge sort"
            elif event.key == pygame.K_h and not sorting:
                sorting_algorithm = heap_sort
                sorting_algorithm_name = "Heap sort"
            elif event.key == pygame.K_KP_PLUS:
                speed = min(speed * 2, 4.0)
                current_fps = default_fps * speed
            elif event.key == pygame.K_KP_MINUS:
                speed = max(speed / 2, 0.25)
                current_fps = default_fps * speed
            elif event.key == pygame.K_KP_MULTIPLY:
                toggle_clock = not toggle_clock
            elif event.key == pygame.K_UP:
                n_elements *= 2
                max_value = n_elements
                reset()
                verify_generator = None
            elif event.key == pygame.K_DOWN:
                n_elements = max(n_elements // 2, 10)
                max_value = n_elements
                reset()
                verify_generator = None

    pygame.quit()


if __name__ == "__main__":
    main()
