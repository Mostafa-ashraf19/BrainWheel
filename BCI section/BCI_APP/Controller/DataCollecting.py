# import our BCI

class Collect:
    def __init__(self,UserName='',label_sq='',data_points=1,Flashing_time=2):
        self.UserName = UserName
        self.seq_list = label_sq.split(',')
        self.data_points = data_points
        self.Flashing_time = Flashing_time
        self.bci = '' #bci 





if __name__ == '__main__':
    collect = Collect()