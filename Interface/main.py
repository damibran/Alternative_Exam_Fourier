import sys
from GUI import *
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

class MyFun(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setXRange(0, 10, padding=0)
        self.graphWidget.setYRange(20, 55, padding=0)

        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]

        # plot data: x, y values
        self.graphWidget.plot(hour, temperature,size=30)
        

        self.ui.proceedBut.clicked.connect(self.onButtonClicked)

    def onButtonClicked(self):
        pass
        


        

if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    myapp=MyFun()
    myapp.show()
    sys.exit(app.exec_())
