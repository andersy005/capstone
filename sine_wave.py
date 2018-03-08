# main.py -- put your code here!
import pyb
from pyb import DAC
import math
from array import array

# Configure and Initialize Pin 'PA4' as analog
pin = pyb.Pin('A5', pyb.Pin.ANALOG)
pin2 = pyb.Pin('A4', pyb.Pin.ANALOG)

# create a buffer containing a sine-wave, using half-word samples
buf = array('H', 2048 + int(2047 * math.sin(2 * math.pi * i / 128)) for i in range(128))

# Initialize channel 1 and 2 of DAC
dac = DAC(pin, bits=12)
dac2 = DAC(pin2, bits=12)

#dac.write_timed(buf, 800 * len(buf), mode=DAC.CIRCULAR)
dac.write_timed(buf, pyb.Timer(6, freq=100), mode=DAC.CIRCULAR)
dac2.write_timed(buf, pyb.Timer(6, freq=100), mode=DAC.CIRCULAR)
