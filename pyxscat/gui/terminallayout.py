from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtWidgets import QPlainTextEdit, QHBoxLayout, QTabWidget

LABEL_TERMINAL = "Output Terminal"

class TerminalLayout(QWidget):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self._build()

    def _build(self):
        self.setGeometry(300, 300, 300, 200)
        hbox_main = QHBoxLayout()
        self.setLayout(hbox_main)

        widget_terminal_tab = QTabWidget()
        hbox_main.addWidget(widget_terminal_tab)   

        self.plaintext_output = QPlainTextEdit()
        self.plaintext_output.setReadOnly(True)
        widget_terminal_tab.addTab(self.plaintext_output, LABEL_TERMINAL)

        hbox_terminal_top = QHBoxLayout()
        widget_terminal_top = QWidget()
        widget_terminal_top.setLayout(hbox_terminal_top)