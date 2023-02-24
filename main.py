import pygame
from pygame.constants import QUIT
import random


pygame.init()

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
colors = [WHITE, VIOLET, INDIGO, BLUE, GREEN, YELLOW, ORANGE, RED]


ball = pygame.Surface((20, 20))
ball.fill(WHITE)
ball_rect = ball.get_rect()
ball_speed = [1, 1]


is_working = True

while is_working:
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

    ball_rect = ball_rect.move(ball_speed)

    if ball_rect.bottom >= height or ball_rect.top <= 0:
        ball_speed[1] = -ball_speed[1]
        ball.fill(random.choice(colors))

    if ball_rect.left >= width or ball_rect.right <= 0:
        ball_speed[0] = -ball_speed[0]
        ball.fill(random.choice(colors))

    main_surface.fill(BLACK)
    main_surface.blit(ball, ball_rect)
    pygame.display.flip()
