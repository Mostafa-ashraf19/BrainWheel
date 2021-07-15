import datetime
from PyQt5.Qt import Qt
from .gui_comp import FlashingBox, movigArrow
from .dataThread_pool import DataAcquisition_thread
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QMessageBox
from serial_send import SerialSender


class expScenario(QWidget):

    def __init__(self, boxes_num=4, flash_time=1, moving_time=4, sequence=[4, 2, 3, 1, 2],
                 freqs=[12.0, 10.0, 8.57, 7.5], real_time=False):
        super(expScenario, self).__init__()
        self.space_pushed = False
        self.seq = sequence
        self._FREQ = freqs
        self.boxes_num = boxes_num
        self.flash_time = flash_time
        self.moving_time = moving_time
        self.real_time = real_time
        self.collect = False
        self.boxes = []
        self.freq_index = 0
        self.sequence_len = len(sequence)
        self.setLayout(QVBoxLayout())
        self.data_acqu = DataAcquisition_thread(sequence=self.seq, flickering_time=self.flash_time,
                                                moving_time=self.moving_time, freqs=self._FREQ, real_time=self.real_time)
        self.init_session()


    def start_box_flashing(self):
        for box in self.boxes:
            box.startFlashing()

    def stop_box_flashing(self):
        for box in self.boxes:
            box.stopFlashing()    

    def sessionEnd(self):

        print('session ended')
        self.stop_box_flashing()
        print ('box stopped')
        self.arrow.stopMoving()
       
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Session Ended")
        msgBox.setWindowTitle("QMessageBox Example")
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            self.close()


    # new function for autonomus mode
    def autonomus_mode(self):
        #print(f'fire switch mode  {datetime.datetime.now()}')
        self.data_acqu.switch_mode_signal.emit()
        if self.space_pushed:
            #send auto through serial
            # self.data_acqu.process.autonomus_signal.emit(1)
            SerialSender.send_inst("auto")
            # close main window
            self.main_container.close()
            self.stop_box_flashing()
            # create autonomus window
            self.autonomus_window_comp()
            self.start_box_flashing()
        else:
            SerialSender.send_inst("auto")
            if self.data_acqu.dataThread.isAlive():
                print ('there is a problem \n')
            self.auto_window.close()
            self.main_window_comp()
            self.data_acqu.collectData()
            self.start_box_flashing()

    # triggering autonomous/manual mode by pressing space button form keyboard
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.space_pushed = not self.space_pushed
            self.autonomus_mode()

    def autonomus_window_comp(self):
        self.setStyleSheet("background-color: rgb(0,0,0)")
        box1 = FlashingBox(self._FREQ[0], 0)
        box2 = FlashingBox(self._FREQ[1], 1)
        self.boxes = [box1, box2]

        # create widget to add boxes
        self.auto_window = QWidget()
        self.auto_window.setLayout(QGridLayout())
        self.auto_window.layout().addWidget(QLabel(), 0, 0, 1, 4)
        self.auto_window.layout().addWidget(QLabel(), 2, 0, 1, 4)
        self.auto_window.layout().addWidget(QLabel(), 1, 1, 1, 2)
        self.auto_window.layout().addWidget(box1, 0, 0)
        self.auto_window.layout().addWidget(box2, 2, 3)

        self.layout().addWidget(self.auto_window)



    def main_window_comp(self):
        self.setStyleSheet("background-color: rgb(0,0,0)")
        self.boxes=[]
        for i in range(self.boxes_num):
            box = FlashingBox(self._FREQ[i], i)
            self.boxes.append(box)
        
        # create widget to add boxes
        self.main_container = QWidget()
        self.main_container.setLayout(QGridLayout())
        self.main_container.layout().addWidget(self.boxes[0], 0, 0)
        self.main_container.layout().addWidget(QLabel(), 0, 1)

        if self.boxes_num == 4:
            self.main_container.layout().addWidget(self.boxes[1], 0, 3)
            self.main_container.layout().addWidget(self.boxes[2], 3, 0)
            self.main_container.layout().addWidget(self.boxes[3], 3, 3)

        # real_time
        # still working on 4 boxes as a max
        if not self.real_time or self.boxes_num >1:
            # arrow
            l1 = QLabel()
            l1.adjustSize()
            l1.setStyleSheet("background-color: rgb(0, 0, 0)")
            self.arrow = movigArrow(l1, self.flash_time, self.seq, start_flash=False)
            self.main_container.layout().addWidget(l1, 1, 0, 2, 4)

        # add widget on the main window
        self.layout().addWidget(self.main_container)


    def init_session(self):
        self.main_window_comp()  # display boxes

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






    

 

