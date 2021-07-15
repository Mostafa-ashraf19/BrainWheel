from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox as MBox
from PyQt5.QtCore import QTimer


class CountDown:
    def __init__(self, timeout=5, username=''):
        self.timer = QTimer()
        self.username = username
        self.timeout = timeout
        self.ourmessage = MBox()
        self.ourmessage.setIcon(MBox.Question)
        self.ourmessage.setWindowTitle('Record DataSet of ' + self.username)
        self.ourmessage.setText(
            'Stay Ready '+self.username + ' Will Start After '+str(self.timeout))

        self.timer.timeout.connect(self.tick)
        self.timer.setInterval(1000)

    def tick(self):
        self.timeout -= 1
        if self.timeout >= 0:
            self.ourmessage.setText(
                'Stay Ready '+self.username + ' Will Start After '+str(self.timeout))
        else:
            self.timer.stop()
            self.ourmessage.done(1)

    def update(self):
        self.ourmessage.setText(str(self.timeout))

    def show(self):
        self.timer.start()
        self.ourmessage.exec_()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    m = CountDown(timeout=10)
    m.show()
    # print('Hello')
