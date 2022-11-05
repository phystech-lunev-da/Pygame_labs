import pygame
from pygame.draw import circle, rect, polygon

FPS = 30
SCREEN_SIZE = (900, 600)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


def draw_circle(surface, color, pos, radius):
    circle(surface, color, pos, radius, 0)
    circle(surface, BLACK, pos, radius, 1)


pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.update()

finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    screen.fill((255, 255, 255))
    draw_circle(screen, YELLOW, (450, 300), 100)
    draw_circle(screen, RED, (410, 275), 30)
    draw_circle(screen, RED, (490, 275), 25)
    draw_circle(screen, BLACK, (410, 275), 10)
    draw_circle(screen, BLACK, (490, 275), 10)

    rect(screen, BLACK, (410, 350, 80, 25), 0)

    points = [(440, 255), (450, 245), (380, 230), (370, 240)]
    polygon(screen, BLACK, points)

    symmetric_points = [(2 * 450 - x[0], x[1]) for x in points]
    polygon(screen, BLACK, symmetric_points)

    pygame.display.update()

pygame.quit()

