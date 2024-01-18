import random

import pygame

SIZE = WIDTH, HEIGHT = 1000, 650
FPS = 30

CACTUS_APPEARANCE_EVENT = 234
CACTUS_DELAY = range(100, 2000)


def update_cactus_event():
    pygame.time.set_timer(CACTUS_APPEARANCE_EVENT,
                          random.choice(CACTUS_DELAY))


def cancel_cactus_event():
    pygame.time.set_timer(CACTUS_APPEARANCE_EVENT, 0)


LEVEL_SPEED = []


def load_level_speed():
    with open('data/level_speed.txt') as f:
        LEVEL_SPEED.clear()
        LEVEL_SPEED.extend([int(speed) for speed in f.readlines()])
        print(LEVEL_SPEED)
