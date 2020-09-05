import sys
from PyQt5.QtCore import *
from tools import *
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QHBoxLayout,QGraphicsDropShadowEffect, QPushButton,  QComboBox,QMessageBox,QCommandLinkButton,QMainWindow,QDialog,QFrame,QVBoxLayout,QLineEdit
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QUrl,Qt
from shapely.geometry import (LinearRing, LineString, MultiLineString,
                       MultiPoint, MultiPolygon, Point, Polygon)
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget,QMessageBox
from PyQt5.QtCore import QThread,QTimer
from PyQt5 import *
from Ui_keti import *
from Ui_login import *
import kejitu_rc
from my_style import *
import time
import pandas as pd
import os
class logindialog(QDialog,Ui_Dialog):
    def __init__(self):
        super(logindialog, self).__init__()
        self.setupUi(self)
        # self.buttonBox = QPushButton()
        # self.buttonBox.setText("确定")

        ##### 绑定按钮事件
        self.buttonBox22.clicked.connect(self.accept)

    def accept(self):
        print('执行一次')
        if self.lineEdit.text().strip() == "aa" and self.lineEdit_2.text() == "bb":
            # self.accept()
            super(logindialog, self).accept()
            return 1
        else:
            QMessageBox.warning(self,"警告","用户名或密码错误！")
            print('111')
            self.lineEdit.clear()
            self.lineEdit_2.clear()
        
if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    dialog = logindialog()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/kejitu2/poto/tubiao2.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
    dialog.setWindowIcon(icon)
    # if dialog.exec_()==QDialog.Accepted:
    #     print('13')
    #     RoundProgress = RoundProgress()
    #     RoundProgress.setWindowIcon(icon)
    #     RoundProgress.show()
    #     print('14')
    #     sys.exit(app.exec_())
    #     print('15')
    dialog.show()
    sys.exit(app.exec_())