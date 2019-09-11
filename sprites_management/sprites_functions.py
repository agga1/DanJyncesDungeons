""" Collection of functions shared between different sprites """

import pygame
import math
import os
import random

from management_and_config.configurations import sprite_size


# ----- ANIMATIONS -----
def find_character_angle(directions):
    if directions == [0, 0]:
        return 0
    if directions[0] == 0:
        if directions[1] > 0:
            return 0
        return 180
    if directions[1] == 0:
        if directions[0] > 0:
            return 90
        return 270
    if directions[0] > 0:
        if directions[1] > 0:
            return 45
        return 135
    if directions[1] > 0:
        return 315
    return 225


def connect_frames(directory):
    images = []

    frames = os.listdir(directory)
    frames.sort()   # To ensure alphabetical order

    for frame in frames:
        next_frame = pygame.image.load(directory + "/" + frame)
        images.append(next_frame)

    return images


def animate(images, curr_time, start_time, speed):
    curr_frame = math.floor((curr_time - start_time)/speed) % len(images)

    return images[curr_frame]


# ----- MATHS -----
def calculate_arctan(direction):
    """ calculating arcus tangens """
    if direction[0] != 0:
        angle = math.atan(direction[1] / direction[0])
    elif direction[1] > 0:
        angle = math.pi / 2
    else:
        angle = math.pi * 3 / 2

    return angle


def set_velocity_in_given_direction(direction, speed):
    """ calculating angle and using it to calculate velocity """

    angle = calculate_arctan(direction)

    # setting velocity
    if direction[0] >= 0:
        return [-1 * speed * math.cos(angle), -1 * speed * math.sin(angle)]
    else:
        return [speed * math.cos(angle), speed * math.sin(angle)]


def calculate_knockback(aggressor, victim):
    # choosing direction to make the biggest distance between aggressor and victim
    aggressor_position = [aggressor.get_position()[0] + sprite_size[0], aggressor.get_position()[1] + sprite_size[1]]
    victim_position = [victim.get_position()[0] + sprite_size[0], victim.get_position()[1] + sprite_size[1]]
    knockback_direction = [aggressor_position[0] - victim_position[0], aggressor_position[1] - victim_position[1]]

    knockback = aggressor.knockback

    # setting velocity
    velocity = set_velocity_in_given_direction(knockback_direction, victim.speed)

    # multiplying by knockback
    return [velocity[0] * knockback, velocity[1] * knockback]


def calculate_to_next_level_exp(level):
    return 6 + 4*level


def decide_critical_attack(chance):
    random_number = random.randrange(10)
    if random_number < int(round(chance, 1) * 10):
        return True
    else:
        return False
