import pygame
from character.Character import Character
from core.Inventory import Inventory
from enemies.Enemy import Enemy
from obstacles.Wall import Wall

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
character_start_point = [300, 300]

character = pygame.sprite.Group()
character.add(Character(character_start_point, character_image))

# ENEMIES
enemy_start_point = [550, 550]

enemies = pygame.sprite.Group()
enemies.add(Enemy(enemy_start_point, enemy_image))

# WALLS
walls = pygame.sprite.Group()
for i in range(0, 12):      # it will be in room class in the future
    walls.add(Wall([50 * i, 0], terrain_border_image))
    walls.add(Wall([50 * i, 550], terrain_border_image))
for i in range(0, 11):
    walls.add(Wall([0, 50 + 50 * i], terrain_border_image))
    walls.add(Wall([550, 50 + 50 * i], terrain_border_image))

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
    walls.draw(screen)


def character_display():
    character.draw(screen)


def enemy_display():
    enemies.draw(screen)


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
        character_display()
        enemy_display()

    for main_character in character.sprites():
        # KEYS MANAGEMENT & QUIT GAME
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit(1)
            if e.type == pygame.KEYDOWN:
                # movement
                if e.key == pygame.K_w:
                    main_character.change_velocity([0, -1])
                if e.key == pygame.K_s:
                    main_character.change_velocity([0, 1])
                if e.key == pygame.K_a:
                    main_character.change_velocity([-1, 0])
                if e.key == pygame.K_d:
                    main_character.change_velocity([1, 0])

                # inventory
                if e.key == pygame.K_i and not inventory.active:
                    inventory.activate()
                elif e.key == pygame.K_i and inventory.active:
                    inventory.deactivate()

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_w:
                    main_character.change_velocity([0, 1])
                if e.key == pygame.K_s:
                    main_character.change_velocity([0, -1])
                if e.key == pygame.K_a:
                    main_character.change_velocity([1, 0])
                if e.key == pygame.K_d:
                    main_character.change_velocity([-1, 0])

    if not inventory.active:
        for main_character in character.sprites():
            main_character.move(walls)  # move if not colliding with walls

        for enemy in enemies.sprites():
            enemy.move()

    pygame.display.flip()
