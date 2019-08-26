import pygame

start_health = 5


class Character:
    def __init__(self, start_point):
        self.position_x = start_point[0]
        self.position_y = start_point[1]

        self.health = start_health
        self.money = 0

        self.speed = 7

        self.velocity = [0, 0]

    def change_velocity(self, directions):
            self.velocity[0] += directions[0]*self.speed
            self.velocity[1] += directions[1]*self.speed

    def stop(self):
        self.velocity = [0, 0]

    def move(self):
        self.position_x += self.velocity[0]
        self.position_y += self.velocity[1]
