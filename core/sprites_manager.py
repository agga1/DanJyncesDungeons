""" Managing creation and addition of new sprites """

from enemies.Enemy import Enemy
from obstacles.Wall import Wall
from character.Character import Character


def create_enemy(enemy_type, enemy_start_point):
    if enemy_type == "bat":
        from resources.image_manager import get_bat_images
        bat_images = get_bat_images()

        return Enemy(enemy_start_point, bat_images)
    return None


def add_walls(walls, room_size, room_type):      # classic: walls are in the borders of room
    from resources.image_manager import get_wall_image
    wall_image = get_wall_image()

    for i in range(0, room_size[0]):
        if "top" not in room_type or (i != room_size[0]/2 and i != room_size[0]/2 - 1):
            walls.add(Wall([50 * i, 0], wall_image))

        if "bottom" not in room_type or (i != room_size[0]/2 and i != room_size[0]/2 - 1):
            walls.add(Wall([50 * i, 550], wall_image))

    for i in range(0, room_size[1] - 2):
        if "left" not in room_type or (i != (room_size[1] - 2) / 2 and i != (room_size[1] - 2) / 2 - 1):
            walls.add(Wall([0, 50 + 50 * i], wall_image))

        if "right" not in room_type or (i != (room_size[1] - 2) / 2 and i != (room_size[1] - 2) / 2 - 1):
            walls.add(Wall([550, 50 + 50 * i], wall_image))


def add_enemies(enemies_group, enemies_list):
    if enemies_list:
        for enemy in enemies_list:
            enemies_group.add(enemy)


def add_character(character, character_start_point):
    from resources.image_manager import get_character_rest_image, get_character_walk_images
    character_rest_image = get_character_rest_image()
    character_walk_images = get_character_walk_images()

    character.add(Character(character_start_point, character_rest_image, character_walk_images))
