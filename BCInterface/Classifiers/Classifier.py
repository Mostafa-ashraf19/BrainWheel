
class Classifier:
    @abstractmethod
    def __init__(self):
        raise

    @abstractmethod
    def Train(self):
        pass

    @abstractmethod
    def predict(self):
        pass

















import pandas as pd
import scipy.io
import numpy as np
import csv

for x in range(1, 35):
    # loading the data mat file
    file = scipy.io.loadmat('EEG\eeg_record' + str(x) + '.mat')  # change filename accordingly
    data = pd.DataFrame.from_dict(file["o"]["data"][0, 0])

    data = data.to_numpy()  # transform to numpy array
    new_data = data[:, 3:17]  # trancating the data of the sensors only from the array
    print(np.size(new_data, 0))
    print(np.size(new_data, 1))
    rows = new_data.shape[0]  # getting the number of rows
    # applying the car filter to the data by getting the mean and subtract it from all sensors data
    for i in range(0, rows):
        mean = new_data[i].mean()
        new_data[i] = new_data[i] - mean

    # removing the dc component by getting the mean of every sensor values and subtracting it from the sensor data
    new_data = new_data.T
    rows = new_data.shape[0]
    for i in range(0, rows):
        mean = new_data[i].mean()
        new_data[i] = new_data[i] - mean
    new_data = new_data.T
    # saving the result in csv file
    np.savetxt("data" + str(x) + ".csv", new_data, delimiter=",")