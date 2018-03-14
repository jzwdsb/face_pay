#! /usr/bin/python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!


import cv2

from PIL import Image
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, pyqtSlot, pyqtSignal


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cap = None
        self.mat = None
        self.timer = QTimer()
        self.setObjectName("MainWindow")
        self.resize(1022, 672)
        self.centralWidget = QtWidgets.QWidget()
        self.centralWidget.setObjectName("centralWidget")
        self.video = QtWidgets.QLabel(self.centralWidget)
        self.video.setGeometry(QtCore.QRect(20, 20, 640, 480))
        self.video.setText("")
        self.video.setObjectName("video")
        self.screen_capture = QtWidgets.QPushButton(self.centralWidget)
        self.screen_capture.setGeometry(QtCore.QRect(770, 100, 151, 41))
        self.screen_capture.setObjectName("screen_capture")
        self.recognise = QtWidgets.QPushButton(self.centralWidget)
        self.recognise.setGeometry(QtCore.QRect(770, 190, 151, 41))
        self.recognise.setObjectName("recognise")
        self.closeBtn = QtWidgets.QPushButton(self.centralWidget)
        self.closeBtn.setGeometry(QtCore.QRect(770, 270, 151, 41))
        self.closeBtn.setObjectName("close")
        self.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1022, 23))
        self.menuBar.setObjectName("menuBar")
        self.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(self)
        self.mainToolBar.setObjectName("mainToolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.setObjectName("statusBar")
        self.setStatusBar(self.statusBar)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setWindowTitle(QtCore.QCoreApplication.translate("Mainwindow", "MainWindow"))
        self.timer.start(20)
        self.signal_connect()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.screen_capture.setText(_translate("MainWindow", "截屏"))
        self.recognise.setText(_translate("MainWindow", "识别"))
        self.closeBtn.setText(_translate("MainWindow", "关闭"))

    def signal_connect(self):
        self.timer.timeout.connect(self.play_video)
        self.screen_capture.clicked.connect(self.capture)
        self.closeBtn.clicked.connect(self.close)

    @
    def recognise_face(self):


    @pyqtSlot(name="play_video")
    def play_video(self):
        ret, frame = self.cap.read()
        rgbframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        convert_to_qt = QImage(rgbframe, rgbframe.shape[1], rgbframe.shape[0], QImage.Format_RGB888)
        self.video.setPixmap(QPixmap.fromImage(convert_to_qt))

    @pyqtSlot(bool, name="capture")
    def capture(self):
        ret, frame = self.cap.read()

