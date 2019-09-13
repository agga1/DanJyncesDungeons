import pygame

from management_and_config.configurations import *
from management_and_config.display_functions import display_skill_tree_stats_bar
from resources.image_manager import get_upgrade_stat_image, get_sword_skill_image, get_bought_sword_skill_image


def add_upgrade_stat_buttons():
    button_attack_damage = get_upgrade_stat_image().get_rect()
    button_attack_damage.center = [st_attack_damage_plus_start_point[0] + button_attack_damage.width / 2,
                                   st_attack_damage_plus_start_point[1] + button_attack_damage.height / 2]

    button_attack_speed = get_upgrade_stat_image().get_rect()
    button_attack_speed.center = [st_attack_speed_plus_start_point[0] + button_attack_speed.width / 2,
                                  st_attack_speed_plus_start_point[1] + button_attack_speed.height / 2]

    button_critical_attack = get_upgrade_stat_image().get_rect()
    button_critical_attack.center = [st_critical_attack_chance_plus_start_point[0] + button_critical_attack.width / 2,
                                     st_critical_attack_chance_plus_start_point[1] + button_critical_attack.height / 2]

    button_health = get_upgrade_stat_image().get_rect()
    button_health.center = [st_health_plus_start_point[0] + button_health.width / 2,
                            st_health_plus_start_point[1] + button_health.height / 2]

    button_mana = get_upgrade_stat_image().get_rect()
    button_mana.center = [st_mana_plus_start_point[0] + button_mana.width / 2,
                          st_mana_plus_start_point[1] + button_mana.height / 2]

    return button_attack_damage, button_attack_speed, button_critical_attack, button_health, button_mana


def display_skill_tree(character):  # in display_functions? (i'd rather not bc its used only here)
    # TODO get from character if skill is active and display proper image
    # sword_skill_image = get_bought_sword_skill_image() if character.sword_skill else get_sword_skill_image()
    # sword_skill_rect = get_sword_skill_image().get_rect()
    # screen.blit(sword_skill_image, [100, 100])
    pass


def skill_tree_run(character):
    upgrade_stat_buttons = add_upgrade_stat_buttons()

    while True:
        # drawing
        screen.fill(BROWN)
        display_skill_tree_stats_bar(character)
        display_skill_tree(character)

        # return to game
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit(1)

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_k:
                    return "game"

                if e.key == pygame.K_i:
                    return "inventory"

            if character.skill_points > 0 and e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if upgrade_stat_buttons[0].collidepoint(e.pos):
                    character.upgrade_stat_attack_damage()
                elif upgrade_stat_buttons[1].collidepoint(e.pos):
                    character.upgrade_stat_attack_speed()
                elif upgrade_stat_buttons[2].collidepoint(e.pos):
                    character.upgrade_stat_critical_attack_chance()
                elif upgrade_stat_buttons[3].collidepoint(e.pos):
                    character.upgrade_stat_health()
                elif upgrade_stat_buttons[4].collidepoint(e.pos):
                    character.upgrade_stat_mana()

        pygame.display.flip()
