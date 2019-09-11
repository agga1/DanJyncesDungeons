from sprites_management.sprites_functions import *
from management_and_config.configurations import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_id, start_point, movement_animation, *groups):
        super().__init__(*groups)
        # id
        self._id = enemy_id

        # images
        self._original_image = movement_animation[0]
        self.image = movement_animation[0]
        self._angle = 0
        self.rect = self.image.get_rect()

        # animation
        self._animation_start = 0  # time when current animation started
        self._movement_animation = movement_animation

        # position
        self.rect.x = start_point[0]
        self.rect.y = start_point[1]

        # rect.x and rec.y must be integers so to make movement more precise we need that float
        self._exact_pos = start_point

        # movement
        self._speed = enemy_speed
        self._velocity = [0, 0]

        # health
        self._max_health = enemy_health
        self._health = enemy_health  # it will be changed after hit

        # combat
        self._damage = enemy_damage
        self._knockback_multiplier = enemy_knockback_multiplier

        self._stunned = False
        self._immune = False
        self._stop_stun_time = 0
        self._stop_immunity_time = 0

        # after being killed
        self._drop = {"coin_range": enemy_money_drop_range, "exp": enemy_exp_drop}

    # ----- MOVEMENT -----
    def set_velocity_to_follow(self, main_character):
        # main character is a target
        curr_character_position_center = [main_character.get_position()[0] + sprite_size[0]/2,
                                          main_character.get_position()[1] + sprite_size[1]/2]
        position_difference = [self.rect.x - curr_character_position_center[0],
                               self.rect.y - curr_character_position_center[1]]

        # calculating angle
        angle = calculate_arctan(position_difference)

        # setting velocity
        if position_difference[0] >= 0:
            self._velocity = [-1 * self._speed * math.cos(angle), -1 * self._speed * math.sin(angle)]
        else:
            self._velocity = [self._speed * math.cos(angle), self._speed * math.sin(angle)]

        # changing angle for rotation (it is for animation)
        if not (self._velocity[0] == 0 and self._velocity[1] == 0):
            self._angle = calculate_arctan(self._velocity)

            if self._velocity[0] < 0:
                self._angle = math.degrees(-1 * self._angle + math.pi / 2)
            else:
                self._angle = math.degrees(-1 * self._angle - math.pi / 2)

    def move(self, character_group, time):
        # checking if can move and be hit
        self.check_stun_and_immunity(time)

        # following main character if not colliding with him
        for main_character in character_group:
            # to not change velocity during stun
            if not self._stunned:
                self.set_velocity_to_follow(main_character)

            colliding_with_character = pygame.sprite.spritecollide(self, character_group, False)

            if self._stunned or not colliding_with_character:
                # to improve softness of movement
                self._exact_pos[0] += self._velocity[0]
                self._exact_pos[1] += self._velocity[1]

                self.rect.x = self._exact_pos[0]
                self.rect.y = self._exact_pos[1]

        # animation
        self._original_image = animate(self._movement_animation, time, self._animation_start, enemy_frame_change_time)

        # rotation
        self.rot_center()

    def rot_center(self):
        self.image = pygame.transform.rotate(self._original_image, self._angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    # ----- COMBAT -----
    def hit(self, curr_room, main_character, time, critical):
        if not self._immune:
            if not critical:
                self._health -= main_character.attack_damage
            else:
                self._health -= 2 * main_character.get_attack_damage()

            self.check_death(curr_room)

            self.knockback(main_character, time)

    def check_death(self, curr_room):
        if self._health <= 0:
            curr_room.kill_enemy(self)

    def knockback(self, main_character, time):
        # setting variables
        self._stop_stun_time = time + knockback_duration
        self._stop_immunity_time = time + immunity_duration
        self._immune = True
        self._stunned = True

        # choosing direction to make the biggest distance between enemy and character
        character_position = main_character.get_position()
        knockback_direction = [character_position[0] - self.rect.x, character_position[1] - self.rect.y]
        knockback = main_character.knockback

        # calculating angle
        angle = calculate_arctan(knockback_direction)

        # setting velocity
        if knockback_direction[0] >= 0:
            self._velocity = [-1 * self._speed * math.cos(angle), -1 * self._speed * math.sin(angle)]
        else:
            self._velocity = [self._speed * math.cos(angle), self._speed * math.sin(angle)]

        # multiplying by knockback
        self._velocity = [self._velocity[0] * knockback, self._velocity[1] * knockback]

    def check_stun_and_immunity(self, time):
        if time == self._stop_stun_time:
            self._stunned = False
        if time == self._stop_immunity_time:
            self._immune = False

    def rest_after_attack(self, time):
        self._stop_stun_time = time + rest_duration
        self._stunned = True

        self._velocity = [0, 0]

    # ----- GETTERS AND SETTERS -----
    def get_position(self):
        return [self.rect.x, self.rect.y]

    @property
    def id(self):
        """ enemy's id """
        return self._id

    @property
    def speed(self):
        """ enemy's speed """
        return self._speed

    @property
    def velocity(self):
        """ enemy's current velocity """
        return self._velocity

    @property
    def max_health(self):
        """ enemy's maximum health """
        return self._max_health

    @property
    def health(self):
        """ enemy's current health """
        return self._health

    @property
    def damage(self):
        """ enemy's attack damage """
        return self._damage

    @property
    def knockback_multiplier(self):
        """ enemy's knockback """
        return self._knockback_multiplier

    @property
    def drop(self):
        """ enemy's drop """
        return self._drop
