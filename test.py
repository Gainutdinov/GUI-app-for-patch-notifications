import sys

from PyQt5 import QtCore, QtWidgets, QtMultimedia, QtGui
from progressbar_ui import Ui_Form
import os
import sys
import time


class MyWin(QtWidgets.QWidget, Ui_Form):
    
    def __init__(self, parent=None):
        super(MyWin, self).__init__(parent)
        #super().__init__()
        #QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.progress=0
        QtCore.QTimer.singleShot(3000, self.increaseProgressBar)
        QtCore.QTimer.singleShot(5000, self.increaseProgressBar)
        QtCore.QTimer.singleShot(10000, self.increaseProgressBar)
        QtCore.QTimer.singleShot(13000, self.increaseProgressBar)
        QtCore.QTimer.singleShot(15000, self.increaseProgressBar)
        #QtCore.QTimer.singleShot(3000, self.increaseProgressBar)
        #QtCore.QTimer.singleShot(3000, self.increaseProgressBar)
        #QtCore.QTimer.singleShot(20000, self.lastFunc)
    
    
    def increaseProgressBar(self):
        print(self.ui.progressBar.value())
        self.ui.progressBar.setValue(self.progress)
        self.progress += 25
        if self.ui.progressBar.value() == 100:
            self.lastFunc()

    
    def lastFunc(self):
        self.close()


        #self.ui.setWindowFlags(QtWidgets.QWidget().windowFlags() | QtCore.Qt.FramelessWindowHint)
        # self.myThread = MyThread()     # create mytThread instance
        #self.ui.pushButton.clicked.connect(self.chooseFolder) 
        #self.ui.pushButton_2.clicked.connect(self.populateTblWdt)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #ico = QtWidgets.QWidget().style().standardIcon(QtWidgets.QStyle.SP_FileIcon)
    #app.setWindowIcon(ico)
    w = MyWin()
    w.show()

    sys.exit(app.exec())