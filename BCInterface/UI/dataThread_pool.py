
import time
import datetime
from BCInterface.Preprocessing import Filesmanager
from BCInterface.Headset import Collect
print(Collect)

from mainproccess import Process
import threading
from serial_send import SerialSender
from PyQt5.QtCore import QObject, pyqtSignal

from serial_send import SerialSender

# autonomus  mode is not documented

class DataAcquisition_thread(QObject):
    """
        class description:
        This class handles the  acquisition of the  data from the headset for both training and real-time.
        Training mode: sequence  by which user determine which box to look at. collected data is stored in files
        Real time mode: data collected for flickering time then passed to be processed and predict the freq of flickering.

        class attributes:
            - sequence -(manual mode):  list of int refer to sequence of flickering boxes the user has to stare at
            - flickering_time: time of flickering of the boxes "in sec"
            - freqs: list of boxes frequencies
            - real_time: bool to choose between training and  real-time  "set true if you wanna activate real time mode"
            - finish_signal: pyqtSignal used through training mode fired when entered sequence is finished
            - collect_signal: pyqtSignal used through training mode emitted every "flickering" period to start or stop boxes flickering

        class method
            - collectData: created a Thread to collect data while boxes is flickering in the main thread
            - collectSeq: the task of the thread, loops over sequence of frequency "training mode",
            sequence*2 cause each flickering period is followed  by no stimulus period
            saving data collected at flickering time and trash  data at no stimulus period
            for real time mode data collected and passed to process class.
    """

    collect_signal = pyqtSignal(bool)
    finish_signal = pyqtSignal()
    switch_mode_signal = pyqtSignal()

    def __init__(self, sequence,flickering_time,moving_time,freqs, real_time):
        super(DataAcquisition_thread, self).__init__()

        self.flag = False
        self.sequence = sequence
        self.freqs = freqs
        self.real_time = real_time
        self.moving_time = moving_time
        
        self.flickering_time =flickering_time
        self.manual_mode = True

        #self.serial_sende = SerialSender()
        self.collect = Collect(False)
        self.switch_mode_signal.connect(self.switch_mode_handle)
        self.data_save = Filesmanager()


    def collectData(self):
        self.dataThread = threading.Thread(target=self.collectSeq, daemon=True)
        self.dataThread.start()



    def switch_mode_handle(self):
        print(f'emite switch mode  {datetime.datetime.now()}')
        self.manual_mode = not self.manual_mode

    def collectSeq(self):
        if self.real_time:
            print ('real time is activated')
            self.process = Process()
            while (self.manual_mode):
                #if self.manual_mode:
                print (f'new iteration {datetime.datetime.now()}')
                # self.serial_sende.send_inst('stop')
                SerialSender.send_inst("stop") # comment if continus 
                Data = self.collect.record(1)
                #time.sleep(1)
                Data = self.collect.record(self.flickering_time)
                Data = Data.astype(float)
                self.process.make_process(Data)
                # moving time msh b3mel 7aga
                Data = self.collect.record(self.moving_time)
                #time.sleep(self.moving_time) # comment if continus 
            print (self.manual_mode)



        else:
            for i in range (len(self.sequence)*2):
                print(f'start collect at: {datetime.datetime.now()}\n')
                Data = self.collect.record(self.flickering_time)

                if self.flag :
                    if self.sequence[int(i / 2)] == 0:
                        Data['Label'] = 1
                    else:
                        Data['Label'] = self.freqs[self.sequence[int(i / 2)]-1]

                    self.data_save.save(data=Data)

                self.flag = not self.flag
                self.collect_signal.emit(self.flag)
            print ('fire signal to close gui')
            self.finish_signal.emit()



   
        
       


