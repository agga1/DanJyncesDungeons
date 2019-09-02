"""Main menu activity, main file running on startup"""
from resources import image_manager
from management_and_config.configurations import *
from management_and_config.display_functions import *
pygame.init()


def get_save_status(db):
    return [db.get_if_new(1), db.get_if_new(2), db.get_if_new(3)]


def menu_run(db):
    # info if 1st, 2nd and 3rd slot are new or have been previously saved
    save_status = get_save_status(db)
    buttons = menu_draw(save_status)  # (A, B, C, del_A, del_B, del_C)

    while True:

        clock.tick(60)

        for e in pygame.event.get():
            # QUIT GAME
            if e.type == pygame.QUIT:
                exit(1)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    return 1
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_a:
                    return 1
                if e.key == pygame.K_b:
                    return 2
                if e.key == pygame.K_c:
                    return 3
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                i = 0
                for new_save in save_status:
                    if not new_save and buttons[i+len(save_status)].collidepoint(e.pos):
                        print('deleting save...')
                        safe_delete(db, i+1)
                        # update save status and components to be displayed
                        save_status = get_save_status(db)
                        buttons = menu_draw(save_status)  # (A, B, C, del_A, del_B, del_C)
                        break
                    elif buttons[i].collidepoint(e.pos):  # only if delete not pressed should you enter a game during this event
                        return i+1
                    i += 1

        pygame.display.flip()


def safe_delete(db, row_id):
    if confirm_delete_draw():
        db.reset_row(row_id)


def confirm_delete_draw():  # return 0 - do delete, 1 - dont delete
    show_popup("Are you sure you want to delete this save? (y/n)")

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for e in pygame.event.get():
            # QUIT GAME
            if e.type == pygame.QUIT:
                exit(1)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    return 0
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_y:
                    return 1
                if e.key == pygame.K_n:
                    return 0

        pygame.display.flip()


def menu_draw(save_status):  # (?, ?, ?) 1 = new game, 0 = saved game
    screen.fill(WHITE)
    bg_image = image_manager.get_bg()
    screen.blit(bg_image, [0, 0])

    # draw background of buttons---------------------------
    btn_image = image_manager.get_btn()

    btn_a_rect = btn_image.get_rect()
    btn_a_rect.center = (screen_width/2, screen_height*4/8)
    screen.blit(btn_image, btn_a_rect)

    btn_b_rect = btn_image.get_rect()
    btn_b_rect.center = (screen_width / 2, screen_height * 5/8)
    screen.blit(btn_image, btn_b_rect)

    btn_c_rect = btn_image.get_rect()
    btn_c_rect.center = (screen_width / 2, screen_height * 6/8)
    screen.blit(btn_image, btn_c_rect)

    # draw button texts ------------------------------------
    draw_btn_text(save_status[0], btn_a_rect, 'A.')
    draw_btn_text(save_status[1], btn_b_rect, 'B.')
    draw_btn_text(save_status[2], btn_c_rect, 'C.')

    # draw delete buttons ---------------------------------------
    del_a_rect = draw_delete(save_status[0], [btn_a_rect[0] + btn_a_rect.width, btn_a_rect[1] + 5])
    del_b_rect = draw_delete(save_status[1], [btn_b_rect[0] + btn_b_rect.width, btn_b_rect[1] + 5])
    del_c_rect = draw_delete(save_status[2], [btn_c_rect[0] + btn_c_rect.width, btn_c_rect[1] + 5])

    return [btn_a_rect, btn_b_rect, btn_c_rect, del_a_rect, del_b_rect, del_c_rect]


def draw_btn_text(if_new, btn_rect, letter):
    font = pygame.font.Font(main_font, 22)
    if if_new:
        text_string = letter + ' New Game'
        btn_text = font.render(text_string, True, YELLOW)
    else:
        text_string = letter + ' Saved Game'
        btn_text = font.render(text_string, True, YELLOW)
    text_rect = btn_text.get_rect()
    text_rect.center = btn_rect.center
    screen.blit(btn_text, text_rect)


def draw_delete(dont_display, coord):
    btn_delete_image = image_manager.get_delete()
    btn_rect = btn_delete_image.get_rect()
    btn_rect.center = coord
    if not dont_display:
        screen.blit(btn_delete_image, btn_rect)
    return btn_rect
