
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QGridLayout, QListWidget, QTableWidget, QLabel, QComboBox, QCheckBox, QLineEdit, QDoubleSpinBox, QPlainTextEdit, QTabWidget
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from silx.gui.plot.PlotWindow import Plot1D, Plot2D
from other.units import DICT_UNIT_ALIAS, CAKE_INTEGRATIONS, BOX_INTEGRATIONS
from . import GUI_PATH

# TABS
LABEL_TAB_FILES = "Folders and files"
LABEL_TAB_SETUP = "Setup information"
LABEL_TAB_CAKE = "Cake integration"
LABEL_TAB_BOX = "Box integration"

# INPUT FILE PARAMETERS
LABEL_INPUT_PARAMETERS = "====== Input File Parameters ======"
LABEL_RECENT_H5 = "Recent .h5 files:"
LABEL_H5_FILE = "Main directory:"
LABEL_EXTENSION = "File extension:"
LABEL_WILDCARDS = "Wildcards(*):"
LABEL_PONIFILE = "Ponifile:"
LABEL_REFERENCE_FOLDER = "Reference folder:"
LABEL_SAMPLE_ORIENTATION = "Sample orientation:"
BUTTON_QZ = "qz \u2191\u2191"
BUTTON_QR = "qr \u2191\u2191"
BUTTON_PONIFILE = "Pick new ponifile"
BUTTON_PYFAI_GUI = " pyFAI calibration GUI "
BUTTON_UPDATE_DATA = " Update data "
LIST_EXTENSION = [".edf", ".tiff"]
WILDCARDS_DEFAULT = "*"
ICON_FOLDER_PATH = "folder.png"
LABEL_PICK_MAINDIR = "Pick the directory container of data files."
ICON_H5_PATH = "hdf5.png"
LABEL_PICK_H5 = "Pick an .hdf5 file."
ICON_FILE_PATH = "file.png"
ICON_REFRESH_PATH = "refresh.png"
ICON_PYFAI_PATH = "pyfai.png"

# LIST OF FOLDERS
LABEL_LIST_FOLDERS = "====== List of folders ======"

# LIST OF FILES
LABEL_LIST_FILES = "====== List of files ======"
LABEL_METADATA = "Metadata:"

# LIVE BAR
LABEL_LIVE = "Live"

# SAVE_FOLDER BAR
LABEL_SAVE_FOLDER = "Save folder:"

# OUTPUT TERMINAL
LABEL_TERMINAL = "====== Output terminal ======"
BUTTON_HIDE_TERMINAL = "HIDE TERMINAL"

# 2D MAP
LABEL_2D_MAP = "====== 2D Map Parameters ======"
BUTTON_LOG = "LOG"
BUTTON_COLORBAR = "COLORBAR OFF"
BUTTON_AUTO = "AUTO LIMITS ON"
BUTTON_SHOW_QMAP = "SHOW Q-MAP"
BUTTON_SAVE_QMAP = "SAVE Q-MAP"
LABEL_MAP_TITLES = "Map titles:"
LABEL_MAP_UNITS = "Units for 2D map:"
LABEL_XLIMS = "x-lims:"
LABEL_YLIMS = "y-lims:"
LABEL_XTICKS = "x-ticks:"
LABEL_YTICKS = "y-ticks:"

# 1D CHART
LABEL_1D_CHART = "====== 1D Plot Parameters ======"
LABEL_SUB_FACTOR = "Subtraction scale factor (0.0 - 1.0):"
BUTTON_CLEAR_PLOT = "CLEAR PLOT"
BUTTON_SAVE_INTEGRATIONS = "SAVE INTEGRATIONS"
BUTTON_BATCH = "BATCH INTEGRATION & SAVE"
BUTTON_FITTING = "OPEN FITTING FORM"
LABEL_INTEGRATIONS = "Integrations:"
LABEL_MASK = "Mask 2D map"
STEP_SUB_SPINBOX = 0.01

# SETUP INFORMATION TAB
LABEL_DICT_SETUP = "Choose a setup dictionary:"
BUTTON_PICK_JSON = "Pick a .json file"
LABEL_IANGLE = "Motor - Incident angle:"
LABEL_TILTANGLE = "Motor - Tilt angle:"
LABEL_NORMFACTOR = "Counter - Norm. factor:"
LABEL_EXPOSURE = "Counter - Exposition time:"
LABEL_SETUP_NAME = "Setup name:"
BUTTON_JSON_FILE = "Save .json file"
ICON_SAVE_PATH = "save.png"
BUTTON_UPDATE_KEYS = "UPDATE METADATA KEYS TO .H5 FILE"

# CAKE TAB
LABEL_CAKE_NAME = "Name of file:"
LABEL_CAKE_SUFFIX = "Suffix:"
LABEL_CAKE_TYPE = "Type:"
LABEL_CAKE_UNITS = "Units:"
LABEL_CAKE_RADIAL = "Radial range:"
LABEL_CAKE_AZIM = "Azimuthal range:"
LABEL_CAKE_BINS = "Azimuthal bins:"
LABEL_MIN = "Min:"
LABEL_MAX = "Max."

# BOX TAB
LABEL_BOX_NAME = "Name of file:"
LABEL_BOX_SUFFIX = "Suffix:"
LABEL_BOX_DIRECTION = "Direction:"
LABEL_BOX_INPUT_UNITS = "Input units:"
LABEL_BOX_IP_RANGE = "In-plane range:"
LABEL_BOX_OOP_RANGE = "Out-of-plane range:"
LABEL_BOX_OUTPUT_UNITS = "Output units:"

