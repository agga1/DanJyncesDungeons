import pygame

enemy_speed = 3


class Enemy:
    def __init__(self, start_point):
        self.position = start_point

        self.speed = enemy_speed

    def move(self):
        from core.main import character
        curr_character_position = character.get_position()
        position_difference = [curr_character_position[0] - self.position[0],
                               curr_character_position[1] - self.position[1]]

        self.position[0] += self.speed * position_difference[0] / (
                    abs(position_difference[0]) + abs(position_difference[1]))
        self.position[1] += self.speed * position_difference[1] / (
                    abs(position_difference[0]) + abs(position_difference[1]))
