import pygame

BROWN = (150, 75, 0)


class Inventory:
    def __init__(self):
        self.active = False

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    @staticmethod
    def draw():
        from core.main import screen
        screen.fill(BROWN)

    def get_active(self):
        return self.active
