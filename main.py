import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random


pygame.init()

FPS = pygame.time.Clock()

screen = width, height = 800, 600
main_surface = pygame.display.set_mode(screen)


# colors
BLACK = 0, 0, 0
WHITE = 255, 255, 255
VIOLET = 148, 0, 211
INDIGO = 75, 0, 130
BLUE = 0, 0, 255
GREEN = 0, 255, 0
YELLOW = 255, 255, 0
ORANGE = 255, 127, 0
RED = 255, 0, 0
colors = [WHITE, VIOLET, INDIGO, BLUE, YELLOW, ORANGE]


ball = pygame.Surface((20, 20))
ball.fill(WHITE)
ball_rect = ball.get_rect()
ball_speed = 5


def create_enemy():
    enemy = pygame.Surface((20, 20))
    enemy.fill(RED)
    enemy_rect = pygame.Rect(
        width, random.randint(0, height), *enemy.get_size())
    enemy_speed = random.randint(2, 6)
    return [enemy, enemy_rect, enemy_speed]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

enemies = []


def create_bonus():
    bonus = pygame.Surface((20, 20))
    bonus.fill(GREEN)
    bonus_rect = pygame.Rect(
        random.randint(0, width), -20, *bonus.get_size())
    bonus_speed = random.randint(2, 6)
    return [bonus, bonus_rect, bonus_speed]


CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2500)

bonuses = []

font = pygame.font.SysFont('Verdana', 20)
socers = 0

is_working = True

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

    pressed_keys = pygame.key.get_pressed()

    main_surface.fill(BLACK)
    main_surface.blit(ball, ball_rect)
    main_surface.blit(font.render(str(socers), True, WHITE), (width - 30, 0))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < -10:
            enemies.pop(enemies.index(enemy))

        if ball_rect.colliderect(enemy[1]):
            enemies.pop(enemies.index(enemy))
            socers -= 1

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom > height + 10:
            bonuses.pop(bonuses.index(bonus))

        if ball_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            socers += 1
            

    if pressed_keys[K_DOWN] and not ball_rect.bottom >= height:
        ball_rect = ball_rect.move((0, ball_speed))

    if pressed_keys[K_UP] and not ball_rect.top <= 0:
        ball_rect = ball_rect.move((0, -ball_speed))

    if pressed_keys[K_LEFT] and not ball_rect.left <= 0:
        ball_rect = ball_rect.move((-ball_speed, 0))

    if pressed_keys[K_RIGHT] and not ball_rect.right >= width:
        ball_rect = ball_rect.move((ball_speed, 0))

    pygame.display.flip()
