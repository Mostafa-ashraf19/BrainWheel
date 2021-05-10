import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget # it's a base class of all user insterface objects in PyQt 
from PyQt5.uic import loadUiType 
from os import path
import sys
from exp_senario2 import expScenario
 

OUR_UI= loadUiType(path.join(path.dirname(__file__),'MainLayout.ui'))[0]
# return tuple of child and base class  

class OurAPP(QWidget,OUR_UI):
    def __init__(self,parent=None):
        super(OurAPP,self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.RecordButton_Handling()
        self.back_handling()
        self.initiators()
        self.sc1= expScenario()
        self.stacklayout.insertWidget(1,self.sc1)

    def RecordButton_Handling(self):
        self.RecordButton.clicked.connect(lambda : self.stacklayout.setCurrentIndex(1))

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
    main()
    # print(OUR_UI)
