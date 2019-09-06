import pygame
import math

from sprites_management.sprites_functions import calculate_arctan
from management_and_config.configurations import *


class Drop(pygame.sprite.Sprite):
    def __init__(self, name, position, image, *groups):
        super().__init__(*groups)

        # core variables
        self.name = name  # now just "coin" and "exp"
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        # rect.x and rec.y must be integers so to make movement more precise we need that float
        self.exact_pos = position

        # movement towards character
        self.base_speed = drop_speed
        self.velocity = [0, 0]

    def move_towards_character(self, main_character):
        # main character is a target
        curr_character_position_center = [main_character.get_position()[0] + sprite_size[0] / 2,
                                          main_character.get_position()[1] + sprite_size[1] / 2]
        position_difference = [self.rect.x - curr_character_position_center[0],
                               self.rect.y - curr_character_position_center[1]]

        # following character just if it is closer than drop_moving_distance
        distance = math.sqrt(position_difference[0] ** 2 + position_difference[1] ** 2)
        if distance < drop_moving_distance:
            # moving faster when the character is closer
            curr_speed = drop_moving_distance * self.base_speed / distance

            # calculating angle
            angle = calculate_arctan(position_difference)

            # setting velocity
            if position_difference[0] >= 0:
                self.velocity = [-1 * curr_speed * math.cos(angle), -1 * curr_speed * math.sin(angle)]
            else:
                self.velocity = [curr_speed * math.cos(angle), curr_speed * math.sin(angle)]

            # to improve softness of movement
            self.exact_pos[0] += self.velocity[0]
            self.exact_pos[1] += self.velocity[1]

            # movement
            self.rect.x = self.exact_pos[0]
            self.rect.y = self.exact_pos[1]

    def get_name(self):
        return self.name
