
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QListWidget, QTableWidget, QLabel, QComboBox
from PyQt5.QtWidgets import QCheckBox, QLineEdit, QDoubleSpinBox, QPlainTextEdit, QTabWidget, QSpinBox, QSplitter, QHBoxLayout, QVBoxLayout, QFrame
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from silx.gui.plot.PlotWindow import Plot1D, Plot2D

from pyxscat.edf import DICT_SAMPLE_ORIENTATIONS
from pyxscat.other.units import DICT_UNIT_ALIAS, CAKE_INTEGRATIONS, BOX_INTEGRATIONS
from . import ICON_DIRECTORY

from .multi_combobox import CheckableComboBox


BUTTON_STYLE_ENABLE = """
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

BUTTON_STYLE_DISABLE = """
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



# TABS
LABEL_TAB_FILES = "Setup"
LABEL_TAB_SETUP = "Metadata"
LABEL_TAB_CAKE = "Cake Int."
LABEL_TAB_BOX = "Box Int."
LABEL_TAB_PONIFILE = "Ponifile"
LABEL_TAB_H5 = "HDF5 File"

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

QZ_BUTTON_LABEL = "qz"
QZ_DEFAULT_STATE = True
QR_BUTTON_LABEL = "qr"
QR_DEFAULT_STATE = True
MIRROR_BUTTON_LABEL = "mirror"
MIRROR_DEFAULT_STATE = False
WRONG_LABEL = ""

BUTTON_ORIENTATIONS_LAYOUT = {
    QZ_BUTTON_LABEL : {
        True : {
            "label" : "qz \u2191\u2191",
            "style" : BUTTON_STYLE_ENABLE,
        },
        False : {
            "label" : "qz \u2191\u2193",
            "style" : BUTTON_STYLE_DISABLE,
        },  
    },
    QR_BUTTON_LABEL : {
        True : {
            "label" : "qr \u2191\u2191",
            "style" : BUTTON_STYLE_ENABLE,
        },
        False : {
            "label" : "qr \u2191\u2193",
            "style" : BUTTON_STYLE_DISABLE,
        },  
    },
    MIRROR_BUTTON_LABEL : {
        True : {
            "label" : f"\u2713",
            "style" : BUTTON_STYLE_ENABLE,
        },
        False : {
            "label" : f"\u2716",
            "style" : BUTTON_STYLE_DISABLE,
        },  
    },
}




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

LABEL_H5_H5FILE = "H5 file:"
LABEL_H5_MAINDIR = "Root Directory:"
LABEL_H5_IANGLE_KEY = "Inc. angle (key):"
LABEL_H5_TANGLE_KEY = "Tilt angle (key)"
LABEL_H5_NORM_KEY = "Norm. factor (key)"
LABEL_H5_ACQ_KEY = "Acq. time (key)"
LABEL_H5_NFILES = "Number of files:"

