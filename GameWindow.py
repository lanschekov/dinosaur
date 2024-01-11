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
    FRAMES = [load_image('dino_right_up.png'),
              load_image('dino_left_up.png')]

    START_X, START_Y = 100, 367

    JUMP_HEIGHT = 200
    JUMP_SPEED = 30
    MIN_JUMP_SPEED = 10
    GRAVITY = 2

    def __init__(self, *groups):
        super(Dino, self).__init__(*groups)
        self.image = self.FRAMES[0]
        self.cur_frame = 0
        # Frame change counter for animation speed task
        self.frame_counter = 0

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.START_X, self.START_Y

        self.dy = self.JUMP_SPEED
        self.is_going_up = False
        self.is_going_down = False

    def update(self, *args: Any, **kwargs: Any) -> None:
        # Animation
        self.frame_counter += 1
        if self.frame_counter == 3:
            self.cur_frame = (self.cur_frame + 1) % len(self.FRAMES)
            self.image = self.FRAMES[self.cur_frame]
            self.frame_counter = 0

        # Probable jump
        if self.is_going_up:
            self.go_up()
        elif self.is_going_down:
            self.go_down()

    def go_down(self) -> None:
        # Increase Y coordinate
        self.dy += self.GRAVITY
        self.rect.y += self.dy

        if self.rect.y > self.START_Y:
            self.rect.y = self.START_Y
            self.is_going_down = False
            self.dy = self.JUMP_SPEED

    def go_up(self) -> None:
        # Decrease Y coordinate
        self.dy -= self.GRAVITY
        if self.dy < self.MIN_JUMP_SPEED:
            self.dy = self.MIN_JUMP_SPEED
        self.rect.y -= self.dy

        if self.rect.y < self.START_Y - self.JUMP_HEIGHT:
            self.rect.y = self.START_Y - self.JUMP_HEIGHT
            self.is_going_up = False
            self.is_going_down = True

    def start_jumping(self) -> None:
        if not self.is_going_up and not self.is_going_down:
            self.is_going_up = True


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

            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
                dino.start_jumping()

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
