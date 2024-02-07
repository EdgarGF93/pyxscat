

from PyQt5.QtWidgets import QWidget, QMainWindow, QHBoxLayout, QFrame, QVBoxLayout, QSplitter
from PyQt5.QtCore import Qt

from pyxscat.gui.browser import Browser
from pyxscat.gui.graph import Graph
from pyxscat.gui.terminal import Terminal

class GUILayout(QWidget):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self._build()
    
    def _build(self):
        hbox_main = QHBoxLayout()
        self.setLayout(hbox_main)
        splitter_main = QSplitter(orientation=Qt.Horizontal)
        hbox_main.addWidget(splitter_main)  

        vbox_browser = QVBoxLayout()
        frame_browser = QFrame(self)       
        frame_browser.setFrameShape(QFrame.StyledPanel)
        frame_browser.setLayout(vbox_browser)
        self.browser = Browser()
        vbox_browser.addWidget(self.browser)

        vbox_right = QVBoxLayout()
        frame_right = QFrame(self)       
        frame_right.setFrameShape(QFrame.StyledPanel)
        frame_right.setLayout(vbox_right)

        splitter_right = QSplitter(orientation=Qt.Vertical)
        vbox_right.addWidget(splitter_right)

        self.graphs =  Graph()
        self.terminal = Terminal()
        splitter_right.addWidget(self.graphs)
        splitter_right.addWidget(self.terminal)

        splitter_main.addWidget(frame_browser)
        splitter_main.addWidget(frame_right)

        splitter_main.setStretchFactor(0, 1)
        splitter_main.setStretchFactor(1, 3)