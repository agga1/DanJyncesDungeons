import pygame

from management_and_config.configurations import *
from management_and_config.display_functions import display_items
from resources.image_manager import get_inventory_bg_image, get_inventory_equip_bar_image


def inventory_run(character):

    inventory_bg = get_inventory_bg_image()
    inventory_bar = get_inventory_equip_bar_image()
    screen.blit(inventory_bg, [0, 0])
    screen.blit(inventory_bar, [600, 0])
    inv_content = character.inventory
    buttons = display_items(inv_content)

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

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if buttons["sword"].collidepoint(e.pos):
                    print("clicked sword") # TODO equip sword 
                if buttons["health_potion"].collidepoint(e.pos):
                    print("clicked health") # TODO increase health, decrease potion quantity


        pygame.display.flip()
