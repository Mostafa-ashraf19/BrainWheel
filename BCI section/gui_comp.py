from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QBrush, QFont, QPen, QColor, QPixmap

import time 

images = ['up.png','right.png','left.png','back.png']

class movigArrow(QLabel):

  def __init__(self,parent,delay):
    super(movigArrow,self).__init__(parent)
    self.index = 0
    self.resize(45,45)
    self.delay = delay
    self.location_index = 0
    self.label_visibility = 0
    self.location = [[210,220],[950,220],[590,450],[590,220],[590,0]]
    self.move(*self.location[0])
    pixmap = QPixmap("arrow3.png")
    self.setPixmap(pixmap)

  def timerEvent(self, event):
    #self.flashing_num+=1
    self.index = (self.index + 1) % 2
    if self.index == 0:
      self.show() == True
    else:
      self.hide() == True
    self.location_index = (self.location_index +1)%5
    self.move (*self.location[self.location_index]) 
    self.update()


  def startMoving(self):
    self._timer = self.startTimer( self.delay*1000, Qt.PreciseTimer)


  def stopMoving(self):
    self.killTimer(self._timer)
    self._timer = None
    self.update()


class FlashingBox(QLabel):
  
  def __init__(self,freq,idx): #parent,
    super(FlashingBox, self).__init__()#parent)
    self.freq = freq
    self.brushes = [QBrush(QColor(0, 0, 0)),QBrush(QColor(131, 238, 66))]
    self.index = 0
    self.resize(330, 240)
    self.label1 =  QLabel(self)
    self.label1.setStyleSheet("background-color:  rgba(0,0,0,0%)")
    self.label1.setPixmap(QPixmap(images[idx]).scaled(150, 150, Qt.KeepAspectRatio,Qt.SmoothTransformation))
    self.label1.move(120,45)                     

  def setFreq(self, freq):
    self.freq = freq


  def timerEvent(self, event):
    self.index = (self.index + 1) % 2
    self.update()


  def paintEvent(self, event):
    painter = QPainter(self)
    painter.fillRect(event.rect(), self.brushes[self.index])


  def startFlashing(self):
    delay = int(1000/(2 * self.freq))  #in mSec
    self._timer = self.startTimer(delay, Qt.PreciseTimer)


  def stopFlashing(self):
    self.index = 1
    self.killTimer(self._timer)
    self._timer = None
    self.update()

