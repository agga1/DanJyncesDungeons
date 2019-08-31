import pygame

from core.Inventory import Inventory
from worlds_management.WorldsManager import WorldsManager
from db.MyDatabase import MyDatabase
from core.menu_activity import menu_run
from core.game_activity import game_run

pygame.init()

# database

db = MyDatabase()
# TO DO: show start screen: buttons: new game->db.insert() continue->choose from saved versions
# ----- VARIABLES -----

# CAPTION
pygame.display.set_caption("Dan Jynce's Dungeons")

game_version = menu_run(db)  # returns which game should be played (equals to row_id in db)
game_run(db, game_version)
