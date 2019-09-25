import pygame

from management_and_config.configurations import *
from management_and_config.display_functions import display_items
from resources.image_manager import get_inventory_bg_image, get_shop_bar


# TODO add buying logic (refresh display after purchase, add items to shop bar)
def shop_run(character, shop_inventory=None):

    inventory_bg = get_inventory_bg_image()
    shop_bar = get_shop_bar()
    screen.blit(inventory_bg, [0, 0])
    screen.blit(shop_bar, [600, 0])
    inv_buttons = display_items(character.inventory)  # buttons: sword, health_potion
    # TODO shop_buttons = display_products(shop_inventory)
    pygame.display.flip()

    while True:

        # return to game
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit(1)

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_i:
                    return "inventory"

                if e.key == pygame.K_k:
                    return "skill tree"

                if e.key == pygame.K_e:
                    return "game"
            # ev. for key, button in buttons: if collidept -> button_action(character, key)
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for key, button in inv_buttons.items():
                    if inv_buttons[key].collidepoint(e.pos):
                        character.use(key)
                        screen.blit(inventory_bg, [0, 0])
                        inv_buttons = display_items(character.inventory)

        pygame.display.flip()
