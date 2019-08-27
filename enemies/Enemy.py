import pygame
import math

enemy_speed = 3
enemy_damage = 1
enemy_knockback = 30


class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_point, image, *groups):
        super().__init__(*groups)

        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = start_point[0]
        self.rect.y = start_point[1]
        self.exact_pos = start_point   # rect.x and rec.y must be integers so to make it more precise we need that float

        self.speed = enemy_speed
        self.velocity = [0, 0]

        self.damage = enemy_damage
        self.knockback = enemy_knockback

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

    def move(self):
        # following main character
        self.set_velocity()

        # to improve softness of movement
        self.exact_pos[0] += self.velocity[0]
        self.exact_pos[1] += self.velocity[1]

        self.rect.x = self.exact_pos[0]
        self.rect.y = self.exact_pos[1]

    def get_velocity(self):
        return self.velocity

    def get_damage(self):
        return self.damage

    def get_knockback(self):
        return self.knockback
