import modules_qt.widget_methods.lineedit_methods as le
import modules_qt.widget_methods.combobox_methods as cb
import modules_qt.widget_methods.listwidget_methods as lt
import modules_qt.widget_methods.table_methods as tm
import modules_qt.widget_methods.graph_methods as gm

import modules_qt.directory_methods as dm
from modules_qt.main_window import Ui_MainWindow

from module_edf.edf import EdfClass
from module_geometry.geometry import Geometry
from module_integrator.integrator import Integrator
from modules_other.other_functions import np_weak_lims, dict_to_str
from module_integrator.search_functions import search_files_recursively, list_files_to_dict, create_folder, get_subfolder
from modules_other.plots import *

from os.path import join, dirname
import os

GLOBAL_PATH = dirname(dirname(__file__))
DIRECTORY_SETUPS = join(GLOBAL_PATH, 'module_edf', 'setup_dictionaries')
DIRECTORY_INTEGRATIONS = join(GLOBAL_PATH, 'module_integrator', 'integration_dictionaries')


SYMBOL_CHECK = '\u2705'
SYMBOL_X = '\u274C'

SEPARATOR_CONDITIONS = ','
SEPARATOR_LINEEDIT = ','

INTERVAL_SEARCH_DATA = 1000

OUTPUT_FOLDER = 'PyXScat'

BASH_FILE_1S = 'last_file_1s.sh'
BASH_FILE_NOTIME = 'last_file_notime.sh'

ERROR_OS = "Unkown operating system."
PLOT_SELECTED_TABLE = False
ROTATED_ERROR = 'Error on arrays shape correspondende. Check rotation.'

DICT_DEFAULT_2THETA = {
    "UNIT":'2th_deg',
    "XLIM":[-2,25],
    "YLIM":[0,25],
    "XLABEL":"\u03C9 (\u00b0)",
    "YLABEL":"\u03b1 (\u00b0)",
    "XTICKS":[0,5,10,15,20,25],
    "YTICKS":[0,5,10,15,20,25],
}

DICT_DEFAULT_QNM = {
    "UNIT":'q_nm^-1',
    "XLIM":[-2,20],
    "YLIM":[0,20],
    "XLABEL":"$q_{r}$ $(nm^{-1})$",
    "YLABEL":"$q_{z}$ $(nm^{-1})$",
    "XTICKS":[0,5,10,15,20],
    "YTICKS":[0,5,10,15,20],
}

DICT_DEFAULT_QA = {
    "UNIT":'q_A^-1',
    "XLIM":[-0.2,2],
    "YLIM":[0,2],
    "XLABEL":"$q_{r}$ $(\u212B^{-1})$",
    "YLABEL":"$q_{z}$ $(\u212B^{-1})$",
    "XTICKS":[0,0.5,1.0,1.5,2.0],
    "YTICKS":[0,0.5,1.0,1.5,2.0],
}