
from PyQt5.QtWidgets import QApplication
from modules_qt.gui_window import GUIPyX_Window
import sys
# Open the GUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = GUIPyX_Window()
    main_window.show()
    app.exec_()