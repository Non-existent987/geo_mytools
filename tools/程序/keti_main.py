# encoding='utf-8'
# 同时输出到控制台和文件中
import sys
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
import time
def tm():
    return time.strftime("%Y-%m-%d %H:%M:%S")+':'
from tools import *
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QHBoxLayout,QGraphicsDropShadowEffect, QPushButton,  QComboBox,QMessageBox,QCommandLinkButton,QMainWindow
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QUrl,Qt
from shapely.geometry import (LinearRing, LineString, MultiLineString,
                       MultiPoint, MultiPolygon, Point, Polygon)
# import kejitu_rc
from my_style import *
import sys
import os
from Ui_keti import *
import geopandas as gpd
import pandas as pd

class MyMainWindow(QWidget, Ui_dn):
    #-----0-1
    #MyMainWindow（QWidget, Ui_Form）MyMainWindow是类名字自定义的
    #QWidget 继承父类QWidget Ui_Form是窗体的类名称
    data_name = 'C:/'
    name_linshi1 = 'C:/'
    data_wenti = pd.DataFrame()
    data_name_2 = ''
    data_xianwang = pd.DataFrame()
    #----2-建设
    data_name_jianshe_wenti = ''
    data_name_jianshe_guihua = ''
    data_jianshe_wenti = pd.DataFrame()
    data_jianshe_guihua = pd.DataFrame()
    #---工具sheet站间距
    data_zhanjianju = pd.DataFrame()
    data_zhanjianju_file_name = ''
    #---工具sheet单表最近
    data_danbiaozuijin = pd.DataFrame()
    data_danbiaozuijin_file_name = ''   
    #---工具sheet双表最近
    data_shuangbiaozuijin_x = pd.DataFrame()
    data_shuangbiaozuijin_file_name_x = ''   
    data_shuangbiaozuijin_y = pd.DataFrame()
    #---工具sheet表关联图
    data_biaoguanliantu_x = gpd.GeoDataFrame()
    data_biaoguanliantu_file_name_y = ''   
    data_biaoguanliantu_y = pd.DataFrame()
    #---工具sheet表拆合
    data_biaochaihe = pd.DataFrame()
    file_biaochaihe_name = ''
    biaochaihe_name = ''
    nn_m = 1
    #---工具sheet_buff圈点
    data_buff_qd_x = pd.DataFrame()
    buff_qd_file_name_x = ''   
    data_buff_qd_y = pd.DataFrame()
    #---工具sheet_扇区圈点
    data_shanqu_qd_x = pd.DataFrame()
    shanqu_qd_file_name_x = ''   
    data_shanqu_qd_y = pd.DataFrame()
    def __init__(self, parent=None):#parent = None代表此QWidget属于最上层的窗口,也就是MainWindows.
        super(MyMainWindow, self).__init__(parent)#因为继承关系，要对父类初始化
        # 通过super初始化父类，__init__()函数无self，若直接QtWidgets.QWidget.__init__(self)，括号里是有self的
        self.setupUi(self)

        # --事件设置---0-1
        self.B_jizhan.clicked.connect(self.openMsg_jianshe)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        self.yunxing.clicked.connect(self.kaishi) #开始执行
        self.B_wenti.clicked.connect(self.openMsg_jianshe)
        self.pushButton_3.clicked.connect(self.closeEvent)
        self.pushButton.clicked.connect(self.pushButton_c)
        # self.web_d.load(QUrl('file:///E:/PyCharm/qt/gg.html'))
        self.pushButton_4.released.connect(self.qiehuan)
        self.pushButton_7.released.connect(self.qiehuan)
        self.pushButton_8.released.connect(self.qiehuan)

        self.pushButton_2.released.connect(self.qiehuan_nei)
        self.pushButton_9.released.connect(self.qiehuan_nei)
        self.pushButton_20.released.connect(self.qiehuan_nei)
        self.pushButton_24.released.connect(self.qiehuan_nei)
        self.pushButton_25.released.connect(self.qiehuan_nei)
        self.pushButton_21.released.connect(self.qiehuan_nei)
        self.pushButton_5.released.connect(self.qiehuan_nei)
        self.pushButton_11.released.connect(self.qiehuan_nei)
        self.pushButton_23.released.connect(self.qiehuan_nei)
        self.pushButton_22.released.connect(self.qiehuan_nei)

        self.commandLinkButton_4.released.connect(self.zhuye_nei)
        self.commandLinkButton_5.released.connect(self.zhuye_nei)
        self.commandLinkButton_6.released.connect(self.zhuye_nei)
        self.commandLinkButton_7.released.connect(self.zhuye_nei)
        self.commandLinkButton_8.released.connect(self.zhuye_nei)
        self.commandLinkButton_9.released.connect(self.zhuye_nei)
        self.commandLinkButton_10.released.connect(self.zhuye_nei)
        self.commandLinkButton_11.released.connect(self.zhuye_nei)
        self.commandLinkButton_12.released.connect(self.zhuye_nei)
        self.commandLinkButton_13.released.connect(self.zhuye_nei)
        

        self.commandLinkButton.released.connect(self.zhuye)
        self.commandLinkButton_2.released.connect(self.zhuye)
        self.commandLinkButton_3.released.connect(self.zhuye)
        #--事件设置---2--建设
        self.pushButton_6.clicked.connect(self.openMsg_jianshe)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        self.pushButton_12.clicked.connect(self.openMsg_jianshe)
        self.yunxing_2.clicked.connect(self.kaishi_2) #开始执行
        #---时间设置--工具sheet中的（站间距设置）
        self.pushButton_10.clicked.connect(self.xuanze_file_zhanjianju)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        self.yunxing_5.clicked.connect(self.kaishi_zhanjianju)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        #---时间设置--工具sheet中的（单表最近）
        self.pushButton_14.clicked.connect(self.xuanze_file_danbiaozuijin)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        self.yunxing_7.clicked.connect(self.kaishi_danbiaozuijin)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        #---时间设置--工具sheet中的（双表最近）
        self.pushButton_16.clicked.connect(self.xuanze_file_shuangbiaozuijin_x)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        self.pushButton_15.clicked.connect(self.xuanze_file_shuangbiaozuijin_y)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        self.yunxing_8.clicked.connect(self.kaishi_shuangbiaozuijin)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        #---时间设置--工具sheet中的（表关联图）
        self.pushButton_17.clicked.connect(self.xuanze_file_biaoguanliantu_x)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        self.pushButton_18.clicked.connect(self.xuanze_file_biaoguanliantu_y)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        self.yunxing_9.clicked.connect(self.kaishi_biaoguanliantu)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        #---时间设置--工具sheet中的（表关联图）
        self.pushButton_13.clicked.connect(self.xuanze_file_biaohechai)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        self.pushButton_19.clicked.connect(self.xuanze_file_biaohechai_data)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        self.yunxing_10.clicked.connect(self.kaishi_biaohechai_he)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        self.yunxing_11.clicked.connect(self.kaishi_biaohechai_chai)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        #---时间设置--工具sheet中的（buffer_圈点）
        self.pushButton_26.clicked.connect(self.buff_quandian_x)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        self.pushButton_27.clicked.connect(self.buff_quandian_y)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        self.yunxing_12.clicked.connect(self.kaishi_buffer_qd)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        #---时间设置--工具sheet中的（buffer_圈点）
        self.pushButton_28.clicked.connect(self.shanqu_quandian_x)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        self.pushButton_29.clicked.connect(self.shanqu_quandian_y)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        self.yunxing_13.clicked.connect(self.kaishi_shanqu_qd)  # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()

        #--样式设置--0-1-3
        #ico

        self.pushButton_2.setStyleSheet(MyStyleSheet.button_ico_1())
        self.pushButton_9.setStyleSheet(MyStyleSheet.button_ico_2())
        self.pushButton_20.setStyleSheet(MyStyleSheet.button_ico_3())
        self.pushButton_24.setStyleSheet(MyStyleSheet.button_ico_4())
        self.pushButton_25.setStyleSheet(MyStyleSheet.button_ico_5())
        self.pushButton_21.setStyleSheet(MyStyleSheet.button_ico_6())
        self.pushButton_5.setStyleSheet(MyStyleSheet.button_ico_7())
        self.pushButton_11.setStyleSheet(MyStyleSheet.button_ico_8())
        self.pushButton_23.setStyleSheet(MyStyleSheet.button_ico_9())
        self.pushButton_22.setStyleSheet(MyStyleSheet.button_ico_10())
        # self.setStyleSheet(MyStyleSheet.main_sty())
        self.gridLayout.setSpacing(0)#模块间隔
        self.pushButton_4.setStyleSheet(MyStyleSheet.button_style_tupian_1())
        self.pushButton_7.setStyleSheet(MyStyleSheet.button_style_tupian_2())
        self.pushButton_8.setStyleSheet(MyStyleSheet.button_style_tupian_3())
        self.yunxing.setStyleSheet(MyStyleSheet.button_style())
        self.B_jizhan.setStyleSheet(MyStyleSheet.button_style_z())
        self.B_wenti.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_3.setStyleSheet(MyStyleSheet.my_style_1())
        self.pushButton.setStyleSheet(MyStyleSheet.my_style_1())
        self.toolBox_2.setStyleSheet(MyStyleSheet.button_style_toolBox())
        self.toolBox.setStyleSheet(MyStyleSheet.button_style_toolBox())
        # self.stackedWidget.
        # self.stackedWidget.setStyleSheet(MyStyleSheet.button_style_tabWidget())
        # self.tabWidget_2.setStyleSheet(MyStyleSheet.button_style_tabWidget_2())
        # self.frame.setStyleSheet(MyStyleSheet.frame_style())
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
        self.widget_bian.setGraphicsEffect(self.shadow)#添加阴影,这个会报错 “UpdateLayeredWindowIndirect failed ”
        # --样式设置--2-----------------------------------------
        self.yunxing_2.setStyleSheet(MyStyleSheet.button_style())
        self.pushButton_6.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_12.setStyleSheet(MyStyleSheet.button_style_z())
        #-----------------3_1----样式设置--------------
        # self.yunxing_3.setStyleSheet(MyStyleSheet.button_style())
        # self.pushButton_2.setStyleSheet(MyStyleSheet.button_style_z())
        # ------------工具sheet站间距样式---
        self.pushButton_10.setStyleSheet(MyStyleSheet.button_style_z())
        self.yunxing_5.setStyleSheet(MyStyleSheet.button_style())
        # ------------工具sheet单表最近样式---
        self.pushButton_14.setStyleSheet(MyStyleSheet.button_style_z())
        self.yunxing_7.setStyleSheet(MyStyleSheet.button_style())
        # ------------工具sheet双表最近样式---
        self.pushButton_15.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_16.setStyleSheet(MyStyleSheet.button_style_z())
        self.yunxing_8.setStyleSheet(MyStyleSheet.button_style())
        # ------------工具sheet表关联图最近样式---
        self.pushButton_17.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_18.setStyleSheet(MyStyleSheet.button_style_z())
        self.yunxing_9.setStyleSheet(MyStyleSheet.button_style())
        # ------------工具sheet表合并拆分最近样式---
        self.pushButton_13.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_19.setStyleSheet(MyStyleSheet.button_style_z())
        self.yunxing_10.setStyleSheet(MyStyleSheet.button_style())
        self.yunxing_11.setStyleSheet(MyStyleSheet.button_style())
        # ------------工具sheet_buffer圈点---
        self.pushButton_26.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_27.setStyleSheet(MyStyleSheet.button_style_z())
        self.yunxing_12.setStyleSheet(MyStyleSheet.button_style())
        # ------------工具sheet扇区圈点---
        self.pushButton_28.setStyleSheet(MyStyleSheet.button_style_z())
        self.pushButton_29.setStyleSheet(MyStyleSheet.button_style_z())
        self.yunxing_13.setStyleSheet(MyStyleSheet.button_style())

    #函数0-1---
    def zhuye(self):
        self.stackedWidget.setCurrentIndex(0)
    def zhuye_nei(self):
        self.stackedWidget_2.setCurrentIndex(12)
    #--事件函数--
    def add_points(self,
               df,
               coords=['', '', '', ''],
               has_z=False,
               pnt_col='geometry',
               **kwargs):
        """根据经纬度挂高所在列，为df增加CRS和 geometry 列

        Returns:
           [type] -- [description]
        """
        if coords == ['', '', '', '']:
            coords = [self.lon, self.lat, self.height, self.azimuth]
        # lon, lat, height, *oth = coords
        lon, lat, *oth = coords
        height, azimuth = oth
        if has_z:
            df = df.copy()
            df[pnt_col] = [Point(x) for x in zip(df[lon], df[lat], df[height])]
        else:
            df = df.copy()
            df[pnt_col] = [Point(x) for x in zip(df[lon], df[lat])]
        df = gpd.GeoDataFrame(
            df, crs={"init": "epsg:4326"}, geometry=pnt_col)  # 实例化化成geodataframe
        return df

    def kaishi1(self):
        QMessageBox.about(self, "标题", "处理完成")
    def kaishi(self):
        if (MyMainWindow.data_xianwang.shape[0]>1)&(MyMainWindow.data_wenti.shape[0]>1):
            print(tm(),'开始获取优化的输入参数')
            #获取所有参数的值x（问题小区）
            xiaoquming_x = self.comboBox_45.currentText()  # 获取下拉菜单的值
            lon_x = self.comboBox_47.currentText()  # 获取下拉菜单的值
            lat_x = self.comboBox_46.currentText()  # 获取下拉菜单的值
            fangwei_x = self.comboBox_48.currentText()  # 获取下拉菜单的值
            leibie_x = self.comboBox_49.currentText()  # 获取下拉菜单的值
            zhishi_x = self.comboBox_44.currentText()  # 获取下拉菜单的值
            guagao_x = self.comboBox_51.currentText()  # 获取下拉菜单的值
            guzhang_x = self.comboBox_50.currentText()  # 获取下拉菜单的值
            guzhang_ok_x = self.radioButton_25.isChecked() #是否选中故障
            guagao_ok_x = self.radioButton_26.isChecked()  # 是否选中故障
            guzhang_shaixuan_x = self.lineEdit_72.text()  # 获取单行输入框
            xiaqingjiao_x = self.comboBox_52.currentText()  # 获取下拉菜单的值
            xiaqingjiao_ok_x = self.radioButton_27.isChecked()  # 是否选中下倾角
            print(tm(),'问题点第一页获取成功')
            cj_900_hxcq_x = self.lineEdit_90.text()  # 获取单行输入框
            cj_900_ybcq_x = self.lineEdit_93.text()  # 获取单行输入框
            cj_900_cj_x = self.lineEdit_89.text()  # 获取单行输入框
            cj_900_xc_x = self.lineEdit_92.text()  # 获取单行输入框
            cj_900_xz_x = self.lineEdit_85.text()  # 获取单行输入框
            cj_900_nc_x = self.lineEdit_83.text()  # 获取单行输入框

            cj_1800_hxcq_x = self.lineEdit_87.text()  # 获取单行输入框
            cj_1800_ybcq_x = self.lineEdit_86.text()  # 获取单行输入框
            cj_1800_cj_x = self.lineEdit_84.text()  # 获取单行输入框
            cj_1800_xc_x = self.lineEdit_82.text()  # 获取单行输入框
            cj_1800_xz_x = self.lineEdit_91.text()  # 获取单行输入框
            cj_1800_nc_x = self.lineEdit_88.text()  # 获取单行输入框

            gongzhijuli_x = self.spinBox_7.value() #获取计数器的值
            bobankuandu_x = self.spinBox_9.value() #获取计数器的值

            leixing_1_gaodu_x = self.lineEdit_94.text()  # 获取单行输入框
            leixing_1_xiaqing_x = self.lineEdit_95.text()  # 获取单行输入框
            leixing_2_gaodu_x = self.lineEdit_97.text()  # 获取单行输入框
            leixing_2_xiaqing_x = self.lineEdit_96.text()  # 获取单行输入框
            print(tm(),'问题点第二页获取成功')

            # 获取所有参数的值y（现网小区）
            xiaoquming_y = self.comboBox_80.currentText()  # 获取下拉菜单的值
            lon_y = self.comboBox_82.currentText()  # 获取下拉菜单的值
            lat_y = self.comboBox_81.currentText()  # 获取下拉菜单的值
            zhishi_y = self.comboBox_83.currentText()  # 获取下拉菜单的值
            guzhang_y = self.comboBox_84.currentText()  # 获取下拉菜单的值
            guzhang_ok_y = self.radioButton_28.isChecked()  # 是否选中故障
            guzhang_shaixuan_y = self.lineEdit_98.text()  # 获取单行输入框
            guagao_ok_y = self.radioButton_29.isChecked()  # 是否选中故障
            guagao_y = self.comboBox_85.currentText()  # 获取下拉菜单的值
            print(tm(),'现网第一页获取成功')
            tichu_gaotie_y = self.lineEdit_11.text()  # 获取单行输入框
            tichu_gaotie_ok_y = self.radioButton_30.isChecked()  # 是否选中故障
            tichu_shifen_y = self.lineEdit_100.text()  # 获取单行输入框
            tichu_shifen_y_ok_y = self.radioButton_31.isChecked()  # 是否选中故障
            tichu_weizhan_y = self.lineEdit_99.text()  # 获取单行输入框
            tichu_weizhan_ok_y = self.radioButton_32.isChecked()  # 是否选中故障
            print(tm(),'现网第二页获取成功')
            #制作图层-数据整理
            print(tm(),'开始导入现网数据')
            ditu_cell = MyMainWindow.data_xianwang.copy()
            print(tm(),ditu_cell.shape)
            print(tm(),'现网小区数量：', ditu_cell.shape)
            ditu_cell = ditu_cell.loc[(ditu_cell[lon_y] < 150) & (ditu_cell[lat_y] < 50) & (ditu_cell[lat_y] > 10)]
            ditu_cell[xiaoquming_y] = ditu_cell[xiaoquming_y].fillna('无')
            print(tm(),'数据整理中,问题小区的行列',ditu_cell.shape)
            # if tichu_gaotie_ok_y == True:
            #    ditu_cell = ditu_cell[~ditu_cell[xiaoquming_y].str.contains(tichu_gaotie_y)]  # 删除某列包含特殊字符，过滤删除，筛选剔除
            # if tichu_weizhan_ok_y == True:
            #    ditu_cell = ditu_cell[~ ditu_cell[xiaoquming_y].str.contains(tichu_weizhan_y)]  # 删除某列包含特殊字符的行
            # if tichu_shifen_y_ok_y == True:
            #    ditu_cell = ditu_cell[~ ditu_cell[xiaoquming_y].str.contains(tichu_shifen_y)]  # 删除某列包含特殊字符的行
            # print('158')
            # ditu_cell = ditu_cell.dropna(subset=[lon_y, lat_y])  #dfsd
            # print('现网小区剔除无效数据后数量：',ditu_cell.shape)
            print(tm(),'开始获取问题数据')
            wt_cell = MyMainWindow.data_wenti.copy()
            wt_cell[xiaoquming_x] = wt_cell[xiaoquming_x].fillna('无')
            # wt_cell_x = wt_cell[[xiaoquming_x]]
            # res = ditu_cell.merge(wt_cell_x, how='left', left_on=xiaoquming_y, right_on=xiaoquming_x, suffixes=('', '_y'),
            #                       indicator=True)
            # ditu_cell = res.loc[res['_merge'] == 'both']
            # print(ditu_cell.shape)
            print(tm(),'数据整理中，问题点的行列共计',wt_cell.shape)
            def juli(df, changjing, zhishi):
                try:
                    F900 = {0: cj_900_hxcq_x, 1: cj_900_ybcq_x, 2: cj_900_cj_x, 3: cj_900_xc_x, 4: cj_900_xz_x, 5: cj_900_nc_x}
                    TDD = {0: cj_1800_hxcq_x, 1: cj_1800_ybcq_x, 2: cj_1800_cj_x, 3: cj_1800_xc_x, 4: cj_1800_xz_x, 5: cj_1800_nc_x}
                    df['juli']= [F900[cj] if pid == 'FDD900' else TDD[cj] 
                             for cj , pid in zip(df[changjing],df[zhishi])]
                except:
                    try:
                        F900 = {'主城区': cj_900_hxcq_x, '一般城区': cj_900_ybcq_x, '市郊': cj_900_cj_x, '县城': cj_900_xc_x, '乡镇': cj_900_xz_x, '农村': cj_900_nc_x}
                        TDD = {'主城区': cj_1800_hxcq_x, '一般城区': cj_1800_ybcq_x, '市郊': cj_1800_cj_x, '县城': cj_1800_xc_x, '乡镇': cj_1800_xz_x, '农村': cj_1800_nc_x}
                        df['juli']= [F900[cj] if pid == 'FDD900' else TDD[cj]
                                 for cj , pid in zip(df[changjing],df[zhishi])]
                    except:
                        F900 = {'核心城区':cj_900_hxcq_x,'一般城区':cj_900_ybcq_x,'市郊':cj_900_cj_x,'县城':cj_900_xc_x,'乡镇':cj_900_xz_x,'农村':cj_900_nc_x}
                        TDD = {'核心城区':cj_1800_hxcq_x,'一般城区':cj_1800_ybcq_x,'市郊':cj_1800_cj_x,'县城':cj_1800_xc_x,'乡镇':cj_1800_xz_x,'农村':cj_1800_nc_x}
                        df['juli']= [F900[cj] if pid == 'FDD900' else TDD[cj]
                                 for cj , pid in zip(df[changjing],df[zhishi])]
                df['juli'] = pd.to_numeric(df['juli'])
                return df
            # wt_cell[leibie_x] = wt_cell[leibie_x].fillna(3)  # na的用3填充
            # wt_cell[zhishi_x] = wt_cell[zhishi_x].fillna('TDD')  # na的用TDD填充
            print(cj_900_hxcq_x,cj_900_ybcq_x,cj_900_cj_x,cj_900_xz_x,cj_900_nc_x)
            print(cj_1800_hxcq_x, cj_1800_ybcq_x, cj_1800_cj_x,cj_1800_xc_x,cj_1800_xz_x, cj_1800_nc_x)
            print(wt_cell.shape, leibie_x, zhishi_x)
            print(tm(),'添加距离')
            wt_cell1 = juli(wt_cell, leibie_x, zhishi_x)
            print(tm(),'添加距离ok')
            # wt_cell1 = wt_cell.dropna(subset=[lon_x, lat_x, fangwei_x, 'juli'])  #
            wt_cell1 = wt_cell1.loc[wt_cell1[lon_x] < 150]
            wt_cell12 = wt_cell1.copy()
            wt_cell12[lon_x] = pd.to_numeric(wt_cell12[lon_x])
            wt_cell12[lat_x] = pd.to_numeric(wt_cell12[lat_x])
            wt_cell12[fangwei_x] = pd.to_numeric(wt_cell12[fangwei_x])
            wt_cell12['juli'] = pd.to_numeric(wt_cell12['juli'])
            nb = wt_cell12[[lon_x, lat_x, fangwei_x, 'juli']].isnull().sum().sum()
            print(tm(),'经度、纬度、方位角、距离为空的数量',nb)
            # 制作图层-开始
            print(tm(),'开始制作图层')
            shanqu = add_sectors_df(wt_cell12,
                       coords=[lon_x, lat_x, 'd_height', fangwei_x, 'juli'],
                       has_z=False,
                       sec_col='geometry',
                       shape_dict={'beam': int(bobankuandu_x),'per_degree': 10},)
            shanqu.rename(columns = {zhishi_x:'zhishi_x'
                            ,lon_x:'lon_x'
                            ,lat_x:'lat_x'
                            , xiaqingjiao_x: 'xiaqingjiao_x'
                            ,fangwei_x:'fangwei_x'
                            ,guzhang_x:'guzhang_x'
                            ,guagao_x:'guagao_x'
                            ,xiaoquming_x:'xiaoquming_x'},inplace = True)
         
            print(tm(),'扇区的个数',shanqu.shape)
            print(tm(),shanqu.columns)
            dian_ditu = add_points(ditu_cell,
                   lon=lon_y,
                   lat=lat_y,
                   pnt_col='geometry')
            dian_ditu.rename(columns={
                zhishi_y: 'zhishi_y'
                , lon_y: 'lon_y'
                , lat_y: 'lat_y'
                , guagao_y: 'guagao_y'
                , guzhang_y: 'guzhang_y'
                , xiaoquming_y: 'xiaoquming_y'}, inplace=True)
            print(tm(),'现网小区点图制作完成',dian_ditu.shape)
            print(tm(),dian_ditu.columns)
            print(tm(),'210')
            #图层相交
            res_zong = gpd.sjoin(shanqu, dian_ditu)
            print(tm(),'gpd.sjoin后的数量',res_zong.shape)
            # res_zong.to_csv('ttttt.csv',encoding = 'gbk')
            # print('215')
            #整理结果
            # if guzhang_ok_x == True:
            #    res_zong['guzhang_x'] = res_zong['guzhang_x'].fillna('无')
            # if guzhang_ok_y == True:
            #    res_zong['guzhang_y'] = res_zong['guzhang_y'].fillna('无')

            print(tm(),'图层相交')
            res_zong['方案类型'] = '优化周边站点'
            res_zong_jl = distancea_df(res_zong, 'lon_x', 'lat_x', 'lon_y', 'lat_y')

            res_zong_jl = res_zong_jl.reset_index(drop=True)
            # print(7)
            # if guzhang_ok_x == True:
            #    res_zong_jl.loc[(res_zong_jl['guzhang_x'].str.contains(guzhang_shaixuan_x)), '方案类型'] = '问题小区故障处理'
            # print(8)
            # if guzhang_ok_y == True:
            #    res_zong_jl.loc[(res_zong_jl['guzhang_y'].str.contains(guzhang_shaixuan_y)), '方案类型'] = '周边小区故障处理'
            # print(4)
            # 删除距离小于25米，现网站点网络制式不是FDD的小区。
            print(tm(),'剔除共址小区')
            res_zong_j2 = res_zong_jl.drop(
            res_zong_jl[(res_zong_jl['距离'] < gongzhijuli_x)
                     & (res_zong_jl['zhishi_y'] != 'FDD900')].index)  # 多条件删除，符合条件的行
            # 删除距离小于25米，现网站点和问题小区网络制式都为FDD的小区
            res_zong_j3 = res_zong_j2.drop(
                res_zong_j2[(res_zong_j2['距离'] < gongzhijuli_x)
                         & (res_zong_j2['zhishi_y'] == 'FDD900')
                         & (res_zong_j2['zhishi_x'] == 'FDD900')].index)  # 多条件删除，符合条件的行
            print(tm(),'剔除共址小区后的数量',res_zong_j3.shape)
            # 增加自身有故障的问题小区
            # if guzhang_ok_x == True:
            #    shanqu_add = shanqu[['xiaoquming_x', 'lon_x', 'lat_x', 'guagao_x', 'xiaqingjiao_x','fangwei_x','guzhang_x']]
            #    shanqu_add_guzhang = shanqu_add.loc[(shanqu_add['guzhang_x'].str.contains(guzhang_shaixuan_x))]
            #    shanqu_add_guzhang['方案类型'] = '问题小区故障处理'
            #    res_zong_j3 = pd.concat([res_zong_j3,shanqu_add_guzhang])
            # print('244')
            # print(11)
            # #增加自身有问题小区
            # if (guagao_ok_x == True) & (xiaqingjiao_ok_x == True):
            #    shanqu_add = shanqu[['xiaoquming_x','lon_x','lat_x','guagao_x','xiaqingjiao_x','fangwei_x','guzhang_x']]
            #    shanqu_add1 = shanqu_add.copy()
            #    shanqu_add1['guagao_x'] = pd.to_numeric(shanqu_add['guagao_x'])
            #    shanqu_add1['xiaqingjiao_x'] = pd.to_numeric(shanqu_add['xiaqingjiao_x'])
            #    shanqu_add1['guagao_x'].fillna(31,inplace=True)
            #    shanqu_add1['xiaqingjiao_x'].fillna(3, inplace=True)

            #    print(111)
            #    print(shanqu_add1.columns)
            #    print(shanqu_add1.dtypes)
            #    add_data2 = shanqu_add1.loc[(shanqu_add1['guagao_x']>int(leixing_1_gaodu_x)) & (shanqu_add1['xiaqingjiao_x']<int(leixing_1_xiaqing_x))]
            #    print(112)
            #    add_data2['得分'] = 40
            #    print(113)
            #    add_data2['方案类型'] = '优化自身'
            #    print(12)
            #    add_data3 = shanqu_add1.loc[(shanqu_add1['guagao_x']<int(leixing_2_gaodu_x)) & (shanqu_add1['xiaqingjiao_x']>int(leixing_2_xiaqing_x))]
            #    add_data3['得分'] = 40
            #    add_data3['方案类型'] = '优化自身'
            #    res_zong_j4 = pd.concat([res_zong_j3,add_data2,add_data3], axis=0)
            # else:
            print(tm(),'开始计算得分')
            res_zong_j4 = res_zong_j3.copy()
            res_zong_j4['得分'] = 50
            res_zong_j4.loc[res_zong_j4['juli']/res_zong_j4['距离']>2,'得分']=70
            print(13)
            #得分计算基础
            print(res_zong_j4.dtypes)
            res_zong_j4['zhishi_y'].fillna('TDD', inplace=True)
            res_zong_j4['zhishi_x'].fillna('TDD', inplace=True)
            res_zong_j4.loc[res_zong_j4['方案类型'] == '问题小区故障处理', '得分'] = 72
            res_zong_j4.loc[res_zong_j4['方案类型'] == '周边小区故障处理', '得分'] = 71
            print(1333)
            # res_zong_j4.to_csv('text-aa.csv',encoding = 'gbk')
            res_zong_j4.loc[(res_zong_j4['zhishi_y'].str.contains('FDD900')), '得分'] = 65
            res_zong_j4.loc[(res_zong_j4['zhishi_y'].str.contains('TDD900')), '得分'] = 60
            print(133)
            if guagao_ok_y == True:
                res_zong_j4.loc[res_zong_j4['guagao_y'] < 25, '得分'] = 55
            print(15)

            #1/2区域内得分计算
            res_zong_j4.loc[
                ((res_zong_j4['juli'] / res_zong_j4['距离'] > 2) & (res_zong_j4['方案类型'] == '问题小区故障处理')), '得分'] = 92
            res_zong_j4.loc[
                ((res_zong_j4['juli'] / res_zong_j4['距离'] > 2) & (res_zong_j4['方案类型'] == '周边小区故障处理')), '得分'] = 91
            res_zong_j4.loc[
                ((res_zong_j4['juli'] / res_zong_j4['距离'] > 2) & (res_zong_j4['zhishi_y'].str.contains('FDD900'))), '得分'] = 85
            res_zong_j4.loc[
                ((res_zong_j4['juli'] / res_zong_j4['距离'] > 2) & (res_zong_j4['zhishi_y'].str.contains('TDD900'))), '得分'] = 80
            if guagao_ok_y == True:
                res_zong_j4.loc[((res_zong_j4['juli'] / res_zong_j4['距离'] > 2) & (res_zong_j4['guagao_y'] < 25)), '得分'] = 75
            print(tm(),'去重前的数量',res_zong_j4.shape)
            res_zong_qc = res_zong_j4.sort_values(by="得分")  # 按照优先级排序默认升序
            print(tm(),'去重按照字段',xiaoquming_x)
            res_zong_youhua = res_zong_qc.drop_duplicates(subset='xiaoquming_x')  # 删除重复项
            print(tm(),'去重后的数量,',res_zong_youhua.shape)
            print(tm(),16)
            if guzhang_ok_x == True &  guzhang_ok_y == True & xiaqingjiao_ok_x == True & guagao_ok_x == True & guagao_ok_y == True:
                res_1 = res_zong_youhua[['xiaoquming_x','zhishi_x','juli','lon_x','lat_x','guagao_x','xiaqingjiao_x','fangwei_x','guzhang_x','方案类型','得分','xiaoquming_y','zhishi_y','lon_y','lat_y','guagao_y','guzhang_y','距离']]
            else:
                res_1 = res_zong_youhua[['xiaoquming_x','zhishi_x','juli','lon_x','lat_x','fangwei_x','方案类型','得分','xiaoquming_y','zhishi_y','lon_y','lat_y','距离']]
            print(tm(),217)
            print(tm(),res_1.columns)
            if guzhang_ok_x == True &  guzhang_ok_y == True & xiaqingjiao_ok_x == True & guagao_ok_x == True & guagao_ok_y == True:
                res_1.columns = ['问题小区名', '问题小区制式','场景距离', '问题小区经度', '问题小区纬度', '问题小区挂高',
                '问题小区下倾角', '问题小区方位角', '问题小区故障', '解决方案', '得分','解决方案小区名',
                '解决方案制式', '解决方案经度', '解决方案纬度', '解决方案挂高', '解决方案故障', '距离']
            else:
                res_1.columns = ['问题小区名', '问题小区制式','场景距离', '问题小区经度', '问题小区纬度',
                '问题小区方位角', '解决方案', '得分','解决方案小区名',
                '解决方案制式', '解决方案经度', '解决方案纬度', '距离']
            print(tm(),'开始导出数据')
            res_1.to_csv(MyMainWindow.name_linshi1+'/可优化的'+str(res_1.shape[0])+'个小区结果方案.csv', encoding='gbk', index=False)
            print(tm(),'输出结果，存放在py文件根目录中')

            jieguo_hanglie = '处理完成,'+'共计'+str(wt_cell12.shape[0])+'个有效问题小区，输出'+str(res_1.shape[0])+'个问题小区解决方案,文件存放位置{}'.format(MyMainWindow.name_linshi1)
            QMessageBox.about(self, "标题",jieguo_hanglie)
        else:
            QMessageBox.warning(self, "标题", "请选择有效数据后执行")





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
    #--关闭和最小化按钮函数--
    def pushButton_3_c(self):
        """
        关闭窗口
        """
        try:
            print('os guanbi')
            os._exit(5) 
        except Exception as e:
            print('yuanlaide close guanbi')
            self.close()
    def pushButton_c(self):
        """
        最小化窗口
        """
        self.showMinimized()
    #函数============================================ 1 = 2 ================= 打开文件函数（通用）===================
    def qiehuan(self):
        print(tm(),'开始467')
        pushButton_4_name = self.pushButton_4.objectName()
        pushButton_7_name = self.pushButton_7.objectName()
        pushButton_8_name = self.pushButton_8.objectName()
        print(pushButton_4_name,pushButton_7_name,pushButton_8_name)
        sending_button = self.sender()
        print(sending_button.objectName())
        if pushButton_4_name == sending_button.objectName():
            self.stackedWidget.setCurrentIndex(1)
        elif pushButton_7_name == sending_button.objectName():
            self.stackedWidget.setCurrentIndex(2)
        elif pushButton_8_name == sending_button.objectName():
            self.stackedWidget.setCurrentIndex(3)
    def qiehuan_nei(self):
        print(tm(),'开始,qiehuan函数分支')
        pushButton_2_name = self.pushButton_2.objectName()
        print(1)
        pushButton_9_name = self.pushButton_9.objectName()
        print(2)
        pushButton_20_name = self.pushButton_20.objectName()
        pushButton_24_name = self.pushButton_24.objectName()
        pushButton_25_name = self.pushButton_25.objectName()
        pushButton_21_name = self.pushButton_21.objectName()
        pushButton_5_name = self.pushButton_5.objectName()
        pushButton_11_name = self.pushButton_11.objectName()
        pushButton_23_name = self.pushButton_23.objectName()
        pushButton_22_name = self.pushButton_22.objectName()

        sending_button = self.sender()
        print(sending_button.objectName())
        if pushButton_2_name == sending_button.objectName():
            self.stackedWidget_2.setCurrentIndex(0)
        elif pushButton_9_name == sending_button.objectName():
            self.stackedWidget_2.setCurrentIndex(1)
        elif pushButton_20_name == sending_button.objectName():
            self.stackedWidget_2.setCurrentIndex(2)
        elif pushButton_24_name == sending_button.objectName():
            self.stackedWidget_2.setCurrentIndex(3)
        elif pushButton_25_name == sending_button.objectName():
            self.stackedWidget_2.setCurrentIndex(4)
        elif pushButton_21_name == sending_button.objectName():
            self.stackedWidget_2.setCurrentIndex(5)
        elif pushButton_5_name == sending_button.objectName():
            self.stackedWidget_2.setCurrentIndex(6)
        elif pushButton_11_name == sending_button.objectName():
            self.stackedWidget_2.setCurrentIndex(7)
        elif pushButton_23_name == sending_button.objectName():
            self.stackedWidget_2.setCurrentIndex(8)
        elif pushButton_22_name == sending_button.objectName():
            self.stackedWidget_2.setCurrentIndex(9)
    def openMsg_jianshe(self):
        print(tm(),'开始481，打开文件')
        wenti_t = self.pushButton_6.objectName()
        guihua_t = self.pushButton_12.objectName()
        wenti_t_y = self.B_wenti.objectName()
        xianwang_t_y = self.B_jizhan.objectName()

        sender_name = self.sender()
        print(tm(),sender_name.objectName())

        def xxx2(ss, vv=['ca']):
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
        try:
            MyMainWindow.name_linshi1 = os.path.split(MyMainWindow.data_name)[0]
            print(tm(),'打开路径为',MyMainWindow.name_linshi1)
            file, ok = QFileDialog.getOpenFileName(self, "打开", MyMainWindow.name_linshi1,"CSV files (*.txt , *.csv);;Excel files(*.xlsx , *.xls)")
            if 'csv' in(ok):
                try:
                    data_ttt = pd.read_csv(open(file, encoding='gbk'))  # panda
                    # QMessageBox.about(self, "标题", "选择数据成功")
                except:
                    data_ttt = pd.read_csv(open(file))  # pandas
                    # QMessageBox.about(self, "标题", "选择数据成功")
            elif 'Excel' in (ok):
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
            def comboBox_chuli(lie_t = 'lie',
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
                    f.setCurrentIndex(xxx2(lie_t, vv=comboBox_dict[comboBox_t]))
            #------2-问题------------------
            if sender_name.objectName() == wenti_t:
                MyMainWindow.data_name = file
                print(tm(),file)
                print(tm(),'data_name_jianshe_wenti',MyMainWindow.data_name_jianshe_wenti)
                MyMainWindow.data_jianshe_wenti = data_ttt
                lie_jianshe_wenti = MyMainWindow.data_jianshe_wenti.columns.values  # pandas
                comboBox_chuli(lie_t = lie_jianshe_wenti,
                    comboBox_dict = {
                    'comboBox_39':['GI','cg','小区','id','名'],
                    'comboBox_41':['lon','经度'],
                    'comboBox_40':['lat','纬度'],
                    'comboBox_42':['方位','az'],
                    'comboBox_43':['类别','场景'],
                    'comboBox_38':['工作频段','制式']
                    }
                    )
                print(tm(),555)
                print(tm(),MyMainWindow.data_jianshe_wenti.shape)
            #--------2-规划------------------------------------------------------
            elif sender_name.objectName() == guihua_t:
                MyMainWindow.data_name = file
                print(tm(),'data_name_jianshe_guihua',MyMainWindow.data_name_jianshe_guihua)
                MyMainWindow.data_jianshe_guihua = data_ttt
                lie_jianshe_guihua = MyMainWindow.data_jianshe_guihua.columns.values  # pandas
                comboBox_chuli(lie_t = lie_jianshe_guihua,
                    comboBox_dict = {
                    'comboBox_76':['id','规划站号','站','号'],
                    'comboBox_78':['lon','经度'],
                    'comboBox_77':['lat','纬度'],
                    'comboBox_79':['工作频段','制式']
                    }
                    )
                print(tm(),'571')
                print(tm(),MyMainWindow.data_jianshe_guihua.shape)
                #-----------1- 问题 ---------------------------------------------------

            elif sender_name.objectName() == wenti_t_y:
                MyMainWindow.data_name = file
                print(tm(),'data_name',MyMainWindow.data_name)
                MyMainWindow.data_wenti = data_ttt
                print(tm(),'579')
                lie_wenti = MyMainWindow.data_wenti.columns.values  # pandas
                print(tm(),lie_wenti)
                comboBox_chuli(lie_t = lie_wenti,
                    comboBox_dict = {
                    'comboBox_45':['cgi','名','cell','id','号'],
                    'comboBox_47':['lon','经度'],
                    'comboBox_46':['lat','纬度'],
                    'comboBox_48':['az','方位'],
                    'comboBox_49':['类别','场景'],
                    'comboBox_44':['频段','制式'],
                    'comboBox_51':['挂高', '高度','高','high'],
                    'comboBox_52':['下倾','倾角'],
                    'comboBox_50':['故障', '告警','状态','统计分类']
                    }
                    )
                print(tm(),MyMainWindow.data_wenti.shape)
                # -----------1- 现网 ---------------------------------------------------
            elif sender_name.objectName() == xianwang_t_y:
                MyMainWindow.data_name = file
                print(tm(),'data_name_2',MyMainWindow.data_name_2)
                MyMainWindow.data_xianwang = data_ttt
                print(tm(),'41')
                lie_xianwang = MyMainWindow.data_xianwang.columns.values  # pandas
                comboBox_chuli(lie_t = lie_xianwang,
                    comboBox_dict = {
                    'comboBox_80':['cgi','名','cell','id','号'],
                    'comboBox_82':['lon','经度'],
                    'comboBox_81':['lat','纬度'],
                    'comboBox_83':['频段','制式'],
                    'comboBox_85':['挂高', '高度','高','high'],
                    'comboBox_84':['故障', '告警','状态','统计分类']
                    }
                    )
                print(tm(),MyMainWindow.data_xianwang.shape)
            QMessageBox.about(self, "标题", "选择数据成功")
        except:
            QMessageBox.warning(self, "标题", "选择数据有误")
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
    def openfile_tu(self):
        MyMainWindow.name_linshi1 = os.path.split(MyMainWindow.data_name)[0]
        print(tm(),'打开路径为',MyMainWindow.name_linshi1)
        try:
            file, ok = QFileDialog.getOpenFileName(self, "打开", MyMainWindow.name_linshi1,"gis files (*.tab , *.shp);;geo files(*.geojson , *.json)")
            try:
                data_ttt = gpd.read_file(file, encoding='gbk') # panda
                # QMessageBox.about(self, "标题", "选择数据成功")
            except:
                try:
                    data_ttt = gpd.read_file(file, encoding='utf-8') # pandas
                    # QMessageBox.about(self, "标题", "选择数据成功")
                except:
                    try:
                        data_ttt = gpd.read_file(open(file, encoding='gbk'))  # pandas
                    except:
                        data_ttt = gpd.read_file(open(file, encoding='utf-8'))  # pandas
            return [data_ttt,file]
        except:
            QMessageBox.warning(self, "标题", "选择数据有误")
            
    def openfile(self):
        MyMainWindow.name_linshi1 = os.path.split(MyMainWindow.data_name)[0]
        print(tm(),'打开路径为',MyMainWindow.name_linshi1)
        try:
            file, ok = QFileDialog.getOpenFileName(self, "打开", MyMainWindow.name_linshi1,"one files (*.xlsx , *.xls, *.csv)")
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

    #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓--2--↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓--执行2建设类的函数-开始-↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    def kaishi_2(self):
        if (MyMainWindow.data_jianshe_wenti.shape[0]>0)&(MyMainWindow.data_jianshe_guihua.shape[0]>0):
            #获取所有参数的值x（问题小区）
            print(tm(),'开始执行建设类的方案计算')
            xiaoquming_2_x = self.comboBox_39.currentText()  # 获取下拉菜单的值
            lon_2_x = self.comboBox_41.currentText()  # 获取下拉菜单的值
            lat_2_x = self.comboBox_40.currentText()  # 获取下拉菜单的值
            fangwei_2_x = self.comboBox_42.currentText()  # 获取下拉菜单的值
            leibie_2_x = self.comboBox_43.currentText()  # 获取下拉菜单的值
            zhishi_2_x = self.comboBox_38.currentText()  # 获取下拉菜单的值

            cj_900_hxcq_2_x = self.lineEdit_77.text()  # 获取单行输入框
            cj_900_ybcq_2_x = self.lineEdit_80.text()  # 获取单行输入框
            cj_900_cj_2_x = self.lineEdit_76.text()  # 获取单行输入框
            cj_900_xc_2_x = self.lineEdit_79.text()  # 获取单行输入框
            cj_900_xz_2_x = self.lineEdit_57.text()  # 获取单行输入框
            cj_900_nc_2_x = self.lineEdit_55.text()  # 获取单行输入框

            cj_1800_hxcq_2_x = self.lineEdit_74.text()  # 获取单行输入框
            cj_1800_ybcq_2_x = self.lineEdit_73.text()  # 获取单行输入框
            cj_1800_cj_2_x = self.lineEdit_56.text()  # 获取单行输入框
            cj_1800_xc_2_x = self.lineEdit_54.text()  # 获取单行输入框
            cj_1800_xz_2_x = self.lineEdit_78.text()  # 获取单行输入框
            cj_1800_nc_2_x = self.lineEdit_75.text()  # 获取单行输入框

            cj_fanbei_2_x = self.lineEdit_81.text()  # 获取单行输入框
            cj_bobankuaidu_2_x = self.spinBox_8.value() #获取计数器的值

            #获取所有参数的值y（规划站点）
            xiaoquming_2_y = self.comboBox_76.currentText()  # 获取下拉菜单的值
            lon_2_y = self.comboBox_78.currentText()  # 获取下拉菜单的值
            lat_2_y = self.comboBox_77.currentText()  # 获取下拉菜单的值
            zhishi_2_y = self.comboBox_79.currentText()  # 获取下拉菜单的值
            print(tm(),'准备做图层')
            #作图层
            def juli_2(df, changjing, pinduan,beishu=1):
                try:
                    F900 = {0: cj_900_hxcq_2_x, 1: cj_900_ybcq_2_x, 2: cj_900_cj_2_x, 3: cj_900_xc_2_x, 4: cj_900_xz_2_x, 5: cj_900_nc_2_x}
                    TDD = {0: cj_1800_hxcq_2_x, 1: cj_1800_ybcq_2_x, 2: cj_1800_cj_2_x, 3: cj_1800_xc_2_x, 4: cj_1800_xz_2_x, 5: cj_1800_nc_2_x}
                    df['juli'] = [F900[cj] if pid == 'FDD900' else TDD[cj] 
                            for cj, pid in zip(df[changjing], df[pinduan])]
                except:
                    F900 = {'主城区': cj_900_hxcq_2_x, '一般城区': cj_900_ybcq_2_x, '市郊': cj_900_cj_2_x, '县城': cj_900_xc_2_x, '乡镇': cj_900_xz_2_x, '农村': cj_900_nc_2_x}
                    TDD = {'主城区': cj_1800_hxcq_2_x, '一般城区': cj_1800_ybcq_2_x, '市郊': cj_1800_cj_2_x, '县城': cj_1800_xc_2_x, '乡镇': cj_1800_xz_2_x, '农村': cj_1800_nc_2_x}
                    df['juli'] = [F900[cj] if pid == 'FDD900' else TDD[cj] 
                            for cj, pid in zip(df[changjing], df[pinduan])]                    

                df['juli'] = pd.to_numeric(df['juli'])
                df['juli'] = df['juli']*float(beishu)
                return df
            print('copy数据',MyMainWindow.data_jianshe_wenti.shape)
            data_2copy=MyMainWindow.data_jianshe_wenti.copy()
            print('to_numeric',leibie_2_x)
            try:
                data_2copy[leibie_2_x] = pd.to_numeric(data_2copy[leibie_2_x])
            except:
                pass
            print('开始执行juli_2')
            data_jianshe_wenti_jl = juli_2(data_2copy,leibie_2_x,zhishi_2_x,beishu = float(cj_fanbei_2_x))
            print(tm(),data_jianshe_wenti_jl.info())
            print(tm(),lon_2_x,lat_2_x,fangwei_2_x)
            data_wenti_2_s = add_sectors_df(data_jianshe_wenti_jl, coords=[lon_2_x,lat_2_x,'d_height',fangwei_2_x,'juli'], has_z=False, sec_col='geometry', shape_dict={'beam': int(cj_bobankuaidu_2_x),'per_degree': 10})
            print(tm(),MyMainWindow.data_jianshe_guihua.info())
            data_guihua_2_p = add_points(MyMainWindow.data_jianshe_guihua,lon_2_y,lat_2_y)
            data_wenti_2_s.rename(columns = {xiaoquming_2_x:'xiaoquming_2_x',lon_2_x:'lon_2_x',lat_2_x:'lat_2_x'},inplace = True)
            data_guihua_2_p.rename(columns = {xiaoquming_2_y:'xiaoquming_2_y',lon_2_y:'lon_2_y',lat_2_y:'lat_2_y'},inplace = True)
            data_2_res = gpd.sjoin(data_wenti_2_s,data_guihua_2_p)
            print(tm(),data_2_res.shape)
            data_2_res_juli = distancea_df(data_2_res,'lon_2_x','lat_2_x','lon_2_y','lat_2_y')
            data_2_res_juli_qc = data_2_res_juli.sort_values('距离')
            data_2_res_juli_qc_res = data_2_res_juli_qc.drop_duplicates('xiaoquming_2_x')
            print(tm(),'开始导出数据')
            data_2_res_juli_qc_res.to_csv(MyMainWindow.name_linshi1+'/可建设的'+str(data_2_res_juli_qc_res.shape[0])+'个小区结果方案.csv', encoding='gbk', index=False)
            print(tm(),'输出结果，存放在py文件根目录中')
            jieguo_hanglie_2 = '处理完成,'+'共计'+str(data_jianshe_wenti_jl.shape[0])+'个问题小区，输出'+str(data_2_res_juli_qc_res.shape[0])+'个问题小区建设解决方案'+MyMainWindow.name_linshi1
            QMessageBox.about(self, "标题",jieguo_hanglie_2 )

    #↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑--2--↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑--执行2的函数-完成-↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-----↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-----↓↓↓↓↓↓↓↓↓-工具sheet中的第一个程序计算站间距-开始↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    def xuanze_file_zhanjianju(self):
        print(tm(),'开始打开')
        MyMainWindow.data_zhanjianju,file_name_zz = self.openfile()
        if file_name_zz=='open_false':
            pass
        else:
            MyMainWindow.data_zhanjianju_file_name = file_name_zz
            print(tm(),file_name_zz)
            print(tm(),'data_name_jianshe_wenti',MyMainWindow.data_zhanjianju_file_name)
            lie_zhanjianju = MyMainWindow.data_zhanjianju.columns.values  # pandas
            self.comboBox_chuli(lie_t = lie_zhanjianju,
                comboBox_dict = {
                'comboBox_58':['GI','cg','小区','id','名'],
                'comboBox_6':['lon','经度'],
                'comboBox_7':['lat','纬度']
                }
                )
            print(tm(),'打开文件完成')
            print(tm(),MyMainWindow.data_zhanjianju.shape)
            QMessageBox.about(self, "标题", "选择数据成功")
    def kaishi_zhanjianju(self):
        if MyMainWindow.data_zhanjianju.shape[0]>1:
            #获取所有参数的值x（问题小区）
            print(tm(),'获取选择值')
            zhanjianju_data_use = MyMainWindow.data_zhanjianju
            print(tm(),'数据共计',zhanjianju_data_use.shape)
            zhanjianju_id = self.comboBox_58.currentText()  # 获取下拉菜单的值
            zhanjianju_lon = self.comboBox_6.currentText()  # 获取下拉菜单的值
            zhanjianju_lat = self.comboBox_7.currentText()  # 获取下拉菜单的值

            zhanjianju_max_d = self.lineEdit_6.text()  # 获取单行输入框
            zhanjianju_n_nmb = self.lineEdit_7.text()  # 获取单行输入框
            print(tm(),'开始执行站间距的计算')
            print(zhanjianju_id,zhanjianju_lon,zhanjianju_lat,zhanjianju_n_nmb,zhanjianju_max_d)
            res = nearest_site(
                zhanjianju_data_use,
                id_name_column=zhanjianju_id,lon=zhanjianju_lon,
                lat=zhanjianju_lat,
                num_min_results = int(zhanjianju_n_nmb),
                Including_itself = False,
                juli_n = int(zhanjianju_max_d))
            print(tm(),'开始导出数据')
            res.to_csv(MyMainWindow.data_zhanjianju_file_name.split('.')[0]+'_站间距.csv', encoding='gbk', index=False)
            print(tm(),'输出结果，存放在py文件根目录中')
            QMessageBox.about(self, "标题",'完成输出至文件源目录' )
        else:
            QMessageBox.warning(self, "标题", "请选择有效数据后执行")
    #↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-----↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-----↑↑↑↑↑↑↑↑↑-工具sheet中的第一个程序计算站间距-完成-↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-----↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-----↓↓↓↓↓↓↓↓↓↓↓↓工具sheet中的第二个程序单表最近-开始-↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    def xuanze_file_danbiaozuijin(self):
        print(tm(),'开始打开') 
        MyMainWindow.data_danbiaozuijin,file_name_zz = self.openfile()
        if file_name_zz=='open_false':
            pass
        else:
            MyMainWindow.data_danbiaozuijin_file_name = file_name_zz
            print(tm(),file_name_zz)
            print(tm(),'data_name_单表最近',MyMainWindow.data_danbiaozuijin_file_name)
            lie_danbiaozuijin = MyMainWindow.data_danbiaozuijin.columns.values  # pandas
            self.comboBox_chuli(lie_t = lie_danbiaozuijin,
                comboBox_dict = {
                'comboBox_62':['GI','cg','小区','id','名'],
                'comboBox_11':['lon','经度'],
                'comboBox_12':['lat','纬度']
                }
                )
            print(tm(),'打开文件完成')
            print(tm(),MyMainWindow.data_danbiaozuijin.shape)
            QMessageBox.about(self, "标题", "选择数据成功")
    def kaishi_danbiaozuijin(self):
        if MyMainWindow.data_danbiaozuijin.shape[0]>1:
            #获取所有参数的值x（问题小区）
            print(tm(),'获取选择值')
            print(tm(),'数据共计',MyMainWindow.data_danbiaozuijin.shape)
            danbiaozuijin_id = self.comboBox_62.currentText()  # 获取下拉菜单的值
            danbiaozuijin_lon = self.comboBox_11.currentText()  # 获取下拉菜单的值
            danbiaozuijin_lat = self.comboBox_12.currentText()  # 获取下拉菜单的值

            danbiaozuijin_n_nmb = self.lineEdit_8.text()  # 获取单行输入框
            print(danbiaozuijin_id,danbiaozuijin_lon,danbiaozuijin_lat,danbiaozuijin_n_nmb)
            print(tm(),'开始执行站间距的计算')
            res = nearest_site_one(MyMainWindow.data_danbiaozuijin,
                id_name_column=danbiaozuijin_id,
                lon=danbiaozuijin_lon,
                lat=danbiaozuijin_lat,
                num_min_results = int(danbiaozuijin_n_nmb),
                Including_itself = False
                )
            print(tm(),'开始导出数据')
            res.to_csv(MyMainWindow.data_danbiaozuijin_file_name.split('.')[0]+'_单表最近.csv', encoding='gbk', index=False)
            print(tm(),'输出结果，存放在py文件根目录中')
            QMessageBox.about(self, "标题",'完成输出至文件源目录' )
        else:
            QMessageBox.warning(self, "标题", "请选择有效数据后执行")
    #↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-----↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-----↑↑↑↑↑↑↑↑↑↑↑↑工具sheet中的第二个程序单表最近-完成-↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


    #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-----↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-----↓↓↓↓↓↓↓↓↓工具sheet中的第三个程序双表最近-开始-↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    def xuanze_file_shuangbiaozuijin_x(self):
        print(tm(),'开始打开') 
        MyMainWindow.data_shuangbiaozuijin_x,file_name_zz = self.openfile()
        if file_name_zz=='open_false':
            pass
        else:
            MyMainWindow.data_shuangbiaozuijin_file_name_x = file_name_zz
            print(tm(),file_name_zz)
            print(tm(),'data_name_单表最近',MyMainWindow.data_shuangbiaozuijin_file_name_x)
            lie_shangbiaozuijin = MyMainWindow.data_shuangbiaozuijin_x.columns.values  # pandas
            self.comboBox_chuli(lie_t = lie_shangbiaozuijin,
                comboBox_dict = {
                'comboBox_16':['lon','经度'],
                'comboBox_15':['lat','纬度']
                }
                )
            print(tm(),'打开文件完成')
            print(tm(),MyMainWindow.data_shuangbiaozuijin_x.shape)
            QMessageBox.about(self, "标题", "选择数据成功")
    def xuanze_file_shuangbiaozuijin_y(self):
        print(tm(),'开始打开') 
        MyMainWindow.data_shuangbiaozuijin_y,file_name_zz = self.openfile()
        if file_name_zz=='open_false':
            pass
        else:
            print(tm(),file_name_zz)
            print(tm(),'data_name_单表最近',file_name_zz)
            lie_shuangbiaozuijin_y = MyMainWindow.data_shuangbiaozuijin_y.columns.values  # pandas
            self.comboBox_chuli(lie_t = lie_shuangbiaozuijin_y,
                comboBox_dict = {
                'comboBox_14':['lon','经度'],
                'comboBox_13':['lat','纬度']
                }
                )
            print(tm(),'打开文件完成')
            print(tm(),MyMainWindow.data_shuangbiaozuijin_y.shape)
            QMessageBox.about(self, "标题", "选择数据成功")
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

    #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-----↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-工具sheet第四个程序图层与表相交-开始-↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    def xuanze_file_biaoguanliantu_x(self):
        print(tm(),'开始打开') 
        MyMainWindow.data_biaoguanliantu_x,file_name_zz = self.openfile_tu()
        print(tm(),file_name_zz)
        print(tm(),'打开文件完成')
        print(tm(),MyMainWindow.data_biaoguanliantu_x.shape)
        QMessageBox.about(self, "标题", "选择图层成功")
    def xuanze_file_biaoguanliantu_y(self):
        print(tm(),'开始打开') 
        MyMainWindow.data_biaoguanliantu_y,file_name_zz = self.openfile()
        if file_name_zz=='open_false':
            pass
        else:
            MyMainWindow.data_biaoguanliantu_file_name_y = file_name_zz
            print(tm(),file_name_zz)
            print(tm(),'data_name_单表最近',MyMainWindow.data_biaoguanliantu_file_name_y)
            lie_biaoguanliantu_y = MyMainWindow.data_biaoguanliantu_y.columns.values  # pandas
            self.comboBox_chuli(lie_t = lie_biaoguanliantu_y,
            comboBox_dict = {
                'comboBox_63':['lon','经度'],
                'comboBox_64':['lat','纬度']
                }
                )
            print(tm(),'打开文件完成')
            print(tm(),MyMainWindow.data_biaoguanliantu_y.shape)
            QMessageBox.about(self, "标题", "选择数据成功")
    def kaishi_biaoguanliantu(self):
        if (MyMainWindow.data_biaoguanliantu_x.shape[0]>0) & (MyMainWindow.data_biaoguanliantu_y.shape[0]>1): 
            #获取所有参数的值x（问题小区）
            print(tm(),'获取选择值')
            print(tm(),'数据共计',MyMainWindow.data_biaoguanliantu_x.shape)
            print(tm(),'数据共计',MyMainWindow.data_biaoguanliantu_y.shape)
            biaoguanliantu_lon = self.comboBox_63.currentText()  # 获取下拉菜单的值
            biaoguanliantu_lat = self.comboBox_64.currentText()  # 获取下拉菜单的值
            biaoguanliantu_fangshi = self.comboBox_65.currentText()  # 获取下拉菜单的值
            print(tm(),'开始执行站间距的计算1，转换crs')
            tu2 = MyMainWindow.data_biaoguanliantu_x.to_crs({"init": "epsg:4326"})
            print(tm(),'坐标系转换成功')
            data_p = add_points(MyMainWindow.data_biaoguanliantu_y,biaoguanliantu_lon,biaoguanliantu_lat)
            print(tm(),'创建点成功')
            print(tm(),'开始相交')
            if biaoguanliantu_fangshi=='相交-图层信息在左边':
                res = gpd.sjoin(tu2,data_p)
            else:
                res = gpd.sjoin(data_p,tu2)
            print(tm(),'相交结束')
            res = res.drop(columns='geometry')
            print(tm(),'开始导出数据')
            res.to_csv(MyMainWindow.data_biaoguanliantu_file_name_y.split('.')[0]+'_图层关联.csv', encoding='gbk', index=False)
            print(tm(),'输出结果，存放在py文件根目录中')
            QMessageBox.about(self, "标题",'完成输出至文件源目录' )  
        else:
            QMessageBox.warning(self, "标题", "请选择有效数据后执行")
    #↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-----↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-工具sheet第四个程序图层与表相交-完成-↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-----↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-----↓↓↓↓↓↓↓↓↓-开始-↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    def openfile_files_name(self):
        MyMainWindow.name_linshi1 = os.path.split(MyMainWindow.data_name)[0]
        print(tm(),'打开路径为',MyMainWindow.name_linshi1)
        try:
            files_name = QFileDialog.getExistingDirectory(self,"选取文件夹","C:/")
        except:
            QMessageBox.warning(self, "标题", "选择数据有误")
        return [files_name]
    def xuanze_file_biaohechai(self):
        print(tm(),'开始打开') 
        MyMainWindow.file_biaochaihe_name = self.openfile_files_name()
        if MyMainWindow.file_biaochaihe_name[0]=='':
            QMessageBox.warning(self, "标题", "选择文件夹失败")
        else:
            print(tm(),MyMainWindow.file_biaochaihe_name)
            print(tm(),'打开文件完成')
            QMessageBox.about(self, "标题", "选择文件夹成功")
    def xuanze_file_biaohechai_data(self):
        print(tm(),'开始打开')
        MyMainWindow.data_biaochaihe , MyMainWindow.biaochaihe_name = self.openfile()
        if MyMainWindow.biaochaihe_name=='open_false':
            pass
        else:
            lie_biaochaihe = MyMainWindow.data_biaochaihe.columns.values  # pandas
            self.comboBox_chuli(lie_t = lie_biaochaihe,
                comboBox_dict = {
                'comboBox_67':['地市','city','城市','区县']
                }
                )
            print(tm(),MyMainWindow.biaochaihe_name)
            print(tm(),'打开文件完成')
            QMessageBox.about(self, "标题", "选择数据成功")

    def kaishi_biaohechai_he(self):
        if len(MyMainWindow.file_biaochaihe_name) <1 :
            QMessageBox.warning(self, "标题", "请选择有效数据后执行")
        else:
            #获取所有参数的值x（问题小区）
            print(tm(),'获取选择值')
            print(tm(),'目录为',MyMainWindow.file_biaochaihe_name)
            biaogehechai_leixing = self.comboBox_66.currentText()  # 获取下拉菜单的值
            biaogehechai_bianma = self.comboBox_68.currentText()  # 获取下拉菜单的值

            print(tm(),'选择表格的类型为',biaogehechai_leixing)
            print(tm(),'选择的编码为',biaogehechai_bianma)
            print(tm(),'存放表的文件夹为',MyMainWindow.file_biaochaihe_name)
            file_names_lishi = MyMainWindow.file_biaochaihe_name[0]
            res = pd.DataFrame()
            print(tm(),'开始汇总数据...')
            f = file_name_paths(path=file_names_lishi,find=biaogehechai_leixing)
            print(f)
            print(22)
            for name in f:
                print(name)
                if biaogehechai_leixing == 'CSV':
                    if biaogehechai_bianma == 'GBK':
                        print(33)
                        try:
                            data_t = pd.read_csv(name,encoding='gbk')
                            print(333)
                        except:
                            try:
                                data_t = pd.read_csv(open(name,encoding='gbk'))
                            except:
                                QMessageBox.about(self, "标题",'数据读取失败，检查类型和编码格式以及数据一致性' ) 
                                break
                    elif biaogehechai_leixing == 'UTF-8':
                        print(44)
                        try:
                            data_t = pd.read_csv(name,encoding='utf-8')
                        except:
                            try:
                                data_t = pd.read_csv(open(name,encoding='utf-8'))
                            except:
                                QMessageBox.about(self, "标题",'数据读取失败，检查类型和编码格式以及数据一致性' ) 
                                break
                    else:
                        print(55)
                        try:
                            data_t = pd.read_csv(name,encoding='utf-8',sep='\t')
                        except:
                            try:
                                data_t = pd.read_csv(open(name,encoding='utf-8'),sep='\t')
                            except:
                                QMessageBox.about(self, "标题",'数据读取失败，检查类型和编码格式以及数据一致性' ) 
                                break
                elif biaogehechai_leixing == 'EXCEL':
                    if biaogehechai_bianma == 'GBK':
                        try:
                            data_t = pd.read_excle(name,encoding='gbk')
                        except:
                            QMessageBox.about(self, "标题",'数据读取失败，检查类型和编码格式以及数据一致性' ) 
                            break
                    elif biaogehechai_leixing == 'UTF-8':
                        try:
                            ata_t = pd.read_excel(name,encoding='utf-8')
                        except:
                            QMessageBox.about(self, "标题",'数据读取失败，检查类型和编码格式以及数据一致性' ) 
                            break
                    else:
                        try:
                            data_t = pd.read_excel(name,encoding='utf-8',sep='\t')
                        except:
                            QMessageBox.about(self, "标题",'数据读取失败，检查类型和编码格式以及数据一致性' ) 
                            break
                else:
                    if biaogehechai_bianma == 'GBK':
                        try:
                            data_t = pd.read_txt(name,encoding='gbk')
                        except:
                            QMessageBox.about(self, "标题",'数据读取失败，检查类型和编码格式以及数据一致性' ) 
                            break
                    elif biaogehechai_leixing == 'UTF-8':
                        try:
                            data_t = pd.read_txt(name,encoding='utf-8')
                        except:
                            QMessageBox.about(self, "标题",'数据读取失败，检查类型和编码格式以及数据一致性' ) 
                            break
                    else:
                        try:
                            data_t = pd.read_txt(name,encoding='utf-8',sep='\t')
                        except:
                            QMessageBox.about(self, "标题",'数据读取失败，检查类型和编码格式以及数据一致性' ) 
                            break
                res = res.append(data_t)
            print(tm(),'合并成功')
            res.to_csv(MyMainWindow.file_biaochaihe_name[0]+'/合并后数据.csv', encoding='gbk', index=False)
            print(tm(),'输出结果，存放在py文件根目录中')
            QMessageBox.about(self, "标题",'完成输出至文件源目录' )  

    def kaishi_biaohechai_chai(self):
        if MyMainWindow.data_biaochaihe.shape[0]>1:
            #获取所有参数的值x（问题小区）
            print(tm(),'获取选择值')
            print(tm(),'导入数据总数',MyMainWindow.data_biaochaihe.shape)
            print(tm(),'导入数据位置',MyMainWindow.biaochaihe_name)
            data_use_1 = MyMainWindow.data_biaochaihe
            groupy_columns = self.comboBox_67.currentText()  # 获取下拉菜单的值
            row_nmb = self.lineEdit_9.text()  # 获取单行输入框
            fen_lie = self.radioButton.isChecked()
            fen_row = self.radioButton_2.isChecked()
            if fen_lie:
                print(tm(),'开始导出数据')
                data_groupby = data_use_1.groupby(groupy_columns)
                for name , data_t in data_groupby:
                    data_t.to_csv(MyMainWindow.biaochaihe_name.split('.')[0]+'_'+name+'.csv',encoding='gbk',index=False)
            elif fen_row:
                print(tm(),'开始导出数据')
                print(tm(),'按照行数输出',row_nmb)
                print(data_use_1.shape,int(row_nmb))
                a = df_yield(data_use_1,number=int(row_nmb),print_info=True)
                nn_m = 1
                print(tm(),'开始')
                for data_t in a:
                    print('循环')
                    data_t.to_csv(MyMainWindow.biaochaihe_name.split('.')[0]+str(nn_m)+'.csv',encoding='gbk',index=False)
                    nn_m = nn_m+1
            print(tm(),'输出结果，存放在py文件根目录中')
            QMessageBox.about(self, "标题",'完成输出至文件源目录' )  
        else:
            QMessageBox.warning(self, "标题", "请选择有效数据后执行")
    #↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-----↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-----↑↑↑↑↑↑↑↑↑-完成-↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-----↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-----↓↓↓↓↓↓↓↓↓↓↓↓buff_圈点开始-↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    def buff_quandian_x(self):
        print(tm(),'开始打开')
        MyMainWindow.data_buff_qd_x,file_name_zz = self.openfile()
        if file_name_zz=='open_false':
            pass
        else:
            MyMainWindow.buff_qd_file_name_x = file_name_zz
            print(tm(),file_name_zz)
            print(tm(),'buff_qd_file_name_x',MyMainWindow.buff_qd_file_name_x)
            lie_buff_qd = MyMainWindow.data_buff_qd_x.columns.values  # pandas
            self.comboBox_chuli(lie_t = lie_buff_qd,
                comboBox_dict = {
                'comboBox_69':['lon','经度'],
                'comboBox_70':['lat','纬度'],
                'comboBox_71':['dis','距离','半径']
                }
                )
            print(tm(),'打开文件完成')
            print(tm(),MyMainWindow.data_buff_qd_x.shape)
            QMessageBox.about(self, "标题", "选择数据成功")
    def buff_quandian_y(self):
        print(tm(),'开始打开')
        MyMainWindow.data_buff_qd_y,file_name_zz = self.openfile()
        if file_name_zz=='open_false':
            pass
        else:
            print(tm(),file_name_zz)
            lie_buff_qd_y = MyMainWindow.data_buff_qd_y.columns.values  # pandas
            self.comboBox_chuli(lie_t = lie_buff_qd_y,
                comboBox_dict = {
                'comboBox_72':['lon','经度'],
                'comboBox_73':['lat','纬度']
                }
                )
            print(tm(),'打开文件完成')
            print(tm(),MyMainWindow.data_buff_qd_y.shape)
            QMessageBox.about(self, "标题", "选择数据成功")
    def kaishi_buffer_qd(self):
        if (MyMainWindow.data_buff_qd_x.shape[0]>1) & (MyMainWindow.data_buff_qd_y.shape[0]>1):
            #获取所有参数的值x（问题小区）
            print(tm(),'获取选择值')
            print(tm(),'数据共计',MyMainWindow.data_buff_qd_x.shape)
            print(tm(),'数据共计',MyMainWindow.data_buff_qd_y.shape)
            lon_x = self.comboBox_69.currentText()  # 获取下拉菜单的值
            lat_x = self.comboBox_70.currentText()  # 获取下拉菜单的值
            lie_x = self.comboBox_71.currentText()  # 获取下拉菜单的值
            lon_y = self.comboBox_72.currentText()  # 获取下拉菜单的值
            lat_y = self.comboBox_73.currentText()  # 获取下拉菜单的值
            juli = self.lineEdit_10.text()  # 获取单行输入框
            shuru_juli = self.radioButton_3.isChecked() #是否选中故障
            de_juli = self.radioButton_4.isChecked() #是否选中故障
            print(tm(),'开始生成buff')
            print(int(juli))
            if shuru_juli==True:
                print(tm(),'使用的是输入距离')
                data_buff = add_buffer(MyMainWindow.data_buff_qd_x,
                                        lon=lon_x,
                                        lat=lat_x,
                                        buff_float= int(juli) ,
                                        geometry='geometry'
                                        )
            elif de_juli==True:
                print(tm(),'使用的是列中的距离')
                data_buff = add_buffer_df(MyMainWindow.data_buff_qd_x,
                                            lon=lon_x,
                                            lat=lat_x,
                                            buff_col=lie_x,
                                            geometry='geometry'
                                            )
            print(tm(),'生成buff完成')
            print(tm(),'开始生成y的点')
            data_y_p = add_points(MyMainWindow.data_buff_qd_y,
                                    lon=lon_y,
                                    lat=lat_y,
                                    pnt_col='geometry'
                                    )

            print(tm(),'开始sjoin计算')
            res = gpd.sjoin(data_buff,data_y_p)
            print(tm(),'sjoin计算完成')
            res = res.drop(columns='geometry')
            print(tm(),'开始导出数据')
            res.to_csv(MyMainWindow.buff_qd_file_name_x.split('.')[0]+'_buff圈的点.csv', encoding='gbk', index=False)
            print(tm(),'输出结果，存放在{}目录中'.format(MyMainWindow.buff_qd_file_name_x.split('.')[0]))
            QMessageBox.about(self, "标题",'完成输出至文件源目录' ) 
        else:
            QMessageBox.warning(self, "标题", "请选择有效数据后执行")

    #↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-----↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-----↑↑↑↑↑↑↑↑↑↑↑↑-完成-↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


    #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-----↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-----↓↓↓↓↓↓↓↓↓扇形圈点-开始-↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    def shanqu_quandian_x(self):
        print(tm(),'开始打开')
        MyMainWindow.data_shanqu_qd_x,file_name_zz = self.openfile()
        if file_name_zz=='open_false':
            pass
        else:
            MyMainWindow.shanqu_qd_file_name_x = file_name_zz
            print(tm(),file_name_zz)
            print(tm(),'shanqu_qd_file_name_x',MyMainWindow.shanqu_qd_file_name_x)
            lie_shanqu_qd = MyMainWindow.data_shanqu_qd_x.columns.values  # pandas
            self.comboBox_chuli(lie_t = lie_shanqu_qd,
                comboBox_dict = {
                'comboBox_75':['lon','经度'],
                'comboBox_86':['lat','纬度'],
                'comboBox_87':['am','方位'],
                'comboBox_74':['dis','距离','半径','juli']
                }
                )
            print(tm(),'打开文件完成')
            print(tm(),MyMainWindow.data_shanqu_qd_x.shape)
            QMessageBox.about(self, "标题", "选择数据成功")
    def shanqu_quandian_y(self):
        print(tm(),'开始打开')
        MyMainWindow.data_shanqu_qd_y,file_name_zz = self.openfile()
        if file_name_zz=='open_false':
            pass
        else:
            print(tm(),file_name_zz)
            lie_shanqu_qd_y = MyMainWindow.data_shanqu_qd_y.columns.values  # pandas
            self.comboBox_chuli(lie_t = lie_shanqu_qd_y,
                comboBox_dict = {
                'comboBox_89':['lon','经度'],
                'comboBox_88':['lat','纬度']
                }
                )
            print(tm(),'打开文件完成')
            print(tm(),MyMainWindow.data_shanqu_qd_y.shape)
            QMessageBox.about(self, "标题", "选择数据成功")
    def kaishi_shanqu_qd(self):
        if (MyMainWindow.data_shanqu_qd_x.shape[0]>1) & (MyMainWindow.data_shanqu_qd_y.shape[0]>1):
            #获取所有参数的值x（问题小区）
            print(tm(),'获取选择值')
            print(tm(),'数据共计',MyMainWindow.data_shanqu_qd_x.shape)
            print(tm(),'数据共计',MyMainWindow.data_shanqu_qd_y.shape)
            lon_x = self.comboBox_75.currentText()  # 获取下拉菜单的值
            lat_x = self.comboBox_86.currentText()  # 获取下拉菜单的值
            fw_x = self.comboBox_87.currentText()  # 获取下拉菜单的值
            lie_x = self.comboBox_74.currentText()  # 获取下拉菜单的值
            lon_y = self.comboBox_89.currentText()  # 获取下拉菜单的值
            lat_y = self.comboBox_88.currentText()  # 获取下拉菜单的值
            juli = self.lineEdit_12.text()  # 获取单行输入框
            shanqu_bobankuaidu = self.spinBox.value() #获取计数器的值
            shuru_juli = self.radioButton_5.isChecked() #是否选中故障
            df_juli = self.radioButton_6.isChecked() #是否选中故障
            print(tm(),'开始生成扇区')
            print(int(juli))
            if shuru_juli==True:
                print(tm(),'使用的是输入距离')
                data_buff = add_sectors(MyMainWindow.data_shanqu_qd_x,
                                        coords=[lon_x,lat_x,'',fw_x],
                                        has_z=False,
                                        sec_col='geometry',
                                        shape_dict={
                                            'radius': int(juli),
                                            'beam': int(shanqu_bobankuaidu),
                                            'per_degree': 10
                                        })
            elif df_juli==True:
                print(tm(),'使用的是列中的距离')
                data_buff = add_sectors_df(MyMainWindow.data_shanqu_qd_x,
                                            coords=[lon_x,lat_x,'d_height',fw_x,lie_x],
                                            has_z=False,
                                            sec_col='geometry',
                                            shape_dict={'beam': int(shanqu_bobankuaidu),'per_degree': 10})
            print(tm(),'生成扇区完成')
            print(tm(),'开始生成y的点')
            data_y_p = add_points(MyMainWindow.data_shanqu_qd_y,
                                    lon=lon_y,
                                    lat=lat_y,
                                    pnt_col='geometry'
                                    )

            print(tm(),'开始sjoin计算')
            res = gpd.sjoin(data_buff,data_y_p)
            print(tm(),'sjoin计算完成')
            res = res.drop(columns='geometry')
            print(tm(),'开始导出数据')
            res.to_csv(MyMainWindow.shanqu_qd_file_name_x.split('.')[0]+'_扇区圈的点.csv', encoding='gbk', index=False)
            print(tm(),'输出结果，存放在{}目录中'.format(MyMainWindow.shanqu_qd_file_name_x.split('.')[0]))
            QMessageBox.about(self, "标题",'完成输出至文件源目录' ) 
        else:
            QMessageBox.warning(self, "标题", "请选择有效数据后执行")
    #↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-----↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-----↑↑↑↑↑↑↑↑↑扇形圈点-完成-↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-----↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓-----↓↓↓↓↓↓↓↓↓↓↓↓-开始-↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    #↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-----↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑-----↑↑↑↑↑↑↑↑↑↑↑↑-完成-↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    # app = 0
    app = QApplication(sys.argv)#声明变量
    myWin = MyMainWindow()#创建窗口
    #样式可批量操作
    # qssStyle = MyStyleSheet.button_style_z()
    # myWin.setStyleSheet(qssStyle)
    #设置图标
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("poto/tubiao2.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
    myWin.setWindowIcon(icon)

    myWin.show()#todo 正常比例显示
    sys.exit(app.exec_())#应用程序事件循环