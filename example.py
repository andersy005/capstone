import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui


app = QtGui.QApplication([])
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType




params = [{'name': 'Quantum Cascade Laser Settings', 'type':'group', 'children':
[{'name': 'Frequency', 'type': 'float', 'value': 10.},
{'name': 'Duty Cycle', 'type': 'float', 'value': 20.}]}]


def change():
    pass
    
## Create tree of Parameter objects
p = Parameter.create(name='params', type='group', children=params)
p.sigTreeStateChanged.connect(change)

t = ParameterTree()
t.setParameters(p, showTop=False)


win = QtGui.QWidget()
win.show()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
