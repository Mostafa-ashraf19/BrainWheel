import os
import time

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import  QPixmap
from PyQt5.QtWidgets import QLabel

images = ['up.png', 'right.png', 'left.png', 'back.png']


class FlashingBox(QLabel):
  def __init__(self, freq, idx):
    super(FlashingBox, self).__init__()
    self.flag = True
    self.idx = idx
    self.timer = QTimer(self, interval=int(1000/(2 * freq)))
    self.timer.timeout.connect(self.flashing)
    #self.setStyleSheet(f"background-image: url({images[idx]}); background-repeat: no-repeat; background-position: center;background-color: rgb(0, 0, 0);Width : 50%")
    self.setStyleSheet("background-color: rgb(0, 0, 0)")

  def startFlashing(self):
    self.timer.start()

  def stopFlashing(self):
    self.timer.stop()
    #self.setStyleSheet(f"background-image: url({images[self.idx]}); background-repeat: no-repeat; background-position: center;background-color: rgb(0, 0, 0);Width : 50%")
    self.setStyleSheet("background-color: rgb(0, 0, 0)")

  def flashing(self):
    if self.flag:
      #self.setStyleSheet(f"background-image: url({images[self.idx]}); background-repeat: no-repeat; background-position: center;background-color: rgb(0, 0, 0)")
       self.setStyleSheet("background-color: rgb(0, 0, 0)")


    else:
      #self.setStyleSheet(f"background-image: url({images[self.idx]}); background-repeat: no-repeat; background-position: center;background-color: rgb(131, 238, 66)")
      self.setStyleSheet("background-color: rgb(131, 238, 66)")

    self.flag = not self.flag




class movigArrow(QLabel):
    
    def __init__(self,parent,delay,seq,start_flash=False):
        super(movigArrow, self).__init__(parent)

        self.seq_idx =0 
        self.flag = True
        self.hide() == True
        self.location = [[150, 20], [1100, 20], [150, 150], [1100, 150]]# nzbtha m3 l freq
        self.sequence = seq

        # state initial position of green flag if flashing is first 
        if start_flash:
            self.flag = False
            self.move(*self.location[0])
            self.location_index = self.sequence[0]-1
            self.move(*self.location[self.location_index])
            self.show()==True

        
        pixmap = QPixmap('star.png')
        self.setPixmap(pixmap)

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
       
