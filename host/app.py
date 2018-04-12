import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
import sys

# Serial Communication Utilities
from json_pkt import JSON_Packet
from serial_port import SerialPort


class QCLAPP(QtGui.QWidget):
    def __init__(self, serial_port=None):
        super(QCLAPP, self).__init__()
        self.serial_port = serial_port
        self.setupGUI()
        
        self.p.param('Set Parameters').sigActivated.connect(self.send_params)


    def setupGUI(self):
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.set_params()
        self.layout.addWidget(self.t) # add parameter tree widget 


    def set_params(self):

        self.params = [{
            'name':
            'Current Setting parameters Options',
            'type':
            'group',
            'children': [
                {
                    'name': 'Power',
                    'type': 'float',
                    'value': 0.0,
                    'step': 1e-1,
                    'limits': [0.0, None],
                    'siPrefix': True,
                    'suffix': 'W'
                },
                {
                    'name': 'Voltage',
                    'type': 'float',
                    'value': 1.0,
                    'step': 1e-1,
                    'limits': [0.01, None],
                    'siPrefix': True,
                    'suffix': 'V'
                },
            ]
        }, {
            'name':
            'Pulse Width Modulation Options',
            'type':
            'group',
            'children': [{
                'name': 'Frequency',
                'type': 'float',
                'value': 500.,
                'step': 1,
                'limits':[0, None],
                'siPrefix': True,
                'suffix': 'Hz'
            }, {
                'name': 'Duty Cycle',
                'type': 'int',
                'value': 50,
                'step': 1,
                'limits': [0, 100]
            }]
        }, {
            'name': 'Set Parameters',
            'type': 'action'
        }]

        self.p = Parameter.create(name='params', type='group', children=self.params)
        self.t = ParameterTree()
        self.t.setParameters(self.p, showTop=False)
        

    def change(self, param, changes):
        print("tree changes:")
        for param, change, data in changes:
            path = self.p.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()
            print('  parameter: %s'% childName)
            print('  change:    %s'% change)
            print('  data:      %s'% str(data))
            print('  ----------')

    
    def send_params(self, show_packets=False):
        
        current = self.p.param('Current Setting parameters Options')['Power'] / self.p.param('Current Setting parameters Options')['Voltage']
        params = {'frequency': self.p.param('Pulse Width Modulation Options')['Frequency'],
                   'duty': self.p.param('Pulse Width Modulation Options')['Duty Cycle'] / 100.,
                   'current': current,
                   'voltage': self.p.param('Current Setting parameters Options')['Voltage'] }

        self.jpkt = JSON_Packet(self.serial_port, show_packets=False)
        print('Sending', params)
        self.jpkt.send(params)
        while True:
            byte = self.serial_port.read_byte()
            if byte is not None:
                obj = self.jpkt.process_byte(byte)
                if obj is not None:
                    print('   Rcvd', obj)
                    break
            



if __name__ == '__main__':

    sp = SerialPort(port='/dev/ttyACM1')
    pg.mkQApp()
    win = QCLAPP(serial_port=sp)
    win.show()
    win.resize(1100, 700)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
