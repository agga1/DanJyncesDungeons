import pygame

start_health = 5


class Character(pygame.sprite.Sprite):
    def __init__(self, start_point, *groups):
        super().__init__(*groups)

        self.position = start_point

        self.image = pygame.image.load("../resources/main_character.png")
        self.rect = self.image.get_rect()

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
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def get_position(self):
        return self.position

