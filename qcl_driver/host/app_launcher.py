from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import sys 

class QCLGUI(QtGui.QWidget):
    
    def __init__(self):

        super(QCLGUI, self).__init__()
        self.setupGUI()

    def setupGUI(self):
        self.layout = QtGui.QVBoxLayout()
        self.setWindowIcon(QtGui.QIcon('qcl.png'))
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)



if __name__ == '__main__':
    pg.mkQApp()
    win = QCLGUI()
    win.setWindowTitle('QCL Driver User Interface')
    win.show()
    win.resize(1100, 700)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()