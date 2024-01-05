from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QTabWidget
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QPushButton, QCheckBox, QSpinBox, QDoubleSpinBox
from PyQt5.QtCore import Qt
from silx.gui.plot.PlotWindow import Plot1D, Plot2D
from pyxscat.other.units import DICT_UNIT_ALIAS
from .multi_combobox import CheckableComboBox

LABEL_FILENAME = "Current displayed file:"
LABEL_SAVE_FOLDER = "Save folder:"

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

DEFAULT_BINNING = int(2)
BINNING_STEP = int(1)
BINNING_RANGE_MIN = int(1)
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



class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


class GraphLayout(QWidget):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self._build()

    def _build(self):
        self.setGeometry(300, 300, 300, 200)
        hbox_main = QHBoxLayout()
        self.setLayout(hbox_main)

        splitter_screen = QSplitter(orientation=Qt.Vertical)
        hbox_main.addWidget(splitter_screen)   

        hbox_top_label = QHBoxLayout()
        hbox_top_label.setContentsMargins(1,0,1,0)
        widget_top_label = QWidget()
        widget_top_label.setLayout(hbox_top_label)
        splitter_graphs = QSplitter()
        vbox_terminal = QVBoxLayout()
        vbox_terminal.setContentsMargins(1,0,1,0)

        splitter_screen.addWidget(widget_top_label)
        splitter_screen.addWidget(splitter_graphs)

        splitter_screen.setStretchFactor(0,1)
        splitter_screen.setStretchFactor(1,20)
        splitter_screen.setStretchFactor(2,2)

        #######################################
        ########## LABEL TITLE      ###########
        #######################################

        # label_filename = QLabel(LABEL_FILENAME)
        # self.lineedit_filename = QLineEdit()
        # self.lineedit_filename.setEnabled(False)

        # hbox_top_label.addWidget(label_filename)
        # hbox_top_label.addWidget(self.lineedit_filename)

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
        # self.combobox_headeritems_title = QComboBox()
        self.combobox_headeritems_title = CheckableComboBox()
        self.lineedit_headeritems_title = QLineEdit()
        self.button_reshape_map = QPushButton(BUTTON_SHOW_RESHAPE)
        self.button_reshape_map.setStyleSheet(button_style_thin)

        hbox_graph_toolbar_1.addWidget(label_units)
        hbox_graph_toolbar_1.addWidget(self.combobox_units)
        hbox_graph_toolbar_1.addWidget(label_title)
        hbox_graph_toolbar_1.addWidget(self.combobox_headeritems_title)
        hbox_graph_toolbar_1.setStretch(3,15)
        # hbox_graph_toolbar_1.addWidget(self.lineedit_headeritems_title)

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
        label_xlims = QLabel(LABEL_XLIMS)
        self.lineedit_xlims = QLineEdit()
        label_ylims = QLabel(LABEL_YLIMS)
        self.lineedit_ylims = QLineEdit()

        hbox_graph_toolbar_3.addWidget(label_xticks)
        hbox_graph_toolbar_3.addWidget(self.lineedit_xticks)
        hbox_graph_toolbar_3.addWidget(label_yticks)
        hbox_graph_toolbar_3.addWidget(self.lineedit_yticks)
        hbox_graph_toolbar_3.addWidget(label_xlims)
        hbox_graph_toolbar_3.addWidget(self.lineedit_xlims)
        hbox_graph_toolbar_3.addWidget(label_ylims)
        hbox_graph_toolbar_3.addWidget(self.lineedit_ylims)

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
        # self.combobox_integration = QComboBox()
        self.combobox_integration = CheckableComboBox()
        self.lineedit_integrations = QLineEdit()
        self.checkbox_mask_integration = QCheckBox(LABEL_MASK_MAP)

        hbox_chart_toolbar_1.addWidget(label_integrations)
        hbox_chart_toolbar_1.addWidget(self.combobox_integration)
        # hbox_chart_toolbar_1.addWidget(self.lineedit_integrations)
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
        hbox_chart_toolbar_1.setStretch(1,20)