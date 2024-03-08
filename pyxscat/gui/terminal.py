

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from pyxscat.gui.terminallayout import TerminalLayout
import sys



class Terminal(TerminalLayout):
    pass





def main():
    app = QApplication(sys.argv)
    mw = QMainWindow()
    terminal = Terminal()
    mw.setCentralWidget(terminal)
    mw.show()
    app.exec_()

if __name__ == "__main__":
    main()