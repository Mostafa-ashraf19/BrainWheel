import sys
import datetime 

import sys
print(sys.path)

# from BCInterface.UI.count_down import CountDown
from BCInterface.UI.exp_scenario2 import expScenario
from PyQt5.QtWidgets import QApplication


# configure sequence of frequency 
seq1 =  [4 ,2 ,3 ,1 ,2 ,4 ,2 ,3 ,1 ,4]    # 10
seq2 =  [3 ,2 ,4 ,1 ,2 ,3 ,4 ,1 ,3 ,1 ,3] # 11


#configuration 
boxes_num = 1  # 4 or 1 
sequence = seq1
flash_time = 5 # time in seconds 
frequencies = [12.0, 10.0, 8.57, 7.5]


if __name__ == "__main__":

    print (str(datetime.datetime.now()))
    app = QApplication(sys.argv)
    # m = CountDown(timeout=5)
    # m.show()

    sc1 = expScenario(boxes_num=boxes_num, flash_time=flash_time,sequence=seq1,freqs=frequencies)
    sc1.showMaximized()

    app.exec_()



