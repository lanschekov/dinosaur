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
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (pos_x, pos_y)
        self.delta = -1000
        self.is_jumping = False

    def is_kill(self):
        if pygame.sprite.spritecollideany(self, cactus_group):
            self.kill()
            for sprite in cactus_group:
                sprite.v = 0
            for sprite in boost_group:
                sprite.v = 0
        if pygame.sprite.spritecollideany(self, boost_group):
            for sprite in cactus_group:
                sprite.v *= 2
            for sprite in boost_group:
                sprite.v *= 2
        if pygame.sprite.spritecollideany(self, boost2_group):
            for sprite in cactus_group:
                sprite.v /= 2
            for sprite in boost2_group:
                sprite.v /= 2

    def update(self):
        self.rect = self.rect.move(0, self.delta * delta_time)
        if self.delta < 1000:
            self.delta += 25
        else:
            self.is_jumping = False
            self.delta = -1000


class Cactus(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(cactus_group, all_sprites)
        self.pos_x, self.pos_y = pos_x, pos_y
        self.image = load_image(
            random.choice(['cactus.png', 'cactus-1.png', 'cactus-2.png']))
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.rect.w * 1.5, self.rect.h * 1.5))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (pos_x, pos_y)
        self.v = 1000

    def update(self):
        if self.rect.right < 0:
            self.kill()
        self.rect = self.rect.move(-self.v * delta_time, 0)


class Boost(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(boost_group, all_sprites)
        self.pos_x, self.pos_y = pos_x, pos_y
        self.image = load_image('boost.png')
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (pos_x, pos_y)
        self.v = 1000

    def update(self):
        if self.rect.right < 0 or pygame.sprite.spritecollideany(self, player_group):
            self.kill()
        self.rect = self.rect.move(-self.v * delta_time, 0)


class Boost2(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(boost2_group, all_sprites)
        self.pos_x, self.pos_y = pos_x, pos_y
        self.image = load_image('boost2.png')
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (pos_x, pos_y)
        self.v = 1000

    def update(self):
        if self.rect.right < 0 or pygame.sprite.spritecollideany(self, player_group):
            self.kill()
        self.rect = self.rect.move(-self.v * delta_time, 0)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1980, 1080
    screen = pygame.display.set_mode(size)

    min_spawn_time = 2
    waiting_time = min_spawn_time + random.randint(0, 2)
    between_spawns = 0

    old_time = pygame.time.get_ticks()
    delta_time = 0

    clock = pygame.time.Clock()
    fps = 60

    player_image = load_image('dino.png')

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    cactus_group = pygame.sprite.Group()
    boost_group = pygame.sprite.Group()
    boost2_group = pygame.sprite.Group()

    player = Player(250, 1000)
    cactus = Cactus(2000, 1000)
    cactus_group.add(cactus)
    boost_group.add(Boost(2000, 500))
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

        if between_spawns > waiting_time:
            between_spawns = 0
            waiting_time = min_spawn_time + random.randint(0, 2)
            cactus_group.add(Cactus(2000, 1000))
            if random.randint(0, 1) == 0:
                boost_group.add(Boost(2000, 600))
            else:
                boost2_group.add(Boost2(2100, 500))
        between_spawns += delta_time

        if player.is_jumping:
            player_group.update()
        player.is_kill()
        cactus_group.update()
        boost_group.update()
        boost2_group.update()

        screen.fill((120, 120, 120))
        cactus_group.draw(screen)
        boost_group.draw(screen)
        boost2_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()

        time_now = pygame.time.get_ticks()
        delta_time = (time_now - old_time) / 1000.0
        old_time = time_now
        clock.tick(fps)
    pygame.quit()
