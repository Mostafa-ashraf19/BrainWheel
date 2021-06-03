from RpiSerial import RpiSerial as r

GSM_port = "/dev/ttyS0"
GSM_phone_num = "+201144175105"
GSM_message = "JETSON NANO!"
GSM = r.GSM(port=GSM_port, baudrate=115200)

