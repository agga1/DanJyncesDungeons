import pygame

pygame.init()

# ----- VARIABLES -----

# SCREEN
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Dan Jynce's Dungeons")

# TIME
clock = pygame.time.Clock()

# IMAGES
character_image = pygame.image.load("../resources/main_character.png")
item_image = pygame.image.load("../resources/item.png")
enemy_image = pygame.image.load("../resources/enemy.png")
terrain_border_image = pygame.image.load("../resources/terrain_border.png")

# POINTS
character_start_point = (300, 300)


# ----- FUNCTIONS -----
def wall_display():
    for i in range(0, 12):
        screen.blit(terrain_border_image, (50 * i, 0))
        screen.blit(terrain_border_image, (50 * i, 550))

    for i in range(0, 11):
        screen.blit(terrain_border_image, (0, 50 + 50 * i))
        screen.blit(terrain_border_image, (550, 50 + 50 * i))


# ----- MAIN LOOP -----
while True:

    clock.tick(90)

    # TERRAIN
    screen.fill((255, 255, 255))
    screen.blit(character_image, character_start_point)
    wall_display()

    # QUIT GAME
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit(1)

    pygame.display.flip()
