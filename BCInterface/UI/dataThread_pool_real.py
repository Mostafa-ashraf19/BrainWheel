
import time
import datetime
from BCInterface.Preprocessing import Filesmanager
from BCInterface.Headset import Collect
print(Collect)

from mainproccess import Process
import threading
from PyQt5.QtCore import QObject, pyqtSignal


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

    def __init__(self, sequence,flickering_time,freqs, real_time):
        super(DataAcquisition_thread, self).__init__()

        self.flag = False
        self.sequence = sequence
        self.freqs = freqs
        self.real_time = real_time
        
        self.flickering_time =flickering_time

        self.collect = Collect(False)

        self.data_save = Filesmanager()
    
     
    def collectData(self):
        self.dataThread = threading.Thread(target=self.collectSeq, daemon=True)
        self.dataThread.start()

    def collectSeq(self):


        if self.real_time:
            print ('real time is activated')
            process = Process()
            while (True):
                print (f'time for read new data in real time {datetime.datetime.now()}')
                Data = self.collect.record(self.flickering_time)
                Data = Data.astype(float)
                
                process.make_process(Data)
        else:
            for i in range (len(self.sequence)*2):
                print(f'start collect at: {datetime.datetime.now()}\n')
                Data = self.collect.record(self.flickering_time)

                if self.flag:
                    Data['Label'] = self.freqs[self.sequence[int(i / 2)]-1]
                    self.data_save.save(data=Data)

                self.flag = not self.flag
                self.collect_signal.emit(self.flag)


            self.finish_signal.emit()

