"""Serial Communication with Laptop.

Connect the serial cable as follows:
    white wire (RXD) -> Pin 8  (TXD)
    green wire (TXD) -> Pin 10 (RXD)
    black wire (GND) -> Pin 9  (GND)

Note: Needs `sudo` to run properly
"""

import time
import serial

from ..errors import InvalidSerialCharError

class SerialReciever:
    def __init__(self):
        self.port = serial.Serial(
            port="/dev/ttyTHS1",
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
        )
        # Wait a second to let the port initialize
        time.sleep(1)
        self.port.write("hello".encode())

    def __del__(self):
        self.port.close()

    def get_inst(self):
        if self.port.inWaiting() > 0:
            data = self.port.read().decode()
            if data == 'w':
                return "forward"
            elif data == 's':
                return "stop"
            elif data == 'a':
                return "left"
            elif data == 'd':
                return "right"
            elif data == 'q':
                return "auto"
            else:
                raise InvalidSerialCharError(data)

        return "same"