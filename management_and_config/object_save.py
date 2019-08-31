import pickle
import os
location = os.path.abspath('../data/config.character')


def save_character(character):  # temporary only money
    with open(location, 'wb') as config_character_file:
        pickle.dump(character, config_character_file)
    get_character()


def get_character():
    with open(location, 'rb') as config_character_file:
        # Step 3
        character = pickle.load(config_character_file)

        # After config_dictionary is read from file
        print(character)
        return character
