import Jetson.GPIO as GPIO

from ..errors import InvalidDirectionError
import time
GPIO.setmode(GPIO.BOARD)

GPIO_motor_pin_1 = 11
GPIO_motor_pin_2 = 12

GPIO.setup(GPIO_motor_pin_1, GPIO.OUT)
GPIO.setup(GPIO_motor_pin_2, GPIO.OUT)

def move_wheelchair(direction):
    if direction == "forward":
        GPIO.output(GPIO_motor_pin_1, True)
        GPIO.output(GPIO_motor_pin_2, True)

    elif direction == "left":
        GPIO.output(GPIO_motor_pin_1, True)
        GPIO.output(GPIO_motor_pin_2, False)
    
    elif direction == "right":
        GPIO.output(GPIO_motor_pin_1, False)
        GPIO.output(GPIO_motor_pin_2, True)
    
    elif direction == "stop":
        GPIO.output(GPIO_motor_pin_1, False)
        GPIO.output(GPIO_motor_pin_2, False)
    
    else:
        raise InvalidDirectionError()