MSG_QZ_DIRECTION_UPDATED = "The qz direction was updated."
MSG_QR_DIRECTION_UPDATED = "The qr direction was updated."
INFO_MIRROR_DISABLE = "Mirror transformation disable."
INFO_MIRROR_ENABLE = "Mirror transformation enable. 2D map has been flipped left-right."


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
        hbox_main = QHBoxLayout()
        self.setLayout(hbox_main)

        vbox_left = QVBoxLayout()
        vbox_right = QVBoxLayout()

        frame_left = QFrame(self)       
        frame_left.setFrameShape(QFrame.StyledPanel)
        frame_left.setLayout(vbox_left)

        frame_right = QFrame(self)       
        frame_right.setFrameShape(QFrame.StyledPanel)
        frame_right.setLayout(vbox_right)

        # Main splitter and two vertical boxes with frames
        splitter_main = QSplitter(orientation=Qt.Horizontal)

        hbox_main.addWidget(splitter_main)        

        splitter_vbox_left = QSplitter(orientation=Qt.Vertical)
        splitter_vbox_right = QSplitter(orientation=Qt.Vertical)

        vbox_left.addWidget(splitter_vbox_left)
        vbox_right.addWidget(splitter_vbox_right)

        splitter_main.addWidget(frame_left)
        splitter_main.addWidget(frame_right)

        splitter_main.setStretchFactor(0, 1)
        splitter_main.setStretchFactor(1, 3)

        vbox_input = QVBoxLayout()
        widget_tabs = QTabWidget()
        widget_tabs.setLayout(vbox_input)
        vbox_list_folder = QVBoxLayout()
        widget_folder_tab = QTabWidget()
        widget_folder_tab.setLayout(vbox_list_folder)
        vbox_table_files = QVBoxLayout()        
        widget_file_tab = QTabWidget()
        widget_file_tab.setLayout(vbox_table_files)

        splitter_vbox_left.addWidget(widget_tabs)
        splitter_vbox_left.addWidget(widget_folder_tab)
        splitter_vbox_left.addWidget(widget_file_tab)

        hbox_top_label = QHBoxLayout()
        hbox_top_label.setContentsMargins(1,0,1,0)
        widget_top_label = QWidget()
        widget_top_label.setLayout(hbox_top_label)
        splitter_graphs = QSplitter()
        vbox_terminal = QVBoxLayout()
        vbox_terminal.setContentsMargins(1,0,1,0)
        widget_terminal_tab = QTabWidget()
        widget_terminal_tab.setLayout(vbox_terminal)

        splitter_vbox_right.addWidget(widget_top_label)
        splitter_vbox_right.addWidget(splitter_graphs)
        splitter_vbox_right.addWidget(widget_terminal_tab)

        splitter_vbox_right.setStretchFactor(0,1)
        splitter_vbox_right.setStretchFactor(1,20)
        splitter_vbox_right.setStretchFactor(2,2)

        #######################################
        ########## WIDGET_TABS ################
        #######################################

        vbox_input = QVBoxLayout()
        vbox_metadata = QVBoxLayout()
        vbox_metadata.setSpacing(0)
        hbox_cake = QHBoxLayout()
        hbox_box = QHBoxLayout()
        vbox_poni = QVBoxLayout()
        vbox_h5 = QVBoxLayout()

        vbox_metadata.setStretch(0,1)
        vbox_metadata.setStretch(1,1)
        vbox_metadata.setStretch(2,1)
        vbox_metadata.setStretch(3,1)
        vbox_metadata.setStretch(4,1)

        widget_vbox_input = QWidget()
        widget_vbox_metadata = QWidget()
        widget_cake = QWidget()
        widget_box = QWidget()
        widget_vbox_poni = QWidget()
        widget_vbox_h5 = QWidget()

        widget_vbox_input.setLayout(vbox_input)        
        widget_vbox_metadata.setLayout(vbox_metadata)
        widget_cake.setLayout(hbox_cake)
        widget_box.setLayout(hbox_box)
        widget_vbox_poni.setLayout(vbox_poni)
        widget_vbox_h5.setLayout(vbox_h5)

        widget_tabs.addTab(widget_vbox_input, LABEL_TAB_FILES)
        widget_tabs.addTab(widget_vbox_metadata, LABEL_TAB_SETUP)
        widget_tabs.addTab(widget_cake, LABEL_TAB_CAKE)
        widget_tabs.addTab(widget_box, LABEL_TAB_BOX)
        widget_tabs.addTab(widget_vbox_poni, LABEL_TAB_PONIFILE)
        widget_tabs.addTab(widget_vbox_h5, LABEL_TAB_H5)

        ### INPUT TAB ###

        hbox_recent_h5 = QHBoxLayout()
        hbox_recent_h5.setContentsMargins(1, 0, 1, 0)
        hbox_maindir = QHBoxLayout()
        hbox_maindir.setContentsMargins(1, 0, 1, 0)
        hbox_pattern = QHBoxLayout()
        hbox_pattern.setContentsMargins(1, 0, 1, 0)
        hbox_poni = QHBoxLayout()
        hbox_poni.setContentsMargins(1, 0, 1, 0)
        hbox_reffolder = QHBoxLayout()
        hbox_reffolder.setContentsMargins(1, 0, 1, 0)
        hbox_reffile = QHBoxLayout()
        hbox_reffile.setContentsMargins(1, 0, 1, 0)

        hbox_sample_orientation = QHBoxLayout()
        hbox_sample_orientation.setContentsMargins(1, 0, 1, 0)
        hbox_pyfai = QHBoxLayout()
        hbox_pyfai.setContentsMargins(1, 0, 1, 0)

        widget_recent_h5 = QWidget()
        widget_maindir = QWidget()
        widget_pattern = QWidget()
        widget_poni = QWidget()
        widget_reffolder = QWidget()
        widget_reffile = QWidget()

        widget_sample_orientation = QWidget()
        widget_pyfai = QWidget()

        widget_recent_h5.setLayout(hbox_recent_h5)
        widget_maindir.setLayout(hbox_maindir)
        widget_pattern.setLayout(hbox_pattern)
        widget_poni.setLayout(hbox_poni)
        widget_reffolder.setLayout(hbox_reffolder)
        widget_reffile.setLayout(hbox_reffile)
        widget_sample_orientation.setLayout(hbox_sample_orientation)
        widget_pyfai.setLayout(hbox_pyfai)

        vbox_input.addWidget(widget_recent_h5)
        vbox_input.addWidget(widget_maindir)
        vbox_input.addWidget(widget_pattern)
        vbox_input.addWidget(widget_poni)
        vbox_input.addWidget(widget_reffolder)
        vbox_input.addWidget(widget_reffile)
        # vbox_input.addWidget(widget_savefolder)
        vbox_input.addWidget(widget_sample_orientation)
        vbox_input.addWidget(widget_pyfai)

        label_recent_h5 = QLabel(LABEL_RECENT_H5)
        self.combobox_h5_files = QComboBox()

        hbox_recent_h5.addWidget(label_recent_h5, Qt.AlignLeft)
        hbox_recent_h5.addWidget(self.combobox_h5_files, Qt.AlignLeft)

        hbox_recent_h5.setStretch(0,1)
        hbox_recent_h5.setStretch(1,10)

        label_h5file = QLabel(LABEL_H5_FILE)
        self.lineedit_h5file = QLineEdit()
        self.lineedit_h5file.setEnabled(False)
        self.button_pick_maindir = QPushButton()
        self.button_pick_maindir.setIcon(QIcon(ICON_FOLDER_PATH))
        self.button_pick_maindir.setToolTip(LABEL_PICK_MAINDIR)    
        self.button_pick_maindir.setStyleSheet(BUTTON_STYLE_ENABLE)    
        self.button_pick_hdf5 = QPushButton()
        self.button_pick_hdf5.setIcon(QIcon(H5_ICON_PATH))
        self.button_pick_hdf5.setToolTip(LABEL_PICK_H5)
        self.button_pick_hdf5.setStyleSheet(BUTTON_STYLE_ENABLE)

        hbox_maindir.addWidget(label_h5file)
        hbox_maindir.addWidget(self.lineedit_h5file)
        hbox_maindir.addWidget(self.button_pick_maindir)
        hbox_maindir.addWidget(self.button_pick_hdf5)

        label_extension = QLabel(LABEL_EXTENSION)
        self.combobox_extension = QComboBox()
        for ext in LIST_EXTENSION:
            self.combobox_extension.addItem(ext)
        label_wildcard = QLabel(LABEL_WILDCARDS)
        self.lineedit_wildcards = QLineEdit(WILDCARDS_DEFAULT)

        hbox_pattern.addWidget(label_extension)
        hbox_pattern.addWidget(self.combobox_extension)
        hbox_pattern.addWidget(label_wildcard)
        hbox_pattern.addWidget(self.lineedit_wildcards)

        label_ponifile = QLabel(LABEL_PONIFILE)
        self.combobox_ponifile = QComboBox()
        self.button_add_ponifile = QPushButton(BUTTON_PONIFILE)
        self.button_add_ponifile.setIcon(QIcon(ICON_FILE_PATH))
        self.button_add_ponifile.setStyleSheet(BUTTON_STYLE_ENABLE)
        self.button_update_ponifile = QPushButton()
        self.button_update_ponifile.setIcon(QIcon(ICON_REFRESH_PATH))
        self.button_update_ponifile.setStyleSheet(BUTTON_STYLE_ENABLE)

        hbox_poni.addWidget(label_ponifile, Qt.AlignLeft)
        hbox_poni.addWidget(self.combobox_ponifile, Qt.AlignLeft)

        hbox_poni.setStretch(0,1)
        hbox_poni.setStretch(1,10)

        label_reffolder = QLabel(LABEL_REFERENCE_FOLDER)
        self.combobox_reffolder = QComboBox()

        hbox_reffolder.addWidget(label_reffolder, Qt.AlignLeft)
        hbox_reffolder.addWidget(self.combobox_reffolder, Qt.AlignLeft)

        hbox_reffolder.setStretch(0,1)
        hbox_reffolder.setStretch(1,10)

        label_reffile = QLabel(LABEL_REFERENCE_FILE)
        self.combobox_reffile = QComboBox()
        self.combobox_reffile.setEnabled(False)
        self.checkbox_auto_reffile = QCheckBox(LABEL_AUTO_REFERENCE)
        self.checkbox_auto_reffile.setChecked(True)

        hbox_reffile.addWidget(label_reffile, Qt.AlignLeft)
        hbox_reffile.addWidget(self.combobox_reffile, Qt.AlignLeft)
        hbox_reffile.addWidget(self.checkbox_auto_reffile, Qt.AlignLeft)

        hbox_reffile.setStretch(0,1)
        hbox_reffile.setStretch(1,10)
        hbox_reffile.setStretch(2,1)

        label_sample_orientation = QLabel(LABEL_SAMPLE_ORIENTATION)
        self.button_mirror = QPushButton(BUTTON_ORIENTATIONS_LAYOUT[MIRROR_BUTTON_LABEL][MIRROR_DEFAULT_STATE]["label"])
        self.button_mirror.setStyleSheet(BUTTON_ORIENTATIONS_LAYOUT[MIRROR_BUTTON_LABEL][MIRROR_DEFAULT_STATE]["style"])        
        BUTTON_ORIENTATIONS_LAYOUT[MIRROR_BUTTON_LABEL]["widget"] = self.button_mirror
        self.button_mirror.setIcon(QIcon(ICON_MIRROR_PATH))
        self.button_mirror.setCheckable(True)
        self.button_mirror.setChecked(MIRROR_DEFAULT_STATE)

        self.button_qz = QPushButton(BUTTON_ORIENTATIONS_LAYOUT[QZ_BUTTON_LABEL][QZ_DEFAULT_STATE]["label"])
        self.button_qz.setStyleSheet(BUTTON_ORIENTATIONS_LAYOUT[QZ_BUTTON_LABEL][QZ_DEFAULT_STATE]["style"])    
        BUTTON_ORIENTATIONS_LAYOUT[QZ_BUTTON_LABEL]["widget"] = self.button_qz
        self.button_qz.setCheckable(True)
        self.button_qz.setChecked(QZ_DEFAULT_STATE)

        self.button_qr = QPushButton(BUTTON_ORIENTATIONS_LAYOUT[QR_BUTTON_LABEL][QR_DEFAULT_STATE]["label"])
        self.button_qr.setStyleSheet(BUTTON_ORIENTATIONS_LAYOUT[QR_BUTTON_LABEL][QR_DEFAULT_STATE]["style"])   
        BUTTON_ORIENTATIONS_LAYOUT[QR_BUTTON_LABEL]["widget"] = self.button_qr
        self.button_qr.setCheckable(True)
        self.button_qr.setChecked(QR_DEFAULT_STATE)
        self.button_qr.setStyleSheet(BUTTON_STYLE_ENABLE)

        hbox_sample_orientation.addWidget(label_sample_orientation)
        hbox_sample_orientation.addWidget(self.button_mirror)
        hbox_sample_orientation.addWidget(self.button_qz)
        hbox_sample_orientation.addWidget(self.button_qr)

        self.button_pyfaicalib = QPushButton(BUTTON_PYFAI_GUI)
        self.button_pyfaicalib.setIcon(QIcon(ICON_PYFAI_PATH))
        self.button_pyfaicalib.setStyleSheet(BUTTON_STYLE_ENABLE)
        self.button_start = QPushButton(BUTTON_UPDATE_DATA)
        self.button_start.setIcon(QIcon(ICON_REFRESH_PATH))
        self.button_start.setStyleSheet(BUTTON_STYLE_ENABLE)
        self.button_live = QPushButton(BUTTON_LIVE)
        self.button_live.setStyleSheet(BUTTON_STYLE_ENABLE)

        hbox_pyfai.addWidget(self.button_pyfaicalib)
        hbox_pyfai.addWidget(self.button_start)
        hbox_pyfai.addWidget(self.button_live)

        ### METADATA TAB ###

        hbox_metadata_choose = QHBoxLayout()
        hbox_metadata_choose.setContentsMargins(1, 0, 1, 0)

        hbox_metadata_iangle = QHBoxLayout()
        hbox_metadata_iangle.setContentsMargins(1, 0, 1, 0)

        hbox_metadata_tangle = QHBoxLayout()
        hbox_metadata_tangle.setContentsMargins(1, 0, 1, 0)

        hbox_metadata_norm = QHBoxLayout()
        hbox_metadata_norm.setContentsMargins(1, 0, 1, 0)

        hbox_metadata_acq = QHBoxLayout()
        hbox_metadata_acq.setContentsMargins(1, 0, 1, 0)

        hbox_metadata_name = QHBoxLayout()
        hbox_metadata_name.setContentsMargins(1, 0, 1, 0)

        widget_metadata_choose = QWidget()
        widget_metadata_iangle = QWidget()
        widget_metadata_tangle = QWidget()
        widget_metadata_norm = QWidget()
        widget_metadata_acq = QWidget()
        widget_metadata_name = QWidget()

        widget_metadata_choose.setLayout(hbox_metadata_choose)
        widget_metadata_iangle.setLayout(hbox_metadata_iangle)
        widget_metadata_tangle.setLayout(hbox_metadata_tangle)
        widget_metadata_norm.setLayout(hbox_metadata_norm)
        widget_metadata_acq.setLayout(hbox_metadata_acq)
        widget_metadata_name.setLayout(hbox_metadata_name)

        label_setup = QLabel(LABEL_DICT_SETUP)
        self.combobox_setup = QComboBox()
        self.button_pick_json = QPushButton(BUTTON_PICK_JSON)
        self.button_pick_json.setStyleSheet(BUTTON_STYLE_ENABLE)

        hbox_metadata_choose.addWidget(label_setup, Qt.AlignLeft)
        hbox_metadata_choose.addWidget(self.combobox_setup, Qt.AlignLeft)
        hbox_metadata_choose.addWidget(self.button_pick_json, Qt.AlignLeft)

        hbox_metadata_choose.setStretch(1,10)

        label_angle = QLabel(LABEL_IANGLE)
        self.lineedit_angle = QLineEdit()
        self.combobox_angle = QComboBox()

        hbox_metadata_iangle.addWidget(label_angle)
        hbox_metadata_iangle.addWidget(self.lineedit_angle)
        hbox_metadata_iangle.addWidget(self.combobox_angle)

        label_tilt_angle = QLabel(LABEL_TILTANGLE)
        self.lineedit_tilt_angle = QLineEdit()
        self.combobox_tilt_angle = QComboBox()

        hbox_metadata_tangle.addWidget(label_tilt_angle)
        hbox_metadata_tangle.addWidget(self.lineedit_tilt_angle)
        hbox_metadata_tangle.addWidget(self.combobox_tilt_angle)

        label_normfactor = QLabel(LABEL_NORMFACTOR)
        self.lineedit_normfactor = QLineEdit()
        self.combobox_normfactor = QComboBox()

        hbox_metadata_norm.addWidget(label_normfactor)
        hbox_metadata_norm.addWidget(self.lineedit_normfactor)
        hbox_metadata_norm.addWidget(self.combobox_normfactor)

        label_exposure = QLabel(LABEL_EXPOSURE)
        self.lineedit_exposure = QLineEdit()
        self.combobox_exposure = QComboBox()

        hbox_metadata_acq.addWidget(label_exposure)
        hbox_metadata_acq.addWidget(self.lineedit_exposure)
        hbox_metadata_acq.addWidget(self.combobox_exposure)

        label_setup_name = QLabel(LABEL_SETUP_NAME)
        self.lineedit_setup_name = QLineEdit()   
        self.button_metadata_save = QPushButton(BUTTON_JSON_FILE)
        self.button_metadata_save.setStyleSheet(BUTTON_STYLE_ENABLE)
        self.button_metadata_save.setIcon(QIcon(ICON_SAVE_PATH))

        hbox_metadata_name.addWidget(label_setup_name)
        hbox_metadata_name.addWidget(self.lineedit_setup_name)
        hbox_metadata_name.addWidget(self.button_metadata_save)

        self.button_metadata_update = QPushButton(BUTTON_UPDATE_KEYS)
        self.button_metadata_update.setStyleSheet(BUTTON_STYLE_ENABLE)

        vbox_metadata.addWidget(widget_metadata_choose)
        vbox_metadata.addWidget(widget_metadata_iangle)
        vbox_metadata.addWidget(widget_metadata_tangle)
        vbox_metadata.addWidget(widget_metadata_norm)
        vbox_metadata.addWidget(widget_metadata_acq)
        vbox_metadata.addWidget(widget_metadata_name)
        vbox_metadata.addWidget(self.button_metadata_update)

        ## CAKE INTEGRATION TAB

        vbox_cake_parameters = QVBoxLayout()
        widget_cake_parameters = QWidget()
        widget_cake_parameters.setLayout(vbox_cake_parameters)
        self.list_cakes = QListWidget()

        hbox_cake.setStretch(0,1)
        hbox_cake.setStretch(1,10)

        hbox_cake.addWidget(widget_cake_parameters)
        hbox_cake.addWidget(self.list_cakes)
    
        hbox_cake_name = QHBoxLayout()
        hbox_cake_name.setContentsMargins(1, 0, 1, 0)
        hbox_cake_suffix = QHBoxLayout()
        hbox_cake_suffix.setContentsMargins(1, 0, 1, 0)
        hbox_cake_type = QHBoxLayout()
        hbox_cake_type.setContentsMargins(1, 0, 1, 0)
        hbox_cake_unit = QHBoxLayout()
        hbox_cake_unit.setContentsMargins(1, 0, 1, 0)
        hbox_cake_radial = QHBoxLayout()
        hbox_cake_radial.setContentsMargins(1, 0, 1, 0)
        hbox_cake_azimut = QHBoxLayout()
        hbox_cake_azimut.setContentsMargins(1, 0, 1, 0)
        hbox_cake_bins = QHBoxLayout()
        hbox_cake_bins.setContentsMargins(1, 0, 1, 0)

        widget_cake_name = QWidget()
        widget_cake_suffix = QWidget()
        widget_cake_type = QWidget()
        widget_cake_unit = QWidget()
        widget_cake_radial = QWidget()
        widget_cake_azimut = QWidget()
        widget_cake_bins = QWidget()

        widget_cake_name.setLayout(hbox_cake_name)
        widget_cake_suffix.setLayout(hbox_cake_suffix)
        widget_cake_type.setLayout(hbox_cake_type)
        widget_cake_unit.setLayout(hbox_cake_unit)
        widget_cake_radial.setLayout(hbox_cake_radial)
        widget_cake_azimut.setLayout(hbox_cake_azimut)
        widget_cake_bins.setLayout(hbox_cake_bins)

        vbox_cake_parameters.addWidget(widget_cake_name)
        vbox_cake_parameters.addWidget(widget_cake_suffix)
        vbox_cake_parameters.addWidget(widget_cake_type)
        vbox_cake_parameters.addWidget(widget_cake_unit)
        vbox_cake_parameters.addWidget(widget_cake_radial)
        vbox_cake_parameters.addWidget(widget_cake_azimut)
        vbox_cake_parameters.addWidget(widget_cake_bins)

        label_name_cake = QLabel(LABEL_CAKE_NAME)
        self.lineedit_name_cake = QLineEdit()

        hbox_cake_name.addWidget(label_name_cake)
        hbox_cake_name.addWidget(self.lineedit_name_cake)

        label_suffix_cake = QLabel(LABEL_CAKE_SUFFIX)
        self.lineedit_suffix_cake = QLineEdit()

        hbox_cake_suffix.addWidget(label_suffix_cake)
        hbox_cake_suffix.addWidget(self.lineedit_suffix_cake)

        label_type_cake = QLabel(LABEL_CAKE_TYPE)
        self.combobox_type_cake = QComboBox()
        for cake_int in CAKE_INTEGRATIONS:
            self.combobox_type_cake.addItem(cake_int)

        hbox_cake_type.addWidget(label_type_cake, Qt.AlignLeft)
        hbox_cake_type.addWidget(self.combobox_type_cake, Qt.AlignLeft)

        hbox_cake_type.setStretch(1,10)

        label_units_cake = QLabel(LABEL_CAKE_UNITS)
        self.combobox_units_cake = QComboBox()
        for unit in DICT_UNIT_ALIAS.values():
            self.combobox_units_cake.addItem(unit)

        hbox_cake_unit.addWidget(label_units_cake, Qt.AlignLeft)
        hbox_cake_unit.addWidget(self.combobox_units_cake, Qt.AlignLeft)

        hbox_cake_unit.setStretch(1,10)

        label_radialrange_cake = QLabel(LABEL_CAKE_RADIAL)
        self.spinbox_radialmin_cake = QDoubleSpinBox()
        self.spinbox_radialmin_cake.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_radialmin_cake.setRange(SPINBOX_RADIAL_MIN, SPINBOX_RADIAL_MAX)
        self.spinbox_radialmax_cake = QDoubleSpinBox()
        self.spinbox_radialmax_cake.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_radialmax_cake.setRange(SPINBOX_RADIAL_MIN, SPINBOX_RADIAL_MAX)
        
        hbox_cake_radial.addWidget(label_radialrange_cake)
        hbox_cake_radial.addWidget(self.spinbox_radialmin_cake)
        hbox_cake_radial.addWidget(self.spinbox_radialmax_cake)
        
        self.spinbox_radialmin_cake.setMaximumWidth(WIDTH_SPINBOX_MAX)
        self.spinbox_radialmax_cake.setMaximumWidth(WIDTH_SPINBOX_MAX)

        label_azimrange_cake = QLabel(LABEL_CAKE_AZIM)
        self.spinbox_azimmin_cake = QDoubleSpinBox()
        self.spinbox_azimmin_cake.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_azimmin_cake.setRange(SPINBOX_AZIM_MIN, SPINBOX_AZIM_MAX)
        self.spinbox_azimmax_cake = QDoubleSpinBox()
        self.spinbox_azimmax_cake.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_azimmax_cake.setRange(SPINBOX_AZIM_MIN, SPINBOX_AZIM_MAX)
        
        hbox_cake_azimut.addWidget(label_azimrange_cake)
        hbox_cake_azimut.addWidget(self.spinbox_azimmin_cake)
        hbox_cake_azimut.addWidget(self.spinbox_azimmax_cake)

        self.spinbox_azimmin_cake.setMaximumWidth(WIDTH_SPINBOX_MAX)
        self.spinbox_azimmax_cake.setMaximumWidth(WIDTH_SPINBOX_MAX)
        
        self.label_azimbins_cake = QLabel(LABEL_CAKE_BINS_OPT)
        self.spinbox_azimbins_cake = QDoubleSpinBox()
        self.spinbox_azimbins_cake.setSingleStep(1)
        self.spinbox_azimbins_cake.setRange(0, 1e9)

        hbox_cake_bins.addWidget(self.label_azimbins_cake)
        hbox_cake_bins.addWidget(self.spinbox_azimbins_cake)

        # BOX INTEGRATION TAB

        vbox_box_parameters = QVBoxLayout()
        widget_box_parameters = QWidget()
        widget_box_parameters.setLayout(vbox_box_parameters)
        self.list_box = QListWidget()

        hbox_box.addWidget(widget_box_parameters)
        hbox_box.addWidget(self.list_box)

        hbox_box_name = QHBoxLayout()
        hbox_box_name.setContentsMargins(1, 0, 1, 0)
        hbox_box_suffix = QHBoxLayout()
        hbox_box_suffix.setContentsMargins(1, 0, 1, 0)
        hbox_box_direction = QHBoxLayout()
        hbox_box_direction.setContentsMargins(1, 0, 1, 0)
        hbox_box_unit_input = QHBoxLayout()
        hbox_box_unit_input.setContentsMargins(1, 0, 1, 0)
        hbox_box_ip = QHBoxLayout()
        hbox_box_ip.setContentsMargins(1, 0, 1, 0)
        hbox_box_oop = QHBoxLayout()
        hbox_box_oop.setContentsMargins(1, 0, 1, 0)
        hbox_box_unit_output = QHBoxLayout()
        hbox_box_unit_output.setContentsMargins(1, 0, 1, 0)

        widget_box_name = QWidget()
        widget_box_suffix = QWidget()
        widget_box_direction = QWidget()
        widget_box_unit_input = QWidget()
        widget_box_ip = QWidget()
        widget_box_oop = QWidget()
        widget_box_unit_output = QWidget()

        widget_box_name.setLayout(hbox_box_name)
        widget_box_suffix.setLayout(hbox_box_suffix)
        widget_box_direction.setLayout(hbox_box_direction)
        widget_box_unit_input.setLayout(hbox_box_unit_input)
        widget_box_ip.setLayout(hbox_box_ip)
        widget_box_oop.setLayout(hbox_box_oop)
        widget_box_unit_output.setLayout(hbox_box_unit_output)

        vbox_box_parameters.addWidget(widget_box_name)
        vbox_box_parameters.addWidget(widget_box_suffix)
        vbox_box_parameters.addWidget(widget_box_direction)
        vbox_box_parameters.addWidget(widget_box_unit_input)
        vbox_box_parameters.addWidget(widget_box_ip)
        vbox_box_parameters.addWidget(widget_box_oop)
        vbox_box_parameters.addWidget(widget_box_unit_output)

        label_name_box = QLabel(LABEL_BOX_NAME)
        self.lineedit_name_box = QLineEdit()

        hbox_box_name.addWidget(label_name_box)
        hbox_box_name.addWidget(self.lineedit_name_box)

        label_suffix_box = QLabel(LABEL_BOX_SUFFIX)
        self.lineedit_suffix_box = QLineEdit()

        hbox_box_suffix.addWidget(label_suffix_box)
        hbox_box_suffix.addWidget(self.lineedit_suffix_box)

        label_direction_box = QLabel(LABEL_BOX_DIRECTION)
        self.combobox_direction_box = QComboBox()
        for box in BOX_INTEGRATIONS:
            self.combobox_direction_box.addItem(box)

        hbox_box_direction.addWidget(label_direction_box, Qt.AlignLeft)
        hbox_box_direction.addWidget(self.combobox_direction_box, Qt.AlignLeft)

        hbox_box_direction.setStretch(1,10)

        label_input_units_box = QLabel(LABEL_BOX_INPUT_UNITS)
        self.combobox_units_box = QComboBox()
        for unit in DICT_UNIT_ALIAS.values():
            self.combobox_units_box.addItem(unit)

        hbox_box_unit_input.addWidget(label_input_units_box, Qt.AlignLeft)
        hbox_box_unit_input.addWidget(self.combobox_units_box, Qt.AlignLeft)

        hbox_box_unit_input.setStretch(1,10)

        label_iprange_box = QLabel(LABEL_BOX_IP_RANGE)
        self.spinbox_ipmin_box = QDoubleSpinBox()
        self.spinbox_ipmin_box.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_ipmin_box.setRange(SPINBOX_RANGE_MIN, SPINBOX_RANGE_MAX)
        self.spinbox_ipmax_box = QDoubleSpinBox()
        self.spinbox_ipmax_box.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_ipmax_box.setRange(SPINBOX_RANGE_MIN, SPINBOX_RANGE_MAX)

        hbox_box_ip.addWidget(label_iprange_box)
        hbox_box_ip.addWidget(self.spinbox_ipmin_box)
        hbox_box_ip.addWidget(self.spinbox_ipmax_box)

        self.spinbox_ipmin_box.setMaximumWidth(WIDTH_SPINBOX_MAX)
        self.spinbox_ipmax_box.setMaximumWidth(WIDTH_SPINBOX_MAX)

        label_ooprange_box = QLabel(LABEL_BOX_OOP_RANGE)
        self.spinbox_oopmin_box = QDoubleSpinBox()
        self.spinbox_oopmin_box.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_oopmin_box.setRange(SPINBOX_RANGE_MIN, SPINBOX_RANGE_MAX)
        self.spinbox_oopmax_box = QDoubleSpinBox()
        self.spinbox_oopmax_box.setSingleStep(STEP_INTEGRATION_SPINBOX)
        self.spinbox_oopmax_box.setRange(SPINBOX_RANGE_MIN, SPINBOX_RANGE_MAX)

        hbox_box_oop.addWidget(label_ooprange_box)
        hbox_box_oop.addWidget(self.spinbox_oopmin_box)
        hbox_box_oop.addWidget(self.spinbox_oopmax_box)

        self.spinbox_oopmin_box.setMaximumWidth(WIDTH_SPINBOX_MAX)
        self.spinbox_oopmax_box.setMaximumWidth(WIDTH_SPINBOX_MAX)

        label_outputunits_box = QLabel(LABEL_BOX_OUTPUT_UNITS)  
        self.combobox_outputunits_box = QComboBox()
        for unit in DICT_UNIT_ALIAS.values():
            self.combobox_outputunits_box.addItem(unit)
        
        hbox_box_unit_output.addWidget(label_outputunits_box, Qt.AlignLeft)
        hbox_box_unit_output.addWidget(self.combobox_outputunits_box, Qt.AlignLeft)

        hbox_box_unit_output.setStretch(1,10)

        # PONI PARAMETERS TAB

        hbox_poni_mod = QHBoxLayout()
        hbox_poni_mod.setContentsMargins(1,0,1,0)
        hbox_poni_wave = QHBoxLayout()
        hbox_poni_wave.setContentsMargins(1,0,1,0)
        hbox_poni_dist = QHBoxLayout()
        hbox_poni_dist.setContentsMargins(1,0,1,0)
        hbox_poni_detector = QHBoxLayout()
        hbox_poni_detector.setContentsMargins(1,0,1,0)
        hbox_poni_poni_1 = QHBoxLayout()
        hbox_poni_poni_1.setContentsMargins(1,0,1,0)
        hbox_poni_poni_2 = QHBoxLayout()
        hbox_poni_poni_2.setContentsMargins(1,0,1,0)
        hbox_poni_rot_1 = QHBoxLayout()
        hbox_poni_rot_1.setContentsMargins(1,0,1,0)
        hbox_poni_rot_2 = QHBoxLayout()
        hbox_poni_rot_2.setContentsMargins(1,0,1,0)
        hbox_poni_rot_3 = QHBoxLayout()
        hbox_poni_rot_3.setContentsMargins(1,0,1,0)
        hbox_poni_buttons = QHBoxLayout()
        hbox_poni_buttons.setContentsMargins(1,0,1,0)

        widget_poni_mod = QWidget()
        widget_poni_wave = QWidget()
        widget_poni_dist = QWidget()
        widget_poni_detector = QWidget()
        widget_poni_poni_1 = QWidget()
        widget_poni_poni_2 = QWidget()
        widget_poni_rot_1 = QWidget()
        widget_poni_rot_2 = QWidget()
        widget_poni_rot_3 = QWidget()
        widget_poni_buttons = QWidget()

        widget_poni_mod.setLayout(hbox_poni_mod)
        widget_poni_wave.setLayout(hbox_poni_wave)
        widget_poni_dist.setLayout(hbox_poni_dist)
        widget_poni_detector.setLayout(hbox_poni_detector)
        widget_poni_poni_1.setLayout(hbox_poni_poni_1)
        widget_poni_poni_2.setLayout(hbox_poni_poni_2)
        widget_poni_rot_1.setLayout(hbox_poni_rot_1)
        widget_poni_rot_2.setLayout(hbox_poni_rot_2)
        widget_poni_rot_3.setLayout(hbox_poni_rot_3)
        widget_poni_buttons.setLayout(hbox_poni_buttons)

        self.checkbox_poni_mod = QCheckBox(LABEL_PONI_MOD)

        hbox_poni_mod.addWidget(self.checkbox_poni_mod)

        label_wavelength = QLabel(LABEL_PONI_WAVELENGTH)
        self.lineedit_wavelength = QLineEdit()
        self.lineedit_wavelength.setEnabled(False)
        label_distance = QLabel(LABEL_DISTANCE)
        self.lineedit_distance = QLineEdit()
        self.lineedit_distance.setEnabled(False)

        hbox_poni_wave.addWidget(label_wavelength)
        hbox_poni_wave.addWidget(self.lineedit_wavelength)
        hbox_poni_dist.addWidget(label_distance)
        hbox_poni_dist.addWidget(self.lineedit_distance)

        label_detector = QLabel(LABEL_DETECTOR)
        self.lineedit_detector = QLineEdit()
        self.lineedit_detector.setEnabled(False)

        hbox_poni_detector.addWidget(label_detector)
        hbox_poni_detector.addWidget(self.lineedit_detector)

        label_poni_1 = QLabel(LABEL_PONI_PONI_1)
        self.lineedit_poni1 = QLineEdit()   

        label_poni_2 = QLabel(LABEL_PONI_PONI_2)
        self.lineedit_poni2 = QLineEdit()
        self.lineedit_poni1.setEnabled(False)
        self.lineedit_poni2.setEnabled(False)

        hbox_poni_poni_1.addWidget(label_poni_1)
        hbox_poni_poni_1.addWidget(self.lineedit_poni1)

        hbox_poni_poni_2.addWidget(label_poni_2)
        hbox_poni_poni_2.addWidget(self.lineedit_poni2)

        label_rot_1 = QLabel(LABEL_PONI_ROT_1)
        self.lineedit_rot1 = QLineEdit()
        label_rot_2 = QLabel(LABEL_PONI_ROT_2)
        self.lineedit_rot2 = QLineEdit()
        label_rot_3 = QLabel(LABEL_PONI_ROT_3)
        self.lineedit_rot3 = QLineEdit()
        self.lineedit_rot1.setEnabled(False)
        self.lineedit_rot2.setEnabled(False)
        self.lineedit_rot3.setEnabled(False)

        hbox_poni_rot_1.addWidget(label_rot_1)
        hbox_poni_rot_1.addWidget(self.lineedit_rot1)
        hbox_poni_rot_2.addWidget(label_rot_2)
        hbox_poni_rot_2.addWidget(self.lineedit_rot2)
        hbox_poni_rot_3.addWidget(label_rot_3)
        hbox_poni_rot_3.addWidget(self.lineedit_rot3)

        self.button_update_old_poni_parameters = QPushButton(BUTTON_UPDATE_OLD_PONI_PARAMETERS)
        self.button_update_old_poni_parameters.setStyleSheet(BUTTON_STYLE_ENABLE)
        self.button_update_poni_parameters = QPushButton(BUTTON_UPDATE_PONI_PARAMETERS)
        self.button_update_poni_parameters.setStyleSheet(BUTTON_STYLE_ENABLE)
        self.button_save_poni_parameters = QPushButton(BUTTON_SAVE_PONI_PARAMETERS)
        self.button_save_poni_parameters.setStyleSheet(BUTTON_STYLE_ENABLE)

        hbox_poni_buttons.addWidget(self.button_update_old_poni_parameters)
        hbox_poni_buttons.addWidget(self.button_update_poni_parameters)
        hbox_poni_buttons.addWidget(self.button_save_poni_parameters)

        vbox_poni.addWidget(widget_poni_mod)
        vbox_poni.addWidget(widget_poni_wave)
        vbox_poni.addWidget(widget_poni_dist)
        vbox_poni.addWidget(widget_poni_detector)
        vbox_poni.addWidget(widget_poni_poni_1)
        vbox_poni.addWidget(widget_poni_poni_2)
        vbox_poni.addWidget(widget_poni_rot_1)
        vbox_poni.addWidget(widget_poni_rot_2)
        vbox_poni.addWidget(widget_poni_rot_3)
        vbox_poni.addWidget(widget_poni_buttons)

        # H5 PARAMETERS TAB
        hbox_h5_h5file = QHBoxLayout()
        hbox_h5_h5file.setContentsMargins(1,0,1,0)
        hbox_h5_attrs = QHBoxLayout()
        hbox_h5_attrs.setContentsMargins(1,0,1,0)

        widget_h5_h5file = QWidget()
        widget_h5_attrs = QWidget()
        widget_h5_h5file.setLayout(hbox_h5_h5file)
        widget_h5_attrs.setLayout(hbox_h5_attrs)

        label_h5_h5file = QLabel(LABEL_H5_H5FILE)
        self.lineedit_h5file = QLineEdit()
        self.lineedit_h5file.setEnabled(False)

        hbox_h5_h5file.addWidget(label_h5_h5file)
        hbox_h5_h5file.addWidget(self.lineedit_h5file)

        self.h5_plaintext = QPlainTextEdit()
        self.h5_plaintext.setReadOnly(True)

        hbox_h5_attrs.addWidget(self.h5_plaintext)

        vbox_h5.addWidget(widget_h5_h5file)
        vbox_h5.addWidget(widget_h5_attrs)


        # class H5Params:
            # hbox_h5_h5file = QHBoxLayout()
            # hbox_h5_h5file.setContentsMargins(1,0,1,0)
            # hbox_h5_maindir = QHBoxLayout()
            # hbox_h5_maindir.setContentsMargins(1,0,1,0)
            # hbox_h5_iangle_key = QHBoxLayout()
            # hbox_h5_iangle_key.setContentsMargins(1,0,1,0)
            # hbox_h5_tangle_key = QHBoxLayout()
            # hbox_h5_tangle_key.setContentsMargins(1,0,1,0)
            # hbox_h5_norm_key = QHBoxLayout()
            # hbox_h5_norm_key.setContentsMargins(1,0,1,0)
            # hbox_h5_acq_key = QHBoxLayout()
            # hbox_h5_acq_key.setContentsMargins(1,0,1,0)
            # hbox_h5_nfiles = QHBoxLayout()
            # hbox_h5_nfiles.setContentsMargins(1,0,1,0)

            # widget_h5_h5file = QWidget()
            # widget_h5_maindir = QWidget()
            # widget_h5_iangle_key = QWidget()
            # widget_h5_tangle_key = QWidget()
            # widget_h5_norm_key = QWidget()
            # widget_h5_acq_key = QWidget()
            # widget_h5_nfiles = QWidget()

            # widget_h5_h5file.setLayout(hbox_h5_h5file)
            # widget_h5_maindir.setLayout(hbox_h5_maindir)
            # widget_h5_iangle_key.setLayout(hbox_h5_iangle_key)
            # widget_h5_tangle_key.setLayout(hbox_h5_tangle_key)
            # widget_h5_norm_key.setLayout(hbox_h5_norm_key)
            # widget_h5_acq_key.setLayout(hbox_h5_acq_key)
            # widget_h5_nfiles.setLayout(hbox_h5_nfiles)

            # label_h5_h5file = QLabel(LABEL_H5_H5FILE)
            # self.lineedit_h5file = QLineEdit()
            # self.lineedit_h5file.setEnabled(False)
            # label_h5_maindir = QLabel(LABEL_H5_MAINDIR)
            # self.lineedit_h5_maindir = QLineEdit()
            # self.lineedit_h5_maindir.setEnabled(False)
            # label_h5_iangle_key = QLabel(LABEL_H5_IANGLE_KEY)
            # self.lineedit_h5_iangle_key = QLineEdit()
            # self.lineedit_h5_iangle_key.setEnabled(False)
            # label_h5_tangle_key = QLabel(LABEL_H5_TANGLE_KEY)
            # self.lineedit_h5_tangle_key = QLineEdit()
            # self.lineedit_h5_tangle_key.setEnabled(False)
            # label_h5_norm_key = QLabel(LABEL_H5_NORM_KEY)
            # self.lineedit_h5_norm_key = QLineEdit()
            # self.lineedit_h5_norm_key.setEnabled(False)
            # label_h5_acq_key = QLabel(LABEL_H5_ACQ_KEY)
            # self.lineedit_h5_acq_key = QLineEdit()
            # self.lineedit_h5_acq_key.setEnabled(False)
            # label_h5_nfiles = QLabel(LABEL_H5_NFILES)
            # self.lineedit_h5_nfiles = QLineEdit()
            # self.lineedit_h5_nfiles.setEnabled(False)

            # hbox_h5_h5file.addWidget(label_h5_h5file)
            # hbox_h5_h5file.addWidget(self.lineedit_h5file)
            # hbox_h5_maindir.addWidget(label_h5_maindir)
            # hbox_h5_maindir.addWidget(self.lineedit_h5_maindir)
            # hbox_h5_iangle_key.addWidget(label_h5_iangle_key)
            # hbox_h5_iangle_key.addWidget(self.lineedit_h5_iangle_key)
            # hbox_h5_tangle_key.addWidget(label_h5_tangle_key)
            # hbox_h5_tangle_key.addWidget(self.lineedit_h5_tangle_key)
            # hbox_h5_norm_key.addWidget(label_h5_norm_key)
            # hbox_h5_norm_key.addWidget(self.lineedit_h5_norm_key)
            # hbox_h5_acq_key.addWidget(label_h5_acq_key)
            # hbox_h5_acq_key.addWidget(self.lineedit_h5_acq_key)
            # hbox_h5_nfiles.addWidget(label_h5_nfiles)
            # hbox_h5_nfiles.addWidget(self.lineedit_h5_nfiles)

            # vbox_h5.addWidget(widget_h5_h5file)
            # vbox_h5.addWidget(widget_h5_maindir)
            # vbox_h5.addWidget(widget_h5_iangle_key)
            # vbox_h5.addWidget(widget_h5_tangle_key)
            # vbox_h5.addWidget(widget_h5_norm_key)
            # vbox_h5.addWidget(widget_h5_acq_key)
            # vbox_h5.addWidget(widget_h5_nfiles)



        #######################################
        ####### SPLITTER FOLDER-FILES##########
        #######################################

        self.listwidget_folders = QListWidget()

        widget_folder_tab.addTab(self.listwidget_folders, LABEL_LIST_FOLDERS)

        vbox_files = QVBoxLayout()
        widget_files = QWidget()
        widget_files.setLayout(vbox_files)

        widget_file_tab.addTab(widget_files, LABEL_LIST_FILES)

        hbox_metadata_items = QHBoxLayout()
        widget_metadata_items = QWidget()
        widget_metadata_items.setLayout(hbox_metadata_items)

        label_headeritems = QLabel(LABEL_METADATA)
        self.combobox_headeritems = QComboBox()
        self.lineedit_headeritems = QLineEdit()

        self.combobox_multi = CheckableComboBox()

        hbox_metadata_items.addWidget(label_headeritems)
        # hbox_metadata_items.addWidget(self.combobox_headeritems)
        # hbox_metadata_items.addWidget(self.lineedit_headeritems)
        hbox_metadata_items.addWidget(self.combobox_multi)
        hbox_metadata_items.setStretch(1,15)

        self.table_files = QTableWidget()

        vbox_files.addWidget(widget_metadata_items)
        vbox_files.addWidget(self.table_files)

        #######################################
        ########## LABEL TITLE      ###########
        #######################################

        label_filename = QLabel(LABEL_FILENAME)
        self.lineedit_filename = QLineEdit()
        self.lineedit_filename.setEnabled(False)

        hbox_top_label.addWidget(label_filename)
        hbox_top_label.addWidget(self.lineedit_filename)

        #######################################
        ########## SPLITTER GRAPHS  ###########
        #######################################

        self.tab_graph_widget = QTabWidget()
        self.tab_chart_widget = QTabWidget()

        splitter_graphs.addWidget(self.tab_graph_widget)
        splitter_graphs.addWidget(self.tab_chart_widget)

        # 2D GRAPHS
        self.graph_raw_widget = Plot2D()
        self.tab_graph_widget.addTab(self.graph_raw_widget, LABEL_RAW_MAP)

        vbox_reshape = QVBoxLayout()
        widget_reshape = QWidget()
        widget_reshape.setLayout(vbox_reshape)

        self.canvas_reshape_widget = MplCanvas(self, width=4, height=3, dpi=50)
        toolbar_reshape_matplotlib = NavigationToolbar2QT(self.canvas_reshape_widget, self)

        vbox_reshape.addWidget(toolbar_reshape_matplotlib)
        vbox_reshape.addWidget(self.canvas_reshape_widget)

        self.tab_graph_widget.addTab(widget_reshape, LABEL_RESHAPE_MAP)

        vbox_graph_q = QVBoxLayout()
        widget_graph_q = QWidget()
        widget_graph_q.setLayout(vbox_graph_q)

        self.tab_graph_widget.addTab(widget_graph_q, LABEL_Q_MAP)

        hbox_graph_toolbar_1 = QHBoxLayout()
        hbox_graph_toolbar_2 = QHBoxLayout()
        hbox_graph_toolbar_3 = QHBoxLayout()

        widget_graph_toolbar_1 = QWidget()
        widget_graph_toolbar_2 = QWidget()
        widget_graph_toolbar_3 = QWidget()

        widget_graph_toolbar_1.setLayout(hbox_graph_toolbar_1)
        widget_graph_toolbar_2.setLayout(hbox_graph_toolbar_2)
        widget_graph_toolbar_3.setLayout(hbox_graph_toolbar_3)

        label_units = QLabel(LABEL_MAP_UNITS)
        self.combobox_units = QComboBox()
        for unit in DICT_UNIT_ALIAS.values():
            self.combobox_units.addItem(unit)
        self.button_log = QPushButton(BUTTON_LOG)
        self.button_log.setStyleSheet(button_on)
        self.button_colorbar = QPushButton(BUTTON_COLORBAR)
        self.button_colorbar.setStyleSheet(button_on)
        self.button_default_graph = QPushButton(BUTTON_AUTO)
        self.button_default_graph.setStyleSheet(button_on)
        label_title = QLabel(LABEL_MAP_TITLES)
        self.combobox_headeritems_title = QComboBox()
        self.lineedit_headeritems_title = QLineEdit()
        self.button_reshape_map = QPushButton(BUTTON_SHOW_RESHAPE)
        self.button_reshape_map.setStyleSheet(button_style_thin)

        hbox_graph_toolbar_1.addWidget(label_units)
        hbox_graph_toolbar_1.addWidget(self.combobox_units)
        hbox_graph_toolbar_1.addWidget(label_title)
        hbox_graph_toolbar_1.addWidget(self.combobox_headeritems_title)
        hbox_graph_toolbar_1.addWidget(self.lineedit_headeritems_title)

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
        label_binning_data = QLabel(LABEL_BINNING_DATA)
        self.spinbox_binnning_data = QSpinBox()
        self.spinbox_binnning_data.setValue(DEFAULT_BINNING)
        self.spinbox_binnning_data.setSingleStep(BINNING_STEP)
        self.spinbox_binnning_data.setRange(BINNING_RANGE_MIN, BINNING_RANGE_MAX)
        self.button_savemap = QPushButton(BUTTON_SAVE_QMAP)
        self.button_savemap.setStyleSheet(button_style_thin)

        hbox_graph_toolbar_2.addWidget(self.button_font_m)
        hbox_graph_toolbar_2.addWidget(self.button_font_M)
        hbox_graph_toolbar_2.addWidget(self.button_reduce_comma)
        hbox_graph_toolbar_2.addWidget(self.button_enhance_comma)
        hbox_graph_toolbar_2.addWidget(self.button_log)
        hbox_graph_toolbar_2.addWidget(label_binning_data)
        hbox_graph_toolbar_2.addWidget(self.spinbox_binnning_data)
        # hbox_graph_toolbar_2.addWidget(self.button_savemap)

        label_xticks = QLabel(LABEL_XTICKS)
        self.lineedit_xticks = QLineEdit()
        label_yticks = QLabel(LABEL_YTICKS)
        self.lineedit_yticks = QLineEdit()

        hbox_graph_toolbar_3.addWidget(label_xticks)
        hbox_graph_toolbar_3.addWidget(self.lineedit_xticks)
        hbox_graph_toolbar_3.addWidget(label_yticks)
        hbox_graph_toolbar_3.addWidget(self.lineedit_yticks)

        self.canvas_2d_q = MplCanvas(self, width=4, height=3, dpi=50)
        toolbar_q_matplotlib = NavigationToolbar2QT(self.canvas_2d_q, self)

        vbox_graph_q.addWidget(widget_graph_toolbar_1)
        vbox_graph_q.addWidget(widget_graph_toolbar_3)
        vbox_graph_q.addWidget(widget_graph_toolbar_2)
        vbox_graph_q.addWidget(toolbar_q_matplotlib)
        vbox_graph_q.addWidget(self.canvas_2d_q)

        vbox_graph_q.setStretch(4,20)

        hbox_graph_toolbar_1.setContentsMargins(1,1,1,0)
        hbox_graph_toolbar_2.setContentsMargins(1,0,1,0)
        hbox_graph_toolbar_3.setContentsMargins(1,0,1,0)
        toolbar_q_matplotlib.setContentsMargins(1,0,1,0)
        self.canvas_2d_q.setContentsMargins(1,0,1,0)

        # 1D CHART
        vbox_chart = QVBoxLayout()
        widget_chart = QWidget()
        widget_chart.setLayout(vbox_chart)

        self.tab_chart_widget.addTab(widget_chart, LABEL_TAB_1D_INT)

        hbox_chart_toolbar_1 = QHBoxLayout()
        hbox_chart_toolbar_2 = QHBoxLayout()
        hbox_chart_toolbar_3 = QHBoxLayout()
        hbox_savefolder = QHBoxLayout()

        widget_chart_toolbar_1 = QWidget()
        widget_chart_toolbar_2 = QWidget()
        widget_chart_toolbar_3 = QWidget()
        widget_savefolder = QWidget()

        widget_chart_toolbar_1.setLayout(hbox_chart_toolbar_1)
        widget_chart_toolbar_2.setLayout(hbox_chart_toolbar_2)
        widget_savefolder.setLayout(hbox_savefolder)        
        widget_chart_toolbar_3.setLayout(hbox_chart_toolbar_3)

        label_integrations = QLabel(LABEL_INTEGRATIONS)
        self.combobox_integration = QComboBox()
        self.lineedit_integrations = QLineEdit()
        self.checkbox_mask_integration = QCheckBox(LABEL_MASK_MAP)

        hbox_chart_toolbar_1.addWidget(label_integrations)
        hbox_chart_toolbar_1.addWidget(self.combobox_integration)
        hbox_chart_toolbar_1.addWidget(self.lineedit_integrations)
        hbox_chart_toolbar_1.addWidget(self.checkbox_mask_integration)

        label_sub = QLabel(LABEL_SUB_FACTOR)
        self.spinbox_sub = QDoubleSpinBox()
        self.spinbox_sub.setSingleStep(STEP_SUB_SPINBOX)
        self.button_clearplot = QPushButton(BUTTON_CLEAR_PLOT)
        self.button_clearplot.setStyleSheet(button_style_thin)
        self.button_saveplot = QPushButton(BUTTON_SAVE_INTEGRATIONS)
        self.button_saveplot.setStyleSheet(button_style_thin)        
        self.button_batch = QPushButton(BUTTON_BATCH)
        self.button_batch.setStyleSheet(button_style_thin) 

        hbox_chart_toolbar_2.addWidget(label_sub)
        hbox_chart_toolbar_2.addWidget(self.spinbox_sub)
        hbox_chart_toolbar_2.addWidget(self.button_clearplot)
        hbox_chart_toolbar_2.addWidget(self.button_saveplot)
        hbox_chart_toolbar_2.addWidget(self.button_batch)

        label_savefolder = QLabel(LABEL_SAVE_FOLDER)
        self.lineedit_savefolder = QLineEdit()

        hbox_savefolder.addWidget(label_savefolder)
        hbox_savefolder.addWidget(self.lineedit_savefolder)

        self.graph_1D_widget = Plot1D()

        vbox_chart.addWidget(widget_chart_toolbar_1)
        vbox_chart.addWidget(widget_savefolder)        
        vbox_chart.addWidget(widget_chart_toolbar_2)
        vbox_chart.addWidget(self.graph_1D_widget)

        vbox_chart.setStretch(3,20)

        hbox_chart_toolbar_1.setContentsMargins(1,1,1,0)
        hbox_chart_toolbar_2.setContentsMargins(1,0,1,0)
        hbox_savefolder.setContentsMargins(1, 0, 1, 0)
        self.graph_1D_widget.setContentsMargins(1,0,1,0)

        #######################################
        ########## TERMINAL OUTPUT  ###########
        #######################################

        self.plaintext_output = QPlainTextEdit()
        self.plaintext_output.setReadOnly(True)
        widget_terminal_tab.addTab(self.plaintext_output, LABEL_TERMINAL)

        hbox_terminal_top = QHBoxLayout()
        widget_terminal_top = QWidget()
        widget_terminal_top.setLayout(hbox_terminal_top)

        label_plaintext = QLabel(LABEL_TERMINAL)
        label_plaintext.setStyleSheet("background-color: white;border: 1px solid black;")
        label_plaintext.setAlignment(Qt.AlignCenter)
        self.button_hide_terminal = QPushButton(BUTTON_HIDE_TERMINAL)
        self.button_hide_terminal.setStyleSheet(button_on)

    # METHODS AND CALLBACKS WITHIN THE LAYOUT
    def callbacks_layout(self):
        self.checkbox_poni_mod.stateChanged.connect(
            lambda : (
                self.disable_ponifile_mod(),
            )
        )

    def disable_ponifile_mod(self) -> None:
        """
        Enable or disable the lineedits to modify ponifile parameters
        """
        if self.checkbox_poni_mod.isChecked():
            state = True
        else:
            state = False
            # self.update_ponifile_widgets(
            #     dict_poni=self._dict_poni_cache,
            # )            
        self.lineedit_wavelength.setEnabled(state)
        self.lineedit_distance.setEnabled(state)
        self.lineedit_poni1.setEnabled(state)
        self.lineedit_poni2.setEnabled(state)
        self.lineedit_rot1.setEnabled(state)
        self.lineedit_rot2.setEnabled(state)
        self.lineedit_rot3.setEnabled(state)

    def update_button_orientation(self, button_label=str(), new_state=True):
            dict_button = BUTTON_ORIENTATIONS_LAYOUT.get(button_label, WRONG_LABEL)

            if isinstance(dict_button, dict):
                button_widget = dict_button["widget"]
                new_label = dict_button[new_state]["label"]
                new_style = dict_button[new_state]["style"]

                button_widget.setText(new_label)
                button_widget.setStyleSheet(new_style)

    @property
    def state_qz(self):
        state = self.button_qz.isChecked()
        return state

    @property
    def state_qr(self):
        state = self.button_qr.isChecked()
        return state

    @property
    def state_orientation(self):
        qz = self.state_qz()
        qr = self.state_qr()
        so = DICT_SAMPLE_ORIENTATIONS[(self._qz_parallel, self._qr_parallel)]
        return so

    @property
    def state_mirror(self):
        state = self.button_mirror.isChecked()
        return state