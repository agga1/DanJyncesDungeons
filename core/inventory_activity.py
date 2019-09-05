import pygame

from management_and_config.configurations import *
from resources.image_manager import get_inventory_image


def inventory_run(character):

    inventory_image = get_inventory_image()
    screen.blit(inventory_image, [0, 0])
    pygame.display.flip()

    while True:

        # return to game
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit(1)

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_i:
                    return "game"

                if e.key == pygame.K_k:
                    return "skill tree"
