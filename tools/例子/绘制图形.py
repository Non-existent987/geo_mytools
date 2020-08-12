import sys,math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
class DrawAll(QWidget):
    def __init__(self):
        super(DrawAll, self).__init__()
        self.setWindowTitle("绘制各种图形")
        self.resize(300, 300)
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        # qp.setPen(Qt.blue)
        qp.setPen(Qt.red)
        # qp.drawArc(120, 10, 100, 100, 0, 360 * 16)
        point1 = QPoint(140, 380)
        point2 = QPoint(270, 420)
        point3 = QPoint(290, 512)
        point4 = QPoint(290, 588)
        point5 = QPoint(200, 533)
        polygon = QPolygon([point1, point2, point3, point4, point5])
        qp.drawPolygon(polygon)
        # 绘制弧
        # 先选定绘制区域，绘制区域为矩形（QRect）
        # 左上角坐标为(0, 10), 长为100， 宽为100
        # rect = QRect(0, 10, 100, 100)
        # # 弧为圆的一部分，角度的单位是alen:1个alen等于1/16度
        # # 下面在rect代表的区域中绘制，起始角度为0，终止角度为50度(50 * 16 alen)

        # qp.drawArc(rect, 0, 50 * 16)
        qp.end()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = DrawAll()
    main.show()
    sys.exit(app.exec_())