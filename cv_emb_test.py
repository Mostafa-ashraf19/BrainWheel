import time 
import cv2

from computer_vision import ComputerVision
from embedded_system import move_wheelchair

def main():
    CV = ComputerVision()
    t0= time.time()

    for cache in CV.loop(depth_map_img=True, is_close_simple=True, min_dist_simple=True):
        depth_map_img, is_close, min_dist = cache
        cv2.imshow('Depth Map', depth_map_img)
        # print(is_close, min_dist)

        if is_close:
            move_wheelchair('stop')
        else:
            move_wheelchair('forward')

        t1 = time.time()
        print(is_close, t1-t0)
        t0 = time.time()

if __name__ == "__main__":
    main()