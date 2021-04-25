import numpy as np
import pandas as pd
import logging
import datetime

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


channels_def = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']
channels_indix=[  0,     1,   2,     3,     4,    5,    6,    7,    8,    9,    10,    11,   12,   13 ]


class Collect:

    def __init__(self, emotiv_hs=True):
        self.emotiv_hs = emotiv_hs  # True For Emotive, False EEG
        if self.emotiv_hs == True:
            from emokit.emotiv import Emotiv
            self.reader = Emotiv()

        else:
            # import EEG
            from BCInterface.Headset.cykit.epoc_plus import EEG
            print(EEG)
            self.reader = EEG()

    def record_eeg(self):
        """
        return one sample from EEG cykit package
        """
        return self.reader.get_data().split(',')

    def record_emotive(self, no_of_seconds):
        """
        return no_of_seconds*128 samples from EEG Emotiv package
        """
        return self.read(no_of_seconds)

    def read(self, no_of_seconds):
        """
        Read all samples from EEG Emotive package
        """

        # with Emotiv() as headset:
        all_data = []
        logging.warning('start collect '+ str(datetime.datetime.now()))
        for _ in range(no_of_seconds*128):
            all_data.append(self.get_single_sample(self.reader))
            logging.warning('collect '+ str(datetime.datetime.now()))
        logging.warning('end collect '+ str(datetime.datetime.now()))
        return all_data

    def get_single_sample(self, headset):
        '''
        get one sample from EEG Emotive package
        '''
        data = []
        while True:
            packet = headset.dequeue()
            # print(packet)
            if packet is not None:
                data.append(packet.sensors['AF3']['value'])
                data.append(packet.sensors['F7']['value'])
                data.append(packet.sensors['F3']['value'])
                data.append(packet.sensors['FC5']['value'])

                data.append(packet.sensors['T7']['value'])
                data.append(packet.sensors['P7']['value'])
                data.append(packet.sensors['O1']['value'])
                data.append(packet.sensors['O2']['value'])

                data.append(packet.sensors['P8']['value'])
                data.append(packet.sensors['T8']['value'])

                data.append(packet.sensors['FC6']['value'])
                data.append(packet.sensors['F4']['value'])
                data.append(packet.sensors['F8']['value'])
                data.append(packet.sensors['AF4']['value'])
                break
        return data

    def record(self, no_of_seconds):  # Secs number
        """
        collect n seconds data then return it as dataframe
        @Args  no_of_seconds:int
        @return DataFrame
        """
        if self.emotiv_hs == True:  # Emotive
            self.reader.clear_queue()
            return pd.DataFrame(self.record_emotive(no_of_seconds=no_of_seconds),
                                columns=channels_def)

        else:
            data = []
            self.reader.wanna_read(True)
            for _ in range(no_of_seconds * 128):
                data.append(self.record_eeg())
            self.reader.wanna_read(False)
            return pd.DataFrame(data, columns=channels_def)

# main test
import time
import csv
import os
def save(user_name,Data,label):
    'data in dataframe'
    # file = os.path.join(os.getcwd(), ) + user_name + '.csv'
    Data['Label'] = label
    pd.DataFrame(Data).to_csv(user_name+'.csv',header=False if os.path.isfile(user_name+'.csv') else True, index=False,mode='a')




if __name__ == '__main__':

    collect = Collect(False)
    start = time.perf_counter()

    print(collect.record(5))

    stop = time.perf_counter()
    print(stop - start)

    ##############################
    # start = time.perf_counter()

    # print(collect.record(10))
    # print('sleep .. 5 sec...')
    # time.sleep(5)
    # print('LOOK.')
    # for i in range(10):
    #     Data = collect.record(5)
    #     # print(Data[0])
    #     save(user_name='girgis_7.5(2)',Data=Data,label=i)
    #     print('break!')
    #     time.sleep(4)
    #     print('ready !')
    #     time.sleep(1)
    #     print('LOOK.')

    # Data = collect.record(1)
    # # print(Data[1])
    # save(user_name='girgis', Data=Data, label=20)

    # stop = time.perf_counter()
    # print(stop-start)

    # ##############################
    # time.sleep(4)
    # ##############################








#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

# from cykit.epoc_plus import EEG
# # from emokit3.emokit.emotiv import Emotiv
#
# class Collect:
#
#     def __init__(self,head_set=True):
#
#         self.head_set = head_set # True For Emotive, False EEG
#         if self.head_set == True:
#             self.Reader = Emotiv()
#         else :
#             self.Reader = EEG()
#
#
#     def Record_EEG(self):
#         # print(self.Reader.tasks.qsize())
#         return self.Reader.get_data().split(',')
#
#     def Record_Emotive(self):
#         pass
#
#     def get_single_sample(headset, index, data, quality):
#         '''
#         TODO:
#         packet = headset.dequeue()
#         while packet is None:
#         packet = headset.dequeue()
#         '''
#         while True:
#             packet = headset.dequeue()
#
#             # print(packet)
#             if packet is not None:
#                 data[0][index] = packet.sensors['O1']['value']
#                 data[1][index] = packet.sensors['O2']['value']
#                 data[2][index] = packet.sensors['P7']['value']
#                 data[3][index] = packet.sensors['P8']['value']
#
#                 quality[0][index] = packet.sensors['O1']['quality']
#                 quality[1][index] = packet.sensors['O2']['quality']
#                 quality[2][index] = packet.sensors['P7']['quality']
#                 quality[3][index] = packet.sensors['P8']['quality']
#                 break
#
#     def Record(self,no_of_seconds): # secs number
#         data = []
#         if self.head_set == True: # Emotive
#                 return self.Record_Emotive()
#         else :
#             for i in range(no_of_seconds * 128):
#                 data.append(self.Record_EEG())
#         return data
#
# import time
# if __name__ == '__main__':
#     collect=Collect(False)
#     time.sleep(3)
#
#     print(len(collect.Record(3)))