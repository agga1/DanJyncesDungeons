import pygame

start_health = 5


class Character(pygame.sprite.Sprite):
    def __init__(self, start_point, image, *groups):
        super().__init__(*groups)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = start_point[0]
        self.rect.y = start_point[1]

        self.health = start_health
        self.money = 0

        self.speed = 7

        self.velocity = [0, 0]

    def change_velocity(self, directions):
        self.velocity[0] += directions[0]*self.speed
        self.velocity[1] += directions[1]*self.speed

    def stop(self):
        self.velocity = [0, 0]

    def move(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def get_position(self):
        return [self.rect.x, self.rect.y]

