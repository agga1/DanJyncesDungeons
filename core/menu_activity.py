"""Main menu activity, main file running on startup"""
import pygame
from resources import image_manager
from core.configurations import *
pygame.init()

screen = pygame.display.set_mode([screen_width, screen_height])
clock = pygame.time.Clock()


def menu_run():
    game_version = 0
    while True:

        clock.tick(60)
        menu_draw()

        for e in pygame.event.get():
            # QUIT GAME
            if e.type == pygame.QUIT:
                exit(1)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    return game_version

        pygame.display.flip()


def menu_draw():
    screen.fill(WHITE)
