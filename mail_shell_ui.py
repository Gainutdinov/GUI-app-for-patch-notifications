# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mail_shell_ui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import sys

class Mail_Ui_MainWindow(QtWidgets.QMainWindow,object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 2, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 3, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setStyleSheet("")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 6, 0, 1, 2)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 4, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 5, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Title"))
        self.label_4.setText(_translate("MainWindow", "From"))
        self.label_3.setText(_translate("MainWindow", "Carbon Copy (CC)"))
        self.pushButton.setText(_translate("MainWindow", "Send an email"))
        self.label_2.setText(_translate("MainWindow", "To"))

    def closeEvent(self, event):
        event.accept()
    
    def sendMessage(self):
        print('sendMessage')
        HOST = self.SMTPSERVER
        SUBJECT = self.lineEdit_3.text()
        CC = self.lineEdit_2.text().split(';')
        TO = self.lineEdit.text().split(';') #"Marat.Gainutdinov@icl-services.com"
        FROM = self.lineEdit_4.text().split(';') # "marat@daimler.com"
        #"Test email for notifications"
        BODY = (self.textEdit.toPlainText()) #.encode("utf-8", errors="ignore")
        msg = MIMEText(BODY, _charset="UTF-8")
        msg['Subject'] = Header(SUBJECT, "utf-8")
        msg['To'] = ','.join(TO)
        msg['Cc'] = ','.join(CC)

        server = smtplib.SMTP(HOST)
        server.sendmail(FROM, TO + CC, msg.as_string())
        server.quit()
        # QtCore.QCoreApplication.().quit()

