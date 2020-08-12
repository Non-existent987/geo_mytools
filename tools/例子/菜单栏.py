
# mainwindow.py
from PyQt5.QtWidgets import QApplication,  QAction,  QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
 
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,  parent= None):
        QtWidgets.QMainWindow.__init__(self)
        
        self.resize(250,  150)
        self.setWindowTitle('mainwindow')
        
        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)
        
        exit = QAction(QIcon('icons/Blue_Flower.ico'),  'Exit',  self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        exit.triggered.connect(self.close)
        
        self.statusBar()
        
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exit)
 
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())