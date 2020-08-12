# -*- coding: utf-8 -*-
from shapely.geometry import Polygon
import pandas as pd
import pot_style
import simplekml
import qdarkstyle
from geographiclib.geodesic import Geodesic
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget, QFileDialog,QColorDialog,QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

from kml_shetup import *
#___________插入窗体2_____________
from kml_shetup_2 import *
class Widget(QMainWindow, Ui_Form):
    k = '1-1'
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.setupUi(self)
        Widget.hang_v_z=self.hang_v.text()
        print(Widget.hang_v_z)
        Widget.lie_v_z=self.lie_v.text()
        print(Widget.lie_v_z)
        self.pushButton.clicked.connect(self.tt)
    def tt(self):
        hang_v_z=self.hang_v.text()
        print(hang_v_z)
        lie_v_z=self.lie_v.text()
        print(lie_v_z)
        MyMainWindow.k = str(hang_v_z) + '-' + str(lie_v_z)
        self.close()
#-^^^^^^^^^^^^^^窗体2^^^^^^^^^^^^^^^^

class MyMainWindow(QMainWindow, Ui_MainWindow):
    xiantiaoyanse = 'ffff0000'
    shanquyanse = 'ffff0000'
    data_table1 = pd.DataFrame()
    data_name = ''
    k = '1-1'
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.open.clicked.connect(self.openMsg)# 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        self.comboBox.currentIndexChanged.connect(self.my_comboBox)  # 当下拉索引发生改变时发射信号触发绑定的事件
        self.comboBox_2.currentIndexChanged.connect(self.my_comboBox)
        self.comboBox_3.currentIndexChanged.connect(self.my_comboBox)
        self.id_box.currentIndexChanged.connect(self.my_comboBox)
        
        self.xiantiao.clicked.connect(self.showDialog2)#点击弹出颜色窗体
        self.shanqu_2.clicked.connect(self.showDialog1)#点击弹出颜色窗体
        self.shengcheng.clicked.connect(self.strat_kml)#点击制作图层开始制作kml
        self.zuixiao.clicked.connect(self.on_pushButton_2_clicked)
        self.guanbi.clicked.connect(self.on_pushButton_clicked)
        # 两个按钮，选择一个关闭另一个
        self.radioButton_4.toggled.connect(lambda: self.btnstate1(self.radioButton_4))
        self.radioButton_3.toggled.connect(lambda: self.btnstate1(self.radioButton_3))
        self.shanqu.toggled.connect(lambda: self.btnstate(self.shanqu))
        self.pot.toggled.connect(lambda: self.btnstate(self.pot))
        # self.statusBar.showMessage('制作点方位角可以不选', 0)  # 状态栏本身显示的信息 第二个参数是信息停留的时间，单位是毫秒，默认是0（0表示在下一个操作来临前一直显示）
        self.setWindowFlags(Qt.FramelessWindowHint)#无边框模式
        self.setAttribute(Qt.WA_TranslucentBackground)
