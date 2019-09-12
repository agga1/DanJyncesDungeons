import pygame
import math

from sprites_management.sprites_functions import set_velocity_in_given_direction
from management_and_config.configurations import *


class Drop(pygame.sprite.Sprite):
    def __init__(self, name, position, image, time, *groups):
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

        # delay after creation
        self._pick_up_time = time + pick_up_time

    def move_towards_character(self, character, time):
        if time >= self._pick_up_time:
            # main character is a target
            curr_character_position_center = [character.get_position()[0] + sprite_size[0] / 2,
                                              character.get_position()[1] + sprite_size[1] / 2]

            position_difference = [self.rect.x - curr_character_position_center[0],
                                   self.rect.y - curr_character_position_center[1]]

            # following character just if it is closer than drop_moving_distance
            distance = math.sqrt(position_difference[0] ** 2 + position_difference[1] ** 2)
            if distance < drop_moving_distance:
                # moving faster when the character is closer
                if distance != 0:
                    curr_speed = drop_moving_distance * self._base_speed / distance
                else:
                    curr_speed = drop_moving_distance * self._base_speed

                # setting velocity
                self._velocity = set_velocity_in_given_direction(position_difference, curr_speed)

                # to improve softness of movement
                self._exact_pos[0] += self._velocity[0]
                self._exact_pos[1] += self._velocity[1]

                # movement
                self.rect.x = self._exact_pos[0]
                self.rect.y = self._exact_pos[1]

    @property
    def name(self):
        return self._name

    @property
    def pick_up_time(self):
        return self._pick_up_time
