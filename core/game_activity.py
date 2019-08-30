import pygame

from core.Inventory import Inventory
from worlds_management.WorldsManager import WorldsManager
from db.MyDatabase import MyDatabase
from core.menu_activity import menu_run


# ----- MAIN LOOP -----
def game_run(db):
    pygame.init()

    # database
    money = 0
    # ----- VARIABLES -----

    # TIME
    clock = pygame.time.Clock()
    time = 0

    # INVENTORY
    inventory = Inventory()

    # ATTACK
    attack_duration = 30
    attack_interval = 60 + attack_duration

    last_attack = 0

    # MONEY
    # money = 0

    # WORLDS MANAGER
    worlds_manager = WorldsManager()

    worlds_manager.game_start()

    while True:

        clock.tick(60)

        if inventory.get_active():
            inventory.draw()
        else:
            worlds_manager.draw(money)

        for e in pygame.event.get():
            # QUIT GAME
            if e.type == pygame.QUIT:
                exit(1)

            # KEYS MANAGEMENT
            for main_character in worlds_manager.get_character().sprites():
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

                    # start attacking
                    if e.key == pygame.K_SPACE and (time - last_attack > attack_interval or last_attack == 0):
                        last_attack = time
                        main_character.start_attack()

                # movement
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_w:
                        main_character.change_velocity([0, 1])
                    if e.key == pygame.K_s:
                        main_character.change_velocity([0, -1])
                    if e.key == pygame.K_a:
                        main_character.change_velocity([1, 0])
                    if e.key == pygame.K_d:
                        main_character.change_velocity([-1, 0])

                # stop attacking
                if main_character.get_is_attacking() and time - last_attack >= attack_duration:
                    main_character.stop_attack()

        if not inventory.active:
            for main_character in worlds_manager.get_character().sprites():
                # move if not colliding with walls
                main_character.move(worlds_manager.get_curr_world().get_curr_room().get_walls(), time)

                # colliding with enemies
                money += main_character.check_collisions(worlds_manager.get_curr_world().get_curr_room())

                # checking changing room
                worlds_manager.get_curr_world().check_room(main_character)

                # saving money to database
                db.update_money(money)

                for enemy in worlds_manager.get_curr_world().get_curr_room().get_enemies().sprites():
                    enemy.move(main_character, time)

        pygame.display.flip()
        time += 1

        if time % 30 == 0:
            print(db.get_money())
            print("version ", db.get_version())
