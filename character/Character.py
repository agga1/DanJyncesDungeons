import pygame

from core import sprites_functions
from core.configurations import *
from resources.image_manager import get_coin_image, get_heart_image

start_health = 5
character_speed = 5
frame_change_time = 20 / character_speed  # inverse proportion to make it more universal


class Character(pygame.sprite.Sprite):
    def __init__(self, start_point, staying_image, movement_animation, *groups):
        super().__init__(*groups)

        # image
        self.original_image = staying_image
        self.image = staying_image
        self.angle = 0
        self.rect = self.image.get_rect()

        # animations
        self.staying_image = staying_image  # animation name: "rest"
        self.movement_animation = movement_animation  # animation name: "move"
        self.curr_animation = "rest"
        self.animation_start = 0  # time when current animation started

        # position
        self.rect.x = start_point[0]
        self.rect.y = start_point[1]

        # health
        self.max_health = start_health
        self.health = start_health

        # levels
        self.level = 1
        self.curr_exp = 0
        self.to_next_level_exp = 10

        # movement
        self.speed = character_speed
        self.velocity = [0, 0]

        # attack
        self.is_attacking = False

    def draw_stats(self, money):
        self.health_display()
        self.money_display(money)
        self.level_display()

    def health_display(self):
        heart_image = get_heart_image()

        screen.blit(heart_image, health_start_point)

        pygame.draw.rect(screen, RED,
                         [health_start_point[0] + 35, health_start_point[1], health_bar_length,
                          health_bar_width], 1)

        pygame.draw.rect(screen, RED, [health_start_point[0] + 35, health_start_point[1],
                                       self.health * health_bar_length / self.max_health, health_bar_width])

    def money_display(self, money):
        coin_image = get_coin_image()

        money_number = money_font.render(str(money), True, YELLOW)
        screen.blit(coin_image, money_start_point)
        screen.blit(money_number, [money_start_point[0] + 25, money_start_point[1]])

    def level_display(self):

        level_number = level_font.render(str(self.level), True, GREEN)
        screen.blit(level_number, level_start_point)

        pygame.draw.rect(screen, GREEN,
                         [level_start_point[0] + 35, level_start_point[1] + 10, experience_bar_length,
                          experience_bar_width], 1)

        pygame.draw.rect(screen, GREEN, [level_start_point[0] + 35, level_start_point[1] + 10,
                                         self.curr_exp * experience_bar_length / self.to_next_level_exp,
                                         experience_bar_width])

    def change_velocity(self, directions):
        self.velocity[0] += directions[0] * self.speed
        self.velocity[1] += directions[1] * self.speed

        # changing angle for rotation
        if not (self.velocity[0] == 0 and self.velocity[1] == 0):
            self.angle = sprites_functions.find_angle(self.velocity)

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

        # rotation
        self.rot_center()

    def check_collisions(self, curr_room):
        # checking collision with enemies, function returns money as a reward for killing enemy
        attackers = pygame.sprite.spritecollide(self, curr_room.get_enemies(), False)
        for attacker in attackers:
            if self.is_attacking:
                reward = attacker.get_reward()

                curr_room.get_enemies().remove(attacker)

                exp = attacker.get_exp_for_kill()
                self.curr_exp += exp
                self.check_level()

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
        # end of the game
        if self.health <= 0:
            exit(1)

    def rot_center(self, ):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def start_attack(self):
        self.is_attacking = True

    def stop_attack(self):
        self.is_attacking = False

    def check_level(self):
        while self.curr_exp >= self.to_next_level_exp:
            self.level += 1
            self.curr_exp -= self.to_next_level_exp

    def set_position(self, new_room_direction, new_room_size):
        new_position = [0, 0]

        if new_room_direction == "top":
            new_position[0] = self.rect.x
            new_position[1] = new_room_size[1] * 50 - distance_from_door
        elif new_room_direction == "bottom":
            new_position[0] = self.rect.x
            new_position[1] = distance_from_door
        elif new_room_direction == "left":
            new_position[0] = new_room_size[0] * 50 - distance_from_door
            new_position[1] = self.rect.y
        elif new_room_direction == "right":
            new_position[0] = distance_from_door
            new_position[1] = self.rect.y

        self.rect.x = new_position[0]
        self.rect.y = new_position[1]

    def get_position(self):
        return [self.rect.x, self.rect.y]

    def get_is_attacking(self):
        return self.is_attacking
