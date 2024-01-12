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
        if self.rect.x < 0 and len(game.tile_group) == 2:
            Tile(WIDTH + self.rect.x, game.tile_group, game.all_sprites)

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

        # Collision with a cactus
        if pygame.sprite.spritecollideany(self, game.cactus_group):
            game.stop()

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
    bg_image = load_image('game_bg.png')

    def __init__(self):
        self.bg_image = Game.bg_image
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
            Cactus(self.cactus_group, self.all_sprites)
            update_cactus_event()

        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
            self.dino.start_jumping()

    def handle_stop_event(self, event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.restart()

    def update(self) -> None:
        screen.blit(self.bg_image, (0, 0))

        self.all_sprites.update()
        self.all_sprites.draw(screen)

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
        Tile(0, self.tile_group, self.all_sprites)
        Tile(WIDTH // 2, self.tile_group, self.all_sprites)

        self.dino = Dino(self.dino_group, self.all_sprites)

        self.is_playing = True
        update_cactus_event()


if __name__ == '__main__':
    game = Game()
    game.start()