STEP_INTEGRATION_SPINBOX = 0.5
STEP_BINS_SPINBOX = 1
SPINBOX_BINS_MIN = 0
SPINBOX_BINS_MAX = 1E9
SPINBOX_RANGE_MIN = -100
SPINBOX_RANGE_MAX = 100
ERROR_OUTPUT = "Something went wrong with the output message..."
button_on = """

QPushButton {
    font-weight: bold;
    color : white;
    background-color: #009150;
    border-width: 2px;
    border-radius: 3px;
    padding : 5px;
    }
QPushButton:hover  {
    font-weight: bold;
    color : white;
    background-color: #3cb371;
    border-width: 2px;
    border-radius: 3px;
    padding : 5px;
    }
QPushButton:pressed  {
    font-weight: bold;
    color : white;
    background-color: #93c572;
    border-width: 2px;
    border-radius: 3px;
    padding : 5px;
    }
"""
button_style_plot = """
QPushButton {
    font-weight: bold;
    color : white;
    background-color: #31659C;
    border-width: 2px;
    border-radius: 3px;
    padding : 10px;
    }
QPushButton:hover  {
    font-weight: bold;
    color : white;
    background-color: #639ACE;
    border-width: 2px;
    border-radius: 3px;
    padding : 10px;
    }
QPushButton:pressed  {
    font-weight: bold;
    color : white;
    background-color: #94BAE7;
    border-width: 2px;
    border-radius: 3px;
    padding : 10px;
    }
"""

button_style_thin = """
QPushButton {
    font-weight: bold;
    color : white;
    background-color: #31659C;
    border-width: 2px;
    border-radius: 3px;
    padding : 5px;
    }
QPushButton:hover  {
    font-weight: bold;
    color : white;
    background-color: #639ACE;
    border-width: 2px;
    border-radius: 3px;
    padding : 5px;
    }
QPushButton:pressed  {
    font-weight: bold;
    color : white;
    background-color: #94BAE7;
    border-width: 2px;
    border-radius: 3px;
    padding : 5px;
    }
"""

button_style_input = """
QPushButton {
    font-weight: bold;
    color : black;
    background-color: #bfe6ff;
    border-width: 2px;
    border-radius: 3px;
    padding : 5px;
    }
QPushButton:hover  {
    font-weight: bold;
    color : black;
    background-color: #BFCFCC;
    border-width: 2px;
    border-radius: 3px;
    padding : 5px;
    }
QPushButton:pressed  {
    font-weight: bold;
    color : black;
    background-color: #D6E4E1;
    border-width: 2px;
    border-radius: 3px;
    padding : 5px;
    }
"""

def set_bstyle(qlabels=[]):
    myFont=QFont("avenir.otf")
    myFont.setBold(True)
    for qlabel in qlabels:
        qlabel.setFont(myFont)


