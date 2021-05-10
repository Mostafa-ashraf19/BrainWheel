import os
from datetime import datetime
def Current_dt():
    current  = datetime.now()
    return current.strftime("%d/%m/%Y %H:%M:%S")

class Users:
    def __init__(self,UserName='',Headset_data=''):
        self.Headset_data = Headset_data
        self._Username = UserName

    def CreateUser(self):
        if not os.path.exists('Dataset/'+self._Username):
            os.makedirs('Dataset/'+self._Username)
            



if __name__ == '__main__':
    print(Current_dt())

              

