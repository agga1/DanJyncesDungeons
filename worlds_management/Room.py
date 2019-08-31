""" Manages actual screen display w all sprites and elements, hardcoded values included """

import sprites_management.sprites_manager
from management_and_config.configurations import *
from resources import image_manager

pygame.init()

money_font = pygame.font.Font('freesansbold.ttf', 25)
level_font = pygame.font.Font('freesansbold.ttf', 40)


class Room:
    def __init__(self, room_size, room_type, room_enemies):
        # specification of the room
        self.size = room_size
        self.type = room_type

        # walls group
        self.walls = pygame.sprite.Group()
        sprites_management.sprites_manager.add_walls(self.walls, room_size, room_type)

        # enemies group
        self.enemies = pygame.sprite.Group()
        sprites_management.sprites_manager.add_enemies(self.enemies, room_enemies)

    def draw_room(self):
        screen.fill(WHITE)
        self.terrain_display()
        self.wall_display()
        self.enemy_display()

    def terrain_display(self):
        terrain_image = image_manager.get_terrain_image()
        screen.blit(terrain_image, terrain_image_start_point)

    def wall_display(self):
        self.walls.draw(screen)

    def enemy_display(self):
        self.enemies.draw(screen)

    def get_size(self):
        return self.size

    def get_walls(self):
        return self.walls

    def get_enemies(self):
        return self.enemies
