import pygame

enemy_speed = 3


class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_point, image, *groups):
        super().__init__(*groups)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = start_point[0]
        self.rect.y = start_point[1]

        self.speed = enemy_speed

    def move(self):
        from core.main import character
        for main_character in character.sprites():
            # following main character
            curr_character_position = main_character.get_position()
            position_difference = [curr_character_position[0] - self.rect.x,
                                   curr_character_position[1] - self.rect.y]

            self.rect.x += self.speed * position_difference[0] / (
                        abs(position_difference[0]) + abs(position_difference[1]))
            self.rect.y += self.speed * position_difference[1] / (
                        abs(position_difference[0]) + abs(position_difference[1]))
