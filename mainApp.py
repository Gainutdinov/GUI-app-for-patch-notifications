#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtMultimedia, QtGui
from shell_ui import Ui_MainWindow
import os
import sys

from excelRead import readExcelFile
from cmdb import findServerInfo


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
        pathToPatchFile=self.ui.lineEdit_2.text()
        dateOfPatching=self.ui.dateEdit.date().toString('MM/dd/yyyy') # '05/11/2019' # '05/11/2019'
        print(dateOfPatching,'---',pathToPatchFile)
        serversToPatch=readExcelFile(pathToPatchFile, dateOfPatching)
        self.ui.tableWidget.clear()
        if len(serversToPatch):
            self.ui.tableWidget.setColumnCount(6)    # Устанавливаем шесть колонок
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)#  .setSectionResizeMode(QHeaderView.Stretch)  # Устанавливаем три колонки
            self.ui.tableWidget.setRowCount(len(serversToPatch))
            self.ui.tableWidget.setHorizontalHeaderLabels(["","Hostname", "Next Maintenace start", "Next maintenance window end","Server owner","Workinstruction status"]) 
            # ["" - 0 ,"Hostname" - 1, "Next Maintenace start" - 2, "Next maintenance window end" - 3,"Server owner" - 4,"Workinstruction status" - 5]


            row=0
            for serverName, value in serversToPatch.items():
                srv=serverName+' - '+str(value)
                mntStart=value[0]
                mntEnd=value[1]
                chkBoxItem = QtWidgets.QTableWidgetItem()
                chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                chkBoxItem.setCheckState(QtCore.Qt.Checked)
                serverOwner,wrkInstruction = findServerInfo(serverName)

                self.ui.textBrowser.append(srv)

                self.ui.tableWidget.setItem(row, 0, chkBoxItem)
                self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(serverName))
                self.ui.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(mntStart))
                self.ui.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(mntEnd))
                self.ui.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(serverOwner))
                self.ui.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(wrkInstruction))
                row += 1
        else:
            self.ui.textBrowser.append('No matches found...')

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


