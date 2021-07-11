try:

    def help():
        print("Help.")

    def doStuff():
        print("Doing Stuff")

    while True:
        x = int(input())
        if x == 1:
            help()
        elif x == 2:
            doStuff()
        else:
            exit()

except KeyboardInterrupt:
    exit()