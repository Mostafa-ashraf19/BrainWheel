import time

from embedded_system import move_wheelchair

def main():
    time.sleep(2)
    print("forward")
    move_wheelchair("forward")
    time.sleep(1)

    # print("right")
    # move_wheelchair("right")
    # time.sleep(1)

    # print("left")
    # move_wheelchair("left")
    # time.sleep(1)
    
    print("stop")
    move_wheelchair("stop")


if __name__ == "__main__":
    main()