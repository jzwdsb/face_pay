# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_client.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_add_client(object):
    def setupUi(self, add_client):
        add_client.setObjectName("add_client")
        add_client.resize(400, 300)
        self.name_input = QtWidgets.QLineEdit(add_client)
        self.name_input.setGeometry(QtCore.QRect(210, 160, 142, 26))
        self.name_input.setObjectName("name_input")
        self.label = QtWidgets.QLabel(add_client)
        self.label.setGeometry(QtCore.QRect(100, 160, 30, 18))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(add_client)
        self.label_2.setGeometry(QtCore.QRect(100, 210, 60, 18))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(add_client)
        self.lineEdit_2.setGeometry(QtCore.QRect(210, 200, 142, 26))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.OK_btn = QtWidgets.QPushButton(add_client)
        self.OK_btn.setGeometry(QtCore.QRect(300, 260, 80, 26))
        self.OK_btn.setObjectName("OK_btn")
        self.cancel_btn = QtWidgets.QPushButton(add_client)
        self.cancel_btn.setGeometry(QtCore.QRect(100, 260, 80, 26))
        self.cancel_btn.setObjectName("cancel_btn")
        self.face_label = QtWidgets.QLabel(add_client)
        self.face_label.setGeometry(QtCore.QRect(100, 20, 131, 111))
        self.face_label.setAlignment(QtCore.Qt.AlignCenter)
        self.face_label.setObjectName("face_label")

        self.retranslateUi(add_client)
        QtCore.QMetaObject.connectSlotsByName(add_client)

    def retranslateUi(self, add_client):
        _translate = QtCore.QCoreApplication.translate
        add_client.setWindowTitle(_translate("add_client", "Form"))
        self.label.setText(_translate("add_client", "姓名"))
        self.label_2.setText(_translate("add_client", "初始金额"))
        self.OK_btn.setText(_translate("add_client", "OK"))
        self.cancel_btn.setText(_translate("add_client", "cancel"))
        self.face_label.setText(_translate("add_client", "TextLabel"))

