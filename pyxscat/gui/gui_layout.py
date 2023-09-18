
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QListWidget, QTableWidget, QLabel, QComboBox
from PyQt5.QtWidgets import QCheckBox, QLineEdit, QDoubleSpinBox, QPlainTextEdit, QTabWidget, QSpinBox, QSplitter, QHBoxLayout, QVBoxLayout, QFrame
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from silx.gui.plot.PlotWindow import Plot1D, Plot2D
from other.units import DICT_UNIT_ALIAS, CAKE_INTEGRATIONS, BOX_INTEGRATIONS
from . import ICON_DIRECTORY

# TABS
LABEL_TAB_FILES = "Setup"
LABEL_TAB_SETUP = "Metadata"
LABEL_TAB_CAKE = "Cake Int."
LABEL_TAB_BOX = "Box Int."
LABEL_TAB_PONIFILE = "Ponifile"

# INPUT FILE PARAMETERS
LABEL_INPUT_PARAMETERS = "====== Input File Parameters ======"
LABEL_RECENT_H5 = "Recent .h5 files:"
LABEL_H5_FILE = "Main directory:"
LABEL_EXTENSION = "File extension:"
LABEL_WILDCARDS = "Wildcards(*):"
LABEL_PONIFILE = "Ponifile:"
LABEL_REFERENCE_FOLDER = "Reference folder:"
LABEL_REFERENCE_FILE = "Reference file:"
LABEL_AUTO_REFERENCE = "Auto"
LABEL_MASK_FOLDER = "Mask folder:"
LABEL_MASK_CHECK = "Use Mask"
LABEL_SAMPLE_ORIENTATION = "Sample orientation:"
BUTTON_MIRROR_DISABLE = ""
BUTTON_MIRROR_ENABLE = ""
BUTTON_QZ_PAR = "qz \u2191\u2191"
BUTTON_QZ_ANTIPAR = "qz \u2191\u2193"
BUTTON_QR_PAR = "qr \u2191\u2191"
BUTTON_QR_ANTIPAR = "qr \u2191\u2193"
BUTTON_PONIFILE = ""
BUTTON_PYFAI_GUI = " pyFAI "
BUTTON_UPDATE_DATA = " Update"
BUTTON_LIVE = " Live OFF"
BUTTON_LIVE_ON = " Live ON"
LIST_EXTENSION = [".edf", ".tif", ".tiff", ".cbf"]
WILDCARDS_DEFAULT = "*"
ICON_FOLDER = "folder.png"
ICON_FOLDER_PATH = str(ICON_DIRECTORY.joinpath(ICON_FOLDER))
LABEL_PICK_MAINDIR = "Pick the directory container of data files."
ICON_H5 = "hdf5.png"
H5_ICON_PATH = str(ICON_DIRECTORY.joinpath(ICON_H5))
ICON_MIRROR = "mirror.png"
ICON_MIRROR_PATH = str(ICON_DIRECTORY.joinpath(ICON_MIRROR))
LABEL_PICK_H5 = "Pick an .hdf5 file."
ICON_FILE = "file.png"
ICON_FILE_PATH = str(ICON_DIRECTORY.joinpath(ICON_FILE))
ICON_REFRESH = "refresh.png"
ICON_REFRESH_PATH = str(ICON_DIRECTORY.joinpath(ICON_REFRESH))
ICON_PYFAI = "pyfai.png"
ICON_PYFAI_PATH = str(ICON_DIRECTORY.joinpath(ICON_PYFAI))

# LIST OF FOLDERS
LABEL_LIST_FOLDERS = "Folders"

# LIST OF FILES
LABEL_LIST_FILES = "Files"
LABEL_METADATA = "Metadata:"

# LIVE BAR
LABEL_LIVE = "Live"

# SAVE_FOLDER BAR
LABEL_SAVE_FOLDER = "Save folder:"

# OUTPUT TERMINAL
LABEL_TERMINAL = "Output Terminal"
BUTTON_HIDE_TERMINAL = "HIDE TERMINAL"

LABEL_FILENAME = "Current displayed file:"

INDEX_TAB_1D_INTEGRATION = 0
INDEX_TAB_RAW_MAP = 0
INDEX_TAB_RESHAPE_MAP = 1
INDEX_TAB_Q_MAP = 2

# 2D MAP
LABEL_2D_MAP = "====== 2D Map Parameters ======"
BUTTON_LOG = "LOG"
BUTTON_COLORBAR = "COLORBAR OFF"
BUTTON_AUTO = "AUTO LIMITS ON"
BUTTON_SHOW_RESHAPE = "RESHAPE MAP"
BUTTON_SHOW_QMAP = "SHOW Q-MAP"
BUTTON_SAVE_QMAP = "SAVE Q-MAP"
LABEL_MAP_TITLES = "Map titles:"
LABEL_MAP_UNITS = "Units for 2D map:"
LABEL_XLIMS = "x-lims:"
LABEL_YLIMS = "y-lims:"
LABEL_XTICKS = "x-ticks:"
LABEL_YTICKS = "y-ticks:"

DEFAULT_BINNING = int(4)
BINNING_STEP = int(1)
BINNING_RANGE_MIN = int(0)
BINNING_RANGE_MAX = int(100)

BUTTON_LABEL_MINUS = "a"
BUTTON_LABEL_PLUS = "A"
BUTTON_COMMA_MINUS = "(-)"
BUTTON_COMMA_PLUS = "(+)"
LABEL_BINNING_DATA = "Binning Data:"

# 1D CHART
LABEL_1D_CHART = "====== 1D Plot Parameters ======"
LABEL_Q_MAP = "Q-map"
LABEL_RAW_MAP = "Raw Map"
LABEL_RESHAPE_MAP = "Reshape"
LABEL_TAB_1D_INT = "1D Integration"
LABEL_SUB_FACTOR = "Sub. factor:"
BUTTON_CLEAR_PLOT = "CLEAR"
BUTTON_SAVE_INTEGRATIONS = "SAVE"
BUTTON_BATCH = "BATCH"
BUTTON_FITTING = "OPEN FITTING FORM"
LABEL_INTEGRATIONS = "Integrations:"
LABEL_MASK_MAP = "Mask"
STEP_SUB_SPINBOX = 0.01

# SETUP INFORMATION TAB
LABEL_DICT_SETUP = "Metadata Dict.:"
BUTTON_PICK_JSON = "Pick .json"
LABEL_IANGLE = "Incident Angle:"
LABEL_TILTANGLE = "Tilt Angle:"
LABEL_NORMFACTOR = "Norm. Factor:"
LABEL_EXPOSURE = "Acquisition Time:"
LABEL_SETUP_NAME = "Dict. Name:"
BUTTON_JSON_FILE = "Save .json"
ICON_SAVE = "save.png"
ICON_SAVE_PATH = str(ICON_DIRECTORY.joinpath(ICON_SAVE))
BUTTON_UPDATE_KEYS = "UPDATE METADATA KEYS TO .H5 FILE"

# CAKE TAB
LABEL_CAKE_NAME = "Name:"
LABEL_CAKE_SUFFIX = "Suffix:"
LABEL_CAKE_TYPE = "Type:"
LABEL_CAKE_UNITS = "Units:"
LABEL_CAKE_RADIAL = "Radial range:"
LABEL_CAKE_AZIM = "Azimuthal range:"
LABEL_CAKE_BINS_OPT = "Azimuthal bins (optional):"
LABEL_CAKE_BINS_MAND = "Azimuthal bins (mandatory):"
LABEL_MIN = "Min:"
LABEL_MAX = "Max."

# BOX TAB
LABEL_BOX_NAME = "Name:"
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

SPINBOX_RADIAL_MIN = 0
SPINBOX_RADIAL_MAX = 1E9
SPINBOX_AZIM_MIN = -180
SPINBOX_AZIM_MAX = 180

