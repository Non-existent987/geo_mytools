import sys
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
from Ui_Stack_Widget import Ui_Dialog
# from PyQt5.QtCore import *
 
# 导入matplotlib模块并使用Qt5Agg
import matplotlib
matplotlib.use('Qt5Agg')
# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtWidgets import QDialog,QApplication
import matplotlib.pyplot as plt
import sys
import numpy as np
from numpy import *
import pandas as pd
import sys,mytools


from descartes import PolygonPatch
from shapely.geometry import Point, Polygon, MultiPolygon

# data = pd.read_csv('C:/Users/Administrator/Desktop/NB.csv',encoding='gbk')
# data_p = mytools.gisn.add_points(data,'经度','纬度')
tu =mytools.gisn.maps()
class Test(QDialog, Ui_Dialog):
    def __init__(self,parent=None):
        super(Test, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
 
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.gridlayout = QGridLayout(self.groupBox)  # 继承容器groupBox
        self.gridlayout.addWidget(self.canvas,0,1)
        self.plot_()
 
    def plot_(self):
        ax = self.figure.add_subplot(111)
        # ax.YAxis.Visible = 'off'
        ax.clear() #每次绘制一个函数时清空绘图
        tu.plot(ax=ax)
        self.canvas.draw()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()
    sys.exit(app.exec_())