class GUIPyX_Widget_layout(QWidget):

    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self._build()

    def _write_output(self, cmd='Testing PyXScat...'):
        try:
            self.plaintext_output.appendPlainText(str(cmd))
        except:
            self.plaintext_output.appendPlainText(ERROR_OUTPUT)

    def _build(self):
        # Build the global widget, which is a Grid
        self.gridlayout = QGridLayout()
        self.setLayout(self.gridlayout)
        self.gridlayout.setColumnStretch(1,1)
        self.gridlayout.setColumnStretch(2,3)

        # Build the two main layouts, which are Grids
        self.grid_left = QGridLayout()
        self.grid_right = QGridLayout()
        self.gridlayout.addLayout(self.grid_left,1,1)
        self.gridlayout.addLayout(self.grid_right,1,2)

        self.grid_left.setRowStretch(1,6)
        self.grid_left.setRowStretch(2,1)
        self.grid_left.setRowStretch(3,9)
        self.grid_left.setRowStretch(4,1)
        self.grid_left.setRowStretch(5,1)
        self.grid_left.setRowStretch(6,9)

        self.grid_right.setRowStretch(1,1)
        self.grid_right.setRowStretch(2,1)
        self.grid_right.setRowStretch(3,20)
        self.grid_right.setRowStretch(4,1)
        self.grid_right.setRowStretch(5,4)

        self.grid_input_data = QGridLayout()
        self.widget_input_data = QWidget()
        self.grid_input_info = QGridLayout()
        self.widget_input_info = QWidget()
        self.grid_input_integration_cake = QGridLayout()
        self.widget_input_integration_cake = QWidget()
        self.grid_input_integration_box = QGridLayout()
        self.widget_input_integration_box = QWidget()

        self.tab_input_data = QTabWidget()
        self.tab_input_data.addTab(self.widget_input_data, LABEL_TAB_FILES)
        self.tab_input_data.addTab(self.widget_input_info, LABEL_TAB_SETUP)
        self.tab_input_data.addTab(self.widget_input_integration_cake, LABEL_TAB_CAKE)
        self.tab_input_data.addTab(self.widget_input_integration_box, LABEL_TAB_BOX)

        self.widget_input_data.setLayout(self.grid_input_data)
        self.widget_input_info.setLayout(self.grid_input_info)
        self.widget_input_integration_cake.setLayout(self.grid_input_integration_cake)
        self.widget_input_integration_box.setLayout(self.grid_input_integration_box)

        self.label_folders = QLabel(LABEL_LIST_FOLDERS)
        self.label_folders.setStyleSheet("background-color: white;border: 1px solid black;")
        self.label_folders.setAlignment(Qt.AlignCenter)
        self.label_files = QLabel(LABEL_LIST_FILES)
        self.label_files.setStyleSheet("background-color: white;border: 1px solid black;")
        self.label_files.setAlignment(Qt.AlignCenter)
        self.listwidget_folders = QListWidget()
        self.grid_input_files = QGridLayout()
        self.table_files = QTableWidget()
        self.grid_left.addWidget(self.tab_input_data,1,1)
        self.grid_left.addWidget(self.label_folders,2,1)
        self.grid_left.addWidget(self.listwidget_folders,3,1)
        self.grid_left.addWidget(self.label_files,4,1)
        self.grid_left.addLayout(self.grid_input_files,5,1)
        self.grid_left.addWidget(self.table_files,6,1)
        
        self.grid_live_title = QGridLayout()
        self.grid_save = QGridLayout()

        self.label_savefolder = QLabel(LABEL_SAVE_FOLDER)
        self.lineedit_savefolder = QLineEdit()

        self.grid_save.addWidget(self.label_savefolder,1,1)
        self.grid_save.addWidget(self.lineedit_savefolder,1,2)

        self.grid_input_and_graphs = QGridLayout()
        self.grid_label_terminal = QGridLayout()
        self.label_plaintext = QLabel(LABEL_TERMINAL)
        self.label_plaintext.setStyleSheet("background-color: white;border: 1px solid black;")
        self.label_plaintext.setAlignment(Qt.AlignCenter)
        self.button_hide_terminal = QPushButton(BUTTON_HIDE_TERMINAL)
        self.button_hide_terminal.setStyleSheet(button_on)
        self.grid_label_terminal.setColumnStretch(1,6)
        self.grid_label_terminal.setColumnStretch(1,1)
        self.grid_label_terminal.addWidget(self.label_plaintext, 1, 1)
        self.grid_label_terminal.addWidget(self.button_hide_terminal, 1, 2)

        self.plaintext_output = QPlainTextEdit()
        self.plaintext_output.setReadOnly(True)
        self.grid_right.addLayout(self.grid_live_title,1,1)
        self.grid_right.addLayout(self.grid_save,2,1)
        self.grid_right.addLayout(self.grid_input_and_graphs,3,1)
        self.grid_right.addLayout(self.grid_label_terminal,4,1)
        self.grid_right.addWidget(self.plaintext_output,5,1)

        #############################
        # GRID OF INPUT DATA
        #############################
        self.title_input = QLabel(LABEL_INPUT_PARAMETERS)
        self.title_input.setStyleSheet("background-color: white;border: 1px solid black;padding:4px;")
        self.title_input.setAlignment(Qt.AlignCenter)

        self.grid_input_setup = QGridLayout()
        self.grid_recent_h5 = QGridLayout()
        self.grid_input_maindir = QGridLayout()
        self.grid_input_conditions = QGridLayout()
        self.grid_input_ponifile = QGridLayout()
        self.grid_input_reference = QGridLayout()
        self.grid_input_orientations = QGridLayout()
        self.grid_input_buttons = QGridLayout()
        self.grid_input_data.addWidget(self.title_input,1,1)
        self.grid_input_data.addLayout(self.grid_recent_h5,2,1)
        self.grid_input_data.addLayout(self.grid_input_maindir,3,1)
        self.grid_input_data.addLayout(self.grid_input_conditions,4,1)
        self.grid_input_data.addLayout(self.grid_input_ponifile,5,1)
        self.grid_input_data.addLayout(self.grid_input_reference,6,1)
        self.grid_input_data.addLayout(self.grid_input_orientations,7,1)
        self.grid_input_data.addLayout(self.grid_input_buttons,8,1)
        self.grid_input_info.addLayout(self.grid_input_setup,1,1)

        self.grid_recent_h5.setColumnStretch(1,1)
        self.grid_recent_h5.setColumnStretch(2,15)
        self.grid_input_maindir.setColumnStretch(1,1)
        self.grid_input_maindir.setColumnStretch(2,15)
        self.grid_input_maindir.setColumnStretch(3,1)
        self.grid_input_conditions.setColumnStretch(1,1)
        self.grid_input_conditions.setColumnStretch(2,4)
        self.grid_input_conditions.setColumnStretch(3,1)
        self.grid_input_conditions.setColumnStretch(4,4)
        self.grid_input_ponifile.setColumnStretch(1,1)
        self.grid_input_ponifile.setColumnStretch(2,15)
        self.grid_input_ponifile.setColumnStretch(3,1)
        self.grid_input_reference.setColumnStretch(1,1)
        self.grid_input_reference.setColumnStretch(2,15)
        self.grid_input_buttons.setColumnStretch(1,1)
        self.grid_input_buttons.setColumnStretch(2,1)

        self.label_recent_h5 = QLabel(LABEL_RECENT_H5)
        self.combobox_h5_files = QComboBox()
        # self.combobox_h5_files.addItem("")        
        self.label_h5file = QLabel(LABEL_H5_FILE)
        self.lineedit_h5file = QLineEdit()
        self.lineedit_h5file.setEnabled(False)
        self.button_pick_maindir = QPushButton()
        self.button_pick_hdf5 = QPushButton()
        folder_icon_path = str(GUI_PATH.joinpath(ICON_FOLDER_PATH))
        self.button_pick_maindir.setIcon(QIcon(folder_icon_path))
        self.button_pick_maindir.setToolTip(LABEL_PICK_MAINDIR)
        h5_icon_path = str(GUI_PATH.joinpath(ICON_H5_PATH))
        self.button_pick_hdf5.setIcon(QIcon(h5_icon_path))
        self.button_pick_hdf5.setToolTip(LABEL_PICK_H5) 
        self.button_qz = QPushButton(BUTTON_QZ)
        self.button_qr = QPushButton(BUTTON_QR)
        self.label_extension = QLabel(LABEL_EXTENSION)
        self.combobox_extension = QComboBox()
        for ext in LIST_EXTENSION:
            self.combobox_extension.addItem(ext)
        self.label_conditions = QLabel(LABEL_WILDCARDS)
        self.lineedit_wildcards = QLineEdit(WILDCARDS_DEFAULT)
        self.label_ponifile = QLabel(LABEL_PONIFILE)
        self.combobox_ponifile = QComboBox()
        self.button_add_ponifile = QPushButton(BUTTON_PONIFILE)
        file_icon_path = str(GUI_PATH.joinpath(ICON_FILE_PATH))
        self.button_add_ponifile.setIcon(QIcon(file_icon_path))
        self.button_update_ponifile = QPushButton()
        refresh_icon_path = str(GUI_PATH.joinpath(ICON_REFRESH_PATH))
        self.button_update_ponifile.setIcon(QIcon(refresh_icon_path))
        self.label_reffolder = QLabel(LABEL_REFERENCE_FOLDER)
        self.combobox_reffolder = QComboBox()
        self.label_sample_orientation = QLabel(LABEL_SAMPLE_ORIENTATION)
        self.button_pyfaicalib = QPushButton(BUTTON_PYFAI_GUI)
        pyfai_icon_path = str(GUI_PATH.joinpath(ICON_PYFAI_PATH))
        self.button_pyfaicalib.setIcon(QIcon(pyfai_icon_path)) 
        self.button_start = QPushButton(BUTTON_UPDATE_DATA)
        self.button_start.setIcon(QIcon(refresh_icon_path)) 

        self.button_pick_maindir.setStyleSheet(button_style_input)
        self.button_pick_hdf5.setStyleSheet(button_style_input)
        self.button_add_ponifile.setStyleSheet(button_style_input)
        self.button_update_ponifile.setStyleSheet(button_style_input)
        self.button_qz.setStyleSheet(button_style_input)
        self.button_qr.setStyleSheet(button_style_input)
        self.button_pyfaicalib.setStyleSheet(button_style_input)
        self.button_start.setStyleSheet(button_style_input)

        set_bstyle([self.label_recent_h5, self.label_h5file, self.label_folders, self.label_files, self.label_extension, self.label_conditions, self.label_ponifile, self.label_reffolder, self.label_sample_orientation, self.title_input])

        self.grid_recent_h5.addWidget(self.label_recent_h5, 1, 1)
        self.grid_recent_h5.addWidget(self.combobox_h5_files, 1, 2)
        self.grid_input_maindir.addWidget(self.label_h5file, 1, 1)
        self.grid_input_maindir.addWidget(self.lineedit_h5file, 1, 2)
        self.grid_input_maindir.addWidget(self.button_pick_maindir, 1, 3)
        self.grid_input_maindir.addWidget(self.button_pick_hdf5, 1, 4)
        self.grid_input_conditions.addWidget(self.label_extension, 1, 1)
        self.grid_input_conditions.addWidget(self.combobox_extension, 1, 2)
        self.grid_input_conditions.addWidget(self.label_conditions, 1, 3)
        self.grid_input_conditions.addWidget(self.lineedit_wildcards, 1, 4)
        self.grid_input_ponifile.addWidget(self.label_ponifile, 1, 1)
        self.grid_input_ponifile.addWidget(self.combobox_ponifile, 1, 2)
        self.grid_input_ponifile.addWidget(self.button_add_ponifile, 1, 3)
        self.grid_input_ponifile.addWidget(self.button_update_ponifile, 1, 4)
        self.grid_input_reference.addWidget(self.label_reffolder, 1, 1)
        self.grid_input_reference.addWidget(self.combobox_reffolder, 1, 2)
        self.grid_input_orientations.addWidget(self.label_sample_orientation, 1, 1)
        self.grid_input_orientations.addWidget(self.button_qz, 1, 2)
        self.grid_input_orientations.addWidget(self.button_qr, 1, 3)
        self.grid_input_buttons.addWidget(self.button_pyfaicalib, 1, 1)
        self.grid_input_buttons.addWidget(self.button_start, 1, 2)

        self.grid_header_items = QGridLayout()
        self.label_headeritems = QLabel(LABEL_METADATA)
        self.combobox_headeritems = QComboBox()
        self.lineedit_headeritems = QLineEdit()
        # self.grid_plot_average = QGridLayout()
        # self.button_plot = QPushButton("UPDATE PLOT")
        # self.button_average = QPushButton("AVERAGE PLOT")
        # self.button_plot.setStyleSheet(button_style_plot)
        # self.button_average.setStyleSheet(button_style_plot)
        self.grid_header_items.setColumnStretch(1,1)
        self.grid_header_items.setColumnStretch(2,1)
        self.grid_header_items.setColumnStretch(3,3)
        self.grid_header_items.addWidget(self.label_headeritems, 1, 1)
        self.grid_header_items.addWidget(self.combobox_headeritems, 1, 2)
        self.grid_header_items.addWidget(self.lineedit_headeritems, 1, 3)
        # self.grid_plot_average.addWidget(self.button_plot, 1, 1)
        # self.grid_plot_average.addWidget(self.button_average, 1, 2)
        # self.grid_input_files.addLayout(self.grid_plot_average, 2, 1)

        self.grid_input_files.setRowStretch(1,1)
        self.grid_input_files.setRowStretch(2,2)
        self.grid_input_files.addLayout(self.grid_header_items, 1, 1)
        self.grid_live_title.setColumnStretch(1,1)
        self.grid_live_title.setColumnStretch(2,20)
        self.checkbox_live = QCheckBox(LABEL_LIVE)
        self.lineedit_filename = QLineEdit()
        self.lineedit_filename.setEnabled(False)
        self.combobox_units = QComboBox()
        self.button_log = QPushButton(BUTTON_LOG)
        self.button_colorbar = QPushButton(BUTTON_COLORBAR)
        self.button_default_graph = QPushButton(BUTTON_AUTO)
        self.button_log.setStyleSheet(button_on)
        self.button_colorbar.setStyleSheet(button_on)
        self.button_default_graph.setStyleSheet(button_on)
        for unit in DICT_UNIT_ALIAS.values():
            self.combobox_units.addItem(unit)
        self.button_map = QPushButton(BUTTON_SHOW_QMAP)
        self.button_savemap = QPushButton(BUTTON_SAVE_QMAP)
        
        self.button_map.setStyleSheet(button_style_thin)
        self.button_savemap.setStyleSheet(button_style_thin)
        self.label_title = QLabel(LABEL_MAP_TITLES)
        self.label_units = QLabel(LABEL_MAP_UNITS)
        self.combobox_headeritems_title = QComboBox()
        self.lineedit_headeritems_title = QLineEdit()
        self.xlims = QLabel(LABEL_XLIMS)
        self.ylims = QLabel(LABEL_YLIMS)
        self.xticks = QLabel(LABEL_XTICKS)
        self.yticks = QLabel(LABEL_YTICKS)
        self.lineedit_xmin = QLineEdit()
        self.lineedit_xmax = QLineEdit()
        self.lineedit_ymin = QLineEdit()
        self.lineedit_ymax = QLineEdit()
        self.lineedit_xticks = QLineEdit()
        self.lineedit_yticks = QLineEdit()

        self.lineedit_xmin.setEnabled(False)
        self.lineedit_xmax.setEnabled(False)
        self.lineedit_ymin.setEnabled(False)
        self.lineedit_ymax.setEnabled(False)
        self.lineedit_xticks.setEnabled(False)
        self.lineedit_yticks.setEnabled(False)

        self.label_sub = QLabel(LABEL_SUB_FACTOR)
        self.spinbox_sub = QDoubleSpinBox()
        self.spinbox_sub.setSingleStep(STEP_SUB_SPINBOX)
        # self.button_plot_2 = QPushButton("UPDATE PLOT")
        # self.button_plot_2.setStyleSheet(button_style_thin)
        self.button_clearplot = QPushButton(BUTTON_CLEAR_PLOT)
        self.grid_sub = QGridLayout()
        self.grid_sub.addWidget(self.label_sub, 1, 1)
        self.grid_sub.addWidget(self.spinbox_sub, 1, 2)
        self.grid_sub.addWidget(self.button_clearplot, 1, 3)

        self.button_saveplot = QPushButton(BUTTON_SAVE_INTEGRATIONS)
        self.button_batch = QPushButton(BUTTON_BATCH)
        self.button_fit = QPushButton(BUTTON_FITTING)

        self.button_clearplot.setStyleSheet(button_style_thin)
        self.button_saveplot.setStyleSheet(button_style_thin)
        self.button_batch.setStyleSheet(button_style_thin)
        self.button_fit.setStyleSheet(button_style_thin)

        self.label_integrations = QLabel(LABEL_INTEGRATIONS)
        self.combobox_integration = QComboBox()
        self.lineedit_integrations = QLineEdit()
        self.checkbox_mask_integration = QCheckBox(LABEL_MASK)

        self.grid_live_title.addWidget(self.checkbox_live, 1, 1)
        self.grid_live_title.addWidget(self.lineedit_filename, 1, 2)

        self.grid_input_and_graphs.setColumnStretch(1,1)
        self.grid_input_and_graphs.setColumnStretch(2,1)
        self.grid_input_and_graphs.setRowStretch(1,1)
        self.grid_input_and_graphs.setRowStretch(2,3)
        self.grid_input_and_graphs.setRowStretch(3,20)

        self.label_input_graph = QLabel(LABEL_2D_MAP)
        self.label_input_graph.setStyleSheet("background-color: white;border: 1px solid black;")
        self.label_input_graph.setAlignment(Qt.AlignCenter)
        self.label_input_chart = QLabel(LABEL_1D_CHART)
        self.label_input_chart.setStyleSheet("background-color: white;border: 1px solid black;")
        self.label_input_chart.setAlignment(Qt.AlignCenter)

        self.grid_input_graph = QGridLayout()
        self.grid_input_chart = QGridLayout()
        self.graph_2D_widget = Plot2D()
        self.graph_1D_widget = Plot1D()

        self.grid_input_and_graphs.addWidget(self.label_input_graph,1,1)
        self.grid_input_and_graphs.addWidget(self.label_input_chart,1,2)
        self.grid_input_and_graphs.addLayout(self.grid_input_graph,2,1)
        self.grid_input_and_graphs.addLayout(self.grid_input_chart,2,2)
        self.grid_input_and_graphs.addWidget(self.graph_2D_widget,3,1)
        self.grid_input_and_graphs.addWidget(self.graph_1D_widget,3,2)

        self.grid_units_graph = QGridLayout()
        self.grid_input_graph_buttons = QGridLayout()
        self.grid_input_graph_lims = QGridLayout()

        self.grid_input_graph.addLayout(self.grid_units_graph, 1, 1)
        self.grid_input_graph.addLayout(self.grid_input_graph_lims, 2, 1)
        self.grid_input_graph.addLayout(self.grid_input_graph_buttons, 3, 1)
        
        self.grid_units_graph.addWidget(self.label_units, 1, 1)
        self.grid_units_graph.addWidget(self.combobox_units, 1, 2)
        self.grid_units_graph.addWidget(self.button_log, 1, 3)
        self.grid_units_graph.addWidget(self.button_colorbar, 1, 4)
        self.grid_units_graph.addWidget(self.button_default_graph, 1, 5)

        self.grid_input_graph_buttons.addWidget(self.label_title, 1, 1)
        self.grid_input_graph_buttons.addWidget(self.combobox_headeritems_title, 1, 2)
        self.grid_input_graph_buttons.addWidget(self.lineedit_headeritems_title, 1, 3)
        self.grid_input_graph_buttons.addWidget(self.button_map, 1, 4)
        self.grid_input_graph_buttons.addWidget(self.button_savemap, 1, 5)

        self.grid_input_graph_lims.setColumnStretch(10,3)
        self.grid_input_graph_lims.addWidget(self.xlims, 1, 1)
        self.grid_input_graph_lims.addWidget(self.lineedit_xmin, 1, 2)
        self.grid_input_graph_lims.addWidget(self.lineedit_xmax, 1, 3)
        self.grid_input_graph_lims.addWidget(self.xticks, 1, 4)
        self.grid_input_graph_lims.addWidget(self.lineedit_xticks, 1, 5)
        self.grid_input_graph_lims.addWidget(self.ylims, 1, 6)
        self.grid_input_graph_lims.addWidget(self.lineedit_ymin, 1, 7)
        self.grid_input_graph_lims.addWidget(self.lineedit_ymax, 1, 8)
        self.grid_input_graph_lims.addWidget(self.yticks, 1, 9)
        self.grid_input_graph_lims.addWidget(self.lineedit_yticks, 1, 10)

        self.grid_input_chart.setRowStretch(1,1)
        self.grid_input_chart.setRowStretch(2,1)
        self.grid_input_chart.setRowStretch(3,1)
        self.grid_input_chart_integrations = QGridLayout()
        self.grid_chart_buttons = QGridLayout()
        self.grid_input_chart.addLayout(self.grid_input_chart_integrations, 1, 1)
        self.grid_input_chart.addLayout(self.grid_sub, 2, 1)
        self.grid_input_chart.addLayout(self.grid_chart_buttons, 3, 1)

        self.grid_input_chart_integrations.setColumnStretch(1,1)
        self.grid_input_chart_integrations.setColumnStretch(2,2)
        self.grid_input_chart_integrations.setColumnStretch(3,2)

        # self.grid_chart_buttons.addWidget(self.button_clearplot, 1, 1)
        self.grid_chart_buttons.addWidget(self.button_saveplot, 1, 1)
        self.grid_chart_buttons.addWidget(self.button_batch, 1, 2)
        self.grid_chart_buttons.addWidget(self.button_fit, 1, 3)

        self.grid_input_chart_integrations.addWidget(self.label_integrations, 1, 1)
        self.grid_input_chart_integrations.addWidget(self.combobox_integration, 1, 2)
        self.grid_input_chart_integrations.addWidget(self.lineedit_integrations, 1, 3)
        self.grid_input_chart_integrations.addWidget(self.checkbox_mask_integration, 1, 4)

        ##############################
        ### Tab for setup information
        ##############################

        self.grid_input_setup.setRowStretch(1,1)
        self.grid_input_setup.setRowStretch(1,2)
        self.grid_input_setup.setRowStretch(1,3)
        self.grid_input_setup.setRowStretch(1,4)
        self.grid_input_setup.setRowStretch(1,5)
        self.grid_input_setup.setColumnStretch(1,1)
        self.grid_input_setup.setColumnStretch(1,2)
        self.grid_input_setup.setColumnStretch(1,3)

        self.label_setup = QLabel(LABEL_DICT_SETUP)
        self.combobox_setup = QComboBox()
        self.button_setup = QPushButton(BUTTON_PICK_JSON)
        self.label_angle = QLabel(LABEL_IANGLE)
        self.lineedit_angle = QLineEdit()
        self.combobox_angle = QComboBox()
        self.label_tilt_angle = QLabel(LABEL_TILTANGLE)
        self.lineedit_tilt_angle = QLineEdit()
        self.combobox_tilt_angle = QComboBox()
        self.label_normfactor = QLabel(LABEL_NORMFACTOR)
        self.lineedit_normfactor = QLineEdit()
        self.combobox_normfactor = QComboBox()
        self.label_exposure = QLabel(LABEL_EXPOSURE)
        self.lineedit_exposure = QLineEdit()
        self.combobox_exposure = QComboBox()    
        self.label_setup_name = QLabel(LABEL_SETUP_NAME)
        self.lineedit_setup_name = QLineEdit()   
        self.button_setup_save = QPushButton(BUTTON_JSON_FILE)
        save_icon_path = str(GUI_PATH.joinpath(ICON_SAVE_PATH))
        self.button_setup_save.setIcon(QIcon(save_icon_path))
        self.button_setup_update = QPushButton(BUTTON_UPDATE_KEYS)

        self.grid_input_setup.addWidget(self.label_setup, 1, 1)
        self.grid_input_setup.addWidget(self.combobox_setup, 1, 2)
        self.grid_input_setup.addWidget(self.button_setup, 1, 3)
        self.grid_input_setup.addWidget(self.label_angle, 2, 1)
        self.grid_input_setup.addWidget(self.lineedit_angle, 2, 2)
        self.grid_input_setup.addWidget(self.combobox_angle, 2, 3)
        self.grid_input_setup.addWidget(self.label_tilt_angle, 3, 1)
        self.grid_input_setup.addWidget(self.lineedit_tilt_angle, 3, 2)
        self.grid_input_setup.addWidget(self.combobox_tilt_angle, 3, 3)
        self.grid_input_setup.addWidget(self.label_normfactor, 4, 1)
        self.grid_input_setup.addWidget(self.lineedit_normfactor, 4, 2)
        self.grid_input_setup.addWidget(self.combobox_normfactor, 4, 3)
        self.grid_input_setup.addWidget(self.label_exposure, 5, 1)
        self.grid_input_setup.addWidget(self.lineedit_exposure, 5, 2)
        self.grid_input_setup.addWidget(self.combobox_exposure, 5, 3)
        self.grid_input_setup.addWidget(self.label_setup_name, 6, 1)
        self.grid_input_setup.addWidget(self.lineedit_setup_name, 6, 2)
        self.grid_input_setup.addWidget(self.button_setup_save, 6, 3)
        self.grid_input_setup.addWidget(self.button_setup_update, 7, 1)

        # Build the grid for input integration parameters CAKE
        self.grid_input_integration_cake_up = QGridLayout()
        # self.button_add_cake = QPushButton("Add integration")    
        # self.grid_input_integration_cake.setRowStretch(1,7)
        # self.grid_input_integration_cake.setRowStretch(2,1)
        self.grid_input_integration_cake.addLayout(self.grid_input_integration_cake_up,1,1)
        # self.grid_input_integration_cake.addWidget(self.button_add_cake,2,1)

        self.grid_labels_cake = QGridLayout()
        self.grid_inputs_cake = QGridLayout()
        self.list_cakes = QListWidget()

        self.grid_input_integration_cake_up.addLayout(self.grid_labels_cake,1,1)
        self.grid_input_integration_cake_up.addLayout(self.grid_inputs_cake,1,2)
        self.grid_input_integration_cake_up.addWidget(self.list_cakes,1,3)

        self.label_name_cake = QLabel(LABEL_CAKE_NAME)
        self.label_suffix_cake = QLabel(LABEL_CAKE_SUFFIX)
        self.label_type_cake = QLabel(LABEL_CAKE_TYPE)
        self.label_units_cake = QLabel(LABEL_CAKE_UNITS)
        self.label_radialrange_cake = QLabel(LABEL_CAKE_RADIAL)
        self.label_azimrange_cake = QLabel(LABEL_CAKE_AZIM)
        self.label_azimbins_cake = QLabel(LABEL_CAKE_BINS)  

        self.grid_labels_cake.addWidget(self.label_name_cake,1,1)
        self.grid_labels_cake.addWidget(self.label_suffix_cake,2,1)
        self.grid_labels_cake.addWidget(self.label_type_cake,3,1)
        self.grid_labels_cake.addWidget(self.label_units_cake,4,1)
        self.grid_labels_cake.addWidget(self.label_radialrange_cake,5,1)
        self.grid_labels_cake.addWidget(self.label_azimrange_cake,6,1)
        self.grid_labels_cake.addWidget(self.label_azimbins_cake,7,1)

        self.lineedit_name_cake = QLineEdit()
        self.lineedit_suffix_cake = QLineEdit()
        self.combobox_type_cake = QComboBox()
        for cake_int in CAKE_INTEGRATIONS:
            self.combobox_type_cake.addItem(cake_int)
        self.combobox_units_cake = QComboBox()
        for unit in DICT_UNIT_ALIAS.values():
            self.combobox_units_cake.addItem(unit)
        # self.combobox_units_cake.addItem("q_A^-1")
        # self.combobox_units_cake.addItem("2th_deg")
        # self.combobox_units_cake.addItem("2th_rad")
        self.grid_radialrange = QGridLayout()
        self.label_radialmin_cake = QLabel(LABEL_MIN)
        self.spinbox_radialmin_cake = QDoubleSpinBox()
        self.spinbox_radialmin_cake.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_radialmin_cake.setRange(SPINBOX_RANGE_MIN, SPINBOX_RANGE_MAX)
        self.label_radialmax_cake = QLabel(LABEL_MAX)
        self.spinbox_radialmax_cake = QDoubleSpinBox()
        self.spinbox_radialmax_cake.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_radialmax_cake.setRange(SPINBOX_RANGE_MIN, SPINBOX_RANGE_MAX)
        self.grid_radialrange.addWidget(self.label_radialmin_cake,1,1)
        self.grid_radialrange.addWidget(self.spinbox_radialmin_cake,1,2)
        self.grid_radialrange.addWidget(self.label_radialmax_cake,1,3)
        self.grid_radialrange.addWidget(self.spinbox_radialmax_cake,1,4)
        self.grid_azimrange = QGridLayout()
        self.label_azimmin_cake = QLabel(LABEL_MIN)
        self.spinbox_azimmin_cake = QDoubleSpinBox()
        self.spinbox_azimmin_cake.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_azimmin_cake.setRange(SPINBOX_RANGE_MIN, SPINBOX_RANGE_MAX)
        self.label_azimmax_cake = QLabel(LABEL_MAX)
        self.spinbox_azimmax_cake = QDoubleSpinBox()
        self.spinbox_azimmax_cake.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_azimmax_cake.setRange(SPINBOX_RANGE_MIN, SPINBOX_RANGE_MAX)
        self.grid_azimrange.addWidget(self.label_azimmin_cake,1,1)
        self.grid_azimrange.addWidget(self.spinbox_azimmin_cake,1,2)
        self.grid_azimrange.addWidget(self.label_azimmax_cake,1,3)
        self.grid_azimrange.addWidget(self.spinbox_azimmax_cake,1,4)
        self.lineedit_azimbins_cake = QLineEdit()
        # self.spinbox_azimbins_cake = QDoubleSpinBox()
        # self.spinbox_azimbins_cake.setSingleStep(STEP_BINS_SPINBOX)
        # self.spinbox_azimbins_cake.setRange(SPINBOX_BINS_MIN, SPINBOX_BINS_MAX)

        self.grid_inputs_cake.addWidget(self.lineedit_name_cake,1,1)
        self.grid_inputs_cake.addWidget(self.lineedit_suffix_cake,2,1)
        self.grid_inputs_cake.addWidget(self.combobox_type_cake,3,1)
        self.grid_inputs_cake.addWidget(self.combobox_units_cake,4,1)
        self.grid_inputs_cake.addLayout(self.grid_radialrange,5,1)
        self.grid_inputs_cake.addLayout(self.grid_azimrange,6,1)
        self.grid_inputs_cake.addWidget(self.lineedit_azimbins_cake,7,1)

        # Build the grid for input integration parameters BOX
        self.grid_input_integration_box_up = QGridLayout()
        # self.button_add_box = QPushButton("Add integration")    

        # self.grid_input_integration_box.setRowStretch(1,7)
        # self.grid_input_integration_box.setRowStretch(2,1)
        self.grid_input_integration_box.addLayout(self.grid_input_integration_box_up,1,1)
        # self.grid_input_integration_box.addWidget(self.button_add_box,2,1)

        self.grid_labels_box = QGridLayout()
        self.grid_inputs_box = QGridLayout()
        self.list_boxs = QListWidget()

        self.grid_input_integration_box_up.addLayout(self.grid_labels_box,1,1)
        self.grid_input_integration_box_up.addLayout(self.grid_inputs_box,1,2)
        self.grid_input_integration_box_up.addWidget(self.list_boxs,1,3)

        self.label_name_box = QLabel(LABEL_BOX_NAME)
        self.label_suffix_box = QLabel(LABEL_BOX_SUFFIX)
        self.label_direction_box = QLabel(LABEL_BOX_DIRECTION)
        self.label_input_units_box = QLabel(LABEL_BOX_INPUT_UNITS)
        self.label_iprange_box = QLabel(LABEL_BOX_IP_RANGE)
        self.label_ooprange_box = QLabel(LABEL_BOX_OOP_RANGE)
        self.label_outputunits_box = QLabel(LABEL_BOX_OUTPUT_UNITS)  

        self.grid_labels_box.addWidget(self.label_name_box,1,1)
        self.grid_labels_box.addWidget(self.label_suffix_box,2,1)
        self.grid_labels_box.addWidget(self.label_direction_box,3,1)
        self.grid_labels_box.addWidget(self.label_input_units_box,4,1)
        self.grid_labels_box.addWidget(self.label_iprange_box,5,1)
        self.grid_labels_box.addWidget(self.label_ooprange_box,6,1)
        self.grid_labels_box.addWidget(self.label_outputunits_box,7,1)

        self.lineedit_name_box = QLineEdit()
        self.lineedit_suffix_box = QLineEdit()
        self.combobox_direction_box = QComboBox()
        for box in BOX_INTEGRATIONS:
            self.combobox_direction_box.addItem(box)
        self.combobox_units_box = QComboBox()
        for unit in DICT_UNIT_ALIAS.values():
            self.combobox_units_box.addItem(unit)
        self.grid_iprange = QGridLayout()
        self.label_ipmin_box = QLabel(LABEL_MIN)
        self.spinbox_ipmin_box = QDoubleSpinBox()
        self.spinbox_ipmin_box.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_ipmin_box.setRange(SPINBOX_RANGE_MIN, SPINBOX_RANGE_MAX)
        self.label_ipmax_box = QLabel(LABEL_MAX)
        self.spinbox_ipmax_box = QDoubleSpinBox()
        self.spinbox_ipmax_box.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_ipmax_box.setRange(SPINBOX_RANGE_MIN, SPINBOX_RANGE_MAX)
        self.grid_iprange.addWidget(self.label_ipmin_box,1,1)
        self.grid_iprange.addWidget(self.spinbox_ipmin_box,1,2)
        self.grid_iprange.addWidget(self.label_ipmax_box,1,3)
        self.grid_iprange.addWidget(self.spinbox_ipmax_box,1,4)
        self.grid_ooprange = QGridLayout()
        self.label_oopmin_box = QLabel(LABEL_MIN)
        self.spinbox_oopmin_box = QDoubleSpinBox()
        self.spinbox_oopmin_box.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_oopmin_box.setRange(SPINBOX_RANGE_MIN, SPINBOX_RANGE_MAX)
        self.label_oopmax_box = QLabel(LABEL_MAX)
        self.spinbox_oopmax_box = QDoubleSpinBox()
        self.spinbox_oopmax_box.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_oopmax_box.setRange(SPINBOX_RANGE_MIN, SPINBOX_RANGE_MAX)
        self.grid_ooprange.addWidget(self.label_oopmin_box,1,1)
        self.grid_ooprange.addWidget(self.spinbox_oopmin_box,1,2)
        self.grid_ooprange.addWidget(self.label_oopmax_box,1,3)
        self.grid_ooprange.addWidget(self.spinbox_oopmax_box,1,4)
        self.combobox_outputunits_box = QComboBox()
        for unit in DICT_UNIT_ALIAS.values():
            self.combobox_outputunits_box.addItem(unit)
        self.grid_inputs_box.addWidget(self.lineedit_name_box,1,1)
        self.grid_inputs_box.addWidget(self.lineedit_suffix_box,2,1)
        self.grid_inputs_box.addWidget(self.combobox_direction_box,3,1)
        self.grid_inputs_box.addWidget(self.combobox_units_box,4,1)
        self.grid_inputs_box.addLayout(self.grid_iprange,5,1)
        self.grid_inputs_box.addLayout(self.grid_ooprange,6,1)
        self.grid_inputs_box.addWidget(self.combobox_outputunits_box,7,1)

        set_bstyle([self.label_headeritems, self.label_plaintext, self.xlims, self.ylims, self.label_units, self.xticks, self.yticks, self.label_savefolder, self.label_integrations, self.label_sub, self.label_title,self.label_input_graph,self.label_input_chart])