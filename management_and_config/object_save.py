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


def save_curr_room(curr_room, db):
    room_str = ', '.join(map(str, curr_room))  # looks like string 5, 2
    db.update_curr_room(room_str)
    pass

# TODO edit
def load_curr_room(db):
    curr_room_str = db.get_curr_room()
    if curr_room_str is None:
        return None
    curr_room = [int(s) for s in curr_room_str.split(',')]
    return curr_room


def save_curr_world(curr_world, db):
    db.update_curr_world(curr_world)
    pass


def load_curr_world(db):
    curr_world = db.get_curr_world()
    return curr_world


