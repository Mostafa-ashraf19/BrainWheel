import threading 
from BCI import BCI
#import multiprocessing

class DataAcquisition_thread():

    def __init__(self, no_of_seconds, current_freq):
        #self.bci_demo = BCI()
        self.current_freq = current_freq
        self.collect_time = no_of_seconds
        self.data_thread = threading.Thread(target=self.collectData)
        #self.data_thread = multiprocessing.Process(target=self.collectData)

    def collectData(self):
        start  = time.perf_counter()
        bci_demo = BCI()
        for i in range(self.collect_time*128):
            logging.warning('abda2 a5od sample'+str(datetime.datetime.now()))
            self.bci_demo.record_data()
            logging.warning('end sample'+str(datetime.datetime.now()))
            #logging.warning('This will get logged to a file')
        #logging.warning('end'+str(datetime.datetime.now()))
            
            #pass

        self.save_file(self.current_freq)

        end  = time.perf_counter()
        print (f'time {end - start}')

    def save_file(self, label):
       #pass
       #print(f'label is {label}')
       #self.bci_demo.save_data("3bas",label)
       self.bci_demo.save_data("3bas"+str(datetime.datetime.now()).split()[0],label) # self.bci_demo.data,
