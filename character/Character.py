import pygame

start_health = 5


class Character:
    def __init__(self, start_point):
        self.position_x = start_point[0]
        self.position_y = start_point[1]

        self.health = start_health
        self.money = 0

        self.velocity_x = 0
        self.velocity_y = 0

    def change_velocity(self, direction, turn, value):
        # if turn == -1, the character loses his velocity
        if direction == "up":
            self.velocity_y -= turn * value
        elif direction == "down":
            self.velocity_y += turn * value
        elif direction == "left":
            self.velocity_x -= turn * value
        elif direction == "right":
            self.velocity_x += turn * value

    def move(self):
        self.position_x += self.velocity_x
        self.position_y += self.velocity_y
