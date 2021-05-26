import time 
import cv2

from .buffer import _Buffer
from ..computer_vision import ComputerVision
from ..embedded_system import move_wheelchair
from ..embedded_system import SerialReciever


def manual_mode(CV_object=None, *, timer=False, verbose=False):
    if CV_object is None:
        CV_object = ComputerVision()
    if timer:
        t0 = time.time()

    serial = SerialReciever()


    is_close_buffer = _Buffer()

    for cache in CV_object.loop(depth_map_img=True, is_close_simple=True, min_dist_simple=True):
        depth_map_img, is_close, min_dist = cache
        is_close_buffer.append(is_close)

        if verbose:
            cv2.imshow('Depth Map', depth_map_img)
            print(is_close_buffer, min_dist)

        instruction = serial.get_inst()
        # instruction = "forward"

        if instruction == "auto":
            # Goto auto mode
            return

        if is_close_buffer.is_any_true() and instruction == "forward":
            move_wheelchair("stop")
        else:
            move_wheelchair(instruction)

        if timer:
            t1 = time.time()
            
            if not verbose:
                print(is_close_buffer, end=' ')
            print(t1-t0)
            
            t0 = time.time()