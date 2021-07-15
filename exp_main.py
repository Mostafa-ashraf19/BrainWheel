import sys
import datetime 

import sys
print(sys.path)

from BCInterface.UI.count_down import CountDown
from BCInterface.UI.exp_scenario2 import expScenario
from PyQt5.QtWidgets import QApplication

import sklearn
sklearn_version = sklearn.__version__
print(sklearn_version)

# configure sequence of frequency
seq1 = [4, 2, 3, 1, 2, 4, 2, 3, 1, 4]    # 10
seq2 = [3, 2, 4]#, 1, 2, 3, 4, 1, 3]#, 1, 3] # 11
seq_null = [1, 2, 0, 3, 4, 3, 1, 4, 0, 2]  # 4,2,0,1,3,  4,2,3,0,1


# switch to autonomous mode by pressing space and return to manual mode again by pressing space again
# autonomous mode has only two flickering boxes display saved location user wanna go to.



#last changes:
#1.arrangement of boxes
#2.add autonomous mode code ()


#configuration 
boxes_num = 4  # 4 or 1
sequence = seq_null
flash_time = 5 # time in seconds
moving_time = 1 # ----------------------> da 3aiz nmshi ad a w flashing time hikon l wa2t l hia2of fi
frequencies = [7.5, 12, 10, 8.57]
real_time = True


if __name__ == "__main__":

    print(str(datetime.datetime.now()))
    app = QApplication(sys.argv)
    m = CountDown(timeout=5)
    m.show()

    sc1 = expScenario(boxes_num=boxes_num, flash_time=flash_time, moving_time=moving_time,
                      sequence=sequence, freqs=frequencies, real_time=real_time)
    sc1.showMaximized()

    app.exec_()


#TODO
# 0- GitHub
# 1- channels check
# 2- Note_book train (togather)
# 3- record data for 3 files(on my PC)
# 4- Head_Set linux (after all)