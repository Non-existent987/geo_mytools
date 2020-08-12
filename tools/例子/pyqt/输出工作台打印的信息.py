# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
from PyQt5.Qt import QListWidget, QAbstractItemView, QListWidgetItem, QThread,\
    pyqtSignal, QDir
from PyQt5.QtCore import Qt
import time
import traceback
import subprocess
import datetime

st=subprocess.STARTUPINFO
st.dwFlags=subprocess.STARTF_USESHOWWINDOW
st.wShowWindow=subprocess.SW_HIDE

class Logger(object):
    
    def _now(self):
        return str(datetime.datetime.now()).split(".")[0]

    def debug(self,message):
        print(self._now()+"-[DEBUG]-"+message)
 
    def info(self,message):
        print(self._now()+"-[INFO]-"+message)
Logger=Logger() 
class Ui_MainWindow(QtWidgets.QMainWindow):
    pressRun=pyqtSignal(str)
    pressStop=pyqtSignal(str)
    def __init__(self):
        super(Ui_MainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1131, 667)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 341, 611))
        self.groupBox.setObjectName("groupBox")
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox)
        self.scrollArea.setGeometry(QtCore.QRect(10, 60, 321, 541))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 319, 539))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(10, 19, 180, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.toolButton = QtWidgets.QToolButton(self.groupBox)
        self.toolButton.setGeometry(QtCore.QRect(200, 20, 41, 31))
        self.toolButton.setObjectName("toolButton")
        self.loadButton = QtWidgets.QPushButton(self.groupBox)
        self.loadButton.setGeometry(QtCore.QRect(245, 20, 41, 31))
        self.loadButton.setObjectName("loadButton")
        self.clearButton = QtWidgets.QPushButton(self.groupBox)
        self.clearButton.setGeometry(QtCore.QRect(290, 20, 41, 31))
        self.clearButton.setObjectName("loadButton")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(360, 10, 371, 271))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(10, 30, 51, 20))
        self.label.setObjectName("label")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(70, 30, 111, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 54, 20))
        self.label_2.setObjectName("label_2_1")
        self.label_2_1 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2_1.setGeometry(QtCore.QRect(200, 70, 50, 21))
        self.label_2_1.setObjectName("label_2_1")
        self.lineEdit_3_1 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_3_1.setGeometry(QtCore.QRect(240, 70, 100, 21))
        self.lineEdit_3_1.setObjectName("lineEdit_3_1")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_3.setGeometry(QtCore.QRect(70, 70, 113, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 91, 21))
        self.label_3.setObjectName("label_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(100, 110, 141, 21))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(10, 150, 81, 21))
        self.label_4.setObjectName("label_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_5.setGeometry(QtCore.QRect(100, 150, 141, 21))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(10, 190, 61, 20))
        self.label_5.setObjectName("label_5")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox.setGeometry(QtCore.QRect(70, 190, 71, 21))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_2.setGeometry(QtCore.QRect(150, 190, 101, 21))
        self.checkBox_2.setObjectName("checkBox_2")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(10, 230, 81, 21))
        self.label_6.setObjectName("label_6")
        self.spinBox = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox.setGeometry(QtCore.QRect(100, 230, 42, 22))
        self.spinBox.setMinimum(1)
        self.spinBox.setProperty("value", 1)
        self.spinBox.setObjectName("spinBox")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(360, 290, 751, 331))
        self.groupBox_3.setObjectName("groupBox_3")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.groupBox_3)
        self.scrollArea_2.setGeometry(QtCore.QRect(10, 20, 731, 301))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 729, 299))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.textEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents_2)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 731, 301))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(True)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(740, 10, 371, 271))
        self.groupBox_4.setObjectName("groupBox_4")
        self.runButton = QtWidgets.QPushButton(self.groupBox_4)
        self.runButton.setGeometry(QtCore.QRect(150, 180, 75, 23))
        self.runButton.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.runButton.setObjectName("runButton")
        self.stopButton = QtWidgets.QPushButton(self.groupBox_4)
        self.stopButton.setGeometry(QtCore.QRect(250, 180, 75, 23))
        self.stopButton.setObjectName("stopButton")
        self.label_7 = QtWidgets.QLabel(self.groupBox_4)
        self.label_7.setGeometry(QtCore.QRect(20, 40, 54, 21))
        self.label_7.setObjectName("label_7")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton.setGeometry(QtCore.QRect(80, 40, 89, 21))
        self.radioButton.setObjectName("radioButton")
        self.label_8 = QtWidgets.QLabel(self.groupBox_4)
        self.label_8.setGeometry(QtCore.QRect(20, 80, 54, 21))
        self.label_8.setObjectName("label_8")
        self.spinBox_2 = QtWidgets.QSpinBox(self.groupBox_4)
        self.spinBox_2.setGeometry(QtCore.QRect(80, 80, 71, 22))
        self.spinBox_2.setObjectName("spinBox_2")
        self.label_9 = QtWidgets.QLabel(self.groupBox_4)
        self.label_9.setGeometry(QtCore.QRect(20, 120, 54, 21))
        self.label_9.setObjectName("label_9")
        self.spinBox_3 = QtWidgets.QSpinBox(self.groupBox_4)
        self.spinBox_3.setGeometry(QtCore.QRect(80, 120, 71, 22))
        self.spinBox_3.setObjectName("spinBox_3")
        self.spinBox_3.setProperty("value", 1)
        self.spinBox_3.setMinimum(1)
