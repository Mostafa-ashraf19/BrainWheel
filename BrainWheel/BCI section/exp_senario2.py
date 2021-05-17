import sys
import time
# import BCI
from BCI import BCI
from gui_comp import FlashingBox, movigArrow
from PyQt5.QtWidgets import QWidget,QLabel,QApplication,QGridLayout,QVBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal,QEventLoop,QTimer
from PyQt5.QtGui import QPixmap


class expScenario(QWidget):
    
    def __init__(self,boxes_num = 4,session_period=20, flash_time = 1, static_time = 1):
        super(expScenario,self).__init__()
        
        self.index = 0
        self.boxes = []
        self.data_acqu = None
        self.freq_index = 0 
        self.boxes_num = boxes_num
        self.flash_time = flash_time
        self.static_time = static_time
        self.session_period = session_period
        self._FREQ = [12.00, 10.00, 8.57, 7.50, 6.67] # make it variable
        self.setLayout(QVBoxLayout())
        # self.index = 0

        #2t2kdi 3iznha mra w7da bs wla la2
        self.session_timer = QTimer()
        self.init_session()
        #self.update_frequency_idx = pyqtSignal(float)
        #self.update_frequency_idx.connect(self.update_idx)


    #def update_idx (self):
    #   self.freq_index = (self.freq_index+1) %4

    def start_box_flashing(self):
        global start1
        start1 = time.perf_counter()
        for box in self.boxes:
            box.startFlashing()

    def stop_flashing (self):
        for box in self.boxes:
            box.stopFlashing()
    
    def window_comp (self):

        self.setStyleSheet("background-color: rgb(0,0,0)")
        for i in range (self.boxes_num):
            box = FlashingBox(self._FREQ[i],i)
            self.boxes.append(box)
        # create widget to add boxes 
        container = QWidget()
        container.setLayout(QGridLayout())
        container.layout().addWidget( self.boxes[0],0,0)
        container.layout().addWidget( self.boxes[1],2,0)
        container.layout().addWidget( self.boxes[2],0,2)
        container.layout().addWidget( self.boxes[3],2,2)
        # add black widget 3shan n7afez 3la l shakl
        container.layout().addWidget(QLabel(),1,2)
        container.layout().addWidget(QLabel(),0,1)
        #add widget on the main window
        self.layout().addWidget(container)
               

    def init_session(self):
        self.window_comp() #display boxes

        #make it in separete class thread?
        self.session_timer.start(self.session_period*1000)
        self.data_acqu = DataAcquisition_thread(self._FREQ[self.freq_index])
        self.start_box_flashing()        
        self.data_acqu.start()
        
        
    def timerEvent(self, event):
        self.index = (self.index + 1) % 2
        if self.index == 0:
            self.start_box_flashing()
            #self.data_acqu = DataAcquisition_thread(self._FREQ[self.freq_index])
            self.data_acqu.start()
            
            print('should be true',self.data_acqu.active_state())
        else:
            # remove save file mn hna w a5liha ta7t 
            #freq_index= self._FREQ[self.freq_index]

            self.data_acqu.switch_()
            self.stop_flashing ()
            print('should be false', self.data_acqu.active_state())
        self.update()

    def start_session(self):
        self._timer = self.startTimer( self.static_time *1000, Qt.PreciseTimer) #flashing and stop 



class DataAcquisition_thread(QThread):

    def __init__(self,freq):
        super(DataAcquisition_thread,self).__init__()
        self.current_freq_idx = 0
        self.bci_demo = BCI()
        self._FREQ = [12.00, 10.00, 8.57, 7.50, 6.67]
        self.id=0
        # self.bci_collect= BCI.BCI(labels_sequence=[12.00, 10.00, 8.57, 7.50])
    def active_state(self):  # for debug
        return self._active
    def run (self):
        self._active = True
        # print('aaaa')
        self.collectData()

    def collectData(self):
        start  = time.perf_counter()
        i =0

        while self._active :
            self.bci_demo.record_data()

        print('done')    
        self.save_file(self._FREQ[self.id])
        # self.bci_collect.record_data()
        self.id=(self.id+1)%4
        print (self.id)
        end  = time.perf_counter()
        print (f'time {end - start}')


    def switch_ (self):
        self._active = not self._active

    def save_file(self,label):
       print(f'label is {label}')
       self.bci_demo.save_data("3bas",label) # self.bci_demo.data,
        # fadl azai ageb asm l subject 
        #self.bci_collect.save_data("pierre",self.bci_collect.data,self.current_freq)


    

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    sc1= expScenario()
    sc1.start_session()
    sc1.showMaximized()
    app.exec_()
    




