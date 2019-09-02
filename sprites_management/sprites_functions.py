""" Collection of functions shared between different sprites """

import pygame
import math
import os


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
def calculate_arctan(values):
    if values[0] != 0:
        angle = math.atan(values[1] / values[0])
    elif values[1] > 0:
        angle = math.pi / 2
    else:
        angle = math.pi * 3 / 2

    return angle


def calculate_to_next_level_exp(level):
    return 6 + 4*level

