from BCInterface.Helpers import helper

import pickle as pk
import pandas as pd
import numpy as np

# from serial_send import SerialSender
Model_Name = 'Finalized_Model_model.sav'
Pca_Name = 'Finalized_PCA_model.sav'


class Process:
    '''
        this class responsible for BCI real time response
    '''

    def __init__(self):
        """
        - Load Pretrained Model & Pca
        - open serial communication with jetson
        """
        # print ('process is created')
        self.Model = pk.load(open(Model_Name, 'rb'))
        self.pca = pk.load(open(Pca_Name, 'rb'))
        # self.serial_sender = SerialSender()

    def _predict(self, Feature):
        """
        private function
            :param Feature: the Feature vector of the data
            :return: Model prediction
        """
        Feature = pd.DataFrame(self.pca.transform(Feature))
        p = np.array(self.Model.decision_function(Feature))  # decision is a voting function
        prob = np.exp(p) / np.sum(np.exp(p), axis=1, keepdims=True)  # softmax after the voting
        print(prob)
        return self.Model.predict(Feature)

    def _prepare_data(self, Data):
        """
        the function pass Real time Data through \
        signal processing pipeline (CAR -> Filter -> Welch -> Feature Extraction block)
            :param Data: data recorded by the head set in n seconds
            :return: Feature vector
        """
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
        """
        this function sends prediction to jetson due to serial communication port
            :param prediction: the prediction of the model
        """
        # map prediction to characters
        print(prediction)
        char = {7.5: 'forward', 8.57: 'right', 10.0: 'left', 12.0: 'stop'}
        # characters to bus
        # self.serial_sender.send_inst(char[prediction])

    # preds = predict(x_train[:5], model)
    # print(preds)

    def make_process(self, Data):
        """
        the interface function with the Gui
            :param Data: data recorded sent from GUi
            :return: prediction to Jetson
        """
        # print ('data is sent')
        freq = {0: 7.5, 1: 8.57, 2: 10.0, 3: 12.0}
        # print (Data)
        # access data then get feature
        Features = self._prepare_data(Data)

        # predict
        prediction = self._predict(Features)
        # results to serial
        self._send_to_jetson(freq[prediction[0]])


# from BCInterface.Preprocessing.DataPrepare import DataPrepare
# import glob
#
# if __name__ == "__main__":
#     number_sec = 5  # sellect example time
#     path_dir_ = 'C:/Users/compuland/Documents/GitHub/BCI_interface/EEG-SSVEP-DataSet/mike/mike 2/'
#     File_regexp = 'U0000[c|d|e|f]*.csv'
#     prepare = DataPrepare()
#     data = prepare.get_dataFromFiles(glob.glob(path_dir_ + File_regexp), concate=True)
#     Labels = data['Label']  # .drop('Label',axis=1)
#
#     Run_time = Process()
#
#     example = 0
#     print(data.iloc[example * 640:example * 640 + 640, :-1])
#     Run_time.make_process(data.iloc[example * 640:example * 640 + 640, :-1])
