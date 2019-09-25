from management_and_config.display_functions import attack_ready_display
from worlds_management.WorldsManager import WorldsManager
from management_and_config.object_save import *
from core.inventory_activity import inventory_run
from core.skill_tree_activity import skill_tree_run


def game_run(db, memory_slot):
    # DATABASE
    db.update_date(memory_slot)
    db.update_if_new(memory_slot)
    db.set_row_id(memory_slot)
    pygame.init()

    # TIME
    time = 0

    can_attack_time = 0
    stop_attack_time = 0

    # WORLDS MANAGER
    character = pygame.sprite.Group()
    main_character = load_character(db)
    character.add(main_character)
    worlds_manager = WorldsManager(character, db)
    worlds_manager.game_start()

    # CURRENT DISPLAY MANAGEMENT
    curr_display = "game"

    while True:
        clock.tick(60)

        for main_character in worlds_manager.character.sprites():
            # changing display to inventory or skill tree if activated
            if curr_display != "game":
                while curr_display != "game":
                    if curr_display == "inventory":
                        curr_display = inventory_run(main_character)
                    elif curr_display == "skill tree":
                        curr_display = skill_tree_run(main_character)

                # stopping character movement to avoid bugs
                main_character.set_key_clicked("top", False)
                main_character.set_key_clicked("bottom", False)
                main_character.set_key_clicked("left", False)
                main_character.set_key_clicked("right", False)

            # drawing all elements of the display
            worlds_manager.draw()
            if time > can_attack_time:
                attack_ready_display(True)
            else:
                attack_ready_display(False)

            for e in pygame.event.get():
                # quit game
                if e.type == pygame.QUIT:
                    exit(1)

                # keys management
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

                    # start attacking
                    if e.key == pygame.K_SPACE and time > can_attack_time:
                        stop_attack_time = time + attack_duration
                        can_attack_time = int(time + 60/main_character.attack_speed)
                        main_character.start_attack()

                    # inventory
                    if e.key == pygame.K_i:
                        curr_display = "inventory"

                    # skill tree
                    if e.key == pygame.K_k:
                        curr_display = "skill tree"

                    # open door or enter shop
                    if e.key == pygame.K_e:
                        if not worlds_manager.curr_world.curr_room.open_door(main_character):
                            if worlds_manager.curr_world.curr_room.enter_shop(main_character):
                                print("enter shop")

                # movement (saving information about keys stop being pressed)
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
            if main_character.is_attacking and time == stop_attack_time:
                main_character.stop_attack()

            # set character velocity
            if not main_character.stunned:
                vertical_velocity = 0
                if main_character.key_clicked["top"] and main_character.key_clicked["bottom"]:
                    vertical_velocity = 0
                elif main_character.key_clicked["top"]:
                    vertical_velocity = -1
                elif main_character.key_clicked["bottom"]:
                    vertical_velocity = 1

                horizontal_velocity = 0
                if main_character.key_clicked["left"] and main_character.key_clicked["right"]:
                    horizontal_velocity = 0
                elif main_character.key_clicked["left"]:
                    horizontal_velocity = -1
                elif main_character.key_clicked["right"]:
                    horizontal_velocity = 1

                main_character.set_velocity([horizontal_velocity, vertical_velocity])

            # move if not colliding with walls and check collision with drop
            main_character.move(worlds_manager.curr_world.curr_room, time)

            # colliding with enemies
            main_character.check_collisions(worlds_manager.curr_world.curr_room, time)

            # checking stun and immunity to enemies
            main_character.check_stun_and_immunity(time)

            # checking changing room
            worlds_manager.curr_world.check_room(main_character)

            # enemies movement
            for enemy in worlds_manager.curr_world.curr_room.enemies.sprites():
                enemy.move(worlds_manager, time)

            # drop moving towards character
            for drop in worlds_manager.curr_world.curr_room.dropped_items.sprites():
                drop.move_towards_character(main_character, time)

        pygame.display.flip()
        time += 1
