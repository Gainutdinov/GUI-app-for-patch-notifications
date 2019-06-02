#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtMultimedia, QtGui
from shell_ui import Ui_MainWindow
from mail_shell_ui import Mail_Ui_MainWindow
import os
import sys

from excelRead import readExcelFile
from cmdb import findServerInfo, fakeFunction


class MyWin(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(MyWin, self).__init__(parent)
        #super().__init__()
        #QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.chooseFolder) 
        self.ui.pushButton_2.clicked.connect(self.populateTblWdt)
        self.ui.pushButton_3.clicked.connect(self.openEmailWindows)

    
    def openEmailWindows(self):
        emailMsg={}
        for row in range(self.ui.tableWidget.rowCount()):
            # self.ui.tableWidget.itemAt(row, 0)
            if self.ui.tableWidget.item(row,0).checkState() != 0: # if user checked a server for patching
                hostname=self.ui.tableWidget.item(row,1).text()
                mntStr=self.ui.tableWidget.item(row,2).text()
                mntFns=self.ui.tableWidget.item(row,3).text()
                srvOwner=self.ui.tableWidget.item(row,4).text()
                wrkInstruction=self.ui.tableWidget.item(row,5).text()
                if srvOwner in emailMsg:
                    emailMsg[srvOwner] = emailMsg[srvOwner] + [[hostname, mntStr, mntFns, srvOwner, wrkInstruction]]
                else:
                    emailMsg[srvOwner] = [[hostname, mntStr, mntFns, srvOwner, wrkInstruction]]
                # S137FWP004 2019-05-02 21:00:00  2019-05-02 23:00:00  ServerOwner WorkInstruction
            else:
                print('Skipped cause user unchecked it')
        print(emailMsg)
        self.mailWindow_list = []
        # objs2 = [ for i in objs1] 
        
        for _ in range(len(emailMsg)):
            window = QtWidgets.QMainWindow()
            mail_ui = Mail_Ui_MainWindow()
            mail_ui.setupUi(window)
            mail_ui.lineEdit_2.setText(self.ui.lineEdit_3.text())
            mail_ui.lineEdit_4.setText(self.ui.lineEdit_4.text())
            mail_ui.pushButton.clicked.connect(mail_ui.sendMessage)
            mail_ui.smtpServer=self.ui.lineEdit.text()
            # mail_ui.lineEdit_2
            # mail_ui.lineEdit_3.setText() # message title
            self.mailWindow_list.append([mail_ui, window])

        for key, obj in zip(emailMsg.keys(),self.mailWindow_list):
            print(key)
            print(obj[1])
            # make email window more customized

            selectedDate = dateOfPatching=self.ui.dateEdit.date().toString('dd/MM/yyyy')
            serversToPatch = ','.join([ _[0] for _ in emailMsg[key]])
            emailTitle = 'Servers to patch on ' + selectedDate + ' - ' + serversToPatch
            toField = emailMsg[key][0][3]
            serverInfo = "\n".join([ str(_[0]+' - '+_[1]+' - '+_[2]+" - \n"+_[4]) for _ in emailMsg[key] ])
            print(type(serverInfo))
            emailText = '''
Hello colleagues,
I let you know that the following servers will be patched soon:
Hostname - MaintenanceStarts - MaintenanceEnds - Worksintruction
{0}'''.format(serverInfo)


            self.mailWindow_list[self.mailWindow_list.index(obj)][0].lineEdit_3.setText(emailTitle)
            self.mailWindow_list[self.mailWindow_list.index(obj)][0].lineEdit.setText(toField)
            self.mailWindow_list[self.mailWindow_list.index(obj)][0].textEdit.setText(emailText)

            self.mailWindow_list[self.mailWindow_list.index(obj)][1].show()

        #mailWindow_list[0][0].show()
        #mailWindow_list[1][0].show()
            # self.window = QtWidgets.QMainWindow()
            # self.mail_ui = Mail_Ui_MainWindow()
            # self.mail_ui.setupUi(self.window)
            # self.mail_ui.lineEdit
            # self.mail_ui.lineEdit_2
            # self.mail_ui.lineEdit_3.setText('TEST')
            # self.mail_ui.pushButton.clicked.connect(self.mail_ui.sendMessage)
            # self.window.show()

        # self.close()



    def chooseFolder(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), "Excel files (*.xlsx *.xls)")
        if fileName[0] and (fileName[0][-4:] == 'xlsx' or fileName[0][-4:] == '.xls'):
            self.ui.lineEdit_2.setText(fileName[0])
            self.ui.lineEdit_3.setEnabled(True)
            self.ui.pushButton_2.setEnabled(True)
            self.ui.dateEdit.setEnabled(True)
        # print(fileName[0][-4:])
    
    def populateTblWdt(self):
        pathToPatchFile=self.ui.lineEdit_2.text()
        dateOfPatching=self.ui.dateEdit.date().toString('MM/dd/yyyy') # '05/11/2019' # '05/11/2019'
        serversToPatch=readExcelFile(pathToPatchFile, dateOfPatching)
        self.ui.tableWidget.clear()
        if len(serversToPatch):
            
            self.ui.pushButton_3.setEnabled(True)
            self.ui.tableWidget.setColumnCount(6)    # Устанавливаем шесть колонок
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)#  .setSectionResizeMode(QHeaderView.Stretch)  # Устанавливаем три колонки
            rows=len(serversToPatch)
            self.ui.tableWidget.setRowCount(rows)
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

                serverOwner,wrkInstruction = fakeFunction(serverName)

                self.ui.textBrowser.append(srv)
                self.ui.tableWidget.setItem(row, 0, chkBoxItem)
                self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(serverName))
                self.ui.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(mntStart))
                self.ui.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(mntEnd))
                self.ui.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(serverOwner))
                self.ui.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(wrkInstruction))
                row += 1
                self.ui.progressBar.setValue(row/rows*100)
        else:
            self.ui.pushButton_3.setEnabled(False)
            self.ui.tableWidget.setRowCount(0)
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


