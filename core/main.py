import pygame

from core.Inventory import Inventory
from worlds_management.Room import Room

pygame.init()

# ----- VARIABLES -----

# CAPTION
pygame.display.set_caption("Dan Jynce's Dungeons")

# TIME
clock = pygame.time.Clock()
time = 0

# INVENTORY
inventory = Inventory()

# ATTACK
attack_duration = 60
attack_interval = 60 + attack_duration

last_attack = 0

# MONEY
money = 0

# ROOM
room = Room()

# ----- MAIN LOOP -----
while True:

    clock.tick(60)

    if inventory.get_active():
        inventory.draw()
    else:
        room.draw_room()

    for e in pygame.event.get():
        # QUIT GAME
        if e.type == pygame.QUIT:
            exit(1)

        # KEYS MANAGEMENT
        for main_character in room.get_character().sprites():
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
        for main_character in room.get_character().sprites():
            main_character.move(room.get_walls(), time)  # move if not colliding with walls
            money += main_character.check_collisions(room.get_enemies())

        for enemy in room.get_enemies().sprites():
            enemy.move(time)

    pygame.display.flip()
    time += 1
