# main.py -- put your code here!
import pyb
from pyb import DAC
import math
from array import array


def sign(x): return math.copysign(1, x)

# Configure and Initialize Pin 'PA4' as analog
pin = pyb.Pin('A5', pyb.Pin.ANALOG)


# create a buffer containing a square-wave, using half-word samples
buf = array('H', 2048 + int(2047 * sign(math.sin(2 * math.pi * i / 128))) for i in range(128))

# output the square-wave at 800Hz
dac = DAC(pin, bits=12)
dac.write_timed(buf, 800 * len(buf), mode=DAC.CIRCULAR)
#dac.write_timed(buf, pyb.Timer(6, freq=100), mode=DAC.CIRCULAR)
