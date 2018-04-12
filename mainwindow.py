#! /usr/bin/python3
# -*- coding: utf-8 -*-

import cv2

import pymysql
from numpy import ndarray, array

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, pyqtSlot, pyqtSignal, QPoint


from UI_MainWindow import Ui_MainWindow
from face_handle import Face_handle


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.client_name = []
        self.timer = QTimer()
        self.face_handle = Face_handle()
        self.timer.start(20)
        self.UI = Ui_MainWindow()
        self.UI.setupUi(self)
        self.signal_connect()


    def signal_connect(self):
        self.timer.timeout.connect(self.play_video)
        self.UI.pay_btn.clicked.connect(self.recognise_face)

    @pyqtSlot(name="play_video")
    def play_video(self):
        ret, frame = self.cap.read()
        if ret:
            self.play_frame(self.UI.video_label, frame)

    def play_frame(self, label: QtWidgets.QLabel, frame: ndarray):
        rbgframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        convert_to_qt = QImage(rbgframe, rbgframe.shape[1], rbgframe.shape[0], QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(convert_to_qt))

    def recognise_face(self):
        """
            this function recognise face from the current frame
          cut out the face part and show it in a other label, the
          name display in the label blow
        :return:
        """
        self.timer.timeout.disconnect(self.play_video)
        ret, frame = self.cap.read()
        name, box = self.face_handle.recognise(frame)
        top, right, bottom, left = box
        face_part = frame[top: bottom, left: right]
        new_size = self.UI.face.size().height(), self.UI.face.size().width()
        face_part = cv2.resize(face_part, new_size)
        self.play_frame(self.UI.face, face_part)
        self.UI.name_label.setText(name)
        self.timer.timeout.connect(self.play_video)



