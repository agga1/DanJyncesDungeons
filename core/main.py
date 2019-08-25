import pygame
from character import Character
from core.Inventory import Inventory

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

# COLOURS
WHITE = (255, 255, 255)
BROWN = (150, 75, 0)

# POINTS
character_start_point = (300, 300)

# MAIN CHARACTER
character = Character.Character(character_start_point)
character_speed = 7

# INVENTORY
inventory = Inventory()


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

    clock.tick(60)

    if inventory.active:
        screen.fill(BROWN)
    else:
        # TERRAIN
        screen.fill(WHITE)
        screen.blit(character_image, (character.position_x, character.position_y))
        wall_display()

    # KEYS MANAGEMENT & QUIT GAME
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit(1)
        if e.type == pygame.KEYDOWN:
            # movement
            if not inventory.active:
                if e.key == pygame.K_w:
                    character.change_velocity("up", 1, character_speed)
                if e.key == pygame.K_s:
                    character.change_velocity("down", 1, character_speed)
                if e.key == pygame.K_a:
                    character.change_velocity("left", 1, character_speed)
                if e.key == pygame.K_d:
                    character.change_velocity("right", 1, character_speed)

            # inventory
            if e.key == pygame.K_i and not inventory.active:
                inventory.activate()
            elif e.key == pygame.K_i and inventory.active:
                inventory.deactivate()

        if e.type == pygame.KEYUP:
            if not inventory.active:
                if e.key == pygame.K_w:
                    character.change_velocity("up", -1, character_speed)
                if e.key == pygame.K_s:
                    character.change_velocity("down", -1, character_speed)
                if e.key == pygame.K_a:
                    character.change_velocity("left", -1, character_speed)
                if e.key == pygame.K_d:
                    character.change_velocity("right", -1, character_speed)

    character.move()

    pygame.display.flip()
