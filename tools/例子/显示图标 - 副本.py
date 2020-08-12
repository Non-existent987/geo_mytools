#coding:utf-8

# 导入必要的模块
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets,QtGui
import matplotlib.pyplot as plt
import sys,mytools
import pandas as pd
data = pd.read_csv('C:/Users/Administrator/Desktop/NB.csv',encoding='gbk')
data_p = mytools.gisn.add_points(data,'经度','纬度')

class My_Main_window(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(My_Main_window,self).__init__(parent)
        # 重新调整大小
        self.resize(800, 659)
        # 添加菜单中的按钮
        self.menu = QtWidgets.QMenu("绘图")
        self.menu_action = QtWidgets.QAction("绘制",self.menu)
        self.menu.addAction(self.menu_action)
        self.menuBar().addMenu(self.menu)
        # 添加事件
        self.menu_action.triggered.connect(self.plot_2)
        self.setCentralWidget(QtWidgets.QWidget())
    # 绘图方法
    def plot_2(self):
        # 清屏
        cavans = data_p.plot()
        print(cavans)
        # 将绘制好的图像设置为中心 Widget
        self.setCentralWidget(cavans)
    # 绘图方法
    def plot_(self):
        # 清屏
        plt.cla()
        # 获取绘图并绘制
        fig = plt.figure()
        ax =fig.add_axes([0.1,0.1,0.8,0.8])
        ax.set_xlim([-1,6])
        ax.set_ylim([-1,6])
        ax.plot([0,1,2,3,4,5],'o--')
        cavans = FigureCanvas(fig)
        print(cavans)
        # 将绘制好的图像设置为中心 Widget
        self.setCentralWidget(cavans)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = My_Main_window()
    main_window.show()
    app.exec()
