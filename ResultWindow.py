import os
import sys

import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from system import SIZE, FPS


class ResultWindow:
    def __init__(self, result_time: int, game_level: int):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption('Cyber Dino')

        self.bg_image = self.load_image('game_bg.png')
        self.clock = pygame.time.Clock()

        self.result_time: int = result_time
        self.game_level: int = game_level

        self.ui_manager: pygame_gui.UIManager | None = None
        self.close_btn: pygame_gui.elements.UIButton | None = None

        self.flag = False

    def show(self):
        self.initialize()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.close_btn:
                        running = False

                self.ui_manager.process_events(event)

            self.screen.blit(self.bg_image, (0, 0))

            self.ui_manager.update(self.clock.tick(FPS) / 1000.0)
            self.ui_manager.draw_ui(self.screen)

            pygame.display.flip()

        pygame.quit()

    def initialize(self):
        self.ui_manager = pygame_gui.UIManager(SIZE, theme_path='data/game_window_theme.json')

        # Message (at the beginning)
        pygame_gui.elements.UILabel(
            pygame.Rect((206, 30), (580, 42)),
            text="YOUR RESULT",
            manager=self.ui_manager,
            object_id=ObjectID(object_id='#message', class_id='@big_text')
        )

        # Description
        pygame_gui.elements.UITextBox(
            html_text=f'Поздравляем! Вы продержались {self.result_time} сек. на {self.game_level} '
                      f'уровне по сложности. Возвращайтесь в следующий раз и ставьте новые рекорды!',
            relative_rect=pygame.Rect((60, 130), (880, 220)),
            manager=self.ui_manager,
            object_id=ObjectID(object_id='#description', class_id='@long_text')
        )

        # Close window button
        self.close_btn = pygame_gui.elements.UIButton(
            pygame.Rect((378, 450), (243, 45)),
            'Завершить', manager=self.ui_manager,
            object_id=ObjectID(object_id='#close_btn', class_id='@game_btn')
        )

        # App name (logo)
        pygame_gui.elements.UILabel(
            pygame.Rect((436, 617), (130, 13)),
            text='CYBER DINO',
            manager=self.ui_manager,
            object_id=ObjectID(object_id='#small_logo', class_id='@big_text')
        )

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
