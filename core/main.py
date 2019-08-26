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

# COLOURS
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# TIME
clock = pygame.time.Clock()

# IMAGES
character_image = pygame.image.load("../resources/main_character.png")
item_image = pygame.image.load("../resources/item.png")
enemy_image = pygame.image.load("../resources/enemy.png")
terrain_image = pygame.image.load("../resources/terrain.png")
terrain_border_image = pygame.image.load("../resources/terrain_border.png")

# MAIN CHARACTER
character_start_point = (300, 300)
character = Character.Character(character_start_point)

# INVENTORY
inventory = Inventory()

# HEALTH
health_start_point = (15, 15)

# MONEY
money = 0
money_start_point = (500, 15)
font = pygame.font.Font('freesansbold.ttf', 25)


# ----- FUNCTIONS -----
def terrain_display():
    screen.blit(terrain_image, (50, 50))


def wall_display():
    for i in range(0, 12):
        screen.blit(terrain_border_image, (50 * i, 0))
        screen.blit(terrain_border_image, (50 * i, 550))

    for i in range(0, 11):
        screen.blit(terrain_border_image, (0, 50 + 50 * i))
        screen.blit(terrain_border_image, (550, 50 + 50 * i))


def health_display():
    pygame.draw.rect(screen, RED, (health_start_point[0], health_start_point[1], 100, 20))


def money_display():
    money_text = font.render(str(money), True, YELLOW)
    screen.blit(money_text, money_start_point)


# ----- MAIN LOOP -----
while True:

    clock.tick(60)

    if inventory.active:
        inventory.draw()
    else:
        # TERRAIN
        screen.fill(WHITE)
        terrain_display()
        wall_display()
        health_display()
        money_display()
        screen.blit(character_image, (character.position_x, character.position_y))

    # KEYS MANAGEMENT & QUIT GAME
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit(1)
        if e.type == pygame.KEYDOWN:
            # movement
            if not inventory.active:
                if e.key == pygame.K_w:
                    character.change_velocity("up", character.speed)
                if e.key == pygame.K_s:
                    character.change_velocity("down", character.speed)
                if e.key == pygame.K_a:
                    character.change_velocity("left", character.speed)
                if e.key == pygame.K_d:
                    character.change_velocity("right", character.speed)

            # inventory
            if e.key == pygame.K_i and not inventory.active:
                inventory.activate()
                character.stop()
            elif e.key == pygame.K_i and inventory.active:
                inventory.deactivate()
                character.stop()

        if e.type == pygame.KEYUP:
            if not inventory.active:
                if e.key == pygame.K_w:
                    character.change_velocity("up", -1 * character.speed)
                if e.key == pygame.K_s:
                    character.change_velocity("down", -1 * character.speed)
                if e.key == pygame.K_a:
                    character.change_velocity("left", -1 * character.speed)
                if e.key == pygame.K_d:
                    character.change_velocity("right", -1 * character.speed)

    character.move()

    pygame.display.flip()
