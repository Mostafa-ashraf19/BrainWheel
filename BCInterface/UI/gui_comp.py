import os
import time

from PyQt5.QtCore import QTimer,Qt
from PyQt5.QtGui import QPixmap

from PyQt5.QtGui import QPainter, QBrush, QFont, QPen, QColor, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QMessageBox

images = [os.path.join(os.getcwd() +'\\BCInterface\\assets\\',image) for image in ['up.png', 'back.png', 'left.png', 'right.png']]
arrow_path = os.path.join(os.getcwd() +'\\BCInterface\\assets\\','arrow.png')

fig_loaction = [(0,0),(220,0),(0,70),(220,70)]

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
        self.label1.setPixmap(QPixmap(images[idx]).scaled(100, 100))

        x,y = fig_loaction[idx]
        self.label1.move(x,y)

        self.counter = 0

    def startFlashing(self):
        delay = int(1000 / (2 * self.freq))  # in mSec
        self._timer = self.startTimer(delay, Qt.PreciseTimer)

    def stopFlashing(self):
        self.flag = 0
        if self._timer:
            self.killTimer(self._timer)
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
        self.location = [[660, 160], [150, 20], [150, 270], [1150, 20], [1150, 270]]# nzbtha m3 l freq
        self.sequence = seq

        # state initial position of green flag if flashing is first 
        if start_flash:
            self.flag = False
            self.move(*self.location[0])
            self.location_index = self.sequence[0]
            self.move(*self.location[self.location_index])
            self.show()==True

        self.setPixmap(QPixmap(arrow_path))

        # set timer for moving flag to recognize current frequency 
        #self.timer = QTimer(self, interval=1000*delay)
        #self.timer.timeout.connect(self.movigArrow)


    def movigArrow(self):
        if  self.flag:
            self.location_index = self.sequence[self.seq_idx]
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
       
