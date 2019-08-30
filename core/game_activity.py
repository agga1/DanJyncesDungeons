import pygame

from core.Inventory import Inventory
from worlds_management.WorldsManager import WorldsManager
from db.MyDatabase import MyDatabase
from core.menu_activity import menu_run


# ----- MAIN LOOP -----
def game_run(db, game_version):
    print(game_version)
    db.update_date(game_version)
    db.update_if_new(game_version)
    print(db.get_date(game_version))
    pygame.init()

    # database
    money = db.get_money(game_version)
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
            # quit game
            if e.type == pygame.QUIT:
                exit(1)

            # keys management
            for main_character in worlds_manager.get_character().sprites():
                if e.type == pygame.KEYDOWN:
                    # movement (saving information about keys being pressed)
                    if e.key == pygame.K_w:
                        main_character.set_key_clicked("top", True)
                    if e.key == pygame.K_s:
                        main_character.set_key_clicked("bottom", True)
                    if e.key == pygame.K_a:
                        main_character.set_key_clicked("left", True)
                    if e.key == pygame.K_d:
                        main_character.set_key_clicked("right", True)

                    # inventory
                    if e.key == pygame.K_i and not inventory.active:
                        inventory.activate()
                    elif e.key == pygame.K_i and inventory.active:
                        inventory.deactivate()

                    # start attacking
                    if e.key == pygame.K_SPACE and (time - last_attack > attack_interval or last_attack == 0):
                        last_attack = time
                        main_character.start_attack()

                # movement (velocity is multiplied by the values in the brackets: 0 - stop moving in that direction)
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_w:
                        main_character.set_key_clicked("top", False)
                    if e.key == pygame.K_s:
                        main_character.set_key_clicked("bottom", False)
                    if e.key == pygame.K_a:
                        main_character.set_key_clicked("left", False)
                    if e.key == pygame.K_d:
                        main_character.set_key_clicked("right", False)

                # stop attacking
                if main_character.get_is_attacking() and time - last_attack >= attack_duration:
                    main_character.stop_attack()

        if not inventory.active:
            for main_character in worlds_manager.get_character().sprites():
                # set character velocity
                if not main_character.get_stunned():
                    vertical_velocity = 0
                    if main_character.get_key_clicked("top") and main_character.get_key_clicked("bottom"):
                        vertical_velocity = 0
                    elif main_character.get_key_clicked("top"):
                        vertical_velocity = -1
                    elif main_character.get_key_clicked("bottom"):
                        vertical_velocity = 1

                    horizontal_velocity = 0
                    if main_character.get_key_clicked("left") and main_character.get_key_clicked("right"):
                        horizontal_velocity = 0
                    elif main_character.get_key_clicked("left"):
                        horizontal_velocity = -1
                    elif main_character.get_key_clicked("right"):
                        horizontal_velocity = 1

                    main_character.set_velocity([horizontal_velocity, vertical_velocity])

                # move if not colliding with walls
                main_character.move(worlds_manager.get_curr_world().get_curr_room().get_walls(), time)

                # colliding with enemies
                money_change = main_character.check_collisions(worlds_manager.get_curr_world().get_curr_room(), time)
                money += money_change
                # checking stun and immunity to enemies
                main_character.check_stun_and_immunity(time)

                # checking changing room
                worlds_manager.get_curr_world().check_room(main_character)

                # saving money to database
                if money_change != 0:
                    db.update_money(money, game_version)

            # enemies movement
            for enemy in worlds_manager.get_curr_world().get_curr_room().get_enemies().sprites():
                enemy.move(worlds_manager.get_character(), time)

        pygame.display.flip()
        time += 1

