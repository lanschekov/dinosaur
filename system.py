import os
import random
import sys

import pygame

SIZE = WIDTH, HEIGHT = 1000, 650
FPS = 30

CACTUS_APPEARANCE_EVENT = 234
CACTUS_DELAY = range(100, 2000)


def update_cactus_event():
    pygame.time.set_timer(CACTUS_APPEARANCE_EVENT,
                          random.choice(CACTUS_DELAY))


def load_image(name, colorkey=None):
    fullname = 'data/' + name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
