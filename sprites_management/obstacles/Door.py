import pygame


class Door(pygame.sprite.Sprite):
    def __init__(self, side_of_room, position, image, open_image, color, *groups):
        super().__init__(*groups)

        self.image = image
        self._open_image = open_image
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        self._side_of_room = side_of_room  # like in room config texts ("top", "bottom", "left", "right")

        self._color = color     # None - open door; blue, green, grey, yellow - closed door

        if not color:
            self._closed = False
        else:
            self._closed = True

    def open(self):
        self._closed = False
        self._color = None
        self.image = self._open_image

    def get_position_center(self):
        return self.rect.center

    @property
    def side_of_room(self):
        """ side in the room where is that door """
        return self._side_of_room

    @property
    def color(self):
        """ color of the door if closed, None otherwise """
        return self._color

    @property
    def closed(self):
        """ true if the door is still closed """
        return self._closed
