import sys
from PyQt5.QtCore import *
from tools import *
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QHBoxLayout,QGraphicsDropShadowEffect, QPushButton,  QComboBox,QMessageBox,QCommandLinkButton,QMainWindow
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
import kejitu_rc
from my_style import *
import time
import pandas as pd
import os
import cgitb
cgitb.enable( format = 'text')
class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')
    # write()函数这样写，每调用一次就写到记录文件中，不需要等待程序运行结束。
    def write(self, message):
        self.terminal.write(message)
        self.terminal.flush()
        self.log.write(message)
        self.log.flush()

    def flush(self):
        pass
sys.stdout = Logger('output.log', sys.stdout)
sys.stderr = Logger('output.log_file', sys.stderr)      # redirect std err, if necessary
def tm():
    return time.strftime("%Y-%m-%d %H:%M:%S")+':'
#输出控制台的主要信号发送
class EmittingStr(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str) #定义一个发送str的信号
    def write(self, text):
      self.textWritten.emit(str(text)) 
#主窗体类
class RoundProgress(QWidget,Ui_dn):
    name_linshi1 = 'C:/'
    def __init__(self):
        super(RoundProgress, self).__init__()
        self.setupUi(self)
        #读取上次目录
        if os.path.isfile("config.ini"):
            self.init_login_info()
        #添加一个gif动画 
        # self.widget_7.setStyleSheet("border-image: url(:/kejitu2/poto/zhineng_zhonglou.png);")
        self.movie = QMovie(":/kejitu2/poto/tongtai1.gif")
        self.label.setMovie(self.movie)
        # self.label.setAlignment()
        # setAlignment(Qt::Alignment align)
        self.movie.start()


        #按钮返回主页
        self.commandLinkButton.released.connect(self.zhuye)
        self.commandLinkButton_2.released.connect(self.zhuye)
        self.commandLinkButton_3.released.connect(self.zhuye)
        self.commandLinkButton_4.released.connect(self.zhuye)
        self.commandLinkButton_5.released.connect(self.zhuye)
        self.commandLinkButton_6.released.connect(self.zhuye)
        self.commandLinkButton_7.released.connect(self.zhuye)
        self.commandLinkButton_15.released.connect(self.zhuye)
        self.pushButton_41.released.connect(self.zhuye)
        

        #最小化和关闭
        self.pushButton_3.clicked.connect(self.closeEvent)
        self.pushButton.clicked.connect(self.pushButton_c)

        #按钮切换页面
        self.pushButton_4.released.connect(self.qiehuan)
        self.pushButton_9.released.connect(self.qiehuan)
        self.pushButton_2.released.connect(self.qiehuan)
        self.pushButton_24.released.connect(self.qiehuan)
        self.pushButton_5.released.connect(self.qiehuan)
        self.pushButton_21.released.connect(self.qiehuan)
        self.pushButton_25.released.connect(self.qiehuan)
        self.yunxing.released.connect(self.qiehuan)
        self.B_wenti.released.connect(self.qiehuan)
        self.pushButton_12.released.connect(self.qiehuan)
        self.B_jizhan.released.connect(self.qiehuan)
        self.commandLinkButton_16.released.connect(self.qiehuan)
        


        #控制台输出用# 下面将输出重定向到textBrowser中
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)

        #--样式设置--
        self.pushButton_4.setStyleSheet(MyStyleSheet.button_style_tupian_1())
        self.pushButton_9.setStyleSheet(MyStyleSheet.button_ico_1())
        self.pushButton_2.setStyleSheet(MyStyleSheet.button_ico_2())
        self.pushButton_24.setStyleSheet(MyStyleSheet.button_ico_3())
        self.pushButton_5.setStyleSheet(MyStyleSheet.button_ico_4())
        self.pushButton_21.setStyleSheet(MyStyleSheet.button_ico_5())
        self.pushButton_25.setStyleSheet(MyStyleSheet.button_ico_6())

        #最小化和关闭样式
        self.pushButton_3.setStyleSheet(MyStyleSheet.my_style_1())
        self.pushButton.setStyleSheet(MyStyleSheet.my_style_1())

        #yunxing 样式
        self.yunxing.setStyleSheet(MyStyleSheet.button_style())
        self.yunxing_5.setStyleSheet(MyStyleSheet.button_style())
        self.yunxing_12.setStyleSheet(MyStyleSheet.button_style())
        self.yunxing_13.setStyleSheet(MyStyleSheet.button_style())
        self.yunxing_7.setStyleSheet(MyStyleSheet.button_style())
        self.yunxing_8.setStyleSheet(MyStyleSheet.button_style())
        self.yunxing_9.setStyleSheet(MyStyleSheet.button_style())
        self.yunxing_10.setStyleSheet(MyStyleSheet.button_style())
        self.yunxing_11.setStyleSheet(MyStyleSheet.button_style())
        # self.B_jizhan.setStyleSheet(MyStyleSheet.button_style_z())
        # self.B_wenti.setStyleSheet(MyStyleSheet.button_style_z())

        #导入数据样式
        self.B_jizhan.setStyleSheet(MyStyleSheet.button_style_z())
        self.B_wenti.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_12.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_28.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_29.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_26.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_27.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_10.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_14.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_15.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_17.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_18.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_13.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_19.setStyleSheet(MyStyleSheet.button_style_z())

        self.label_35.setStyleSheet(MyStyleSheet.textBrowser_8_sty())
        self.label_13.setStyleSheet(MyStyleSheet.textBrowser_8_sty())
        self.label.setStyleSheet(MyStyleSheet.textBrowser_8_sty())
        self.textBrowser_7.setStyleSheet(MyStyleSheet.textBrowser_7_sty())
        self.widget_2.setStyleSheet(MyStyleSheet.button_style_widget_bian2())
        self.widget_3.setStyleSheet(MyStyleSheet.button_style_widget_bian3())
        self.widget_bian.setStyleSheet(MyStyleSheet.main_sty())
        self.setWindowOpacity(0.99)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.shadow = QGraphicsDropShadowEffect(self.widget_bian)#添加阴影
        self.shadow.setBlurRadius(8)#阴影半径
        self.shadow.setOffset(0, 0)#阴影偏移x y
        self.shadow.setColor(QColor("#444444"))
        self.shadow.setXOffset(0)#阴影偏移
        self.shadow.setYOffset(2)#添加阴影
        self.widget_bian.setGraphicsEffect(self.shadow)#添
        self.gridLayout.setSpacing(0)#模块间隔
        op = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op.setOpacity(0)
        self.pushButton_41.setGraphicsEffect(op)
        
        # self.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)  # dockWidget控件指定区域
        # self.dockWidget.hide()


    def yincang(self,i=1):
        if i==1:
            self.commandLinkButton_15.setVisible(True)
            self.label.setVisible(False)
            self.label_13.setVisible(False)
            self.label_35.setVisible(False)
        else:
            self.commandLinkButton_15.setVisible(False)
            self.label.setVisible(True)
    #--无边框模式移动--
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            try:
                self.m_flag = True
                self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
                event.accept()
                self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标
            except:
                pass
    def mouseMoveEvent(self, QMouseEvent):
        try:
            if Qt.LeftButton and self.m_flag:
                self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
                QMouseEvent.accept()
        except:
            pass
    def mouseReleaseEvent(self, QMouseEvent):
        try:
            self.m_flag = False
            self.setCursor(QCursor(Qt.ArrowCursor))
        except:
            pass

    #--关闭和最小化按钮函数--
    def closeEvent(self):#函数名固定不可变
        reply=QMessageBox.question(self,u'警告',u'确认退出?',QMessageBox.Yes,QMessageBox.No)
        if reply==QMessageBox.Yes:
            try:
                print('os guanbi')
                os._exit(5) 
            except Exception as e:
                print('yuanlaide close guanbi')
                self.close()
        else:
            pass
    def pushButton_c(self):
        """
        最小化窗口
        """
        self.showMinimized()
    #控制台输出用
    def outputWritten(self, text):
        cursor = self.textBrowser_7.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser_7.setTextCursor(cursor)
        self.textBrowser_7.ensureCursorVisible()
    #返回主页函数
    def zhuye(self):
        self.stackedWidget.setCurrentIndex(0)
    #切换页面函数
    def qiehuan(self):
        sending_button = self.sender()
        MyThread.sending_button=sending_button.objectName()
        print(sending_button.objectName())
        if self.pushButton_4.objectName() == sending_button.objectName():
            self.stackedWidget.setCurrentIndex(1)    
        if self.yunxing.objectName() == sending_button.objectName():
            self.yincang(0)
            self.stackedWidget.setCurrentIndex(8) 
            self.yunxing_sheet_0()

        if self.pushButton_9.objectName() == sending_button.objectName():
            self.stackedWidget.setCurrentIndex(5) 
        if self.pushButton_2.objectName() == sending_button.objectName():
            self.stackedWidget.setCurrentIndex(4) 
        if self.pushButton_24.objectName() == sending_button.objectName():
            self.stackedWidget.setCurrentIndex(6) 
        if self.pushButton_5.objectName() == sending_button.objectName():
            self.stackedWidget.setCurrentIndex(2) 
        if self.pushButton_21.objectName() == sending_button.objectName():
            self.stackedWidget.setCurrentIndex(3) 
        if self.pushButton_25.objectName() == sending_button.objectName():
            self.stackedWidget.setCurrentIndex(7) 
        if self.B_wenti.objectName() == sending_button.objectName():
            self.xuanze_file_wenti()
        if self.pushButton_12.objectName() == sending_button.objectName():
            self.xuanze_file_guihua()
        if self.B_jizhan.objectName() == sending_button.objectName():
            self.xuanze_file_xianwang()
        if self.commandLinkButton_16.objectName() == sending_button.objectName():
            self.stackedWidget.setCurrentIndex(8) 
            self.yincang(1)
            
    def gengxin(self,i):
        if i ==0: 
            QMessageBox.information(self, "提示", "数据计算完成，结果存放在{}/目录中。".format(os.path.split(MyThread.data_wenti_file)[0]))
            self.stackedWidget.setCurrentIndex(1)
    #多线程信号传递使用
    def jindutiao(self):
        print(tm(),'程序开始：')
        print(tm(),'开始多线程')
        self.thread_1 = MyThread()# 创建线程
        self.thread_1.my_signal.connect(self.gengxin)# 连接信号
        self.thread_1.start()# 开始线程
        # gengxin(self.thread_1.my_signal)
    def xxx2(self,ss, vv=['ca']):
        nu_x = 0
        a = 0
        for x in enumerate(ss):
            for vv_t in vv:
                if vv_t in x[1]:
                    nu_x = x[0]
                    a = 1
                    break
            if a == True:
                break
        if a == False:
            nu_x = 0
        return nu_x
    def comboBox_chuli(self,lie_t = 'lie',
            comboBox_dict = {
            'comboBox_39':['cgi','小区','cell','id'],
            'comboBox_41':['lon','经度'],
            'comboBox_39':['名','cell','id']
            }
            ):
        for comboBox_t in comboBox_dict:
            f = getattr(self,comboBox_t)
            f.clear()
            f.addItems(lie_t) 
            f.setCurrentIndex(self.xxx2(lie_t, vv=comboBox_dict[comboBox_t]))
    # 保存登录信息
    def save_login_info(self):
        settings = QSettings("config.ini", QSettings.IniFormat)        #方法1：使用配置文件
        #settings = QSettings("mysoft","myapp")                        #方法2：使用注册表
        settings.setValue("file_name",self.name_linshi1)
    # 初始化登录信息
    def init_login_info(self):
        settings = QSettings("config.ini", QSettings.IniFormat)        #方法1：使用配置文件
        #settings = QSettings("mysoft","myapp")                        #方法2：使用注册表
        self.name_linshi1 =settings.value("file_name")

    #---------------数据处理函数----------------
    #打开文件
    def openfile2(self):
        filename = QFileDialog.getOpenFileName(self,
                   'Open File', 'c:/', 'Images (*.xlsx , *.xls, *.csv)',QFileDialog.DontUseNativeDialog)
    def openfile(self):
        self.name_linshi1 = os.path.split(self.name_linshi1)[0]
        print(tm(),'打开路径为',self.name_linshi1)
        try:
            file, ok = QFileDialog.getOpenFileName(self, "打开", self.name_linshi1,"one files (*.xlsx , *.xls, *.csv)")
            self.name_linshi1 = file
            self.save_login_info()
            print('ok',ok,'file:',file)
            if 'csv' in(file):
                print('csv')
                try:
                    data_ttt = pd.read_csv(open(file, encoding='gbk'))  # panda
                    # QMessageBox.about(self, "标题", "选择数据成功")
                except:
                    data_ttt = pd.read_csv(open(file))  # pandas
                    # QMessageBox.about(self, "标题", "选择数据成功")
            elif 'xls' in (file):
                print('excel')
                try:
                    print(tm(),'尝试使用gbk代开excel')
                    data_ttt = pd.read_excel(file, encoding='gbk')
                    # QMessageBox.about(self, "标题", "选择excel数据成功")
                    print(tm(),'excel使用gbk打开成功')
                except:
                    print(tm(),'尝试使用utf8代开excel')
                    data_ttt = pd.read_excel(file, encoding="utf-8", )
                    # QMessageBox.about(self, "标题", "选择excel数据成功")
                    print(tm(),'Excel使用utf8打开成功')
            return [data_ttt,file]
        except:
            QMessageBox.warning(self, "标题", "选择数据有误")
            return ['open_false','open_false']

    #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-----↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-----↓↓↓↓↓↓↓↓↓制定方案-开始-↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    def xuanze_file_wenti(self):
        print(tm(),'开始打开问题小区数据') 
        MyThread.data_wenti,file_name_zz = self.openfile()
        if file_name_zz=='open_false':
            pass
        else:
            MyThread.data_wenti_file = file_name_zz
            print(tm(),file_name_zz)
            print(tm(),'问题小区所在的目录',MyThread.data_wenti_file)
            lie_wenti = MyThread.data_wenti.columns.values  # pandas
            self.comboBox_chuli(lie_t = lie_wenti,
                comboBox_dict = {
                'comboBox_45':['CGI','cgi','id','小区名'],
                'comboBox_47':['lon','经度'],
                'comboBox_46':['lat','纬度'],
                'comboBox_48':['方位','az'],
                'comboBox_49':['区域类型','场景'],
                'comboBox_44':['频段','制式'],
                'comboBox_51':['挂高','高','high'],
                'comboBox_52':['下倾','倾角'],
                'comboBox_50':['故障', '告警','状态','统计分类']
                }
                )
            print(tm(),'打开文件完成')
            print(tm(),MyThread.data_wenti.shape)
            QMessageBox.about(self, "标题", "选择数据成功")
    def xuanze_file_xianwang(self):
        print(tm(),'开始打开现网小区数据') 
        MyThread.data_xianwang,file_name_zz = self.openfile()
        if file_name_zz=='open_false':
            pass
        else:
            MyThread.data_xianwang_file = file_name_zz
            print(tm(),file_name_zz)
            print(tm(),'现网小区所在的目录',MyThread.data_xianwang_file)
            lie_wenti = MyThread.data_xianwang.columns.values  # pandas
            self.comboBox_chuli(lie_t = lie_wenti,
                comboBox_dict = {
                'comboBox_112':['CGI','cgi','id','小区名'],
                'comboBox_114':['lon','经度'],
                'comboBox_113':['lat','纬度'],
                'comboBox_115':['频段','制式'],
                'comboBox_117':['挂高','高','high'],
                'comboBox_116':['故障', '告警','状态','统计分类']
                }
                )
            print(tm(),'打开文件完成')
            print(tm(),MyThread.data_xianwang.shape)
            QMessageBox.about(self, "标题", "选择数据成功")
    def xuanze_file_guihua(self):
        print(tm(),'开始打开规划数据数据') 
        MyThread.data_guihua,file_name_zz = self.openfile()
        if file_name_zz=='open_false':
            pass
        else:
            MyThread.data_guihua_file = file_name_zz
            print(tm(),file_name_zz)
            print(tm(),'规划数据所在的目录',MyThread.data_guihua_file)
            lie_wenti = MyThread.data_guihua.columns.values  # pandas
            self.comboBox_chuli(lie_t = lie_wenti,
                comboBox_dict = {
                'comboBox_80':['id','站名','号'],
                'comboBox_82':['lon','经度'],
                'comboBox_81':['lat','纬度'],
                'comboBox_83':['频段','制式'],
                'comboBox_84':['工期','期']
                }
                )
            print(tm(),'打开文件完成')
            print(tm(),MyThread.data_guihua.shape)
            QMessageBox.about(self, "标题", "选择数据成功")
    def yunxing_sheet_0(self):
        
        print(tm(),'选择的问题、现网和规划数据都应大于1条，目前的情况如下：问题{}条，规划{}条，现网{}条，'.format(MyThread.data_wenti.shape[0],MyThread.data_guihua.shape[0],MyThread.data_xianwang.shape[0]))
        if (MyThread.data_guihua.shape[0]>1) & (MyThread.data_xianwang.shape[0]>1)& (MyThread.data_wenti.shape[0]>1):
            #获取所有参数的值x（问题小区）
            print(tm(),'获取选择值')
            print(tm(),'问题小区数据共计',MyThread.data_wenti.shape)
            print(tm(),'现网小区数据共计',MyThread.data_xianwang.shape)
            print(tm(),'规划数据共计',MyThread.data_guihua.shape)
            print(tm(),'开始传递参数')
            MyThread.wenti_id = self.comboBox_45.currentText()  # 获取下拉菜单的值
            MyThread.wenti_lon = self.comboBox_47.currentText()  # 获取下拉菜单的值
            MyThread.wenti_lat = self.comboBox_46.currentText()  # 获取下拉菜单的值
            MyThread.wenti_fw = self.comboBox_48.currentText()  # 获取下拉菜单的值
            MyThread.wenti_cj = self.comboBox_49.currentText()  # 获取下拉菜单的值
            MyThread.wenti_zs = self.comboBox_44.currentText()  # 获取下拉菜单的值
            MyThread.wenti_gg = self.comboBox_51.currentText()  # 获取下拉菜单的值
            MyThread.wenti_xq = self.comboBox_52.currentText()  # 获取下拉菜单的值
            MyThread.wenti_gz = self.comboBox_50.currentText()  # 获取下拉菜单的值
            MyThread.text_guzhang = self.lineEdit_72.text()# 获取单行输入框
            MyThread.text_900_hx = self.lineEdit_90.text()# 获取单行输入框
            MyThread.text_900_yb = self.lineEdit_93.text()# 获取单行输入框
            MyThread.text_900_cj = self.lineEdit_89.text()# 获取单行输入框
            MyThread.text_900_xc = self.lineEdit_92.text()# 获取单行输入框
            MyThread.text_900_xz = self.lineEdit_85.text()# 获取单行输入框
            MyThread.text_900_nc = self.lineEdit_83.text()# 获取单行输入框
            MyThread.text_1800_hx = self.lineEdit_87.text()# 获取单行输入框
            MyThread.text_1800_yb = self.lineEdit_86.text()# 获取单行输入框
            MyThread.text_1800_cj = self.lineEdit_84.text()# 获取单行输入框
            MyThread.text_1800_xc = self.lineEdit_82.text()# 获取单行输入框
            MyThread.text_1800_xz = self.lineEdit_91.text()# 获取单行输入框
            MyThread.text_1800_nc = self.lineEdit_88.text()# 获取单行输入框
            MyThread.text_fb = self.lineEdit_81.text()# 获取单行输入框
            MyThread.text_g_g = self.lineEdit_94.text()# 获取单行输入框
            MyThread.text_g_d = self.lineEdit_97.text()# 获取单行输入框
            MyThread.text_x_x = self.lineEdit_95.text()# 获取单行输入框
            MyThread.text_x_d = self.lineEdit_96.text()# 获取单行输入框
            MyThread.gongzhijuli = self.spinBox_7.value() #获取计数器的值
            MyThread.bobankuandu = self.spinBox_9.value() #获取计数器的值
            MyThread.text_guzhang = self.lineEdit_72.text()# 获取单行输入框
            MyThread.text_guzhang = self.lineEdit_72.text()# 获取单行输入框
            MyThread.text_guzhang = self.lineEdit_72.text()# 获取单行输入框
            MyThread.xz_wenti_guagao = self.radioButton_26.isChecked()  # 是否选中故障
            MyThread.xz_wenti_guzhang = self.radioButton_25.isChecked()  # 是否选中故障
            print(tm(),'问题小区传递参数完成')
            print(tm(),'开始现网小区传递参数')
            MyThread.xianwang_id = self.comboBox_112.currentText()  # 获取下拉菜单的值
            MyThread.xianwang_lon = self.comboBox_114.currentText()  # 获取下拉菜单的值
            MyThread.xianwang_lat = self.comboBox_113.currentText()  # 获取下拉菜单的值
            MyThread.xianwang_zs = self.comboBox_115.currentText()  # 获取下拉菜单的值
            MyThread.xianwang_gg = self.comboBox_117.currentText()  # 获取下拉菜单的值
            MyThread.xianwang_gz = self.comboBox_116.currentText()  # 获取下拉菜单的值

            MyThread.text_xw_guagao_d = self.lineEdit_98.text()# 获取单行输入框
            MyThread.text_xw_guzhang = self.lineEdit_121.text()# 获取单行输入框
            MyThread.xz_xw_guagao = self.radioButton_42.isChecked()  # 是否选中故障
            MyThread.xz_xw_guzhang = self.radioButton_41.isChecked()  # 是否选中故障
            print(tm(),'现网小区传递参数完成')
            print(tm(),'开始规划数据传递参数')
            MyThread.guihua_id = self.comboBox_80.currentText()  # 获取下拉菜单的值
            MyThread.guihua_lon = self.comboBox_82.currentText()  # 获取下拉菜单的值
            MyThread.guihua_lat = self.comboBox_81.currentText()  # 获取下拉菜单的值
            MyThread.guihua_zs = self.comboBox_83.currentText()  # 获取下拉菜单的值
            MyThread.guihua_gq = self.comboBox_84.currentText()  # 获取下拉菜单的值

            print(tm(),'规划数据传递参数完成')

