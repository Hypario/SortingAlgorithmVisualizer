from collections.abc import Iterator, MutableSequence
from dataclasses import dataclass, field
from time import perf_counter
from typing import Callable

import numpy as np
import pygame

import src.display as display
from src.algorithms import (
    SortStep,
    bubble_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)

SortAlgorithm = Callable[[MutableSequence[int]], Iterator[SortStep]]

DEFAULT_FPS = 60
MAX_FRAME_BUDGET_SECONDS = 0.005
MIN_ELEMENTS = 10
ALGORITHMS: dict[int, tuple[SortAlgorithm, str]] = {
    pygame.K_b: (bubble_sort, "Bubble sort"),
    pygame.K_i: (insertion_sort, "Insertion sort"),
    pygame.K_s: (selection_sort, "Selection sort"),
    pygame.K_q: (quick_sort, "Quick sort"),
    pygame.K_m: (merge_sort, "Merge sort"),
    pygame.K_h: (heap_sort, "Heap sort"),
}


def generate_starting_list(
    n: int, min_val: int, max_val: int, rng: np.random.Generator
) -> list[int]:
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


@dataclass
class Visualizer:
    n_elements: int = 10
    min_value: int = 1
    rng: np.random.Generator = field(default_factory=np.random.default_rng)
    numbers: list[int] = field(default_factory=list)
    speed: float = 1.0
    toggle_clock: bool = False
    sorting: bool = False
    list_sorted: bool = False
    colored: dict[int, tuple[int, int, int]] = field(default_factory=dict)
    sorting_algorithm: SortAlgorithm = bubble_sort
    sorting_algorithm_name: str = "Bubble sort"
    sorting_generator: Iterator[SortStep] | None = None
    verify_generator: Iterator[int] | None = None
    running: bool = True
    clock: pygame.time.Clock = field(default_factory=pygame.time.Clock)

    @property
    def max_value(self) -> int:
        return self.n_elements

    @property
    def current_fps(self) -> float:
        return DEFAULT_FPS * self.speed

    def reset(self) -> None:
        self.numbers = generate_starting_list(
            self.n_elements, self.min_value, self.max_value, self.rng
        )
        self.sorting = False
        self.list_sorted = False
        self.sorting_generator = None
        self.verify_generator = None
        self.colored.clear()

    def start_sorting(self) -> None:
        self.sorting = True
        self.sorting_generator = self.sorting_algorithm(self.numbers)

    def advance_sorting(self, deadline: float | None) -> None:
        while self.sorting:
            if deadline is not None and perf_counter() >= deadline:
                return
            if self.sorting_generator is None:
                raise RuntimeError("Sorting is active without an algorithm generator.")
            try:
                step = next(self.sorting_generator)
            except StopIteration:
                self.sorting = False
                self.list_sorted = True
                self.verify_generator = verify(self.numbers)
                break

            self.colored = {
                index: display.GREEN if position == 0 else display.RED
                for position, index in enumerate(step)
            }
            if deadline is None:
                return

    def advance_verification(self, deadline: float | None) -> None:
        while self.verify_generator is not None:
            if deadline is not None and perf_counter() >= deadline:
                return
            try:
                index = next(self.verify_generator)
            except StopIteration:
                self.verify_generator = None
                break
            self.colored[index] = display.GREEN
            if deadline is None:
                return

    def handle_keydown(self, key: int) -> None:
        if key == pygame.K_r:
            self.reset()
        elif key == pygame.K_SPACE and not (self.sorting or self.list_sorted):
            self.start_sorting()
        elif key in ALGORITHMS and not self.sorting:
            self.sorting_algorithm, self.sorting_algorithm_name = ALGORITHMS[key]
        elif key == pygame.K_KP_PLUS:
            self.speed = min(self.speed * 2, 4.0)
        elif key == pygame.K_KP_MINUS:
            self.speed = max(self.speed / 2, 0.25)
        elif key == pygame.K_KP_MULTIPLY:
            self.toggle_clock = not self.toggle_clock
        elif key == pygame.K_UP:
            self.n_elements *= 2
            self.reset()
        elif key == pygame.K_DOWN:
            self.n_elements = max(self.n_elements // 2, MIN_ELEMENTS)
            self.reset()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            self.handle_keydown(event.key)

    def run_frame(self) -> None:
        if not self.toggle_clock:
            self.clock.tick(self.current_fps)

        display.draw_interface(
            self.numbers,
            self.sorting_algorithm_name,
            self.speed,
            self.toggle_clock,
            self.colored,
        )

        deadline = (
            perf_counter() + MAX_FRAME_BUDGET_SECONDS
            if self.toggle_clock
            else None
        )
        if self.sorting:
            self.advance_sorting(deadline)
        if self.verify_generator is not None:
            self.advance_verification(deadline)

        for event in pygame.event.get():
            self.handle_event(event)

    def run(self) -> None:
        self.reset()
        try:
            while self.running:
                self.run_frame()
        finally:
            pygame.quit()


def main() -> None:
    Visualizer().run()


if __name__ == "__main__":
    main()
