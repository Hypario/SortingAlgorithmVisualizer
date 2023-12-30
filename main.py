import pygame
import src.display as display
import numpy as np

# TODO : refactor this mess

# global variables
n_elements = 10
min_value = 1
max_value = n_elements

numbers = []

default_fps = 60
current_fps = default_fps
speed = 1.0

toggle_clock = False

sorting = False
list_sorted = False
colored = {}


def generate_starting_list(n: int, min_val: int, max_val: int) -> list[int]:
    if n > max_val - min_val + 1:
        raise Exception("Error: Cannot generate more unique elements than the range allows.")
    else: 
        return np.random.choice(np.arange(min_val, max_val + 1), size=n, replace=False)

def bubble_sort(array):
    for i in range(len(array) - 1):
        for j in range(len(array) - 1 - i):
            num1 = array[j]
            num2 = array[j + 1]
            if num1 > num2:
                array[j], array[j + 1] = array[j + 1], array[j]
                display.draw_list(array, {j: display.GREEN, j + 1: display.RED}, True)
                yield
    return array

def insertion_sort(array):
    for i in range(1, len(array)):
        current = array[i]
        while True:
            sort = i > 0 and array[i - 1] > current
            if not sort: break
            
            array[i] = array[i-1]
            i -= 1
            array[i] = current
            display.draw_list(array, {i - 1: display.GREEN, i: display.RED}, True)
            yield

def selection_sort(array):
    for i in range(len(array)):
        minimum = i
        for j in range(i, len(array)):
            if array[minimum] > array[j]:
                minimum = j
            display.draw_list(array, {j: display.GREEN, i: display.RED}, True)
        array[minimum], array[i] = array[i], array[minimum]
        display.draw_list(array, {minimum: display.GREEN, i: display.RED}, True)
        yield

def quick_sort(array, low: int = 0, high: int = None):
    # uses the quick sort algorithm, this one makes a lot of calls, so it's slower (as it shows step by step) but it's ok for a visualizer
    if high == None: high = len(array) - 1
    if (low < high):
        wall = low
        pivot = high
        for i in range(low, high):
            if array[i] < array[pivot]:
                array[i], array[wall] = array[wall], array[i]
                wall += 1
                display.draw_list(array, {wall: display.RED, pivot: display.GREEN, i: display.RED}, True)
                yield
        array[wall], array[pivot] = array[pivot], array[wall]
        display.draw_list(array, {wall: display.RED, pivot: display.GREEN}, True)
        yield from quick_sort(array, low, wall - 1)
        yield from quick_sort(array, wall + 1, high)


def verify(array, colored):
    previous = array[0];
    colored[0] = display.GREEN
    for i in range(0, len(array)):
        if array[i] > previous:
            colored[i] = display.GREEN
            display.draw_list(array, colored, True)
            yield
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
    
    global toggle_clock, current_fps, speed, colored, sorting, list_sorted, numbers, n_elements, min_value, max_value

    numbers = generate_starting_list(n_elements, min_value, max_value)
    
    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble sort"
    sorting_algorithm_generator = None
    
    verify_generator = None
    
    while running:
        
        if not toggle_clock:
            clock.tick(current_fps) # set FPS
        
        display.draw_interface(numbers, sorting_algorithm_name, speed, toggle_clock, colored)
        
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
                verify_generator = verify(numbers, colored)
                list_sorted = True

        if verify_generator is not None:
            try:
                next(verify_generator)
            except StopIteration:
                pass
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type != pygame.KEYDOWN:
                continue
            
            if event.key == pygame.K_r:
                numbers = generate_starting_list(n_elements, min_value, max_value)
                reset()
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
            elif event.key == pygame.K_DOWN:
                n_elements = max(n_elements // 2, 10)
                max_value = n_elements
                reset()

if __name__ == "__main__":
    main()