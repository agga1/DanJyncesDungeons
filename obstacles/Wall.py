import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self,  position, image, *groups):
        super().__init__(*groups)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