SPINBOX_RANGE_MIN = -100
SPINBOX_RANGE_MAX = 100
ERROR_OUTPUT = "Something went wrong with the output message..."

WIDTH_SPINBOX_MAX = 75

# PONIFILE PARAMETERS TAB
LABEL_PONI_MOD_WARNING = "CHANGING THESE PARAMETERS WON'T CHANGE THE .PONI FILE. USE IT WISELY."
LABEL_PONI_MOD = "Modify .poni parameters"
LABEL_DETECTOR = "Detector"
LABEL_DETECTOR_BINNING = "Detector Binning"
LABEL_PIXEL_1 = "Pixel size horz. (m):"
LABEL_PIXEL_2 = "Pixel size vert. (m):"
LABEL_SHAPE_1 = "Detector shape (1):"
LABEL_SHAPE_2 = "Detector shape (2):"
LABEL_DISTANCE = "Distance (m):"
LABEL_PONI_PONI_1 = "PONI 1 (m):"
LABEL_PONI_PONI_2 = "PONI 2 (m):"
LABEL_PONI_ROT_1 = "Rots (rads) (1):"
LABEL_PONI_ROT_2 = "Rots (rads) (2):"
LABEL_PONI_ROT_3 = "Rots (rads) (3):"
LABEL_PONI_WAVELENGTH = "Wavelength (m):"
BUTTON_UPDATE_PONI_PARAMETERS = "UPDATE"
BUTTON_UPDATE_OLD_PONI_PARAMETERS = "RETRIEVE"
BUTTON_SAVE_PONI_PARAMETERS = "SAVE"

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

