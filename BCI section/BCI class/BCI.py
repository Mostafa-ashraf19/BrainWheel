import csv
import os.path
import os
import numpy as np
import pandas as pd
from scipy import signal #for welch
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import PCA
from scipy.signal import butter, filtfilt

import matplotlib.pyplot as plt
import epoc_plus as eeg_reader

#highpass filter
def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a
def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y
# low pass filter
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a
def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

class BCI:

    def __init__(self):

        self.data = []
        #self.labels_sequence = labels_sequence

        self.cyHeadset = eeg_reader.EEG()
        #self.time_session = time_in_sec

        self.PCA = True
        self.COMMON_AVG_Noise = True
        self.pca = PCA(n_components=35)

        self.model = None
        #self.train= train

    def record_data(self):
        '''
            this function record data from headset or up load it from and show signals
        '''
        '''
            #TODO
            -Depend on GUI (take period)
            -save a file with all recored data

            CSV File Format:
                samples_time, Ch1, Ch2, Ch3, Ch4, Ch5, Ch6, Ch7, Ch8, Ch9, Ch10, Ch11, Ch12, Ch13, Ch14
                1, channels values...
                2, channels values...
                3, channels values...
                4, channels values...
                5, channels values...
                ......
        '''
        self.data.append(self.cyHeadset.get_data().split(','))

        #start = time.perf_counter()
        # print(cyHeadset.get_data().split(','))
        #stop = time.perf_counter()
        #print(stop - start)

    def save_data(self, user_name='user',label=1):
        '''
            save in Csv file

            input: 2d array , username
            ex:
            data = [['first', 'second', 'third', 'first321', 'second2', 'third12', 'first321', 'second2', 'third12', 'first321',
                            'second2', 'third12', 'first321', 'second2'],
                        ['first', 'second', 'third', 'first321', 'second2', 'third12', 'first321', 'second2', 'third12', 'first321',
                            'second2', 'third12', 'first321', 'second2']]
        '''
        self.data[0].append(label)

        file = os.path.join(os.getcwd(), 'Users\\') + user_name + '.csv'
        print(file)
        if os.path.isfile(file):
            with open(file, 'a', newline='') as f:
                writer = csv.writer(f)
                for i in self.data:
                    writer.writerow(i)
        else:
            pd.DataFrame(self.data).to_csv(file, header=['ch0', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'ch9','ch10', 'ch11', 'ch12', 'ch13','Label'], index=False)
        self.data = []


    def Extract_features(self,trails):
        '''
            this function takes
            input:  trails for users in 2D list
            output: features
        '''

        features = []
        for trail in trails:
            feature = []
            for feature_num in [5,6,7,8,9,13]: #[2, 3, 4, 6, 7, 8, 9, 11] 5?
                # [2,3,4,6,7,8,9,11] bad=[10,13,^1] [0,1,5]
                y = trail[feature_num]
                y = butter_lowpass_filter(y, 40, 128)
                y = butter_highpass_filter(y, 2, 128)
                channel7_welch = signal.welch(y, fs=128, nfft=640)
                feature.extend(
                    list(channel7_welch[1][31:36]) + list(channel7_welch[1][65:70]) + list(channel7_welch[1][98:103]) +
                    list(channel7_welch[1][35:40]) + list(channel7_welch[1][73:78]) + list(channel7_welch[1][111:116]) +
                    list(channel7_welch[1][41:46]) + list(channel7_welch[1][84:89]) + list(channel7_welch[1][127:132]) +
                    list(channel7_welch[1][48:53]) + list(channel7_welch[1][98:103]) + list(
                        list(channel7_welch[1][148:153]) +
                        list(channel7_welch[1][58:63]) + list(channel7_welch[1][118:123]) + list(
                            channel7_welch[1][178:183])))
            # feature.append(trail[-1])
            features.append(feature)
        return features

    def commen_avg_noise(self,trails_s):
        for i in range(len(trails_s)):
            trails_s[i] = trails_s[i] - np.mean(trails_s[i], axis=0)
        return trails_s

    def pipe_line(self):
        pass

    def signals_test(self, users_list=[], matrices=[], PCA=False, COMMON_AVG_Noise=False):

        self.PCA = PCA
        self.COMMON_AVG_Noise = COMMON_AVG_Noise
        # concat all files in one dataframe
        files = [os.path.join(os.getcwd(), 'Users\\') + user_name + '.csv' for user_name in users_list]
        li = []
        for filename in files:
            li.append(pd.read_csv(filename, index_col=None, header=0))
        frame_with_data = pd.concat(li, axis=0, ignore_index=True)
        # print (frame_with_data)

        # get labels with index to extract each sample assigned with its label
        Get_labels_ind = frame_with_data.loc[frame_with_data.Label.notna()]['Label']
        labels = list(Get_labels_ind.values)

        # extract trails and label them
        trails = []
        index_of_labels = list(Get_labels_ind.keys())
        for i in range(len(index_of_labels) - 1):
            trails.append(
                frame_with_data.drop(['Label'], axis=1).iloc[index_of_labels[i]:index_of_labels[i + 1]].T.to_numpy())
        trails.append(frame_with_data.drop(['Label'], axis=1).iloc[index_of_labels[-1]:].T.to_numpy())
        # print(trails[0], labels[0])
        # apply Common avg noise filter

        if COMMON_AVG_Noise == True:
            trails = self.commen_avg_noise(trails.copy())
        y = trails[0][6]
        # print(y)
        y = butter_lowpass_filter(y, 40, 128)
        y = butter_highpass_filter(y, 5, 128)
        channel7_welch = signal.welch(y, fs=128, nfft=256)
        plt.title('Frequency domain')
        plt.ylabel('Power')
        plt.xlabel('Frequency')
        plt.plot(channel7_welch[0], channel7_welch[1])
        plt.grid()
        plt.show()



        # X = self.Extract_features(trails)

    def train_data(self, users_list=[], matrices=[], PCA=True, COMMON_AVG_Noise=True):
        '''
            build the data -> common avarage -> pca ->  normalize -> train (gride search) -> evaluation

            input: data as a folder path for user or many users ,
            output: return model (optional) to show it's evaluation for list of matrices
        '''
        '''
                #TODO
                -read from the csvfile
                -get_all data in 2D array for each session
                -common avarage noies
                -pca
                -normalize
                -train (outomatic trianing)
                -return list of evaluation
        '''
        self.PCA = PCA
        self.COMMON_AVG_Noise = COMMON_AVG_Noise
        # concat all files in one dataframe
        files=[os.path.join(os.getcwd(), 'Users\\') + user_name + '.csv' for user_name in users_list]
        li = []
        for filename in files:
            li.append(pd.read_csv(filename, index_col=None, header=0))
        frame_with_data = pd.concat(li, axis=0, ignore_index=True)
        #print (frame_with_data)

        # get labels with index to extract each sample assigned with its label
        Get_labels_ind = frame_with_data.loc[frame_with_data.Label.notna()]['Label']
        labels = list(Get_labels_ind.values)

        # extract trails and label them
        trails = []
        index_of_labels = list(Get_labels_ind.keys())
        for i in range(len(index_of_labels) - 1):
            trails.append(frame_with_data.drop(['Label'], axis=1).iloc[index_of_labels[i]:index_of_labels[i + 1]].T.to_numpy())
        trails.append(frame_with_data.drop(['Label'], axis=1).iloc[index_of_labels[-1]:].T.to_numpy())
        # print(trails[0],labels[0])
        # apply Common avg noise filter
        if COMMON_AVG_Noise == True:
            trails = self.commen_avg_noise(trails.copy())

        X   = self.Extract_features(trails)

        lab_enc = preprocessing.LabelEncoder()
        encoded = lab_enc.fit_transform(labels)
        x_train, x_test, y_train, y_test = train_test_split(X, encoded, random_state=42, train_size=.7)

        #apply pca
        if PCA==True:
            self.pca.fit(x_train)
            x_train = pd.DataFrame(self.pca.transform(x_train))
            x_test = pd.DataFrame(self.pca.transform(x_test))
        else:
            x_train = pd.DataFrame(x_train)
            x_test  = pd.DataFrame(x_test)

        # Build Model
        # self.model = Pipeline([
        #     ("scaler", Normalizer(norm='l1')),
        #     ("svm_clf", SVC(kernel="poly", degree=3, coef0=1, gamma=.5, C=9))
        # ])

        self.model = Pipeline([
            ("scaler", Normalizer(norm='l1')),
            ("svm_clf", SVC(kernel="poly", degree=3, coef0=1, gamma=.5, C=20))
        ])

        self.model.fit(x_train, y_train)
        print(self.model.score(x_train, y_train))
        print(self.model.score(x_test, y_test))
        print('traing shape=',x_train.shape)
        print('testing shape=',x_test.shape)

        # from sklearn import metrics
        # # accuracy and confusion matrix
        # predicted = self.model.predict(x_test)
        # expected = y_test
        # print(expected)
        # print("Classification report for classifier %s:\n%s\n"
        #       % (self.model, metrics.classification_report(expected, predicted)))
        # print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))

        counts, bins = np.histogram(labels)
        plt.hist(bins[:-1], bins, weights=counts)

    def Prediction_realtime(self):
        pass
    def test_head_set(self):
        for i in range (128):
            self.record_data()
        self.save_data(user_name='test',label=0)

demo = BCI()
# demo.test_head_set()
#=['te','te1','te2','te3','te4','te5','te6','te7','te8']
# ['Girgis_4.1','Girgis_4.2','Girgis_4.3','Girgis_4.4','Girgis_4.5','Girgis_4.6']
# ['Girgis_2.1','Girgis_2.2','Girgis_2.4','Girgis_2.5','Girgis_2.6']
# ['Girgis_5.1','Girgis_5.2','Girgis_5.3','Girgis_5.4','Girgis_5.5','Girgis_5.6','Girgis_5.7','Girgis_5.8']
demo.train_data(users_list= ['Girgis_2.1','Girgis_2.2','Girgis_2.4','Girgis_2.5','Girgis_2.6','Girgis_2.7','Girgis_2.8','Girgis_2.9','Girgis_2.13','Girgis_2.11'], PCA=True, COMMON_AVG_Noise=True)
# demo.signals_test(users_list=['te_1'],PCA=True,COMMON_AVG_Noise=True)

