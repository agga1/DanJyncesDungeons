from sprites_management.sprites_functions import *
from management_and_config.configurations import *
from resources.image_manager import get_coin_image, get_heart_image


class Character(pygame.sprite.Sprite):
    def __init__(self, start_point, staying_image, movement_animation, stats, *groups):
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
        self.health = start_health  # will be passed in stats

        # money

        self.money = stats[0]

        # levels
        self.level = 1  # will be passed in stats
        self.exp = 0  # will be passed in stats
        self.to_next_level_exp = 10

        # checking if character is moving
        self.key_clicked = {"top": False, "bottom": False, "left": False, "right": False}

        # movement
        self.speed = character_speed
        self.velocity = [0, 0]

        # combat
        self.attack_damage = character_attack_damage
        self.knockback = character_knockback
        self.is_attacking = False

        self.stunned = False
        self.immune = False
        self.stop_stun_time = 0
        self.stop_immunity_time = 0

    # ----- DRAWING -----
    def draw_stats(self):
        self.health_display()
        self.money_display()
        self.level_display()

    def health_display(self):
        heart_image = get_heart_image()

        screen.blit(heart_image, health_start_point)

        pygame.draw.rect(screen, RED,
                         [health_start_point[0] + 35, health_start_point[1], health_bar_length,
                          health_bar_width], 1)

        pygame.draw.rect(screen, RED, [health_start_point[0] + 35, health_start_point[1],
                                       self.health * health_bar_length / self.max_health, health_bar_width])

    def money_display(self):
        coin_image = get_coin_image()

        money_number = money_font.render(str(self.money), True, YELLOW)
        screen.blit(coin_image, money_start_point)
        screen.blit(money_number, [money_start_point[0] + 25, money_start_point[1]])

    def level_display(self):

        level_number = level_font.render(str(self.level), True, GREEN)
        screen.blit(level_number, level_start_point)

        pygame.draw.rect(screen, GREEN,
                         [level_start_point[0] + 35, level_start_point[1] + 10, experience_bar_length,
                          experience_bar_width], 1)

        pygame.draw.rect(screen, GREEN, [level_start_point[0] + 35, level_start_point[1] + 10,
                                         self.exp * experience_bar_length / self.to_next_level_exp,
                                         experience_bar_width])

    # ----- MOVEMENT -----
    def set_velocity(self, direction):
        self.velocity[0] = direction[0] * self.speed
        self.velocity[1] = direction[1] * self.speed

        # changing angle for rotation
        if not (self.velocity[0] == 0 and self.velocity[1] == 0):
            self.angle = find_character_angle(self.velocity)

    def move(self, walls, time):
        curr_position = [self.rect.x, self.rect.y]

        # attempt to move
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # checking collision with walls
        if pygame.sprite.spritecollide(self, walls, False):
            # if collide, do not move
            self.rect.x = curr_position[0]
            self.rect.y = curr_position[1]

        # changing current animation
        if (self.velocity[0] == 0 and self.velocity[1] == 0) or self.stunned:
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
            self.original_image = animate(self.movement_animation, time, self.animation_start, frame_change_time)

        # rotation
        self.rot_center()

    def rot_center(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    # ----- COMBAT -----
    def check_collisions(self, curr_room, time):
        # checking collision with enemies
        attackers = pygame.sprite.spritecollide(self, curr_room.get_enemies(), False)
        for attacker in attackers:
            if self.is_attacking:
                attacker.hit(curr_room, self, time)
            else:
                self.hit(attacker, time)

    def hit(self, attacker, time):
        if not self.immune:
            # damage and death
            self.health -= attacker.get_damage()
            self.check_death()

            # stun
            self.stunned = True
            self.stop_stun_time = time + knockback_duration

            # immunity to attacks
            self.immune = True
            self.stop_immunity_time = time + immunity_duration

            # knockback
            attacker_velocity = attacker.get_velocity()
            attacker_speed = attacker.get_speed()
            attacker_knockback = attacker.get_knockback_multiplier()

            self.set_velocity([attacker_velocity[0] * attacker_knockback / (attacker_speed * self.speed),
                               attacker_velocity[1] * attacker_knockback / (attacker_speed * self.speed)])

            # stunning enemy for a while
            attacker.rest_after_attack(time)

    def check_death(self):
        # end of the game
        if self.health <= 0:
            exit(1)

    def start_attack(self):
        self.is_attacking = True

    def stop_attack(self):
        self.is_attacking = False

    def check_stun_and_immunity(self, time):
        if time == self.stop_stun_time:
            self.stunned = False
            self.set_velocity([0, 0])
        if time == self.stop_immunity_time:
            self.immune = False

    def add_experience(self, amount):
        self.exp += amount
        self.check_level()

    def check_level(self):
        while self.exp >= self.to_next_level_exp:
            self.level += 1
            self.exp -= self.to_next_level_exp

    def add_money(self, amount):
        self.money += amount

    # ----- GETTERS AND SETTERS -----
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

    def set_key_clicked(self, direction, click):  # setting that the movement key is (not) being pressed
        self.key_clicked[direction] = click

    def get_position(self):
        return [self.rect.x, self.rect.y]

    def get_key_clicked(self, direction):
        return self.key_clicked[direction]

    def get_attack_damage(self):
        return self.attack_damage

    def get_knockback(self):
        return self.knockback

    def get_is_attacking(self):
        return self.is_attacking

    def get_stunned(self):
        return self.stunned

    def get_money(self):
        return self.money

    def set_money(self, money):
        self.money = money
