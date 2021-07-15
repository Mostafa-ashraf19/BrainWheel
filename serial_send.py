import serial

DEFAULT_PORT = 'com6'

class SerialSender:
	device = serial.Serial(DEFAULT_PORT, 115200)
	device.timeout = 1

	# def __del__(self):
	# 	self.device.close()

	@classmethod
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

	@classmethod
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