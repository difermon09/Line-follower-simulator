# This is the application entry point. It reads configuration files from resources,
# creates the QApplication, instantiates the main window, and starts the event loop.

from PyQt6.QtWidgets import QApplication
from src.main_win import MainWin

def read_file (f):
    with open (f,'r') as file:
        file_list = [] 
        for file_line in file:
            if ' ' in file_line:
                file_list.append(file_line.strip().split())
            else:
                file_list.append(file_line.strip())
    return file_list



if __name__ == '__main__':
    magatzem_list = read_file('Practica_4_4_pixels_por_4\\resources\Magatzem.txt')
    robot_list = read_file('Practica_4_4_pixels_por_4\\resources\Robot.txt')
    app = QApplication([])
    window = MainWin(magatzem_list, robot_list)
    window.setWindowTitle('Pràctica 4. <Dídac Fernández>')
    window.show()
    app.exec()

'''
Recorreguts:
1: r e d d e d r d r r e e e t e e d d p
2: e d t r d d t d r r r d r d e d r e r d r p
'''