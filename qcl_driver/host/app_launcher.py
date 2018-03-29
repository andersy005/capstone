from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import sys 

class QCLGUI(QtGui.QWidget):
    
    def __init__(self):

        super(QCLGUI, self).__init__()
        self.setupGUI()
        self.plotter()

    def setupGUI(self):
        self.layout = QtGui.QVBoxLayout()
        self.setWindowIcon(QtGui.QIcon('qcl.png'))
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def plotter(self):
        self.p = pg.plot()
        self.p.plot(x=[0, 1, 2, 4], y=[4, 5, 9, 6])



if __name__ == '__main__':
    pg.mkQApp()
    win = QCLGUI()
    win.setWindowTitle('QCL Driver User Interface')
    win.show()
    win.resize(1100, 700)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()