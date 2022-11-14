import random

import pygame
from random import randint

FPS = 60
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

DEFAULT_CIRCLE = {'position': (0, 0), 'radius': SMALL_RADIUS, 'color': BLACK, 'velocity': (0, 0)}


def create_circle(r, x, y, vx = 0, vy = 0):
    global DEFAULT_CIRCLE
    '''
    create a dictionary that contains ball settings
    :return: ball dictionary
    '''
    ball = DEFAULT_CIRCLE.copy()
    color = random.choice(BALL_COLORS)

    ball['radius'] = r
    ball['position'] = (x, y)
    ball['color'] = color
    ball['velocity'] = (vx, vy)
    return ball

def create_particle(center_x, center_y):

    x = randint(center_x - 10, center_x + 10)
    y = randint(center_y - 10, center_y + 10)
    r = 2
    vx = (x - center_x)
    vy = (y - center_y)

    return create_circle(r, x, y, vx, vy)

def move_circle(ball):
    ball['position'] = (
        ball['position'][0] + ball['velocity'][0],
        ball['position'][1] + ball['velocity'][1]
    )

def move_particle_system(system):
    for s in system:
        move_circle(s)

def create_particle_system(x, y):
    COUNT = 30
    return [create_particle(x, y) for i in range(COUNT)]


def create_ball():
    '''
    create a dictionary that contains ball settings
    :return: ball dictionary
    '''
    r = random.choices([LARGE_RADIUS, SMALL_RADIUS], (10, 1))
    r = r[0]
    x = randint(r, SCREEN_SIZE[0] - r)
    y = randint(r, SCREEN_SIZE[1] - r)

    return create_circle(r, x, y)


def draw_circle(surface, ball):
    '''
    draw a ball that is dictionary on surface
    '''
    pygame.draw.circle(surface, ball['color'], ball['position'], ball['radius'])


def draw_particle_system(surface, system):
    for s in system:
        draw_circle(surface, s)


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

particles = None


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
    pygame.time.set_timer(pygame.USEREVENT + 0, timer_time, 1)


def recreate_timer():
    update_timer_time()
    set_ball_life_timer()


def on_new_ball_event():
    global ball, ball_count
    ball = create_ball()
    ball_count += 1
    recreate_timer()


set_ball_life_timer()

def set_particle_life_timer():
    pygame.time.set_timer(pygame.USEREVENT + 1, 500, 1)


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
                particles = create_particle_system(*ball['position'])
                set_particle_life_timer()

                if ball['radius'] == SMALL_RADIUS:
                    points_count += 10
                else:
                    points_count += 1
                click_count += 1
                on_new_ball_event()
        if event.type == pygame.USEREVENT + 0:
            on_new_ball_event()
        if event.type == pygame.USEREVENT + 1:
            particles = None



    screen.fill(BLACK)
    draw_circle(screen, ball)
    click_count_text_surface = font.render(f'Счет: {points_count}', False, WHITE)
    screen.blit(click_count_text_surface, (0, 0))
    ball_count_text_surface = font.render(f'Пропущено: {ball_count - click_count}', False, WHITE)
    screen.blit(ball_count_text_surface, (150, 0))
    if particles:
        draw_particle_system(screen, particles)
        move_particle_system(particles)
    pygame.display.update()

pygame.quit()
