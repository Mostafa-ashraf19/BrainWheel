import time 
import cv2

from computer_vision import ComputerVision
from embedded_system import move_wheelchair

IS_CLOSE_BUFFER_SIZE = 2



class _Buffer:
    def __init__(self, size=IS_CLOSE_BUFFER_SIZE, start_value=False):
        self.buffer = [start_value] * size

    def append(self, value):
        self.buffer.append(value)
        self.buffer.pop(0)

    def is_any_true(self):
        return any(self.buffer)

    def is_any_false(self):
        return not all(self.buffer)

    def __str__(self):
        return str(self.buffer)



def manual_mode(CV_object=None, *, timer=False, verbose=False):
    if CV_object is None:
        CV_object = ComputerVision()
    if timer:
        t0 = time.time()


    is_close_buffer = _Buffer()

    for cache in CV_object.loop(depth_map_img=True, is_close_simple=True, min_dist_simple=True):
        depth_map_img, is_close, min_dist = cache
        is_close_buffer.append(is_close)

        if verbose:
            cv2.imshow('Depth Map', depth_map_img)
            print(is_close_buffer, min_dist)

        # TODO:
        # Get instruction from BCI
        instruction = "forward"

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