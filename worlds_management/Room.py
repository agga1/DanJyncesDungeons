import pygame

from core import sprites_functions
from resources import image_manager

pygame.init()

# ----- VARIABLES -----
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

font = pygame.font.Font('freesansbold.ttf', 25)


# ----- CLASS -----
class Room:
    def __init__(self, room_size, room_type, room_enemies):
        # specification of the room
        self.size = room_size
        self.type = room_type

        # walls group
        self.walls = pygame.sprite.Group()
        if room_type == "classic":
            sprites_functions.add_walls(self.walls, room_size)

        # enemies group
        self.enemies = pygame.sprite.Group()
        sprites_functions.add_enemies(self.enemies, room_enemies)

        # character group
        self.character = pygame.sprite.Group()
        self.character_start_point = [300, 300]
        sprites_functions.add_character(self.character, self.character_start_point)

        # terrain
        self.terrain_image_start_point = [50, 50]

        # health
        self.health_start_point = (10, 5)
        self.health_bar_width = 20
        self.health_bar_length = 120

        # money
        self.money_start_point = [510, 15]

    def draw_room(self):
        screen.fill(WHITE)
        self.terrain_display()
        self.wall_display()
        self.health_display()
        self.money_display()
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

    def money_display(self):
        coin_image = image_manager.get_coin_image()

        from core.main import money
        money_text = font.render(str(money), True, YELLOW)
        screen.blit(coin_image, self.money_start_point)
        screen.blit(money_text, [self.money_start_point[0] + 25, self.money_start_point[1]])

    def get_walls(self):
        return self.walls

    def get_character(self):
        return self.character

    def get_enemies(self):
        return self.enemies
