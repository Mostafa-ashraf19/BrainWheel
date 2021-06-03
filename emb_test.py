import time

from BrainWheel.embedded_system import *

def main ():

    time.sleep(2)
    print("forward")
    
    move_wheelchair("forward")
    time.sleep(3)

    print("right")
    move_wheelchair("right")
    time.sleep(3)

    print("left")
    move_wheelchair("left")
    time.sleep(3)
    
    print("stop")
    move_wheelchair("stop")


if __name__ == "__main__":
    main()
