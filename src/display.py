import pygame
import math

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
    
    block_width = windowSize[0] / len(array)
    ceil_width = math.ceil(block_width)
    
    block_height = windowSize[1] - TOP_PAD
    
    for i, val in enumerate(array):
        x = block_width * i
        block_height = math.floor(val / len(array) * (windowSize[1] - TOP_PAD))
        y = windowSize[1] - block_height
        
        color = color_positions[i] if i in color_positions else WHITE
        
        pygame.draw.rect(surface=screen, color=color, rect=(x, y, ceil_width, block_height))
    
    if clear_bg:
        pygame.display.update()

def draw_interface(array, algorithm_name, speed: float, bypass_clock: bool, colored = {}):
    screen.fill(BLACK)
    
    title = baseFont.render(f"{algorithm_name} - speed {'x' + str(speed) if not bypass_clock else 'MAX'} - {len(array)} elements", 1, GREEN)
    screen.blit(title, (windowSize[0] / 2 - title.get_width() / 2, 5))
    
    controls = baseFont.render("R - Reset | SPACE - Start sorting | +/- speed up / slow down", 1, WHITE)
    screen.blit(controls, (windowSize[0] / 2 - controls.get_width() / 2, 45))
    
    sorting = baseFont.render("B - Bubble sort | I - Insertion sort | S - Selection sort | Q - Quick sort", 1, WHITE)
    screen.blit(sorting, (windowSize[0] / 2 - sorting.get_width() / 2, 75))
    
    draw_list(array, colored)
    
    pygame.display.update()