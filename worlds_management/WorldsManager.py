import pygame
import os

from worlds_management.World import World
from management_and_config.configurations import screen, character_start_point

curr_world = 0


class WorldsManager:
    def __init__(self, character):  # gets passed character GROUP
        self.worlds_number = 0
        self.worlds_list = []

        # entering worlds to worlds_list
        worlds = os.listdir("../worlds_management/worlds/")
        worlds.sort()   # To ensure alphabetical order

        for world in worlds:
            self.worlds_list.append(World("../worlds_management/worlds/" + world))

        self.worlds_number = len(self.worlds_list)

        # current world
        self.curr_world = 0

        # character group
        self.character = character

    def draw(self):
        self.worlds_list[self.curr_world].get_curr_room().draw_room()

        for main_character in self.character.sprites():
            main_character.draw_stats()

        self.character.draw(screen)

    def game_start(self):
        self.worlds_list[0].load_world()

    def next_world(self):
        self.curr_world += 1

        self.worlds_list[self.curr_world].load_world()

    def get_curr_world(self):
        return self.worlds_list[self.curr_world]

    def get_character(self):
        return self.character
