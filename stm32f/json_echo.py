
# This is a version of the echo server which runs on the Microcontroller.
#
# It parses packets received over the USB VCP (USB REPL) and when a complete
# json packet (containing parameters) is received, the microcontroller sets the configurations.

from stm_usb_port import USB_Port
from json_pkt import JSON_Packet
import pyb 
import json
from utils import PulseGenerator, Controller


def main(serial_port):
    pg = PulseGenerator()
    control = Controller()
    jpkt = JSON_Packet(serial_port)
    while True:
        byte = serial_port.read_byte()
        if byte is not None:
            obj = jpkt.process_byte(byte)
            if obj is not None:
            	duty = obj['duty']
                freq = obj['frequency']
                current = obj['current']
                volt = obj['voltage']
                        
                pg.duty_cycle = duty
                pg.timer.freq(freq)
                pg.set()
                control.current_setting(volt)
                read_current = control.feedback_loop()
                jpkt.send(read_current)
               
	

main(USB_Port())
