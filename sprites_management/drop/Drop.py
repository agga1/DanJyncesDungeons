import pygame
import math

from sprites_management.sprites_functions import calculate_arctan
from management_and_config.configurations import *


class Drop(pygame.sprite.Sprite):
    def __init__(self, name, position, image, *groups):
        super().__init__(*groups)

        # core variables
        self._name = name  # now just "coin" and "exp"
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        # rect.x and rec.y must be integers so to make movement more precise we need that float
        self._exact_pos = position

        # movement towards character
        self._base_speed = drop_speed
        self._velocity = [0, 0]

    def move_towards_character(self, character):
        # main character is a target
        curr_character_position_center = [character.get_position()[0] + sprite_size[0] / 2,
                                          character.get_position()[1] + sprite_size[1] / 2]

        position_difference = [self.rect.x - curr_character_position_center[0],
                               self.rect.y - curr_character_position_center[1]]

        # following character just if it is closer than drop_moving_distance
        distance = math.sqrt(position_difference[0] ** 2 + position_difference[1] ** 2)
        if distance < drop_moving_distance:
            # moving faster when the character is closer
            curr_speed = drop_moving_distance * self._base_speed / distance

            # calculating angle
            angle = calculate_arctan(position_difference)

            # setting velocity
            if position_difference[0] >= 0:
                self._velocity = [-1 * curr_speed * math.cos(angle), -1 * curr_speed * math.sin(angle)]
            else:
                self._velocity = [curr_speed * math.cos(angle), curr_speed * math.sin(angle)]

            # to improve softness of movement
            self._exact_pos[0] += self._velocity[0]
            self._exact_pos[1] += self._velocity[1]

            # movement
            self.rect.x = self._exact_pos[0]
            self.rect.y = self._exact_pos[1]

    @property
    def name(self):
        return self._name
