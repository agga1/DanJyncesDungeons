import pygame
from core.sprites_functions import connect_frames

# terrain and walls
terrain_image = pygame.image.load("../resources/images_and_animations/terrain.png")
wall_image = pygame.image.load("../resources/images_and_animations/terrain_border.png")

# enemies
bat_images = connect_frames("../resources/images_and_animations/bat")

# character
character_rest_image = pygame.image.load("../resources/images_and_animations/character_walk/character_walk_0.png")
character_walk_images = connect_frames("../resources/images_and_animations/character_walk")

# health
heart_image = pygame.image.load("../resources/images_and_animations/heart.png")

# money
coin_image = pygame.image.load("../resources/images_and_animations/coin.png")

# items
item_image = pygame.image.load("../resources/images_and_animations/item.png")


def get_terrain_image():
    return terrain_image


def get_wall_image():
    return wall_image


def get_bat_images():
    return bat_images


def get_character_rest_image():
    return character_rest_image


def get_character_walk_images():
    return character_walk_images


def get_heart_image():
    return heart_image


def get_coin_image():
    return coin_image


def get_item_image():
    return item_image
