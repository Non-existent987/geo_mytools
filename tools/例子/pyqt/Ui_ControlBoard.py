# -*- coding: utf-8 -*-
 
# Form implementation generated from reading ui file 'Ui_ControlBoard.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
 
from PyQt5 import QtCore, QtWidgets
 
class Ui_MainWindow(object):
  def setupUi(self, MainWindow):
    MainWindow.setObjectName("MainWindow")
    MainWindow.resize(800, 600)
    self.centralwidget = QtWidgets.QWidget(MainWindow)
    self.centralwidget.setObjectName("centralwidget")
    self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
    self.textBrowser.setGeometry(QtCore.QRect(50, 180, 591, 171))
    self.textBrowser.setObjectName("textBrowser")
    self.pushButton = QtWidgets.QPushButton(self.centralwidget)
    self.pushButton.setGeometry(QtCore.QRect(450, 390, 93, 28))
    self.pushButton.setObjectName("pushButton")
    MainWindow.setCentralWidget(self.centralwidget)
    self.menubar = QtWidgets.QMenuBar(MainWindow)
    self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
    self.menubar.setObjectName("menubar")
    MainWindow.setMenuBar(self.menubar)
    self.statusbar = QtWidgets.QStatusBar(MainWindow)
    self.statusbar.setObjectName("statusbar")
    MainWindow.setStatusBar(self.statusbar)
 
    self.retranslateUi(MainWindow)
    QtCore.QMetaObject.connectSlotsByName(MainWindow)
 
  def retranslateUi(self, MainWindow):
    _translate = QtCore.QCoreApplication.translate
    MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
    self.pushButton.setText(_translate("MainWindow", "PushButton"))