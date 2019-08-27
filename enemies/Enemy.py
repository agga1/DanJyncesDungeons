import pygame

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

        self.speed = enemy_speed
        self.velocity = [0, 0]

        self.damage = enemy_damage
        self.knockback = enemy_knockback

    def set_velocity(self):
        from core.main import character
        for main_character in character.sprites():
            curr_character_position = main_character.get_position()
            position_difference = [curr_character_position[0] - self.rect.x,
                                   curr_character_position[1] - self.rect.y]

            self.velocity = [
                self.speed * position_difference[0] / (abs(position_difference[0]) + abs(position_difference[1])),
                self.speed * position_difference[1] / (abs(position_difference[0]) + abs(position_difference[1]))]

    def move(self):
        # following main character
        self.set_velocity()

        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def get_velocity(self):
        return self.velocity

    def get_damage(self):
        return self.damage

    def get_knockback(self):
        return self.knockback
