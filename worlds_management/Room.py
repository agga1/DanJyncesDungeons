import pygame

from character.Character import Character
from enemies.Enemy import Enemy
from obstacles.Wall import Wall

from core.main import screen_width, screen_height, money
from core import sprites_functions

# ----- VARIABLES -----
screen = pygame.display.set_mode([screen_width, screen_height])

RED = (255, 0, 0)
YELLOW = (255, 255, 0)

font = pygame.font.Font('freesansbold.ttf', 25)


# ----- CLASS -----
class Room:
    def __init__(self):
        # sprite groups
        self.walls = pygame.sprite.Group()
        sprites_functions.add_walls(self.walls)

        self.enemies = pygame.sprite.Group()
        sprites_functions.add_enemies(self.enemies)

        self.character = pygame.sprite.Group()
        self.character_start_point = [300, 300]
        sprites_functions.add_character(self.character, self.character_start_point)

        # other variables
        self.terrain_image_start_point = [50, 50]

        self.health_start_point = (10, 5)
        self.health_bar_width = 20
        self.health_bar_length = 120

        self.money_start_point = [510, 15]

    def terrain_display(self):
        terrain_image = pygame.image.load("../resources/terrain.png")
        screen.blit(terrain_image, self.terrain_image_start_point)

    def wall_display(self):
        self.walls.draw(screen)

    def enemy_display(self):
        self.enemies.draw(screen)

    def character_display(self):
        self.character.draw(screen)

    def health_display(self):
        heart_image = pygame.image.load("../resources/heart.png")

        screen.blit(heart_image, self.health_start_point)

        for player in self.character.sprites():
            health = player.get_health()
            max_health = player.get_max_health()
            pygame.draw.rect(screen, RED,
                             [self.health_start_point[0] + 35, self.health_start_point[1], self.health_bar_length,
                              self.health_bar_width], 1)

            pygame.draw.rect(screen, RED, [self.health_start_point[0] + 35, self.health_start_point[1],
                                           health * self.health_bar_length / max_health, self.health_bar_width])

    def money_display(self):
        coin_image = pygame.image.load("../resources/coin.png")

        money_text = font.render(str(money), True, YELLOW)
        screen.blit(coin_image, self.money_start_point)
        screen.blit(money_text, [self.money_start_point[0] + 25, self.money_start_point[1]])