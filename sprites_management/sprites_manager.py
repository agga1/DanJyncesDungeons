""" Managing creation and addition of new sprites """
import pygame
import random

from sprites_management.enemies.Bat import Bat
from sprites_management.enemies.Hedgehog import Hedgehog
from sprites_management.obstacles.Wall import Wall
from sprites_management.obstacles.Door import Door
from sprites_management.drop.Drop import Drop
from resources.image_manager import get_bat_images, get_hedgehog_images, get_wall_image, get_open_door_image, \
    get_door_closed_blue_image, get_door_closed_green_image, get_door_closed_grey_image, \
    get_door_closed_yellow_image, get_key_grey_image, get_key_blue_image, get_key_green_image, get_key_yellow_image, \
    get_coin_point_image, get_exp_point_image


def create_enemy(enemy_id, enemy_type, enemy_start_point, enemy_drop, enemy_start_direction):
    if enemy_type == "bat":
        bat_images = get_bat_images()

        return Bat(enemy_id, enemy_start_point, bat_images, enemy_drop)
    elif enemy_type == "hedgehog":
        hedgehog_images = get_hedgehog_images()

        return Hedgehog(enemy_id, enemy_start_point, hedgehog_images, enemy_drop, enemy_start_direction)
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


def add_doors(doors, room_size, doors_config):
    open_door_image = get_open_door_image()  # to pass a rotated image of open door to Door class

    for door_config in doors_config:
        door = door_config.split("-")  # 2 variables: side and color (or being open)
        door_image = get_open_door_image()
        door_color = None

        if door[1] == "blue":
            door_image = get_door_closed_blue_image()
            door_color = "blue"
        elif door[1] == "green":
            door_image = get_door_closed_green_image()
            door_color = "green"
        elif door[1] == "grey":
            door_image = get_door_closed_grey_image()
            door_color = "grey"
        elif door[1] == "yellow":
            door_image = get_door_closed_yellow_image()
            door_color = "yellow"

        if door[0] == "top":
            doors.add(Door("top", [50 * (room_size[0] / 2 - 1), 0], door_image, open_door_image, door_color))

        elif door[0] == "bottom":
            door_image_rotated = pygame.transform.rotate(door_image, 180)
            open_door_image_rotated = pygame.transform.rotate(open_door_image, 180)
            doors.add(Door("bottom", [50 * (room_size[0] / 2 - 1), 50 * (room_size[1] - 1)], door_image_rotated,
                           open_door_image_rotated, door_color))

        elif door[0] == "left":
            door_image_rotated = pygame.transform.rotate(door_image, 90)
            open_door_image_rotated = pygame.transform.rotate(open_door_image, 90)
            doors.add(
                Door("left", [0, 50 * (room_size[1] / 2 - 1)], door_image_rotated, open_door_image_rotated, door_color))

        elif door[0] == "right":
            door_image_rotated = pygame.transform.rotate(door_image, 270)
            open_door_image_rotated = pygame.transform.rotate(open_door_image, 270)
            doors.add(Door("right", [50 * (room_size[0] - 1), 50 * (room_size[1] / 2 - 1)], door_image_rotated,
                           open_door_image_rotated, door_color))


def add_enemies(enemies_group, enemies_list):
    if enemies_list:
        for enemy in enemies_list:
            enemies_group.add(enemy)


def add_drop(drop_group, enemy, time):
    # variables connected with fixed drop (money, exp)
    enemy_fixed_drop = enemy.fixed_drop

    # position of the enemy
    enemy_position = enemy.get_position()

    # getting number of coins
    number_of_coins = random.randint(enemy_fixed_drop["coin_range"][0], enemy_fixed_drop["coin_range"][1])

    # getting number of exp points
    number_of_exp = enemy_fixed_drop["exp"]

    # images
    coin_image = get_coin_point_image()
    exp_image = get_exp_point_image()

    # adding coins to the drop group of current room object
    for i in range(0, number_of_coins):
        coin_position = [random.randint(enemy_position[0], enemy_position[0] + 50),
                         random.randint(enemy_position[1], enemy_position[1] + 50)]

        drop_group.add(Drop("coin", coin_position, coin_image, time))

    # adding exp points to the drop group of current room object
    for i in range(0, number_of_exp):
        exp_position = [random.randint(enemy_position[0], enemy_position[0] + 50),
                        random.randint(enemy_position[1], enemy_position[1] + 50)]

        drop_group.add(Drop("exp", exp_position, exp_image, time))

    # getting other drop
    enemy_drop = enemy.drop

    if enemy_drop != "none":
        for item in enemy_drop:
            item_position = [random.randint(enemy_position[0], enemy_position[0] + 50),
                             random.randint(enemy_position[1], enemy_position[1] + 50)]

            # now just keys
            if item == "grey":
                drop_group.add(Drop("grey key", item_position, get_key_grey_image(), time))
            elif item == "blue":
                drop_group.add(Drop("blue key", item_position, get_key_blue_image(), time))
            elif item == "green":
                drop_group.add(Drop("green key", item_position, get_key_green_image(), time))
            elif item == "yellow":
                drop_group.add(Drop("yellow key", item_position, get_key_yellow_image(), time))
