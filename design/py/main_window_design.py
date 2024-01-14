# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\main_window_design.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 650)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 650))
        MainWindow.setMaximumSize(QtCore.QSize(1000, 650))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 1000, 650))
        self.background.setText("")
        self.background.setPixmap(QtGui.QPixmap(".\\../../data/game_bg.png"))
        self.background.setObjectName("background")
        self.app_name = QtWidgets.QLabel(self.centralwidget)
        self.app_name.setGeometry(QtCore.QRect(210, 36, 576, 39))
        font = QtGui.QFont()
        font.setPointSize(45)
        self.app_name.setFont(font)
        self.app_name.setStyleSheet("color: #E8E5E5;\n"
"")
        self.app_name.setPixmap(QtGui.QPixmap(".\\../../data/app_name.png"))
        self.app_name.setObjectName("app_name")
        self.level_label = QtWidgets.QLabel(self.centralwidget)
        self.level_label.setGeometry(QtCore.QRect(419, 186, 160, 18))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.level_label.setFont(font)
        self.level_label.setStyleSheet("color: #E8E5E5;")
        self.level_label.setPixmap(QtGui.QPixmap(".\\../../data/levels_label.png"))
        self.level_label.setObjectName("level_label")
        self.level_1 = QtWidgets.QLabel(self.centralwidget)
        self.level_1.setGeometry(QtCore.QRect(51, 250, 279, 211))
        self.level_1.setText("")
        self.level_1.setPixmap(QtGui.QPixmap(".\\../../data/level_1.png"))
        self.level_1.setObjectName("level_1")
        self.level_2 = QtWidgets.QLabel(self.centralwidget)
        self.level_2.setGeometry(QtCore.QRect(363, 250, 279, 211))
        self.level_2.setText("")
        self.level_2.setPixmap(QtGui.QPixmap(".\\../../data/level_2.png"))
        self.level_2.setObjectName("level_2")
        self.level_3 = QtWidgets.QLabel(self.centralwidget)
        self.level_3.setGeometry(QtCore.QRect(675, 250, 279, 211))
        self.level_3.setText("")
        self.level_3.setPixmap(QtGui.QPixmap(".\\../../data/level_3.png"))
        self.level_3.setObjectName("level_3")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Homepage"))
