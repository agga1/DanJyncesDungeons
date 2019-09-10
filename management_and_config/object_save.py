""" Currently all saving functions are to be invoked in World class, during room changing by the main character.
When you go to the next WORLD, information about rooms' state in prev. world is overwritten by new world.
Eventually separate columns for each world could be made and all states would be remembered(but is it necessary?)"""

import os
import pickle

from management_and_config.configurations import *
from management_and_config.display_functions import show_popup, freeze_clock
from resources.image_manager import get_character_rest_image, get_character_walk_images, get_character_attack_image
from sprites_management.character.Character import Character

location = os.path.abspath('../data/config.character')


def save_active_enemies(active_enemies, db):
    active_enemies_str = ''.join(map(str, active_enemies))  # looks like string 11011101
    db.update_active_enemies(active_enemies_str)
    pass


def load_active_enemies(db):
    act_en_str = db.get_active_enemies()  # looks like 1101101
    active_enemies = []
    for c in act_en_str:
        active_enemies.append(int(c))
    return active_enemies


def save_character(character, db, memory_slot = -1):
    # saving info
    db.update_date()
    # general stats
    db.update_money(character.get_money())
    db.update_health(character.get_health())
    db.update_mana(character.get_mana())
    db.update_experience(character.get_exp())
    db.update_lvl(character.get_level())
    db.update_skill_points(character.get_skill_points())
    # skills upgrades
    db.update_attack_damage(character.get_attack_damage())
    db.update_attack_speed(character.get_attack_speed())
    db.update_critical_attack_chance(character.get_critical_attack_chance())


def load_character(db, memory_slot=-1):
    character_rest_image = get_character_rest_image()
    character_walk_images = get_character_walk_images()
    character_attack_image = get_character_attack_image()

    stats = {
        "money": db.get_money(),
        "health": db.get_health(),
        "mana": db.get_mana(),
        "exp": db.get_experience(),
        "lvl": db.get_lvl(),
        "skill_points": db.get_skill_points(),
        "attack_damage": db.get_attack_damage(),
        "attack_speed": db.get_attack_speed(),
        "critical_attack_chance": db.get_critical_attack_chance(),
    }
    return Character(character_start_point, character_rest_image, character_walk_images, character_attack_image, stats)


def save_curr_room(curr_room, db):
    room_str = ', '.join(map(str, curr_room))  # looks like string 5, 2
    db.update_curr_room(room_str)


def load_curr_room(db):
    curr_room_str = db.get_curr_room()
    if curr_room_str is None:
        return None
    curr_room = [int(s) for s in curr_room_str.split(',')]
    return curr_room


def save_curr_world(curr_world, db):
    pass


def load_curr_world(db):
    pass


def get_character():
    with open(location, 'rb') as config_character_file:
        # Step 3
        character = pickle.load(config_character_file)

        # After config_dictionary is read from file
        print(character)
        return character

