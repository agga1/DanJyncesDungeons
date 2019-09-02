import pygame

from management_and_config.configurations import main_font, font_size_info, BLACK, screen_height, screen_width, screen, \
    SHADOW, WHITE


def show_popup(text_string):
    font = pygame.font.Font(main_font, font_size_info)
    text = font.render(text_string, True, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (screen_height / 2, screen_width / 2)
    # shadow behind popup
    bg_rect_shadow = pygame.rect.Rect(0, 0, text_rect.width + 10, text_rect.height + 10)
    bg_rect_shadow.center = (screen_height / 2 + 5, screen_width / 2 + 5)
    pygame.draw.rect(screen, SHADOW, bg_rect_shadow)
    # popup window
    bg_rect = pygame.rect.Rect(0, 0, text_rect.width + 10, text_rect.height + 10)
    bg_rect.center = (screen_height / 2, screen_width / 2)
    pygame.draw.rect(screen, WHITE, bg_rect)
    screen.blit(text, text_rect)
    pygame.display.flip()


def freeze_clock(time_in_sek):
    clock = pygame.time.Clock()
    time_in_sek *= 60
    time_passed = 0
    while time_passed <= time_in_sek:
        clock.tick(60)
        time_passed += 1
