# Secondary UI window module. Loads the .ui file, displays robot direction/coordinates
# and the program, and provides controls to pause/resume the robot.

from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class SecondaryWin(QWidget):
    StateButton = pyqtSignal(str)
    def __init__(self, mother, program):
        super().__init__(mother)
        uic.loadUi("Practica_4_4_pixels_por_4\resources\secondary_win.ui",self)
        self.move(780,280)
        f=self.windowFlags()
        self.setWindowFlags(f|Qt.WindowType.Window)
        self.__button_state = 'Active'
        self.active_pause_button.clicked.connect(self.active_stop_button)
        self.__wally_program = program
        self.program_label.setText('Programa')
        self.str_program()
    
    def update_secon_win_data (self, text):
        self.direc_label.setText('Direcció: ' + text[0])
        self.x_y_label.setText(f'({text[1]} , {text[2]})')
    
    def active_stop_button (self):
        if self.__button_state == 'Active':
            self.__button_state = 'Stopped'
            self.StateButton.emit(self.__button_state)
            self.active_pause_button.setText('Activar')
        else:
            self.__button_state = 'Active'
            self.StateButton.emit(self.__button_state)
            self.active_pause_button.setText('Parar')
    
    def str_program (self):
        self.__string_program = ''
        for word in self.__wally_program:
            self.__string_program += f'{word} '
        self.program_lineEdit.setText(self.__string_program)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            QApplication.instance().quit()
        else:
            super().keyPressEvent(event)