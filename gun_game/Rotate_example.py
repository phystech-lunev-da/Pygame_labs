import math
import random
from random import choice

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
finished = False

x = 0

while not finished:
    rectangle_surface = pygame.Surface((WIDTH, HEIGHT))
    old_center = rectangle_surface.get_rect().center
    pygame.draw.rect(rectangle_surface, (255, 255, 255), pygame.Rect(WIDTH//2, HEIGHT//2, 200, 100))
    rectangle_surface = pygame.transform.rotate(rectangle_surface, x)
    rect = rectangle_surface.get_rect()
    rect.center = old_center
    screen.blit(rectangle_surface, rect)

    x += 0.5

    pygame.display.update()

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()