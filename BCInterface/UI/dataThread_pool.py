
import time
import datetime
from BCInterface.Preprocessing import Filesmanager
from BCInterface.Headset import Collect
print(Collect)

import threading
from PyQt5.QtCore import QObject, pyqtSignal

freq_map = { 1:12.00, 2:10.00, 3:8.57, 4:7.50, 5:6.66}

class DataAcquisition_thread(QObject):
    """

        class attributes:
            - sequence: is a list has flickering frquency sequence 
            - flickering_time: number of seconds of flickering

        class method 
            - collectData: ThreadPoolExecutor is created for data colleciton 

            - collectSeq: it is the task of the thread, loops over sequence of frequency,
            sequence*2 cause each flickering period is followed  by no stimulus period  
            saving data collected at flickering time and trash  data at no stimulus period

        collect_signal: signal emitted every "flickering" period to start or stop boxes flickering 
        finish_signal: emitted after finshing the loop to indicate end of session


    """

    collect_signal = pyqtSignal(bool)
    finish_signal = pyqtSignal()

    def __init__(self, sequence,flickering_time):
        super(DataAcquisition_thread, self).__init__()

        self.flag = False
        self.sequence = sequence
        
        self.flickering_time =flickering_time

        self.collect = Collect(False)

        self.data_save = Filesmanager()
    
     
    def collectData(self):
        self.dataThread = threading.Thread(target=self.collectSeq, args=(self.flickering_time, self.flag, self.sequence), daemon=True)
        self.dataThread.start()

    def collectSeq(self, flickering_time, flag, sequence):

        for i in range (len(sequence)*2):
            print(f'start collect at: {datetime.datetime.now()}\n')
            Data = self.collect.record(flickering_time)

            if flag:
                # Data['Label'] = self.sequence[int(i/2)]
                Data['Label'] = freq_map[self.sequence[int(i / 2)]]
            
                self.data_save.save(data=Data)

            flag = not flag
            self.collect_signal.emit(flag)


        self.finish_signal.emit()



   
        
       


