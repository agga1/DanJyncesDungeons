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
        buttons = menu_draw(save_status)

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
                if buttons[0].collidepoint(e.pos):
                    return 1
                if buttons[1].collidepoint(e.pos):
                    return 2
                if buttons[2].collidepoint(e.pos):
                    return 3



        pygame.display.flip()


def menu_draw(save_status):
    screen.fill(WHITE)
    bg_image = image_manager.get_bg()
    screen.blit(bg_image, [0, 0])

    # draw background of buttons---------------------------
    btn_image = image_manager.get_btn()
    btn_width = btn_image.get_size()[0]
    btn_height = btn_image.get_size()[1]
    btn_a_rect = btn_image.get_rect()
    btn_a_rect.center = (screen_width/2, screen_height*4/8)
    screen.blit(btn_image, btn_a_rect)
    btn_b_rect = btn_image.get_rect()
    btn_b_rect.center = (screen_width / 2, screen_height * 5/8)
    screen.blit(btn_image, btn_b_rect)
    btn_c_rect = btn_image.get_rect()
    btn_c_rect.center = (screen_width / 2, screen_height * 6/8)
    screen.blit(btn_image, btn_c_rect)

    draw_btn_text(save_status[0], btn_a_rect, 'A.')
    draw_btn_text(save_status[1], btn_b_rect, 'B.')
    draw_btn_text(save_status[2], btn_c_rect, 'C.')

    return [btn_a_rect, btn_b_rect, btn_c_rect]


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
