import os
import time

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

images = [os.path.join(os.getcwd() +'\\BCInterface\\assets\\',image) for image in ['up.png', 'right.png', 'left.png', 'back.png']]
arrow_path = os.path.join(os.getcwd() +'\\BCInterface\\assets\\','arrow.png')

class FlashingBox(QLabel):
  def __init__(self, freq, idx):
    super(FlashingBox, self).__init__()
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
    #print (f'frequ of box {self.freq} is {self.counter}')
    self.timer.stop()
    self.setStyleSheet("background-color: rgb(0, 0, 0)")

  def flashing(self):
    if self.flag:
       self.counter+=1
       self.setStyleSheet("background-color: rgb(0, 0, 0)")

    else:
        self.setStyleSheet("background-color: rgb(131, 238, 66)")

    self.flag = not self.flag




class movigArrow(QLabel):
    
    def __init__(self, parent, delay, seq, start_flash=False):
        super(movigArrow, self).__init__(parent)

        self.seq_idx = 0
        self.flag = True
        self.hide() == True
        self.location = [[170, 20], [170, 150], [1100, 20],[1100, 150]]# nzbtha m3 l freq
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
        self.timer = QTimer(self, interval=1000*delay)
        self.timer.timeout.connect(self.movigArrow)


    def movigArrow(self):
        if self.flag:
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
        self.timer.stop()
       
