import pygame
import math

from core import sprites_functions

enemy_speed = 3
enemy_damage = 1
enemy_knockback = 30
enemy_reward = 10
enemy_frame_change_time = 5


class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_point, movement_animation, *groups):
        super().__init__(*groups)

        self.original_image = movement_animation[0]
        self.image = movement_animation[0]
        self.angle = 0
        self.rect = self.image.get_rect()

        self.animation_start = 0  # time when current animation started
        self.movement_animation = movement_animation

        self.rect.x = start_point[0]
        self.rect.y = start_point[1]

        # rect.x and rec.y must be integers so to make movement more precise we need that float
        self.exact_pos = start_point

        self.speed = enemy_speed
        self.velocity = [0, 0]

        self.damage = enemy_damage
        self.knockback = enemy_knockback

        self.reward = enemy_reward

    def set_velocity(self):
        from core.main import character
        for main_character in character.sprites():
            curr_character_position = main_character.get_position()
            position_difference = [self.rect.x - curr_character_position[0], self.rect.y - curr_character_position[1]]

            # calculating angle
            if position_difference[0] != 0:
                angle = math.atan(position_difference[1]/position_difference[0])
            elif position_difference[1] > 0:
                angle = math.pi/2
            else:
                angle = math.pi * 3/2

            # setting velocity
            if position_difference[0] >= 0:
                self.velocity = [-1 * self.speed * math.cos(angle), -1 * self.speed * math.sin(angle)]
            else:
                self.velocity = [self.speed * math.cos(angle), self.speed * math.sin(angle)]

            # rotation
            if not (self.velocity[0] == 0 and self.velocity[1] == 0):
                if self.velocity[0] != 0:
                    self.angle = math.atan(self.velocity[1]/self.velocity[0])
                elif self.velocity[1] > 0:
                    self.angle = math.pi/2
                else:
                    self.angle = math.pi * 3/2

                if self.velocity[0] < 0:
                    self.angle = math.degrees(-1 * self.angle + math.pi/2)
                else:
                    self.angle = math.degrees(-1 * self.angle - math.pi/2)

            self.rot_center(self.angle)

    def move(self, time):
        # following main character
        self.set_velocity()

        # to improve softness of movement
        self.exact_pos[0] += self.velocity[0]
        self.exact_pos[1] += self.velocity[1]

        self.rect.x = self.exact_pos[0]
        self.rect.y = self.exact_pos[1]

        # animation
        self.original_image = sprites_functions.animate(self.movement_animation, time, self.animation_start,
                                                        enemy_frame_change_time)
        self.rot_center(self.angle)

    def rot_center(self, angle):
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_velocity(self):
        return self.velocity

    def get_damage(self):
        return self.damage

    def get_knockback(self):
        return self.knockback

    def get_reward(self):
        return self.reward
