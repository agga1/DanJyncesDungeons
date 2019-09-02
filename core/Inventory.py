import pygame

from management_and_config.configurations import *


class Inventory:
    def __init__(self):
        self.active = False

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    @staticmethod
    def draw():
        screen.fill(BROWN)

    def get_active(self):
        return self.active
