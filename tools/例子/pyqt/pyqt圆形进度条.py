import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import *
 
class RoundProgress(QWidget):
 
    def __init__(self):
        super(RoundProgress, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去边框
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.persent = 0
        self.my_thread = MyThread()
        self.my_thread.my_signal.connect(self.parameterUpdate)
        self.my_thread.start()
 
    def parameterUpdate(self, p):
        self.persent = p
 
    def paintEvent(self, event):
        rotateAngle = 360 * self.persent / 100
        # 绘制准备工作，启用反锯齿
        painter = QPainter(self)
        painter.setRenderHints(QtGui.QPainter.Antialiasing)
 
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QBrush(QColor("#5F89FF")))
        painter.drawEllipse(3, 3, 400, 400)  # 画外圆
 
        painter.setBrush(QBrush(QColor("#e3ebff")))
        painter.drawEllipse(5, 5, 396, 396)  # 画内圆
 
        gradient = QConicalGradient(50, 50, 91)
        gradient.setColorAt(0, QColor("#95BBFF"))
        # gradient.setColorAt(1, QColor("#5C86FF"))
        self.pen = QPen()
        self.pen.setBrush(gradient)  # 设置画刷渐变效果
        self.pen.setWidth(8)
        self.pen.setCapStyle(Qt.RoundCap)
        painter.setPen(self.pen)
        painter.drawArc(QtCore.QRectF(4, 4, 398, 398), (90 - 0) * 16, -rotateAngle * 16)  # 画圆环
 
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(25)
        # font.SET
        painter.setFont(font)
        painter.setPen(QColor("#5481FF"))
        painter.drawText(QtCore.QRectF(4, 4, 398, 398), Qt.AlignCenter, "%d%%" % self.persent)  # 显示进度条当前进度
        self.update()
 
class MyThread(QThread):
    my_signal = pyqtSignal(int)
    p = 0
    def __init__(self):
        super(MyThread, self).__init__()
 
    def run(self):
        while self.p < 100:
            self.p += 1
            self.my_signal.emit(self.p)
            self.msleep(100)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    RoundProgress = RoundProgress()
    RoundProgress.show()
    sys.exit(app.exec_())