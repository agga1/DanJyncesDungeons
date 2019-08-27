import pygame
import math
import os


def find_angle(directions):
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
