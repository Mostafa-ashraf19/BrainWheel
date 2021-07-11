import os
import time
import logging 
import datetime 

from .gui_comp import FlashingBox, movigArrow
from .dataThread_pool import DataAcquisition_thread
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QMessageBox


# for real time 
# 1. stop moving of arrow 
# 2. for every flickering time  data should be sent - create process and with each finihsing call function that take the data
# 3. stop  stop function of flashing boxes 
# 4. take no sequence 
# 5. no sessionEnd 


class expScenario(QWidget):
    #real_time
    def __init__(self, boxes_num=4, flash_time=1, sequence=[4, 2, 3, 1, 2], freqs=[12.0, 10.0, 8.57, 7.5], real_time=False):

        super(expScenario, self).__init__()
        self.seq = sequence
        self._FREQ = freqs
        self.boxes_num = boxes_num
        self.flash_time = flash_time
        #real_time
        self.real_time = real_time

        self.collect = False
        self.boxes = []
        self.freq_index = 0
        self.sequence_len = len(sequence)

        self.setLayout(QVBoxLayout())
    
        self.data_acqu = DataAcquisition_thread(self.seq, self.flash_time,self._FREQ,self.real_time)

        self.init_session()
        

    def start_box_flashing(self):
        for box in self.boxes:
            box.startFlashing()

    def stop_box_flashing(self):
        print ('closing from stop box flashing')
        for box in self.boxes:
            print('from inside')
            box.stopFlashing()

    def sessionEnd(self):
        #self.flashing_timer.stop()
        self.stop_box_flashing()
        self.arrow.stopMoving()
       
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Session Ended")
        msgBox.setWindowTitle("QMessageBox Example")
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            self.close()


    def window_comp(self):
        self.setStyleSheet("background-color: rgb(0,0,0)")
        for i in range(self.boxes_num):
            box = FlashingBox(self._FREQ[i], i)
            self.boxes.append(box)
        
        # create widget to add boxes
        container = QWidget()
        container.setLayout(QGridLayout())
        container.layout().addWidget(self.boxes[0], 0, 0)
        container.layout().addWidget(QLabel(), 0, 1)

        if self.boxes_num == 4:
            container.layout().addWidget(self.boxes[1], 3, 0)
            container.layout().addWidget(self.boxes[2], 0, 3)
            container.layout().addWidget(self.boxes[3], 3, 3)

        # real_time
        # still working on 4 boxes as a max
        if not self.real_time or self.boxes_num >1:
            # arrow
            l1 = QLabel()
            l1.adjustSize()

            l1.setStyleSheet("background-color: rgb(0, 0, 0)")
            self.arrow = movigArrow(l1, self.flash_time, self.seq, start_flash=False)
            container.layout().addWidget(l1, 1, 0, 2, 3)



        # add widget on the main window
        self.layout().addWidget(container)



    def init_session(self):
        self.window_comp()  # display boxes

        if self.real_time:
            self.start_box_flashing()
        else:
            self.data_acqu.collect_signal.connect(self.switch_mode)
            self.data_acqu.finish_signal.connect(self.sessionEnd)

        self.data_acqu.collectData()  # collect thread

    # real_time for this mode this not be called  -> configured in the __init__ function
    def switch_mode(self, collect):
        print(collect)
        if collect:
            self.arrow.movigArrow()
            self.start_box_flashing()
            print(f'start flashing at: {datetime.datetime.now()}')
        else:
            self.arrow.movigArrow()
            self.stop_box_flashing()






    

 