button_style_input_disable = """
QPushButton {
    font-weight: bold;
    color : black;
    background-color: #fbe5d6;
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

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


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
        self.setGeometry(300, 300, 300, 200)
        self.hbox_main = QHBoxLayout()
        self.setLayout(self.hbox_main)

        self.vbox_left = QVBoxLayout()
        self.vbox_right = QVBoxLayout()

        self.frame_left = QFrame(self)       
        self.frame_left.setFrameShape(QFrame.StyledPanel)
        self.frame_left.setLayout(self.vbox_left)

        self.frame_right = QFrame(self)       
        self.frame_right.setFrameShape(QFrame.StyledPanel)
        self.frame_right.setLayout(self.vbox_right)

        # Main splitter and two vertical boxes with frames
        self.splitter_main = QSplitter(orientation=Qt.Horizontal)

        self.hbox_main.addWidget(self.splitter_main)        

        self.splitter_vbox_left = QSplitter(orientation=Qt.Vertical)
        self.splitter_vbox_right = QSplitter(orientation=Qt.Vertical)

        self.vbox_left.addWidget(self.splitter_vbox_left)
        self.vbox_right.addWidget(self.splitter_vbox_right)

        self.splitter_main.addWidget(self.frame_left)
        self.splitter_main.addWidget(self.frame_right)

        self.splitter_main.setStretchFactor(0, 1)
        self.splitter_main.setStretchFactor(1, 3)

        self.vbox_input = QVBoxLayout()
        self.widget_tabs = QTabWidget()
        self.widget_tabs.setLayout(self.vbox_input)
        self.vbox_list_folder = QVBoxLayout()
        self.widget_folder_tab = QTabWidget()
        self.widget_folder_tab.setLayout(self.vbox_list_folder)
        self.vbox_table_files = QVBoxLayout()        
        self.widget_file_tab = QTabWidget()
        self.widget_file_tab.setLayout(self.vbox_table_files)

        self.splitter_vbox_left.addWidget(self.widget_tabs)
        self.splitter_vbox_left.addWidget(self.widget_folder_tab)
        self.splitter_vbox_left.addWidget(self.widget_file_tab)

        self.hbox_top_label = QHBoxLayout()
        self.hbox_top_label.setContentsMargins(1,0,1,0)
        self.widget_top_label = QWidget()
        self.widget_top_label.setLayout(self.hbox_top_label)
        self.splitter_graphs = QSplitter()
        self.vbox_terminal = QVBoxLayout()
        self.vbox_terminal.setContentsMargins(1,0,1,0)
        self.widget_terminal_tab = QTabWidget()
        self.widget_terminal_tab.setLayout(self.vbox_terminal)

        self.splitter_vbox_right.addWidget(self.widget_top_label)
        self.splitter_vbox_right.addWidget(self.splitter_graphs)
        self.splitter_vbox_right.addWidget(self.widget_terminal_tab)

        self.splitter_vbox_right.setStretchFactor(0,1)
        self.splitter_vbox_right.setStretchFactor(1,20)
        self.splitter_vbox_right.setStretchFactor(2,2)

        #######################################
        ########## WIDGET_TABS ################
        #######################################

        self.vbox_input = QVBoxLayout()
        self.vbox_metadata = QVBoxLayout()
        self.vbox_metadata.setSpacing(0)
        self.hbox_cake = QHBoxLayout()
        self.hbox_box = QHBoxLayout()
        self.vbox_poni = QVBoxLayout()

        self.vbox_metadata.setStretch(0,1)
        self.vbox_metadata.setStretch(1,1)
        self.vbox_metadata.setStretch(2,1)
        self.vbox_metadata.setStretch(3,1)
        self.vbox_metadata.setStretch(4,1)

        self.widget_vbox_input = QWidget()
        self.widget_vbox_metadata = QWidget()
        self.widget_cake = QWidget()
        self.widget_box = QWidget()
        self.widget_vbox_poni = QWidget()

        self.widget_vbox_input.setLayout(self.vbox_input)        
        self.widget_vbox_metadata.setLayout(self.vbox_metadata)
        self.widget_cake.setLayout(self.hbox_cake)
        self.widget_box.setLayout(self.hbox_box)
        self.widget_vbox_poni.setLayout(self.vbox_poni)

        self.widget_tabs.addTab(self.widget_vbox_input, LABEL_TAB_FILES)
        self.widget_tabs.addTab(self.widget_vbox_metadata, LABEL_TAB_SETUP)
        self.widget_tabs.addTab(self.widget_cake, LABEL_TAB_CAKE)
        self.widget_tabs.addTab(self.widget_box, LABEL_TAB_BOX)
        self.widget_tabs.addTab(self.widget_vbox_poni, LABEL_TAB_PONIFILE)

        ### INPUT TAB ###

        self.hbox_recent_h5 = QHBoxLayout()
        self.hbox_recent_h5.setContentsMargins(1, 0, 1, 0)
        self.hbox_maindir = QHBoxLayout()
        self.hbox_maindir.setContentsMargins(1, 0, 1, 0)
        self.hbox_pattern = QHBoxLayout()
        self.hbox_pattern.setContentsMargins(1, 0, 1, 0)
        self.hbox_poni = QHBoxLayout()
        self.hbox_poni.setContentsMargins(1, 0, 1, 0)
        self.hbox_reffolder = QHBoxLayout()
        self.hbox_reffolder.setContentsMargins(1, 0, 1, 0)
        self.hbox_reffile = QHBoxLayout()
        self.hbox_reffile.setContentsMargins(1, 0, 1, 0)

        self.hbox_sample_orientation = QHBoxLayout()
        self.hbox_sample_orientation.setContentsMargins(1, 0, 1, 0)
        self.hbox_pyfai = QHBoxLayout()
        self.hbox_pyfai.setContentsMargins(1, 0, 1, 0)

        self.widget_recent_h5 = QWidget()
        self.widget_maindir = QWidget()
        self.widget_pattern = QWidget()
        self.widget_poni = QWidget()
        self.widget_reffolder = QWidget()
        self.widget_reffile = QWidget()

        self.widget_sample_orientation = QWidget()
        self.widget_pyfai = QWidget()

        self.widget_recent_h5.setLayout(self.hbox_recent_h5)
        self.widget_maindir.setLayout(self.hbox_maindir)
        self.widget_pattern.setLayout(self.hbox_pattern)
        self.widget_poni.setLayout(self.hbox_poni)
        self.widget_reffolder.setLayout(self.hbox_reffolder)
        self.widget_reffile.setLayout(self.hbox_reffile)
        self.widget_sample_orientation.setLayout(self.hbox_sample_orientation)
        self.widget_pyfai.setLayout(self.hbox_pyfai)

        self.vbox_input.addWidget(self.widget_recent_h5)
        self.vbox_input.addWidget(self.widget_maindir)
        self.vbox_input.addWidget(self.widget_pattern)
        self.vbox_input.addWidget(self.widget_poni)
        self.vbox_input.addWidget(self.widget_reffolder)
        self.vbox_input.addWidget(self.widget_reffile)
        # self.vbox_input.addWidget(self.widget_savefolder)
        self.vbox_input.addWidget(self.widget_sample_orientation)
        self.vbox_input.addWidget(self.widget_pyfai)

        self.label_recent_h5 = QLabel(LABEL_RECENT_H5)
        self.combobox_h5_files = QComboBox()

        self.hbox_recent_h5.addWidget(self.label_recent_h5, Qt.AlignLeft)
        self.hbox_recent_h5.addWidget(self.combobox_h5_files, Qt.AlignLeft)

        self.hbox_recent_h5.setStretch(0,1)
        self.hbox_recent_h5.setStretch(1,10)

        self.label_h5file = QLabel(LABEL_H5_FILE)
        self.lineedit_h5file = QLineEdit()
        self.lineedit_h5file.setEnabled(False)
        self.button_pick_maindir = QPushButton()
        self.button_pick_maindir.setIcon(QIcon(ICON_FOLDER_PATH))
        self.button_pick_maindir.setToolTip(LABEL_PICK_MAINDIR)    
        self.button_pick_maindir.setStyleSheet(button_style_input)    
        self.button_pick_hdf5 = QPushButton()
        self.button_pick_hdf5.setIcon(QIcon(H5_ICON_PATH))
        self.button_pick_hdf5.setToolTip(LABEL_PICK_H5)
        self.button_pick_hdf5.setStyleSheet(button_style_input)

        self.hbox_maindir.addWidget(self.label_h5file)
        self.hbox_maindir.addWidget(self.lineedit_h5file)
        self.hbox_maindir.addWidget(self.button_pick_maindir)
        self.hbox_maindir.addWidget(self.button_pick_hdf5)

        self.label_extension = QLabel(LABEL_EXTENSION)
        self.combobox_extension = QComboBox()
        for ext in LIST_EXTENSION:
            self.combobox_extension.addItem(ext)
        self.label_wildcard = QLabel(LABEL_WILDCARDS)
        self.lineedit_wildcards = QLineEdit(WILDCARDS_DEFAULT)

        self.hbox_pattern.addWidget(self.label_extension)
        self.hbox_pattern.addWidget(self.combobox_extension)
        self.hbox_pattern.addWidget(self.label_wildcard)
        self.hbox_pattern.addWidget(self.lineedit_wildcards)

        self.label_ponifile = QLabel(LABEL_PONIFILE)
        self.combobox_ponifile = QComboBox()
        self.button_add_ponifile = QPushButton(BUTTON_PONIFILE)
        self.button_add_ponifile.setIcon(QIcon(ICON_FILE_PATH))
        self.button_add_ponifile.setStyleSheet(button_style_input)
        self.button_update_ponifile = QPushButton()
        self.button_update_ponifile.setIcon(QIcon(ICON_REFRESH_PATH))
        self.button_update_ponifile.setStyleSheet(button_style_input)

        self.hbox_poni.addWidget(self.label_ponifile, Qt.AlignLeft)
        self.hbox_poni.addWidget(self.combobox_ponifile, Qt.AlignLeft)

        self.hbox_poni.setStretch(0,1)
        self.hbox_poni.setStretch(1,10)

        self.label_reffolder = QLabel(LABEL_REFERENCE_FOLDER)
        self.combobox_reffolder = QComboBox()

        self.hbox_reffolder.addWidget(self.label_reffolder, Qt.AlignLeft)
        self.hbox_reffolder.addWidget(self.combobox_reffolder, Qt.AlignLeft)

        self.hbox_reffolder.setStretch(0,1)
        self.hbox_reffolder.setStretch(1,10)

        self.label_reffile = QLabel(LABEL_REFERENCE_FILE)
        self.combobox_reffile = QComboBox()
        self.combobox_reffile.setEnabled(False)
        self.checkbox_auto_reffile = QCheckBox(LABEL_AUTO_REFERENCE)
        self.checkbox_auto_reffile.setChecked(True)

        self.hbox_reffile.addWidget(self.label_reffile, Qt.AlignLeft)
        self.hbox_reffile.addWidget(self.combobox_reffile, Qt.AlignLeft)
        self.hbox_reffile.addWidget(self.checkbox_auto_reffile, Qt.AlignLeft)

        self.hbox_reffile.setStretch(0,1)
        self.hbox_reffile.setStretch(1,10)
        self.hbox_reffile.setStretch(2,1)

        self.label_sample_orientation = QLabel(LABEL_SAMPLE_ORIENTATION)
        self.button_mirror = QPushButton(BUTTON_MIRROR_DISABLE)
        self.button_mirror.setIcon(QIcon(ICON_MIRROR_PATH))
        self.button_mirror.setStyleSheet(button_style_input)
        self.button_qz = QPushButton(BUTTON_QZ_PAR)
        self.button_qz.setStyleSheet(button_style_input)
        self.button_qr = QPushButton(BUTTON_QR_PAR)
        self.button_qr.setStyleSheet(button_style_input)

        self.hbox_sample_orientation.addWidget(self.label_sample_orientation)
        self.hbox_sample_orientation.addWidget(self.button_mirror)
        self.hbox_sample_orientation.addWidget(self.button_qz)
        self.hbox_sample_orientation.addWidget(self.button_qr)

        self.button_pyfaicalib = QPushButton(BUTTON_PYFAI_GUI)
        self.button_pyfaicalib.setIcon(QIcon(ICON_PYFAI_PATH))
        self.button_pyfaicalib.setStyleSheet(button_style_input)
        self.button_start = QPushButton(BUTTON_UPDATE_DATA)
        self.button_start.setIcon(QIcon(ICON_REFRESH_PATH))
        self.button_start.setStyleSheet(button_style_input)
        self.button_live = QPushButton(BUTTON_LIVE)
        self.button_live.setStyleSheet(button_style_input)

        self.hbox_pyfai.addWidget(self.button_pyfaicalib)
        self.hbox_pyfai.addWidget(self.button_start)
        self.hbox_pyfai.addWidget(self.button_live)

        ### METADATA TAB ###

        self.hbox_metadata_choose = QHBoxLayout()
        self.hbox_metadata_choose.setContentsMargins(1, 0, 1, 0)

        self.hbox_metadata_iangle = QHBoxLayout()
        self.hbox_metadata_iangle.setContentsMargins(1, 0, 1, 0)

        self.hbox_metadata_tangle = QHBoxLayout()
        self.hbox_metadata_tangle.setContentsMargins(1, 0, 1, 0)

        self.hbox_metadata_norm = QHBoxLayout()
        self.hbox_metadata_norm.setContentsMargins(1, 0, 1, 0)

        self.hbox_metadata_acq = QHBoxLayout()
        self.hbox_metadata_acq.setContentsMargins(1, 0, 1, 0)

        self.hbox_metadata_name = QHBoxLayout()
        self.hbox_metadata_name.setContentsMargins(1, 0, 1, 0)

        self.widget_metadata_choose = QWidget()
        self.widget_metadata_iangle = QWidget()
        self.widget_metadata_tangle = QWidget()
        self.widget_metadata_norm = QWidget()
        self.widget_metadata_acq = QWidget()
        self.widget_metadata_name = QWidget()

        self.widget_metadata_choose.setLayout(self.hbox_metadata_choose)
        self.widget_metadata_iangle.setLayout(self.hbox_metadata_iangle)
        self.widget_metadata_tangle.setLayout(self.hbox_metadata_tangle)
        self.widget_metadata_norm.setLayout(self.hbox_metadata_norm)
        self.widget_metadata_acq.setLayout(self.hbox_metadata_acq)
        self.widget_metadata_name.setLayout(self.hbox_metadata_name)

        self.label_setup = QLabel(LABEL_DICT_SETUP)
        self.combobox_setup = QComboBox()
        self.button_setup = QPushButton(BUTTON_PICK_JSON)
        self.button_setup.setStyleSheet(button_style_input)

        self.hbox_metadata_choose.addWidget(self.label_setup, Qt.AlignLeft)
        self.hbox_metadata_choose.addWidget(self.combobox_setup, Qt.AlignLeft)
        self.hbox_metadata_choose.addWidget(self.button_setup, Qt.AlignLeft)

        self.hbox_metadata_choose.setStretch(1,10)

        self.label_angle = QLabel(LABEL_IANGLE)
        self.lineedit_angle = QLineEdit()
        self.combobox_angle = QComboBox()

        self.hbox_metadata_iangle.addWidget(self.label_angle)
        self.hbox_metadata_iangle.addWidget(self.lineedit_angle)
        self.hbox_metadata_iangle.addWidget(self.combobox_angle)

        self.label_tilt_angle = QLabel(LABEL_TILTANGLE)
        self.lineedit_tilt_angle = QLineEdit()
        self.combobox_tilt_angle = QComboBox()

        self.hbox_metadata_tangle.addWidget(self.label_tilt_angle)
        self.hbox_metadata_tangle.addWidget(self.lineedit_tilt_angle)
        self.hbox_metadata_tangle.addWidget(self.combobox_tilt_angle)

        self.label_normfactor = QLabel(LABEL_NORMFACTOR)
        self.lineedit_normfactor = QLineEdit()
        self.combobox_normfactor = QComboBox()

        self.hbox_metadata_norm.addWidget(self.label_normfactor)
        self.hbox_metadata_norm.addWidget(self.lineedit_normfactor)
        self.hbox_metadata_norm.addWidget(self.combobox_normfactor)

        self.label_exposure = QLabel(LABEL_EXPOSURE)
        self.lineedit_exposure = QLineEdit()
        self.combobox_exposure = QComboBox()

        self.hbox_metadata_acq.addWidget(self.label_exposure)
        self.hbox_metadata_acq.addWidget(self.lineedit_exposure)
        self.hbox_metadata_acq.addWidget(self.combobox_exposure)

        self.label_setup_name = QLabel(LABEL_SETUP_NAME)
        self.lineedit_setup_name = QLineEdit()   
        self.button_setup_save = QPushButton(BUTTON_JSON_FILE)
        self.button_setup_save.setStyleSheet(button_style_input)
        self.button_setup_save.setIcon(QIcon(ICON_SAVE_PATH))

        self.hbox_metadata_name.addWidget(self.label_setup_name)
        self.hbox_metadata_name.addWidget(self.lineedit_setup_name)
        self.hbox_metadata_name.addWidget(self.button_setup_save)

        self.button_setup_update = QPushButton(BUTTON_UPDATE_KEYS)
        self.button_setup_update.setStyleSheet(button_style_input)

        self.vbox_metadata.addWidget(self.widget_metadata_choose)
        self.vbox_metadata.addWidget(self.widget_metadata_iangle)
        self.vbox_metadata.addWidget(self.widget_metadata_tangle)
        self.vbox_metadata.addWidget(self.widget_metadata_norm)
        self.vbox_metadata.addWidget(self.widget_metadata_acq)
        self.vbox_metadata.addWidget(self.widget_metadata_name)
        self.vbox_metadata.addWidget(self.button_setup_update)

        ## CAKE INTEGRATION TAB

        self.vbox_cake_parameters = QVBoxLayout()
        self.widget_cake_parameters = QWidget()
        self.widget_cake_parameters.setLayout(self.vbox_cake_parameters)
        self.list_cakes = QListWidget()

        self.hbox_cake.setStretch(0,1)
        self.hbox_cake.setStretch(1,10)

        self.hbox_cake.addWidget(self.widget_cake_parameters)
        self.hbox_cake.addWidget(self.list_cakes)
    
        self.hbox_cake_name = QHBoxLayout()
        self.hbox_cake_name.setContentsMargins(1, 0, 1, 0)
        self.hbox_cake_suffix = QHBoxLayout()
        self.hbox_cake_suffix.setContentsMargins(1, 0, 1, 0)
        self.hbox_cake_type = QHBoxLayout()
        self.hbox_cake_type.setContentsMargins(1, 0, 1, 0)
        self.hbox_cake_unit = QHBoxLayout()
        self.hbox_cake_unit.setContentsMargins(1, 0, 1, 0)
        self.hbox_cake_radial = QHBoxLayout()
        self.hbox_cake_radial.setContentsMargins(1, 0, 1, 0)
        self.hbox_cake_azimut = QHBoxLayout()
        self.hbox_cake_azimut.setContentsMargins(1, 0, 1, 0)
        self.hbox_cake_bins = QHBoxLayout()
        self.hbox_cake_bins.setContentsMargins(1, 0, 1, 0)

        self.widget_cake_name = QWidget()
        self.widget_cake_suffix = QWidget()
        self.widget_cake_type = QWidget()
        self.widget_cake_unit = QWidget()
        self.widget_cake_radial = QWidget()
        self.widget_cake_azimut = QWidget()
        self.widget_cake_bins = QWidget()

        self.widget_cake_name.setLayout(self.hbox_cake_name)
        self.widget_cake_suffix.setLayout(self.hbox_cake_suffix)
        self.widget_cake_type.setLayout(self.hbox_cake_type)
        self.widget_cake_unit.setLayout(self.hbox_cake_unit)
        self.widget_cake_radial.setLayout(self.hbox_cake_radial)
        self.widget_cake_azimut.setLayout(self.hbox_cake_azimut)
        self.widget_cake_bins.setLayout(self.hbox_cake_bins)

        self.vbox_cake_parameters.addWidget(self.widget_cake_name)
        self.vbox_cake_parameters.addWidget(self.widget_cake_suffix)
        self.vbox_cake_parameters.addWidget(self.widget_cake_type)
        self.vbox_cake_parameters.addWidget(self.widget_cake_unit)
        self.vbox_cake_parameters.addWidget(self.widget_cake_radial)
        self.vbox_cake_parameters.addWidget(self.widget_cake_azimut)
        self.vbox_cake_parameters.addWidget(self.widget_cake_bins)

        self.label_name_cake = QLabel(LABEL_CAKE_NAME)
        self.lineedit_name_cake = QLineEdit()

        self.hbox_cake_name.addWidget(self.label_name_cake)
        self.hbox_cake_name.addWidget(self.lineedit_name_cake)

        self.label_suffix_cake = QLabel(LABEL_CAKE_SUFFIX)
        self.lineedit_suffix_cake = QLineEdit()

        self.hbox_cake_suffix.addWidget(self.label_suffix_cake)
        self.hbox_cake_suffix.addWidget(self.lineedit_suffix_cake)

        self.label_type_cake = QLabel(LABEL_CAKE_TYPE)
        self.combobox_type_cake = QComboBox()
        for cake_int in CAKE_INTEGRATIONS:
            self.combobox_type_cake.addItem(cake_int)

        self.hbox_cake_type.addWidget(self.label_type_cake, Qt.AlignLeft)
        self.hbox_cake_type.addWidget(self.combobox_type_cake, Qt.AlignLeft)

        self.hbox_cake_type.setStretch(1,10)

        self.label_units_cake = QLabel(LABEL_CAKE_UNITS)
        self.combobox_units_cake = QComboBox()
        for unit in DICT_UNIT_ALIAS.values():
            self.combobox_units_cake.addItem(unit)

        self.hbox_cake_unit.addWidget(self.label_units_cake, Qt.AlignLeft)
        self.hbox_cake_unit.addWidget(self.combobox_units_cake, Qt.AlignLeft)

        self.hbox_cake_unit.setStretch(1,10)

        self.label_radialrange_cake = QLabel(LABEL_CAKE_RADIAL)
        self.label_radialmin_cake = QLabel(LABEL_MIN)
        self.spinbox_radialmin_cake = QDoubleSpinBox()
        self.spinbox_radialmin_cake.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_radialmin_cake.setRange(SPINBOX_RADIAL_MIN, SPINBOX_RADIAL_MAX)
        self.label_radialmax_cake = QLabel(LABEL_MAX)
        self.spinbox_radialmax_cake = QDoubleSpinBox()
        self.spinbox_radialmax_cake.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_radialmax_cake.setRange(SPINBOX_RADIAL_MIN, SPINBOX_RADIAL_MAX)
        
        self.hbox_cake_radial.addWidget(self.label_radialrange_cake)
        self.hbox_cake_radial.addWidget(self.spinbox_radialmin_cake)
        self.hbox_cake_radial.addWidget(self.spinbox_radialmax_cake)
        
        self.spinbox_radialmin_cake.setMaximumWidth(WIDTH_SPINBOX_MAX)
        self.spinbox_radialmax_cake.setMaximumWidth(WIDTH_SPINBOX_MAX)

        self.label_azimrange_cake = QLabel(LABEL_CAKE_AZIM)
        self.label_azimmin_cake = QLabel(LABEL_MIN)
        self.spinbox_azimmin_cake = QDoubleSpinBox()
        self.spinbox_azimmin_cake.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_azimmin_cake.setRange(SPINBOX_AZIM_MIN, SPINBOX_AZIM_MAX)
        self.label_azimmax_cake = QLabel(LABEL_MAX)
        self.spinbox_azimmax_cake = QDoubleSpinBox()
        self.spinbox_azimmax_cake.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_azimmax_cake.setRange(SPINBOX_AZIM_MIN, SPINBOX_AZIM_MAX)
        
        self.hbox_cake_azimut.addWidget(self.label_azimrange_cake)
        self.hbox_cake_azimut.addWidget(self.spinbox_azimmin_cake)
        self.hbox_cake_azimut.addWidget(self.spinbox_azimmax_cake)

        self.spinbox_azimmin_cake.setMaximumWidth(WIDTH_SPINBOX_MAX)
        self.spinbox_azimmax_cake.setMaximumWidth(WIDTH_SPINBOX_MAX)
        
        self.label_azimbins_cake = QLabel(LABEL_CAKE_BINS_OPT) 
        self.lineedit_azimbins_cake = QLineEdit()

        self.hbox_cake_bins.addWidget(self.label_azimbins_cake)
        self.hbox_cake_bins.addWidget(self.lineedit_azimbins_cake)

        # BOX INTEGRATION TAB

        self.vbox_box_parameters = QVBoxLayout()
        self.widget_box_parameters = QWidget()
        self.widget_box_parameters.setLayout(self.vbox_box_parameters)
        self.list_box = QListWidget()

        self.hbox_box.addWidget(self.widget_box_parameters)
        self.hbox_box.addWidget(self.list_box)

        self.hbox_box_name = QHBoxLayout()
        self.hbox_box_name.setContentsMargins(1, 0, 1, 0)
        self.hbox_box_suffix = QHBoxLayout()
        self.hbox_box_suffix.setContentsMargins(1, 0, 1, 0)
        self.hbox_box_direction = QHBoxLayout()
        self.hbox_box_direction.setContentsMargins(1, 0, 1, 0)
        self.hbox_box_unit_input = QHBoxLayout()
        self.hbox_box_unit_input.setContentsMargins(1, 0, 1, 0)
        self.hbox_box_ip = QHBoxLayout()
        self.hbox_box_ip.setContentsMargins(1, 0, 1, 0)
        self.hbox_box_oop = QHBoxLayout()
        self.hbox_box_oop.setContentsMargins(1, 0, 1, 0)
        self.hbox_box_unit_output = QHBoxLayout()
        self.hbox_box_unit_output.setContentsMargins(1, 0, 1, 0)

        self.widget_box_name = QWidget()
        self.widget_box_suffix = QWidget()
        self.widget_box_direction = QWidget()
        self.widget_box_unit_input = QWidget()
        self.widget_box_ip = QWidget()
        self.widget_box_oop = QWidget()
        self.widget_box_unit_output = QWidget()

        self.widget_box_name.setLayout(self.hbox_box_name)
        self.widget_box_suffix.setLayout(self.hbox_box_suffix)
        self.widget_box_direction.setLayout(self.hbox_box_direction)
        self.widget_box_unit_input.setLayout(self.hbox_box_unit_input)
        self.widget_box_ip.setLayout(self.hbox_box_ip)
        self.widget_box_oop.setLayout(self.hbox_box_oop)
        self.widget_box_unit_output.setLayout(self.hbox_box_unit_output)

        self.vbox_box_parameters.addWidget(self.widget_box_name)
        self.vbox_box_parameters.addWidget(self.widget_box_suffix)
        self.vbox_box_parameters.addWidget(self.widget_box_direction)
        self.vbox_box_parameters.addWidget(self.widget_box_unit_input)
        self.vbox_box_parameters.addWidget(self.widget_box_ip)
        self.vbox_box_parameters.addWidget(self.widget_box_oop)
        self.vbox_box_parameters.addWidget(self.widget_box_unit_output)

        self.label_name_box = QLabel(LABEL_BOX_NAME)
        self.lineedit_name_box = QLineEdit()

        self.hbox_box_name.addWidget(self.label_name_box)
        self.hbox_box_name.addWidget(self.lineedit_name_box)

        self.label_suffix_box = QLabel(LABEL_BOX_SUFFIX)
        self.lineedit_suffix_box = QLineEdit()

        self.hbox_box_suffix.addWidget(self.label_suffix_box)
        self.hbox_box_suffix.addWidget(self.lineedit_suffix_box)

        self.label_direction_box = QLabel(LABEL_BOX_DIRECTION)
        self.combobox_direction_box = QComboBox()
        for box in BOX_INTEGRATIONS:
            self.combobox_direction_box.addItem(box)

        self.hbox_box_direction.addWidget(self.label_direction_box, Qt.AlignLeft)
        self.hbox_box_direction.addWidget(self.combobox_direction_box, Qt.AlignLeft)

        self.hbox_box_direction.setStretch(1,10)

        self.label_input_units_box = QLabel(LABEL_BOX_INPUT_UNITS)
        self.combobox_units_box = QComboBox()
        for unit in DICT_UNIT_ALIAS.values():
            self.combobox_units_box.addItem(unit)

        self.hbox_box_unit_input.addWidget(self.label_input_units_box, Qt.AlignLeft)
        self.hbox_box_unit_input.addWidget(self.combobox_units_box, Qt.AlignLeft)

        self.hbox_box_unit_input.setStretch(1,10)

        self.label_iprange_box = QLabel(LABEL_BOX_IP_RANGE)
        self.label_ipmin_box = QLabel(LABEL_MIN)
        self.spinbox_ipmin_box = QDoubleSpinBox()
        self.spinbox_ipmin_box.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_ipmin_box.setRange(SPINBOX_RANGE_MIN, SPINBOX_RANGE_MAX)
        self.label_ipmax_box = QLabel(LABEL_MAX)
        self.spinbox_ipmax_box = QDoubleSpinBox()
        self.spinbox_ipmax_box.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_ipmax_box.setRange(SPINBOX_RANGE_MIN, SPINBOX_RANGE_MAX)

        self.hbox_box_ip.addWidget(self.label_iprange_box)
        self.hbox_box_ip.addWidget(self.spinbox_ipmin_box)
        self.hbox_box_ip.addWidget(self.spinbox_ipmax_box)

        self.spinbox_ipmin_box.setMaximumWidth(WIDTH_SPINBOX_MAX)
        self.spinbox_ipmax_box.setMaximumWidth(WIDTH_SPINBOX_MAX)

        self.label_ooprange_box = QLabel(LABEL_BOX_OOP_RANGE)
        self.label_oopmin_box = QLabel(LABEL_MIN)
        self.spinbox_oopmin_box = QDoubleSpinBox()
        self.spinbox_oopmin_box.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_oopmin_box.setRange(SPINBOX_RANGE_MIN, SPINBOX_RANGE_MAX)
        self.label_oopmax_box = QLabel(LABEL_MAX)
        self.spinbox_oopmax_box = QDoubleSpinBox()
        self.spinbox_oopmax_box.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_oopmax_box.setRange(SPINBOX_RANGE_MIN, SPINBOX_RANGE_MAX)

        self.hbox_box_oop.addWidget(self.label_ooprange_box)
        self.hbox_box_oop.addWidget(self.spinbox_oopmin_box)
        self.hbox_box_oop.addWidget(self.spinbox_oopmax_box)

        self.spinbox_oopmin_box.setMaximumWidth(WIDTH_SPINBOX_MAX)
        self.spinbox_oopmax_box.setMaximumWidth(WIDTH_SPINBOX_MAX)

        self.label_outputunits_box = QLabel(LABEL_BOX_OUTPUT_UNITS)  
        self.combobox_outputunits_box = QComboBox()
        for unit in DICT_UNIT_ALIAS.values():
            self.combobox_outputunits_box.addItem(unit)
        
        self.hbox_box_unit_output.addWidget(self.label_outputunits_box, Qt.AlignLeft)
        self.hbox_box_unit_output.addWidget(self.combobox_outputunits_box, Qt.AlignLeft)

        self.hbox_box_unit_output.setStretch(1,10)

        # PONI PARAMETERS TAB

        self.hbox_poni_mod = QHBoxLayout()
        self.hbox_poni_mod.setContentsMargins(1,0,1,0)
        self.hbox_poni_wave = QHBoxLayout()
        self.hbox_poni_wave.setContentsMargins(1,0,1,0)
        self.hbox_poni_dist = QHBoxLayout()
        self.hbox_poni_dist.setContentsMargins(1,0,1,0)
        self.hbox_poni_detector = QHBoxLayout()
        self.hbox_poni_detector.setContentsMargins(1,0,1,0)
        self.hbox_poni_poni_1 = QHBoxLayout()
        self.hbox_poni_poni_1.setContentsMargins(1,0,1,0)
        self.hbox_poni_poni_2 = QHBoxLayout()
        self.hbox_poni_poni_2.setContentsMargins(1,0,1,0)
        self.hbox_poni_rot_1 = QHBoxLayout()
        self.hbox_poni_rot_1.setContentsMargins(1,0,1,0)
        self.hbox_poni_rot_2 = QHBoxLayout()
        self.hbox_poni_rot_2.setContentsMargins(1,0,1,0)
        self.hbox_poni_rot_3 = QHBoxLayout()
        self.hbox_poni_rot_3.setContentsMargins(1,0,1,0)
        self.hbox_poni_buttons = QHBoxLayout()
        self.hbox_poni_buttons.setContentsMargins(1,0,1,0)

        self.widget_poni_mod = QWidget()
        self.widget_poni_wave = QWidget()
        self.widget_poni_dist = QWidget()
        self.widget_poni_detector = QWidget()
        self.widget_poni_poni_1 = QWidget()
        self.widget_poni_poni_2 = QWidget()
        self.widget_poni_rot_1 = QWidget()
        self.widget_poni_rot_2 = QWidget()
        self.widget_poni_rot_3 = QWidget()
        self.widget_poni_buttons = QWidget()

        self.widget_poni_mod.setLayout(self.hbox_poni_mod)
        self.widget_poni_wave.setLayout(self.hbox_poni_wave)
        self.widget_poni_dist.setLayout(self.hbox_poni_dist)
        self.widget_poni_detector.setLayout(self.hbox_poni_detector)
        self.widget_poni_poni_1.setLayout(self.hbox_poni_poni_1)
        self.widget_poni_poni_2.setLayout(self.hbox_poni_poni_2)
        self.widget_poni_rot_1.setLayout(self.hbox_poni_rot_1)
        self.widget_poni_rot_2.setLayout(self.hbox_poni_rot_2)
        self.widget_poni_rot_3.setLayout(self.hbox_poni_rot_3)
        self.widget_poni_buttons.setLayout(self.hbox_poni_buttons)

        self.checkbox_poni_mod = QCheckBox(LABEL_PONI_MOD)

        self.hbox_poni_mod.addWidget(self.checkbox_poni_mod)

        self.label_wavelength = QLabel(LABEL_PONI_WAVELENGTH)
        self.lineedit_wavelength = QLineEdit()
        self.lineedit_wavelength.setEnabled(False)
        self.label_distance = QLabel(LABEL_DISTANCE)
        self.lineedit_distance = QLineEdit()
        self.lineedit_distance.setEnabled(False)

        self.hbox_poni_wave.addWidget(self.label_wavelength)
        self.hbox_poni_wave.addWidget(self.lineedit_wavelength)
        self.hbox_poni_dist.addWidget(self.label_distance)
        self.hbox_poni_dist.addWidget(self.lineedit_distance)

        self.label_detector = QLabel(LABEL_DETECTOR)
        self.lineedit_detector = QLineEdit()
        self.lineedit_detector.setEnabled(False)

        self.hbox_poni_detector.addWidget(self.label_detector)
        self.hbox_poni_detector.addWidget(self.lineedit_detector)

        self.label_poni_1 = QLabel(LABEL_PONI_PONI_1)
        self.lineedit_poni1 = QLineEdit()   

        self.label_poni_2 = QLabel(LABEL_PONI_PONI_2)
        self.lineedit_poni2 = QLineEdit()
        self.lineedit_poni1.setEnabled(False)
        self.lineedit_poni2.setEnabled(False)

        self.hbox_poni_poni_1.addWidget(self.label_poni_1)
        self.hbox_poni_poni_1.addWidget(self.lineedit_poni1)

        self.hbox_poni_poni_2.addWidget(self.label_poni_2)
        self.hbox_poni_poni_2.addWidget(self.lineedit_poni2)

        self.label_rot_1 = QLabel(LABEL_PONI_ROT_1)
        self.lineedit_rot1 = QLineEdit()
        self.label_rot_2 = QLabel(LABEL_PONI_ROT_2)
        self.lineedit_rot2 = QLineEdit()
        self.label_rot_3 = QLabel(LABEL_PONI_ROT_3)
        self.lineedit_rot3 = QLineEdit()
        self.lineedit_rot1.setEnabled(False)
        self.lineedit_rot2.setEnabled(False)
        self.lineedit_rot3.setEnabled(False)

        self.hbox_poni_rot_1.addWidget(self.label_rot_1)
        self.hbox_poni_rot_1.addWidget(self.lineedit_rot1)
        self.hbox_poni_rot_2.addWidget(self.label_rot_2)
        self.hbox_poni_rot_2.addWidget(self.lineedit_rot2)
        self.hbox_poni_rot_3.addWidget(self.label_rot_3)
        self.hbox_poni_rot_3.addWidget(self.lineedit_rot3)

        self.button_update_old_poni_parameters = QPushButton(BUTTON_UPDATE_OLD_PONI_PARAMETERS)
        self.button_update_old_poni_parameters.setStyleSheet(button_style_input)
        self.button_update_poni_parameters = QPushButton(BUTTON_UPDATE_PONI_PARAMETERS)
        self.button_update_poni_parameters.setStyleSheet(button_style_input)
        self.button_save_poni_parameters = QPushButton(BUTTON_SAVE_PONI_PARAMETERS)
        self.button_save_poni_parameters.setStyleSheet(button_style_input)

        self.hbox_poni_buttons.addWidget(self.button_update_old_poni_parameters)
        self.hbox_poni_buttons.addWidget(self.button_update_poni_parameters)
        self.hbox_poni_buttons.addWidget(self.button_save_poni_parameters)

        self.vbox_poni.addWidget(self.widget_poni_mod)
        self.vbox_poni.addWidget(self.widget_poni_wave)
        self.vbox_poni.addWidget(self.widget_poni_dist)
        self.vbox_poni.addWidget(self.widget_poni_detector)
        self.vbox_poni.addWidget(self.widget_poni_poni_1)
        self.vbox_poni.addWidget(self.widget_poni_poni_2)
        self.vbox_poni.addWidget(self.widget_poni_rot_1)
        self.vbox_poni.addWidget(self.widget_poni_rot_2)
        self.vbox_poni.addWidget(self.widget_poni_rot_3)
        self.vbox_poni.addWidget(self.widget_poni_buttons)

        #######################################
        ####### SPLITTER FOLDER-FILES##########
        #######################################

        self.listwidget_folders = QListWidget()

        self.widget_folder_tab.addTab(self.listwidget_folders, LABEL_LIST_FOLDERS)

        self.vbox_files = QVBoxLayout()
        self.widget_files = QWidget()
        self.widget_files.setLayout(self.vbox_files)

        self.widget_file_tab.addTab(self.widget_files, LABEL_LIST_FILES)

        self.hbox_metadata_items = QHBoxLayout()
        self.widget_metadata_items = QWidget()
        self.widget_metadata_items.setLayout(self.hbox_metadata_items)

        self.label_headeritems = QLabel(LABEL_METADATA)
        self.combobox_headeritems = QComboBox()
        self.lineedit_headeritems = QLineEdit()

        self.hbox_metadata_items.addWidget(self.label_headeritems)
        self.hbox_metadata_items.addWidget(self.combobox_headeritems)
        self.hbox_metadata_items.addWidget(self.lineedit_headeritems)

        self.table_files = QTableWidget()

        self.vbox_files.addWidget(self.widget_metadata_items)
        self.vbox_files.addWidget(self.table_files)

        #######################################
        ########## LABEL TITLE      ###########
        #######################################

        self.label_filename = QLabel(LABEL_FILENAME)
        self.lineedit_filename = QLineEdit()
        self.lineedit_filename.setEnabled(False)

        self.hbox_top_label.addWidget(self.label_filename)
        self.hbox_top_label.addWidget(self.lineedit_filename)

        #######################################
        ########## SPLITTER GRAPHS  ###########
        #######################################

        self.tab_graph_widget = QTabWidget()
        self.tab_chart_widget = QTabWidget()

        self.splitter_graphs.addWidget(self.tab_graph_widget)
        self.splitter_graphs.addWidget(self.tab_chart_widget)

        # 2D GRAPHS
        self.graph_raw_widget = Plot2D()
        self.tab_graph_widget.addTab(self.graph_raw_widget, LABEL_RAW_MAP)

        self.vbox_reshape = QVBoxLayout()
        self.widget_reshape = QWidget()
        self.widget_reshape.setLayout(self.vbox_reshape)

        self.canvas_reshape_widget = MplCanvas(self, width=4, height=3, dpi=50)
        self.toolbar_reshape_matplotlib = NavigationToolbar2QT(self.canvas_reshape_widget, self)

        self.vbox_reshape.addWidget(self.toolbar_reshape_matplotlib)
        self.vbox_reshape.addWidget(self.canvas_reshape_widget)

        self.tab_graph_widget.addTab(self.widget_reshape, LABEL_RESHAPE_MAP)

        self.vbox_graph_q = QVBoxLayout()
        self.widget_graph_q = QWidget()
        self.widget_graph_q.setLayout(self.vbox_graph_q)

        self.tab_graph_widget.addTab(self.widget_graph_q, LABEL_Q_MAP)

        self.hbox_graph_toolbar_1 = QHBoxLayout()
        self.hbox_graph_toolbar_2 = QHBoxLayout()
        self.hbox_graph_toolbar_3 = QHBoxLayout()

        self.widget_graph_toolbar_1 = QWidget()
        self.widget_graph_toolbar_2 = QWidget()
        self.widget_graph_toolbar_3 = QWidget()

        self.widget_graph_toolbar_1.setLayout(self.hbox_graph_toolbar_1)
        self.widget_graph_toolbar_2.setLayout(self.hbox_graph_toolbar_2)
        self.widget_graph_toolbar_3.setLayout(self.hbox_graph_toolbar_3)

        self.label_units = QLabel(LABEL_MAP_UNITS)
        self.combobox_units = QComboBox()
        for unit in DICT_UNIT_ALIAS.values():
            self.combobox_units.addItem(unit)
        self.button_log = QPushButton(BUTTON_LOG)
        self.button_log.setStyleSheet(button_on)
        self.button_colorbar = QPushButton(BUTTON_COLORBAR)
        self.button_colorbar.setStyleSheet(button_on)
        self.button_default_graph = QPushButton(BUTTON_AUTO)
        self.button_default_graph.setStyleSheet(button_on)
        self.label_title = QLabel(LABEL_MAP_TITLES)
        self.combobox_headeritems_title = QComboBox()
        self.lineedit_headeritems_title = QLineEdit()
        self.button_reshape_map = QPushButton(BUTTON_SHOW_RESHAPE)
        self.button_reshape_map.setStyleSheet(button_style_thin)

        self.hbox_graph_toolbar_1.addWidget(self.label_units)
        self.hbox_graph_toolbar_1.addWidget(self.combobox_units)
        self.hbox_graph_toolbar_1.addWidget(self.label_title)
        self.hbox_graph_toolbar_1.addWidget(self.combobox_headeritems_title)
        self.hbox_graph_toolbar_1.addWidget(self.lineedit_headeritems_title)

        # self.xlims = QLabel(LABEL_XLIMS)
        # self.lineedit_xmin = QLineEdit()
        # self.lineedit_xmin.setEnabled(False)
        # self.lineedit_xmax = QLineEdit()
        # self.lineedit_xmax.setEnabled(False)
        # self.ylims = QLabel(LABEL_YLIMS)
        # self.lineedit_ymin = QLineEdit()
        # self.lineedit_ymin.setEnabled(False)
        # self.lineedit_ymax = QLineEdit()
        # self.lineedit_ymax.setEnabled(False)

        self.button_font_m = QPushButton(BUTTON_LABEL_MINUS)
        self.button_font_m.setStyleSheet(button_style_thin)
        self.button_font_M = QPushButton(BUTTON_LABEL_PLUS)
        self.button_font_M.setStyleSheet(button_style_thin)
        self.button_reduce_comma = QPushButton(BUTTON_COMMA_MINUS)
        self.button_reduce_comma.setStyleSheet(button_style_thin)
        self.button_enhance_comma = QPushButton(BUTTON_COMMA_PLUS)
        self.button_enhance_comma.setStyleSheet(button_style_thin)
        self.button_log = QPushButton(BUTTON_LOG)
        self.button_log.setStyleSheet(button_style_thin)
        self.label_binning_data = QLabel(LABEL_BINNING_DATA)
        self.spinbox_binnning_data = QSpinBox()
        self.spinbox_binnning_data.setValue(DEFAULT_BINNING)
        self.spinbox_binnning_data.setSingleStep(BINNING_STEP)
        self.spinbox_binnning_data.setRange(BINNING_RANGE_MIN, BINNING_RANGE_MAX)
        self.button_savemap = QPushButton(BUTTON_SAVE_QMAP)
        self.button_savemap.setStyleSheet(button_style_thin)

        self.hbox_graph_toolbar_2.addWidget(self.button_font_m)
        self.hbox_graph_toolbar_2.addWidget(self.button_font_M)
        self.hbox_graph_toolbar_2.addWidget(self.button_reduce_comma)
        self.hbox_graph_toolbar_2.addWidget(self.button_enhance_comma)
        self.hbox_graph_toolbar_2.addWidget(self.button_log)
        self.hbox_graph_toolbar_2.addWidget(self.label_binning_data)
        self.hbox_graph_toolbar_2.addWidget(self.spinbox_binnning_data)
        # self.hbox_graph_toolbar_2.addWidget(self.button_savemap)

        self.label_xticks = QLabel(LABEL_XTICKS)
        self.lineedit_xticks = QLineEdit()
        self.label_yticks = QLabel(LABEL_YTICKS)
        self.lineedit_yticks = QLineEdit()

        self.hbox_graph_toolbar_3.addWidget(self.label_xticks)
        self.hbox_graph_toolbar_3.addWidget(self.lineedit_xticks)
        self.hbox_graph_toolbar_3.addWidget(self.label_yticks)
        self.hbox_graph_toolbar_3.addWidget(self.lineedit_yticks)

        self.canvas_2d_q = MplCanvas(self, width=4, height=3, dpi=50)
        self.toolbar_q_matplotlib = NavigationToolbar2QT(self.canvas_2d_q, self)

        self.vbox_graph_q.addWidget(self.widget_graph_toolbar_1)
        self.vbox_graph_q.addWidget(self.widget_graph_toolbar_3)
        self.vbox_graph_q.addWidget(self.widget_graph_toolbar_2)
        self.vbox_graph_q.addWidget(self.toolbar_q_matplotlib)
        self.vbox_graph_q.addWidget(self.canvas_2d_q)

        self.vbox_graph_q.setStretch(4,20)

        self.hbox_graph_toolbar_1.setContentsMargins(1,1,1,0)
        self.hbox_graph_toolbar_2.setContentsMargins(1,0,1,0)
        self.hbox_graph_toolbar_3.setContentsMargins(1,0,1,0)
        self.toolbar_q_matplotlib.setContentsMargins(1,0,1,0)
        self.canvas_2d_q.setContentsMargins(1,0,1,0)

        # 1D CHART
        self.vbox_chart = QVBoxLayout()
        self.widget_chart = QWidget()
        self.widget_chart.setLayout(self.vbox_chart)

        self.tab_chart_widget.addTab(self.widget_chart, LABEL_TAB_1D_INT)

        self.hbox_chart_toolbar_1 = QHBoxLayout()
        self.hbox_chart_toolbar_2 = QHBoxLayout()
        self.hbox_chart_toolbar_3 = QHBoxLayout()
        self.hbox_savefolder = QHBoxLayout()

        self.widget_chart_toolbar_1 = QWidget()
        self.widget_chart_toolbar_2 = QWidget()
        self.widget_chart_toolbar_3 = QWidget()
        self.widget_savefolder = QWidget()

        self.widget_chart_toolbar_1.setLayout(self.hbox_chart_toolbar_1)
        self.widget_chart_toolbar_2.setLayout(self.hbox_chart_toolbar_2)
        self.widget_savefolder.setLayout(self.hbox_savefolder)        
        self.widget_chart_toolbar_3.setLayout(self.hbox_chart_toolbar_3)

        self.label_integrations = QLabel(LABEL_INTEGRATIONS)
        self.combobox_integration = QComboBox()
        self.lineedit_integrations = QLineEdit()
        self.checkbox_mask_integration = QCheckBox(LABEL_MASK_MAP)

        self.hbox_chart_toolbar_1.addWidget(self.label_integrations)
        self.hbox_chart_toolbar_1.addWidget(self.combobox_integration)
        self.hbox_chart_toolbar_1.addWidget(self.lineedit_integrations)
        self.hbox_chart_toolbar_1.addWidget(self.checkbox_mask_integration)

        self.label_sub = QLabel(LABEL_SUB_FACTOR)
        self.spinbox_sub = QDoubleSpinBox()
        self.spinbox_sub.setSingleStep(STEP_SUB_SPINBOX)
        self.button_clearplot = QPushButton(BUTTON_CLEAR_PLOT)
        self.button_clearplot.setStyleSheet(button_style_thin)
        self.button_saveplot = QPushButton(BUTTON_SAVE_INTEGRATIONS)
        self.button_saveplot.setStyleSheet(button_style_thin)        
        self.button_batch = QPushButton(BUTTON_BATCH)
        self.button_batch.setStyleSheet(button_style_thin) 

        self.hbox_chart_toolbar_2.addWidget(self.label_sub)
        self.hbox_chart_toolbar_2.addWidget(self.spinbox_sub)
        self.hbox_chart_toolbar_2.addWidget(self.button_clearplot)
        self.hbox_chart_toolbar_2.addWidget(self.button_saveplot)
        self.hbox_chart_toolbar_2.addWidget(self.button_batch)

        self.label_savefolder = QLabel(LABEL_SAVE_FOLDER)
        self.lineedit_savefolder = QLineEdit()

        self.hbox_savefolder.addWidget(self.label_savefolder)
        self.hbox_savefolder.addWidget(self.lineedit_savefolder)

        self.graph_1D_widget = Plot1D()

        self.vbox_chart.addWidget(self.widget_chart_toolbar_1)
        self.vbox_chart.addWidget(self.widget_savefolder)        
        self.vbox_chart.addWidget(self.widget_chart_toolbar_2)
        self.vbox_chart.addWidget(self.graph_1D_widget)

        self.vbox_chart.setStretch(3,20)

        self.hbox_chart_toolbar_1.setContentsMargins(1,1,1,0)
        self.hbox_chart_toolbar_2.setContentsMargins(1,0,1,0)
        self.hbox_savefolder.setContentsMargins(1, 0, 1, 0)
        self.graph_1D_widget.setContentsMargins(1,0,1,0)

        #######################################
        ########## TERMINAL OUTPUT  ###########
        #######################################

        self.plaintext_output = QPlainTextEdit()
        self.plaintext_output.setReadOnly(True)
        self.widget_terminal_tab.addTab(self.plaintext_output, LABEL_TERMINAL)

        self.hbox_terminal_top = QHBoxLayout()
        self.widget_terminal_top = QWidget()
        self.widget_terminal_top.setLayout(self.hbox_terminal_top)

        self.label_plaintext = QLabel(LABEL_TERMINAL)
        self.label_plaintext.setStyleSheet("background-color: white;border: 1px solid black;")
        self.label_plaintext.setAlignment(Qt.AlignCenter)
        self.button_hide_terminal = QPushButton(BUTTON_HIDE_TERMINAL)
        self.button_hide_terminal.setStyleSheet(button_on)

       


        # set_bstyle([self.label_poni_warning, self.label_headeritems, self.label_plaintext, self.xlims, self.ylims, self.label_units, self.xticks, self.yticks, self.label_savefolder, self.label_integrations, self.label_sub, self.label_title,self.label_input_graph,self.label_input_chart])
        # set_bstyle([self.label_setup, self.label_angle, self.label_tilt_angle, self.label_normfactor, self.label_exposure, self.label_setup_name])
        # set_bstyle([self.label_name_cake, self.label_suffix_cake, self.label_type_cake, self.label_units_cake, self.label_radialrange_cake, self.label_azimrange_cake, self.label_azimbins_cake])
        # set_bstyle([self.label_name_box, self.label_suffix_box, self.label_direction_box, self.label_input_units_box, self.label_iprange_box, self.label_ooprange_box, self.label_outputunits_box])
        # set_bstyle([self.label_binning_data])