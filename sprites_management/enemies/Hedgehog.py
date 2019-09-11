from sprites_management.sprites_functions import *
from management_and_config.configurations import *

from sprites_management.enemies.Enemy import Enemy


class Hedgehog(Enemy):
    def __init__(self, enemy_id, start_point, movement_animation, direction, *groups):
        super().__init__(enemy_id, start_point, movement_animation, *groups)

        # animation
        self._frame_change_time = hedgehog_frame_change_time

        # movement
        self._speed = hedgehog_speed
        self._curr_direction = direction

        # health
        self._max_health = hedgehog_health
        self._health = hedgehog_health

        # combat
        self._damage = hedgehog_damage
        self._knockback = hedgehog_knockback

        # after death
        self._drop = {"coin_range": hedgehog_money_drop_range, "exp": hedgehog_exp_drop}

    def set_velocity(self, worlds_manager):
        # wandering up and down or left and right
        if self._curr_direction == "up":
            if self.rect.y > sprite_size[1] + self._speed:  # +-self._speed to avoid bugs
                self._velocity = [0, -self._speed]
            else:
                self._curr_direction = "down"

        elif self._curr_direction == "down":
            if self.rect.y < worlds_manager.curr_world.curr_room.size[1] * sprite_size[1] - 2 * sprite_size[1]\
                    - self._speed:
                self._velocity = [0, self._speed]
            else:
                self._curr_direction = "up"

        elif self._curr_direction == "left":
            if self.rect.x > sprite_size[0] + self._speed:
                self._velocity = [-self._speed, 0]
            else:
                self._curr_direction = "right"

        elif self._curr_direction == "right":
            if self.rect.x < worlds_manager.curr_world.curr_room.size[0] * sprite_size[0] - 2 * sprite_size[0]\
                    - self._speed:
                self._velocity = [self._speed, 0]
            else:
                self._curr_direction = "left"

        # changing angle for rotation (animation)
        self.change_angle()
