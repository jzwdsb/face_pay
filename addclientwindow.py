#! /usr/bin/python3
# -*- coding: utf8 -*-

import pymysql

import cv2
from numpy import ndarray

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage

from UI_add_client import Ui_add_client


class AddClientWindow(QDialog):
    def __init__(self, parent, connect: pymysql.connections, face: ndarray, flags, *args, **kwargs):
        super().__init__(flags, parent, *args, **kwargs)
        self.UI = Ui_add_client()
        self.UI.setupUi(self)
        self.connect = connect
        face = cv2.resize(face, (self.UI.face_label.size().height(), self.UI.face_label.size().width()))
        image = QImage(face, face.shape[1], face.shape[0], QImage.Format_RGB888)
        self.UI.face_label.setPixmap(QPixmap.fromImage(image))

    def signal_connect(self):
        self.UI.OK_btn.clicked.connect(self.commit)
        self.UI.cancel_btn.clicked.connect()

    def commit(self):
        name = self.UI.name_input.text()
        balance = self.UI.balance_input.text()
        if len(name) == 0 or len(balance) == 0:
            QMessageBox.warning(self, '错误', '请输入用户名和余额')
            return
        sql = 'INSERT INTO `client_record`(`user_name`, `balance`) VALUES (%s, %s)'
        with self.connect.cursor() as cursor:
            cursor.execute(sql, name, balance)
        try:
            self.connect.commit()
        except pymysql.MySQLError as e:
            QMessageBox.warning(self, '错误', '数据库连接失败')
        except Exception as e:
            QMessageBox.warning(self, '错误', '数据库连接失败')

        self.done(QDialog.Accepted)

    def cancel(self):
        self.done(QDialog.Rejected)
