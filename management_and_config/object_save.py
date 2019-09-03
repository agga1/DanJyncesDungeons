import os
import pickle


from management_and_config.configurations import *
from management_and_config.display_functions import show_popup, freeze_clock
from resources.image_manager import get_character_rest_image, get_character_walk_images, get_character_attack_image
from sprites_management.character.Character import Character

location = os.path.abspath('../data/config.character')


def save_character(character, db, memory_slot = -1):
    db.update_money(character.get_money())
    db.update_date()
    db.update_health(character.get_health())
    db.update_experience(character.get_exp())
    db.update_lvl(character.get_lvl())
    show_popup('Progress saved!')
    freeze_clock(0.5)


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
    # health = db.get_health(game_version) ...
    # exp
    return Character(character_start_point, character_rest_image, character_walk_images, character_attack_image, stats)
