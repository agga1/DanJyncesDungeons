import pygame

from core import sprites_functions

start_health = 5
character_speed = 5
frame_change_time = 20 / character_speed    # inverse proportion to make it more universal


class Character(pygame.sprite.Sprite):
    def __init__(self, start_point, staying_image, movement_animation, *groups):
        super().__init__(*groups)

        self.position = start_point

        self.original_image = staying_image
        self.image = staying_image
        self.angle = 0
        self.rect = self.image.get_rect()

        self.staying_image = staying_image  # animation name: "rest"
        self.movement_animation = movement_animation  # animation name: "move"
        self.curr_animation = "rest"
        self.animation_start = 0    # time when current animation started

        self.rect.x = start_point[0]
        self.rect.y = start_point[1]

        self.max_health = start_health
        self.health = start_health
        self.money = 0

        self.speed = character_speed

        self.velocity = [0, 0]

        self.is_attacking = False

    def change_velocity(self, directions):
        self.velocity[0] += directions[0] * self.speed
        self.velocity[1] += directions[1] * self.speed

        # rotation
        if not (self.velocity[0] == 0 and self.velocity[1] == 0):
            self.angle = sprites_functions.find_angle(self.velocity)
        self.rot_center(self.angle)

    def move(self, walls, time):
        curr_position = [self.rect.x, self.rect.y]
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # checking collision with walls
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x = curr_position[0]
            self.rect.y = curr_position[1]

        # changing current animation
        if self.velocity[0] == 0 and self.velocity[1] == 0:
            self.curr_animation = "rest"
            self.animation_start = time
        else:
            if not self.curr_animation == "move":
                self.animation_start = time
                self.curr_animation = "move"

        # animation
        if self.curr_animation == "rest":
            self.original_image = self.staying_image
        elif self.curr_animation == "move":
            self.original_image = sprites_functions.animate(self.movement_animation, time, self.animation_start,
                                                            frame_change_time)
            self.rot_center(self.angle)

    def check_collisions(self, enemies):
        # checking collision with enemies, function returns money as a reward for killing enemy
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
        # damage and death
        self.health -= attacker.get_damage()
        self.check_death()

        # knockback
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
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, [self.rect.x, self.rect.y])

    def start_attack(self):
        self.is_attacking = True

    def stop_attack(self):
        self.is_attacking = False

    def get_position(self):
        return [self.rect.x, self.rect.y]

    def get_max_health(self):
        return self.max_health

    def get_health(self):
        return self.health

    def get_is_attacking(self):
        return self.is_attacking
