from BCInterface.Preprocessing.DataPrepare import DataPrepare
from sklearn.decomposition import PCA
# from Helpers import helper
from BCInterface.Helpers import helper
from BCInterface.Headset.collect import Collect
# from ..BCInterface.BCInterface.Helpers.helpers import helper
from BCInterface.Preprocessing.DataPrepare import DataPrepare
from BCInterface.Preprocessing.files_manager import Filesmanager
from BCInterface.Visualization.Visualization import graphs



import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.decomposition import PCA

class Process:

    def __init__(self,Num_compunant=35):
        self.Num_compunant = Num_compunant

        self.DataPrepare = DataPrepare()
        self.pca = PCA(n_components=self.Num_compunant)
        self.model = None
        # self.collect = Collect(False) # False for cykit3 software

    def extract_Labels(self,Data,Num_sec):
        """
        Input: Df
        Return: Data, Labels :list, trial_index :list
        """
        labels= list()
        trial_index=list()
        for i in range(0,Data.shape[0],128*Num_sec):
            labels.append(Data.iloc[i, -1])
            trial_index.append(i)

        return labels , trial_index

    # def _Train_testData(self,Features,labels):

    # def Extraxt_feature(self,One_trail):
    def Extraxt_trials(self,Data,Num_sec):
        trials = list()
        for i in range(0, Data.shape[0], 128 * Num_sec):
            trials.append(Data.iloc[i:i+128 * Num_sec, :-1])
        return trials


    def encod_split(self, X, labels, train_size):
        lab_enc = preprocessing.LabelEncoder()
        encoded = lab_enc.fit_transform(labels)
        return train_test_split(X, encoded, random_state=0, train_size=train_size)

    def Make_process(self,Data_in,train=True):

        Data = Data_in

        # applay car DF -> Df
        Data = helper.CAR(Data)

        # applay Filter Df -> Df
        Data = helper.butter_band_filter(Data, lowcut=5, highcut=60, FS=128, Order=5)


        freq = helper.welch_file(Data, 5)
        # print(len(freq[0][0]))

        (Features ,Labels) = helper.featureExtraction_welch(freq, 3,['P7', 'O1', 'O2', 'P8', 'T8', 'AF4'])


        if train:
            return Features, Labels
        else:
            return Features
        # # applay Welch  Df -> list
        # # [[],[],[],[]...14],[],[]..125 trial (Num_trials, Num_channels,power_dim)
        # power = helper.welch_files(Data)
        # # [([]...[] * 14, label), ...([]...[] * 14, label)]
        # # extract features for each trail (num_of_trails, number_of_features)
        # Features ,Labels = helper.extract_features(power) # [ [ ([[],[],[],[],[],[]],[[],[],[],[],[],[],label)] , [], [], [] ]

        # [
        #     [features] trial1
        #     [features]
        #     [features]
        #     [features]
        #     [features]
        #     [features]
        # ]
        # labels =[label1,label2,.....]



        # TODO welch for all trails
        # TODO extraxtFeatures

        # TODO split
        # TODO Pca fit
        # TODO Train

    def train(self,Data_in): #,files=['User_2']):
        #Data in time domain
        Data = Data_in    #self.DataPrepare.get_dataFromFiles(files, True) # get Data from files

        Feature, Labels = self.Make_process(Data,train=True)  # list[ [[power],[power],[power],[power]], [[power],[power],[power],[power]] ]
        # print('labels',Feature[])

        x_train, x_test, y_train, y_test = self.encod_split(Feature, Labels,.8)

        self.pca.fit(x_train)
        x_train = pd.DataFrame(self.pca.transform(x_train))
        x_test  = pd.DataFrame(self.pca.transform(x_test))

        self.model = Pipeline([
            ("scaler", Normalizer(norm='l1')),
            ("svm_clf", SVC(kernel="poly", degree=3, coef0=1, gamma=.6, C=25))
        ])

        self.model.fit(x_train,y_train)

        print(self.model.score(x_train, y_train))
        print(self.model.score(x_test, y_test))
        print('traing shape=', x_train.shape)
        print('testing shape=', x_test.shape)

    def predict(self):
        Data  = self.collect.record(5)
        Feature = self.Make_process(Data,train=False) # [[],[]...]
        Feature = pd.DataFrame(self.pca.transform(Feature))
        return  self.model.predict(Feature)


if __name__ == '__main__':

    prepare =  DataPrepare()
    data = prepare.get_dataFromFiles(['D:/Graduation Project/EEG-SSVEP-DataSet/5_S/U0000ai.csv'], concate=True)

    process = Process()
    process.train(data)

    # col = Collect(True)
    # prepare = DataPrepare()
    # file_M = Filesmanager()
    # d = col.record(5)
    # file_M.save(d)
    #
    # data = prepare.get_dataFromFiles(['D:/Graduation Project/EEG-SSVEP-DataSet/5_S/U0000ai.csv'], concate=True)
    #
    # process = Process()
    # # process.train(['D:/Graduation Project/EEG-SSVEP-DataSet/5_S/U0000ai.csv'])
    # process.train(data)


    # prepare = DataPrepare()
    # data = prepare.get_dataFromFiles(['D:/Graduation Project/EEG-SSVEP-DataSet/5_S/U0000ai.csv'],concate=True)
    #
    # data = prepare.Extraxt_trials(data, 5)
    #
    # print(data[0])
    # graphs.time_vis(data[0])
    #
    # car = helper.CAR(data.copy())
    # # print(car)
    #
    #
    # filter = helper.butter_band_filter(car.copy(), 5, 40)
    # # print(filter)
    #
    # freq = helper.welch_file(filter,5)
    # print(freq[0][0])

    #
    # features = helper.featureExtraction_welch(freq, 2, ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4'])
    # print(len(features[0][0]))


    # graphs.time_vis(car)

    # print(prepare.Concate_frequanceis(data,FreqS=[10]))
        # get_dataFromFiles(['User_2'], True)
        # print(Data)



    #     Data
    #     Data = get_data()
    #     CAR()
    #     Band_pass()
    #     Welch()
    #     Extract_features()
    #
    #     pass
    #
    # def Train(self):
    #     Make_process()
    #     FitTRansform_PCA()
    #     Train()
    #     pass
    #
    # def Predict(self):
    #     Make_process()
    #     Fit_PCA()
    #     predict()
    #     pass

    #         Extract_features()
    # freq , power = helper.welch(Data)
    # print(power)

    #  # 2 lists
    # list_data = self.Extraxt_trials(Data, 5)
    #
    # print(list_data[0])
    # # trails = list_data.T
    # # print(trails)
    #
    # print(Data)

    # print(list_data[0].to_numpy())

    # print(list_data[0].to_numpy()[639])

    # freq , power= helper.welch(list_data[0])
    # print(len(power))

    # print(list_data[0])

    # print(Labels)
    # print(trial_index)

    '''
    Data = CAR(Data) # Df -> Df

    Data = Band_bass(Data) # Df ->

    pewer , freq = welch(Data) # 2D-list ->

    Features = Extraxt_features(pewer , freq) # list of lists of Features

    x_train, x_test, y_train, y_test = encod_split(Features , labels)

    Fit_pca(x_train)

    Train()
    '''

# process = Process()
# process.Make_process()
# def Extraxt_trials(Data,Num_sec):
#     trials = list()
#     for i in range(0, Data.shape[0], 128 * Num_sec):
#
#         trials.append(Data.iloc[i:i+128 * Num_sec, :-1])
#
#     return trials
import matplotlib.pyplot as plt