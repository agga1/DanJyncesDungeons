import pygame
import math
import os

from enemies.Enemy import Enemy
from obstacles.Wall import Wall


# ----- SPRITE GROUPS -----
def add_walls(walls):
    from resources.image_manager import get_wall_image
    wall_image = get_wall_image()

    for i in range(0, 12):
        walls.add(Wall([50 * i, 0], wall_image))
        walls.add(Wall([50 * i, 550], wall_image))
    for i in range(0, 11):
        walls.add(Wall([0, 50 + 50 * i], wall_image))
        walls.add(Wall([550, 50 + 50 * i], wall_image))


def add_enemies(enemies, enemy_start_point):
    from resources.image_manager import get_bat_images
    bat_images = get_bat_images()

    enemies.add(Enemy(enemy_start_point, bat_images))


def add_character(character, character_start_point):
    from resources.image_manager import get_character_rest_image, get_character_walk_images
    character_rest_image = get_character_rest_image()
    character_walk_images = get_character_walk_images()

    from character.Character import Character
    character.add(Character(character_start_point, character_rest_image, character_walk_images))


# ----- ANIMATIONS -----
def find_angle(directions):
    if directions == [0, 0]:
        return 0
    if directions[0] == 0:
        if directions[1] > 0:
            return 0
        return 180
    if directions[1] == 0:
        if directions[0] > 0:
            return 90
        return 270
    if directions[0] > 0:
        if directions[1] > 0:
            return 45
        return 135
    if directions[1] > 0:
        return 315
    return 225


def connect_frames(directory):
    images = []

    frames = os.listdir(directory)
    frames.sort()   # To ensure alphabetical order

    for frame in frames:
        next_frame = pygame.image.load(directory + "/" + frame)
        images.append(next_frame)

    return images


def animate(images, curr_time, start_time, speed):
    curr_frame = math.floor((curr_time - start_time)/speed) % len(images)

    return images[curr_frame]
