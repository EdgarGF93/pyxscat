
from PyQt5.QtWidgets import QApplication
from gui.gui_window import GUIPyX_Window
import sys
# Open the GUI

def run():
    app = QApplication(sys.argv)
    main_window = GUIPyX_Window()
    main_window.show()
    app.exec_()