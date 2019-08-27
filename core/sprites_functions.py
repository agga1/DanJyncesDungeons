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
    for frame in os.listdir(directory):
        images.append(pygame.image.load(frame))


def animate(images, time, start_time, speed):
    curr_frame = math.floor((time - start_time)/speed) % len(images)

    return images[curr_frame]
