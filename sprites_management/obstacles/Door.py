import pygame


class Door(pygame.sprite.Sprite):
    def __init__(self,  position, image, color, *groups):
        super().__init__(*groups)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        self._color = color     # None - open door; blue, green, grey, yellow - closed door
