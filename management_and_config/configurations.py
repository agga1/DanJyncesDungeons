""" Contains all hardcoded gui values (fonts, colors, coord)"""
import pygame

pygame.init()

# ----- GENERAL -----

screen_width = 600
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])

clock = pygame.time.Clock()

# fonts
main_font = 'freesansbold.ttf'

font_size_info = 14
font_size_bar = 12
font_size_money = 25
font_size_level = 40
font_size_enemy_health = 15

money_font = pygame.font.Font(main_font, font_size_money)
level_font = pygame.font.Font(main_font, font_size_level)
enemy_health_font = pygame.font.Font(main_font, font_size_enemy_health)

# colors
GREEN = (0, 185, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 150, 150)
BROWN = (150, 75, 0)
SHADOW = (95, 95, 95)


# ----- ROOM DISPLAY -----

# terrain
terrain_image_start_point = [50, 50]

# character
character_start_point = [300, 300]
start_health = 10
start_lvl = 1
character_attack_damage = 1
character_knockback = 2
character_speed = 5
frame_change_time = 20 / character_speed  # inverse proportion to make it more universal

# enemies
enemy_speed = 2.5     # other types of enemies will have different set of these values
enemy_health = 2
enemy_damage = 1
enemy_knockback_multiplier = 4
enemy_reward = 10
enemy_exp_for_kill = 4
enemy_frame_change_time = 5
enemy_health_bar_display_difference = [-2, 0]
enemy_health_bar_width = 9
enemy_health_bar_length = 54
enemy_health_text_center_difference = [28, 7]

# health
health_start_point = [430, 5]
health_bar_width = 20
health_bar_length = 120

# money
money_start_point = [510, 560]

# levels
level_start_point = [10, 5]
experience_bar_width = 10
experience_bar_length = 120

# changing room
distance_from_door = 50

# combat
attack_duration = 20
attack_interval = 70 + attack_duration

knockback_duration = 15     # also stun duration
immunity_duration = 30
rest_duration = 15
