import os
import time
import logging 
import datetime 

from gui_comp import FlashingBox, movigArrow
#from dataThread import DataAcquisition_thread

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGridLayout, QVBoxLayout, QMessageBox


# logging file for tracing only 
logging.basicConfig(filename='app2.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')



class expScenario(QWidget):
    def __init__(self, boxes_num=4, flash_time=1,sequence=[4 ,2 ,3 ,1 ,2],freqs= [12.0, 10.0, 8.57, 7.5]):

        super(expScenario, self).__init__()

        self.seq = sequence
        self._FREQ = freqs
        self.boxes_num = boxes_num
        self.flash_time = flash_time

        self.flag = True
        self.boxes = []
        self.freq_index = 0
        self.sequence_len = len (sequence)
        self.session_period = self.sequence_len*(flash_time*2)

        self.data_acqu = None
        self.setLayout(QVBoxLayout())

        # needed timers 
        # session timer for whole session 
        self.session_timer = QTimer()
        self.session_timer.timeout.connect(self.sessionEnd)
        # flashing timer 
        self.flashing_timer = QTimer(self, interval= 1000*flash_time)
        self.flashing_timer.timeout.connect(self.flashing)

        self.init_session()
        

    def start_box_flashing(self):
        for box in self.boxes:
            box.startFlashing()

    def stop_box_flashing(self):
        for box in self.boxes:
            box.stopFlashing()    

    def sessionEnd(self):
        self.flashing_timer.stop()
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
        if self.boxes_num == 4:
            container.layout().addWidget(self.boxes[1], 2, 0)
            container.layout().addWidget(self.boxes[2], 0, 2)
            container.layout().addWidget(self.boxes[3], 2, 2)
        
        l1 = QLabel()
        l1.adjustSize()
        self.arrow = movigArrow(l1, self.flash_time,self.seq,start_flash=False)
        container.layout().addWidget(l1, 1, 0, 1, 3)
        container.layout().addWidget(QLabel(), 0, 1)
        # add widget on the main window
        self.layout().addWidget(container)



    def init_session(self):
        self.window_comp()  # display boxes
        self.session_timer.start(self.session_period*1000)
        self.flashing_timer.start()
        if self.boxes_num == 4:
            self.arrow.startMoving()
    

    def flashing(self):
      if self.flag:
        #print(time.perf_counter()-self.start)
        self.start_box_flashing()
        #self.data_acqu = DataAcquisition_thread(self.flash_time, self._FREQ[self.freq_index])
        #self.data_acqu.data_thread.start()

      else:
        self.stop_box_flashing()
        self.freq_index = (self.freq_index+1) % 4
        #if self.data_acqu.data_thread.is_alive():
        #    print('there is a problem')

      self.flag = not self.flag

 

