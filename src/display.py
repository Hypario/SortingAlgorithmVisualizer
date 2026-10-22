import math

import numpy as np
import pygame

pygame.init()

# display settings
windowSize = (900, 500)
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption("Sorting Algorithms Visualizer")

# font
baseFont = pygame.font.SysFont("Arial", 24)
BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
RED = 255, 0, 0
BG_COLOR = BLACK

TOP_PAD = 150


def draw_list(array, color_positions={}, clear_bg=False):
    if clear_bg:
        clear_rect = (0, TOP_PAD, windowSize[0], windowSize[1])
        pygame.draw.rect(screen, BG_COLOR, clear_rect)

    if not array:
        return

    if len(array) > windowSize[0]:
        _draw_dense_list(array, color_positions)
        if clear_bg:
            pygame.display.update()
        return

    block_width = windowSize[0] / len(array)
    ceil_width = math.ceil(block_width)

    for i, val in enumerate(array):
        x = block_width * i
        block_height = math.floor(val / len(array) * (windowSize[1] - TOP_PAD))
        y = windowSize[1] - block_height
        color = color_positions[i] if i in color_positions else WHITE
        pygame.draw.rect(
            surface=screen,
            color=color,
            rect=(x, y, ceil_width, block_height),
        )

    if clear_bg:
        pygame.display.update()


def _draw_dense_list(array, color_positions):
    # Bars narrower than a pixel are represented by the tallest value in each column.
    values = np.asarray(array, dtype=np.int64)
    column_starts = (
        np.arange(windowSize[0], dtype=np.int64) * len(values)
        + windowSize[0]
        - 1
    ) // windowSize[0]
    column_values = np.maximum.reduceat(values, column_starts)
    heights = column_values * (windowSize[1] - TOP_PAD) // len(values)
    colors = np.full((windowSize[0], 3), WHITE, dtype=np.uint8)

    for index, color in color_positions.items():
        if 0 <= index < len(values):
            column = index * windowSize[0] // len(values)
            colors[column] = color

    pixels = pygame.surfarray.pixels3d(screen)
    try:
        for x, bar_height in enumerate(heights):
            if bar_height:
                pixels[x, windowSize[1] - bar_height:windowSize[1], :] = colors[x]
    finally:
        del pixels


def draw_interface(array, algorithm_name, speed: float, bypass_clock: bool, colored={}):
    screen.fill(BLACK)

    title = baseFont.render(
        f"{algorithm_name} - speed {'x' + str(speed) if not bypass_clock else 'MAX'} - {len(array)} elements",
        1,
        GREEN,
    )
    screen.blit(title, (windowSize[0] / 2 - title.get_width() / 2, 5))

    controls = baseFont.render(
        "R - Reset | SPACE - Start sorting | +/- speed up / slow down",
        1,
        WHITE,
    )
    screen.blit(controls, (windowSize[0] / 2 - controls.get_width() / 2, 45))

    sorting = baseFont.render("B - Bubble | I - Insertion | S - Selection", 1, WHITE)
    screen.blit(sorting, (windowSize[0] / 2 - sorting.get_width() / 2, 75))

    advanced_sorting = baseFont.render("Q - Quick | M - Merge | H - Heap", 1, WHITE)
    screen.blit(
        advanced_sorting,
        (windowSize[0] / 2 - advanced_sorting.get_width() / 2, 105),
    )

    draw_list(array, colored)
    pygame.display.update()
