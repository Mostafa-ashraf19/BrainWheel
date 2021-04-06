import sys
import time
import threading
#from BCI import BCI
# from gui_comp import FlashingBox,movigArrow
from UI.gui_comp import FlashingBox, movigArrow
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGridLayout, QVBoxLayout, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap


class expScenario(QWidget):

    def __init__(self, boxes_num=4, session_period=10, flash_time=1, static_time=1):
        super(expScenario, self).__init__()
        self.state = True
        self.boxes = []
        self.data_acqu = None
        self.freq_index = 0
        self.boxes_num = boxes_num
        self.flash_time = flash_time
        self.static_time = static_time
        self.session_period = session_period
        self._FREQ = [12.00, 10.00, 8.57, 7.50, 6.67]  # make it variable
        self.setLayout(QVBoxLayout())

        # 2t2kdi 3iznha mra w7da bs wla la2
        self.session_timer = QTimer()
        self.session_timer.timeout.connect(self.sessionEnd)
        # self.init_session()

    def sessionEnd(self):
        self.killTimer(self._timer)
        self.arrow.stopMoving()
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Session Ended")
        msgBox.setWindowTitle("QMessageBox Example")
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            self.close()

    def start_box_flashing(self):
        for box in self.boxes:
            box.startFlashing()

    def stop_flashing(self):
        for box in self.boxes:
            box.stopFlashing()

    def window_comp(self):

        self.setStyleSheet("background-color: rgb(0,0,0)")
        for i in range(self.boxes_num):
            box = FlashingBox(self._FREQ[i], i)
            self.boxes.append(box)
        # create widget to add boxes
        container = QWidget()
        container.setLayout(QGridLayout())
        container.layout().addWidget(self.boxes[0], 0, 0)
        container.layout().addWidget(self.boxes[1], 2, 0)
        container.layout().addWidget(self.boxes[2], 0, 2)
        container.layout().addWidget(self.boxes[3], 2, 2)
        # add black widget 3shan n7afez 3la l shakl
        l1 = QLabel()
        self.arrow = movigArrow(l1, self.flash_time)
        l1.adjustSize()
        container.layout().addWidget(l1, 1, 0, 1, 3)
        container.layout().addWidget(QLabel(), 0, 1)
        # add widget on the main window
        self.layout().addWidget(container)

    def init_session(self):
        self.window_comp()  # display boxes
        self.session_timer.start(self.session_period*1000)
        self.data_acqu = DataAcquisition_thread(
            self.flash_time, self._FREQ[self.freq_index])
        self.start_session()
        self.start_box_flashing()
        self.arrow.startMoving()
        self.data_acqu.data_thread.start()

    def timerEvent(self, event):

        self.state = not self.state
        if self.state:
            self.start_box_flashing()
            self.data_acqu = DataAcquisition_thread(
                self.flash_time, self._FREQ[self.freq_index])
            self.data_acqu.data_thread.start()

        else:
            self.freq_index = (self.freq_index+1) % 4
            if self.data_acqu.data_thread.is_alive():
                print('there is a problem')
            self.stop_flashing()

        self.update()

    def start_session(self):
        self._timer = self.startTimer(
            self.static_time * 1000, Qt.PreciseTimer)  # flashing and stop


class DataAcquisition_thread():

    def __init__(self, no_of_seconds, current_freq):
        #self.bci_demo = BCI()
        self.current_freq = current_freq
        self.collect_time = no_of_seconds
        self.data_thread = threading.Thread(target=self.collectData)

    def collectData(self):
        #start  = time.perf_counter()

        for i in range(self.collect_time*128):
            # self.bci_demo.record_data()
            print(i)

        # self.save_file(self.current_freq)

        #end  = time.perf_counter()
        #print (f'time {end - start}')

    def save_file(self, label):
        pass
       #print(f'label is {label}')
       # self.bci_demo.save_data("3bas",label) # self.bci_demo.data,


if __name__ == "__main__":

    app = QApplication(sys.argv)
    sc1 = expScenario()
    sc1.showMaximized()
    app.exec_()
