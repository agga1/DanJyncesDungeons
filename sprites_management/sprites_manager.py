""" Managing creation and addition of new sprites """
import pygame
import random

from sprites_management.enemies.Bat import Bat
from sprites_management.enemies.Hedgehog import Hedgehog
from sprites_management.obstacles.Wall import Wall
from sprites_management.obstacles.Door import Door
from sprites_management.drop.Drop import Drop
from resources.image_manager import get_bat_images, get_hedgehog_images, get_wall_image, get_open_door_image, \
    get_coin_point_image, get_exp_point_image


def create_enemy(enemy_id, enemy_type, enemy_start_point, enemy_start_direction):
    if enemy_type == "bat":
        bat_images = get_bat_images()

        return Bat(enemy_id, enemy_start_point, bat_images)
    elif enemy_type == "hedgehog":
        hedgehog_images = get_hedgehog_images()

        return Hedgehog(enemy_id, enemy_start_point, hedgehog_images, enemy_start_direction)
    return None


def add_walls(walls, room_size, room_type):
    wall_image = get_wall_image()

    for i in range(0, room_size[0]):  # ifs are for not displaying walls in the places of doors
        if "top" not in room_type or (i != room_size[0] / 2 and i != room_size[0] / 2 - 1):
            walls.add(Wall([50 * i, 0], wall_image))

        if "bottom" not in room_type or (i != room_size[0] / 2 and i != room_size[0] / 2 - 1):
            walls.add(Wall([50 * i, 550], wall_image))

    for i in range(0, room_size[1] - 2):
        if "left" not in room_type or (i != (room_size[1] - 2) / 2 and i != (room_size[1] - 2) / 2 - 1):
            walls.add(Wall([0, 50 + 50 * i], wall_image))

        if "right" not in room_type or (i != (room_size[1] - 2) / 2 and i != (room_size[1] - 2) / 2 - 1):
            walls.add(Wall([550, 50 + 50 * i], wall_image))


def add_doors(doors, room_size, room_type):
    open_door_image = get_open_door_image()

    if "top" in room_type:
        doors.add(Door([50 * (room_size[0] / 2 - 1), 0], open_door_image))

    if "bottom" in room_type:
        open_door_image_rotated = pygame.transform.rotate(open_door_image, 180)
        doors.add(Door([50 * (room_size[0] / 2 - 1), 50 * (room_size[1] - 1)], open_door_image_rotated))

    if "left" in room_type:
        open_door_image_rotated = pygame.transform.rotate(open_door_image, 270)
        doors.add(Door([0, 50 * (room_size[1] / 2 - 1)], open_door_image_rotated))

    if "right" in room_type:
        open_door_image_rotated = pygame.transform.rotate(open_door_image, 90)
        doors.add(Door([50 * (room_size[0] - 1), 50 * (room_size[1] / 2 - 1)], open_door_image_rotated))


def add_enemies(enemies_group, enemies_list):
    if enemies_list:
        for enemy in enemies_list:
            enemies_group.add(enemy)


def add_drop(drop_group, enemy, time):
    enemy_drop = enemy.drop
    enemy_position = enemy.get_position()
    number_of_coins = random.randint(enemy_drop["coin_range"][0], enemy_drop["coin_range"][1])
    number_of_exp = enemy_drop["exp"]

    coin_image = get_coin_point_image()
    exp_image = get_exp_point_image()

    for i in range(0, number_of_coins):
        coin_position = [random.randint(enemy_position[0], enemy_position[0] + 50),
                         random.randint(enemy_position[1], enemy_position[1] + 50)]

        drop_group.add(Drop("coin", coin_position, coin_image, time))

    for i in range(0, number_of_exp):
        exp_position = [random.randint(enemy_position[0], enemy_position[0] + 50),
                        random.randint(enemy_position[1], enemy_position[1] + 50)]

        drop_group.add(Drop("exp", exp_position, exp_image, time))