#         self.progressBar = QtWidgets.QProgressBar(self.groupBox_4)
#         self.progressBar.setGeometry(QtCore.QRect(20, 220, 341, 16))
#         self.progressBar.setAutoFillBackground(True)
#         self.progressBar.setProperty("value", 24)
#         self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1131, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
#         self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 321, 541))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
#==========================================================================# 
        self.runButton.setStyleSheet('''font: 75 11pt Arial;background-color: green''')
        self.stopButton.setStyleSheet('''font: 75 11pt Arial;background-color: red''')  
        sys.stdout = EmittingStream(textWritten=self.outputWritten)  
        sys.stderr = EmittingStream(textWritten=self.outputWritten)       
        self.toolButton.clicked.connect(self.setBrowerPath)
        self.loadButton.clicked.connect(self.loadTestCases)
        self.clearButton.clicked.connect(self.clearTestCases)
        self.runButton.clicked.connect(self.runThread)
#         self.runButton.clicked.connect(lambda:self.callRun("yellow"))
        self.pressRun.connect(self.runButtonColor)
        self.stopButton.clicked.connect(self.editConfigFile)
        self.stopButton.clicked.connect(self.stopRun)
#         self.stopButton.clicked.connect(lambda:self.callRun("green"))
        self.pressStop.connect(self.runButtonColor)

    def runButtonColor(self, color):
        self.runButton.setStyleSheet("font: 75 11pt Arial;background-color: "+color)
     
    def callRun(self,text):
        self.pressRun.emit(text)   
            
    def setBrowerPath(self): 
        download_path = QtWidgets.QFileDialog.getExistingDirectory(self,  
                                    "浏览",  
                                    QDir.currentPath())   
        self.lineEdit.setText(download_path)  
    
    def _case_path(self):
        return self.lineEdit.text()
    
    def _root_path(self):
        _root_path=self.lineEdit.text().split("test")[0]
        return _root_path
        
    def loadTestCases(self):
        script_path=self._case_path()
#         script_path=r"E:\workspace\GN_AutoTest\test\currentTest"
        if script_path:
            cases_lst=[]
            for root,dirs,files in os.walk(os.path.abspath(script_path)):
                for file in files:
                    file_name=file.split(".")
                    if "py" in file_name:
                        case_name=file_name[0]
                        if case_name !="__init__":  
                            cases_lst.append(case_name)
        
            self.myListWidget=SetItemList(self)
            for case in cases_lst:
                QListWidgetItem(str(case),self.myListWidget)
            for item in self.myListWidget.iterAllItems():
                item.setFlags(item.flags()|Qt.ItemIsUserCheckable)#设置listwidget的条目可选
                item.setCheckState(Qt.Checked)#赋初值，所有条目都选中
                
            self.verticalLayout.addWidget(self.myListWidget)
            self.myListWidget.setAcceptDrops(False)
            self.myListWidget.viewport().update()#默认视口矩形和设备矩形一样
    
    def clearTestCases(self):
        for i in reversed(range(self.verticalLayout.count())): 
            self.verticalLayout.itemAt(i).widget().deleteLater()
     
    def getTestCase(self):
        with open(self._root_path()+"test.txt","w") as t:
            for i in range(self.myListWidget.count()):
                checkbox_case=self.myListWidget.item(i)
                if checkbox_case.checkState()==2:
                    t.write(self._case_path().split("/test/")[1]+"/"+checkbox_case.text()+".py\n")
