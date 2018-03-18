#! /usr/bin/python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

import os

import cv2

from numpy import ndarray, array
from PIL import Image, ImageFont, ImageDraw

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, pyqtSlot, pyqtSignal, QPoint

from face_handle import Face_handle

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.client_name = []
        self.known_face = []
        self.timer = QTimer()
        self.face_handle = Face_handle()
        self.timer.start(20)
        self.initUI()
        self.signal_connect()


    def initUI(self):
        self.centralWidget = QtWidgets.QWidget()
        self.video = QtWidgets.QLabel(self.centralWidget)
        self.screen_capture = QtWidgets.QPushButton(self.centralWidget)
        self.recognise = QtWidgets.QPushButton(self.centralWidget)
        self.closeBtn = QtWidgets.QPushButton(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(self)
        self.mainToolBar = QtWidgets.QToolBar(self)
        self.statusBar = QtWidgets.QStatusBar(self)

        self.setObjectName("MainWindow")
        self.resize(1022, 672)
        self.centralWidget.setObjectName("centralWidget")
        self.video.setGeometry(QtCore.QRect(20, 20, 640, 480))
        self.video.setText("")
        self.video.setObjectName("video")
        self.screen_capture.setGeometry(QtCore.QRect(770, 100, 151, 41))
        self.screen_capture.setObjectName("screen_capture")
        self.recognise.setGeometry(QtCore.QRect(770, 190, 151, 41))
        self.recognise.setObjectName("recognise")
        self.closeBtn.setGeometry(QtCore.QRect(770, 270, 151, 41))
        self.closeBtn.setObjectName("close")
        self.setCentralWidget(self.centralWidget)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1022, 23))
        self.menuBar.setObjectName("menuBar")
        self.setMenuBar(self.menuBar)
        self.mainToolBar.setObjectName("mainToolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar.setObjectName("statusBar")
        self.setStatusBar(self.statusBar)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setWindowTitle(QtCore.QCoreApplication.translate("Mainwindow", "MainWindow"))

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.screen_capture.setText(_translate("MainWindow", "截屏"))
        self.recognise.setText(_translate("MainWindow", "识别"))
        self.closeBtn.setText(_translate("MainWindow", "关闭"))

    def signal_connect(self):
        self.timer.timeout.connect(self.play_video)
        self.screen_capture.clicked.connect(self.capture)
        self.closeBtn.clicked.connect(self.close)
        self.recognise.clicked.connect(self.recognise_face)

    @pyqtSlot(name="play_video")
    def play_video(self):
        ret, frame = self.cap.read()
        if ret:
            self.play_frame(frame)

    def play_frame(self, frame: ndarray):
        rbgframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        convert_to_qt = QImage(rbgframe, rbgframe.shape[1], rbgframe.shape[0], QImage.Format_RGB888)
        self.video.setPixmap(QPixmap.fromImage(convert_to_qt))

    def recognise_face(self):
        frame = self.capture()
        name, box = self.face_handle.recognise(frame)
        top, right, bottom, left = box
        frame_with_face = cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 3)
        font = ImageFont.truetype("/usr/share/fonts/wps-office/simhei.ttf", 24)
        img = Image.fromarray(frame_with_face)
        draw = ImageDraw.Draw(img)
        draw.text((left, bottom), name, font=font, fill=(0, 0, 255))
        frame_with_tag = array(img)
        self.play_frame(frame_with_tag)

    @pyqtSlot(bool, name="capture")
    def capture(self) -> ndarray:
        self.timer.stop()
        ret, frame = self.cap.read()
        if ret:
            self.play_frame(frame)
            return frame



