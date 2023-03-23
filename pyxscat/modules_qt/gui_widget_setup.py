
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QGridLayout, QListWidget, QLabel, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from os.path import join
from . import GLOBAL_PATH_QT

class GUIPyX_Widget_setupform(QWidget):

    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self._build()
        self.setWindowTitle("Setup tool")
        app_icon = QIcon()
        app_icon.addFile(join(GLOBAL_PATH_QT, "pyxscat_icon.png"), QSize(256,256))
        self.setWindowIcon(app_icon)

    # def closeEvent(self, event):
    #     self.kk()
        

    def _build(self):
        # Build the global widget, which is a Grid
        self.gridlayout = QGridLayout()
        self.setLayout(self.gridlayout)
        self.gridlayout.setColumnStretch(1,1)
        self.gridlayout.setColumnStretch(2,1)

        self.grid_left = QGridLayout()
        self.list_setups = QListWidget()

        self.gridlayout.addLayout(self.grid_left,1,1)
        self.gridlayout.addWidget(self.list_setups,1,2)

        self.grid_left.setRowStretch(1,1)
        self.grid_left.setRowStretch(2,1)
        self.grid_input_setup = QGridLayout()
        self.button_input_setup = QPushButton("Add new setup")
        self.grid_left.addLayout(self.grid_input_setup,1,1)
        self.grid_left.addWidget(self.button_input_setup,2,1)

        self.grid_input_setup.setColumnStretch(1,1)
        self.grid_input_setup.setColumnStretch(2,1)
        self.grid_input_setup.setRowStretch(1,1)
        self.grid_input_setup.setRowStretch(2,1)
        self.grid_input_setup.setRowStretch(3,1)
        self.grid_input_setup.setRowStretch(4,1)
        self.grid_input_setup.setRowStretch(5,1)

        self.label_setup = QLabel("Setup name:")
        self.label_incidentangle = QLabel("Motor - Incident angle:")
        self.label_tilttangle = QLabel("Motor - Tilt angle:")
        self.label_normfactor = QLabel("Counter - Norm. factor:")
        self.label_exposure = QLabel("Counter - Exposition time:")
        self.lineedit_setup = QLineEdit()
        self.lineedit_incidentangle = QLineEdit()
        self.lineedit_tiltangle = QLineEdit()
        self.lineedit_normfactor = QLineEdit()
        self.lineedit_exposure = QLineEdit()
        self.grid_input_setup.addWidget(self.label_setup,1,1)
        self.grid_input_setup.addWidget(self.lineedit_setup,1,2)
        self.grid_input_setup.addWidget(self.label_incidentangle,2,1)
        self.grid_input_setup.addWidget(self.lineedit_incidentangle,2,2)
        self.grid_input_setup.addWidget(self.label_tilttangle,3,1)
        self.grid_input_setup.addWidget(self.lineedit_tiltangle,3,2)
        self.grid_input_setup.addWidget(self.label_normfactor,4,1)
        self.grid_input_setup.addWidget(self.lineedit_normfactor,4,2)
        self.grid_input_setup.addWidget(self.label_exposure,5,1)
        self.grid_input_setup.addWidget(self.lineedit_exposure,5,2)