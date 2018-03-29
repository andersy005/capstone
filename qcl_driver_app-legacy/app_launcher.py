from serial_port import SerialPort
from json_pkt import JSON_Packet

import sys 
import os 
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

port = SerialPort(port='/dev/ttyACM1')

class QCLGUI(QtGui.QWidget):
    def __init__(self):
        super(QCLGUI, self).__init__()
        #QtGui.QWidget.__init__(self)

        self.setupGUI()
    

        self.params = Parameter.create(name='params', type='group', children=[
            dict(name='Voltage', type='float', value=2.5, step=0.01, limits=[2.5, 5]),
            dict(name='Current', type='float', values=2, step=0.01, limits=[2, 3.5]),
            dict(name='Duty Cycle', type='float', value=50.0, dec=True, step=0.1, limits=[0.000, 100.000]),
            dict(name='Pulse Width', type='float', value=100.0, step=0.1, limits=[None, None]),
            dict(name='Set parameters', type='action'),
            ])
        self.tree.setParameters(self.params, showTop=True)

        self.params.param('Set parameters').sigActivated.connect(self.set_params)

    
    def setupGUI(self):
        self.layout = QtGui.QVBoxLayout()
        self.setWindowIcon(QtGui.QIcon('qcl.png'))
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.splitter = QtGui.QSplitter()
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.layout.addWidget(self.splitter)
        
        self.tree = ParameterTree(showHeader=False)
        self.splitter.addWidget(self.tree)
        
        self.splitter2 = QtGui.QSplitter()
        self.splitter2.setOrientation(QtCore.Qt.Vertical)
        self.splitter.addWidget(self.splitter2)
        
        self.worldlinePlots = pg.GraphicsLayoutWidget()
        self.splitter2.addWidget(self.worldlinePlots)
        
        self.animationPlots = pg.GraphicsLayoutWidget()
        self.splitter2.addWidget(self.animationPlots)
        
        self.splitter2.setSizes([int(self.height()*0.8), int(self.height()*0.2)])
        
        self.inertWorldlinePlot = self.worldlinePlots.addPlot()
        self.refWorldlinePlot = self.worldlinePlots.addPlot()
        
        self.inertAnimationPlot = self.animationPlots.addPlot()
        self.inertAnimationPlot.setAspectLocked(1)
        self.refAnimationPlot = self.animationPlots.addPlot()
        self.refAnimationPlot.setAspectLocked(1)
        
        self.inertAnimationPlot.setXLink(self.inertWorldlinePlot)
        self.refAnimationPlot.setXLink(self.refWorldlinePlot)



    def send_params(self, PARAMS, serial_port=port, show_packets=False):
        jpkt = JSON_Packet(serial_port, show_packets=show_packets)
        for t in PARAMS:
            print('Sending', t)
            jpkt.send(t)
            while True:
                byte = serial_port.read_byte()
                if byte is not None:
                    obj = jpkt.process_byte(byte)
                    if obj is not None:
                        print('   Rcvd', obj)
                        break


    def set_params(self):
        self.PARAMS = [{'voltage': self.params['Voltage'],
                  'current': self.params['Current'],
                  'duty_cycle': self.params['Duty Cycle'],
                  'pulse_width': self.params['Pulse Width']
        }]
        self.send_params(self.PARAMS)








if __name__ == '__main__':
    pg.mkQApp()
    win = QCLGUI()
    win.setWindowTitle('QCL Driver User Interface')
    win.show()
    win.resize(1100, 700)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()