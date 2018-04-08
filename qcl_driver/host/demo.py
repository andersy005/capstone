import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui


app = QtGui.QApplication([])
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType


params = [

    {'name': ' Current Setting parameters Options', 'type': 'group', 'children': [
        {'name': 'Current', 'type': 'float', 'value': 0.0, 'step': 1e-1, 'limits': [0.0, 3.0], 'siPrefix': True, 'suffix': 'A'},
        {'name': 'Voltage', 'type': 'float', 'value': 0.0, 'step': 1e-1, 'limits': [0.0, 3.0], 'siPrefix': True, 'suffix': 'V'},

        
    ]},

    {'name': 'Pulse Width Modulation Options', 'type': 'group', 'children': [
        {'name': 'Frequency', 'type': 'float', 'value': 0.0, 'step': 1, 'siPrefix': True, 'suffix': 'Hz'},
        {'name': 'Duty Cycle', 'type': 'int', 'value': 0, 'step': 1, 'limits': [0, 100]}
        
    ]}
    
]

## Create tree of Parameter objects
p = Parameter.create(name='params', type='group', children=params)

## If anything changes in the tree, print a message
def change(param, changes):
    print("tree changes:")
    for param, change, data in changes:
        path = p.childPath(param)
        if path is not None:
            childName = '.'.join(path)
        else:
            childName = param.name()
        print('  parameter: %s'% childName)
        print('  change:    %s'% change)
        print('  data:      %s'% str(data))
        print('  ----------')
    
p.sigTreeStateChanged.connect(change)


def valueChanging(param, value):
    print("Value changing (not finalized): %s %s" % (param, value))
    
# Too lazy for recursion:
for child in p.children():
    child.sigValueChanging.connect(valueChanging)
    for ch2 in child.children():
        ch2.sigValueChanging.connect(valueChanging)
        


## Create ParameterTree widget
#t = ParameterTree()
#t.setParameters(p, showTop=False)



win = QtGui.QWidget()
layout = QtGui.QGridLayout()
win.setLayout(layout)
layout.addWidget(QtGui.QLabel("QCL Driver Settings"), 0,  0, 1, 2)
layout.addWidget(p, 1, 0, 1, 1)
win.show()
win.resize(800,800)




## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
