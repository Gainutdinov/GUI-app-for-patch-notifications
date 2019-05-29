#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtMultimedia
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
        if len(serversToPatch):
            for key, value in serversToPatch.items():
                srv=key+' - '+str(value)
                # print(type(srv))
                self.ui.textBrowser.append(srv)#, str(value))

                self.ui.tableWidget.setColumnCount(6)    # Устанавливаем три колонки
                self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)#  .setSectionResizeMode(QHeaderView.Stretch)  # Устанавливаем три колонки
                self.ui.tableWidget.setRowCount(len(serversToPatch))
                self.ui.tableWidget.setHorizontalHeaderLabels(["","Hostname", "Next Maintenace start", "Next maintenance window end","Server owner","Workinstruction status"])
                self.ui.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem("Text in column 1"))
                self.ui.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem("Text in column 2"))
                self.ui.tableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem("Text in column 3"))
                
                cell_widget = QtWidgets.QWidget()
                chk_bx = QtWidgets.QCheckBox()
                chk_bx.setCheckState(QtCore.Qt.Checked)
                lay_out = QtWidgets.QHBoxLayout(cell_widget)
                lay_out.addWidget(chk_bx)
                lay_out.setAlignment(QtCore.Qt.AlignCenter)
                lay_out.setContentsMargins(0,0,0,0)
                cell_widget.setLayout(lay_out)
                self.ui.tableWidget.setItem(0, 0, cell_widget)

                # tableWidget.setCellWidget(i, 0, cell_widget)

                # chkBoxItem = QtWidgets.QTableWidgetItem()
                # chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.AlignCenter)
                # chkBoxItem.setCheckState(QtCore.Qt.Unchecked)    
                
                
                # self.ui.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem("Text in column 3"))
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


