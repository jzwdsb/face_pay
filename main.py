#! /usr/bin/pyhton3
# -*- coding: utf8 -*-

import sys

from mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication

from addclientwindow import AddClientWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())