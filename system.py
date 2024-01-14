import random

import pygame

SIZE = WIDTH, HEIGHT = 1000, 650
FPS = 30

CACTUS_APPEARANCE_EVENT = 234
CACTUS_DELAY = range(100, 2000)


def update_cactus_event():
    pygame.time.set_timer(CACTUS_APPEARANCE_EVENT,
                          random.choice(CACTUS_DELAY))
