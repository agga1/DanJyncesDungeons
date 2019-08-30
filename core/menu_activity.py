"""Main menu activity, main file running on startup"""
import pygame
from resources import image_manager
from core.configurations import *
pygame.init()

screen = pygame.display.set_mode([screen_width, screen_height])
clock = pygame.time.Clock()


def menu_run(save_status):
    while True:

        clock.tick(60)
        buttons = menu_draw(save_status)  # (A, B, C, del_A, del_B, del_C)

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
                if not save_status[0] and buttons[3].collidepoint(e.pos):
                    print('deleting first save...')
                    break
                if not save_status[1] and buttons[4].collidepoint(e.pos):
                    print('deleting 2nd save...')
                    break
                if not save_status[2] and buttons[5].collidepoint(e.pos):
                    print('deleting 3rd save...')
                    break
                if buttons[0].collidepoint(e.pos):
                    return 1
                if buttons[1].collidepoint(e.pos):
                    return 2
                if buttons[2].collidepoint(e.pos):
                    return 3

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
