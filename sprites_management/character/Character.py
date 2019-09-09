from sprites_management.sprites_functions import *
from management_and_config.configurations import *


class Character(pygame.sprite.Sprite):
    def __init__(self, start_point, staying_image, movement_animation, attack_image, stats, *groups):
        super().__init__(*groups)

        # image
        self.original_image = staying_image
        self.image = staying_image
        self.angle = 0
        self.rect = self.image.get_rect()

        # animations
        self.staying_image = staying_image  # animation name: "rest"
        self.movement_animation = movement_animation  # animation name: "move"
        self.attack_image = attack_image  # animation name: "attack"

        self.curr_animation = "rest"
        self.animation_start_time = 0  # time when current animation started

        # position
        self.rect.x = start_point[0]
        self.rect.y = start_point[1]

        # stats
        self.attack_damage = character_start_attack_damage
        self.attack_speed = character_start_attack_speed
        self.critical_attack_chance = character_start_critical_attack_chance

        # health
        self.max_health = start_health
        self.health = stats["health"]

        # mana
        self.max_mana = 0
        self.mana = 0

        # money
        self.money = stats["money"]

        # levels
        self.exp = stats["exp"]
        self.level = stats["lvl"]
        self.to_next_level_exp = calculate_to_next_level_exp(self.level)

        self.skill_points = 0

        # checking if character is moving
        self.key_clicked = {"top": False, "bottom": False, "left": False, "right": False}

        # movement
        self.speed = character_speed
        self.velocity = [0, 0]

        # combat
        self.knockback = character_knockback
        self.is_attacking = False

        self.stunned = False
        self.immune = False
        self.stop_stun_time = 0
        self.stop_immunity_time = 0

    # ----- MOVEMENT -----
    def set_velocity(self, direction):
        self.velocity[0] = direction[0] * self.speed
        self.velocity[1] = direction[1] * self.speed

        # changing angle for rotation
        if not (self.velocity[0] == 0 and self.velocity[1] == 0):
            self.angle = find_character_angle(self.velocity)

    def move(self, curr_room, time):
        curr_position = [self.rect.x, self.rect.y]

        # attempt to move
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # checking collision with walls
        if pygame.sprite.spritecollide(self, curr_room.get_walls(), False):
            # if collide, do not move
            self.rect.x = curr_position[0]
            self.rect.y = curr_position[1]

        # checking animation and animating
        self.animation(time)

        # checking picking up drop
        for loot in pygame.sprite.spritecollide(self, curr_room.get_dropped_items(), False):
            if loot.get_name() == "exp":
                self.add_experience(1)
            elif loot.get_name() == "coin":
                self.add_money(1)

            curr_room.remove_drop(loot)

    # ----- CHARACTER IMAGE -----
    def animation(self, time):
        # changing current animation
        if self.is_attacking:
            self.curr_animation = "attack"
            self.animation_start_time = time
        elif (self.velocity[0] == 0 and self.velocity[1] == 0) or self.stunned:
            self.curr_animation = "rest"
            self.animation_start_time = time
        else:
            if not self.curr_animation == "move":
                self.animation_start_time = time
                self.curr_animation = "move"

        # animation
        if self.curr_animation == "rest":
            self.original_image = self.staying_image
        elif self.curr_animation == "move":
            self.original_image = animate(self.movement_animation, time, self.animation_start_time, frame_change_time)
        elif self.curr_animation == "attack":
            self.original_image = self.attack_image

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
                attacker.hit(curr_room, self, time, decide_critical_attack(self.critical_attack_chance))
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
            self.skill_points += 1
            self.exp -= self.to_next_level_exp
            self.to_next_level_exp = calculate_to_next_level_exp(self.level)

    def add_money(self, amount):
        self.money += amount

    # ----- UPGRADING STATS -----
    def upgrade_stat_attack_damage(self):
        self.attack_damage += upgrade_attack_damage
        self.skill_points -= 1

    def upgrade_stat_attack_speed(self):
        if self.attack_speed < max_attack_speed:
            self.attack_speed += upgrade_attack_speed
            self.attack_speed = round(self.attack_speed, 1)  # to avoid that problem: 0.7 + 0.1 = 0.799999
            self.skill_points -= 1

    def upgrade_stat_critical_attack_chance(self):
        if self.critical_attack_chance < max_critical_attack_chance:
            self.critical_attack_chance += upgrade_critical_attack_chance
            self.skill_points -= 1

    def upgrade_stat_health(self):
        self.max_health += upgrade_health
        self.health += upgrade_health
        self.skill_points -= 1

    def upgrade_stat_mana(self):
        self.max_mana += upgrade_mana
        self.mana += upgrade_mana
        self.skill_points -= 1

    # ----- GETTERS AND SETTERS -----
    def set_position(self, new_room_direction, new_room_size):
        new_position = [0, 0]

        if new_room_direction == "top":
            new_position[0] = self.rect.x
            new_position[1] = new_room_size[1] * 50 - distance_from_door
        elif new_room_direction == "bottom":
            new_position[0] = self.rect.x
            new_position[1] = 0  # distance_from_door
        elif new_room_direction == "left":
            new_position[0] = new_room_size[0] * 50 - distance_from_door
            new_position[1] = self.rect.y
        elif new_room_direction == "right":
            new_position[0] = 0  # distance_from_door
            new_position[1] = self.rect.y

        self.rect.x = new_position[0]
        self.rect.y = new_position[1]

    def set_key_clicked(self, direction, click):  # setting that the movement key is (not) being pressed
        self.key_clicked[direction] = click

    def get_position(self):
        return [self.rect.x, self.rect.y]

    def get_attack_damage(self):
        return self.attack_damage

    def get_attack_speed(self):
        return self.attack_speed

    def get_critical_attack_chance(self):
        return self.critical_attack_chance

    def get_key_clicked(self, direction):
        return self.key_clicked[direction]

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

    def get_max_health(self):
        return self.max_health

    def get_health(self):
        return self.health

    def get_max_mana(self):
        return self.max_mana

    def get_mana(self):
        return self.mana

    def get_exp(self):
        return self.exp

    def get_level(self):
        return self.level

    def get_to_next_level_exp(self):
        return self.to_next_level_exp

    def get_skill_points(self):
        return self.skill_points
