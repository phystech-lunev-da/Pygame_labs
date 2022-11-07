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

GRAVITY = 10
FRICTION_KOEF = 0.7

class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450, vx = 0, vy = 0):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = vx
        self.vy = vy
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy += GRAVITY

        self.x += self.vx
        self.y += self.vy

        if self.x - self.r < 0 or self.x + self.r > WIDTH:
            if self.x - self.r < 0:
                self.x = self.r
            elif self.x + self.r > WIDTH:
                self.x = WIDTH - self.r
            self.vx = -self.vx * FRICTION_KOEF
        if self.y + self.r > HEIGHT:
            self.y = HEIGHT - self.r
            self.vy = -self.vy


    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if type(obj) == Target:
            if (obj.x - self.x)**2 + (obj.y - self.y)**2 <= (obj.r + self.r)**2:
                return True
        return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.y = 450
        self.x = 20
        self.start_length = 50

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1

        new_ball = Ball(
            self.screen,
            int(self.x + self.start_length * math.cos(self.an)),
            int(self.y + self.start_length * math.sin(self.an))
        )
        new_ball.r += 5
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-self.y) / (event.pos[0]-self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        rectangle_surface = pygame.Surface((WIDTH, HEIGHT))
        rectangle_surface.fill((255, 255, 255))
        old_center = rectangle_surface.get_rect().center

        length = self.start_length

        pygame.draw.rect(rectangle_surface, self.color, pygame.Rect(WIDTH//2, HEIGHT//2, length * (1.1 - self.f2_power / 100), 10))
        rectangle_surface = pygame.transform.rotate(rectangle_surface, -self.an * 180 / math.pi)
        rect = rectangle_surface.get_rect()
        rect.center = (old_center[0] + self.x - WIDTH//2, old_center[1] + self.y - HEIGHT//2)
        self.screen.blit(rectangle_surface, rect)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = random.randint(600, 780)
        y = self.y = random.randint(300, 550)
        r = self.r = random.randint(2, 50)
        color = self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pass


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
#target = Target()
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    #target.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
    #     if b.hittest(target) and target.live:
    #         target.live = 0
    #         target.hit()
    #         target.new_target()
    gun.power_up()

pygame.quit()
