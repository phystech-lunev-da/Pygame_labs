import random

import pygame
from pygame.draw import circle
from random import randint

FPS = 30
SCREEN_SIZE = (900, 600)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BALL_COLORS = (RED, BLUE, GREEN, YELLOW, MAGENTA, CYAN, WHITE)

SMALL_RADIUS = 20
LARGE_RADIUS = 40

DEFAULT_BALL = {'position': (0, 0), 'radius': SMALL_RADIUS, 'color': BLACK}


def create_ball():
    global DEFAULT_BALL
    '''
    create a dictionary that contains ball settings
    :return: ball dictionary
    '''
    ball = DEFAULT_BALL.copy()
    r = random.choices([LARGE_RADIUS, SMALL_RADIUS], (10, 1))
    r = r[0]
    x = randint(r, SCREEN_SIZE[0] - r)
    y = randint(r, SCREEN_SIZE[1] - r)
    color = random.choice(BALL_COLORS)

    ball['radius'] = r
    ball['position'] = (x, y)
    ball['color'] = color
    return ball


def draw_circle(surface, ball):
    '''
    draw a ball that is dictionary on surface
    '''
    circle(surface, ball['color'], ball['position'], ball['radius'])


pygame.init()
pygame.font.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.update()

clock = pygame.time.Clock()

finished = False

ball = create_ball()

click_count = 0
ball_count = 0

points_count = 0

timer_time = 0


def update_timer_time():
    '''
    Update time of timer using click_count.
    Function (2/(x+1) + 1) decrease from 3 to 1 asymptotic.
    When click count increase than frequency of appearing ball increase.
    '''
    global timer_time
    timer_time = int(300 * (3 / (click_count + 1)**0.15 + 1))

update_timer_time()


def set_ball_life_timer():
    global timer_time
    pygame.time.set_timer(pygame.USEREVENT, timer_time, 1)


def recreate_timer():
    update_timer_time()
    set_ball_life_timer()


def on_new_ball_event():
    global ball, ball_count
    ball = create_ball()
    ball_count += 1
    recreate_timer()


set_ball_life_timer()

font = pygame.font.SysFont('Comic Sans MS', 15)

while not finished:
    clock.tick(FPS)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            distance = ((ball['position'][0] - mouse_pos[0])**2 + (ball['position'][1] - mouse_pos[1])**2)**0.5
            if distance <= ball['radius']:
                if ball['radius'] == SMALL_RADIUS:
                    points_count += 10
                else:
                    points_count += 1
                click_count += 1
                on_new_ball_event()
        if event.type == pygame.USEREVENT:
            on_new_ball_event()

    screen.fill(BLACK)
    draw_circle(screen, ball)
    click_count_text_surface = font.render(f'Счет: {points_count}', False, WHITE)
    screen.blit(click_count_text_surface, (0, 0))
    ball_count_text_surface = font.render(f'Пропущено: {ball_count - click_count}', False, WHITE)
    screen.blit(ball_count_text_surface, (150, 0))
    pygame.display.update()

pygame.quit()
