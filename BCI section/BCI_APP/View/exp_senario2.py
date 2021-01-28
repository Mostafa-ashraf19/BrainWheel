import time
#from BCI import BCI 
from PyQt5.QtWidgets import QWidget,QLabel
from gui_comp import FlashingBox, movigArrow
from PyQt5.QtCore import Qt, QThread, pyqtSignal,QEventLoop,QTimer


class expScenario(QLabel):
    
    def __init__(self,boxes_num = 5,session_period=20, flash_time = 5, static_time = 5 ):
        super(expScenario,self).__init__()
        
        self.index = 0
        self.boxes = []
        self.freq_index = 0 
        self.boxes_num = boxes_num
        self.flash_time = flash_time
        self.static_time = static_time
        self.session_period = session_period
        self._FREQ = [12.00, 10.00, 8.57, 7.50, 6.67] # make it variable
        self._BOX_LOC = [[130,280],[510,500],[510,50],[880,280],[510,280]]

        #2t2kdi 3iznha mra w7da bs wla la2
        self.session_timer = QTimer()
        #self.session_timer.timeout.connect() #close l widget folkha

        self.init_session()


    def start_box_flashing(self):
        for i in range (self.boxes_num):
            self.boxes[i].startFlashing()

    def stop_flashing (self):
        for i in range (self.boxes_num):
            self.boxes[i].stopFlashing()
    
    def window_comp (self):
        self.setStyleSheet("background-color: rgb(0,0,0)")
        # boxed creation 
        for i in range (self.boxes_num):
            box = FlashingBox(self,self._FREQ[i])
            box.move(* self._BOX_LOC[i])
            self.boxes.append(box)
        
        self.arr= movigArrow(self,self.flash_time)
       

    def init_session(self):
        self.window_comp() #display boxes

        #make it in separete class thread?
        self.start_box_flashing()
        self.arr.startMoving()
        self.session_timer.start(self.session_period*1000)
        #self.session_timer.connect()

        self.data_acqu = DataAcquisition_thread(self._FREQ[self.freq_index])
        self.data_acqu.start()
        
        
    def timerEvent(self, event):
        self.index = (self.index + 1) % 2
        if self.index == 0:
            self.start_box_flashing()
            self.data_acqu = DataAcquisition_thread(self._FREQ[self.freq_index])
            self.data_acqu.start()
        else:
            self.data_acqu.save_file()
            self.data_acqu.switch_()
            self.stop_flashing ()
        self.update()

    def start_session(self):
        self._timer = self.startTimer( self.static_time *1000, Qt.PreciseTimer) #flashing and stop 



class DataAcquisition_thread(QThread):

    def __init__(self,freq):
        super(DataAcquisition_thread,self).__init__()
        # self.bci_collect = BCI()
        self.current_freq = freq

    def run (self):
        self._active = True
        # self.collectData()
        self.current_freq = 80

    def collectData(self):
        start = time.perf_counter()
         
        i = 0
        while self._active :
            i+=1
            # self.bci_collect.record_data()

        print (time.perf_counter()-start)

    def switch_ (self):
        self._active = not self._active

    def save_file(self):
        pass
        # fadl azai ageb asm l subject 
#        self.bci_collect.save_data("pierre",self.bci_collect.data,self.current_freq)


    

    




