from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import QSize
from time import sleep as sleep
import os
import pandas as pd
import numpy as np


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        QMainWindow.__init__(self)
        self.ui = loadUi('./ui/mainwindow/form.ui', self)

        self.filepath = './data'
        self.files = []
        self.pb_loadmsrfiles.clicked.connect(self.load_msr_files)
        self.pb_exit.clicked.connect(self.close)
        self.pb_exit.setStyleSheet('color: red')

    def load_msr_files(self):
        for i in range(11):
            self.progressBar.setValue(i*10)
            QApplication.processEvents()
            sleep(0.5)

    def filelist(self):
        pass


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()