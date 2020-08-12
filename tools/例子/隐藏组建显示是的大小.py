import sys
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl,Qt
from PyQt5.QtWidgets import QWidget, QLabel, QApplication,QMainWindow,QVBoxLayout,QHBoxLayout,QLineEdit,QPushButton,QLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        topLayout = QHBoxLayout()
        label = QLabel("号码")
        edit = QLineEdit()
        hidbutton = QPushButton("展示")

        hidbutton.clicked.connect(self.showHidd)

        topLayout.addWidget(label)
        topLayout.addWidget(edit)
        topLayout.addWidget(hidbutton)
        topLayout.addStretch()

        self.setWindowTitle("打开网页")
        self.browser = QWebEngineView()
        self.browser.load(QUrl("http://www.baidu.com"))

        extension = QVBoxLayout()
        extension.addWidget(self.browser)
        self.ext = QWidget()
        self.ext.setLayout(extension)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.ext)

        self.setLayout(mainLayout)
        #固定大小
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.ext.hide()

    def showHidd(self):
        if self.ext.isHidden():
            self.ext.show()
        else:
            self.ext.hide()

if __name__=='__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
