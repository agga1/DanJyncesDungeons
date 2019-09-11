""" Contains all hardcoded gui values (fonts, colors, coord)"""
import pygame

pygame.init()

# ----- GENERAL -----
square_screen_width = 600
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])

clock = pygame.time.Clock()

# fonts
main_font = 'freesansbold.ttf'
description_font = '../resources/fonts/ARJULIAN.ttf'
font_size_info = 14  # in pop u p windows
font_size_bar = 12
font_size_money = 25
font_size_level = 40
font_size_st_exp = 20
font_size_st_skill_points = 25
font_size_st_stats = 17
font_size_enemy_health = 15

money_font = pygame.font.Font(description_font, font_size_money)
level_font = pygame.font.Font(description_font, font_size_level)
st_exp_font = pygame.font.Font(description_font, font_size_st_exp)
skill_points_font = pygame.font.Font(description_font, font_size_st_skill_points)
stats_font = pygame.font.Font(description_font, font_size_st_stats)
enemy_health_font = pygame.font.Font(description_font, font_size_enemy_health)

# colors
RED = (255, 0, 0)
GREEN = (0, 185, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
PINK = (255, 150, 150)
BROWN = (150, 75, 0)
SHADOW = (95, 95, 95)
STATS_BAR_COLOR = (136, 94, 44)


# ----- ROOM -----
# terrain
terrain_image_start_point = [50, 50]

# attack ready light
attack_ready_coord = [5, 5]

# changing room
distance_from_door = 50


# ----- SPRITES -----
sprite_size = [50, 50]

# character
character_start_point = [300, 300]
start_health = 10
start_lvl = 1

character_start_attack_damage = 1
character_start_attack_speed = 0.7
character_start_critical_attack_chance = 0.0

character_knockback = 2

character_speed = 5
frame_change_time = 20 / character_speed  # inverse proportion to make it more universal

# enemies
enemy_speed = 2.5
enemy_health = 2
enemy_damage = 1
enemy_knockback_multiplier = 2
enemy_frame_change_time = 5
enemy_health_bar_display_difference = [-2, 0]
enemy_health_bar_width = 9
enemy_health_bar_length = 54
enemy_health_text_center_difference = [28, 5]
enemy_money_drop_range = [1, 3]
enemy_exp_drop = 4

bat_speed = 2.5
bat_health = 2
bat_damage = 1
bat_knockback = 1
bat_frame_change_time = 5
bat_health_bar_display_difference = [-2, 0]
bat_health_bar_width = 9
bat_health_bar_length = 54
bat_health_text_center_difference = [28, 5]
bat_money_drop_range = [1, 3]
bat_exp_drop = 4

hedgehog_speed = 2
hedgehog_health = 3
hedgehog_damage = 1
hedgehog_knockback = 1
hedgehog_frame_change_time = 12
hedgehog_health_bar_display_difference = [-2, 0]
hedgehog_health_bar_width = 9
hedgehog_health_bar_length = 54
hedgehog_health_text_center_difference = [28, 5]
hedgehog_money_drop_range = [1, 2]
hedgehog_exp_drop = 3


# dropped items
drop_speed = 0.5
drop_moving_distance = 150

pick_up_time = 25

# ----- STATS DISPLAY -----
# stats bar
stats_bar_rect = [600, 0, 300, 600]

# health
health_start_point = [610, 230]
health_bar_width = 20
health_bar_length = 140

# mana
mana_start_point = [610, 270]
mana_bar_width = 20
mana_bar_length = 140

# levels
level_start_point = [610, 340]
experience_bar_width = 10
experience_bar_length = 140

# money
money_start_point = [610, 560]


# ----- SKILL TREE DISPLAY -----
st_level_text_center = [700, 70]

st_experience_bar_start_point = [620, 120]
st_experience_bar_width = 30
st_experience_bar_length = 160
exp_text_center = [700, 135]

left_margin = 608
st_skill_points_text_start_point = [left_margin, 240]

st_attack_damage_text_start_point = [left_margin, 320]
st_attack_damage_plus_start_point = [778, 320]

st_attack_speed_text_start_point = [left_margin, 370]
st_attack_speed_plus_start_point = [778, 370]

st_critical_attack_chance_text_start_point = [left_margin, 420]
st_critical_attack_chance_plus_start_point = [778, 420]

st_health_text_start_point = [left_margin, 470]
st_health_plus_start_point = [778, 470]

st_mana_text_start_point = [left_margin, 520]
st_mana_plus_start_point = [778, 520]

# ----- UPGRADING STATS -----
upgrade_attack_damage = 1
upgrade_attack_speed = 0.1
upgrade_critical_attack_chance = 0.1
upgrade_health = 5
upgrade_mana = 10

max_attack_speed = 2.0
max_critical_attack_chance = 1.0

# ----- COMBAT -----
# timers
attack_duration = 20

# after attack
knockback_duration = 15     # also stun duration
immunity_duration = 30
rest_duration = 15
