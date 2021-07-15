import datetime
import pandas as pd
import os
import glob


class Filesmanager:


    def __init__(self, seconds='5', user_name='', new_u=False):
        """
        The files manager class acts as a dataset manager, 
        responsible for saving data we got from the EEG headset, 
        return data for the given file name as a data frame, 
        and delete the file of bad data.  
        """
        self._new_U = new_u
        self._seconds = seconds

        #print(os.path.normpath(os.getcwd()))# + os.sep + os.pardir))
        self._dir_path = os.path.join(os.path.normpath(os.getcwd() + os.sep + os.pardir),
                                      'EEG-SSVEP-DataSet\\' + str(self._seconds)+'_S\\')

        self._last_u = self._last_user()
        self._file_name = 'U0000ai.csv' if self._last_u == False else self._next_U_num()


    def save(self, data):
        """
        save EEG data in given file name
        @Params data:df
        @Returns void
        """
        pd.DataFrame(data).to_csv(self._dir_path+self._file_name,
                                  mode='a', header=False  if os.path.isfile(self._dir_path+self._file_name) else True, index=False)

    def get_data(self, file_path: str):
        """
        Return data frame for the given file path.
        @Params file_path:str
        @Returns DataFrame
        """
        return pd.read_csv(file_path)
    def Get_userFiles(self, File_regexp, path_dir_):
        return glob.glob(path_dir_ + File_regexp)

    def _last_user(self):
        """
        Check last user in directory, return it as this template
        U{0-9999}{a-z}{i||ii} or False if dir is empty.
        @Params void
        @Return {str|False} 
        """
        file_template = 'U*.csv'
        files = glob.glob(self._dir_path + file_template)
        # print(self._dir_path)
        if len(files) == 0:
            return False
        max_file = max(files, key=os.path.getctime)
        # print('max=' , max_file)
        return max_file.split('\\')[-1]

    def _next_U_num(self):
        """
        Generate file name in dir
        @Params: void
        @Returns: str:filename
        """
        if self._new_U:
            object_num = str(int(self._last_u[1:5])+1)
            l = 4-len(object_num)
            name = 'U'+('0'*l)+object_num
            return name + 'ai.csv'
        else:

            object_num = str(int(self._last_u[1:5]))
            l = 4-len(object_num)
            name = 'U'+('0'*l)+object_num
            _chr = chr(ord(
                self._last_u[5])+1)+'i.csv' if self._last_u[6:] == 'ii.csv' else self._last_u[5]+'ii.csv'
            return name + _chr

    def delete_file(self, file_path):
        """
        Delete CSV file for given file path.
        @Params file_path:str
        @Returns void
        """
        os.remove(file_path)

#
# if __name__ == '__main__':
#
#     filesmanager = Filesmanager()
#     data = filesmanager.get_data('D:/Graduation Project/EEG-SSVEP-DataSet/5_S/U0000ai.csv')
#     filesmanager.save(data)
#
#     filesmanager.delete_file('D:/Graduation Project/EEG-SSVEP-DataSet/5_S/U0000aii.csv')
