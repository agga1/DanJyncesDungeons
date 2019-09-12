"""Contains universally used gui features like pop-ups, frame freeze"""

from management_and_config.configurations import *
from resources.image_manager import get_heart_image, get_coin_image, get_attack_ready_image, \
    get_attack_not_ready_image, get_stats_bar_image, get_upgrade_stat_image, get_key_grey_image, get_key_blue_image, \
    get_key_green_image, get_key_yellow_image


def show_popup(text_string):
    font = pygame.font.Font(main_font, font_size_info)
    text = font.render(text_string, True, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (screen_width / 2, screen_height / 2)
    # shadow behind popup
    bg_rect_shadow = pygame.rect.Rect(0, 0, text_rect.width + 10, text_rect.height + 10)
    bg_rect_shadow.center = (screen_width / 2 + 5, screen_height / 2 + 5)
    pygame.draw.rect(screen, SHADOW, bg_rect_shadow)
    # popup window
    bg_rect = pygame.rect.Rect(0, 0, text_rect.width + 10, text_rect.height + 10)
    bg_rect.center = (screen_width / 2, screen_height / 2)
    pygame.draw.rect(screen, WHITE, bg_rect)
    screen.blit(text, text_rect)
    pygame.display.flip()


def freeze_clock(time_in_sek):
    # clock = pygame.time.Clock()   # it is defined in configurations
    time_in_sek *= 60
    time_passed = 0
    while time_passed <= time_in_sek:
        clock.tick(60)
        time_passed += 1


def health_display(character):
    heart_image = get_heart_image()

    screen.blit(heart_image, health_start_point)

    pygame.draw.rect(screen, RED,
                     [health_start_point[0] + 35, health_start_point[1], health_bar_length,
                      health_bar_width], 1)

    pygame.draw.rect(screen, RED, [health_start_point[0] + 35, health_start_point[1],
                                   character.health * health_bar_length / character.max_health,
                                   health_bar_width])


def mana_display(character):
    # mana_image = get_mana_image()

    # screen.blit(mana_image, mana_start_point) TODO

    pygame.draw.rect(screen, BLUE,
                     [mana_start_point[0] + 35, mana_start_point[1], mana_bar_length,
                      mana_bar_width], 1)

    if character.max_mana == 0:  # when no mana yet to not dividing by 0
        pygame.draw.rect(screen, BLUE, [mana_start_point[0] + 35, mana_start_point[1],
                                        character.mana * mana_bar_length, mana_bar_width])

    else:
        pygame.draw.rect(screen, BLUE, [mana_start_point[0] + 35, mana_start_point[1],
                                        character.mana * mana_bar_length / character.max_mana,
                                        mana_bar_width])


def level_display(character):
    level_number = level_font.render(str(character.level), True, GREEN)
    screen.blit(level_number, level_start_point)

    pygame.draw.rect(screen, GREEN,
                     [level_start_point[0] + 35, level_start_point[1] + 17, experience_bar_length,
                      experience_bar_width], 1)

    pygame.draw.rect(screen, GREEN, [level_start_point[0] + 35, level_start_point[1] + 17,
                                     character.exp * experience_bar_length / character.to_next_level_exp,
                                     experience_bar_width])


def keys_display(character):
    key_grey_image = get_key_grey_image()
    key_blue_image = get_key_blue_image()
    key_green_image = get_key_green_image()
    key_yellow_image = get_key_yellow_image()

    screen.blit(key_grey_image, key_grey_start_point)
    screen.blit(key_blue_image, key_blue_start_point)
    screen.blit(key_green_image, key_green_start_point)
    screen.blit(key_yellow_image, key_yellow_start_point)

    key_grey_number = stats_font.render(str(character.keys["grey"]), True, BLACK)
    key_blue_number = stats_font.render(str(character.keys["blue"]), True, BLACK)
    key_green_number = stats_font.render(str(character.keys["green"]), True, BLACK)
    key_yellow_number = stats_font.render(str(character.keys["yellow"]), True, BLACK)

    screen.blit(key_grey_number,
                [key_grey_start_point[0] + keys_number_dist[0], key_grey_start_point[1] + keys_number_dist[1]])
    screen.blit(key_blue_number,
                [key_blue_start_point[0] + keys_number_dist[0], key_blue_start_point[1] + keys_number_dist[1]])
    screen.blit(key_green_number,
                [key_green_start_point[0] + keys_number_dist[0], key_green_start_point[1] + keys_number_dist[1]])
    screen.blit(key_yellow_number,
                [key_yellow_start_point[0] + keys_number_dist[0], key_yellow_start_point[1] + keys_number_dist[1]])


def money_display(character):
    coin_image = get_coin_image()

    money_number = money_font.render(str(character.money), True, YELLOW)
    screen.blit(coin_image, money_start_point)
    screen.blit(money_number, [money_start_point[0] + 30, money_start_point[1] - 5])


def display_stats_bar(character):
    bg_image = get_stats_bar_image()
    screen.blit(bg_image, [square_screen_width, 0])
    health_display(character)
    mana_display(character)
    level_display(character)
    keys_display(character)
    money_display(character)


def display_skill_tree_stats_bar(character):
    # bar color
    bg_image = get_stats_bar_image()
    screen.blit(bg_image, [square_screen_width, 0])

    # level
    level_text = level_font.render("level " + str(character.level), True, GREEN)
    level_text_rect = level_text.get_rect()
    level_text_rect.center = st_level_text_center
    screen.blit(level_text, level_text_rect)

    # exp variables
    exp = character.exp
    max_exp = character.to_next_level_exp

    # exp bar
    pygame.draw.rect(screen, GREEN,
                     [st_experience_bar_start_point[0], st_experience_bar_start_point[1], st_experience_bar_length,
                      st_experience_bar_width], 1)

    pygame.draw.rect(screen, GREEN, [st_experience_bar_start_point[0], st_experience_bar_start_point[1],
                                     exp * st_experience_bar_length / max_exp, st_experience_bar_width])

    # text: current exp / max exp in the center of exp bar
    exp_text = st_exp_font.render(str(exp) + "/" + str(max_exp), True, WHITE)
    exp_text_rect = exp_text.get_rect()
    exp_text_rect.center = exp_text_center
    screen.blit(exp_text, exp_text_rect)

    # skill points
    skill_points_text = skill_points_font.render("skill points: " + str(character.skill_points), True, GREEN)
    screen.blit(skill_points_text, st_skill_points_text_start_point)

    # attack damage
    attack_damage_text = stats_font.render("attack damage: " + str(character.attack_damage), True, WHITE)
    screen.blit(attack_damage_text, st_attack_damage_text_start_point)

    # attack speed
    attack_speed_text = stats_font.render("attack speed: " + str(character.attack_speed), True, WHITE)
    screen.blit(attack_speed_text, st_attack_speed_text_start_point)

    # critical chance (int() to avoid displaying 10.0, 20.0 etc - we want 10, 20 etc instead)
    crit_chance_text = stats_font.render(
        "critical chance: " + str(int(character.critical_attack_chance * 100)) + "%", True, WHITE)
    screen.blit(crit_chance_text, st_critical_attack_chance_text_start_point)

    # health
    health_text = stats_font.render("hit points: " + str(character.max_health), True, WHITE)
    screen.blit(health_text, st_health_text_start_point)

    # mana
    mana_text = stats_font.render("mana points: " + str(character.max_mana), True, WHITE)
    screen.blit(mana_text, st_mana_text_start_point)

    if character.skill_points > 0:
        plus_image = get_upgrade_stat_image()

        screen.blit(plus_image, st_attack_damage_plus_start_point)
        if character.attack_speed < max_attack_speed:
            screen.blit(plus_image, st_attack_speed_plus_start_point)
        if character.critical_attack_chance < max_critical_attack_chance:
            screen.blit(plus_image, st_critical_attack_chance_plus_start_point)
        screen.blit(plus_image, st_health_plus_start_point)
        screen.blit(plus_image, st_mana_plus_start_point)


def attack_ready_display(ready):
    attack_ready_image = get_attack_ready_image() if ready else get_attack_not_ready_image()
    screen.blit(attack_ready_image, attack_ready_coord)
