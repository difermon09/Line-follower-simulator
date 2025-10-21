# Main window (warehouse) module. Draws the warehouse lines, creates the robot and
# the secondary status window, manages the movement timer and inter-component signals.

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from src.secondary_win import SecondaryWin
from src.robot import Robot

class MainWin(QWidget):
    def __init__(self, warehouse_list, wally_list): 
        super().__init__()
        self.__X_FinPpal_Origin = 250
        self.__Y_FinPpal_Origin = 250
        self.__X_FinPpal_Size = int(warehouse_list[0][0]) 
        self.__Y_FinPpal_Size = int(warehouse_list[0][1])
        self.__line_width = 4
        self.__lines_list = warehouse_list[1:]
        
        self.setFixedSize(self.__X_FinPpal_Size, self.__Y_FinPpal_Size)
        self.move(self.__X_FinPpal_Origin, self.__Y_FinPpal_Origin)
        self.setStyleSheet("background-color: grey;")
        
        self.__secWindow = SecondaryWin (self, wally_list[4])
        self.__secWindow.setWindowTitle('Dades robot')
        
        self.__robot = Robot(self, wally_list, self.__line_width)
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__robot.robot_move)
        self.__time = int(wally_list[3])
        self.__timer.start(self.__time)
        self.__data_list = [wally_list[2].upper(), int(wally_list[1][0]) - int(wally_list[0][0])//2, int(wally_list[1][1]) - int(wally_list[0][0])//2]
        self.__secWindow.update_secon_win_data (self.__data_list)
        self.__robot.SendData.connect(self.StopTimer)
        self.__secWindow.StateButton.connect(self.active_stop_robot)
        
        self.__secWindow.show()
    
    def paintEvent (self, e):
        FinPpal_painter = QPainter(self)
        FinPpal_painter.setPen(QPen(Qt.GlobalColor.black,self.__line_width))
        for i in range(len(self.__lines_list)):
            FinPpal_painter.drawLine(int(self.__lines_list[i][0]), int(self.__lines_list[i][1]), int(self.__lines_list[i][2]), int(self.__lines_list[i][3])) 
    
    def active_stop_robot(self, robot_state):
        if robot_state == 'Stopped':
            self.StopTimer ('Stopped')
        else:
            self.__timer.start(self.__time)
    
    def StopTimer(self, emitted_message):
        if emitted_message != 'Stopped' and emitted_message != 'Kill':
            self.__data_list = emitted_message.split()
            self.__secWindow.update_secon_win_data (self.__data_list)
        else:
            self.__timer.stop()
            if emitted_message == 'Kill':
                self.__secWindow.active_pause_button.clicked.disconnect()
                self.__secWindow.active_pause_button.setText('Finalitzat')
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            QApplication.instance().quit()
            
        elif event.key() == Qt.Key.Key_F:
            self.__secWindow.show()
        else:
            super().keyPressEvent(event)