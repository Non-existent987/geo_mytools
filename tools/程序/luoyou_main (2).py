# from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QHBoxLayout,QGraphicsDropShadowEffect, QPushButton,  QComboBox,QMessageBox,QMainWindow
# from PyQt5 import QtCore, QtGui
# from PyQt5.QtGui import QColor,QMovie
# from PyQt5.QtCore import QUrl,Qt,pyqtSignal,QSettings,QThread,QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow,  QFileDialog, QColorDialog, QMessageBox, QProgressDialog
from PyQt5.QtCore import Qt, pyqtSignal,  QThread,QSettings
from PyQt5.QtGui import QCursor,QMovie



# from shapely.geometry import (LinearRing, LineString, MultiLineString,
#                        MultiPoint, MultiPolygon, Point, Polygon)

from Ui_luoyou import *
from tools import *
from my_style import *
import time
import pandas as pd
import os,sys
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
class RoundProgress(QMainWindow,Ui_MainWindow):
    name_linshi1 = 'C:/'
    def __init__(self):
        super(RoundProgress, self).__init__()
        self.setupUi(self)
        #读取上次目录
        if os.path.isfile("config.ini"):
            self.init_login_info()
        #添加一个gif动画 
        # self.widget_7.setStyleSheet("border-image: url(:/kejitu2/poto/zhineng_zhonglou.png);")
        self.movie = QMovie(":/poto/jiazai.gif")
        self.label_5.setMovie(self.movie)
        # self.label.setAlignment()
        # setAlignment(Qt::Alignment align)
        self.movie.start()


        #按钮返回主页
        self.pushButton_4.released.connect(self.zhuye)
        

        #执行导入文件程序
        self.pushButton_2.clicked.connect(self.xuanze_file_wenti)
        self.pushButton_3.clicked.connect(self.xuanze_file_xianwang)

        #按钮切换页面
        self.pushButton.released.connect(self.qiehuan)
        # self.pushButton.released.connect(self.yunxing_sheet_0)


        
        #控制台输出用# 下面将输出重定向到textBrowser中
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)

        #--样式设置--
        #yunxing 样式
        self.pushButton.setStyleSheet(MyStyleSheet.button_style())

        #导入数据样式
        self.pushButton_2.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_3.setStyleSheet(MyStyleSheet.button_style_z())

        #主页样式
        # self.centralwidget.setStyleSheet(MyStyleSheet.main_sty())
        

        op = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op.setOpacity(0)
        self.pushButton_4.setGraphicsEffect(op)



    def yincang(self,i=1):
        if i==1:
            self.commandLinkButton_15.setVisible(True)
            self.label.setVisible(False)
            self.label_13.setVisible(False)
            self.label_35.setVisible(False)
        else:
            self.commandLinkButton_15.setVisible(False)
            self.label.setVisible(True)

    #控制台输出用
    def outputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()
    #返回主页函数
    def zhuye(self):
        self.stackedWidget.setCurrentIndex(0)
    #切换页面函数
    def qiehuan(self):
        sending_button = self.sender()
        MyThread.sending_button=sending_button.objectName()
        print(tm(),'点击了按钮',sending_button.objectName())
        if self.pushButton.objectName() == sending_button.objectName():
            self.stackedWidget.setCurrentIndex(1)    
            self.yunxing_sheet_0()

            
    def gengxin(self,i):
        if i ==0: 
            QMessageBox.information(self, "提示", "数据计算完成，结果存放在{}/目录中。".format(os.path.split(MyThread.data_wenti_file)[0]))
            self.stackedWidget.setCurrentIndex(0)  
        elif i ==5:
            QMessageBox.information(self, "提示", "请检查经纬度数据")
            self.stackedWidget.setCurrentIndex(0)
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
                'comboBox_8':['cgi','CGI'],
                'comboBox':['lon','经度'],
                'comboBox_2':['lat','纬度'],
                'comboBox_6':['方位','az']
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
                'comboBox_3':['lon','经度'],
                'comboBox_4':['lat','纬度'],
                'comboBox_7':['cgi','CGI'],
                'comboBox_5':['方位','az']
                }
                )
            print(tm(),'打开文件完成')
            print(tm(),MyThread.data_xianwang.shape)
            QMessageBox.about(self, "标题", "选择数据成功")

    def yunxing_sheet_0(self):
        
        print(tm(),'选择的5G、4G数据都应大于1条，目前的情况如下：5G{}条，4G{}条，'.format(MyThread.data_wenti.shape[0],MyThread.data_xianwang.shape[0]))
        if (MyThread.data_xianwang.shape[0]>1)& (MyThread.data_wenti.shape[0]>1):
            #获取所有参数的值x（问题小区）
            print(tm(),'获取选择值')
            print(tm(),'5G小区数据共计',MyThread.data_wenti.shape)
            print(tm(),'4G小区数据共计',MyThread.data_xianwang.shape)
            print(tm(),'开始传递参数')
            MyThread.wenti_id = self.comboBox_8.currentText()  # 获取下拉菜单的值
            MyThread.wenti_lon = self.comboBox.currentText()  # 获取下拉菜单的值
            MyThread.wenti_lat = self.comboBox_2.currentText()  # 获取下拉菜单的值
            MyThread.wenti_fw = self.comboBox_6.currentText()  # 获取下拉菜单的值
            MyThread.xianwang_lon = self.comboBox_3.currentText()  # 获取下拉菜单的值
            MyThread.xianwang_lat = self.comboBox_4.currentText()  # 获取下拉菜单的值
            MyThread.xianwang_fw = self.comboBox_5.currentText()  # 获取下拉菜单的值
            MyThread.xianwang_id = self.comboBox_7.currentText()  # 获取下拉菜单的值
            MyThread.z_z_jl = self.spinBox_3.value() #获取计数器的值
            MyThread.fw_pc = self.spinBox_2.value() #获取计数器的值

            print(tm(),'数据传递参数完成')

