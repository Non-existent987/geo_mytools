import sys,math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
class MyComboBox(QComboBox):
    def __init__(self):
        super(MyComboBox,self).__init__()
        self.setAcceptDrops(True)  #设置可以接受拖动
    def dragEnterEvent(self,e):
        print(e)
        if e.mimeData().hasText():
           e.accept()
        else:
            e.ignore()
    def dropEvent(self, e):
        self.addItem(e.mimeData().text())
class Dragdomo(QWidget):
    def __init__(self):
        super(Dragdomo,self).__init__()
        formlayout=QFormLayout()
        formlayout.addRow(QLabel("将左边的文本拖动到右边"))
        lineEdit=QLineEdit()
        lineEdit.setDragEnabled(True)   #设置可以被拖动

        combo=MyComboBox()
        formlayout.addRow(lineEdit,combo)
        self.setLayout(formlayout)
        self.setWindowTitle("拖动案例")

if __name__=="__main__":
    app=QApplication(sys.argv)
    p=Dragdomo()
    p.show()
    sys.exit(app.exec_())