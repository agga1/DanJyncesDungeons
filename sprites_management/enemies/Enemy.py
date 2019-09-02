from sprites_management.sprites_functions import *
from management_and_config.configurations import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_point, movement_animation, *groups):
        super().__init__(*groups)

        # images
        self.original_image = movement_animation[0]
        self.image = movement_animation[0]
        self.angle = 0
        self.rect = self.image.get_rect()

        # animation
        self.animation_start = 0  # time when current animation started
        self.movement_animation = movement_animation

        # position
        self.rect.x = start_point[0]
        self.rect.y = start_point[1]

        # rect.x and rec.y must be integers so to make movement more precise we need that float
        self.exact_pos = start_point

        # movement
        self.speed = enemy_speed
        self.velocity = [0, 0]

        # health
        self.max_health = enemy_health
        self.health = enemy_health  # it will be changed after hit

        # combat
        self.damage = enemy_damage
        self.knockback_multiplier = enemy_knockback_multiplier

        self.stunned = False
        self.immune = False
        self.stop_stun_time = 0
        self.stop_immunity_time = 0

        # after being killed
        self.reward = enemy_reward
        self.exp_for_kill = enemy_exp_for_kill

    # ----- MOVEMENT -----
    def set_velocity_to_follow(self, main_character):
        # main character is a target
        curr_character_position = main_character.get_position()
        position_difference = [self.rect.x - curr_character_position[0], self.rect.y - curr_character_position[1]]

        # calculating angle
        angle = calculate_arctan(position_difference)

        # setting velocity
        if position_difference[0] >= 0:
            self.velocity = [-1 * self.speed * math.cos(angle), -1 * self.speed * math.sin(angle)]
        else:
            self.velocity = [self.speed * math.cos(angle), self.speed * math.sin(angle)]

        # changing angle for rotation (it is for animation)
        if not (self.velocity[0] == 0 and self.velocity[1] == 0):
            self.angle = calculate_arctan(self.velocity)

            if self.velocity[0] < 0:
                self.angle = math.degrees(-1 * self.angle + math.pi / 2)
            else:
                self.angle = math.degrees(-1 * self.angle - math.pi / 2)

    def move(self, character_group, time):
        # checking if can move and be hit
        self.check_stun_and_immunity(time)

        # following main character if not colliding with him
        for main_character in character_group:
            # to not change velocity during stun
            if not self.stunned:
                self.set_velocity_to_follow(main_character)

            colliding_with_character = pygame.sprite.spritecollide(self, character_group, False)

            if self.stunned or not colliding_with_character:
                # to improve softness of movement
                self.exact_pos[0] += self.velocity[0]
                self.exact_pos[1] += self.velocity[1]

                self.rect.x = self.exact_pos[0]
                self.rect.y = self.exact_pos[1]

        # animation
        self.original_image = animate(self.movement_animation, time, self.animation_start, enemy_frame_change_time)

        # rotation
        self.rot_center()

    def rot_center(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    # ----- COMBAT -----
    def hit(self, curr_room, main_character, time):
        if not self.immune:
            self.health -= main_character.get_attack_damage()

            self.check_death(curr_room, main_character)

            self.knockback(main_character, time)

    def check_death(self, curr_room, main_character):
        if self.health <= 0:
            main_character.add_money(self.reward)
            main_character.add_experience(self.exp_for_kill)

            curr_room.remove_enemy(self)

    def knockback(self, main_character, time):
        # setting variables
        self.stop_stun_time = time + knockback_duration
        self.stop_immunity_time = time + immunity_duration
        self.immune = True
        self.stunned = True

        # choosing direction to make the biggest distance between enemy and character
        character_position = main_character.get_position()
        knockback_direction = [character_position[0] - self.rect.x, character_position[1] - self.rect.y]
        knockback = main_character.get_knockback()

        # calculating angle
        angle = calculate_arctan(knockback_direction)

        # setting velocity
        if knockback_direction[0] >= 0:
            self.velocity = [-1 * self.speed * math.cos(angle), -1 * self.speed * math.sin(angle)]
        else:
            self.velocity = [self.speed * math.cos(angle), self.speed * math.sin(angle)]

        # multiplying by knockback
        self.velocity = [self.velocity[0] * knockback, self.velocity[1] * knockback]

    def check_stun_and_immunity(self, time):
        if time == self.stop_stun_time:
            self.stunned = False
        if time == self.stop_immunity_time:
            self.immune = False

    def rest_after_attack(self, time):
        self.stop_stun_time = time + rest_duration
        self.stunned = True

        self.velocity = [0, 0]

    # ----- GETTERS AND SETTERS -----
    def get_position(self):
        return [self.rect.x, self.rect.y]

    def get_speed(self):
        return self.speed

    def get_velocity(self):
        return self.velocity

    def get_max_health(self):
        return self.max_health

    def get_health(self):
        return self.health

    def get_damage(self):
        return self.damage

    def get_knockback_multiplier(self):
        return self.knockback_multiplier