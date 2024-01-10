import random
from typing import Any

import pygame

from system import CACTUS_APPEARANCE_EVENT, update_cactus_event
from system import SIZE, WIDTH, FPS
from system import load_image

# load_image() requires pygame and screen initialization
pygame.init()
screen = pygame.display.set_mode(SIZE)


class Tile(pygame.sprite.Sprite):
    images = [load_image('tile_1.png'), load_image('tile_2.png')]
    dx = -10

    def __init__(self, x: int, *groups):
        super(Tile, self).__init__(*groups)
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, 467

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect = self.rect.move(self.dx, 0)

        # If there is an empty space on the right that needs to be filled with tiles
        if self.rect.x < 0 and len(tile_group) == 2:
            Tile(WIDTH + self.rect.x, tile_group, all_sprites)

        # If the tile is no longer visible
        if self.rect.right < 0:
            self.kill()


class Cactus(pygame.sprite.Sprite):
    images = [load_image('cactus.png')]
    dx = -10

    def __init__(self, *groups):
        super(Cactus, self).__init__(*groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = WIDTH, 385

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect = self.rect.move(self.dx, 0)
        # If the cactus is no longer visible
        if self.rect.right < 0:
            self.kill()


class Dino(pygame.sprite.Sprite):
    frames = [load_image('dino_right_up.png'),
              load_image('dino_left_up.png')]

    def __init__(self, *groups):
        super(Dino, self).__init__(*groups)
        self.image = self.frames[0]
        self.cur_frame = 0
        # Frame change counter for animation speed task
        self.frame_counter = 0

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 100, 367

    def update(self, *args: Any, **kwargs: Any) -> None:
        # Animation
        self.frame_counter += 1
        if self.frame_counter == 3:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.frame_counter = 0


if __name__ == '__main__':
    bg_image = load_image('game_bg.png')
    clock = pygame.time.Clock()

    # Sprite groups
    all_sprites = pygame.sprite.Group()
    dino_group = pygame.sprite.Group()
    tile_group = pygame.sprite.Group()
    cactus_group = pygame.sprite.Group()

    # Initial tiles
    Tile(0, tile_group, all_sprites)
    Tile(WIDTH // 2, tile_group, all_sprites)

    update_cactus_event()
    dino = Dino(dino_group, all_sprites)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == CACTUS_APPEARANCE_EVENT:
                Cactus(cactus_group, all_sprites)
                update_cactus_event()

        screen.blit(bg_image, (0, 0))

        tile_group.update()
        tile_group.draw(screen)

        cactus_group.update()
        cactus_group.draw(screen)

        dino_group.update()
        dino_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
