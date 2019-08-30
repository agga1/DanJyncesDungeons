""" Manages actual screen display w all sprites and elements, hardcoded values included """

import pygame

import core.sprites_manager
from resources import image_manager

pygame.init()

# ----- VARIABLES -----
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])

GREEN = (0, 185, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

money_font = pygame.font.Font('freesansbold.ttf', 25)
level_font = pygame.font.Font('freesansbold.ttf', 40)


# ----- CLASS -----
class Room:
    def __init__(self, room_size, room_type, room_enemies):
        # specification of the room
        self.size = room_size
        self.type = room_type

        # walls group
        self.walls = pygame.sprite.Group()
        if room_type == "classic":
            core.sprites_manager.add_walls(self.walls, room_size)

        # enemies group
        self.enemies = pygame.sprite.Group()
        core.sprites_manager.add_enemies(self.enemies, room_enemies)

        # character group
        self.character = pygame.sprite.Group()
        self.character_start_point = [300, 300]
        core.sprites_manager.add_character(self.character, self.character_start_point)

        # terrain
        self.terrain_image_start_point = [50, 50]

        # health
        self.health_start_point = [430, 5]
        self.health_bar_width = 20
        self.health_bar_length = 120

        # money
        self.money_start_point = [510, 560]

        # levels
        self.level_start_point = [10, 5]
        self.experience_bar_width = 10
        self.experience_bar_length = 120

    def draw_room(self, money):
        screen.fill(WHITE)
        self.terrain_display()
        self.wall_display()
        self.health_display()
        self.money_display(money)
        self.level_display()
        self.enemy_display()
        self.character_display()

    def terrain_display(self):
        terrain_image = image_manager.get_terrain_image()
        screen.blit(terrain_image, self.terrain_image_start_point)

    def wall_display(self):
        self.walls.draw(screen)

    def enemy_display(self):
        self.enemies.draw(screen)

    def character_display(self):
        self.character.draw(screen)

    def health_display(self):
        heart_image = image_manager.get_heart_image()

        screen.blit(heart_image, self.health_start_point)

        for player in self.character.sprites():
            health = player.get_health()
            max_health = player.get_max_health()

            pygame.draw.rect(screen, RED,
                             [self.health_start_point[0] + 35, self.health_start_point[1], self.health_bar_length,
                              self.health_bar_width], 1)

            pygame.draw.rect(screen, RED, [self.health_start_point[0] + 35, self.health_start_point[1],
                                           health * self.health_bar_length / max_health, self.health_bar_width])

    def money_display(self, money):
        coin_image = image_manager.get_coin_image()

        money_number = money_font.render(str(money), True, YELLOW)
        screen.blit(coin_image, self.money_start_point)
        screen.blit(money_number, [self.money_start_point[0] + 25, self.money_start_point[1]])

    def level_display(self):
        for main_character in self.character.sprites():
            level_number = level_font.render(str(main_character.get_level()), True, GREEN)
            screen.blit(level_number, self.level_start_point)

            exp = main_character.get_curr_exp()
            max_exp = main_character.get_to_next_level_exp()

            pygame.draw.rect(screen, GREEN,
                             [self.level_start_point[0] + 35, self.level_start_point[1] + 10, self.experience_bar_length,
                              self.experience_bar_width], 1)

            pygame.draw.rect(screen, GREEN, [self.level_start_point[0] + 35, self.level_start_point[1] + 10,
                                             exp * self.experience_bar_length / max_exp, self.experience_bar_width])

    def get_walls(self):
        return self.walls

    def get_character(self):
        return self.character

    def get_enemies(self):
        return self.enemies
