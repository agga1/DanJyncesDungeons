import pygame

from management_and_config.configurations import *
from management_and_config.display_functions import display_skill_tree_stats_bar


def skill_tree_run(character):

    screen.fill(PINK)
    display_skill_tree_stats_bar(character)
    pygame.display.flip()

    while True:

        # return to game
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit(1)

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_k:
                    return "game"

                if e.key == pygame.K_i:
                    return "inventory"




