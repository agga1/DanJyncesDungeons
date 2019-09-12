import pygame
import os

from worlds_management.World import World
from management_and_config.configurations import screen
from management_and_config.display_functions import display_stats_bar

curr_world = 0


class WorldsManager:
    def __init__(self, character, db):  # gets passed character GROUP
        self._worlds_number = 0
        self._worlds_list = []

        # entering worlds to worlds_list
        worlds = os.listdir("../worlds_management/worlds/")
        worlds.sort()   # To ensure alphabetical order

        for world in worlds:
            self._worlds_list.append(World("../worlds_management/worlds/" + world, db))

        self._worlds_number = len(self._worlds_list)

        # current world
        self._curr_world = 0

        # character group
        self._character = character

    def draw(self):
        self._worlds_list[self._curr_world].curr_room.draw_room()

        for main_character in self._character.sprites():
            display_stats_bar(main_character)

        self._character.draw(screen)

    def game_start(self):
        self._worlds_list[0].load_world()

    def next_world(self):
        self._curr_world += 1

        self._worlds_list[self._curr_world].load_world()

    @property
    def curr_world(self):
        """ current world (object) """
        return self._worlds_list[self._curr_world]

    @property
    def character(self):
        """ character sprites group """
        return self._character
