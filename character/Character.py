import pygame

start_health = 5


class Character:
    def __init__(self, start_point):
        self.position_x = start_point[0]
        self.position_y = start_point[1]

        self.health = start_health
        self.money = 0

        self.speed = 7

        self.velocity_x = 0
        self.velocity_y = 0

    def change_velocity(self, direction, value):
            if direction == "up":
                self.velocity_y -= value
            elif direction == "down":
                self.velocity_y += value
            elif direction == "left":
                self.velocity_x -= value
            elif direction == "right":
                self.velocity_x += value

    def stop(self):
        self.velocity_x = 0
        self.velocity_y = 0

    def move(self):
        self.position_x += self.velocity_x
        self.position_y += self.velocity_y

    def get_position(self):
        return [self.position_x, self.position_y]
