"""

"""
import datetime
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QWidget
from UI.count_down import CountDown
from UI.exp_senario2 import expScenario
import sys
from os import path
# it's a base class of all user insterface objects in PyQt
from PyQt5.QtWidgets import QApplication
import os
import datetime
import sys

sys.path.append(os.path.abspath(os.path.join('..', 'BCI-Tool')))

# return tuple of child and base class
OUR_UI = loadUiType(path.join(path.dirname(__file__), 'UI/MainLayout.ui'))[0]


class MainWindow_(QWidget, OUR_UI):
    def __init__(self, parent=None):
        super(MainWindow_, self).__init__(parent)
        QWidget.__init__(self)

        self.setupUi(self)
        self.sc1 = expScenario()
        self.initiators()

    def StartSession(self):
        user_name = str(self.Username_le.text())
        ftime = int(self.Tflash_le.text())
        if not os.path.exists(os.path.join(os.path.abspath(
                'DataSet'), user_name+'-'+str(datetime.datetime.now()).split(' ')[0])):

            path = os.path.join(os.path.abspath(
                'DataSet'), user_name+'-'+str(datetime.datetime.now()).split(' ')[0])

            os.makedirs(path)

        if not os.path.exists(os.path.join(os.path.abspath(
                'DataSet'), user_name+'-'+str(datetime.datetime.now()).split(' ')[0]) + '/' + user_name + '-' + str(ftime) + '-seconds'):

            path = os.path.join(os.path.abspath(
                'DataSet'), user_name+'-'+str(datetime.datetime.now()).split(' ')[0]) + '/' + user_name + '-' + str(ftime) + '-seconds'

            os.makedirs(path)

        m = CountDown(timeout=5, username=user_name)
        m.show()
        self.stacklayout.setCurrentIndex(1)
        self.sc1.init_session()

    def initiators(self):
        self.setWindowTitle('Data Processing-Train-Prediction APP')
        self.Username_le.setPlaceholderText('User Name')
        self.labelseq_le.setPlaceholderText('label seq e.g. 10,6.5,..')
        self.dp_le.setPlaceholderText('Data Points number')
        self.Tflash_le.setPlaceholderText('Flashing Time')

        self.RecordButton.clicked.connect(lambda: self.StartSession())
        self.BackButton.clicked.connect(
            lambda: self.stacklayout.setCurrentIndex(0))

        self.stacklayout.insertWidget(1, self.sc1)


def main():
    app = QApplication(sys.argv)
    window = MainWindow_()
    window.show()
    # terminate system when window is terminated
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
