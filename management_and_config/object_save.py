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
    active_enemies_str = ''.join(map(str, active_enemies))
    db.update_active_enemies(active_enemies_str)
    pass


def load_active_enemies(db):
    act_en_str = db.get_active_enemies()
    print(act_en_str)
    active_enemies = []
    for c in act_en_str:
        active_enemies.append(int(c))
    return active_enemies


def save_character(character, db, memory_slot = -1):
    db.update_money(character.get_money())
    db.update_date()
    db.update_health(character.get_health())
    db.update_experience(character.get_exp())
    db.update_lvl(character.get_level())
    # show_popup('Progress saved!')
    # freeze_clock(0.5)


def get_character():
    with open(location, 'rb') as config_character_file:
        # Step 3
        character = pickle.load(config_character_file)

        # After config_dictionary is read from file
        print(character)
        return character


def load_character(db, memory_slot=-1):
    character_rest_image = get_character_rest_image()
    character_walk_images = get_character_walk_images()
    character_attack_image = get_character_attack_image()

    stats = {
        "money": db.get_money(),
        "health": db.get_health(),
        "exp": db.get_experience(),
        "lvl": db.get_lvl()
    }
    return Character(character_start_point, character_rest_image, character_walk_images, character_attack_image, stats)
