import os
import time

from PyQt5.QtCore import QTimer,Qt
from PyQt5.QtGui import QPixmap

from PyQt5.QtGui import QPainter, QBrush, QFont, QPen, QColor, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QMessageBox

images = [os.path.join(os.getcwd() +'\\BCInterface\\assets\\',image) for image in ['up.png', 'right.png', 'left.png', 'back.png']]
arrow_path = os.path.join(os.getcwd() +'\\BCInterface\\assets\\','arrow.png')


fig_loaction = [(0,0),(0,200),(340,0),(340,200)]


class FlashingBox2(QLabel):
  def __init__(self, freq, idx):
    super(FlashingBox2, self).__init__()
    self.flag = True
    self.idx = idx
    self.timer = QTimer(self, interval=int(1000/(2 * freq)))
    self.timer.timeout.connect(self.flashing)
    image = QPixmap(images[self.idx])
    self.setPixmap(image.scaled(200,200))
    self.setScaledContents(1)
    self.counter = 0

  def startFlashing(self):
    self.timer.start()

  def stopFlashing(self):
    print (f'the counter {self.counter}')
    self.timer.stop()
    self.setStyleSheet("background-color: rgb(0, 0, 0)")

  def flashing(self):
    if self.flag:
       self.counter += 1
       self.setStyleSheet("background-color: rgb(0, 0, 0)")

    else:
        self.setStyleSheet("background-color: rgb(131, 238, 66)")

    self.flag = not self.flag



class FlashingBox(QLabel):

    def __init__(self, freq, idx):
        super(FlashingBox, self).__init__()
        self.flag = 0
        self.idx = idx
        self.freq = freq
        self.brushes = [QBrush(QColor(0, 0, 0)), QBrush(QColor(131, 238, 66))]


        # adding images


        self.label1 = QLabel(self)
        self.label1.setStyleSheet("background-color:  rgba(0,0,0,0%)")
        self.label1.setPixmap(QPixmap(images[idx]).scaled(120, 120))
        #self.label1.setScaledContents(1)
        x,y = fig_loaction[idx]
        self.label1.move(x,y)

        #image = QPixmap(images[self.idx])
        #self.setPixmap(image.scaled(200,200))
        #self.label1.setScaledContents(1)
        #self.setScaledContents(1)
        self.counter = 0

    def startFlashing(self):
        delay = int(1000 / (2 * self.freq))  # in mSec
        self._timer = self.startTimer(delay, Qt.PreciseTimer)

    def stopFlashing(self):
        self.flag = 0
        if self._timer:
            self.killTimer(self._timer)
        #print(f'counter is {self.counter}')
        #self.counter = 0
        self._timer = None
        self.update()

    def timerEvent(self, event):
        self.counter += 1
        self.flag = (self.flag + 1) % 2
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), self.brushes[self.flag])



class movigArrow(QLabel):
    
    def __init__(self, parent, delay, seq, start_flash=False):
        super(movigArrow, self).__init__(parent)

        self.seq_idx = 0
        self.flag = True
        self.hide() == True
        self.location = [[170, 20], [170, 150], [1400, 20],[1400, 150]]# nzbtha m3 l freq
        self.sequence = seq

        # state initial position of green flag if flashing is first 
        if start_flash:
            self.flag = False
            self.move(*self.location[0])
            self.location_index = self.sequence[0]-1
            self.move(*self.location[self.location_index])
            self.show()==True

        self.setPixmap(QPixmap(arrow_path))

        # set timer for moving flag to recognize current frequency 
        #self.timer = QTimer(self, interval=1000*delay)
        #self.timer.timeout.connect(self.movigArrow)


    def movigArrow(self):
        if  self.flag:
            self.location_index = self.sequence[self.seq_idx]-1
            self.show() == True
        else:
            self.seq_idx+=1
            self.hide() == True

        self.flag = not self.flag
        self.move(*self.location[self.location_index])
        self.update()

    def startMoving(self):
        self.timer.start()

    def stopMoving(self):
        self.hide()==True
        #self.timer.stop()
       
