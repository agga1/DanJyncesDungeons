import pygame
from core import sprites_functions
start_health = 5


class Character(pygame.sprite.Sprite):
    def __init__(self, start_point, image,  *groups):
        super().__init__(*groups)

        self.position = start_point

        self.original_image = image
        self.image = image
        self.angle = 0
        self.rect = self.image.get_rect()

        self.rect.x = start_point[0]
        self.rect.y = start_point[1]

        self.max_health = start_health
        self.health = start_health
        self.money = 0

        self.speed = 7

        self.velocity = [0, 0]

    def change_velocity(self, directions):
        self.velocity[0] += directions[0]*self.speed
        self.velocity[1] += directions[1]*self.speed
        if not (self.velocity[0] == 0 and self.velocity[1] == 0):
            self.angle = sprites_functions.find_angle(self.velocity)
        self.rot_center(self.angle)

    def move(self, walls, enemies):
        curr_position = [self.rect.x, self.rect.y]
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # checking collision with walls
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x = curr_position[0]
            self.rect.y = curr_position[1]

        # checking collision with enemies
        attackers = pygame.sprite.spritecollide(self, enemies, False)
        for attacker in attackers:
            self.hit(attacker)

    def hit(self, attacker):
        self.health -= attacker.get_damage()
        self.check_death()

        # KNOCKBACK
        attacker_velocity = attacker.get_velocity()
        attacker_knockback = attacker.get_knockback()

        self.rect.x += attacker_velocity[0] * attacker_knockback
        self.rect.y += attacker_velocity[1] * attacker_knockback

    def check_death(self):
        if self.health <= 0:
            from core.main import character
            character.empty()

    def rot_center(self, angle):
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, [self.rect.x, self.rect.y])

    def get_position(self):
        return [self.rect.x, self.rect.y]

    def get_max_health(self):
        return self.max_health

    def get_health(self):
        return self.health
