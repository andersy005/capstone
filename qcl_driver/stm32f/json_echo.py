# This is a version of the echo server which runs on the pyboard.
#
# It parses packets received over the USB VCP (USB REPL) and when a complete
# json packet is received, this gets echoed back to the sender.

from stm_usb_port import USB_Port
from json_pkt import JSON_Packet
import pyb 
import json
from controller import PulseGenerator


def main(serial_port):
    pg = PulseGenerator()
    jpkt = JSON_Packet(serial_port)
    while True:
        byte = serial_port.read_byte()
        if byte is not None:
            obj = jpkt.process_byte(byte)
            if obj is not None:
		        # Retrieve duty_cycle and generate a pulse modulated signal
		        d = obj['duty_cycle']
		        pg.duty_cycle = d
		        pg.set()
                jpkt.send(pg.ch.pulse_width())
               
	

main(USB_Port())
