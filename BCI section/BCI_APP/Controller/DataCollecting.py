from enum import Enum
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'BCI')))
from Model.Users import Users

class CollectingMode(Enum):
    TRAIN = 0
    PREDCTION=1

class Collect:
    def __init__(self,UserName='',label_sqs='',data_points=1,Flashing_time=2,Mode=CollectingMode.TRAIN):
        # print("Hello from collect")
        self.UserName = UserName
        self.seq_list = label_sqs.split(',')
        self.data_points = data_points
        self.Flashing_time = Flashing_time
        self.user = Users(UserName)
        # self.bci = '' # bci 
        self.data = '' # retived data
        # thread start and data sharing here 

if __name__ == '__main__':
    # u = Users()
    # print(sys.path)
    # print(count)
    collect = Collect()
