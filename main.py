
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
        self.ui = loadUi('./ui/main/mainwindow.ui', self)

        self.filepath = './data'
        self.files = []
        self.pb_loadmsrfiles.clicked.connect(self.load_msr_files)
        self.pb_exit.clicked.connect(self.close)
        self.pb_exit.setStyleSheet('color: red')
        self.pb_test.clicked.connect(self.file_list)
        self.csv_list = []
        self.par_list = []
        self.mod_list = []

    def load_msr_files(self):
        for i in range(11):
            self.progressBar.setValue(i*10)
            QApplication.processEvents()
            sleep(0.5)

    def file_list(self):
        while not os.path.isdir(self.filepath):
            self.filepath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.files = os.listdir(self.filepath)
        self.csv_list = []
        self.par_list = []
        self.mod_list = []

        for file in self.files:
            if file[0:3] == 'msr':
                if file[-3:] == 'txt':
                    self.csv_list.append(file)
                elif file[-3:] == 'par':
                    self.par_list.append(file)
            elif file[-5:] == '.hdf5':
                self.mod_list.append(file)
        print(self.csv_list)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
