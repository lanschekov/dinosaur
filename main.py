import os
import random
import pygame
import sys


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


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos_x, self.pos_y = pos_x, pos_y
        self.image = player_image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.delta = -100
        self.is_jumping = False

    def update(self):
        if pygame.sprite.spritecollideany(self, cactus_group):
            self.kill()
        self.rect = self.rect.move(0, self.delta)
        if self.delta < 100:
            self.delta += 10
        else:
            self.is_jumping = False
            self.delta = -100


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1980, 1080
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 30

    player_image = load_image('dino.png', -1)

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    cactus_group = pygame.sprite.Group()

    player = Player(500, 700)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                player.is_jumping = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.is_jumping = True

        if player.is_jumping:
            player_group.update()

        screen.fill((120, 120, 120))

        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
