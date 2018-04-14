#! /usr/bin/python3
# -*- coding: utf8 -*-


import cv2
import pymysql
from numpy import ndarray
import face_recognition as fr

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage


from UI_add_client import Ui_add_client
from face_handle import Face_handle


class AddClientWindow(QDialog):
    def __init__(self, parent, connect: pymysql.connections, face_handle: Face_handle, frame: ndarray, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.UI = Ui_add_client()
        self.UI.setupUi(self)
        self.connect = connect
        self.face_handle = face_handle
        self.frame = frame
        try:
            top, right, bottom, left = fr.face_locations(frame)[0]
        except IndexError as e:
            QMessageBox.warning(self, '警告', '未识别到人脸')
            self.close()
            return
        face = frame[top:bottom, left:right]
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        face = cv2.resize(face, (self.UI.face_label.size().height(), self.UI.face_label.size().width()))
        image = QImage(face, face.shape[1], face.shape[0], face.shape[1] * 3, QImage.Format_RGB888)
        self.UI.face_label.setPixmap(QPixmap.fromImage(image))
        self.signal_connect()

    def signal_connect(self):
        self.UI.OK_btn.clicked.connect(self.commit)
        self.UI.cancel_btn.clicked.connect(self.cancel)

    @pyqtSlot(name='commit')
    def commit(self):
        name = self.UI.name_input.text()
        balance = self.UI.balance_input.text()
        if len(name) == 0 or len(balance) == 0:
            QMessageBox.warning(self, '错误', '请输入用户名和余额')
            return
        sql = 'INSERT INTO `client_record`(`user_name`, `balance`) VALUES (%s, %s)'
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(sql, (name, balance))
                self.connect.commit()
                self.face_handle.add_new_client(self.frame, name=name)
        except pymysql.MySQLError as e:
            e.with_traceback()
            QMessageBox.warning(self, '错误', '数据库连接失败')
        except Exception as e:
            e.with_traceback()
            QMessageBox.warning(self, '错误', '数据库连接失败')
        self.done(QDialog.Accepted)

    @pyqtSlot(name='cancel')
    def cancel(self):
        self.done(QDialog.Rejected)
