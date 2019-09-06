""" Manages actual screen display w all sprites and elements, hardcoded values included """

import sprites_management.sprites_manager
from management_and_config.configurations import *
from resources import image_manager

pygame.init()


class Room:
    def __init__(self, room_size, room_type, room_enemies):
        # specification of the room
        self.size = room_size
        self.type = room_type

        # walls group
        self.walls = pygame.sprite.Group()
        sprites_management.sprites_manager.add_walls(self.walls, room_size, room_type)

        # doors group
        self.doors = pygame.sprite.Group()
        sprites_management.sprites_manager.add_doors(self.doors, room_size, room_type)

        # enemies group
        self.enemies = pygame.sprite.Group()
        sprites_management.sprites_manager.add_enemies(self.enemies, room_enemies)

        # dropped items group
        self.drop = pygame.sprite.Group()

    def draw_room(self):
        screen.fill(WHITE)
        self.terrain_display()
        self.wall_display()
        self.door_display()
        self.enemy_display()
        self.drop_display()

    def terrain_display(self):
        terrain_image = image_manager.get_terrain_image()
        screen.blit(terrain_image, terrain_image_start_point)

    def wall_display(self):
        self.walls.draw(screen)

    def door_display(self):
        self.doors.draw(screen)

    def enemy_display(self):
        self.enemies.draw(screen)

        # displaying enemies' health
        for enemy in self.enemies.sprites():
            health = enemy.get_health()
            max_health = enemy.get_max_health()
            if health != max_health:
                health_bar_start_point = [enemy.get_position()[0] + enemy_health_bar_display_difference[0],
                                          enemy.get_position()[1] + enemy_health_bar_display_difference[1]]

                health_text_center = [health_bar_start_point[0] + enemy_health_text_center_difference[0],
                                      health_bar_start_point[1] + enemy_health_text_center_difference[1]]

                # health bar
                pygame.draw.rect(screen, PINK, (health_bar_start_point[0], health_bar_start_point[1],
                                                enemy_health_bar_length, enemy_health_bar_width))

                pygame.draw.rect(screen, RED, (health_bar_start_point[0], health_bar_start_point[1],
                                               enemy_health_bar_length * health / max_health, enemy_health_bar_width))

                # text: current health / max health in the center of health bar
                health_text = enemy_health_font.render(str(health) + "/" + str(max_health), True, BLACK)
                health_text_rect = health_text.get_rect()
                health_text_rect.center = health_text_center
                screen.blit(health_text, health_text_rect)

    def drop_display(self):
        self.drop.draw(screen)

    def kill_enemy(self, enemy):
        sprites_management.sprites_manager.add_drop(self.drop, enemy)
        self.enemies.remove(enemy)

    def remove_drop(self, drop):
        self.drop.remove(drop)

    def get_size(self):
        return self.size

    def get_walls(self):
        return self.walls

    def get_enemies(self):
        return self.enemies

    def get_dropped_items(self):
        return self.drop
