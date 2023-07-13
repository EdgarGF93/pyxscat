from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
from . import GUI_PATH


class AboutForm(QWidget):

    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self._build()
        self.setWindowTitle("About PyXScat")
        app_icon = QIcon()
        icon_path = str(GUI_PATH.joinpath("pyxscat_icon.png"))
        app_icon.addFile(icon_path, QSize(256,256))
        self.setWindowIcon(app_icon)

    def _build(self):
        # Build the global widget, which is a Grid
        self.gridlayout = QGridLayout()
        self.setLayout(self.gridlayout)
        self.gridlayout.setRowStretch(1,1)
        self.gridlayout.setRowStretch(2,1)
        self.about_label_1 = QLabel("PyXScat version alpha")
        self.about_label_2 = QLabel("Contact to Edgar Gutierrez Fernandez")
        self.about_label_3 = QLabel("edgar.gutierrez-fernandez@esrf.fr")
        self.about_label_4 = QLabel("XMaS (BM28) - The European Synchrotron")
        self.about_label_5 = QLabel("")
        self.about_label_5.setText('<a href="http://xmas.ac.uk/">XMaS beamline webpage</a>')
        self.about_label_5.setOpenExternalLinks(True)
        self.about_label_6 = QLabel("")
        xmas_logo_path = str(GUI_PATH.joinpath('xmas_logo.png'))
        self.about_icon = QPixmap(xmas_logo_path)
        self.about_label_6.setPixmap(self.about_icon)
        self.gridlayout.addWidget(self.about_label_1,1,1)
        self.gridlayout.addWidget(self.about_label_2,2,1)
        self.gridlayout.addWidget(self.about_label_3,3,1)
        self.gridlayout.addWidget(self.about_label_4,4,1)
        self.gridlayout.addWidget(self.about_label_5,5,1)
        self.gridlayout.addWidget(self.about_label_6,6,1)
