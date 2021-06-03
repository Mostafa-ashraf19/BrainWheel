from BrainWheel.embedded_system import SerialReciever


def main():
    serial = SerialReciever()
    print("Ready to Recieve:")

    while True:
        inst = serial.get_inst()
        if inst != "same":
            print(inst)
        
        if inst == "auto":
            print("Exiting...")
            return


if __name__ == "__main__":
    main()