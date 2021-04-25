from PyQt5.QtWidgets import QOpenGLWidget,QLabel
import sys
from PyQt5.QtCore import Qt,QTimer
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from PyQt5.QtGui import QPainter, QBrush, QFont, QPen, QColor


class FlashingBox(QLabel):
  def __init__(self, freq=1, color=Qt.green):
    super(FlashingBox, self).__init__()
    self.freq = freq
    #self.brushes = [QBrush(Qt.black), QBrush(color)]
    self.index = 0
    self.enabled = False
    self.flag = True
    self.timer = QTimer(self, interval=int(1000/(2 * self.freq)))
    self.timer.timeout.connect(self.flashing)

  def setFreq(self, freq):
    self.freq = freq

  """def setColor(self, color):
          self.brushes[1] = QBrush(color)
      """
  """def timerEvent(self, event):
          if self.enabled:
            self.index = (self.index + 1) % 2
          else:
            self.index = 0
          self.update()"""

  """def paintEvent(self, event):
          painter = QPainter(self)
          painter.fillRect(event.rect(), self.brushes[self.index])"""

  def startFlashing(self):
    self.timer.start()
    #self.index = 0
    #self.enabled = True
    #delay = int(1000/(2 * self.freq))  #in mSec
    #self._timer = self.startTimer(delay, Qt.PreciseTimer)

  def stopFlashing(self):
    if self._timer:
      self.killTimer(self._timer)
    self._timer = None
    self.enabled=False
    self.index = 0
    self.update()

  def flashing(self):
    if self.flag:
      self.setStyleSheet('background-color: rgb(0, 0, 0); font-size: 40px')
    else:
      self.setStyleSheet('background-color: rgb(131, 238, 66); font-size: 40px')

    self.flag = not self.flag



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.init_gui()

    def init_gui(self):
        self.window = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout()
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)

        # 8iro f da
        self.box= FlashingBox(freq=7.5,color=Qt.green)


        self.box1 = FlashingBox(freq=2,color= Qt.black)
        self.box2 = FlashingBox(freq=2,color= Qt.black)



        self.layout.addWidget(self.box1, 0, 1)
        self.layout.addWidget(self.box2, 1, 0)

        self.layout.addWidget(self.box, 0, 0)


    def flash(self):
      self.timer=QTimer()
      self.timer.timeout.connect(self.box.stopFlashing)
      self.timer.start(3)



if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    win = MainWindow()
    win.setStyleSheet("background-color: rgb(0,0,0)")

    win.box.startFlashing()

    win.show()

    sys.exit(app.exec_())
