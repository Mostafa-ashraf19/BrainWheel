import serial

DEFAULT_PORT = 'com3'

class SerialSender:
	def __init__(self, port=DEFAULT_PORT):
		self.device = serial.Serial(port, 115200)
		self.device.timeout = 1

	def __del__(self):
		self.device.close()

	def send_inst(self, instruction):
		if instruction == "forward":
			self._send_char('w')
		if instruction == "stop":
			self._send_char('s')
		if instruction == "left":
			self._send_char('a')
		if instruction == "right":
			self._send_char('d')
		if instruction == 'auto':
			self._send_char('q')

	def _send_char(self, char):
		self.device.write(char.encode())


#
# def test():
# 	import time
# 	sender = SerialSender()
# 	instructions = ["forward", "stop", "left", "right"] * 2 + ['auto']
# 	for i in instructions:
# 		print(i)
# 		sender.send_inst(i)
# 		time.sleep(1)
#
# if __name__ == "__main__":
# 	test()