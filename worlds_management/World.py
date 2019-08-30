import pygame
import os

from worlds_management.Room import Room
from core.sprites_manager import copy_character


def get_position(room):     # example: "room_1_12.txt", we need pos_x = 1 and pos_y = 12
    room = room.split("_")
    pos_x = int(room[1])

    room = room[2].split(".")
    pos_y = int(room[0])

    return [pos_x, pos_y]


class World:
    def __init__(self, world_path):
        self.path = world_path

        # world configurations
        self.size = [0, 0]
        self.rooms = []
        self.start_room = [0, 0]

        # making world
        world_file = open(self.path + "/world.txt", "r")

        world_size = world_file.readline().split()
        self.size[0] = int(world_size[0])   # number of elements from left to right
        self.size[1] = int(world_size[1])   # number of elements from top to bottom

        for i in range(0, self.size[1]):    # making 2d array
            self.rooms.append([None] * self.size[0])

        for i in range(0, self.size[1]):    # checking rooms in the world (now just checking which is the start one)
            curr_line = world_file.readline().split()
            for j in range(0, self.size[0]):
                if int(curr_line[j]) == 1:      # no room == 0, start room == 1, other rooms == 2
                    self.start_room = [j, i]

        world_file.close()

        # start room
        self.curr_room = self.start_room

    def load_world(self):
        rooms = os.listdir(self.path)

        for room in rooms:
            if room != "world.txt":
                position = get_position(room)

                room_file = open(self.path + "/" + room)    # reading specification of the room

                room_size = room_file.readline().split()    # size of the room [from left to right, from top to bottom]
                room_size = [int(room_size[0]), int(room_size[1])]

                room_type = room_file.readline().split()    # places with doors ("top", "bottom", "left", "right")

                enemies_number = int(room_file.readline().split()[0])   # number of enemies in the room

                enemies = []    # list of enemies in the room

                for enemy in range(0, enemies_number):
                    curr_enemy_vars = room_file.readline().split()  # reading variables connected with the enemy

                    enemy_type = curr_enemy_vars[0]     # type (name) of the enemy

                    enemy_start_point = [int(curr_enemy_vars[1]),   # point where is the enemy at the beginning
                                         int(curr_enemy_vars[2])]

                    from core.sprites_manager import create_enemy
                    enemies.append(create_enemy(enemy_type, enemy_start_point))     # creating and adding object: enemy

                room_file.close()

                self.rooms[position[0]][position[1]] = Room(room_size, room_type, enemies)   # adding room

    def change_room(self, direction):
        last_room = self.curr_room

        if direction == "top":
            if self.curr_room[1] > 0 and self.rooms[self.curr_room[0]][self.curr_room[1] - 1]:
                self.curr_room[1] -= 1
        elif direction == "bottom":
            if self.curr_room[1] < self.size[1] - 1 and self.rooms[self.curr_room[0]][self.curr_room[1] + 1]:
                self.curr_room[1] += 1
        elif direction == "left":
            if self.curr_room[0] > 0 and self.rooms[self.curr_room[0] - 1][self.curr_room[1]]:
                self.curr_room[0] -= 1
        elif direction == "right":
            if self.curr_room[0] < self.size[0] - 1 and self.rooms[self.curr_room[0] + 1][self.curr_room[1]]:
                self.curr_room[0] += 1

        # adding character to new room and erasing from the last one
        copy_character(self.rooms[last_room[0]][last_room[1]].get_character(),              # from
                       self.rooms[self.curr_room[0]][self.curr_room[1]].get_character())    # to

        # setting position of the character
        self.rooms[self.curr_room[0]][self.curr_room[1]].set_character_position(direction)

    def check_room(self):
        # checking if we are changing room
        for main_character in self.rooms[self.curr_room[0]][self.curr_room[1]].get_character():
            main_character_pos = main_character.get_position()

            if main_character_pos[1] < 0:
                self.change_room("top")
            elif main_character_pos[1] > self.rooms[self.curr_room[0]][self.curr_room[1]].get_size()[1] * 50:
                self.change_room("bottom")
            elif main_character_pos[0] < 0:
                self.change_room("left")
            elif main_character_pos[0] > self.rooms[self.curr_room[0]][self.curr_room[1]].get_size()[0] * 50:
                self.change_room("right")

    def get_curr_room(self):
        return self.rooms[self.curr_room[0]][self.curr_room[1]]
