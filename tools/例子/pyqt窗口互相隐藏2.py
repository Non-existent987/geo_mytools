import sys
import matplotlib.pyplot as plt

from PyQt5.Qt import QSizePolicy
from PyQt5.QtWidgets import (
    QDialog, QApplication, QGridLayout, QWidget, QGroupBox, QPushButton
)
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.settings = QGroupBox('Settings:')
        self.settingsLayout = QGridLayout()
        self.settings.setLayout(self.settingsLayout)
        self.showFigureBtn = QPushButton('Show Figure')
        self.settingsLayout.addWidget(self.showFigureBtn)
        self.layout.addWidget(self.settings)

        self.figureWidget = QWidget()
        self.figureWidget.setMinimumSize(300, 300)
        self.figureLayout = QGridLayout(self.figureWidget)
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.figureLayout.addWidget(self.canvas)
        self.figureWidget.setLayout(self.figureLayout)
        self.layout.addWidget(self.figureWidget)
        self.figureWidget.setVisible(False)

        self.showFigureBtn.clicked.connect(self.toggle_figure)

        self.min_size = (300, 100)
        self.resize(*self.min_size)

    def toggle_figure(self):
        state = not self.figureWidget.isVisible()
        if state:
            self.showFigureBtn.setText("Hide Figure")
            self.textBrowser.setVisible(state)
        else:
            self.showFigureBtn.setText("Show Figure")
            self.textBrowser.setVisible(state)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = MainWindow()
    GUI.show()
    sys.exit(app.exec_())