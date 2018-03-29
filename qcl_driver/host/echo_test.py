from json_pkt import JSON_Packet
import sys
from serial_port import SerialPort

TEST = [
    [1, 2, 3],
    {'a': 11, 'b': 22, 'c':33},
    {'d': 'This is a test'},
]


def test(serial_port, show_packets):
    jpkt = JSON_Packet(serial_port, show_packets=show_packets)
    for t in TEST:
        print('Sending', t)
        jpkt.send(t)
        while True:
            byte = serial_port.read_byte()
            if byte is not None:
                obj = jpkt.process_byte(byte)
                if obj is not None:
                    print('   Rcvd', obj)
                    break


if __name__=='__main__':
    port = SerialPort(port='/dev/ttyACM1')
    test(port, show_packets=False)