#             for i in range(self.verticalLayout.count()) :
#                 print(self.verticalLayout.item(1))
#             print(self.verticalLayout.count())
            
    def outputWritten(self, text):  
        cursor = self.textEdit.textCursor()  
        cursor.movePosition(QtGui.QTextCursor.End)  
        cursor.insertText(text)  
        self.textEdit.setTextCursor(cursor)  
        self.textEdit.ensureCursorVisible()   
        
    def pro_name(self):
        return self.lineEdit_2.text()
    
    def sw_version(self):
        return self.lineEdit_3.text()
    
    def sw_tat(self):
        return self.lineEdit_3_1.text()
    
    def dut_sn(self):
        return self.lineEdit_4.text()
    
    def subdut_sn(self):
        return self.lineEdit_5.text()
    
    def _DCPower(self):
        if self.checkBox.isChecked() and self.checkBox_2.isChecked():
            self.messageBox("警告", "请选择一个电源设备")
            return "None"
        elif self.checkBox.isChecked():
            return self.checkBox.text()
        elif self.checkBox_2.isChecked():
            return self.checkBox_2.text()
        else:
            return "None"
        
    def _usb_port(self):
        return self.spinBox.value()
    
    def is_OTA(self):
        return  self.radioButton.isChecked()
    
    def delay_time(self):
        return self.spinBox_2.value()
    
    def _loop(self):
        return self.spinBox_3.value()
    
    
    def editConfigFile(self):
        config_path=self._root_path()+"project.json"
        try:
            with open(config_path,"r") as j:
                Data=json.load(j)
                _dut_sn=Data["device"]["DUT"]["sn"]
                _subdut_sn=Data["device"]["SUBDUT1"]["sn"]
                _equipment_dc=Data["equipment"]["dc_power"]
#                 print(_equipment_dc)
                _equipment_usb=Data["equipment"]["usb"]
            with open(config_path, "r") as f:
                s=f.read()
                s=s.replace("\"DUT\":{\"sn\":\""+_dut_sn+"\"","\"DUT\":{\"sn\":\""+self.dut_sn()+"\"")
                s=s.replace("\"SUBDUT1\":{\"sn\":\""+_subdut_sn+"\"","\"SUBDUT1\":{\"sn\":\""+self.subdut_sn()+"\"")
                s=s.replace("\"dc_power\":\""+_equipment_dc+"\"","\"dc_power\":\""+self._DCPower()+"\"")
                s=s.replace("\"usb\":\""+_equipment_usb+"\"","\"usb\":\""+str(self._usb_port())+"\"")
            with open(config_path,"w+") as d:
                d.write(s)
        except Exception as e:
            traceback.print_exc()
            self.messageBox("警告", "请检查配置文件！！！")
    
    def runThread(self):
        self.editConfigFile()
        try:
            self.getTestCase()
            case_path=self.lineEdit.text()
