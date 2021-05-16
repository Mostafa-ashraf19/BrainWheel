import os
import time
import logging 
import datetime 

from .gui_comp import FlashingBox, movigArrow
from .dataThread_pool import DataAcquisition_thread
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QMessageBox


class expScenario(QWidget):
 
    def __init__(self, boxes_num=4, flash_time=1, sequence=[4, 2, 3, 1, 2], freqs=[12.0, 10.0, 8.57, 7.5]):

        super(expScenario, self).__init__()

        self.seq = sequence
        self._FREQ = freqs
        self.boxes_num = boxes_num
        self.flash_time = flash_time

        self.collect = False
        self.boxes = []
        self.freq_index = 0
        self.sequence_len = len(sequence)

        self.setLayout(QVBoxLayout())
    
        self.data_acqu = DataAcquisition_thread(self.seq, self.flash_time,self._FREQ)
        self.data_acqu.collect_signal.connect(self.switch_mode)
        self.data_acqu.finish_signal.connect(self.sessionEnd)

        self.init_session()
        

    def start_box_flashing(self):
        for box in self.boxes:
            box.startFlashing()

    def stop_box_flashing(self):
        for box in self.boxes:
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
            container.layout().addWidget(self.boxes[1], 2, 0)
            container.layout().addWidget(self.boxes[2], 0, 2)
            container.layout().addWidget(self.boxes[3], 2, 2)
            # arrow
            l1 = QLabel()
            l1.adjustSize()
            l1.setStyleSheet("background-color: rgb(0, 0, 0)")
            self.arrow = movigArrow(l1, self.flash_time, self.seq, start_flash=False)
            container.layout().addWidget(l1, 1, 0, 1, 3)


        # add widget on the main window
        self.layout().addWidget(container)



    def init_session(self):
        self.window_comp()  # display boxes
        
        if self.boxes_num == 4:
            self.arrow.startMoving()
        
        self.data_acqu.collectData()  # collect thread

    
    def switch_mode(self, collect):
        print(collect)
        if collect:
            self.start_box_flashing()
            print(f'start flashing at: {datetime.datetime.now()}')
        else:
            self.stop_box_flashing()






    

 

