import sys
import datetime

import sys

print(sys.path)

from BCInterface.UI.count_down import CountDown
from BCInterface.UI.exp_scenario2 import expScenario
from PyQt5.QtWidgets import QApplication

# TODO
# 1. add 5th flashing box
# 2. no sequence for real time
# 3. add null option in sequence and gui -> done

# configure sequence of frequency

# to add null in the sequence add: "NULL"

seq_10_12 = [3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3]
seq1 = [4, 2, 3, 1, 2, 4, 2, 3, 1, 4]  # 10
seq2 = [3, 2, 4, 1, 2, 3, 4, 1, 3, 1, 3]  # 11

# null is encoded by zero
seq_null = [1, 2, 0, 3, 4, 3, 1, 4, 0, 2]  # 4,2,0,1,3,  4,2,3,0,1

# configuration
boxes_num = 4  # 4 or 1
sequence = seq_null

flash_time = 5  # time in seconds
frequencies = [7.5, 8.57, 10.0, 12.0]

if __name__ == "__main__":
    print(str(datetime.datetime.now()))
    app = QApplication(sys.argv)
    m = CountDown(timeout=5)
    m.show()

    sc1 = expScenario(boxes_num=boxes_num, flash_time=flash_time, sequence=sequence, freqs=frequencies, real_time=False)
    sc1.showMaximized()

    app.exec_()
