import time 
import cv2

from .buffer import _Buffer
# from ..computer_vision import ComputerVision
from ..embedded_system import move_wheelchair
from ..embedded_system import SerialReciever


def manual_mode(*, timer=False, verbose=False):
    if timer:
        t0 = time.time()

    serial = SerialReciever()


    is_close_buffer = _Buffer()

    while True:
        instruction = serial.get_inst()
        #instruction = "forward"

        if instruction == "auto":
            # Goto auto mode
            move_wheelchair('stop')
            return

        move_wheelchair(instruction)

        if timer:
            t1 = time.time()
            
            # print(t1-t0)
            if instruction != "same":
                print(instruction)
            
            t0 = time.time()