""" Manages actual screen display w all sprites and elements, hardcoded values included """

import sprites_management.sprites_manager
from management_and_config.configurations import *
from resources import image_manager

pygame.init()


class Room:
    def __init__(self, room_size, room_type, room_enemies):
        # specification of the room
        self._size = room_size
        self._type = room_type

        self._enemies_on_start = []
        for enemy in room_enemies:
            self._enemies_on_start.append(enemy.id)

        # walls group
        self._walls = pygame.sprite.Group()
        sprites_management.sprites_manager.add_walls(self._walls, room_size, room_type)

        # doors group
        self._doors = pygame.sprite.Group()
        sprites_management.sprites_manager.add_doors(self._doors, room_size, room_type)

        # enemies group
        self._enemies = pygame.sprite.Group()
        sprites_management.sprites_manager.add_enemies(self._enemies, room_enemies)

        # dropped items group
        self._drop = pygame.sprite.Group()

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
        self._walls.draw(screen)

    def door_display(self):
        self._doors.draw(screen)

    def enemy_display(self):
        self._enemies.draw(screen)

        # displaying enemies' health
        for enemy in self._enemies.sprites():
            health = enemy.health
            max_health = enemy.max_health
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
        self._drop.draw(screen)

    def kill_enemy(self, enemy, time):
        sprites_management.sprites_manager.add_drop(self._drop, enemy, time)
        self._enemies.remove(enemy)

    def remove_drop(self, drop):
        self._drop.remove(drop)

    def update_active_enemies(self, active_enemies):
        for enemy_id in self._enemies_on_start:
            active_enemies[enemy_id] = 0

        for enemy in self._enemies:
            active_enemies[enemy.id] = 1

        return active_enemies

    @property
    def size(self):
        """ size of the room """
        return self._size

    @property
    def walls(self):
        """ room's walls (sprite group of walls) """
        return self._walls

    @property
    def doors(self):
        """ room's doors (sprite group of doors) """
        return self._doors

    @property
    def enemies(self):
        """ room's enemies (sprite group of enemies) """
        return self._enemies

    @property
    def dropped_items(self):
        """ items dropped in the room (sprite group of drops) """
        return self._drop
