import pickle
import os

from management_and_config.configurations import character_start_point
from resources.image_manager import get_character_rest_image, get_character_walk_images
from sprites_management.character.Character import Character

location = os.path.abspath('../data/config.character')


def save_character(character, db, memory_slot):  # temporary only money
    db.update_money(character.get_money())
    db.update_date()
    db.update_health(character.get_health())
    db.update_experience(character.get_exp())
    show_popup('Progress saved!')


def show_popup(text):
    pass


def get_character():
    with open(location, 'rb') as config_character_file:
        # Step 3
        character = pickle.load(config_character_file)

        # After config_dictionary is read from file
        print(character)
        return character


def load_character(db, memory_slot = -1):
    character_rest_image = get_character_rest_image()
    character_walk_images = get_character_walk_images()
    stats = {
        "money": db.get_money(),
        "health": db.get_health(),
        "exp": db.get_experience()
    }
    # health = db.get_health(game_version) ...
    # exp
    return Character(character_start_point, character_rest_image, character_walk_images, stats)
