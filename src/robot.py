# Robot widget module. Implements the robot representation, sensor handling,
# movement and rotation logic, and emits status signals to the main window.

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from src.line_sensor import Sensor

class Robot(QWidget):
    SendData = pyqtSignal(str)
    def __init__(self, parent, wally_list, line):
        super().__init__(parent)
        self.__width_line = line
        self.__wally_size = int(wally_list[0])
        self.__wally_X_origin = int(wally_list[1][0]) 
        self.__wally_Y_origin = int(wally_list[1][1]) 
        self.__X_witget_origin = self.__wally_X_origin - self.__wally_size//2-1
        self.__Y_witget_origin = self.__wally_Y_origin - self.__wally_size//2-1
        self.setGeometry(self.__X_witget_origin, self.__Y_witget_origin, self.__wally_size + 2, self.__wally_size + 2)
        
        self.__wally_direction = wally_list[2].upper()
        self.__wally_degrees = 0
        self.__wally_program = wally_list[4]
        
        self.__order = self.__wally_program[0].upper()
        self.__order_counter = 0
        self.__c = 1
        self.__values = ""
        
        self.__front_sensor_value = 0
        self.__rear_sensor_value = 0
        self.__right_sensor_value = 0
        self.__left_sensor_value = 0
        
        self.__X_north_sensor = 0
        self.__Y_north_sensor = -self.__width_line
        self.__north_sensor = Sensor(parent, self.__X_north_sensor, self.__Y_north_sensor)
        
        self.__X_est_sensor = self.__width_line
        self.__Y_est_sensor = 0
        self.__est_sensor = Sensor(parent, self.__X_est_sensor, self.__Y_est_sensor)
        
        self.__X_south_sensor = 0
        self.__Y_south_sensor = self.__width_line
        self.__south_sensor = Sensor(parent, self.__X_south_sensor, self.__Y_south_sensor)
        
        self.__X_west_sensor = -self.__width_line
        self.__Y_west_sensor = 0
        self.__west_sensor = Sensor(parent, self.__X_west_sensor, self.__Y_west_sensor)
        
        self.init_wally_degrees()
    
    def paintEvent(self, event):
        super().paintEvent(event)
        robot_painter = QPainter(self)
        for j in range(4):
            if j == 0: #de x derecha a x izquierda (abajo)
                if self.__wally_direction == 'S':
                    robot_painter.setPen(QPen(Qt.GlobalColor.red,2))
                else:
                    robot_painter.setPen(QPen(Qt.GlobalColor.black,2))
                robot_painter.drawLine(self.__wally_size + 1, self.__wally_size + 1, 1, self.__wally_size + 1) 
            
            elif j == 1: #de y abajo a y arriba (izquierda)
                if self.__wally_direction == 'O':
                    robot_painter.setPen(QPen(Qt.GlobalColor.red,2))
                    robot_painter.drawLine(1, self.__wally_size + 1, 1, 1)
                else:
                    robot_painter.setPen(QPen(Qt.GlobalColor.black,2))
                    robot_painter.drawLine(1, self.__wally_size - 1, 1, 1) 
            
            elif j == 2: #de x izquierda a x derecha (arriba)
                if self.__wally_direction == 'N':
                    robot_painter.setPen(QPen(Qt.GlobalColor.red,2))
                    robot_painter.drawLine(1, 1, self.__wally_size + 1, 1) 
                else:
                    robot_painter.setPen(QPen(Qt.GlobalColor.black, 2))
                    robot_painter.drawLine(3, 1, self.__wally_size + 1, 1) 
            
            else: #de y arriba a y abajo (derecha)
                if self.__wally_direction == 'E':
                    robot_painter.setPen(QPen(Qt.GlobalColor.red,2))
                    robot_painter.drawLine(self.__wally_size + 1, 1, self.__wally_size + 1, self.__wally_size + 1) 
                else:
                    robot_painter.setPen(QPen(Qt.GlobalColor.black,2))
                    robot_painter.drawLine(self.__wally_size + 1, 3, self.__wally_size + 1, self.__wally_size - 1)
    
    def robot_move (self):
        self.__values = self.__left_sensor_value + self.__front_sensor_value + self.__right_sensor_value
        if self.__values == "000" and self.__order == 'P':
            self.SendData.emit('Kill')
            
        else:
            if self.__values == "000" and self.__order == 'T':
                self.__order_counter += 1
                self.__order = self.__wally_program[self.__order_counter].upper()
                self.__wally_degrees += 180
            
            elif ((self.__values == "110" or self.__values == "111" or self.__values == "101") and self.__order == 'E' or self.__values == "100") and self.__c == 1:
                if (self.__values == "110" or self.__values == "111" or self.__values == "101") and self.__order == 'E':
                    self.__order_counter += 1
                    self.__order = self.__wally_program[self.__order_counter].upper()
                self.__c = 0
                self.__wally_degrees -= 90
            
            elif ((self.__values == "011" or self.__values == "111" or self.__values == "101") and self.__order == 'D' or self.__values == "001") and self.__c == 1:
                if (self.__values == "011" or self.__values == "111" or self.__values == "101") and self.__order == 'D':
                    self.__order_counter += 1
                    self.__order = self.__wally_program[self.__order_counter].upper()
                self.__wally_degrees += 90
                self.__c = 0
                
            elif ((self.__values == "110" or self.__values == "011"  or self.__values == "111") and self.__order == 'R') and self.__c == 1:
                self.__order_counter += 1
                self.__order = self.__wally_program[self.__order_counter].upper()
                self.__c = 0
                
            else:
                self.move_it()
                if self.__c != 1:
                    self.__c += 1
            
            self.wally_cardinal_point()
            self.SendData.emit(f'{self.__wally_direction} {self.__wally_X_origin} {self.__wally_Y_origin}')
        
    def move_it (self):
        if self.__wally_direction == 'N':
            self.__wally_Y_origin -= self.__width_line
        elif self.__wally_direction == 'S':
            self.__wally_Y_origin += self.__width_line
        elif self.__wally_direction == 'E':
            self.__wally_X_origin += self.__width_line
        else:
            self.__wally_X_origin -= self.__width_line
        self.__X_witget_origin = self.__wally_X_origin - self.__wally_size//2-1
        self.__Y_witget_origin = self.__wally_Y_origin - self.__wally_size//2-1
        self.move(self.__X_witget_origin, self.__Y_witget_origin)
    
    def init_wally_degrees (self):
        if self.__wally_direction == 'N':
            self.__wally_degrees = 0
            self.__front_sensor_value = self.__north_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
            self.__right_sensor_value = self.__est_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
            self.__left_sensor_value = self.__west_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
        
        elif self.__wally_direction == 'E':
            self.__wally_degrees = 90
            self.__front_sensor_value = self.__est_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
            self.__right_sensor_value = self.__south_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
            self.__left_sensor_value = self.__north_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
        
        elif self.__wally_direction == 'S':
            self.__wally_degrees = 180
            self.__front_sensor_value = self.__south_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
            self.__right_sensor_value = self.__west_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
            self.__left_sensor_value = self.__est_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
        else: 
            self.__wally_degrees = 270
            self.__front_sensor_value = self.__west_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
            self.__right_sensor_value = self.__north_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
            self.__left_sensor_value = self.__south_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
    
    def wally_cardinal_point (self):
        if self.__wally_degrees ==  0 or self.__wally_degrees == 360:
            self.__wally_degrees =  0
            self.__wally_direction = 'N'
            self.__front_sensor_value = self.__north_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
            self.__right_sensor_value = self.__est_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
            self.__left_sensor_value = self.__west_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
        
        elif self.__wally_degrees == 90 or self.__wally_degrees == 450:
            self.__wally_degrees =  90
            self.__wally_direction = 'E'
            self.__front_sensor_value = self.__est_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
            self.__right_sensor_value = self.__south_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
            self.__left_sensor_value = self.__north_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
        
        elif self.__wally_degrees == 270 or self.__wally_degrees == -90:
            self.__wally_degrees =  270
            self.__wally_direction = 'O'
            self.__front_sensor_value = self.__west_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
            self.__right_sensor_value = self.__north_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
            self.__left_sensor_value = self.__south_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
        else: 
            self.__wally_direction = 'S'
            self.__front_sensor_value = self.__south_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
            self.__right_sensor_value = self.__west_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
            self.__left_sensor_value = self.__est_sensor.Valor(self.__wally_X_origin, self.__wally_Y_origin)
