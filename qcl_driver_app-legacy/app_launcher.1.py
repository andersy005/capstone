from serial_port import SerialPort
from json_pkt import JSON_Packet
import numpy as np 
import sys 
import os
import ast 
import json 
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from pyqtgraph.ptime import time
from collections import deque
import threading 




class QCLGUI(QtGui.QWidget):
    def __init__(self):
        super(QCLGUI, self).__init__()
        self.serial_port = SerialPort(port='/dev/ttyACM1')
        self.arr = []
        self.disbuffer = deque([1]*length, length)
        self.timebuffer =  deque([0]*length, length)
        self.setupGUI()
       
    

        self.params = Parameter.create(name='params', type='group', children=[
            dict(name='Current', type='float', values=2, step=0.01, limits=[2, 3]),
            dict(name='Duty Cycle', type='float', value=50.0, dec=True, step=0.1, limits=[0.000, 100.000]),
            dict(name='Set parameters', type='action'),
            ])
        self.tree.setParameters(self.params, showTop=True)

        self.params.param('Set parameters').sigActivated.connect(self.set_params)
        self.set_params()

    
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

        self.view = pg.GraphicsLayoutWidget()
        self.splitter2.addWidget(self.view)

        self.w1 = self.view.addPlot()
        self.w1.setTitle('Modulated Signal - 1')
        self.view.nextRow()
        self.w2 = self.view.addPlot()
        self.w2.setTitle('Modulated Signal - 2')
        self.curve2 = self.w2.plot()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updater)
        self.timer.start(0)
        self.ptr2 = 0

    def send_params(self, PARAMS, show_packets=False):
        self.jpkt = JSON_Packet(self.serial_port, show_packets=show_packets)
        for t in PARAMS:
            print('Sending', t)
            self.jpkt.send(t)
            '''
            while True:
                byte = self.serial_port.read_byte()
                if byte is not None:
                    obj = self.jpkt.process_byte(byte)
                    if obj is not None:
                        print('   Rcvd', obj)
                        break
            '''

    def updater(self):
        self.update1()
        

    def plotter(self):
        self.ptr2 += 1
        self.arr += self.arr
        self.curve2.setData(self.arr)
        self.curve2.setPos(self.ptr2, 0)

    def update1(self):
        byte = self.serial_port.read_byte()
        #print(type(byte))
        if byte is not None:
            self.arr = [byte]
            print(self.arr)
            #obj = self.jpkt.process_byte(byte)

            #if obj is not None:
                
                #print(type(obj))
                #print(' Rcvd', obj)
                #self.arr = np.array(ast.literal_eval(data1[11:-1])).astype('float64')
                #self.plotter()
                #self.arr = np.array(obj)
                #print(self.arr)
                #self.plotter()
                

    def set_params(self):
        self.PARAMS = [{
                  'current': self.params['Current'],
                  'duty_cycle': self.params['Duty Cycle'],
                  
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