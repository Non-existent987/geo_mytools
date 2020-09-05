import sys
from PyQt5 import QtWidgets, QtGui

# 对Qt部件的操作一般都要在创建Qt程序后才能进行
app1 = QtWidgets.QApplication(sys.argv)  
# 创建启动界面，支持png透明图片
splash = QtWidgets.QSplashScreen(QtGui.QPixmap('aaa.png'))
splash.show()
# 可以显示启动信息
splash.showMessage('正在加载……')
# 关闭启动画面
splash.close() 

