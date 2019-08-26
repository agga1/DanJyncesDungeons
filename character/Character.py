import pygame

start_health = 5


class Character(pygame.sprite.Sprite):
    def __init__(self, start_point, image,  *groups):
        super().__init__(*groups)

        self.position = start_point
        self.original = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = start_point[0]
        self.rect.y = start_point[1]

        self.health = start_health
        self.money = 0

        self.speed = 7

        self.velocity = [0, 0]
        self.angle = 0

    def change_velocity(self, directions):
        self.velocity[0] += directions[0]*self.speed
        self.velocity[1] += directions[1]*self.speed
        if not (self.velocity[0] == 0 and self.velocity[1] == 0):
            self.angle = self.find_angle(self.velocity)
        self.rot_center(self.angle)

    def stop(self):
        self.velocity = [0, 0]

    def move(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def get_position(self):
        return [self.rect.x, self.rect.y]

    def rot_center(self, angle):
        """rotate an image while keeping its center"""
        self.image = pygame.transform.rotate(self.original, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, self.get_position())

    def find_angle(self, directions):
        if directions == [0, 0]:
            return 0
        if directions[0] == 0:
            if directions[1] > 0:
                return 0
            return 180
        if directions[1] == 0:
            if directions[0] > 0:
                return 90
            return 270
        if directions[0] > 0:
            if directions[1] > 0:
                return 45
            return 135
        if directions[1] > 0:
            return 315
        return 225
