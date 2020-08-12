# -*- coding: utf-8 -*-
# @Time    : 2019/11/17 20:08
# @Author  : dailinqing
# @Email   : dailinqing@126.com
# @File    : print_to_ui.py
# @Software: PyCharm
 
import sys
import time
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QTextEdit
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QThread,QTimer
 
 
 
 
class Stream(QtCore.QObject):
    """Redirects console output to text widget."""
    newText = QtCore.pyqtSignal(str)
 
    def write(self, text):
        self.newText.emit(str(text))
 
 
class QMyWindow(QMainWindow):
    """Main application window."""
    def __init__(self):
        super().__init__()
 
        self.initUI()
 
        # 注掉这句就可以打印到控制台，方便调试
        sys.stdout = Stream(newText=self.onUpdateText)
 
        # 初始化一个定时器
        self.timer = QTimer(self)
        # 将定时器超时信号与槽函数showTime()连接
        self.timer.timeout.connect(self.fun)
 
        self.num = 0
 
 
    def fun(self):
        self.num += 1
        print(self.num)
 
    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.process.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()
 
    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        sys.stdout = sys.__stdout__
        super().closeEvent(event)
 
    def initUI(self):
        """Creates UI window on launch."""
        # Button for generating the master list.
        btn = QPushButton('Run', self)
        btn.move(450, 100)
        btn.resize(100, 100)
        btn.clicked.connect(self.OnBtnClicked)
 
        # Create the text output widget.
        self.process = QTextEdit(self, readOnly=True)
        self.process.ensureCursorVisible()
        self.process.setLineWrapColumnOrWidth(500)
        self.process.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.process.setFixedWidth(400)
        self.process.setFixedHeight(150)
        self.process.move(30, 100)
 
        # Set window size and title, then show the window.
        self.setGeometry(300, 300, 600, 300)
        self.setWindowTitle('print to ui')
        self.show()
 
    def OnBtnClicked(self):
        """Runs the main function."""
 
        print('Running...')
        self.timer.start(1000)
        for nu in list(range(15)):
          print(nu)
        # time.sleep(5)  # time.sleep（）是一个阻塞任务，不允许Qt事件循环运行，从而阻止信号正常工作和GUI更新，解决方案是使用QTimer和QEventLoop替换该GUI睡眠。
        print('Done.')
 
 
if __name__ == '__main__':
    # Run the application.
    app = QApplication(sys.argv)
    # app.aboutToQuit.connect(app.deleteLater)
    gui = QMyWindow()
    print("main")
    sys.exit(app.exec_())