from sprites_management.sprites_functions import *
from management_and_config.configurations import *


class Character(pygame.sprite.Sprite):
    def __init__(self, start_point, staying_image, movement_animation, attack_image, stats, skills, inventory, equipment, keys, *groups):
        super().__init__(*groups)

        # image
        self._original_image = staying_image
        self.image = staying_image
        self._angle = 0
        self.rect = self.image.get_rect()

        # animations
        self._staying_image = staying_image  # animation name: "rest"
        self._movement_animation = movement_animation  # animation name: "move"
        self._attack_image = attack_image  # animation name: "attack"

        self._curr_animation = "rest"
        self._animation_start_time = 0  # time when current animation started

        # position
        self.rect.x = start_point[0]
        self.rect.y = start_point[1]

        # stats
        self._attack_damage = stats["attack_damage"]
        self._attack_speed = stats["attack_speed"]
        self._critical_attack_chance = stats["critical_attack_chance"]

        # inventory TODO: get inv from db
        self._inventory = inventory

        # equipped inventory TODO get from db and save to db
        self._equipment = equipment

        # skills active TODO: get from db active skills (for now: sword skill)
        # TODO: make unique (funny?) names for skills
        self._skills = skills
        self._skills_max_lvl = {"sword_skill": 1}

        # health
        self._max_health = start_health
        self._health = stats["health"]

        # mana
        self._max_mana = 0
        self._mana = stats["mana"]

        # keys
        self._keys = keys

        # money
        self._money = stats["money"]

        # levels
        self._exp = stats["exp"]
        self._level = stats["lvl"]
        self._to_next_level_exp = calculate_to_next_level_exp(self._level)

        self._skill_points = stats["skill_points"]

        # checking if character is moving
        self._key_clicked = {"top": False, "bottom": False, "left": False, "right": False}

        # movement
        self._speed = character_speed
        self._velocity = [0, 0]

        # combat
        self._knockback = character_knockback
        self._is_attacking = False

        self._stunned = False
        self._immune = False
        self._stop_stun_time = 0
        self._stop_immunity_time = 0

    # ----- MOVEMENT -----
    def set_velocity(self, direction):
        self._velocity[0] = direction[0] * self._speed
        self._velocity[1] = direction[1] * self._speed

        # changing angle for rotation
        if not (self._velocity[0] == 0 and self._velocity[1] == 0):
            self._angle = find_character_angle(self._velocity)

    def move(self, curr_room, time):
        curr_position = [self.rect.x, self.rect.y]

        # attempt to move
        self.rect.x += self._velocity[0]
        self.rect.y += self._velocity[1]

        # checking collision with walls
        if pygame.sprite.spritecollide(self, curr_room.walls, False):
            # if collision, do not move
            self.rect.x = curr_position[0]
            self.rect.y = curr_position[1]

        # checking collision with doors
        door_collision = pygame.sprite.spritecollide(self, curr_room.doors, False)
        if door_collision:
            for door in door_collision:
                if door.closed:
                    # if collision with closed doors, do not move
                    self.rect.x = curr_position[0]
                    self.rect.y = curr_position[1]

        # checking animation and animating
        self.animation(time)

        # checking picking up drop
        self.check_drop(curr_room, time)

    def check_drop(self, curr_room, time):
        for loot in pygame.sprite.spritecollide(self, curr_room.dropped_items, False):
            if time >= loot.pick_up_time:
                if loot.name == "exp":
                    self.add_experience(1)
                elif loot.name == "coin":
                    self.add_money(1)
                elif loot.name == "grey key":
                    self.add_key("grey")
                elif loot.name == "blue key":
                    self.add_key("blue")
                elif loot.name == "green key":
                    self.add_key("green")
                elif loot.name == "yellow key":
                    self.add_key("yellow")

                curr_room.remove_drop(loot)

    # ----- CHARACTER IMAGE -----
    def animation(self, time):
        # changing current animation
        if self._is_attacking:
            self._curr_animation = "attack"
            self._animation_start_time = time
        elif (self._velocity[0] == 0 and self._velocity[1] == 0) or self._stunned:
            self._curr_animation = "rest"
            self._animation_start_time = time
        else:
            if not self._curr_animation == "move":
                self._animation_start_time = time
                self._curr_animation = "move"

        # animation
        if self._curr_animation == "rest":
            self._original_image = self._staying_image
        elif self._curr_animation == "move":
            self._original_image = animate(self._movement_animation, time, self._animation_start_time,
                                           frame_change_time)
        elif self._curr_animation == "attack":
            self._original_image = self._attack_image

        # rotation
        self.rot_center()

    def rot_center(self):
        self.image = pygame.transform.rotate(self._original_image, self._angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    # ----- COMBAT -----
    def check_collisions(self, curr_room, time):
        # checking collision with enemies
        aggressors = pygame.sprite.spritecollide(self, curr_room.enemies, False)
        for aggressor in aggressors:
            if self._is_attacking:
                aggressor.hit(curr_room, self, time, decide_critical_attack(self._critical_attack_chance))
            else:
                self.hit(aggressor, time)

    def hit(self, aggressor, time):
        if not self._immune:
            # damage and death
            self._health -= aggressor.damage
            self.check_death()

            # stun
            self._stunned = True
            self._stop_stun_time = time + knockback_duration

            # immunity to attacks
            self._immune = True
            self._stop_immunity_time = time + immunity_duration

            # knockback
            self._velocity = calculate_knockback(aggressor, self)

            # stunning enemy for a while
            aggressor.rest_after_attack(time)

    def check_death(self):
        # end of the game
        if self._health <= 0:
            exit(1)

    def start_attack(self):
        self._is_attacking = True

    def stop_attack(self):
        self._is_attacking = False

    def check_stun_and_immunity(self, time):
        if time == self._stop_stun_time:
            self._stunned = False
            self.set_velocity([0, 0])
        if time == self._stop_immunity_time:
            self._immune = False

    # ----- SKILLS -----
    def buy_skill(self, skill_name):
        if self._skills[skill_name] is not None:
            if self._skills[skill_name] < self._skills_max_lvl[skill_name]:
                self._skills[skill_name] += 1
                self._skill_points -= 1

    # ----- INVENTORY USE & EQUIPMENT ----
    def use(self, item_name):
        if item_name == "sword":
            # TODO equip sword hardcoded
            if self._skills["sword_skill"] == 0:
                return
            self._inventory["sword"] -= 1
            if self._equipment["weapon"] is not "":
                self._inventory[self._equipment["weapon"]] += 1
            self._equipment["weapon"] = "sword"
            # self._bonus_damage = 3 TODO what bonus?
        elif item_name == "health_potion":
            # TODO health potion hardcoded
            self._inventory["health_potion"] -= 1
            self._health = min(self._health + 5, self._max_health)

    def buy(self, item_name, item_price=0):
        if self._money - item_price >= 0:
            self._money -= item_price
            self._inventory[item_name] += 1

    def unequip(self, part):
        if self._equipment[part] is not "":
            self._inventory[self._equipment[part]] += 1
        self._equipment[part] = ""

    # ----- DROP & ITEMS -----
    def add_experience(self, amount):
        self._exp += amount
        self.check_level()

    def check_level(self):
        while self._exp >= self._to_next_level_exp:
            self._level += 1
            self._skill_points += 1
            self._exp -= self._to_next_level_exp
            self._to_next_level_exp = calculate_to_next_level_exp(self._level)

    def add_key(self, key):
        self._keys[key] += 1

    def add_money(self, amount):
        self._money += amount

    def use_key(self, key):
        self._keys[key] -= 1

    # ----- UPGRADING STATS -----
    def upgrade_stat_attack_damage(self):
        self._attack_damage += upgrade_attack_damage
        self._skill_points -= 1

    def upgrade_stat_attack_speed(self):
        if self._attack_speed < max_attack_speed:
            self._attack_speed += upgrade_attack_speed
            self._attack_speed = round(self._attack_speed, 1)  # to avoid that problem: 0.7 + 0.1 = 0.799999
            self._skill_points -= 1

    def upgrade_stat_critical_attack_chance(self):
        if self._critical_attack_chance < max_critical_attack_chance:
            self._critical_attack_chance += upgrade_critical_attack_chance
            self._skill_points -= 1

    def upgrade_stat_health(self):
        self._max_health += upgrade_health
        self._health += upgrade_health
        self._skill_points -= 1

    def upgrade_stat_mana(self):
        self._max_mana += upgrade_mana
        self._mana += upgrade_mana
        self._skill_points -= 1

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
        self._key_clicked[direction] = click

    def get_position(self):
        return [self.rect.x, self.rect.y]

    def get_position_center(self):
        return self.rect.center

    def get_skill_activated(self, skill_name):
        if self._skills[skill_name] > 0:
            return True
        else:
            return False

    @property
    def attack_damage(self):
        """ current attack damage """
        return self._attack_damage

    @property
    def attack_speed(self):
        """ current attack speed """
        return self._attack_speed

    @property
    def critical_attack_chance(self):
        """ current critical attack chance """
        return self._critical_attack_chance

    @property
    def key_clicked(self):
        """ current clicked keys (array) """
        return self._key_clicked

    @property
    def speed(self):
        """ character speed """
        return self._speed

    @property
    def knockback(self):
        """ current knockback """
        return self._knockback

    @property
    def is_attacking(self):
        """ it is true during character attack """
        return self._is_attacking

    @property
    def stunned(self):
        """ it is true when character is stunned """
        return self._stunned

    @property
    def money(self):
        """ current amount of money """
        return self._money

    @property
    def max_health(self):
        """ maximum possible health now """
        return self._max_health

    @property
    def health(self):
        """ current character health """
        return self._health

    @property
    def max_mana(self):
        """ maximum possible mana now """
        return self._max_mana

    @property
    def mana(self):
        """ current character mana """
        return self._mana

    @property
    def keys(self):
        """ array with numbers of particular keys """
        return self._keys

    @property
    def exp(self):
        """ current character experience points """
        return self._exp

    @property
    def level(self):
        """ current character level """
        return self._level

    @property
    def to_next_level_exp(self):
        """ amount of experience needed to get next level """
        return self._to_next_level_exp

    @property
    def skill_points(self):
        """ amount of skill points ready to be spent on new skills or stats improvement """
        return self._skill_points

    @property
    def inventory(self):
        """ directory of items owned by character ( "sword": nr_of_owned_swords )"""
        return self._inventory

    @property
    def equipment(self):
        """ dir {"weapon": "", "armor: ""} """
        return self._equipment

    @money.setter
    def money(self, money):
        self._money = money
