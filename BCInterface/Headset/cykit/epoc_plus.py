# -*- coding: utf8 -*-
#
#  CyKIT  2020.06.05
#  ________________________
#  example_epoc_plus.py       
#  
#  Written by Warren
#
"""
   
  usage:  python.exe .\example_epoc_plus.py
  
  ( May need to adjust the key below, based on whether 
    device is in 14-bit mode or 16-bit mode. )
  
"""

import os
import sys
import time
import queue

from BCInterface.Headset.cykit.Py3 import cyPyWinUSB as hid
from  BCInterface.Headset.cykit.Py3.cyCrypto.Cipher import AES
from  BCInterface.Headset.cykit.Py3.cyCrypto import Random

# sys.path.insert(0, './Py3/cyUSB/')
# sys.path.insert(0, './Py3')

# import cyPyWinUSB as hid
# from .Py3 import cyPyWinUSB as hid

# import cyPyWinUSB as hid

# from cyCrypto.Cipher import AES

# from cyCrypto import Random




class EEG(object):
    
    def __init__(self):
        self.start= time.time()
        self.tasks = queue.Queue()
        self.hid = None
        self.delimiter = ", "
        self.read = False

        devicesUsed = 0
    
        for device in hid.find_all_hid_devices():
                if device.product_name == 'EEG Signals':
                    devicesUsed += 1
                    self.hid = device
                    self.hid.open()
                    self.serial_number = device.serial_number
                    device.set_raw_data_handler(self.dataHandler)

        if devicesUsed == 0:
            os._exit(0)
        sn = self.serial_number
        
        # EPOC+ in 16-bit Mode.
        k = ['\0'] * 16
        k = [sn[-1],sn[-2],sn[-2],sn[-3],sn[-3],sn[-3],sn[-2],sn[-4],sn[-1],sn[-4],sn[-2],sn[-2],sn[-4],sn[-4],sn[-2],sn[-1]]

        # EPOC+ in 14-bit Mode.
        #k = [sn[-1],00,sn[-2],21,sn[-3],00,sn[-4],12,sn[-3],00,sn[-2],68,sn[-1],00,sn[-2],88]
        
        self.key = str(''.join(k))
        self.cipher = AES.new(self.key.encode("utf8"), AES.MODE_ECB)

    def wanna_read(self,Flag):
        self.read =Flag

    def dataHandler(self, data):
        if self.read == True:
            join_data = ''.join(map(chr, data[1:]))
            data = self.cipher.decrypt(bytes(join_data,'latin-1')[0:32])
            # print(data,self.tasks.qsize())
            if str(data[1]) == "32": # No Gyro Data.
                return
            self.tasks.put(data)

    def convertEPOC_PLUS(self, value_1, value_2):
        edk_value = "%.8f" % (((int(value_1) * .128205128205129) + 4201.02564096001) + ((int(value_2) -128) * 32.82051289))
        return edk_value

    def get_data(self):
        data = self.tasks.get()
        #print(str(data[0])) COUNTER

        try:
            packet_data = ""
            for i in range(2,16,2):
                packet_data = packet_data + str(self.convertEPOC_PLUS(str(data[i]), str(data[i+1]))) + self.delimiter

            for i in range(18,len(data),2):
                packet_data = packet_data + str(self.convertEPOC_PLUS(str(data[i]), str(data[i+1]))) + self.delimiter

            packet_data = packet_data[:-len(self.delimiter)]

            return str(packet_data)

        except Exception as exception2:
            print(str(exception2))

    def Buffer_number(self): #to check if buffer has data of not before start record
        print(self.tasks.qsize())


# def read_data22():
#     cyHeadset = EEG()
#     data=[]
#     start=time.perf_counter()
#     cyHeadset.wanna_read(True)
#     for i in range(128*5):
#         data.append(cyHeadset.get_data().split(','))
#     stop=time.perf_counter()
#     cyHeadset.wanna_read(False)
#     print(stop-start)
#     cyHeadset.Buffer_number()
#     time.sleep(5)
#     cyHeadset.Buffer_number()




# time.sleep(5)
# read_data22()
#
# time.sleep(5)
# read_data22()
# read_data22()
# read_data22()
# read_data22()

#print(data)
#print(data[0])
#import pandas as pd
#pd.DataFrame(data).to_csv("foo3.csv",header=['ch0','ch1','ch2','ch3','ch4','ch5','ch6','ch7','ch8','ch9','ch10','ch11','ch12','ch13'])
