import pygame

from management_and_config.configurations import *


def inventory_run():

    screen.fill(GREY)
    pygame.display.flip()

    while True:

        # return to game
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_i:
                    return "game"

                if e.key == pygame.K_k:
                    return "skill tree"
