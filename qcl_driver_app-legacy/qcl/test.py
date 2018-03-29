import serial 
import select 

from json_pkt import JSON_Packet

TEST = [
    [1, 2, 3],
    #{'a': 11, 'b': 22, 'c':33},
    #{'d': 'This is a test'},
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


class SerialPort(object):
    """Implements a PySerial port."""

    def __init__(self, port, baud=115200):
        self.serial_port = serial.Serial(port=port,
                                         baudrate=baud,
                                         timeout=0.1,
                                         bytesize=serial.EIGHTBITS,
                                         parity=serial.PARITY_NONE,
                                         stopbits=serial.STOPBITS_ONE,
                                         xonxoff=False,
                                         rtscts=False,
                                         dsrdtr=False)

    def is_byte_available(self):
        readable, _, _ = select.select([self.serial_port.fileno()], [], [], 0)
        return bool(readable)

    def read_byte(self):
        """Reads a byte from the serial port."""
        if self.is_byte_available():
            data = self.serial_port.read()
            if data:
                return data[0]

    def write(self, data):
        """Write data to a serial port."""
        self.serial_port.write(data)

if __name__ == '__main__':
    port = SerialPort(port='/dev/ttyACM1')
    test(port, show_packets=True)