#             _case_path=self.lineEdit.text().split("/")
#             for i,v in enumerate(_case_path):
#                 if v == 'test':
#                     case_path=_case_path[i:len(_case_path)]
            self.Runer=Runer(case_path=case_path, loop=self._loop(), delay=self.delay_time())
            self.Runer.start()
            self.callRun("yellow")
        except Exception as e:
            self.messageBox("警告", "请先加载测试用例！！")
    
    def stopRun(self):
        try:
            self.Runer.terminate() 
            sys.stdout = EmittingStream(textWritten=self.outputWritten)  
            sys.stderr = EmittingStream(textWritten=self.outputWritten)  
            Logger.info("测试终止") 
            self.callRun("green")
        except Exception as e:
            self.messageBox("警告", "请先启动测试")  
        
    def messageBox(self, mLevel, mContent):
        msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, mLevel, mContent)
        msg_box.exec_()
    
    def outputToFile(self):
        content=self.textEdit.toPlainText()
        with open(self._root_path()+"console_log.txt", "a") as f:
            f.write("========================="+time.strftime("%Y-%m-%d_%H-%M-%S")+"=========================\n")
            f.write(content)
        
    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '警告', '退出后测试将停止,\n你确认要退出吗？',
                                           QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.outputToFile() #关闭程序时自动保存控制台log
            event.accept()
        else:
            event.ignore()
            
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "金兔GTool v_0.0.1"))
        self.groupBox.setTitle(_translate("MainWindow", "测试用例"))
        self.toolButton.setText(_translate("MainWindow", "浏览"))
        self.loadButton.setText(_translate("MainWindow", "加载"))
        self.clearButton.setText(_translate("MainWindow", "清空"))
        self.groupBox_2.setTitle(_translate("MainWindow", "配置"))
        self.label.setText(_translate("MainWindow", "项目代号"))
        self.lineEdit_2.setText(_translate("MainWindow", "例如：BJ17G06A"))
        self.label_2.setText(_translate("MainWindow", "软件版本"))
        self.lineEdit_3.setText(_translate("MainWindow", "None"))
        self.label_2_1.setText(_translate("MainWindow", "标签"))
        self.lineEdit_3_1.setText(_translate("MainWindow", "例如：SignUser"))
        self.label_3.setText(_translate("MainWindow", "主测机ID(sn)"))
        self.label_4.setText(_translate("MainWindow", "辅测机ID(sn)"))
        self.lineEdit_4.setText(_translate("MainWindow", "None"))
        self.lineEdit_5.setText(_translate("MainWindow", "None"))
        self.label_5.setText(_translate("MainWindow", "电源设备"))
        self.checkBox.setText(_translate("MainWindow", "Agilent"))
        self.checkBox_2.setText(_translate("MainWindow", "PowerMonitor"))
        self.label_6.setText(_translate("MainWindow", "USB通断器端口"))
        self.groupBox_3.setTitle(_translate("MainWindow", "控制台"))
        self.groupBox_4.setTitle(_translate("MainWindow", "执行"))
        self.runButton.setText(_translate("MainWindow", "Start"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))
        self.label_7.setText(_translate("MainWindow", "OTA升级"))
        self.radioButton.setText(_translate("MainWindow", "YES/NO"))
        self.label_8.setText(_translate("MainWindow", "延时执行"))
        self.label_9.setText(_translate("MainWindow", "测试Loop"))
        
class SetItemList(QListWidget):
    def __init__(self,types ,parent=None):
        super(SetItemList,self).__init__(parent)
#         self.insertItem(0,"")
#         self.setIconSize(QSize(124,124))#设置icon的大小
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)#说选择模式有:ExtendedSelection 按住ctrl多选,SingleSelection 单选 MultiSelection 点击多选 ContiguousSelection鼠标拖拉多选
        self.setAcceptDrops(True)#setAcceptDrops(bool)
        self.setSelectionRectVisible(True)
        
    def keyPressEvent(self,e):
        if e.key()==Qt.Key_Space:
            if self.selectedItems():
                new_state=Qt.Unchecked if self.selectedItems()[0].checkState() else Qt.Checked
                for item in self.selectedItems():
                    if item.flags()&Qt.ItemIsUserCheckable:
                        item.setCheckState(new_state)
            self.viewport().update()
        elif e.key()==Qt.Key_Delete:
            for item in self.selectedItems():
                self.takeItem(self.row(item))

    def iterAllItems(self):
        for i in range(self.count()):
            yield  self.item(i)

class EmittingStream(QtCore.QObject):  
        textWritten = QtCore.pyqtSignal(str)  
        def write(self, text):
            self.textWritten.emit(str(text))  

