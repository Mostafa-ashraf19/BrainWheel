from RpiSerial import RpiSerial as r
from time import sleep

GPS_port = "COM5"
GPS = r.GPS(port=GPS_port, baudrate=9600)

while True
    latitude, longitude, time, date = GPS.read()
    print(f"Lat: {latitude}\tLong: {longitude}\tTime: {time}\tDate: {date}")
    sleep(1)