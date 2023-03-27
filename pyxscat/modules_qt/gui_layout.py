
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QGridLayout, QListWidget, QTableWidget, QLabel, QComboBox, QCheckBox, QLineEdit, QDoubleSpinBox, QPlainTextEdit, QTabWidget
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from silx.gui.plot.PlotWindow import Plot1D, Plot2D
from os.path import join
from . import GLOBAL_PATH_QT

STEP_SUB_SPINBOX = 0.01
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
        self.grid_left.setRowStretch(5,2)
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

        self.tab_input_data = QTabWidget()
        self.tab_input_data.addTab(self.widget_input_data, "Folders and files")
        self.tab_input_data.addTab(self.widget_input_info, "Setup information")

        self.widget_input_data.setLayout(self.grid_input_data)
        self.widget_input_info.setLayout(self.grid_input_info)
        self.label_folders = QLabel("====== List of folders ======")
        self.label_folders.setStyleSheet("background-color: white;border: 1px solid black;")
        self.label_folders.setAlignment(Qt.AlignCenter)
        self.label_files = QLabel("====== List of files ======")
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

        self.label_savefolder = QLabel("Save folder:")
        self.lineedit_savefolder = QLineEdit()

        self.grid_save.addWidget(self.label_savefolder,1,1)
        self.grid_save.addWidget(self.lineedit_savefolder,1,2)

        self.grid_input_and_graphs = QGridLayout()
        self.grid_label_terminal = QGridLayout()
        self.label_plaintext = QLabel("====== Output terminal ======")
        self.label_plaintext.setStyleSheet("background-color: white;border: 1px solid black;")
        self.label_plaintext.setAlignment(Qt.AlignCenter)
        self.button_hide_terminal = QPushButton("HIDE TERMINAL")
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


        # Build the grid of input data
        self.grid_input_data.setRowStretch(1,1)
        self.grid_input_data.setRowStretch(2,1)
        self.grid_input_data.setRowStretch(3,1)
        self.grid_input_data.setRowStretch(4,1)
        self.grid_input_data.setRowStretch(5,1)
        self.title_input = QLabel("====== Input File Parameters ======")
        self.title_input.setStyleSheet("background-color: white;border: 1px solid black;padding:4px;")
        self.title_input.setAlignment(Qt.AlignCenter)


        self.grid_input_setup = QGridLayout()
        self.grid_input_maindir = QGridLayout()
        self.grid_input_conditions = QGridLayout()
        self.grid_input_ponifile = QGridLayout()
        self.grid_input_reference = QGridLayout()
        self.grid_input_orientations = QGridLayout()
        self.grid_input_buttons = QGridLayout()
        self.grid_input_data.addWidget(self.title_input,1,1)
        self.grid_input_data.addLayout(self.grid_input_maindir,2,1)
        self.grid_input_data.addLayout(self.grid_input_conditions,3,1)
        self.grid_input_data.addLayout(self.grid_input_ponifile,4,1)
        self.grid_input_data.addLayout(self.grid_input_reference,5,1)
        self.grid_input_data.addLayout(self.grid_input_orientations,6,1)
        self.grid_input_data.addLayout(self.grid_input_buttons,7,1)

        self.grid_input_info.addLayout(self.grid_input_setup,1,1)

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
        self.grid_input_reference.setColumnStretch(3,1)

        self.grid_input_buttons.setColumnStretch(1,1)
        self.grid_input_buttons.setColumnStretch(2,1)

        self.label_maindir = QLabel("Main directory:")

        self.lineedit_maindir = QLineEdit("Type here the path or pick it")
        self.button_pick_maindir = QPushButton(" Pick a directory ")
        self.button_pick_maindir.setIcon(QIcon(join(GLOBAL_PATH_QT, "folder.png")))        
        self.button_qz = QPushButton("qz \u2191\u2191")
        self.button_qr = QPushButton("qr \u2191\u2191")

        self.label_extension = QLabel("File extension:")
        self.combobox_extension = QComboBox()
        self.combobox_extension.addItem(".edf")
        self.combobox_extension.addItem(".tiff")
        # self.combobox_extension.addItem(".hdf5")

        self.label_conditions = QLabel("Wildcards(*):")
        self.lineedit_wildcards = QLineEdit('*')

        self.label_ponifile = QLabel("Ponifile:")
        self.combobox_ponifile = QComboBox()

        self.button_add_ponifile = QPushButton(" Pick new ponifile ")
        self.button_add_ponifile.setIcon(QIcon(join(GLOBAL_PATH_QT, "file.png")))  
           
        self.button_add_reference = QPushButton(" Pick a reference file ")
        self.button_add_reference.setIcon(QIcon(join(GLOBAL_PATH_QT, "file.png")))  
        self.label_reffolder = QLabel("Reference folder:")
        self.combobox_reffolder = QComboBox()
        self.label_sample_orientation = QLabel("Sample orientation:")
        self.button_pyfaicalib = QPushButton(" pyFAI calibration GUI ")
        self.button_pyfaicalib.setIcon(QIcon(join(GLOBAL_PATH_QT, "pyfai.png"))) 
        self.button_start = QPushButton(" Update data ")
        self.button_start.setIcon(QIcon(join(GLOBAL_PATH_QT, "refresh.png"))) 

        self.button_pick_maindir.setStyleSheet(button_style_input)
        self.button_add_ponifile.setStyleSheet(button_style_input)
        self.button_add_reference.setStyleSheet(button_style_input)
        self.button_qz.setStyleSheet(button_style_input)
        self.button_qr.setStyleSheet(button_style_input)
        self.button_pyfaicalib.setStyleSheet(button_style_input)
        self.button_start.setStyleSheet(button_style_input)

        set_bstyle([self.label_maindir, self.label_folders, self.label_files, self.label_extension, self.label_conditions, self.label_ponifile, self.label_reffolder, self.label_sample_orientation, self.title_input])

        self.grid_input_maindir.addWidget(self.label_maindir, 1, 1)
        self.grid_input_maindir.addWidget(self.lineedit_maindir, 1, 2)
        self.grid_input_maindir.addWidget(self.button_pick_maindir, 1, 3)
        self.grid_input_conditions.addWidget(self.label_extension, 1, 1)
        self.grid_input_conditions.addWidget(self.combobox_extension, 1, 2)
        self.grid_input_conditions.addWidget(self.label_conditions, 1, 3)
        self.grid_input_conditions.addWidget(self.lineedit_wildcards, 1, 4)

        self.grid_input_ponifile.addWidget(self.label_ponifile, 1, 1)
        self.grid_input_ponifile.addWidget(self.combobox_ponifile, 1, 2)
        self.grid_input_ponifile.addWidget(self.button_add_ponifile, 1, 3)
        self.grid_input_reference.addWidget(self.label_reffolder, 1, 1)
        self.grid_input_reference.addWidget(self.combobox_reffolder, 1, 2)
        self.grid_input_reference.addWidget(self.button_add_reference, 1, 3)

        self.grid_input_orientations.addWidget(self.label_sample_orientation, 1, 1)
        self.grid_input_orientations.addWidget(self.button_qz, 1, 2)
        self.grid_input_orientations.addWidget(self.button_qr, 1, 3)

        self.grid_input_buttons.addWidget(self.button_pyfaicalib, 1, 1)
        self.grid_input_buttons.addWidget(self.button_start, 1, 2)
        self.grid_header_items = QGridLayout()
        self.grid_plot_average = QGridLayout()
        self.label_headeritems = QLabel("Header items:")
        self.combobox_headeritems = QComboBox()
        self.lineedit_headeritems = QLineEdit()
        self.button_plot = QPushButton("UPDATE PLOT")
        self.button_average = QPushButton("AVERAGE PLOT")
  
        self.button_plot.setStyleSheet(button_style_plot)
        self.button_average.setStyleSheet(button_style_plot)

        self.grid_header_items.setColumnStretch(1,1)
        self.grid_header_items.setColumnStretch(2,3)
        self.grid_header_items.setColumnStretch(3,3)
        self.grid_header_items.addWidget(self.label_headeritems, 1, 1)
        self.grid_header_items.addWidget(self.combobox_headeritems, 1, 2)
        self.grid_header_items.addWidget(self.lineedit_headeritems, 1, 3)
        self.grid_plot_average.addWidget(self.button_plot, 1, 1)
        self.grid_plot_average.addWidget(self.button_average, 1, 2)

        self.grid_input_files.setRowStretch(1,1)
        self.grid_input_files.setRowStretch(2,2)


        self.grid_input_files.addLayout(self.grid_header_items, 1, 1)
        self.grid_input_files.addLayout(self.grid_plot_average, 2, 1)
        self.grid_live_title.setColumnStretch(1,1)
        self.grid_live_title.setColumnStretch(2,20)
        self.checkbox_live = QCheckBox("Live")
        self.lineedit_filename = QLineEdit()
        self.lineedit_filename.setEnabled(False)
        self.combobox_units = QComboBox()
        self.button_default_graph = QPushButton("AUTO LIMITS ON")

        self.button_default_graph.setStyleSheet(button_on)
        self.combobox_units.addItem("q_nm^-1")
        self.combobox_units.addItem("q_A^-1")
        self.combobox_units.addItem("2th_deg")
        self.combobox_units.addItem("2th_rad")
        self.button_map = QPushButton("GENERATE 2D MAP")
        self.button_savemap = QPushButton("SAVE 2D MAP")
        
        self.button_map.setStyleSheet(button_style_thin)
        self.button_savemap.setStyleSheet(button_style_thin)
        self.label_title = QLabel("Map titles:")
        self.label_units = QLabel("Units for 2D map:")
        self.combobox_headeritems_title = QComboBox()
        self.lineedit_headeritems_title = QLineEdit()
        self.xlims = QLabel("x-lims:")
        self.ylims = QLabel("y-lims:")
        self.xticks = QLabel("x-ticks:")
        self.yticks = QLabel("y-ticks:")
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

        self.label_sub = QLabel("Subtraction scale factor (0.0 - 1.0):")
        self.spinbox_sub = QDoubleSpinBox()
        self.spinbox_sub.setSingleStep(STEP_SUB_SPINBOX)
        self.button_plot_2 = QPushButton("UPDATE PLOT")
        self.button_plot_2.setStyleSheet(button_style_thin)

        self.grid_sub = QGridLayout()
        self.grid_sub.addWidget(self.label_sub, 1, 1)
        self.grid_sub.addWidget(self.spinbox_sub, 1, 2)
        self.grid_sub.addWidget(self.button_plot_2, 1, 3)


        self.button_clearplot = QPushButton("CLEAR PLOT")
        self.button_saveplot = QPushButton("SAVE INTEGRATIONS")
        self.button_savefit = QPushButton("OPEN FITTING FORM")

        self.button_clearplot.setStyleSheet(button_style_thin)
        self.button_saveplot.setStyleSheet(button_style_thin)
        self.button_savefit.setStyleSheet(button_style_thin)

        self.label_integrations = QLabel("Integrations:")
        self.combobox_integration = QComboBox()
        self.lineedit_integrations = QLineEdit()

        self.grid_live_title.addWidget(self.checkbox_live, 1, 1)
        self.grid_live_title.addWidget(self.lineedit_filename, 1, 2)

        self.grid_input_and_graphs.setColumnStretch(1,1)
        self.grid_input_and_graphs.setColumnStretch(2,1)
        self.grid_input_and_graphs.setRowStretch(1,1)
        self.grid_input_and_graphs.setRowStretch(2,3)
        self.grid_input_and_graphs.setRowStretch(3,20)


        self.label_input_graph = QLabel("====== 2D Map Parameters ======")
        self.label_input_graph.setStyleSheet("background-color: white;border: 1px solid black;")
        self.label_input_graph.setAlignment(Qt.AlignCenter)
        self.label_input_chart = QLabel("====== 1D Plot Parameters ======")
        self.label_input_chart.setStyleSheet("background-color: white;border: 1px solid black;")
        self.label_input_chart.setAlignment(Qt.AlignCenter)

        self.grid_input_graph = QGridLayout()
        self.grid_input_chart = QGridLayout()
        self.graph_widget = Plot2D()
        self.chart_widget = Plot1D()

        self.grid_input_and_graphs.addWidget(self.label_input_graph,1,1)
        self.grid_input_and_graphs.addWidget(self.label_input_chart,1,2)
        self.grid_input_and_graphs.addLayout(self.grid_input_graph,2,1)
        self.grid_input_and_graphs.addLayout(self.grid_input_chart,2,2)
        self.grid_input_and_graphs.addWidget(self.graph_widget,3,1)
        self.grid_input_and_graphs.addWidget(self.chart_widget,3,2)

        self.grid_units_graph = QGridLayout()
        self.grid_input_graph_buttons = QGridLayout()
        self.grid_input_graph_lims = QGridLayout()

        self.grid_input_graph.addLayout(self.grid_units_graph, 1, 1)
        self.grid_input_graph.addLayout(self.grid_input_graph_lims, 2, 1)
        self.grid_input_graph.addLayout(self.grid_input_graph_buttons, 3, 1)
        
        self.grid_units_graph.addWidget(self.label_units, 1, 1)
        self.grid_units_graph.addWidget(self.combobox_units, 1, 2)
        self.grid_units_graph.addWidget(self.button_default_graph, 1, 3)

        self.grid_input_graph_buttons.addWidget(self.label_title, 1, 1)
        self.grid_input_graph_buttons.addWidget(self.combobox_headeritems_title, 1, 2)
        self.grid_input_graph_buttons.addWidget(self.lineedit_headeritems_title, 1, 3)
        self.grid_input_graph_buttons.addWidget(self.button_map, 1, 4)
        self.grid_input_graph_buttons.addWidget(self.button_savemap, 1, 5)


        self.grid_input_graph_lims.setColumnStretch(1,1)
        self.grid_input_graph_lims.setColumnStretch(2,1)
        self.grid_input_graph_lims.setColumnStretch(3,1)
        self.grid_input_graph_lims.setColumnStretch(4,1)
        self.grid_input_graph_lims.setColumnStretch(5,3)
        self.grid_input_graph_lims.setColumnStretch(6,1)
        self.grid_input_graph_lims.setColumnStretch(7,1)
        self.grid_input_graph_lims.setColumnStretch(8,1)
        self.grid_input_graph_lims.setColumnStretch(9,1)
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

        self.grid_chart_buttons.addWidget(self.button_clearplot, 1, 1)
        self.grid_chart_buttons.addWidget(self.button_saveplot, 1, 2)
        self.grid_chart_buttons.addWidget(self.button_savefit, 1, 3)


        self.grid_input_chart_integrations.addWidget(self.label_integrations, 1, 1)
        self.grid_input_chart_integrations.addWidget(self.combobox_integration, 1, 2)
        self.grid_input_chart_integrations.addWidget(self.lineedit_integrations, 1, 3)

        ### Tab for setup information
        self.grid_input_setup.setRowStretch(1,1)
        self.grid_input_setup.setRowStretch(1,2)
        self.grid_input_setup.setRowStretch(1,3)
        self.grid_input_setup.setRowStretch(1,4)
        self.grid_input_setup.setRowStretch(1,5)
        self.grid_input_setup.setColumnStretch(1,1)
        self.grid_input_setup.setColumnStretch(1,2)
        self.grid_input_setup.setColumnStretch(1,3)
        self.label_setup = QLabel("Choose a setup dictionary:")
        self.combobox_setup = QComboBox()
        self.button_setup = QPushButton(" Pick a .json file")
        self.label_angle = QLabel("Motor - Incident angle:")
        self.lineedit_angle = QLineEdit()
        self.combobox_angle = QComboBox()
        self.label_tilt_angle = QLabel("Motor - Tilt angle:")
        self.lineedit_tilt_angle = QLineEdit()
        self.combobox_tilt_angle = QComboBox()
        self.label_normfactor = QLabel("Counter - Norm. factor:")
        self.lineedit_normfactor = QLineEdit()
        self.combobox_normfactor = QComboBox()
        self.label_exposure = QLabel("Counter - Exposition time:")
        self.lineedit_exposure = QLineEdit()
        self.combobox_exposure = QComboBox()    
        self.label_setup_name = QLabel("Setup name:")
        self.lineedit_setup_name = QLineEdit()   
        self.button_setup_save = QPushButton("Save .json file")
        self.button_setup_save.setIcon(QIcon(join(GLOBAL_PATH_QT, "save.png"))) 

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

        set_bstyle([self.label_headeritems, self.label_plaintext, self.xlims, self.ylims, self.label_units, self.xticks, self.yticks, self.label_savefolder, self.label_integrations, self.label_sub, self.label_title,self.label_input_graph,self.label_input_chart])