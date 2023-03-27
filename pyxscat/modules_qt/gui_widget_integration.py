
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QGridLayout, QListWidget, QLabel, QLineEdit, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from os.path import join
from . import GLOBAL_PATH_QT


class GUIPyX_Widget_integrationform(QWidget):

    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self._build()
        self.setWindowTitle("Integration tool")
        app_icon = QIcon()
        app_icon.addFile(join(GLOBAL_PATH_QT, "pyxscat_icon.png"), QSize(256,256))
        self.setWindowIcon(app_icon)

    def _build(self):
        # Build the global widget, which is a Grid
        self.gridlayout = QGridLayout()
        self.setLayout(self.gridlayout)
        self.gridlayout.setRowStretch(1,1)
        self.gridlayout.setRowStretch(2,1)

        self.grid_up = QGridLayout()
        self.grid_down = QGridLayout()
        self.gridlayout.addLayout(self.grid_up,1,1)
        self.gridlayout.addLayout(self.grid_down,2,1)

        self.grid_up.setColumnStretch(1,2)
        self.grid_up.setColumnStretch(2,1)
        self.grid_azrad_left =QGridLayout()
        self.list_azrad = QListWidget()
        self.grid_down.setColumnStretch(1,2)
        self.grid_down.setColumnStretch(2,1)
        self.grid_proj_left =QGridLayout()
        self.list_proj = QListWidget()

        # Left grid of azrad
        self.grid_up.addLayout(self.grid_azrad_left,1,1)
        self.grid_up.addWidget(self.list_azrad,1,2)
        self.grid_down.addLayout(self.grid_proj_left,1,1)
        self.grid_down.addWidget(self.list_proj,1,2)

        self.grid_azrad_left.setRowStretch(1,1)
        self.grid_azrad_left.setRowStretch(2,5)
        self.grid_azrad_left.setRowStretch(3,1)
        self.grid_azrad_left.setRowStretch(4,1)
        self.label_title_azrad = QLabel("Integration type: azimuthal/radial")
        self.grid_azrad_input = QGridLayout()
        self.button_azrad_add = QPushButton("Add Integration")
        # self.button_azrad_check = QPushButton("Check")
        self.grid_azrad_left.addWidget(self.label_title_azrad,1,1)
        self.grid_azrad_left.addLayout(self.grid_azrad_input,2,1)
        self.grid_azrad_left.addWidget(self.button_azrad_add,3,1)
        # self.grid_azrad_left.addWidget(self.button_azrad_check,4,1)

        self.grid_azrad_input.setColumnStretch(1,1)
        self.grid_azrad_input.setColumnStretch(2,3)
        self.label_name_azrad = QLabel("Name:")
        self.lineedit_name_azrad = QLineEdit()
        self.label_suffix_azrad = QLabel("Suffix:")
        self.lineedit_suffix_azrad = QLineEdit()
        self.label_type_azrad = QLabel("Type:")
        self.combobox_type_azrad = QComboBox()
        self.combobox_type_azrad.addItem("Azimuthal")
        self.combobox_type_azrad.addItem("Radial")
        self.label_units_azrad = QLabel("Units:")
        self.combobox_units_azrad = QComboBox()
        self.combobox_units_azrad.addItem("q_nm^-1")
        self.combobox_units_azrad.addItem("q_A^-1")
        self.combobox_units_azrad.addItem("2th_deg")
        self.label_radial_azrad = QLabel("Radial range:")
        self.grid_radial_range = QGridLayout()
        self.label_azimuthal_azrad = QLabel("Azimuthal range:")
        self.grid_azimuthal_range = QGridLayout()
        self.label_azimuthalbins_azrad = QLabel("Azimuthal bins:")
        self.lineedit_azimuthal_bins = QLineEdit()
        self.grid_azrad_input.addWidget(self.label_name_azrad,1,1)
        self.grid_azrad_input.addWidget(self.lineedit_name_azrad,1,2)
        self.grid_azrad_input.addWidget(self.label_suffix_azrad,2,1)
        self.grid_azrad_input.addWidget(self.lineedit_suffix_azrad,2,2)
        self.grid_azrad_input.addWidget(self.label_type_azrad,3,1)
        self.grid_azrad_input.addWidget(self.combobox_type_azrad,3,2)
        self.grid_azrad_input.addWidget(self.label_units_azrad,4,1)
        self.grid_azrad_input.addWidget(self.combobox_units_azrad,4,2)
        self.grid_azrad_input.addWidget(self.label_radial_azrad,5,1)
        self.grid_azrad_input.addLayout(self.grid_radial_range,5,2)
        self.grid_azrad_input.addWidget(self.label_azimuthal_azrad,6,1)
        self.grid_azrad_input.addLayout(self.grid_azimuthal_range,6,2)
        self.grid_azrad_input.addWidget(self.label_azimuthalbins_azrad,7,1)
        self.grid_azrad_input.addWidget(self.lineedit_azimuthal_bins,7,2)

        self.grid_radial_range.setColumnStretch(1,1)
        self.grid_radial_range.setColumnStretch(2,4)
        self.grid_radial_range.setColumnStretch(3,1)
        self.grid_radial_range.setColumnStretch(4,4)
        self.grid_azimuthal_range.setColumnStretch(1,1)
        self.grid_azimuthal_range.setColumnStretch(2,4)
        self.grid_azimuthal_range.setColumnStretch(3,1)
        self.grid_azimuthal_range.setColumnStretch(4,4)

        self.label_minrad = QLabel("Min:")
        self.label_maxrad = QLabel("Max:")
        self.label_minaz = QLabel("Min:")
        self.label_maxaz = QLabel("Max:")
        self.lineedit_minrad = QLineEdit()
        self.lineedit_maxrad = QLineEdit()
        self.lineedit_minaz = QLineEdit()
        self.lineedit_maxaz = QLineEdit()
        self.grid_radial_range.addWidget(self.label_minrad,1,1)
        self.grid_radial_range.addWidget(self.lineedit_minrad,1,2)
        self.grid_radial_range.addWidget(self.label_maxrad,1,3)
        self.grid_radial_range.addWidget(self.lineedit_maxrad,1,4)
        self.grid_azimuthal_range.addWidget(self.label_minaz,1,1)
        self.grid_azimuthal_range.addWidget(self.lineedit_minaz,1,2)
        self.grid_azimuthal_range.addWidget(self.label_maxaz,1,3)
        self.grid_azimuthal_range.addWidget(self.lineedit_maxaz,1,4)

        # Left grid of projection
        self.grid_proj_left.setRowStretch(1,1)
        self.grid_proj_left.setRowStretch(2,5)
        self.grid_proj_left.setRowStretch(3,1)
        self.grid_proj_left.setRowStretch(4,1)
        self.label_title_proj = QLabel("Integration type: projection")
        self.grid_proj_input = QGridLayout()
        self.button_proj_add = QPushButton("Add Integration")
        # self.button_proj_check = QPushButton("Check")
        self.grid_proj_left.addWidget(self.label_title_proj,1,1)
        self.grid_proj_left.addLayout(self.grid_proj_input,2,1)
        self.grid_proj_left.addWidget(self.button_proj_add,3,1)
        # self.grid_proj_left.addWidget(self.button_proj_check,4,1)

        self.grid_proj_input.setColumnStretch(1,1)
        self.grid_proj_input.setColumnStretch(2,3)
        self.label_name_proj = QLabel("Name:")
        self.lineedit_name_proj = QLineEdit()
        self.label_suffix_proj = QLabel("Suffix:")
        self.lineedit_suffix_proj = QLineEdit()
        self.label_direction_proj = QLabel("Direction:")
        self.combobox_direction_proj = QComboBox()
        self.combobox_direction_proj.addItem("Horizontal")
        self.combobox_direction_proj.addItem("Vertical")
        self.label_input_units = QLabel("Input units:")
        self.combobox_input_units = QComboBox()
        self.combobox_input_units.addItem("q_nm^-1")
        self.combobox_input_units.addItem("q_A^-1")
        self.combobox_input_units.addItem("2th_deg")
        self.label_ip_range = QLabel("In-plane range:")
        self.grid_ip_range = QGridLayout()
        self.label_oop_range = QLabel("Out-of-plane range:")
        self.grid_oop_range = QGridLayout()

        self.label_output_units = QLabel("Output units:")
        self.combobox_output_units = QComboBox()
        self.combobox_output_units.addItem("q_nm^-1")
        self.combobox_output_units.addItem("q_A^-1")
        self.combobox_output_units.addItem("2th_deg")

        self.grid_proj_input.addWidget(self.label_name_proj,1,1)
        self.grid_proj_input.addWidget(self.lineedit_name_proj,1,2)
        self.grid_proj_input.addWidget(self.label_suffix_proj,2,1)
        self.grid_proj_input.addWidget(self.lineedit_suffix_proj,2,2)
        self.grid_proj_input.addWidget(self.label_direction_proj,3,1)
        self.grid_proj_input.addWidget(self.combobox_direction_proj,3,2)
        self.grid_proj_input.addWidget(self.label_input_units,4,1)
        self.grid_proj_input.addWidget(self.combobox_input_units,4,2)
        self.grid_proj_input.addWidget(self.label_ip_range,5,1)
        self.grid_proj_input.addLayout(self.grid_ip_range,5,2)
        self.grid_proj_input.addWidget(self.label_oop_range,6,1)
        self.grid_proj_input.addLayout(self.grid_oop_range,6,2)
        self.grid_proj_input.addWidget(self.label_output_units,7,1)
        self.grid_proj_input.addWidget(self.combobox_output_units,7,2)

        self.grid_ip_range.setColumnStretch(1,1)
        self.grid_ip_range.setColumnStretch(2,4)
        self.grid_ip_range.setColumnStretch(3,1)
        self.grid_ip_range.setColumnStretch(4,4)
        self.grid_oop_range.setColumnStretch(1,1)
        self.grid_oop_range.setColumnStretch(2,4)
        self.grid_oop_range.setColumnStretch(3,1)
        self.grid_oop_range.setColumnStretch(4,4)

        self.label_minip = QLabel("Min:")
        self.label_maxip = QLabel("Max:")
        self.label_minoop = QLabel("Min:")
        self.label_maxoop = QLabel("Max:")
        self.lineedit_minip = QLineEdit()
        self.lineedit_maxip = QLineEdit()
        self.lineedit_minoop = QLineEdit()
        self.lineedit_maxoop = QLineEdit()
        self.grid_ip_range.addWidget(self.label_minip,1,1)
        self.grid_ip_range.addWidget(self.lineedit_minip,1,2)
        self.grid_ip_range.addWidget(self.label_maxip,1,3)
        self.grid_ip_range.addWidget(self.lineedit_maxip,1,4)
        self.grid_oop_range.addWidget(self.label_minoop,1,1)
        self.grid_oop_range.addWidget(self.lineedit_minoop,1,2)
        self.grid_oop_range.addWidget(self.label_maxoop,1,3)
        self.grid_oop_range.addWidget(self.lineedit_maxoop,1,4)