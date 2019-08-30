import pygame

pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode([screen_width, screen_height])

main_font = 'freesansbold.ttf'

# START GAME


# ROMM DISPLAY ----------------------------------------

# terrain
terrain_image_start_point = [50, 50]

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

# fonts

money_font = pygame.font.Font(main_font, 25)
level_font = pygame.font.Font(main_font, 40)

# colors

GREEN = (0, 185, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
