import pygame


class Door(pygame.sprite.Sprite):
    def __init__(self,  position, image, open_image, color, *groups):
        super().__init__(*groups)

        self.image = image
        self._open_image = open_image
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        self._color = color     # None - open door; blue, green, grey, yellow - closed door

        if not color:
            self._closed = False
        else:
            self._closed = True

    def open(self, key):
        if key.color == self._color:
            self._closed = False
        self.image = self._open_image
