import os
import random
import sys
from typing import Any

import pygame

from system import CACTUS_APPEARANCE_EVENT, update_cactus_event
from system import SIZE, WIDTH, FPS


class Tile(pygame.sprite.Sprite):
    dx = -10

    def __init__(self, game, x: int, *groups):
        super(Tile, self).__init__(*groups)
        self.game = game
        self.image = random.choice(game.tile_images)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, 467

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect = self.rect.move(self.dx, 0)

        # If there is an empty space on the right that needs to be filled with tiles
        if self.rect.x < 0 and len(self.game.tile_group) == 2:
            Tile(self.game, WIDTH + self.rect.x, self.game.tile_group, self.game.all_sprites)

        # If the tile is no longer visible
        if self.rect.right < 0:
            self.kill()


class Cactus(pygame.sprite.Sprite):
    dx = -10

    def __init__(self, game, *groups):
        super(Cactus, self).__init__(*groups)
        self.image = game.cactus_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = WIDTH, 385
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect = self.rect.move(self.dx, 0)
        # If the cactus is no longer visible
        if self.rect.right < 0:
            self.kill()


class Dino(pygame.sprite.Sprite):
    START_X, START_Y = 100, 367

    JUMP_HEIGHT = 200
    JUMP_SPEED = 30
    MIN_JUMP_SPEED = 10
    GRAVITY = 2

    def __init__(self, game, *groups):
        super(Dino, self).__init__(*groups)
        self.game = game

        self.image = game.dino_images[0]
        self.cur_frame = 0
        # Frame change counter for animation speed task
        self.frame_counter = 0

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.START_X, self.START_Y

        self.mask = pygame.mask.from_surface(self.image)

        self.dy = self.JUMP_SPEED
        self.is_going_up = False
        self.is_going_down = False

    def update(self, *args: Any, **kwargs: Any) -> None:
        # Animation
        self.frame_counter += 1
        if self.frame_counter == 3:
            self.animate()
            self.frame_counter = 0

        # Probable jump
        if self.is_going_up:
            self.go_up()
        elif self.is_going_down:
            self.go_down()

        # Collision with a cactus
        if pygame.sprite.spritecollideany(self, self.game.cactus_group, pygame.sprite.collide_mask):
            self.game.stop()

    def animate(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.game.dino_images)
        self.image = self.game.dino_images[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)

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


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)

        self.bg_image = self.load_image('game_bg.png')

        self.tile_images = [self.load_image('tile_1.png'),
                            self.load_image('tile_2.png')]

        self.cactus_image = self.load_image('cactus.png')

        self.dino_images = [self.load_image('dino_right_up.png'),
                            self.load_image('dino_left_up.png')]

        self.clock = pygame.time.Clock()

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.dino_group = pygame.sprite.Group()
        self.tile_group = pygame.sprite.Group()
        self.cactus_group = pygame.sprite.Group()

        self.is_playing = None
        self.dino = None

    def start(self):
        self.initialize()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.is_playing:
                    self.handle_play_event(event)
                else:
                    self.handle_stop_event(event)

            if self.is_playing:
                self.update()

        pygame.quit()

    def handle_play_event(self, event) -> None:
        if event.type == CACTUS_APPEARANCE_EVENT:
            Cactus(self, self.cactus_group, self.all_sprites)
            update_cactus_event()

        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
            self.dino.start_jumping()

    def handle_stop_event(self, event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.restart()

    def update(self) -> None:
        self.screen.blit(self.bg_image, (0, 0))

        self.tile_group.update()
        self.tile_group.draw(self.screen)

        self.cactus_group.update()
        self.cactus_group.draw(self.screen)

        self.dino_group.update()
        self.dino_group.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(FPS)

    def stop(self) -> None:
        self.is_playing = False

    def restart(self) -> None:
        self.clear()
        self.initialize()

    def clear(self) -> None:
        for cactus in self.cactus_group:
            cactus.kill()
        for tile in self.tile_group:
            tile.kill()
        for dino in self.dino_group:
            dino.kill()

    def initialize(self) -> None:
        Tile(self, 0, self.tile_group, self.all_sprites)
        Tile(self, WIDTH // 2, self.tile_group, self.all_sprites)

        self.dino = Dino(self, self.dino_group, self.all_sprites)

        self.is_playing = True
        update_cactus_event()

    def load_image(self, name, colorkey=None):
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
