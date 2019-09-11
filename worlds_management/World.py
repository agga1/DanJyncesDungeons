""" Manages current world, reading world's and rooms' configuration files, changing rooms, checking room changing"""
import os

from management_and_config.object_save import *
from worlds_management.Room import Room
from sprites_management.sprites_manager import create_enemy
from management_and_config.configurations import *


def extract_room_position(room):  # example: "room_1_12.txt", we need pos_x = 1 and pos_y = 12
    room = room.split("_")
    pos_x = int(room[1])

    room = room[2].split(".")
    pos_y = int(room[0])

    return [pos_x, pos_y]


class World:
    def __init__(self, world_path, db):
        self._path = world_path

        # world configurations
        self._size = [0, 0]
        self._rooms = []
        self._start_room_pos = [0, 0]

        # reading world configurations from a world file
        world_file = open(self._path + "/world.txt", "r")

        world_size = world_file.readline().split()
        self._size[0] = int(world_size[0])  # number of elements from left to right
        self._size[1] = int(world_size[1])  # number of elements from top to bottom

        for i in range(0, self._size[1]):  # making 2d array
            self._rooms.append([None] * self._size[0])

        for i in range(0, self._size[1]):  # checking rooms in the world (now just checking which is the start one)
            curr_line = world_file.readline().split()
            for j in range(0, self._size[0]):
                if int(curr_line[j]) == 1:  # no room == 0, start room == 1, other rooms == 2
                    self._start_room_pos = [j, i]
        world_file.close()

        # active_enemies (array read from db w/ values enemy_id: 0/1 (0- enemy dead),
        self._db = db
        # active_enemies (array read from db w/ values enemy_id: 0/1 (0- enemy dead) = load_active_enemies(db)
        self._active_enemies = load_active_enemies(db)

        # start room
        self._curr_room_pos = load_curr_room(db)  # position of the room in world map
        if self._curr_room_pos is None:  # when new game opens, curr_room in db is not initialized!
            self._curr_room_pos = self._start_room_pos

        # current room object
        self._curr_room = None

    def load_world(self):  # called when starting game or changing world
        rooms = os.listdir(self._path)
        enemy_id = 0  # to give every enemy unique id

        # reading rooms' configuration files
        for room in rooms:
            if room != "world.txt":
                position = extract_room_position(room)

                room_file = open(self._path + "/" + room)  # reading specification of the room

                room_size = room_file.readline().split()  # size of the room [from left to right, from top to bottom]
                room_size = [int(room_size[0]), int(room_size[1])]

                room_type = room_file.readline().split()  # places with doors ("top", "bottom", "left", "right")

                enemies_number = int(room_file.readline().split()[0])  # number of enemies in the room

                enemies = []  # list of enemies in the room

                for enemy in range(0, enemies_number):
                    if len(self._active_enemies) > enemy_id and not self._active_enemies[enemy_id]:
                        enemy_id += 1
                        continue

                    # the first time game opens, active_enemies is empty. default is 1 - enemy active
                    if len(self._active_enemies) <= enemy_id:
                        self._active_enemies.append(1)

                    curr_enemy_vars = room_file.readline().split()  # reading variables connected with the enemy

                    enemy_type = curr_enemy_vars[0]  # type (name) of the enemy

                    enemy_start_point = [int(curr_enemy_vars[1]),  # point where is the enemy at the beginning
                                         int(curr_enemy_vars[2])]

                    enemy_start_direction = ""
                    if len(curr_enemy_vars) >= 4:
                        if curr_enemy_vars[3] == "up" or curr_enemy_vars[3] == "down" or curr_enemy_vars[3] == "left"\
                                or curr_enemy_vars[3] == "right":
                            enemy_start_direction = curr_enemy_vars[3]

                    enemies.append(create_enemy(enemy_id, enemy_type, enemy_start_point,
                                                enemy_start_direction))  # creating and adding object

                    enemy_id += 1

                room_file.close()

                self._rooms[position[0]][position[1]] = Room(room_size, room_type, enemies)  # adding room

        # start room
        self._curr_room = self._rooms[self._curr_room_pos[0]][self._curr_room_pos[1]]

    def check_room(self, main_character):
        # checking if we are changing room
        main_character_pos = main_character.get_position()

        if main_character_pos[1] < 0:
            self.change_room_and_save("top", main_character)
        elif main_character_pos[1] > self._curr_room.size[1] * 50 - sprite_size[1]:
            self.change_room_and_save("bottom", main_character)
        elif main_character_pos[0] < 0:
            self.change_room_and_save("left", main_character)
        elif main_character_pos[0] > self._curr_room.size[0] * 50 - sprite_size[0]:
            self.change_room_and_save("right", main_character)

    def change_room_and_save(self, direction, main_character):
        # TODO: maybe save only in checkpoints? if killed -> reload last checkpoint
        # save game
        self._active_enemies = self.curr_room.update_active_enemies(self._active_enemies)
        save_active_enemies(self._active_enemies, self._db)
        save_character(main_character, self._db)
        save_curr_room(self._curr_room_pos, self._db)

        # changing curr_room_pos variable
        if direction == "top":
            if self._curr_room_pos[1] > 0 and self._rooms[self._curr_room_pos[0]][self._curr_room_pos[1] - 1]:
                self._curr_room_pos[1] -= 1

        elif direction == "bottom":
            if self._curr_room_pos[1] < self._size[1] - 1 and \
                    self._rooms[self._curr_room_pos[0]][self._curr_room_pos[1] + 1]:
                self._curr_room_pos[1] += 1

        elif direction == "left":
            if self._curr_room_pos[0] > 0 and self._rooms[self._curr_room_pos[0] - 1][self._curr_room_pos[1]]:
                self._curr_room_pos[0] -= 1

        elif direction == "right":
            if self._curr_room_pos[0] < self._size[0] - 1 and \
                    self._rooms[self._curr_room_pos[0] + 1][self._curr_room_pos[1]]:
                self._curr_room_pos[0] += 1

        # changing current room variable
        self._curr_room = self._rooms[self._curr_room_pos[0]][self._curr_room_pos[1]]

        # setting position of the character
        main_character.set_position(direction, self._curr_room.size)

    @property
    def curr_room(self):
        """ current room (object) """
        return self._curr_room
