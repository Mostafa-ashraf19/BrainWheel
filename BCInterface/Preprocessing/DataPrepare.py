import os
import pandas as pd
import csv
# from .files_manager import Filesmanager
# import Filesmanager
from .files_manager import Filesmanager
#
# def get_data(user_name):
#
#         # concat all files in one dataframe
#         # files = [os.path.join(os.getcwd(), 'Users\\') + user_name + '.csv' for user_name in users_list]
#         files = os.path.join(os.getcwd()+'\\') + user_name + '.csv'
#
#         return pd.read_csv(files, index_col=None, header=0)
#         # li = []
#
#         # for filename in files:
#         #     li.append(pd.read_csv(filename, index_col=None, header=0))
#         #
#         #
#         # frame_with_data = pd.concat(li, axis=0, ignore_index=True)
#         # return frame_with_data
#         # # get labels with index to extract each sample assigned with its label
#         # Get_labels_ind = frame_with_data.loc[frame_with_data.Label.notna()]['Label']
#         # labels = list(Get_labels_ind.values)
#         #
#         # print(frame_with_data)
#         # # extract trails and label them
#         # trails = []
#         # index_of_labels = list(Get_labels_ind.keys())
#         # for i in range(len(index_of_labels) - 1):
#         #     trails.append(
#         #         frame_with_data.drop(['Label'], axis=1).iloc[index_of_labels[i]:index_of_labels[i + 1]].T.to_numpy())
#         #
#         # trails.append(frame_with_data.drop(['Label'], axis=1).iloc[index_of_labels[-1]:].T#.to_numpy())
#         #



class DataPrepare:

    def __init__(self):
        """
        DataPreparare class offer
        1- get_dataFromFiles(files_paths:list, concate=False)
        2- Concate_frequanceis(Data,FreqS:list)
        3- Delete_File(File_Path)
        4- Trail_LabelSpliter(Data)
        """
        self.Manager = Filesmanager()
        # self.Manager = DataManager() # get_data(file_path) , delete_data(file_path)
        # self.DataFrames = {file_name : {'Data':pd.DataFrame() ,'begin':0 ,'size':0}} # Each file Data in a Data Frame
        pass

    def _Concate_Date(self,DataFramesList):
        if not isinstance(DataFramesList,list):
            raise AttributeError
        if not isinstance(DataFramesList[0],pd.DataFrame):
            raise AttributeError

        return pd.concat(DataFramesList, axis=0, ignore_index=True)

    def _get_dataFromFile(self,file_path):
        try:
            return self.Manager.get_data(file_path)
            # return self.Manager.get_data(file_path)
        except:
            raise FileNotFoundError


    def get_dataFromFiles(self, files_paths:list, concate=False):
        """
        input :  list of File_paths
        output : (Data frame) if concate is True or (list of Data frames) otherwise
        """
        if not isinstance(files_paths,list):
            raise AttributeError

        DataFramesList=list()
        for files_path in files_paths: # get all data in list of DataFrames
            # print(files_path)
            DataFramesList.append(self._get_dataFromFile(files_path))

        if concate:
            return self._Concate_Date(DataFramesList)

        return DataFramesList


    def _Concate_frequancy(self, Data, Freq):
        if not isinstance(Freq,str) and not isinstance(Freq,int) and not isinstance(Freq,float):
            raise AttributeError
        # -> get al the data Frames with (column Labels = Freq)

        return Data[Data['Label']==float(Freq)]



    def Concate_frequanceis(self, Data, FreqS:list):
        """
                input  : Data(Dataframe) , FreqS (list)
                output : Dataframe for the frequencies list
        """

        if not isinstance(FreqS,list):
            raise AttributeError
        DataFreq = list()
        for Freq in FreqS:
            DataFreq.append(self._Concate_frequancy(Data,Freq))
        return self._Concate_Date(DataFreq)


    def Delete_Example(self,Data,example_num):
        # save_file()
        # TODO

        pass

    def Delete_File(self,File_Path):
        """
        delete the file
        input  : File_Path

        """
        self.Manager.delete_file(File_Path)

    def Extraxt_trials(self,Data, Num_sec):
        trials = list()
        for i in range(0, Data.shape[0], 128 * Num_sec):
            # trials.append(Data.iloc[i:i + 128 * Num_sec, :-1])
            trials.append(Data.iloc[i:i + 128 * Num_sec, :])

        return trials

# if __name__ == '__main__':
#
#     prepare = DataPrepare()
#     data = prepare.get_dataFromFiles(['D:/Graduation Project/EEG-SSVEP-DataSet/5_S/U0000ai.csv'])
#     print(data)
    # def Trail_LabelSpliter(self,Data):
    #
    #     return Data.drop(['Label'], axis=1) ,Data['Label']

# unit test

# if __name__ == '__main__':
#     # Data_Prepare= DataPrepare()
#     #
#     # data = Data_Prepare.get_dataFromFiles(['User_2'],True)
#
#     # data = Data_Prepare.Concate_frequanceis(data,[10])
#     data = get_data('User_2')
#     channels_def = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']
#
#     for i in range(int(data.shape[0]/640)):
#         data.iloc[i*640:i*640+640, -1] = data.iloc[i*640, -1]
#
#     pd.DataFrame(data).to_csv('User_2Modified' + '.csv', header= True,
#                               index=False, mode='a')
#
#     print(data)

    # data.iloc[0:640, -1]= data.iloc[0,-1]
    # print(data.iloc[0:641,-1])
