from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

class MatPFC(FigureCanvas):
    def __init__(self, isPolar = False):
        self.__fig__ = Figure()
        if isPolar:
            self.chart = self.__fig__.add_subplot(111, projection = 'polar')
        else:
            self.chart = self.__fig__.add_subplot(111)

        FigureCanvas.__init__(self, self.__fig__)

if __name__ == '__main__':
    import numpy as np
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
    import sys
    
    N = 150
    r = 2 * np.random.rand(N)
    theta = 2 * np.pi * np.random.rand(N)
    area = 200 * r**2
    colors = theta
    print(colors)
    
    app = QApplication(sys.argv)
    frm = QWidget()
    frm.setWindowTitle('NavigationToolbar')
    layout = QVBoxLayout(frm)
    wgtChart = MatPFC(isPolar = True)
    wgtChart.chart.scatter(theta, r, c = colors, s = area, cmap = 'hsv', alpha = 0.75)
    layout.addWidget(wgtChart)
    toolbar = NavigationToolbar(wgtChart, frm)
    layout.addWidget(toolbar)
    frm.show()
    
    sys.exit(app.exec_())