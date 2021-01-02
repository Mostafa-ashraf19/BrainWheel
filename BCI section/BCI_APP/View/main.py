"""

"""
import sys,os
sys.path.append(os.path.abspath(os.path.join('..', 'BCI')))
from  PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget # it's a base class of all user insterface objects in PyQt 
from PyQt5.uic import loadUiType 
from os import path
import sys
from Controller.DataCollecting import Collect

OUR_UI= loadUiType(path.join(path.dirname(__file__),'MainLayout.ui'))[0]
# return tuple of child and base class  

class OurAPP(QWidget,OUR_UI):
    def __init__(self,parent=None):
        super(OurAPP,self).__init__(parent)
        QWidget.__init__(self)
        self.dc = Collect()
        self.setupUi(self)
        self.TrainButton_Handling()
        self.back_handling()
        self.initiators()

    def TrainButton_Handling(self):
        self.TrainButton.clicked.connect(lambda : self.stacklayout.setCurrentIndex(1))

    def back_handling(self):
        self.BackButton.clicked.connect(lambda : self.stacklayout.setCurrentIndex(0))    

    def initiators(self):
        self.setWindowTitle('Data Processing-Train-Prediction APP')
        self.Username_le.setPlaceholderText('User Name')
        self.labelseq_le.setPlaceholderText('label seq e.g. 10,6.5,..')
        self.dp_le.setPlaceholderText('Data Points number')
        self.Tflash_le.setPlaceholderText('Flashing Time')
        
def main():
    app = QApplication(sys.argv)
    window = OurAPP()
    window.show()
    sys.exit(app.exec_()) # terminate system when window is terminated 

if __name__ == '__main__':
    # print(sys.path)
    main()
    # print(OUR_UI)
