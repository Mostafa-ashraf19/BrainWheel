from BCInterface.Helpers import helper

import pickle as pk
import pandas as pd
import numpy as np
from PyQt5.QtCore import QObject,pyqtSignal
from serial_send import SerialSender
Model_Name = 'Finalized_Model_model.sav'
Pca_Name = 'Finalized_PCA_model.sav'


class Process(QObject):
    """
        class description:
        applying the whole pipeline and passing of prediction to jetson
        pipeline:
            1. preprocessing of data (CAR-welch)
            2. feature extraction
            3. predict freq corresponding to the given data

        class methods
        1. _prepare_data:
        parameter: dataframe of data from headset
        return: feature vector
        function: data preparation and feature extraction

        2. _predict
        parameter: feature vector
        returns: prediction "flickering frequency of box"
        function: applying trained model on given data to figure out value of flickering frequency

        3. _send_to_jetson
        parameter: model prediction
        function: send model prediction through serial connection.

    """
    autonomus_signal = pyqtSignal(int)
    def __init__(self):
        super(Process, self).__init__()
        # print ('process is created')
        self.Model = pk.load(open(Model_Name, 'rb'))
        self.pca = pk.load(open(Pca_Name, 'rb'))
        # self.autonomus_signal.connect(self._send_to_jetson)
        # self.autonomus_signal.connect(self._ana_hena)
        # self.serial_sender = SerialSender()

    def _ana_hena(self, param):
        print("______________________ana henaaaaaa: ", param)


    def _predict(self, Feature):
        Feature = pd.DataFrame(self.pca.transform(Feature))
        p = np.array(self.Model.decision_function(Feature))  # decision is a voting function
        prob = np.exp(p) / np.sum(np.exp(p), axis=1, keepdims=True)  # softmax after the voting
        print(prob)
        return self.Model.predict(Feature)

    def _prepare_data(self, Data):
        # print('main process')
        # print(Data)
        # applay car DF -> Df
        Data1 = helper.CAR(Data, train=False)
        # print('CAr',Data1)
        Data2 = helper.butter_band_filter(Data1, lowcut=5, highcut=60, FS=128, Order=5)
        # print('butter')
        # print(Data2)
        freq = helper.welch(Data2, train=False)

        Features = helper.featureExtraction_welch_real(freq, 3, ['P7', 'O1', 'O2', 'P8'])
        # print(Data)
        return Features

    def _send_to_jetson(self, prediction):
        # map prediction to characters
        print(f'predictio of the model {prediction }')
        char = {7.5: 'forward', 8.57: 'right', 10.0: 'left', 12.0: 'stop', 1:'auto'}
        # characters to bus

        SerialSender.send_inst(char[prediction])

    # preds = predict(x_train[:5], model)
    # print(preds)

    def make_process(self, Data):
        # print ('data is sent')
        freq = {0: 7.5, 1: 8.57, 2: 10.0, 3: 12.0}
        # print (Data)
        # access data then get feature
        Features = self._prepare_data(Data)

        # predict
        prediction = self._predict(Features)
        # results to serial
        self._send_to_jetson(freq[prediction[0]])


from BCInterface.Preprocessing.DataPrepare import DataPrepare
import glob

if __name__ == "__main__":
    number_sec = 5  # sellect example time
    path_dir_ = 'C:/Users/compuland/Documents/GitHub/BCI_interface/EEG-SSVEP-DataSet/mike/mike 2/'
    File_regexp = 'U0000[c|d|e|f]*.csv'
    prepare = DataPrepare()
    data = prepare.get_dataFromFiles(glob.glob(path_dir_ + File_regexp), concate=True)
    Labels = data['Label']  # .drop('Label',axis=1)

    Run_time = Process()

    example = 0
    print(data.iloc[example * 640:example * 640 + 640, :-1])
    Run_time.make_process(data.iloc[example * 640:example * 640 + 640, :-1])
