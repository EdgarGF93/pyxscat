
from PyQt5.QtWidgets import QApplication
from pyxscat.gui.gui_mainwindow import GUIMainWindow
import sys

def main():
    app = QApplication(sys.argv)
    main_window = GUIMainWindow()
    main_window.show()
    app.exec_()


if __name__ == "__main__":
    sys.exit(main())