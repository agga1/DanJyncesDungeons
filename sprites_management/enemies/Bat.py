from sprites_management.sprites_functions import *
from management_and_config.configurations import *

from sprites_management.enemies.Enemy import Enemy


class Bat(Enemy):
    def __init__(self, enemy_id, start_point, movement_animation, *groups):
        super().__init__(enemy_id, start_point, movement_animation, *groups)

        # animation
        self._frame_change_time = bat_frame_change_time

        # stats
        self._speed = bat_speed
        self._max_health = bat_health
        self._health = bat_health

        # combat
        self._damage = bat_damage
        self._knockback = bat_knockback

        # after death
        self._drop = {"coin_range": bat_money_drop_range, "exp": bat_exp_drop}

    def set_velocity(self, worlds_manager):
        for main_character in worlds_manager.character.sprites():
            # main character is a target
            curr_character_position_center = [main_character.get_position()[0] + sprite_size[0]/2,
                                              main_character.get_position()[1] + sprite_size[1]/2]
            position_difference = [self.rect.x - curr_character_position_center[0],
                                   self.rect.y - curr_character_position_center[1]]

            # setting velocity
            self._velocity = set_velocity_in_given_direction(position_difference, self._speed)

            # changing angle for rotation (animation)
            self.change_angle()
