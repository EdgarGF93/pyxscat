
from PyQt5.QtWidgets import QApplication
from pyxscat.gui.gui_window import GUIPyX_Window
import sys
# Open the GUI

def run():
    app = QApplication(sys.argv)
    main_window = GUIPyXMWindow()
    main_window.show()
    app.exec_()