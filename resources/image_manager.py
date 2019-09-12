import pygame
from sprites_management.sprites_functions import connect_frames

# menu
bg_image = pygame.image.load("../resources/images_and_animations/menu/menu_bg.png")
btn_image = pygame.image.load("../resources/images_and_animations/menu/menu_button.png")
del_image = pygame.image.load("../resources/images_and_animations/menu/delete_button.png")

# stats bar
stats_bar_image = pygame.image.load("../resources/images_and_animations/stats_bar.png")

# upgrade stat
upgrade_stat_image = pygame.image.load("../resources/images_and_animations/plus.png")

# inventory
inventory_image = pygame.image.load("../resources/images_and_animations/inventory.png")

# terrain
terrain_image = pygame.image.load("../resources/images_and_animations/terrain.png")

# walls
wall_image = pygame.image.load("../resources/images_and_animations/terrain_border.png")

# doors
open_door_image = pygame.image.load("../resources/images_and_animations/doors_n_keys/door_open.png")

door_closed_blue_image = pygame.image.load("../resources/images_and_animations/doors_n_keys/door_closed_blue.png")
door_closed_green_image = pygame.image.load("../resources/images_and_animations/doors_n_keys/door_closed_green.png")
door_closed_grey_image = pygame.image.load("../resources/images_and_animations/doors_n_keys/door_closed_grey.png")
door_closed_yellow_image = pygame.image.load("../resources/images_and_animations/doors_n_keys/door_closed_yellow.png")

# keys
key_blue_image = pygame.image.load("../resources/images_and_animations/doors_n_keys/key_blue.png")
key_green_image = pygame.image.load("../resources/images_and_animations/doors_n_keys/key_green.png")
key_grey_image = pygame.image.load("../resources/images_and_animations/doors_n_keys/key_grey.png")
key_yellow_image = pygame.image.load("../resources/images_and_animations/doors_n_keys/key_yellow.png")

# character
character_rest_image = pygame.image.load(
    "../resources/images_and_animations/character/character_walk/character_walk_0.png")
character_walk_images = connect_frames("../resources/images_and_animations/character/character_walk")
character_attack_image = pygame.image.load("../resources/images_and_animations/character/character_attack.png")

# enemies
bat_images = connect_frames("../resources/images_and_animations/bat")
hedgehog_images = connect_frames("../resources/images_and_animations/hedgehog")

# health
heart_image = pygame.image.load("../resources/images_and_animations/heart.png")

# money
coin_image = pygame.image.load("../resources/images_and_animations/coin.png")

# attack ready diode
attack_ready_image = pygame.image.load("../resources/images_and_animations/attack_diode/attack_ready.png")
attack_not_ready_image = pygame.image.load("../resources/images_and_animations/attack_diode/attack_not_ready.png")

# dropped
coin_point_image = pygame.image.load("../resources/images_and_animations/coin_point.png")
exp_point_image = pygame.image.load("../resources/images_and_animations/exp_point.png")



def get_attack_ready_image():
    return attack_ready_image


def get_attack_not_ready_image():
    return attack_not_ready_image


def get_inventory_image():
    return inventory_image


def get_stats_bar_image():
    return stats_bar_image


def get_upgrade_stat_image():
    return upgrade_stat_image


def get_bg():
    return bg_image


def get_delete():
    return del_image


def get_btn():
    return btn_image


def get_terrain_image():
    return terrain_image


def get_wall_image():
    return wall_image


def get_open_door_image():
    return open_door_image


def get_door_closed_blue_image():
    return door_closed_blue_image


def get_door_closed_green_image():
    return door_closed_green_image


def get_door_closed_grey_image():
    return door_closed_grey_image


def get_door_closed_yellow_image():
    return door_closed_yellow_image


def get_key_blue_image():
    return key_blue_image


def get_key_green_image():
    return key_green_image


def get_key_grey_image():
    return key_grey_image


def get_key_yellow_image():
    return key_yellow_image


def get_character_rest_image():
    return character_rest_image


def get_character_walk_images():
    return character_walk_images


def get_character_attack_image():
    return character_attack_image


def get_bat_images():
    return bat_images


def get_hedgehog_images():
    return hedgehog_images


def get_heart_image():
    return heart_image


def get_coin_image():
    return coin_image


def get_coin_point_image():
    return coin_point_image


def get_exp_point_image():
    return exp_point_image


