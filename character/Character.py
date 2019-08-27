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

        self.max_health = start_health
        self.health = start_health
        self.money = 0

        self.speed = 7

        self.velocity = [0, 0]
        self.angle = 0

        self.is_attacking = False

    def change_velocity(self, directions):
        self.velocity[0] += directions[0]*self.speed
        self.velocity[1] += directions[1]*self.speed
        if not (self.velocity[0] == 0 and self.velocity[1] == 0):
            self.angle = self.find_angle(self.velocity)
        self.rot_center(self.angle)

    def move(self, walls):
        curr_position = [self.rect.x, self.rect.y]
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # checking collision with walls
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x = curr_position[0]
            self.rect.y = curr_position[1]

    def check_collisions(self, enemies):
        # checking collision with enemies
        attackers = pygame.sprite.spritecollide(self, enemies, False)
        for attacker in attackers:
            if self.is_attacking:
                reward = attacker.get_reward()
                enemies.remove(attacker)
                return reward
            else:
                self.hit(attacker)
                return 0
        return 0

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
            exit(1)

    def rot_center(self, angle):
        """rotate an image while keeping its center"""
        self.image = pygame.transform.rotate(self.original, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, [self.rect.x, self.rect.y])

    def start_attack(self):
        self.is_attacking = True

    def stop_attack(self):
        self.is_attacking = False

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

    def get_position(self):
        return [self.rect.x, self.rect.y]

    def get_max_health(self):
        return self.max_health

    def get_health(self):
        return self.health

    def get_is_attacking(self):
        return self.is_attacking
