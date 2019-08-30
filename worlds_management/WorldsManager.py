import pygame
import os

from worlds_management.World import World
from core import menu_activity

curr_world = 0


class WorldsManager:
    def __init__(self):
        self.worlds_number = 0
        self.worlds_list = []

        # entering worlds
        worlds = os.listdir("../worlds_management/worlds/")
        worlds.sort()   # To ensure alphabetical order

        for world in worlds:
            self.worlds_list.append(World("../worlds_management/worlds/" + world))

        self.worlds_number = len(self.worlds_list)

        # ccsndfdsj
        self.curr_world = 0

    def game_start(self):
        self.worlds_list[0].load_world()

    def next_world(self):
        self.curr_world += 1

        self.worlds_list[self.curr_world].load_world()

    def get_curr_world(self):
        return self.worlds_list[self.curr_world]
