import pygame

from character.Character import Character
from enemies.Enemy import Enemy
from core.Inventory import Inventory
from core import sprites_functions
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
time = 0

# IMAGES
character_rest_image = pygame.image.load("../resources/character_walk/character_walk_0.png")
character_walk_images = sprites_functions.connect_frames("../resources/character_walk")

item_image = pygame.image.load("../resources/item.png")
enemy_image = pygame.image.load("../resources/enemy.png")
terrain_image = pygame.image.load("../resources/terrain.png")
terrain_border_image = pygame.image.load("../resources/terrain_border.png")
heart_image = pygame.image.load("../resources/heart.png")
coin_image = pygame.image.load("../resources/coin.png")

# MAIN CHARACTER
character_start_point = [300, 300]  # it will be in the room class in the future

character = pygame.sprite.Group()
character.add(Character(character_start_point, character_rest_image, character_walk_images))

# ENEMIES
enemy_start_point = [450, 450]  # it will be in the room class in the future

enemies = pygame.sprite.Group()
enemies.add(Enemy(enemy_start_point, enemy_image))

# WALLS
walls = pygame.sprite.Group()
for i in range(0, 12):  # it will be in the room class in the future
    walls.add(Wall([50 * i, 0], terrain_border_image))
    walls.add(Wall([50 * i, 550], terrain_border_image))
for i in range(0, 11):
    walls.add(Wall([0, 50 + 50 * i], terrain_border_image))
    walls.add(Wall([550, 50 + 50 * i], terrain_border_image))

# INVENTORY
inventory = Inventory()

# ATTACK
attack_duration = 60
attack_interval = 60 + attack_duration

last_attack = 0

# HEALTH
health_start_point = (10, 5)
health_bar_width = 20
health_bar_length = 120

# MONEY
money = 0
money_start_point = (510, 15)
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
    screen.blit(heart_image, health_start_point)

    for player in character.sprites():
        health = player.get_health()
        max_health = player.get_max_health()
        pygame.draw.rect(screen, RED,
                         [health_start_point[0] + 35, health_start_point[1], health_bar_length, health_bar_width], 1)

        pygame.draw.rect(screen, RED, [health_start_point[0] + 35, health_start_point[1],
                                       health * health_bar_length / max_health, health_bar_width])


def money_display():
    money_text = font.render(str(money), True, YELLOW)
    screen.blit(coin_image, money_start_point)
    screen.blit(money_text, [money_start_point[0] + 25, money_start_point[1]])


# ----- MAIN LOOP -----
while True:

    clock.tick(60)
    time += 1

    if inventory.get_active():
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

    for e in pygame.event.get():
        # QUIT GAME
        if e.type == pygame.QUIT:
            exit(1)

        # KEYS MANAGEMENT
        for main_character in character.sprites():
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

                # attack
                if e.key == pygame.K_SPACE and (time - last_attack > attack_interval or last_attack == 0):
                    last_attack = time
                    main_character.start_attack()
                if main_character.get_is_attacking() and time - last_attack >= attack_duration:
                    main_character.stop_attack()

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
            main_character.move(walls, time)  # move if not colliding with walls
            money += main_character.check_collisions(enemies)

        for enemy in enemies.sprites():
            enemy.move()

    pygame.display.flip()