# ------------------------------------------------------------                
            print(tm(),'处理数据线程开始')
            self.jindutiao()
            
            # self.stackedWidget.setCurrentIndex(1)  
            # QMessageBox.about(self, "标题",'完成输出至文件源目录' )
        else:
            QMessageBox.warning(self, "标题", "请选择有效数据后执行") 
            self.stackedWidget.setCurrentIndex(1)         
        

    #↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-----↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-----↑↑↑↑↑↑↑↑↑↑↑↑制定方案-完成-↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
#另外一个处理数据的线程
class MyThread(QThread):
    my_signal = pyqtSignal(int)# 更新进度条
    data_wenti =data_xianwang=data_guihua=  pd.DataFrame()
    data_wenti_file =data_xianwang_file=data_guihua_file= ''
    #问题点变量
    wenti_id=wenti_lon=wenti_lat=wenti_fw=wenti_cj=wenti_zs=wenti_gg=wenti_xq=wenti_gz=text_guzhang=text_900_hx=text_900_yb=text_900_cj=text_900_xc=text_900_xz=text_900_nc=text_1800_hx=text_1800_yb=text_1800_cj=text_1800_xc=text_1800_xz=text_1800_nc=text_fb=text_g_g=text_g_d=text_x_x=text_x_d=gongzhijuli=bobankuandu=text_guzhang=text_guzhang=text_guzhang=xz_wenti_guagao=xz_wenti_xiaqing=xz_wenti_guzhang=''    # p = 0
    #记录那个按钮被按下
    sending_button=''
    #现网小区变量
    xianwang_id=xianwang_lon=xianwang_lat=xianwang_zs=xianwang_gg=xianwang_gz=text_xw_guagao_d=text_xw_guzhang=xz_xw_guagao=xz_xw_guzhang=''
    #规划站变量
    guihua_id=guihua_lon=guihua_lat=guihua_zs=guihua_gq=''
    def __init__(self):
        super(MyThread, self).__init__()

    #重新run函数，执行MyThread.start()的时候就会执行run
    def run(self):
        self.my_signal.emit(10)  # 发送进度条的值 信号
        self.bClicked()
    #没啥用 一个结构的函数
    def bClicked(self):
        print(tm(),'Begin')
        self.printABCD()
        print(tm(),'处理数据线程结束')
        print(tm(),"End")


    #-------------------------处理数据
    #主要处理数据的函数
    def printABCD(self):
        print(tm(),'按下按钮的名称',self.sending_button)
        if self.sending_button == 'yunxing':
            #--------------------------------优化方案制定--------------------------
            print(tm(),"----------------------开始计算方案输出程序需---------------------")
            print(tm(),"copy导入的数据")
            data_wenti_cp = self.data_wenti.copy()
            print(tm(),"选择使用的列")
            data_wenti_cp = data_wenti_cp[[self.wenti_id,self.wenti_lon,self.wenti_lat,self.wenti_fw,self.wenti_cj,self.wenti_zs,self.wenti_gg,self.wenti_xq,self.wenti_gz]]
            data_wenti_cp.columns=['问题ID','问题经度','问题纬度','问题方位角','问题场景','问题制式','问题挂高','问题下倾','问题故障']
            #空值制替换为无
            print(tm(),"空值制替换为无-问题ID-问题故障-开始")
            data_wenti_cp['问题ID'] = data_wenti_cp['问题ID'].fillna('无')
            data_wenti_cp['问题故障'] = data_wenti_cp['问题故障'].fillna('无')
            print(tm(),"空值制替换为无-问题ID-问题故障-完成")
            data_xianwang_cp = self.data_xianwang.copy()
            print(tm(),"选择使用的列")
            data_xianwang_cp = data_xianwang_cp[[self.xianwang_id,self.xianwang_lon,self.xianwang_lat,self.xianwang_zs,self.xianwang_gg,self.xianwang_gz]]
            data_xianwang_cp.columns=['现网ID','现网经度','现网纬度','现网制式','现网挂高','现网故障']
            print(tm(),"空值制替换为无-现网故障-开始")
            data_xianwang_cp['现网故障'] = data_xianwang_cp['现网故障'].fillna('无')
            print(tm(),"空值制替换为无-现网故障-完成")
            print(tm(),"---------------------------优化方案制定-----------------------")
            data_guihua_cp = self.data_guihua.copy()
            print(tm(),"问题点数据根据场景制式计算距离-开始...")
            data_wenti_cp_juli = changjing_distance(data_wenti_cp,'问题场景','问题制式')
            print(tm(),"问题点数据根据场景制式计算距离-完成")
            print(tm(),"问题点数据-根据经纬度、方位角、距离等算法制作扇区-开始...")
            data_wenti_cp_sq = add_sectors_df(data_wenti_cp_juli,
                    coords=['问题经度','问题纬度','d_height','问题方位角','distance'],has_z=False,
                    shape_dict={'beam': int(self.bobankuandu),'per_degree': 10})
            print(tm(),"问题点数据-根据经纬度、方位角、距离等算法制作扇区-完成{}个扇区制作".format(data_wenti_cp_sq.shape[0]))
            print(tm(),"现网小区数据根据经纬度数据制作点-开始...")
            data_xianwang_p = add_points(data_xianwang_cp,lon='现网经度',lat='现网纬度')
            print(tm(),"现网小区数据根据经纬度数据制作点-完成{}个点图制作".format(data_xianwang_p.shape[0]))
            print(tm(),"问题点根据gis地理位置匹配现网小区-开始...")
            wenti_sjoin_xianwang = gpd.sjoin(data_wenti_cp_sq,data_xianwang_p)
            print(tm(),"问题点根据gis地理位置匹配现网小区-完成")
            print(tm(),"问题点匹配现网小区，共计匹配{}条有重复的数据".format(wenti_sjoin_xianwang.shape[0]))
            print(tm(),"删除geometry,index_right")
            print(wenti_sjoin_xianwang.columns)
            wenti_sjoin_xianwang = wenti_sjoin_xianwang.drop(columns=['geometry','index_right'])
            print(tm(),"删除geometry,index_right完成")
            print(tm(),'gpd.sjoin后的数量',wenti_sjoin_xianwang.shape)
            print(tm(),"数据格式转换-开始")
            wenti_sjoin_xianwang['问题经度']=pd.to_numeric(wenti_sjoin_xianwang['问题经度'])
            wenti_sjoin_xianwang['问题纬度']=pd.to_numeric(wenti_sjoin_xianwang['问题纬度'])
            wenti_sjoin_xianwang['现网经度']=pd.to_numeric(wenti_sjoin_xianwang['现网经度'])
            wenti_sjoin_xianwang['现网纬度']=pd.to_numeric(wenti_sjoin_xianwang['现网纬度'])
            print(tm(),"数据格式转换-完成")
            wenti_sjoin_xianwang=distancea_df(wenti_sjoin_xianwang,'问题经度', '问题纬度', '现网经度', '现网纬度',columns_name='问题和现网距离')
            print(tm(),'开始剔除共址小区')
            wenti_sjoin_xianwang = wenti_sjoin_xianwang.reset_index(drop=True)
            wenti_sjoin_xianwang2 = wenti_sjoin_xianwang.drop(
            wenti_sjoin_xianwang[(wenti_sjoin_xianwang['问题和现网距离'] < int(self.gongzhijuli))& ((wenti_sjoin_xianwang['现网制式'] != 'FDD900')|(wenti_sjoin_xianwang['问题制式'] == 'FDD900'))].index) 
            print(tm(),'剔除共址小区完成，剔除前的数量为：',wenti_sjoin_xianwang.shape,'剔除后的数量为：',wenti_sjoin_xianwang2.shape)
            print(tm(),"---------------------------优化每个小方案得分计算-----------------------")
            print(tm(),'开始计算得分')
            print(tm(),'复制一份数据')
            sjoin_w_x = wenti_sjoin_xianwang2.copy()
            print(tm(),'设置最低分50')

            sjoin_w_x['优化得分'] = 50
            sjoin_w_x['方案类型'] = '优化'
            print(tm(),'靠近问题点的这半边得70分')
            sjoin_w_x.loc[(sjoin_w_x['distance']/sjoin_w_x['问题和现网距离']>2),'优化得分']=sjoin_w_x.loc[(sjoin_w_x['distance']/sjoin_w_x['问题和现网距离']>2),'优化得分']+15
            #得分计算基础
            print(tm(),'制式为空的用TDD填充')
            sjoin_w_x['现网制式'].fillna('TDD', inplace=True)
            sjoin_w_x['问题制式'].fillna('TDD', inplace=True)
            sjoin_w_x.loc[(sjoin_w_x['现网制式'].str.contains('FDD900')), '优化得分']=sjoin_w_x.loc[(sjoin_w_x['现网制式'].str.contains('FDD900')), '优化得分'] + 5
            print(tm(),'开始计算完成')

            print(tm(),'判断是否弃用现网挂高')
            if self.xz_xw_guagao == True:
                try:
                    print(tm(),'********  现网挂高选用，参与计算，删除挂高过低的现网站点,计算开始')
                    print(tm(),'判断是否为数字')
                    sjoin_w_x['现网挂高'] = pd.to_numeric(sjoin_w_x['问题挂高'])
                    print(tm(),'现网挂高列为数字')
                    sjoin_w_x.drop(sjoin_w_x.loc[sjoin_w_x['现网挂高']<int(self.text_xw_guagao_d)].index)    
                    print(tm(),'现网挂高选用，参与计算，删除挂高过低的现网站点,计算完成')
                except:
                    print(tm(),'！！！！！！！！！！！！！现网挂高中有非数字内容，请核查数据！！！！！！！！！！！')
                    QMessageBox.warning(self, "标题", "现网挂高中有非数字内容，请核查数据！")
                    assert 0
            else:
                sjoin_w_x=sjoin_w_x.drop(columns=['现网挂高'])
            print(tm(),'判断是否弃用现网故障')
            if self.xz_xw_guzhang==True:
                try:
                    print(tm(),"********  空值制替换为无-现网故障-开始")
                    sjoin_w_x['现网故障'] = sjoin_w_x['现网故障'].fillna('无')
                    print(tm(),"空值制替换为无-现网故障-完成")
                    print(tm(),'现网故障选用，参与计算，对周边有故障的小区进行打分,计算开始')
                    sjoin_w_x.loc[sjoin_w_x['现网故障'].str.contains(self.text_guzhang),'优化得分']=sjoin_w_x.loc[sjoin_w_x['现网故障'].str.contains(self.text_guzhang),'优化得分']+16
                    sjoin_w_x.loc[sjoin_w_x['现网故障'].str.contains(self.text_guzhang),'方案类型']='故障-周边站点故障'
                    print(tm(),'现网故障选用，参与计算，对周边有故障的小区进行打分,计算完成')
                except:
                    print(tm(),'！！！！！！！！！！！！！现网现网故障列内容错误，请核查数据！！！！！！！！！！！')
                    QMessageBox.warning(self, "标题", "现网现网故障列内容错误，请核查数据！")
                    assert 0
            else:
                sjoin_w_x=sjoin_w_x.drop(columns=['现网故障'])
            print(tm(),'判断是否弃用问题挂高和下倾')
            if self.xz_wenti_guagao == True:
                try:
                    print(tm(),'********  挂高和下倾选用，参与计算，增加两项自由化数据,计算开始')
                    print(tm(),'判断是否为数字')
                    data_wenti_cp['问题挂高'] = pd.to_numeric(data_wenti_cp['问题挂高'])
                    data_wenti_cp['问题下倾'] = pd.to_numeric(data_wenti_cp['问题下倾'])
                    print(tm(),'挂高和下倾列为数字')
                    add_data1 = data_wenti_cp.loc[(data_wenti_cp['问题挂高']>int(self.text_g_g)) & (data_wenti_cp['问题下倾']<int(self.text_x_x))]
                    add_data2 = data_wenti_cp.loc[(data_wenti_cp['问题挂高']<int(self.text_g_d)) & (data_wenti_cp['问题下倾']>int(self.text_x_d))]
                    print(tm(),'其中满足条件的数据有',add_data1.shape[0],add_data2.shape[0])
                    add_data1['优化得分']=75
                    add_data2['优化得分']=75
                    add_data1['方案类型']='优化-自身挂高和下倾问题'
                    add_data2['方案类型']='优化-自身挂高和下倾问题'
                    print(tm(),'挂高和下倾选用，参与计算，增加两项自优化数据，计算完成')
                    print(tm(),'结果增加至sjoin_w_x',add_data1.shape[0],add_data2.shape[0])
                    sjoin_w_x=sjoin_w_x.append(add_data1)
                    print(tm(),'结果增加至sjoin_w_x完成总数量为',sjoin_w_x.shape[0])
                    sjoin_w_x=sjoin_w_x.append(add_data2)
                    print(tm(),'结果增加至sjoin_w_x完成总数量为',sjoin_w_x.shape[0])
                except:
                    print(tm(),'！！！！！！！！！！！！！问题挂高和下倾中有非数字内容，或者其他类型错误，请核查数据！！！！！！！！！！！')
                    QMessageBox.warning(self, "标题", "问题挂高和下倾中有非数字内容，或者其他类型错误，请核查数据！")
                    assert 0
            else:
                sjoin_w_x=sjoin_w_x.drop(columns=['问题挂高','问题下倾'])
            print(tm(),'判断是否弃用故障')
            if self.xz_wenti_guzhang == True:
                try:
                    print(tm(),'********  故障选用，参与计算，增加一项自优化数据,计算开始')
                    add_data3 = data_wenti_cp.loc[data_wenti_cp['问题故障'].str.contains(self.text_guzhang)]
                    print(tm(),'其中满足条件的数据有',add_data3.shape[0])
                    add_data3['优化得分']=80
                    add_data3['方案类型']='故障-自身故障'
                    print(tm(),'结果增加至sjoin_w_x')
                    sjoin_w_x=sjoin_w_x.append(add_data3)
                    print(tm(),'结果增加至sjoin_w_x完成总数量为',sjoin_w_x.shape[0])
                    print(tm(),'故障选用，参与计算，增加一项自优化数据,计算完成')
                except:
                    print(tm(),'！！！！！！！！！！！！！问题故障列内容错误，请核查数据！！！！！！！！！！！')
                    QMessageBox.warning(self, "标题", "问题故障列内容错误，请核查数据！")
                    assert 0
            else:
                sjoin_w_x=sjoin_w_x.drop(columns=['问题故障'])

            print(tm(),'按照每个问题的得分进行排序，选出最优的一个优化方案-开始')
            sjoin_w_x_res = sjoin_w_x.sort_values('优化得分',ascending=False).drop_duplicates('问题ID')    
            print(tm(),'按照每个问题的得分进行排序，选出最优的一个优化方案-按照问题ID去重后共计{}个可以优化解决的问题ID。'.format(sjoin_w_x_res.shape[0]))
            print(tm(),'导出优化结果开始')
            sjoin_w_x_res.to_csv('{}/可优化的{}个问题ID.csv'.format(os.path.split(self.data_wenti_file)[0],sjoin_w_x_res.shape[0]),encoding='gbk',index=False)
            print(tm(),'导出优化结果完成')
            #--------------------------------建设方案制定--------------------------
            print(tm(),'---------------------开始执行建设方案制定-----------------------')
            print(tm(),"copy导入的规划数据")
            data_guihua_cp = self.data_guihua.copy()
            print(tm(),"选择使用的列")
            data_guihua_cp = data_guihua_cp[[self.guihua_id,self.guihua_lon,self.guihua_lat,self.guihua_zs,self.guihua_gq]]
            data_guihua_cp.columns=['规划ID','规划经度','规划纬度','规划制式','规划工期']
            print(tm(),"规划ID，工期、规划制式替换空值为无")
            data_guihua_cp['规划工期'] = data_guihua_cp['规划工期'].fillna('无')
            data_guihua_cp['规划ID'] = data_guihua_cp['规划ID'].fillna('无')
            data_guihua_cp['规划制式'] = data_guihua_cp['规划制式'].fillna('TDD')
            print(tm(),"创建规划点图")
            data_guihua_cp_p = add_points(data_guihua_cp,'规划经度','规划纬度')
            print(tm(),"创建规划点图-完成")
            
            
            print(tm(),"问题扇区与规划点开始求交集-开始...")
            wenti_sjoin_guihau = gpd.sjoin(data_wenti_cp_sq,data_guihua_cp_p)
            print(tm(),"问题扇区与规划点开始求交集-完成",wenti_sjoin_guihau.shape)
            print(tm(),"问题点制作10米buffer-开始...")
            data_wenti_cp_buffer = add_buffer(data_wenti_cp_juli,'问题经度','问题纬度',10)
            print(tm(),"问题点制作10米buffer-完成",data_wenti_cp_buffer.shape)
            print(tm(),"问题buffer与规划点开始求交集-开始...")
            wenti_sjoin_guihau2 = gpd.sjoin(data_wenti_cp_buffer,data_guihua_cp_p)
            print(tm(),"问题buffer与规划点开始求交集-完成",wenti_sjoin_guihau2.shape)
            print(tm(),"合并buffer和扇区的结果-开始...",wenti_sjoin_guihau.shape,wenti_sjoin_guihau2.shape)
            wenti_sjoin_guihau = wenti_sjoin_guihau.append(wenti_sjoin_guihau2)
            print(tm(),"合并buffer和扇区的结果-结束...",wenti_sjoin_guihau.shape)
            print(tm(),"删除索引列和geometry...")
            wenti_sjoin_guihau = wenti_sjoin_guihau.drop(columns=['geometry','index_right'])
            print(tm(),"计算距离")
            wenti_sjoin_guihau=distancea_df(wenti_sjoin_guihau,'问题经度', '问题纬度', '规划经度', '规划纬度',columns_name='问题和规划距离')
            print(tm(),'导出建设结果开始')    
            wenti_sjoin_guihau.to_csv('{}/可建设的{}个问题ID.csv'.format(os.path.split(self.data_wenti_file)[0],wenti_sjoin_guihau.shape[0]),encoding='gbk',index=False)
            print(tm(),'导出建设结果完成')
            # ----------------------------------优化建设合并---------------
            print(tm(),'---------------------开始执行优化建设合并-----------------------')
            print(tm(),'copy数据')
            youhua = sjoin_w_x_res.copy()
            jianshe = wenti_sjoin_guihau.copy()
            print(tm(),'设置不同条件限制数据')
            jianshe2=jianshe.drop(jianshe.loc[(jianshe['问题和规划距离']<int(self.gongzhijuli))&(jianshe['规划制式']!='FDD900')].index)
            jianshe3 = jianshe2.loc[jianshe2['规划工期']!='无']
            jianshe4 = jianshe2.loc[jianshe2['规划工期']=='无']
            print(tm(),'数据排序')
            jianshe3 = jianshe3.sort_values('问题和规划距离')
            print(tm(),'设置方案')
            jianshe3['方案类型']='催开'
            jianshe4 = jianshe4.sort_values('问题和规划距离')
            jianshe4['方案类型']='催可研'
            print(tm(),'数据合并')
            jianshe5 = jianshe3.append(jianshe4)
            print(tm(),'合并后数据按照规则去重')
            jianshe5 = jianshe5.drop_duplicates('问题ID')
            res = youhua.append(jianshe5)
            print(tm(),'加入规划')
            data_wenti_cp_juli['方案类型']='规划'
            res = res.append(data_wenti_cp_juli)
            print(tm(),'合并按照规则去重去重')
            res2 = res.drop_duplicates('问题ID')
            print(tm(),'整理列顺序')
            res3 = res2.reindex(columns=['问题ID', '问题场景', '问题制式',  '问题经度',  '问题纬度','问题下倾','问题方位角','distance', '问题挂高', '问题故障',
                     '现网ID', '现网制式', '现网纬度', '现网经度', 
                     '规划ID', '规划制式', '规划工期', '规划纬度', '规划经度',
                    '问题和现网距离','问题和规划距离','优化得分', '方案类型'])
            res3 = res3.sort_values('问题ID')
            #-------------输出--------------
            print(tm(),'------------------输出excel-----------------------')
            df=res3.copy() #你的df           
            writer = pd.ExcelWriter(os.path.split(self.data_wenti_file)[0]+"/问题整体方案输出表.xlsx", engine='xlsxwriter')#输出地方
            print(tm(),'设置sheet名')
            df.to_excel(writer, sheet_name='方案输出结果', startrow=1, header=False,index=False)
            workbook  = writer.book
            worksheet = writer.sheets['方案输出结果']
            print(tm(),'整理表格样式')
            # Add a header format.
            header_format = workbook.add_format({
                'bold': True,# 字体加粗
                'text_wrap': True,# 是否自动换行
                'valign': 'vcenter',#对其方式 vcenter centre
                'fg_color': '#AAAAAA',# 单元格背景颜色
                'border': 1})# 单元格边框宽度
            print(tm(),'设置表头颜色')
            # 定义标题
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num , value, header_format)
            print(tm(),'导出，关闭。')
            # 导出关闭.
            writer.save()
            writer.close() 
            #-------------输出--------------
            print(tm(),"=======================方案输出程序计算完成======================")
        elif self.sending_button == '':
            print(tm(),"开始计算程序1")
        elif self.sending_button == '':
            print(tm(),"开始计算程序2")
        elif self.sending_button == '':
            print(tm(),"开始计算程序3")
        else:
            print(tm(),"开始计算程序4")
        #处理完成后高速主窗体结束
        time.sleep(2)
        self.my_signal.emit(0)

    #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-----↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-----↓↓↓↓↓↓↓↓↓工具sheet中的第三个程序双表最近-开始-↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    def kaishi_shuangbiaozuijin(self):
        if (MyMainWindow.data_shuangbiaozuijin_x.shape[0]>1) & (MyMainWindow.data_shuangbiaozuijin_y.shape[0]>1):
            #获取所有参数的值x（问题小区）
            print(tm(),'获取选择值')
            print(tm(),'数据共计',MyMainWindow.data_shuangbiaozuijin_x.shape)
            print(tm(),'数据共计',MyMainWindow.data_shuangbiaozuijin_y.shape)
            shuangbiaozuijin_lon_x = self.comboBox_16.currentText()  # 获取下拉菜单的值
            shuangbiaozuijin_lat_x = self.comboBox_15.currentText()  # 获取下拉菜单的值
            shuangbiaozuijin_lon_y = self.comboBox_14.currentText()  # 获取下拉菜单的值
            shuangbiaozuijin_lat_y = self.comboBox_13.currentText()  # 获取下拉菜单的值
            print(tm(),'开始执行站间距的计算')
            res = min_one(
                MyMainWindow.data_shuangbiaozuijin_x,
                MyMainWindow.data_shuangbiaozuijin_y,
                lon_x=shuangbiaozuijin_lon_x,
                lat_x=shuangbiaozuijin_lat_x,
                lon_y=shuangbiaozuijin_lon_y,
                lat_y=shuangbiaozuijin_lat_y)
            print(tm(),'开始导出数据')
            res.to_csv(MyMainWindow.data_shuangbiaozuijin_file_name_x.split('.')[0]+'_双表最近.csv', encoding='gbk', index=False)
            print(tm(),'输出结果，存放在py文件根目录中')
            QMessageBox.about(self, "标题",'完成输出至文件源目录' )
        else:
            QMessageBox.warning(self, "标题", "请选择有效数据后执行")
    #↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-----↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-----↑↑↑↑↑↑↑↑↑工具sheet中的第三个程序双表最近-完成-↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    RoundProgress = RoundProgress()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/kejitu2/poto/tubiao2.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
    RoundProgress.setWindowIcon(icon)
    RoundProgress.show()
    sys.exit(app.exec_())