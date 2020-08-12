from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication,QWidget,QHBoxLayout,QFrame
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
 
class Stacked(QWidget):
    def __init__(self):
        super(Stacked, self).__init__()
        self.initUI()
        self.mainLayout()
 
    def initUI(self):
        self.setGeometry(400,400,800,600)
        self.setWindowTitle("demo1")
 
    def mainLayout(self):
        self.mainhboxLayout = QHBoxLayout(self)
        self.frame = QFrame(self)
        self.mainhboxLayout.addWidget(self.frame)
        self.hboxLayout = QHBoxLayout(self.frame)
        self.myHtml = QWebEngineView()
        url = "http://www.baidu.com"
        #打开本地html文件
        self.myHtml.load(QUrl("file:///D:/360Downloads/Python编程/数据分析+数据可视化/pyecharts/PyQt5+pyecharts/bar1.html"))
        # self.myHtml.load(QUrl("bar1.html"))   #无法显示，要使用绝对地址定位，在地址前面加上 file:/// ，将地址的 \ 改为/
        #打开网页url
        # self.myHtml.load(QUrl(url))
         
        self.hboxLayout.addWidget(self.myHtml)
        self.setLayout(self.mainhboxLayout)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Stacked()
    ex.show()
    sys.exit(app.exec_())