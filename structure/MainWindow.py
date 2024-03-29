from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow

from structure.GameWindow import Game
from design.py.main_window_design import Ui_MainWindow
from system import load_level_speed


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.background.setPixmap(QtGui.QPixmap('data/game_bg.png'))
        self.app_name.setPixmap(QtGui.QPixmap('data/app_name.png'))
        self.level_label.setPixmap(QtGui.QPixmap('data/levels_label.png'))
        self.level_1.setPixmap(QtGui.QPixmap('data/level_1.png'))
        self.level_2.setPixmap(QtGui.QPixmap('data/level_2.png'))
        self.level_3.setPixmap(QtGui.QPixmap('data/level_3.png'))

        self.level_1.mousePressEvent = lambda event: self.start_level(game_level=1)
        self.level_2.mousePressEvent = lambda event: self.start_level(game_level=2)
        self.level_3.mousePressEvent = lambda event: self.start_level(game_level=3)

    def start_level(self, game_level: int):
        load_level_speed()  # Loading speed values for all levels
        game = Game(game_level)  # Game window
        self.close()  # Close main window
        game.show()
