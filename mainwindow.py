#! /usr/bin/python3
# -*- coding: utf-8 -*-

import cv2

import pymysql
from numpy import ndarray
import face_recognition as fr

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, pyqtSlot, pyqtSignal

from UI_MainWindow import Ui_MainWindow

from face_handle import Face_handle
from addclientwindow import AddClientWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.start(20)
        host = 'localhost'
        user = 'root'
        password = '123456'
        db = 'face_pay'
        charset = 'utf8'
        self.connection = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset)
        self.face_handle = Face_handle('known_people_folder/', self.connection)

        self.UI = Ui_MainWindow()
        self.UI.setupUi(self)
        self.signal_connect()

    def signal_connect(self):
        self.timer.timeout.connect(self.play_video)
        self.UI.pay_btn.clicked.connect(self.pay)
        self.UI.add_new_user_btn.clicked.connect(self.add_new_client)
        self.UI.show_balance_btn.clicked.connect(self.show_balance)

    @pyqtSlot(name="play_video")
    def play_video(self):
        ret, frame = self.cap.read()
        if ret:
            MainWindow.play_frame(self.UI.video_label, frame)

    @staticmethod
    def play_frame(label: QtWidgets.QLabel, frame: ndarray):
        rbgframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        convert_to_qt = QImage(rbgframe, rbgframe.shape[1], rbgframe.shape[0], QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(convert_to_qt))

    @pyqtSlot(name='recognise_face')
    def pay(self):
        """
            this function recognise face from the current frame
          cut out the face part and show it in a other label, the
          name display in the label blow
        :return: None
        """
        self.timer.timeout.disconnect(self.play_video)
        ret, frame = self.cap.read()
        name, box = self.face_handle.recognise(frame)
        if name is not None:
            top, right, bottom, left = box
            face_part = frame[top: bottom, left: right]
            new_size = self.UI.face.size().height(), self.UI.face.size().width()
            face_part = cv2.resize(face_part, new_size)
            self.play_frame(self.UI.face, face_part)
            self.UI.name_label.setText(name)
            pay_num = self.UI.pay_num_edit.text()
            if len(pay_num) == 0:
                QMessageBox.warning(self, '错误', '请输入金额')
                self.timer.timeout.connect(self.play_video)
                return
            if QMessageBox.question(self, '提示', '确认支付?') == QMessageBox.Yes:
                with self.connection.cursor() as cursor:
                    sql = 'UPDATE `client_record` SET `balance` = `balance` - %s WHERE `user_name` = %s'
                    cursor.execute(sql, (self.UI.pay_num_edit.text(), name))
                self.connection.commit()
        else:
            self.UI.name_label.setText(box)
        self.timer.timeout.connect(self.play_video)

    @pyqtSlot(name='add_new_client')
    def add_new_client(self):
        self.timer.timeout.disconnect(self.play_video)
        ret, frame = self.cap.read()
        add_client = AddClientWindow(self, self.connection, self.face_handle, frame)
        if add_client.exec() == QDialog.Rejected:
            QMessageBox.information(self, '提示', '取消新增客户')

        self.timer.timeout.connect(self.play_video)

    @pyqtSlot(name='show_balance')
    def show_balance(self):
        self.timer.timeout.disconnect(self.play_video)
        ret, frame = self.cap.read()
        name, box = self.face_handle.recognise(frame)
        sql = 'SELECT `balance` FROM `client_record` WHERE `user_name` = %s'
        with self.connection.cursor() as cursor:
            cursor.execute(sql, name)
            result = cursor.fetchone()
            balance = result[0]
            QMessageBox.information(self, '余额', '%f' % balance)
        self.timer.timeout.connect(self.play_video)
