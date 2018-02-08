import pyb
from pyb import DAC
import math
from array import array


# Configure and Initialize Pin 'PA4' as analog
pin = pyb.Pin('A4', pyb.Pin.ANALOG)


# create a buffer containing a sine-wave, using half-word samples
buf = array('H', 2048 + int(2047 * math.sin(2 * math.pi * i / 128)) for i in range(128))

# output the sine-wave at 400Hz
dac = DAC(pin, bits=12)
dac.write_timed(buf, 400 * len(buf), mode=DAC.CIRCULAR)
