"""
这个例子中我们实现了两个功能：菜单按钮、带倒计时的按钮（账户注册的时候经常会碰到）。
"""
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMenu
from PyQt5.QtCore import QTimer
import sys

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.resize(400,300)
        self.setWindowTitle('早点毕业吧--按钮（QPushButton）')

        bt1 = QPushButton("这是什么",self)
        bt1.move(50,50)

        self.bt2 = QPushButton('发送验证码',self)
        self.bt2.move(200,50)
        """
设置菜单按钮其实很简单，首先我们新建一个QMenu对象。这里的addSeparator()，其实就是给菜单增加一个分隔符。
        """
        menu = QMenu(self)
        menu.addAction('我是')
        menu.addSeparator()
        menu.addAction('世界上')
        menu.addSeparator()
        menu.addAction('最帅的')

        bt1.setMenu(menu)#然后将这个菜单添加到QPushButton对象中
        """
第二个例子，我们使用到QTimer这个类，我们前面很多次都用到了这个和时间相关的类。后面会专门的讲解的。
QTimer类提供重复性和单次定时器。QTimer类为定时器提供高级编程接口。要使用它，请创建一个QTimer，将其timeout()信号连接到相应的插槽，然后调用start()。从此以后，它将以固定的时间间隔发出timeout()信号。
setInterval()该属性拥有以毫秒为单位的超时时间间隔。此属性的默认值为0。 
        """

        self.count = 10
        self.bt2.clicked.connect(self.Action)
        self.time = QTimer(self)
        self.time.setInterval(1000)
        self.time.timeout.connect(self.Refresh)

        self.show()
        """
我们单击按钮后，进行判断若按钮没有被禁用，则激活定时器，同时将按钮禁用，即禁止点击。
        """
    def Action(self):
        if self.bt2.isEnabled():
            self.time.start()
            self.bt2.setEnabled(False)
        """
进入超时状态后，我们开始倒计时。同时让按钮上的文字不断的在变化。
当倒计时完成的时候，我们停止定时器。将按钮恢复成正常的状态。同时重置倒计时的值，为下次的使用做好准备。 
        """
    def Refresh(self):
        if self.count > 0:
            self.bt2.setText(str(self.count)+'秒后重发')
            self.count -= 1
        else:
            self.time.stop()
            self.bt2.setEnabled(True)
            self.bt2.setText('发送验证码')
            self.count = 10

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())