# ------------------------------------------------------------                
            print(tm(),'处理数据线程开始')
            try:
                self.jindutiao()
            except:
                QMessageBox.warning(self, "标题", "请检查经纬度等数据") 
            
            # self.stackedWidget.setCurrentIndex(1)  
            # QMessageBox.about(self, "标题",'完成输出至文件源目录' )
        else:
            QMessageBox.warning(self, "标题", "请选择有效数据后执行") 
            self.stackedWidget.setCurrentIndex(0)         
        

    #↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-----↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-----↑↑↑↑↑↑↑↑↑↑↑↑制定方案-完成-↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
#另外一个处理数据的线程
class MyThread(QThread):
    my_signal = pyqtSignal(int)# 更新进度条
    data_wenti = data_xianwang=  pd.DataFrame()
    data_wenti_file =data_xianwang_file= ''
    #问题点变量
    wenti_id=wenti_lon=wenti_lat=xianwang_lon=xianwang_lat=z_z_jl=fw_pc=wenti_fw=xianwang_fw=xianwang_id=''    # p = 0

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
        try:
            print(tm(),'按下按钮的名称',self.sending_button)
            if self.sending_button == 'pushButton':
                print(tm(),"=======================计算开始======================")
                print(tm(),self.data_wenti.shape,self.data_xianwang.shape)
                print(tm(),'文件copy')
                data_4 = self.data_wenti.copy()
                data_4_lie = list(data_4.columns)
                data_4 = data_4.rename(columns={self.wenti_lon:'4G经度',self.wenti_lat:'4G纬度',self.wenti_fw:'4G方位角',self.wenti_id:'4Gid'})
                data_5 = self.data_xianwang.copy()
                data_5_lie = list(data_5.columns)
                data_5 = data_5.rename(columns={self.xianwang_lon:'5G经度',self.xianwang_lat:'5G纬度',self.xianwang_fw:'5G方位角',self.xianwang_id:'5Gid'})
                print(tm(),'4G小区扩展距离-开始...')
                #-------------------------
                data_4_buffer = add_buffer(data_4,'4G经度','4G纬度',int(self.z_z_jl))
                print(tm(),'4G小区扩展距离-完成')
                print(tm(),'5G小区制作点-开始...')
                data_5_p = add_points(data_5,'5G经度','5G纬度')
                print(tm(),'5G小区制作点-完成')
                print(tm(),'匹配共址信息-开始...')
                res = gpd.sjoin(data_4_buffer,data_5_p)
                print(tm(),'匹配共址信息-完成')
                data_res = pd.DataFrame()
                print(tm(),'计算共覆盖的情况-开始...')
                for name , data_t in res.groupby('4Gid'):
                    data_t['方位角差异'] = np.abs(data_t['4G方位角']- data_t['5G方位角'])
                    data_t['方位角差异2'] = 360-np.abs(data_t['4G方位角']- data_t['5G方位角'])
                    df = data_t.loc[(data_t['方位角差异']<=int(self.fw_pc))|(data_t['方位角差异2']<=int(self.fw_pc))]
                    df_use = pd.DataFrame(df.groupby(by = '4Gid').apply(lambda g:g['5Gid'].str.cat(sep='/'))).reset_index()
                    if df.shape[0] ==0:
                        df_use = df_use.append([{'4Gid':name,'w':np.nan}], ignore_index=True)
                    else:
                        pass
                    df_use.columns=['4Gid','共覆盖cgi']
                    data_res = data_res.append(df_use)
                print(tm(),'计算共覆盖的情况-完成')
                print(tm(),'结果写入原始数据-开始...')
                data_4_rew = data_4.merge(data_res,how='left',on='4Gid')
                print(tm(),'结果写入原始数据-完成')
                #------------------------------------------
                print(tm(),data_4_rew.columns)
                data_4_rew.to_excel(os.path.split(self.data_wenti_file)[0]+"/4G匹配5G共覆盖结果.xlsx",encoding='gbk',index=False)
                time.sleep(2)
                #-------------输出--------------
                print(tm(),"=======================计算完成======================")
            elif self.sending_button == 'ww':
                print(tm(),"开始计算程序1")
            elif self.sending_button == 'ww':
                print(tm(),"开始计算程序2")
            elif self.sending_button == 'ww':
                print(tm(),"开始计算程序3")
            else:
                print(tm(),"开始计算程序4")
            #处理完成后高速主窗体结束
            time.sleep(2)
            self.my_signal.emit(0)
        except:
            self.my_signal.emit(5)



if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    RoundProgress = RoundProgress()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/poto/xxy.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
    RoundProgress.setWindowIcon(icon)
    RoundProgress.show()
    sys.exit(app.exec_())