# This is a version of the echo server which runs on the pyboard.
#
# It parses packets received over the USB VCP (USB REPL) and when a complete
# json packet is received, this gets echoed back to the sender.

from stm_usb_port import USB_Port
from json_pkt import JSON_Packet
import pyb 
import json
from pyb import DAC
import math
from array import array

def sign(x): return math.copysign(1, x)

# Configure and Initialize Pin 'PA4' as analog
pin = pyb.Pin('A4', pyb.Pin.ANALOG)


# create a buffer containing a sine-wave, using half-word samples
buf = array('H', 2048 + int(2047 * math.sin(2 * math.pi * i / 128)) for i in range(128))

# create a buffer containing a square-wave, using half-word samples
#buf = array('H', 2048 + int(2047 * sign(math.sin(2 * math.pi * i / 128))) for i in range(128))


# output the sine-wave at 400Hz
dac = DAC(pin, bits=12)

dac.write_timed(buf, 400 * len(buf), mode=DAC.CIRCULAR)

def main(serial_port):
    jpkt = JSON_Packet(serial_port)
    while True:
        byte = serial_port.read_byte()
        if byte is not None:
            obj = jpkt.process_byte(byte)
            current = obj['current']
            
            if obj is not None:

                #jpkt.send(current)
		jpkt.send([1, 2])
        
        #jpkt.send(json.dumps(current).encode('ascii'))
       
        

main(USB_Port())