import json
import unittest
# import HTMLTestRunner
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
class Runer(QThread):  
    def __init__(self, case_path, loop ,delay):
        QThread.__init__(self)
        self.case_path=case_path.split("/test/")
        self.rootPath = self.case_path[0]
        self.record = time.strftime("%Y-%m-%d_%H-%M-%S")
        self.spath = self.rootPath+"/report/"+"test_"+self.record
        self.jsonFile="project.json"
        self.loop=loop
        self.delay=delay
    def getModuleList(self):
        moduleList=[]
        with open(self.rootPath+"/test.txt") as f:
            for line in f.readlines():
                line=line.split()[0]
                line=line.split(".")[0]
                if line[0] !="#" and len(line) != 0:
                    moduleList.append(line)
        Logger.info("plan to excute :"+str(len(moduleList))+" test cases")
        return moduleList 
      
    def testSuit(self):
        suite = unittest.TestSuite()
        for m in self.getModuleList():
            m=m.replace("/",".").replace("\\",".")
            testModule = __import__(".".join(["test",m]),{},{},["test"])
            for test in testModule.TestScript.__dict__.keys():
                if "test" in test:
                    suite.addTest(testModule.TestScript(test))
        return suite 
     
    def changeConfig(self,A, B):
        f= open(self.rootPath+"\\"+self.jsonFile,"r")
        s=f.read()
        s=s.replace(A, B)
        f.close()
        p=open(self.rootPath+"\\"+self.jsonFile,"w+")
        p.write(s)
        p.close()
    #     print s
     
    def sendEmail(self,newfile):
        jsonFile="project.json"
        with open(self.rootPath+"\\"+jsonFile,"r") as f:
            DATA = json.load(f) 
        if DATA["send_email"]["send"]=="yes":
            #打开文件
            f=open(newfile,'rb')
            #读取文件内容
            mail_body=f.read()
        #     print mail_body
            f.close()
            #发送邮箱服务器
            smtpserver = DATA["send_email"]["smtpserver"]
            #发送邮箱用户名/密码
            user=DATA["send_email"]["user"]
            password=DATA["send_email"]["password"]
            #发送邮箱
            sender=DATA["send_email"]["sender"]
            #多个接收邮箱
            receiver=DATA["send_email"]["receiver"]
            #发送邮件主题
            subject = '【自动化功耗测试】G1602A T0096版本功耗测试报告（自动发送）'
            msg=MIMEMultipart('mixed')          
        #    msg_plain = MIMEText(text,'plain', 'utf-8')    
        #    msg.attach(msg_plain)         
            msg_html1 = MIMEText(mail_body,'html','utf-8')
            msg.attach(msg_html1)
            msg_html = MIMEText(mail_body,'html','utf-8')
            msg_html["Content-Disposition"] = 'attachment; filename="TestReport.html"'
            msg.attach(msg_html)    
            msg['From'] = 'yanglk@gionee.com <yanglk@gionee.com>'
            msg['To'] = ";".join(receiver)
            msg['Subject']=Header(subject,'utf-8')     
            #连接发送邮件
            smtp=smtplib.SMTP()
            smtp.connect(smtpserver,25)
            smtp.login(user, password)
            smtp.sendmail(sender, receiver, msg.as_string())
            smtp.quit()
        else:
            pass  
    
    def runTest(self):
        if self.delay != 0:
            Logger.info("延时"+str(self.delay)+"秒后测试开始...")
            time.sleep(self.delay)
        for i in range(self.loop):
            Logger.info("正在执行第"+str(i+1)+"轮测试")
#             self.changeConfig("\"screencap\":\"no\"", "\"screencap\":\"yes\"")
#             with open(self.rootPath+"\\project.log", 'w+') as f: 
#                 f.write(self.spath)
#             os.makedirs(self.spath)
#             Logger.info("Report saved to :"+self.spath)
#             filename = self.spath+"/Test_Report.html"
#             fp = open(filename,'wb')
            Logger.info("测试开始")
            os.system("Python "+self.rootPath+"/run.py")
#             runner = unittest.TextTestRunner()
#             runner.run(self.testSuit())
#             runner=HTMLTestRunner.HTMLTestRunner(stream=fp,title="AutoTestReport",description='Power Consumption')
#             runner.run(self.testSuit())
#             fp.close()
#             self.changeConfig("\"screencap\":\"yes\"", "\"screencap\":\"no\"")
            Logger.info("测试完成")
#             return filename
            
    def run(self):
        try:
            self.runTest()
        except Exception as e:
            traceback.print_exc()
                    
if __name__ == "__main__":   
    app = QtWidgets.QApplication(sys.argv)
    main = Ui_MainWindow()
    main.show()
    sys.exit(app.exec_())