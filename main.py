import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication
from structure.MainWindow import MainWindow


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    # For high resolution screens
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # Create and show main window
    main_window = MainWindow()
    main_window.show()

    sys.excepthook = except_hook
    sys.exit(app.exec())