##
##    # 无边框模式
##    def mousePressEvent(self, event):
##        if event.button() == Qt.LeftButton:
##            self.m_drag = True
##            self.m_DragPosition = event.globalPos() - self.pos()
##            event.accept()
##            self.setCursor(QCursor(Qt.OpenHandCursor))
##
##
##    def mouseMoveEvent(self, QMouseEvent):
##        if Qt.LeftButton and self.m_drag:
##            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
##            QMouseEvent.accept()
##
##
##    def mouseReleaseEvent(self, QMouseEvent):
##        self.m_drag = False
##        self.setCursor(QCursor(Qt.ArrowCursor))

    #关闭最小化
    def on_pushButton_clicked(self):
        """
        关闭窗口
        """
        self.close()

    def on_pushButton_2_clicked(self):
        """
        最小化窗口
        """
        self.showMinimized()
    # 无边框模式^^^^^^^^^^^^^^^^^^^^

    def btnstate(self, btn):  # 两个按钮，选择一个关闭另一个
        if btn.text() == "创建扇区":
            if btn.isChecked() == True:
                print(btn.text() + " is selected")

        if btn.text() == "创建点":
            if btn.isChecked() == True:
                print(btn.text() + " is selected")
    def btnstate1(self, btn):  # 两个按钮，选择一个关闭另一个
        if btn.text() == "kml":
            if btn.isChecked() == True:
                print(btn.text() + " is selected")

        if btn.text() == "kmz":
            if btn.isChecked() == True:
                print(btn.text() + " is selected")

    def strat_kml(self):##################################################
        try:
            data_yuan=MyMainWindow.data_table1
            if self.shanqu.isChecked() == True and self.biaoji.isChecked() == True:
                lon_n = self.comboBox.currentText()  # 下拉菜单选择的项目赋值变量
                lat_n = self.comboBox_2.currentText()
                fw_n = self.comboBox_3.currentText()
                id_n = self.id_box.currentText()
                banjing_n = self.banjing.text()#获取单行输入框
                jia_jiao =self.lineEdit_3.text()#获取单行输入框
                shiye_n =self.lineEdit.text()#获取单行输入框
                xiangsu_n = self.lineEdit_2.text()#获取单行输入框
                gaodu_n = self.lineEdit_4.text()
                toumingdu=self.horizontalSlider.value()#滑动取值spinbox
                yanse_shanqu =MyMainWindow.shanquyanse
                yanse_xiantiao = MyMainWindow.xiantiaoyanse

                print(lon_n,lat_n,fw_n,id_n,jia_jiao,toumingdu,yanse_shanqu,yanse_xiantiao)
                print(1)
                data_yuan['gaodu'] = int(gaodu_n)
                print(2)
                data_yuan_shi=self.add_sectors(df=data_yuan,coords=[lon_n,lat_n,'gaodu',fw_n],has_z= True)
                # data_yuan_shi.to_csv('d:/up/shuchu.csv',index=False,encoding = 'gbk')
                ##========================================
                row_table = data_yuan_shi.copy()
                kml = simplekml.Kml()
                # colour = 'ff00ffff'  # ^^设置一个颜色
                colour_alpha_x = simplekml.Color.changealphaint(int(toumingdu), yanse_xiantiao)  # ^^^^^将颜色添加透明度0-255
                colour_alpha_m = simplekml.Color.changealphaint(int(toumingdu), yanse_shanqu)
                style = simplekml.Style()
                style.iconstyle.icon.href = None  # 不显示图标
                style.linestyle.color = colour_alpha_x  # 最终线条上色
                style.polystyle.color = colour_alpha_m  # 最终形状上色
                style.labelstyle.scale = 0.8  # 字体大小1是正常
                poif = kml.newfolder(name='名称')
                polf = kml.newfolder(name='扇区')
                lod1 = simplekml.Lod(minlodpixels=xiangsu_n, maxlodpixels=-1, minfadeextent=None, maxfadeextent=None)


                for i in range(len(row_table.index)):
                    row_1 = row_table.iloc[i, :]
                    df2 = row_1.filter(regex="[^geometry,^lon_n,^lat_n]")
                    id_n_v, polygon1, lon_yuan, lat_yuan, fw_yuan = row_1[[id_n, 'geometry', lon_n, lat_n, fw_n]]
                    lon_dd, lat_dd, lon1_dd, lat1_dd = self.lod_lon_lat(lon=lon_yuan, lat=lat_yuan,azimuth=45, azimuth1=225, radius=int(shiye_n))
                    latlonaltbox = simplekml.LatLonAltBox(east=lon_dd, north=lat_dd, south=lat1_dd, west=lon1_dd,
                                                          minaltitude=None, maxaltitude=None, altitudemode=None)

                    pol = polf.newpolygon(name=id_n_v)  # ,description = biaozhu_r
                    pol.region.latlonaltbox = latlonaltbox
                    pol.region.lod = lod1
                    # polygon2=ast.literal_eval(polygon1)
                    pol.outerboundaryis = polygon1   # polygon_1 是一个扇区

                    # lieming = row_1[['小区中文名','空口上下行业务字节数KByte']]#^^^^^^标注可选择，不选则全部
                    lie_ming = list(df2.index)
                    for i in lie_ming:  # ^^^^^^可选去掉不加标注
                        pol.extendeddata.schemadata.newsimpledata(i, df2[i])
                    pol.extrude = 1  # 高度需添加
                    pol.altitudemode = simplekml.AltitudeMode.relativetoground  # 高度需添加
                    # pol.snippet.maxlines = 1 #名字下面的间隔
                    # pol.snippet.content = "名字下面的文字"
                    lon_b, lat_b = self.point_lon_lat(lon=lon_yuan, lat=lat_yuan, azimuth=lat_yuan, radius=int(banjing_n) * 0.7)
                    pnt = poif.newpoint(name=id_n_v)
                    pnt.region.latlonaltbox = latlonaltbox
                    pnt.region.lod = lod1
                    pnt.coords = [(lon_b, lat_b)]
                    pnt.style = style
                    pol.style = style
                lu_name=MyMainWindow.data_name
                res_kml_name=lu_name.split(".")[0]
                if self.radioButton_4.isChecked() == True:
                    kml.save(res_kml_name+".kml")
                    print('ok1')
                    QMessageBox.about(self, "标题", "图层制作完成")
                else:
                    kml.save(res_kml_name+".kmz")
                    print('ok1')
                    QMessageBox.about(self, "标题", "图层制作完成")
            elif self.shanqu.isChecked() == True and self.biaoji.isChecked() == False:
                """无标注代码后面再加"""
                lon_n = self.comboBox.currentText()  # 下拉菜单选择的项目赋值变量
                lat_n = self.comboBox_2.currentText()
                fw_n = self.comboBox_3.currentText()
                id_n = self.id_box.currentText()
                banjing_n = self.banjing.text()#获取单行输入框
                jia_jiao =self.lineEdit_3.text()#获取单行输入框
                shiye_n =self.lineEdit.text()#获取单行输入框
                xiangsu_n = self.lineEdit_2.text()#获取单行输入框
                gaodu_n = self.lineEdit_4.text()
                toumingdu=self.horizontalSlider.value()#滑动取值spinbox
                yanse_shanqu =MyMainWindow.shanquyanse
                yanse_xiantiao = MyMainWindow.xiantiaoyanse

                print(lon_n,lat_n,fw_n,id_n,jia_jiao,toumingdu,yanse_shanqu,yanse_xiantiao)
                print(1)
                data_yuan['gaodu'] = int(gaodu_n)
                print(2)
                data_yuan_shi=self.add_sectors(df=data_yuan,coords=[lon_n,lat_n,'gaodu',fw_n],has_z= True)
                # data_yuan_shi.to_csv('d:/up/shuchu.csv',index=False,encoding = 'gbk')
                ##========================================
                row_table = data_yuan_shi.copy()
                kml = simplekml.Kml()
                # colour = 'ff00ffff'  # ^^设置一个颜色
                colour_alpha_x = simplekml.Color.changealphaint(int(toumingdu), yanse_xiantiao)  # ^^^^^将颜色添加透明度0-255
                colour_alpha_m = simplekml.Color.changealphaint(int(toumingdu), yanse_shanqu)
                style = simplekml.Style()
                style.iconstyle.icon.href = None  # 不显示图标
                style.linestyle.color = colour_alpha_x  # 最终线条上色
                style.polystyle.color = colour_alpha_m  # 最终形状上色
                style.labelstyle.scale = 0.8  # 字体大小1是正常
                poif = kml.newfolder(name='名称')
                polf = kml.newfolder(name='扇区')
                lod1 = simplekml.Lod(minlodpixels=xiangsu_n, maxlodpixels=-1, minfadeextent=None, maxfadeextent=None)


                for i in range(len(row_table.index)):
                    row_1 = row_table.iloc[i, :]
                    df2 = row_1.filter(regex="[^geometry,^lon_n,^lat_n]")
                    id_n_v, polygon1, lon_yuan, lat_yuan, fw_yuan = row_1[[id_n, 'geometry', lon_n, lat_n, fw_n]]
                    lon_dd, lat_dd, lon1_dd, lat1_dd = self.lod_lon_lat(lon=lon_yuan, lat=lat_yuan,azimuth=45, azimuth1=225, radius=int(shiye_n))
                    latlonaltbox = simplekml.LatLonAltBox(east=lon_dd, north=lat_dd, south=lat1_dd, west=lon1_dd,
                                                          minaltitude=None, maxaltitude=None, altitudemode=None)

                    pol = polf.newpolygon(name=id_n_v)  # ,description = biaozhu_r
                    pol.region.latlonaltbox = latlonaltbox
                    pol.region.lod = lod1
                    # polygon2=ast.literal_eval(polygon1)
                    pol.outerboundaryis = polygon1   # polygon_1 是一个扇区

                    # lieming = row_1[['小区中文名','空口上下行业务字节数KByte']]#^^^^^^标注可选择，不选则全部
                    # lie_ming = list(df2.index)
                    # for i in lie_ming:  # ^^^^^^可选去掉不加标注
                    #     pol.extendeddata.schemadata.newsimpledata(i, df2[i])
                    pol.extrude = 1  # 高度需添加
                    pol.altitudemode = simplekml.AltitudeMode.relativetoground  # 高度需添加
                    # pol.snippet.maxlines = 1 #名字下面的间隔
                    # pol.snippet.content = "名字下面的文字"
                    lon_b, lat_b = self.point_lon_lat(lon=lon_yuan, lat=lat_yuan, azimuth=lat_yuan, radius=int(banjing_n) * 0.7)
                    pnt = poif.newpoint(name=id_n_v)
                    pnt.region.latlonaltbox = latlonaltbox
                    pnt.region.lod = lod1
                    pnt.coords = [(lon_b, lat_b)]
                    pnt.style = style
                    pol.style = style
                lu_name=MyMainWindow.data_name
                res_kml_name=lu_name.split(".")[0]
                if self.radioButton_4.isChecked() == True:
                    kml.save(res_kml_name+".kml")
                    print('ok1')
                    QMessageBox.about(self, "标题", "图层制作完成")

                else:
                    kml.save(res_kml_name+".kmz")
                    print('ok1')
                    QMessageBox.about(self, "标题", "图层制作完成")
            elif self.pot.isChecked() == True:#制作点''''''
                kml = simplekml.Kml()
                row_table = MyMainWindow.data_table1.copy()
                lon_n = self.comboBox.currentText()  # 下拉菜单选择的项目赋值变量
                lat_n = self.comboBox_2.currentText()
                id_n = self.id_box.currentText()
                shiye_n =self.lineEdit.text()#获取单行输入框
                xiangsu_n = self.lineEdit_2.text()#获取单行输入框
                style = simplekml.Style()
                pot_ss = MyMainWindow.k
                zz=pot_style.dict[pot_ss]
                style.iconstyle.icon.href = zz
                print(pot_ss,zz)
                lod_p = simplekml.Lod(minlodpixels=xiangsu_n, maxlodpixels=-1, minfadeextent=None, maxfadeextent=None)
                for i in range(len(row_table.index)):
                    row_v = row_table.iloc[i, :]
                    mingcheng, lon_p, lat_p = row_v[[id_n, lon_n, lat_n]]  # +++++++++++++++++++++++名称和经纬度必须
                    # -----------添加lod
                    lon_dd, lat_dd, lon1_dd, lat1_dd = self.lod_lon_lat(lon=lon_p, lat=lat_p, azimuth=45,
                                                                        azimuth1=225, radius=int(shiye_n))
                    latlonaltbox_p = simplekml.LatLonAltBox(east=lon_dd, north=lat_dd, south=lat1_dd, west=lon1_dd,
                                                          minaltitude=None, maxaltitude=None, altitudemode=None)
                    rgn_p = simplekml.Region(latlonaltbox_p, lod_p)
                    # ------------创建点
                    pnt = kml.newpoint(name=mingcheng, region=rgn_p)  #
                    pnt.coords = [(lon_p, lat_p)]
                    pnt.style = style
                    # lie_ming = list(row_v.index)  # 标注全部列
                    # for i in lie_ming:
                    #     pnt.extendeddata.schemadata.newsimpledata(i, row_v[i])
                lu_name=MyMainWindow.data_name
                res_kml_name=lu_name.split(".")[0]
                if self.radioButton_4.isChecked() == True:
                    kml.save(res_kml_name+"_pot.kml")
                    print('ok1')
                    QMessageBox.about(self, "标题", "图层制作完成")
                else:
                    kml.save(res_kml_name+"_pot.kmz")
                    print('ok1')
                    QMessageBox.about(self, "标题", "图层制作完成")
        except:
            QMessageBox.warning(self, "标题", "请核对经纬度方位角不为空，或者特殊字符")

    # ---------找Polygon中标注名称位置的函数
    def point_lon_lat(self,lon=114.198312, lat=30.630697, azimuth=0, radius=50):
        res = Geodesic.WGS84.Direct(lat, lon, azimuth, radius)
        lon = res['lon2']
        lat = res['lat2']
        return lon, lat
    def showDialog1(self):#颜色按钮的窗体
        col = QColorDialog.getColor()
        if col.isValid():
            self.shanqu_2.setStyleSheet('QWidget QPushButton{background-color:%s}' % col.name())
        rgb1=col.getRgb()
        gg=simplekml.Color.rgb(rgb1[0],rgb1[1],rgb1[2],rgb1[3])
        MyMainWindow.shanquyanse = gg
        print('之前：', col.name(), '之后：', gg)


    def showDialog2(self):  # 颜色窗体
        col = QColorDialog.getColor()
        if col.isValid():
            self.xiantiao.setStyleSheet('QWidget QPushButton{background-color:%s}' % col.name())
        rgb1=col.getRgb()
        gg=simplekml.Color.rgb(rgb1[0],rgb1[1],rgb1[2],rgb1[3])

        MyMainWindow.xiantiaoyanse = gg
        print('之前：',col.name(),'之后：',gg)

    def msg5(self):
        QMessageBox.about(self, "标题", "图层制作完成")




    def openMsg(self):
        try:
            file, ok = QFileDialog.getOpenFileName(self, "打开", "C:/", "CSV files (*.txt , *.csv);;Excel files(*.xlsx , *.xls)")
            MyMainWindow.data_name=file
            if file:
                print(0)
                self.comboBox.clear()
                self.comboBox_2.clear()
                self.comboBox_3.clear()
                self.id_box.clear()

                # self.statusBar.showMessage(file)# 在状态栏显示文件地址
                try:
                    try:
                        MyMainWindow.data_table1 = pd.read_csv(open(file,encoding='gbk'))  # pandas
                        QMessageBox.about(self, "标题", "选择数据成功")
                    except:
                        MyMainWindow.data_table1 = pd.read_csv(open(file))  # pandas
                        QMessageBox.about(self, "标题", "选择数据成功")
                except:
                    try:
                        MyMainWindow.data_table1 = pd.read_excel(open(file))
                        QMessageBox.about(self, "标题", "选择数据成功")
                    except:
                        try:
                            MyMainWindow.data_table1 = pd.read_excel(file,encoding = 'gbk')
                            QMessageBox.about(self, "标题", "选择数据成功")
                        except:
                            MyMainWindow.data_table1 = pd.read_excel(file)
                            QMessageBox.about(self, "标题", "选择数据成功")
                self.mulu.setText(file)  # 在文本框中显示文件地址
                lie = MyMainWindow.data_table1.columns.values  # pandas
                self.comboBox.addItems(lie)  # 增加下拉菜单从列表中
                self.comboBox_2.addItems(lie)  # 增加下拉菜单从列表中
                self.comboBox_3.addItems(lie)  # 增加下拉菜单从列表中
                self.id_box.addItems(lie)  # 增加下拉菜单从列表中

        except:
            QMessageBox.warning(self, "标题", "选择数据有误")


    def my_comboBox(self):
        # 标签用来显示选中的文本
        lon_n = self.comboBox.currentText()#下拉菜单选择的项目赋值变量
        lat_n = self.comboBox_2.currentText()
        fw_n = self.comboBox_3.currentText()
        id_n = self.id_box.currentText()
        print(id_n,lon_n,lat_n,fw_n)
        return id_n,lon_n,lat_n,fw_n

    # ---------找lod的四个角
    def lod_lon_lat(self,lon=114.198312, lat=30.630697, azimuth=45, azimuth1=225, radius=7000):  # ^^^^^^^设置视野
        res = Geodesic.WGS84.Direct(lat, lon, azimuth, radius)
        lon_1 = res['lon2']
        lat_1 = res['lat2']
        res1 = Geodesic.WGS84.Direct(lat, lon, azimuth1, radius)
        lon_2 = res1['lon2']
        lat_2 = res1['lat2']
        return lon_1, lat_1, lon_2, lat_2

    def __draw_sector(self,
                      lon=114.198312,
                      lat=30.630697,
                      height=5,
                      azimuth=0,
                      has_z=True,
                      shape_dict={
                          'radius': 100,
                          'beam': 30,
                          'per_degree': 10
                      },
                      **kwargs):
        """制作扇区形状，可以2d也可以3d  has_z就是3d

        """
        radius, beam, per_degree = (shape_dict['radius'], shape_dict['beam'],
                                    shape_dict['per_degree'])
        azimuth_list = list(
            range(
                int(azimuth - beam / 2),
                int(azimuth + beam / 2) + 1, per_degree))

        if has_z:
            points = [(lon, lat, height)]
            for azi in azimuth_list:
                res = Geodesic.WGS84.Direct(lat, lon, azi, radius)
                points.append((res['lon2'], res['lat2'], height))
        else:
            points = [(lon, lat)]
            for azi in azimuth_list:
                res = Geodesic.WGS84.Direct(lat, lon, azi, radius)
                points.append((res['lon2'], res['lat2']))
        points.append(points[0])
        return list(points)

    def add_sectors(self,
                    df,
                    coords=['', '', '', ''],
                    has_z=True,
                    sec_col='geometry',
                    shape_dict={
                        'radius': 100,
                        'beam': 30,
                        'per_degree': 10
                    },
                    **kwargs):
        """根据经纬度挂高方向角所在列，为df增加CRS和 geometry 列
        shape_dict={
                          'radius': 100,
                          'beam': 30,
                          'per_degree': 10
                      },
        Returns:
            [type] -- [description]
        """
        if coords == ['', '', '', '']:
            coords = [self.lon, self.lat, self.height, self.azimuth]
        lon, lat, *oth = coords
        df = df.copy()
        height = oth[0]
        azimuth = oth[1]
        if has_z:
            df.loc[:, sec_col] = [
                self.__draw_sector(*x, shape_dict=shape_dict, has_z=has_z)
                for x in zip(df[lon], df[lat], df[height], df[azimuth])
            ]
        else:
            df.loc[:, sec_col] = [
                self.__draw_sector(*x, shape_dict=shape_dict, has_z=has_z)
                for x in zip(df[lon], df[lat], df[azimuth])
            ]
        return df

if __name__ == "__main__":
    app = QApplication(sys.argv)#声明变量
    myWin = MyMainWindow()#创建窗口
    myWin1 = Widget()#创建窗口2
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())#批量修改样式

    btn = myWin.dianyangshi# 通过toolButton将两个窗体关联
    btn.clicked.connect(myWin1.show)# 通过toolButton将两个窗体关联

    myWin.show()#todo 正常比例显示
    # myWin.setStyleSheet("#MainWindow{background-color: #9FB6CD}")
    # myWin.showMaximized()#todo 调用最大化显示窗口
    # styleFile = './style.qss'#添加背景图片用
    # qssStyle = CommonHelper.readQss(styleFile)#添加背景图片用
    # myWin.setStyleSheet(qssStyle)#添加背景图片用
    sys.exit(app.exec_())#应用程序事件循环

