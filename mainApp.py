#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtMultimedia
from shell_ui import Ui_MainWindow
import os
import sys


class MyWin(QtWidgets.QMainWindow, Ui_MainWindow):
    


    def __init__(self, parent=None):
        super(MyWin, self).__init__(parent)
        #super().__init__()
        #QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.myThread = MyThread()     # create mytThread instance

        self.ui.pushButton.clicked.connect(self.chooseFolder)
        self.ui.pushButton_2.clicked.connect(self.populateTblWdt)
    

    def chooseFolder(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), "Excel files (*.xlsx *.xls)")
        if fileName[0] and (fileName[0][-4:] == 'xlsx' or fileName[0][-4:] == '.xls'):
            self.ui.lineEdit_2.setText(fileName[0])
            self.ui.lineEdit_3.setEnabled(True)
            self.ui.pushButton_2.setEnabled(True)
            self.ui.dateEdit.setEnabled(True)
        print(fileName[0][-4:])
    
    def populateTblWdt(self):
        print('sssss')
        # self.ui.pushButton.clicked.connect(self.stopMonitoring)
        # self.myThread.mySignal.connect(self.updateLCD, QtCore.Qt.QueuedConnection)
        # self.myThread.customSignal.connect(self.stopMonitoring, QtCore.Qt.QueuedConnection)
        # self.myThread.playMusic.connect(self.playMusicFile, QtCore.Qt.QueuedConnection)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ico = QtWidgets.QWidget().style().standardIcon(QtWidgets.QStyle.SP_FileIcon)
    app.setWindowIcon(ico)
    w = MyWin()
    w.show()
    sys.exit(app.exec())


