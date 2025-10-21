# Line sensor helper. Samples a pixel from the warehouse widget under a sensor offset
# and returns whether the sampled pixel corresponds to a line (black) or background.

from PyQt6.QtGui import *
from PyQt6.QtCore import *

class Sensor:
    def __init__(self,magatzem,dx,dy):
        self.__magatzem=magatzem  
        self.__dx=dx
        self.__dy=dy

    def Valor(self,x,y):
        pixMap=QPixmap(1,1)
        self.__magatzem.render(pixMap,QPoint(0,0),QRegion(self.__dx+x,self.__dy+y,1,1))
        image=pixMap.toImage() 
        color=image.pixelColor(0,0) 
        
        if color.red()==0: 
            return "1"      # over line
        else:
            return "0"      # light background
