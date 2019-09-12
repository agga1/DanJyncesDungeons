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
        self._frame_change_time = None

        # position
        self.rect.x = start_point[0]
        self.rect.y = start_point[1]

        # rect.x and rec.y must be integers so to make movement more precise we need that float
        self._exact_pos = start_point

        # movement
        self._speed = None
        self._velocity = [0, 0]

        # health
        self._max_health = None
        self._health = None  # it will be changed after hit

        # combat
        self._damage = None
        self._knockback = None

        self._stunned = False
        self._immune = False
        self._stop_stun_time = 0
        self._stop_immunity_time = 0

        # after death
        self._drop = None

    # ----- MOVEMENT -----
    def set_velocity(self, worlds_manager):
        pass

    def move(self, worlds_manager, time):
        # checking if can move and be hit
        self.check_stun_and_immunity(time)

        # to not change velocity during stun
        if not self._stunned:
            self.set_velocity(worlds_manager)

        # moving if not colliding with character
        colliding_with_character = pygame.sprite.spritecollide(self, worlds_manager.character, False)

        if self._stunned or not colliding_with_character:
            curr_exact_position = [self._exact_pos[0], self._exact_pos[1]]  # to avoid copying variable
            curr_position = [self.rect.x, self.rect.y]

            # attempt to move (exact pos variable is to improve softness of movement)
            self._exact_pos[0] += self._velocity[0]
            self._exact_pos[1] += self._velocity[1]

            self.rect.x = self._exact_pos[0]
            self.rect.y = self._exact_pos[1]

            # checking collision with walls
            if pygame.sprite.spritecollide(self, worlds_manager.curr_world.curr_room.walls, False) or \
                    pygame.sprite.spritecollide(self, worlds_manager.curr_world.curr_room.doors, False):

                # if collision, do not move
                self.rect.x = curr_position[0]
                self.rect.y = curr_position[1]

                self._exact_pos[0] = curr_exact_position[0]
                self._exact_pos[1] = curr_exact_position[1]

        # animation
        self._original_image = animate(self._movement_animation, time, self._animation_start, self._frame_change_time)

        # rotation
        self.rot_center()

    # ----- ANIMATION -----
    def change_angle(self):
        if not (self._velocity[0] == 0 and self._velocity[1] == 0):
            self._angle = calculate_arctan(self._velocity)

            if self._velocity[0] < 0:
                self._angle = math.degrees(-1 * self._angle + math.pi / 2)
            else:
                self._angle = math.degrees(-1 * self._angle - math.pi / 2)

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

            self.check_death(curr_room, time)

            # knockback
            self._stop_stun_time = time + knockback_duration
            self._stop_immunity_time = time + immunity_duration
            self._immune = True
            self._stunned = True

            # calculating knockback velocity
            self._velocity = calculate_knockback(main_character, self)

    def check_death(self, curr_room, time):
        if self._health <= 0:
            curr_room.kill_enemy(self, time)

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
    def knockback(self):
        """ enemy's knockback """
        return self._knockback

    @property
    def drop(self):
        """ enemy's drop """
        return self._drop
