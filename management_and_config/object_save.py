""" Currently all saving functions are to be invoked in World class, during room changing by the main character.
When you go to the next WORLD, information about rooms' state in prev. world is overwritten by new world.
Eventually separate columns for each world could be made and all states would be remembered(but is it necessary?)"""

import os
import pickle
import json

from management_and_config.configurations import *
from management_and_config.display_functions import show_popup, freeze_clock
from resources.image_manager import get_character_rest_image, get_character_walk_images, get_character_attack_image
from sprites_management.character.Character import Character

location = os.path.abspath('../data/config.character')


# sprites------------------------------------------------------------
def save_active_enemies(active_enemies, db):
    db.update_active_enemies(json.dumps(active_enemies))
    pass


def load_active_enemies(db):
    return json.loads(db.get_active_enemies())


def save_character(character, db, memory_slot = -1):
    # saving info
    db.update_date()
    # general stats
    db.update_money(character.money)
    db.update_health(character.health)
    db.update_mana(character.mana)
    db.update_experience(character.exp)
    db.update_lvl(character.level)
    db.update_skill_points(character.skill_points)
    # skills upgrades
    db.update_attack_damage(character.attack_damage)
    db.update_attack_speed(character.attack_speed)
    db.update_critical_attack_chance(character.critical_attack_chance)
    # inventory
    db.update_sword(character.inventory["sword"])
    db.update_health_potion(character.inventory["health_potion"])
    # inventory - keys
    save_keys(character.keys, db)


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

    inventory = {
        "sword": db.get_sword(),
        "health_potion": db.get_health_potion(),
    }

    skills = {
        "sword_skill": db.get_sword_skill(),
    }
    # inventory - keys
    keys = load_keys(db)
    return Character(character_start_point, character_rest_image, character_walk_images, character_attack_image, stats, skills, inventory, keys)


# room state---------------------------------------------------------------
def load_doors(db):
    """ returns list of ints 0 - closed, 1- open"""
    return json.loads(db.get_doors())


def save_doors(open_doors, db):
    db.update_doors(json.dumps(open_doors))
    pass


def save_curr_room(curr_room, db):
    db.update_curr_room(json.dumps(curr_room))


def load_curr_room(db):
    return None if db.get_curr_room() is None else json.loads(db.get_curr_room())


def save_curr_world(curr_world, db):
    pass


def load_curr_world(db):
    pass


# helper functions
def save_keys(keys_dict, db):
    keys = json.dumps(keys_dict)
    db.update_keys(keys)


def load_keys(db):
    keys_dict = json.loads(db.get_keys())
    return keys_dict
