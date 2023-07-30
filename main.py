import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random
from os import listdir


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

IMGS_PATH = 'goose'
"""
    For some reason, this code does not work, although everything was fine before...
    I know it's not nice to leave code in comments, but I don't care
player_imgs = [(pygame.transform.scale(pygame.image.load(
    IMGS_PATH + '/' + file), (121, 51))) for file in listdir(IMGS_PATH)]
"""

# So I fixed it like this
player_imgs = [pygame.transform.scale(pygame.image.load(r'./goose/1-1.png'), (121, 51)), 
               pygame.transform.scale(pygame.image.load(r'./goose/1-2.png'), (121, 51)),
               pygame.transform.scale(pygame.image.load(r'./goose/1-3.png'), (121, 51)),
               pygame.transform.scale(pygame.image.load(r'./goose/1-4.png'), (121, 51)),
               pygame.transform.scale(pygame.image.load(r'./goose/1-5.png'), (121, 51)),]

player = player_imgs[0]
player_rect = player.get_rect()
player_speed = 5


def create_enemy():
    enemy = pygame.transform.scale(
        pygame.image.load('enemy.png').convert_alpha(), (139, 50))
    enemy_rect = pygame.Rect(
        width + 100, random.randint(10, height - 50), *enemy.get_size())
    enemy_speed = random.randint(4, 8)
    return [enemy, enemy_rect, enemy_speed]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

enemies = []


def create_bonus():
    bonus = pygame.transform.scale(pygame.image.load(
        'bonus.png').convert_alpha(), (120, 199))
    bonus_rect = pygame.Rect(
        random.randint(0, width - 80), -100, *bonus.get_size())
    bonus_speed = random.randint(2, 6)
    return [bonus, bonus_rect, bonus_speed]


CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2500)

bonuses = []

bg = pygame.transform.scale(pygame.image.load(
    'background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

font = pygame.font.SysFont('Verdana', 20)
socers = 0

CHANGE_IMGS = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMGS, 125)

img_index = 0

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

        if event.type == CHANGE_IMGS:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]

    pressed_keys = pygame.key.get_pressed()

    # main_surface.blit(bg, (0, 0))
    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < -bg.get_width():
        bgX = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))
    main_surface.blit(player, player_rect)
    main_surface.blit(font.render(str(socers), True, BLACK), (width - 30, 0))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < -200:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            enemies.pop(enemies.index(enemy))
            if socers <= 0:
                is_working = False
            socers -= 1

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom > height + 280:
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            socers += 1

    if pressed_keys[K_DOWN] and not player_rect.bottom >= height:
        player_rect = player_rect.move((0, player_speed))

    if pressed_keys[K_UP] and not player_rect.top <= 0:
        player_rect = player_rect.move((0, -player_speed))

    if pressed_keys[K_LEFT] and not player_rect.left <= 0:
        player_rect = player_rect.move((-player_speed, 0))

    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move((player_speed, 0))

    pygame.display.flip()
