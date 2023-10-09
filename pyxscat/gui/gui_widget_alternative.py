from . import *
from collections import defaultdict
from os.path import join
from pathlib import Path
from pyFAI import __file__ as pyfai_file
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QSplashScreen, QMessageBox
from PyQt5.QtGui import QPixmap
from scipy import ndimage

from pyxscat.other.other_functions import np_weak_lims, dict_to_str, date_prefix, merge_dictionaries, get_dict_files, get_dict_difference
from pyxscat.other.plots import *
from pyxscat.other.integrator_methods import *
from pyxscat.other.setup_methods import save_setup_dictionary, locate_setup_file, search_metadata_names, get_empty_setup_dict
from pyxscat.gui import LOGGER_PATH, SRC_PATH, GUI_PATH
from pyxscat.gui import lineedit_methods as le
from pyxscat.gui import combobox_methods as cb
from pyxscat.gui import listwidget_methods as lt
from pyxscat.gui import table_methods as tm
from pyxscat.gui import graph_methods as gm
from pyxscat.gui.gui_layout_alternative import GUIPyX_Widget_layout
from pyxscat.gui.gui_layout_alternative import LABEL_CAKE_BINS_OPT, LABEL_CAKE_BINS_MAND, BUTTON_LIVE, BUTTON_LIVE_ON
from pyxscat.gui.gui_layout_alternative import INDEX_TAB_1D_INTEGRATION, INDEX_TAB_RAW_MAP, INDEX_TAB_Q_MAP, INDEX_TAB_RESHAPE_MAP, DEFAULT_BINNING
from pyxscat.h5_integrator import H5GIIntegrator
from pyxscat.h5_integrator import PONI_KEY_BINNING, PONI_KEY_DISTANCE, PONI_KEY_SHAPE1, PONI_KEY_SHAPE2, PONI_KEY_DETECTOR, PONI_KEY_DETECTOR_CONFIG, PONI_KEY_PIXEL1, PONI_KEY_PIXEL2, PONI_KEY_WAVELENGTH, PONI_KEY_PONI1, PONI_KEY_PONI2, PONI_KEY_ROT1, PONI_KEY_ROT2, PONI_KEY_ROT3
from pyxscat.h5_integrator import FILENAME_H5_KEY, FILENAME_KEY, DICT_SAMPLE_ORIENTATIONS
from pyxscat.h5_integrator import UNIT_GI
from pyxscat.gui.gui_layout_alternative import QZ_BUTTON_LABEL, QR_BUTTON_LABEL, MIRROR_BUTTON_LABEL

import json
import logging
import numpy as np
import subprocess
import sys
import os
import pandas as pd

from pyxscat.other.setup_methods import *

ICON_SPLASH = join(ICON_DIRECTORY, 'pyxscat_logo_thumb.png')

MSG_SETUP_UPDATED = "New setup dictionary was updated."
MSG_SETUP_ERROR = "The setup dictionary could not be updated."
MSG_ROTATED_UPDATED = "Rotation state was updated."

MSG_MAIN_DIRECTORY = "New main directory updated."
MSG_MAIN_DIRECTORY_ERROR = "No main directory was detected."
MSG_PATTERN_UPDATED = "The file pattern was updated."
MSG_COMBOBOX_PONIFILE = "New ponifiles were detected."
MSG_COMBOBOX_PONIFILE_ERROR = "No ponifiles were detected."
MSG_PONIFILE_UPDATED = "New ponifile updated."
MSG_PONIFILE_ERROR = "No ponifile detected."
MSG_REFERENCE_FILES_UPDATED = "New reference files detected."
MSG_REFERENCE_FILES_ERROR = "No reference files detected."
MSG_REFERENCE_FILE_UPDATED = "New reference file detected."
MSG_NEW_INTEGRATOR = "New integrator was generated."
MSG_NEW_INTEGRATOR_ERROR = "The integrator instance could not be created."
MSG_INTEGRATOR_NEW_FILES = "New files were added to the integrator instance."
MSG_RESET_INTEGRATOR = "Reset integrator, a new integrator was generated."
MSG_NEW_DETECTED_FILES = "New files were detected."
MSG_CLICKED_FLODER_ERROR = "File table could not be updated."
MSG_RESET_DATA = "The data parameters were reinitialized."
MSG_ERROR_BASH = "There was an error during some bash file running. Allow permission with > chmod 777 -R pyxscat-directory"

GET_RELATIVE_ADDRESS = True
INTERVAL_SEARCH_DATA = 1000


MSG_LOGGER_INIT = "Logger was initialized."
MSG_LOGGER_UPDATE_CB_SETUPS = "The combobox of setups was updated."

MSG_H5_FOUNDFILE = "Imported .hdf5 file"
MSG_H5Integrator = "HDF5 container was created."
MSG_H5Integrator_ERROR = "HDF5 container could not be created."

ERROR_H5_NOTEXISTS = "There is no H5Integrator instance."
ERROR_H5_FILENOTFOUND = "The .h5 could not be found."
ERROR_H5_FILECREATION = "The .h5 file could not be created."
ERROR_H5_INSTANCE = "The h5 instance could not be created."
ERROR_H5_UPDATED = "The H5 could not be updated."

ERROR_MAINDIR = "Main directory could not be set."
ERROR_MAINDIR_DONTEXIST = "Main directory does not exists."
ERROR_PICK_FOLDER = "No folder detected."
ERROR_H5DIR = "There is no new address for the .h5 file. Cancel everything."
ERROR_APPEND_H5 = "The .h5 file could not be appended to the combobox."

INFO_NEW_MAINDIR = "New main directory set."
INFO_H5_CREATION = "New .h5 file was created successfully."
INFO_H5_UPDATED = "The .h5 file was updated."
INFO_H5_PONIFILE_CB_UPDATED = "Combobox of ponifiles was updated."
INFO_LIST_FOLDERS_UPDATED = "Updated list widget."
INFO_LIST_NO_FOLDERS_TO_UPDATE = "No new folders."



MSG_H5FILE_CHOICE = "An .h5 file will be created. Do you want to save it in the same directory?"
MSG_H5FILE_OVERWRITE = "There is an h5 file with the same name. Do you want to overwite it?"

DESCRIPTION_HDF5 = "HDF5_XMaS_Beamline"
COMMENT_NEW_FILE = ""

JSON_FILE_H5 = SRC_PATH.joinpath("h5_recent_files.json")

DEFAULT_SCATTER_SIZE = 1.0
DEFAULT_MAP_FONTSIZE = 10

DEFAULT_INCIDENT_ANGLE = 0.0
DEFAULT_TILT_ANGLE = 0.0

RELATIVE_TO_ROOT = False

 # Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

if not Path(LOGGER_PATH).exists():
    Path(LOGGER_PATH).mkdir()

logger_file = LOGGER_PATH.joinpath(f'pyxscat_logger_{date_prefix()}.txt')
file_handler = logging.FileHandler(logger_file)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)
logger.info(MSG_LOGGER_INIT)

def log_info(func):
    """
    To be used as decorator, everytime the function is accesed, a new log info message is written

    Parameters:
    None

    Returns:
    None
    """
    def wrapper(*args, **kwargs):
        logger.info(f'We entered into function: {func.__name__}')
        return func(*args, **kwargs)
    return wrapper

class GUIPyX_Widget(GUIPyX_Widget_layout):
    """
    Class to create a GUI widget, with methods and callbacks
    """

    signal = pyqtSignal(int)

    def __init__(self):
        super(GUIPyX_Widget, self).__init__()

        # Splash screen
        pixmap = QPixmap(ICON_SPLASH)
        splash = QSplashScreen(pixmap)
        splash.show()
        splash.finish(self)

        # Initialize attributes and callbacks
        self.h5 = None
        self._data_cache = None
        self.main_directory = Path()
        self._dict_poni_cache = dict()
        self.clicked_folder = str()
        self.list_results_cache = []
        self.list_dict_integration_cache = []
        self.dict_recent_h5 = {}

        self.scat_horz_cache = None
        self.scat_vert_cache = None
        self.data_bin_cache = None

        self._dict_qmap_cache = {
            'acq_time' : None,
            'qz_parallel' : self.state_qz,
            'qr_parallel' : self.state_qr,
            'mirror' : self.state_mirror,
            'binning' : DEFAULT_BINNING,
            'incident_angle': DEFAULT_INCIDENT_ANGLE,
            'tilt_angle' : DEFAULT_TILT_ANGLE,
        }

        self._graph_log = True
        self._fontsize_cache = DEFAULT_MAP_FONTSIZE
        self._scattersize_cache = DEFAULT_SCATTER_SIZE
        self._terminal_visible = True
        self._live = False

        self.reset_attributes_and_widgets()
        self.init_callbacks()
        
        # self.update_setup_info()
        self.update_lims_ticks()

    def write_terminal_and_loggerinfo(self, msg=str()):
        """
        Types a message in the terminal of the GUI and register the message in the logger file as INFO

        Parameters:
        msg(str) : string to be written in the logger and the output terminal
        """
        self._write_output(msg)
        logger.info(msg)

    def write_terminal_and_loggererror(self, msg=str()):
        """
        Types a message in the terminal of the GUI and register the message in the logger file as INFO

        Parameters:
        msg(str) : string to be written in the logger and the output terminal
        """
        self._write_output(msg)
        logger.error(msg)

    @log_info
    def init_callbacks(self) -> None:
        """
        Updates the callbacks to initiate main attributes

        Parameters:
        None

        Returns:
        None
        """
        #####################################################################
        ##################  MAIN ATTRIBUTES CALLBACKS  ######################
        #####################################################################

        #########################
        # H5 combobox callback
        #########################
        self.combobox_h5_files.currentTextChanged.connect(self.cb_h5_changed)

        #########################
        # Setup dictionary callback
        #########################
        self.combobox_setup.currentTextChanged.connect(self.cb_setup_changed)
        self.combobox_angle.currentTextChanged.connect(self.cb_iangle_changed)
        self.combobox_tilt_angle.currentTextChanged.connect(self.cb_tangle_changed)
        self.combobox_normfactor.currentTextChanged.connect(self.cb_normfactor_changed)
        self.combobox_acquisition.currentTextChanged.connect(self.cb_acquisition_changed)
        self.button_pick_json.clicked.connect(self.pick_json_clicked)
        self.button_metadata_update.clicked.connect(self.metadata_update_clicked)
        self.button_metadata_save.clicked.connect(self.metadata_save_clicked)

        #########################
        # Integration dictionary callback
        #########################
        #### CAKES #####
        ################
        self.list_cakes.itemClicked.connect(self.listcakes_clicked)
        self.combobox_type_cake.currentTextChanged.connect(self.cake_parameter_changed)
        self.combobox_units_cake.currentTextChanged.connect(self.cake_parameter_changed)
        self.combobox_units_cake.currentTextChanged.connect(self.cake_parameter_changed)
        self.spinbox_azimmin_cake.valueChanged.connect(self.cake_parameter_changed)
        self.spinbox_azimmax_cake.valueChanged.connect(self.cake_parameter_changed)
        self.spinbox_radialmin_cake.valueChanged.connect(self.cake_parameter_changed)
        self.spinbox_radialmax_cake.valueChanged.connect(self.cake_parameter_changed)
        self.spinbox_radialmax_cake.valueChanged.connect(self.cake_parameter_changed)
        self.spinbox_azimbins_cake.valueChanged.connect(self.cake_parameter_changed)

        ################
        #### BOXES #####
        ################
        self.list_box.itemClicked.connect(self.listbox_clicked)
        self.combobox_units_box.currentTextChanged.connect(self.box_parameter_changed)
        self.combobox_direction_box.currentTextChanged.connect(self.box_parameter_changed)
        self.combobox_outputunits_box.currentTextChanged.connect(self.box_parameter_changed)
        self.spinbox_ipmin_box.valueChanged.connect(self.box_parameter_changed)
        self.spinbox_ipmax_box.valueChanged.connect(self.box_parameter_changed)
        self.spinbox_oopmin_box.valueChanged.connect(self.box_parameter_changed)
        self.spinbox_oopmax_box.valueChanged.connect(self.box_parameter_changed)

        #########################
        # Callbacks for mirror rotation and parallel/antiparallel axis
        #########################
        self.button_mirror.clicked.connect(self.button_mirror_clicked)
        self.button_qz.clicked.connect(self.button_qz_clicked)
        self.button_qr.clicked.connect(self.button_qr_clicked)

        #########################
        # Pick main directory
        #########################
        self.button_pick_rootdir.clicked.connect(self.pick_rootdir_clicked)
        self.button_pick_hdf5.clicked.connect(self.pick_h5file_clicked)

        #########################
        # Ponifile callbacks
        #########################
        self.combobox_ponifile.currentTextChanged.connect(self.cb_ponifile_changed)

        #########################
        # Reference callbacks
        #########################

        self.checkbox_auto_reffile.stateChanged.connect(self.checkbox_reference_clicked)       

        #####################################################################
        ##################  MAIN BUTTONS CALLBACKS  #########################
        #####################################################################

        #########################
        # Button to open pyFAI-calib2
        #########################
        self.button_pyfaicalib.clicked.connect(self.open_pyFAI_calib2)

        #########################
        # Button to search and update files
        #########################
        self.button_start.clicked.connect(self.update_all_files)

        #########################
        # Checkbox to start live data searching
        #########################
        self.button_live.clicked.connect(self.live_clicked)

        #####################################################################
        ##################  BROWSER CALLBACKS  ##############################
        #####################################################################

        #########################
        # List_widget folder callback
        #########################
        self.listwidget_samples.itemClicked.connect(self.listsamples_clicked)

        #########################
        # Lineedit_items header updates the table of files
        #########################

        # Click on the table updates the chart
        self.table_files.itemSelectionChanged.connect(self.table_clicked)
        self.combobox_metadata.currentTextChanged.connect(self.cb_metadata_changed)

        # Masked 2D for integrations
        self.checkbox_mask_integration.stateChanged.connect(self.checkbox_mask_clicked)

        # Button clear plot clears the chart
        self.combobox_integration.currentTextChanged.connect(self.cb_integration_changed)
        self.button_clearplot.clicked.connect(self.clear_plot)

        self.spinbox_sub.valueChanged.connect(self.sub_factor_changed)

        # visible tab
        self.tab_graph_widget.currentChanged.connect(self.tab_graph_changed)

        #Q-MAP TOOLBAR
        self.button_font_m.clicked.connect(self.reduce_font_clicked)
        self.button_font_M.clicked.connect(self.increase_font_clicked)
        self.button_reduce_comma.clicked.connect(self.reduce_scattersize)
        self.button_enhance_comma.clicked.connect(self.increase_scattersize)
        self.lineedit_xticks.textChanged.connect(self.ticks_changed)
        self.lineedit_yticks.textChanged.connect(self.ticks_changed)
        self.lineedit_xlims.textChanged.connect(self.ticks_changed)
        self.lineedit_ylims.textChanged.connect(self.ticks_changed)
        self.combobox_headeritems_title.currentTextChanged.connect(self.ticks_changed)
        self.button_log.clicked.connect(self.log_clicked)       
        self.combobox_units.currentTextChanged.connect(self.scat_units_changed)
        self.spinbox_binnning_data.valueChanged.connect(self.binning_changed)

        # Button to save the generated map
        self.button_savemap.clicked.connect(self.save_map_clicked)

        # Button to save the dataframe in the chart
        self.button_saveplot.clicked.connect(self.save_plot_clicked)
        self.button_batch.clicked.connect(self.batch_clicked)

        #########################
        ### PONIFILE PARAMETERS
        #########################
        self.checkbox_poni_mod.stateChanged.connect(self.disable_ponifile_mod)
        self.button_update_old_poni_parameters.clicked.connect(self.retrieve_old_poni_clicked)
        self.button_update_poni_parameters.clicked.connect(self.update_poni_clicked)
        self.button_save_poni_parameters.clicked.connect(self.save_poni_clicked)

    @log_info
    def reset_attributes_and_widgets(self) -> None:
        """
        Resets data attributes after changing main directory

        Parameters:
        None

        Returns:
        None
        """
        self.sample_cache = str()
        self.cache_index = []
        self._h5_file = str()
        self._data_cache = None

        # Clear GUI widgets
        cb.clear(self.combobox_ponifile)
        cb.clear(self.combobox_reffolder)
        cb.clear(self.combobox_metadata)
        cb.clear(self.combobox_headeritems_title)
        cb.clear(self.combobox_angle)
        cb.clear(self.combobox_tilt_angle)
        cb.clear(self.combobox_acquisition)
        cb.clear(self.combobox_normfactor)
        lt.clear(self.listwidget_samples)
        tm.reset(self.table_files)
        # le.clear(self.lineedit_headeritems)
        # le.clear(self.lineedit_headeritems_title)
        self.graph_1D_widget.clear()
        self.graph_raw_widget.clear()

        self.write_terminal_and_loggerinfo(MSG_RESET_DATA)

    # #########################
    # # Update self attributes
    # #########################
    @log_info
    def update_combobox_h5(self, change_to_last=True) -> None:
        combobox = self.combobox_h5_files

        json_files = H5_FILES_PATH.rglob("*.json")
        json_list_names = [file.name for file in json_files]
        json_list_names.insert(0, " ")

        cb.insert_list(
            combobox=combobox,
            list_items=json_list_names,
            reset=True,
        )

        if change_to_last:
            cb.set_text(
                combobox=combobox,
                text=self.h5._name.replace(".h5", ".json"),
            )

    @log_info
    def get_recent_h5_files(self):
        h5_files = []
        json_files = H5_FILES_PATH.rglob("*.json")
        for file in json_files:
            dict_h5 = open_json(file)
            h5_file = Path(dict_h5.get("h5_filename"))
            h5_files.append(h5_file)
        return h5_files

    @log_info
    def update_combobox_metadata(self) -> None:
        """
        Take the .json files from the setup directory and feed the combobox_setups

        Parameters:
        None

        Returns:
        None
        """
        # Get the list of stored metadata .json files 
        list_name_setups = search_metadata_names(directory_setups=SETUP_PATH)

        # Feed the combobox
        cb.insert_list(
            combobox=self.combobox_setup,
            list_items=list_name_setups,
            reset=True,
        )

    @log_info
    def fetch_dict_metadata(self) -> defaultdict:
        """
        Retrieves the values for the setup dictionary from the correct lineedits and returns a defaultdict

        Parameters:
        None

        Returns:
        defaultdict: with the correct keys for setup dictionary and values read from lineedits in GUI
        """
        new_setup_dict = defaultdict(str)
        name = le.text(self.lineedit_setup_name)
        iangle_key = le.text(self.lineedit_angle)
        tangle_key = le.text(self.lineedit_tilt_angle)
        norm_key = le.text(self.lineedit_normfactor)
        acq_key = le.text(self.lineedit_exposure)

        new_setup_dict[NAME_METADATA_KEY] = name
        new_setup_dict[INCIDENT_ANGLE_KEY] = iangle_key
        new_setup_dict[TILT_ANGLE_KEY] = tangle_key
        new_setup_dict[NORMALIZATION_KEY] = norm_key
        new_setup_dict[ACQUISITION_KEY] = acq_key

        return new_setup_dict

    @log_info
    def cb_setup_changed(self, name_setup):
        # Check if the .json file exists
        filename_setup = locate_setup_file(name_integration=name_setup)
        if not filename_setup:
            return
        
        # Fetch the dictionary
        dict_cake_integration = fetch_dictionary_from_json(filename_json=filename_setup)

        # Update the widgets
        self.update_metadata_widgets(dict_setup=dict_cake_integration)
    

    # @log_info
    # def update_setup_info(self, name_setup=str(), new_dict=defaultdict) -> None:
    #     """
    #     Declare the setup dictionary of the GUI searching by name (string) or declaring a new one

    #     Parameters:
    #     new_name_setup(str) : key 'Name' of the (already saved) setup dictionary in a .json file
    #     new_dict(defaultdict) : contains the new values for the setup dictionary

    #     Returns:
    #     None
    #     """
    #     if not name_setup:
    #         name_setup = cb.value(self.combobox_setup)

    #     # Search for a .json file with the name_setup string
    #     if name_setup:
    #         new_dict_setup = get_dict_setup_from_name(
    #             name=name_setup,
    #             directory_setups=SETUP_PATH,
    #         )
    #     # Directly update with a defaultdict  
    #     elif new_dict:
    #         new_dict_setup = new_dict
    #     else:
    #         new_dict_setup = get_empty_setup_dict()

    #     new_dict_setup = filter_dict_setup(
    #         dictionary=new_dict_setup,
    #     )

    #     # Updates the instance variable
    #     self._dict_setup = new_dict_setup

    #     self.write_terminal_and_logger(MSG_SETUP_UPDATED)
    #     self.write_terminal_and_logger(self._dict_setup)

    @log_info
    def update_metadata_widgets(self, dict_setup=dict()):

        # Fill the lineedits
        le.substitute(self.lineedit_setup_name, dict_setup['Name'])
        le.substitute(self.lineedit_angle, dict_setup['Angle'])
        le.substitute(self.lineedit_tilt_angle, dict_setup['Tilt angle'])
        le.substitute(self.lineedit_normfactor, dict_setup['Norm'])
        le.substitute(self.lineedit_exposure, dict_setup['Exposure'])

        # Reset and fill the lineedits of items
        le.clear(self.lineedit_headeritems)
        le.insert(self.lineedit_headeritems, dict_setup['Angle'])
        le.insert(self.lineedit_headeritems, dict_setup['Tilt angle'])
        le.insert(self.lineedit_headeritems, dict_setup['Norm'])
        le.insert(self.lineedit_headeritems, dict_setup['Exposure'])

    @log_info
    def cb_iangle_changed(self, iangle_key) -> None:
        """
            Update the incident angle parameter
        """
        list_keys = self.combobox_angle.currentData()
        if list_keys:
            iangle_key = list_keys[0]
            le.substitute(self.lineedit_angle, iangle_key)
        else:
            return           

    @log_info
    def cb_tangle_changed(self, tangle_key) -> None:
        """
            Update the tilt angle parameter
        """
        list_keys = self.combobox_tilt_angle.currentData()
        if list_keys:
            tangle_key = list_keys[0]
            le.substitute(self.lineedit_tilt_angle, tangle_key)
        else:
            return

    @log_info
    def cb_normfactor_changed(self, normfactor_key) -> None:
        """
            Update the normalization factor parameter
        """
        list_keys = self.combobox_normfactor.currentData()
        if list_keys:
            normfactor_key = list_keys[0]
            le.substitute(self.lineedit_normfactor, normfactor_key)
        else:
            return

    @log_info
    def cb_acquisition_changed(self, acq_key) -> None:
        """
            Update the exposition time parameter
        """
        list_keys = self.combobox_acquisition.currentData()
        if list_keys:
            acq_key = list_keys[0]
            le.substitute(self.lineedit_exposure, acq_key)
        else:
            return

    @log_info
    def pick_json_clicked(self, _):
        # Get the address of the .json file
        json_filename = self.pick_json_file()
        if not json_filename:
            return

        # Fetch the dictionary
        dict_setup = fetch_dictionary_from_json(
            filename_json=json_filename,
        )

        # Update metadata widgets
        self.update_metadata_widgets(
            dict_setup=dict_setup,

        )

    @log_info
    def pick_json_file(self):
        json_file = QFileDialog.getOpenFileNames(self, 'Pick .json file', '.', "*.json")
        try:
            json_filename = json_file[0][0]
            return json_filename
        except Exception as e:
            return

    @log_info
    def metadata_update_clicked(self, _):
        if not self.h5:
            return

        # Fetch a dictionary with metadata keys from widgets
        dict_metadata = self.fetch_dict_metadata()

        # Update the attributes in the .h5 file
        self.h5.update_metadata_keys(
            dict_metadata_keys=dict_metadata,
        )

        self.write_terminal_and_loggerinfo(f"New metadata keys: {str(dict_metadata)}")



    @log_info
    def metadata_save_clicked(self, _):
        # Fetch a dictionary with metadata keys from widgets
        dict_metadata = self.fetch_dict_metadata()

        if not dict_metadata['Name']:
            return

        # Save the metadata as a .json file
        save_setup_dictionary(dict_setup=dict_metadata)

        # Update the combobox
        self.update_combobox_metadata()

        # Change the combobox to the last one
        cb.set_text(
            combobox=self.combobox_setup,
            text=dict_metadata["Name"],
        )



    # @log_info
    # def save_metadata(self, dict_setup=dict()) -> None:
    #     """
    #         Collect the dictionary and save a .json file
    #     """
    #     file_json = join(SETUP_PATH, f"{new_dict_info['Name']}.json")
    #     with open(file_json, 'w+') as fp:
    #         json.dump(new_dict_info, fp)
    #     self.update_combobox_setups()



    @log_info
    def listcakes_clicked(self, list_item):
        # Fetch the name of the integration
        name_cake_integration = list_item.text()

        # Check if a file with this name does exist
        filename_integration = locate_integration_file(name_integration=name_cake_integration)
        if not filename_integration:
            self.write_terminal_and_loggerinfo(f"There is no .json file with the name {name_cake_integration}")
            return
        
        # Fetch the dictionary
        dict_cake_integration = fetch_dictionary_from_json(filename_json=filename_integration)

        # Check if the dictionary contains all the parameters and correct types
        if not is_cake_dictionary(dict_integration=dict_cake_integration):
            self.write_terminal_and_loggerinfo(f"The integration dictionary is not correct : {dict_cake_integration}")
            return

        # Update cake widgets
        self.update_cake_widgets(dict_integration=dict_cake_integration)

    @log_info
    def update_cake_widgets(self, dict_integration=dict()):
        """
        Updates the widgets of integration after clicking on the list_cakes
        """
        le.substitute(self.lineedit_name_cake, dict_integration[CAKE_KEY_NAME])
        le.substitute(self.lineedit_suffix_cake, dict_integration[CAKE_KEY_SUFFIX])
        cb.set_text(self.combobox_type_cake, dict_integration[CAKE_KEY_TYPE])
        self.spinbox_radialmin_cake.setValue(dict_integration[CAKE_KEY_RRANGE][0])
        self.spinbox_radialmax_cake.setValue(dict_integration[CAKE_KEY_RRANGE][1])
        self.spinbox_azimmin_cake.setValue(dict_integration[CAKE_KEY_ARANGE][0])
        self.spinbox_azimmax_cake.setValue(dict_integration[CAKE_KEY_ARANGE][1])
        cb.set_text(self.combobox_units_cake, dict_integration[CAKE_KEY_UNIT])
        self.spinbox_azimbins_cake.setValue(dict_integration[CAKE_KEY_ABINS])
        logger.info(f"Updated widgets with cake integration values.")

    @log_info
    def listbox_clicked(self, list_item):
        name_box_integration = list_item.text()

        # Check if a file with this name does exist
        filename_integration = locate_integration_file(name_integration=name_box_integration)
        if not filename_integration:
            return
        
        # Fetch the dictionary
        dict_box_integration = fetch_dictionary_from_json(filename_json=filename_integration)

        # Check if the dictionary contains all the parameters and correct types
        if not is_box_dictionary(dict_integration=dict_box_integration):
            return

        # Update cake widgets
        self.update_box_parameters(dict_integration=dict_box_integration)

    @log_info
    def update_box_parameters(self, dict_integration=dict()):
        """
        Updates the widgets of integration after clicking on the list_boxes
        """
        le.substitute(self.lineedit_name_box, dict_integration[BOX_KEY_NAME])
        le.substitute(self.lineedit_suffix_box, dict_integration[BOX_KEY_SUFFIX])
        cb.set_text(self.combobox_direction_box, dict_integration[BOX_KEY_DIRECTION])
        cb.set_text(self.combobox_units_box, dict_integration[BOX_KEY_INPUT_UNIT])
        self.spinbox_ipmin_box.setValue(dict_integration[BOX_KEY_IPRANGE][0])
        self.spinbox_ipmax_box.setValue(dict_integration[BOX_KEY_IPRANGE][1])
        self.spinbox_oopmin_box.setValue(dict_integration[BOX_KEY_OOPRANGE][0])
        self.spinbox_oopmax_box.setValue(dict_integration[BOX_KEY_OOPRANGE][1])
        cb.set_text(self.combobox_outputunits_box, dict_integration[BOX_KEY_OUTPUT_UNIT])
        logger.info(f"Updated widgets with box integration values.")


    @log_info
    def cake_parameter_changed(self,_):
        # Fetch the integration parameters from the widgets
        dict_integration = self.fetch_cake_integration_parameters()
        if not dict_integration:
            return

        # Save, overwrite the .json file
        save_integration_dictionary(dict_integration=dict_integration)

        # Input the new integration_name if needed
        lt.insert(
            listwidget=self.list_cakes,
            item=dict_integration[CAKE_KEY_NAME],
            repeat_file=False,
        )
        self.feed_integration_widgets()

        # Update the graphs
        self.update_graphs(
            graph_1D=True,
            graph_2D_raw=True,
        )
        

    @log_info
    def fetch_cake_integration_parameters(self):
        dict_cake = dict()

        name = le.text(self.lineedit_name_cake)
        if not name:
            return
        dict_cake[CAKE_KEY_NAME] = name

        suffix = le.text(self.lineedit_suffix_cake)
        if not suffix:
            suffix = name
        dict_cake[CAKE_KEY_SUFFIX] = name

        type_cake = cb.value(self.combobox_type_cake)
        dict_cake[CAKE_KEY_TYPE] = type_cake

        unit = cb.value(self.combobox_units_cake)
        dict_cake[CAKE_KEY_UNIT] = unit

        if type_cake == CAKE_KEY_TYPE_AZIM:
            self.label_azimbins_cake.setText(LABEL_CAKE_BINS_OPT)
        elif type_cake == CAKE_KEY_TYPE_RADIAL:
            self.label_azimbins_cake.setText(LABEL_CAKE_BINS_MAND)

        rad_min = self.spinbox_radialmin_cake.value()
        rad_max = self.spinbox_radialmax_cake.value()
        if rad_min >= rad_max:
            return
        dict_cake[CAKE_KEY_RRANGE] = (rad_min, rad_max)

        az_min = self.spinbox_azimmin_cake.value()
        az_max = self.spinbox_azimmax_cake.value()
        if az_min >= az_max:
            return
        dict_cake[CAKE_KEY_ARANGE] = (az_min, az_max)

        az_bins = self.spinbox_azimbins_cake.value()
        az_bins = int(az_bins)
        dict_cake[CAKE_KEY_ABINS] = az_bins

        dict_cake[KEY_INTEGRATION] = CAKE_LABEL

        return dict_cake

    @log_info
    def box_parameter_changed(self,_):
        # Fetch the integration parameters from the widgets
        dict_integration = self.fetch_box_integration_parameters()
        if not dict_integration:
            return

        # Save, overwrite the .json file
        save_integration_dictionary(dict_integration=dict_integration)

        # Input the new integration_name if needed
        lt.insert(
            listwidget=self.list_box,
            item=dict_integration[BOX_KEY_NAME],
            repeat_file=False,
        )
        self.feed_integration_widgets()

        # Update the graphs
        self.update_graphs(
            graph_1D=True,
            graph_2D_raw=True,
        )

    @log_info
    def fetch_box_integration_parameters(self):
        dict_box = dict()

        name = le.text(self.lineedit_name_box)
        if not name:
            return
        dict_box[BOX_KEY_NAME] = name

        suffix = le.text(self.lineedit_suffix_box)
        if not suffix:
            suffix = name
        dict_box[BOX_KEY_SUFFIX] = name

        direction = cb.value(self.combobox_direction_box)
        dict_box[BOX_KEY_DIRECTION] = direction

        ip_min = self.spinbox_ipmin_box.value()
        ip_max = self.spinbox_ipmax_box.value()
        if ip_min >= ip_max:
            return
        dict_box[BOX_KEY_IPRANGE] = (ip_min, ip_max)

        oop_min = self.spinbox_oopmin_box.value()
        oop_max = self.spinbox_oopmax_box.value()
        if oop_min >= oop_max:
            return
        dict_box[BOX_KEY_OOPRANGE] = (oop_min, oop_max)

        output_unit = cb.value(self.combobox_outputunits_box)
        input_unit = cb.value(self.combobox_units_box)

        dict_box[BOX_KEY_OUTPUT_UNIT] = output_unit
        dict_box[BOX_KEY_INPUT_UNIT] = input_unit

        dict_box[KEY_INTEGRATION] = BOX_LABEL

        return dict_box

    @log_info
    def button_mirror_clicked(self, state_mirror):
        # Update the label and style of button
        self.update_button_orientation(
            button_label=MIRROR_BUTTON_LABEL,
            new_state=state_mirror,
        )

        if self.h5:
            self.update_graphs(
                graph_2D_q=True,
            )

    @log_info
    def button_qz_clicked(self, state_qz):
        # Update the label and style of button
        self.update_button_orientation(
            button_label=QZ_BUTTON_LABEL,
            new_state=state_qz,
        )

        # Update the h5 integrator instance
        if self.h5:
            qz_parallel = self.state_qz
            qr_parallel = self.state_qr
            sample_or = DICT_SAMPLE_ORIENTATIONS[(qz_parallel, qr_parallel)]

            self.h5.update_orientation(
                qz_parallel=qz_parallel,
                qr_parallel=qr_parallel,
            )
            self.write_terminal_and_loggerinfo(f"New sample orientation: {sample_or}")
            self.update_graphs(
                graph_1D=True,
                graph_2D_q=True,
            )

    @log_info
    def button_qr_clicked(self, state_qr):

        # Update the label and style of button
        self.update_button_orientation(
            button_label=QR_BUTTON_LABEL,
            new_state=state_qr,
        )

        # Update the h5 integrator instance
        if self.h5:
            qz_parallel = self.state_qz
            qr_parallel = self.state_qr
            sample_or = DICT_SAMPLE_ORIENTATIONS[(qz_parallel, qr_parallel)]

            self.h5.update_orientation(
                qz_parallel=qz_parallel,
                qr_parallel=qr_parallel,
            )
            self.write_terminal_and_loggerinfo(f"New sample orientation: {sample_or}")
            self.update_graphs(
                graph_1D=True,
                graph_2D_q=True,
            )

    @log_info
    def pick_rootdir_clicked(self,_):
        # Get the address of a root directory
        root_directory = self.pick_root_directory()
        if not root_directory:
            return

        # Generate a filename for the .h5 file
        h5_filename = self.pick_h5_filename(
            root_directory=root_directory,
        )
        if not h5_filename:
            return

        # Create the H5 instance from a root directory
        if not self.init_h5_instance(
            root_directory=root_directory,
            output_filename_h5=h5_filename,
            input_filename_h5=None,
            ):
            return

        # Feed data files and ponifiles within the h5 instance
        self.h5.update_datafiles(
            search=True,
            pattern=self.get_pattern(),
        )
        self.h5.update_ponifiles()

        # Update combobox of ponifiles
        self.update_cb_ponifiles(
            from_h5=True,
            reset=True,
            relative_address=GET_RELATIVE_ADDRESS,
        )

        # Update list of samples
        self.update_listwidget_with_samples(
            listwidget=self.listwidget_samples,
            from_h5=True,
            reset=True,
            relative_address=GET_RELATIVE_ADDRESS,
        )

        # Save a .json file with the attributes of the new h5 instance
        self.save_h5_dict()

        # Update the combobox of h5 files
        self.update_combobox_h5()


    @log_info
    def init_h5_instance(
        self,
        root_directory=str(),
        output_filename_h5=str(),
        input_filename_h5=str(),
        ):
        try:
            self.h5 = H5GIIntegrator(
                root_directory=root_directory,
                output_filename_h5=output_filename_h5,
                input_h5_filename=input_filename_h5,
            )
            self.write_terminal_and_loggerinfo("H5 instance was initialized.")
            return True
        except Exception as e:
            self.h5 = None
            self.write_terminal_and_loggerinfo(f"{e}: H5 instance could not be initiliazed.")
            return False

    @log_info
    def pick_h5_filename(self, root_directory=str()):
        """
        Creates a new filename for the incoming new .h5 file

        Parameters:
        main_directory(srt, Path) : path of the root directory where all the data/metadata will be located recursively

        Return:
        None
        """
        # It has to be a Path where to search the data files
        if not root_directory:
            self.write_terminal_and_loggerinfo(ERROR_MAINDIR_DONTEXIST)
            return

        if not Path(root_directory).exists():
            self.write_terminal_and_loggerinfo(ERROR_MAINDIR_DONTEXIST)
            return
        
        # Save the .h5 file in the same main_directory root or not
        choice_hdf5 = QMessageBox.question(self, 'MessageBox', MSG_H5FILE_CHOICE, QMessageBox.Yes | QMessageBox.No)
        if choice_hdf5 == QMessageBox.Yes:
            h5_filename = root_directory
        elif choice_hdf5 == QMessageBox.No:
            h5_filename = self.pick_hdf5_folder()
        else:
            self.write_terminal_and_loggerinfo(ERROR_H5_FILECREATION)
            return

        # If there is no defined path for the future .h5 file, returns without creating the h5 file
        if not h5_filename:
            self.write_terminal_and_loggerinfo(ERROR_H5_FILECREATION)
            return
        
        # Full filename for the .h5 file
        h5_filename = Path(h5_filename)
        root_directory = Path(root_directory)
        h5_filename = h5_filename.joinpath(f"{root_directory.name}.h5")

        # Check if it is going to be overwritten
        if h5_filename.is_file():
            choice_hdf5_overwrite = QMessageBox.question(self, 'MessageBox', MSG_H5FILE_OVERWRITE, QMessageBox.Yes | QMessageBox.No)
            if choice_hdf5_overwrite == QMessageBox.Yes:
                overwrite = True
            elif choice_hdf5_overwrite == QMessageBox.No:
                overwrite = False
            else:
                self.write_terminal_and_loggerinfo(ERROR_H5_FILECREATION)
                return
        else:
            overwrite = True

        # Join date_prefix if no overwriting
        if not overwrite:
            h5_filename = h5_filename.joinpath(f"{root_directory.name}_{date_prefix()}.h5")

        return h5_filename


    @log_info
    def pick_root_directory(self, timeout=1e9) -> Path:
        """
        Picks a folder as main directory, the root where the data files are searched recursively

        Parameters:
        None

        Returns:
        Path: path instance of the root directory to search data files
        """
        # Pick the folder after pop-up browser window
        self.dialog_maindir = QFileDialog()
        get_directory = self.dialog_maindir.getExistingDirectory(self, 'Choose main directory', str(GLOBAL_PATH))


        # Returns if is not valid, or the dialog was cancelled
        if not get_directory:
            main_directory = ""
            self.write_terminal_and_loggerinfo(ERROR_PICK_FOLDER)
        else:
            try:
                main_directory = Path(get_directory)
            except NotImplementedError:
                main_directory = ""
                self.write_terminal_and_loggerinfo(ERROR_PICK_FOLDER)
        return main_directory




    @log_info
    def get_full_folderpath(self, folder_relative_name=str()) -> Path:
        """
        Join the folder_name (relative to) with the main_directory
        """
        if not self.main_directory:
            return

        folder_relative_name = Path(folder_relative_name)
        full_folder_name = self.main_directory.joinpath(folder_relative_name)
        return full_folder_name

    @log_info
    def pick_hdf5_folder(self) -> Path:
        """
        Picks a folder to save the .h5 file

        Parameters:
        None

        Returns:
        Path: path for the new .h5
        """
        # It has to be a Path where to search the data files
        if not self.main_directory:
            self.write_terminal_and_loggerinfo(ERROR_MAINDIR_DONTEXIST)
            return
        
        dialog_h5_dir = QFileDialog.getExistingDirectory(self, 'Choose main directory', ".")

        if not dialog_h5_dir:
            self.write_terminal_and_loggerinfo(ERROR_H5DIR)
            h5_dir = ""
        else:
            try:
                h5_dir = Path(dialog_h5_dir)
            except NotImplementedError:
                h5_dir = ""
                self.write_terminal_and_loggerinfo(ERROR_H5DIR)

        return h5_dir


    @log_info
    def pick_h5file_clicked(self, _):
        # Get the address of the .h5 file
        h5_filename = self.pick_h5_file()
        if not h5_filename:
            return

        h5_recent_files = self.get_recent_h5_files()

        if h5_filename in h5_recent_files:
            self.write_terminal_and_loggerinfo(f"{h5_filename} is already imported.")
            return

        # Initiate H5 instance from a .h5 file
        if not self.init_h5_instance(
            input_filename_h5=h5_filename,
            ):
            return

        # Update combobox of ponifiles
        self.update_cb_ponifiles(
            from_h5=True,
            reset=True,
            relative_address=GET_RELATIVE_ADDRESS,
        )

        # Update list of samples
        self.update_listwidget_with_samples(
            listwidget=self.listwidget_samples,
            from_h5=True,
            reset=True,
            relative_address=GET_RELATIVE_ADDRESS,
        )

        # Save a .json file with the attributes of the new h5 instance
        self.save_h5_dict()

        # Update the combobox of h5 files
        self.update_combobox_h5()


    @log_info
    def pick_h5_file(self):
        h5_file = QFileDialog.getOpenFileNames(self, 'Pick .hdf5 file', '.', "*.h5")
        try:
            h5_file = h5_file[0][0]
            h5_file = Path(h5_file)
            return h5_file
        except Exception as e:
            return

    @log_info
    def pick_and_activate_hdf5_file(self) -> None:
        """
        Opens a browser to pick a .hdf5 file

        Parameters:
        None

        Returns:
        None
        """
        if self.main_directory:
            h5_file = QFileDialog.getOpenFileNames(self, 'Pick .hdf5 file', str(self.main_directory), "*.h5")
        else:
            h5_file = QFileDialog.getOpenFileNames(self, 'Pick .hdf5 file', '.', "*.h5")

        if h5_file:
            try:
                h5_file = h5_file[0][0]

                self.append_h5_file(
                    h5_file=h5_file,
                )

                cb.set_text(
                    combobox=self.combobox_h5_files,
                    text=h5_file,
                )
            except:
                logger.info("No .h5 file was picked.")
        else:
            return

    @log_info
    def cb_h5_changed(self, json_name):
        # Return if empty
        if not json_name:
            self.reset_attributes_and_widgets()
            return

        # Fetch the full filename
        json_filename = H5_FILES_PATH.joinpath(json_name)
        try:
            dict_h5 = open_json(json_filename)
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: The .json does not contain a valid filename: {json_filename}")
            return

        # Check if this file still exists
        filename_h5 = dict_h5[FILENAME_H5_KEY]
        if not Path(filename_h5).is_file():
            self.write_terminal_and_loggerinfo(f"The file {filename_h5} does not exists.")
            return
        
        # Create the h5 instance from an existing .h5 file
        self.init_h5_instance(
            input_filename_h5=filename_h5,
        )
        if not self.h5:
            return
        
        # Update label
        le.substitute(
            lineedit=self.lineedit_h5file_1,
            new_text=str(filename_h5),
        )

        # Update plain text with h5 information
        self.update_h5_plaintext()

        # Update combobox of ponifiles
        self.update_cb_ponifiles(
            from_h5=True,
            reset=True,
        )

        # Update list of samples and reference combobox
        self.update_listwidget_with_samples(
            listwidget=self.listwidget_samples,
            from_h5=True,
            reset=True,
        )
        self.update_combobox_with_samples(
            combobox=self.combobox_reffolder,
            from_h5=True,
            reset=True,
        )

        self.h5.update_orientation(
            qz_parallel=self.state_qz,
            qr_parallel=self.state_qr,
        )




    @log_info
    def update_h5_plaintext(self):
        self.h5_plaintext.clear()
        if self.h5:
            d = self.h5.h5_get_dict_attrs()
            for k,v in d.items():
                self.h5_plaintext.appendPlainText(f"{str(k)} : {str(v)}\n")

    ##################################################
    ############# PONIFILE METHODS ###################
    ##################################################

    @log_info
    def update_cb_ponifiles(
        self, 
        from_h5=False, 
        ponifile_list=list(), 
        reset=True,
        relative_address=True,
        ):
        if not self.h5:
            return

        # Combobox
        cb_ponifile = self.combobox_ponifile

        # Add ponifiles from h5 instance
        if from_h5:
            # Fetch ponifiles from h5 instance
            ponifiles_in_h5 = self.h5.get_all_ponifiles(get_relative_address=relative_address)
            ponifile_list = ponifiles_in_h5

        if reset:
            cb.insert_list(
                combobox=cb_ponifile,
                list_items=ponifile_list,
                reset=True,
            )
        else:
            # Filter the new files
            ponifiles_in_cb = cb.all_items(cb_ponifile)
            new_ponifiles = [file for file in ponifile_list if file not in ponifiles_in_cb]
            new_ponifiles = [file for file in new_ponifiles if file]
            new_ponifiles.sort()

            cb.insert_list(
                combobox=cb_ponifile,
                list_items=new_ponifiles,
                reset=False,
            )

    @log_info
    def cb_ponifile_changed(self, poni_name):
        if not self.h5:
            return

        # Activate the .poni file in the h5 instance
        self.h5.activate_ponifile(
            poni_filename=poni_name,
        )
        
        # Check if the .poni file does exist
        if self.h5.active_ponifile:
            self.write_terminal_and_loggerinfo(f"Activated {self.h5.active_ponifile}")
            # self.write_terminal_and_loggerinfo(self.h5)
        else:
            self.write_terminal_and_loggerinfo(f"No active ponifile.")
            return

        if not Path(self.h5.active_ponifile).is_file():
            self.write_terminal_and_loggerinfo(f"The .poni file {str(self.h5.active_ponifile)} does not exist.")
            return
        
        # Update the .poni tab widgets
        dict_poni = self.h5.get_poni_dict()
        self.update_ponifile_widgets(
            dict_poni=dict_poni,
        )

        # Update_graphs
        self.update_graphs(
            graph_1D=True,
            graph_2D_q=True,
            graph_2D_reshape=True,
        )

    @log_info
    def retrieve_old_poni_clicked(self,_):
        if not self.h5:
            return
        
        dict_poni = self.h5.get_poni_dict()
        self.update_ponifile_widgets(
            dict_poni=dict_poni,
        )
    
    @log_info
    def update_poni_clicked(self,_):
        if not self.h5:
            return
        
        dict_poni = self.get_poni_dict_from_widgets()
        self.h5.update_ponifile_parameters(
            dict_poni=dict_poni,
        )

    @log_info
    def save_poni_clicked(self,_):
        if not self.h5:
            return
        
        # Get a full poni dictionary from the widgets and h5
        dict_poni = self.get_poni_dict_from_widgets()

        # Save a .poni file
        self.save_poni_dict(
            dict_poni=dict_poni,
        )

        # Update the h5 and combobox
        self.h5.h5_update_ponifiles(search=True)
        self.update_cb_ponifiles(from_h5=True)

    @log_info
    def get_poni_dict_from_widgets(self) -> dict:
        """
        Returns a dictionary with poni parameters from the widgets
        """
        if not self.h5:
            return
        try:
            wave = float(le.text(self.lineedit_wavelength))
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Wavelength could not be retrieved from widget.")
            return
        try:
            dist = float(le.text(self.lineedit_distance))
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Distance could not be retrieved from widget.")
            return
        try:
            poni1 = float(le.text(self.lineedit_poni1))
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: PONI 1 could not be retrieved from widget.")
            return
        try:
            poni2 = float(le.text(self.lineedit_poni2))
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: PONI 2 could not be retrieved from widget.")
            return
        try:
            rot1 = float(le.text(self.lineedit_rot1))
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Rotation 1 could not be retrieved from widget.")
            return
        try:
            rot2 = float(le.text(self.lineedit_rot2))
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Rotation 2 could not be retrieved from widget.")
            return
        try:
            rot3 = float(le.text(self.lineedit_rot3))
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Rotation 3 could not be retrieved from widget.")
            return
        
        dict_poni = self.h5.get_poni_dict()
        dict_poni[PONI_KEY_WAVELENGTH] = wave
        dict_poni[PONI_KEY_DISTANCE] = dist
        dict_poni[PONI_KEY_PONI1] = poni1
        dict_poni[PONI_KEY_PONI2] = poni2
        dict_poni[PONI_KEY_ROT1] = rot1
        dict_poni[PONI_KEY_ROT2] = rot2
        dict_poni[PONI_KEY_ROT3] = rot3

        return dict_poni
        
    @log_info
    def update_dict_poni_cache(self) -> dict:
        """
        Returns a dictionary with poni parameters from the widgets
        """
        if not self.h5:
            return

        try:
            wave = float(le.text(self.lineedit_wavelength))
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Wavelength could not be retrieved from widget.")
            return
        try:
            dist = float(le.text(self.lineedit_distance))
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Distance could not be retrieved from widget.")
            return
        try:
            poni1 = float(le.text(self.lineedit_poni1))
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: PONI 1 could not be retrieved from widget.")
            return
        try:
            poni2 = float(le.text(self.lineedit_poni2))
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: PONI 2 could not be retrieved from widget.")
            return
        try:
            rot1 = float(le.text(self.lineedit_rot1))
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Rotation 1 could not be retrieved from widget.")
            return
        try:
            rot2 = float(le.text(self.lineedit_rot2))
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Rotation 2 could not be retrieved from widget.")
            return
        try:
            rot3 = float(le.text(self.lineedit_rot3))
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Rotation 3 could not be retrieved from widget.")
            return

        self._dict_poni_cache[PONI_KEY_WAVELENGTH] = wave
        self._dict_poni_cache[PONI_KEY_DISTANCE] = dist
        self._dict_poni_cache[PONI_KEY_PONI1] = poni1
        self._dict_poni_cache[PONI_KEY_PONI2] = poni2
        self._dict_poni_cache[PONI_KEY_ROT1] = rot1
        self._dict_poni_cache[PONI_KEY_ROT2] = rot2
        self._dict_poni_cache[PONI_KEY_ROT3] = rot3

    @log_info
    def update_ponifile_widgets(self, dict_poni=dict()) -> None:
        """
        Update the ponifile widgets from a poni dictionary
        """
        if not self.h5:
            return
        try:
            detector_name = dict_poni[PONI_KEY_DETECTOR]
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Detector name could not be retrieved from dictionary.")
            return
        try:
            detector_bin = dict_poni[PONI_KEY_BINNING]
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Detector bin could not be retrieved from dictionary.")
            return
        try:
            wave = dict_poni[PONI_KEY_WAVELENGTH]
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Wavelength could not be retrieved from dictionary.")
            return
        try:
            dist = dict_poni[PONI_KEY_DISTANCE]
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Distance could not be retrieved from dictionary.")
            return
        try:
            pixel1 = dict_poni[PONI_KEY_PIXEL1]
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Pixel 1 could not be retrieved from dictionary.")
            return
        try:
            pixel2 = dict_poni[PONI_KEY_PIXEL2]
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Pixel 2 could not be retrieved from dictionary.")
            return
        try:
            shape1 = dict_poni[PONI_KEY_SHAPE1]
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Shape 1 could not be retrieved from dictionary.")
            return
        try:
            shape2 = dict_poni[PONI_KEY_SHAPE2]
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Shape 2 could not be retrieved from dictionary.")
            return
        try:
            poni1 = dict_poni[PONI_KEY_PONI1]
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: PONI 1 could not be retrieved from dictionary.")
            return
        try:
            poni2 = dict_poni[PONI_KEY_PONI2]
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: PONI 2 could not be retrieved from dictionary.")
            return
        try:
            rot1 = dict_poni[PONI_KEY_ROT1]
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Rotation 1 could not be retrieved from dictionary.")
            return
        try:
            rot2 = dict_poni[PONI_KEY_ROT2]
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Rotation 2 could not be retrieved from dictionary.")
            return
        try:
            rot3 = dict_poni[PONI_KEY_ROT3]
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Rotation 3 could not be retrieved from dictionary.")
            return

        detector_info = f"{str(detector_name)} / {str(detector_bin)} / ({shape1},{shape2}) / ({pixel1},{pixel2})"

        if self.h5.active_ponifile:
            le.substitute(
                lineedit=self.lineedit_detector,
                new_text=detector_info,
            )
            le.substitute(
                lineedit=self.lineedit_wavelength,
                new_text=wave,
            )
            le.substitute(
                lineedit=self.lineedit_distance,
                new_text=dist,
            )
            le.substitute(
                lineedit=self.lineedit_poni1,
                new_text=poni1,
            )
            le.substitute(
                lineedit=self.lineedit_poni2,
                new_text=poni2,
            )
            le.substitute(
                lineedit=self.lineedit_rot1,
                new_text=rot1,
            )
            le.substitute(
                lineedit=self.lineedit_rot2,
                new_text=rot2,
            )
            le.substitute(
                lineedit=self.lineedit_rot3,
                new_text=rot3,
            )

    @log_info
    def update_ponifile_parameters(self, dict_poni=dict()) -> None:
        """
        Changes the functinal poni parameters stored in h5 instance
        """
        if not self.h5:
            return

        self.h5.update_ponifile_parameters(
            dict_poni=dict_poni,
        )

    @log_info
    def save_poni_dict(self, dict_poni=dict()) -> None:
        """
        Saves a new .poni file with updated parameters
        """
        if not self.h5:
            return
        ponifile = str(self.h5.active_ponifile)
        ponifile = ponifile.replace(".poni", f"_{date_prefix()}.poni")

        with open(ponifile, "w+") as fp:
            json.dump(dict_poni, fp)


    @log_info
    def update_reference_widgets(self) -> None:
        """
        Update the reference file widget
        """
        if not self.h5:
            return

        if self.checkbox_auto_reffile.isChecked():
            cb.clear(self.combobox_reffile)
            return

        # Get the name of the folder
        name_ref_folder = cb.value(self.combobox_reffolder)

        # Get the list of files
        list_ref_files = sorted(self.h5.generator_files_in_sample(
            sample_name=name_ref_folder,
            sample_relative_address=True,
            get_relative_address=True,
        ))
        cb.insert_list(
            combobox=self.combobox_reffile,
            list_items=list_ref_files,
            reset=True,
        )

    @log_info
    def checkbox_reference_clicked(self, auto_ref):
        """
        Enable or disable the combobox to choose a reference file within the reference folder
        """
        if auto_ref:
            self.combobox_reffile.setEnabled(False)
        else:
            self.combobox_reffile.setEnabled(True)

        # Feed reference widgets
        self.update_reference_widgets()

        # Update the data if needed
        self.update_cache_data()

        # Update graphs
        self.update_graphs(
            graph_1D=True,
            graph_2D_raw=True,
            graph_2D_reshape=True,
            graph_2D_q=True,
        )

    @log_info
    def get_pattern(self):
        wildcards = le.text(self.lineedit_wildcards).strip()
        extension = cb.value(self.combobox_extension)
        pattern = wildcards + extension
        pattern = pattern.replace('**', '*')
        return pattern

    @log_info
    def update_listwidget_with_samples(
        self, 
        listwidget,
        from_h5=False, 
        list_samples=list(),
        reset=True,
        relative_address=True,
        ):
        if not self.h5:
            return        

        # Add samples from h5 instance
        if from_h5:
            samples_in_h5 = self.h5.get_all_samples(get_relative_address=relative_address)
            list_samples = samples_in_h5
        
        if not list_samples:
            return

        if reset:
            lt.insert_list(
                listwidget=listwidget,
                item_list=list_samples,
                reset=True,
            )
        else:
            # Filter the new files
            samples_in_widget = lt.all_items(listwidget=listwidget)
            new_samples = [s for s in list_samples if s not in samples_in_widget]
            new_samples = [s for s in new_samples if s]
            new_samples.sort()
            lt.insert_list(
                listwidget=listwidget,
                item_list=new_samples,
                reset=False,
            )

    @log_info
    def update_combobox_with_samples(
        self, 
        combobox=None,
        from_h5=False, 
        list_samples=list(),
        reset=True,
        # relative_to=True,
        ):

        # Add samples from h5 instance
        if from_h5:
            if not self.h5:
                return
            # Fetch samples from h5 instance
            samples_in_h5 = self.h5.get_all_samples()
            list_samples = samples_in_h5

        # Make it relative
        # if relative_to:
        #     root_dir = Path(self.h5._root_dir)
        #     list_samples = [str(Path(file).relative_to(root_dir)) for file in list_samples]

        if reset:
            cb.insert_list(
                combobox=combobox,
                list_items=list_samples,
                reset=True,
            )
        else:
            # Filter the new files
            samples_in_widget = cb.all_items(combobox=combobox)
            new_samples = [s for s in list_samples if s not in samples_in_widget]
            new_samples = [s for s in new_samples if s]
            new_samples.sort()
            cb.insert_list(
                combobox=combobox,
                list_items=new_samples,
                reset=False,
            )

    @log_info
    def open_pyFAI_calib2(self,_) -> None:
        """
            Open pyFAI-calib2 GUI, depends on the OS
        """
        dict_calib2_os = {
            'linux': self.open_pyFAI_calib2_linux,
            'linux2': self.open_pyFAI_calib2_linux,
            'win32': self.open_pyFAI_calib2_windows,
        }
        try:
            dict_calib2_os[sys.platform]()
        except:
            return

    @log_info
    def open_pyFAI_calib2_linux(self) -> None:
        """
            If the OS is linux, open pyFAI-calib2 GUI
        """
        if not self.h5:
            open_directory = self.h5.get_main_directory()
        else:
            open_directory = ""
        try:
            subprocess.run([join(GLOBAL_PATH, 'bash_files', 'open_calib2.sh'), open_directory])
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: pyFAI GUI could not be opened.")
        finally:
            self.search_and_update_ponifiles_widgets()

    @log_info
    def open_pyFAI_calib2_windows(self) -> None:
        """
            If the OS is Windows, open pyFAI-calib2 GUI
        """
        if self.h5:
            open_directory = self.h5._root_dir
        else:
            open_directory = ""

        try:
            os.system(f"cd {open_directory}")
            calib_path = str(Path(pyfai_file).parent.joinpath("app", "calib2.py"))
            cmd = f"{sys.executable} {calib_path}"
            os.system(cmd)
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: pyFAI GUI could not be opened.")
        finally:
            self.search_and_update_ponifiles_widgets()
           
    # #########################
    # # Search engines
    # #########################


    @log_info
    def update_all_files(self,_):
        if not self.h5:
            return
        # Get a dictionary with the new files (not stored in h5)
        dict_new_files = self.h5.search_new_datafiles(
            pattern=self.get_pattern(),
        )
        self.write_terminal_and_loggerinfo(f"New detected files: {str(dict_new_files)}.")
        
        self.h5.update_datafiles(          
            dict_new_files=dict_new_files,
            search=False,
        )
        self.h5.update_ponifiles(
            search=True,
        )

        # Update combobox of ponifiles
        self.update_cb_ponifiles(
            from_h5=True,
            reset=True,
        )

        # Update list of samples
        self.update_listwidget_with_samples(
            listwidget=self.listwidget_samples,
            from_h5=True,
            reset=True,
        )

        # Get a Pandas.DataFrame to upload the table
        keys_to_display = self.combobox_metadata.currentData()
        dataframe = self.h5.get_metadata_dataframe(
            sample_name=self.sample_cache,
            list_keys=keys_to_display,
        )

        # Reset and feed the table widget with default metadata keys if needed
        self.update_table(
            dataframe=dataframe,
            reset=True,
        )




    @log_info
    def live_clicked(self,state_live):
        platform = sys.platform
        if 'linux' not in platform:
            self.write_terminal_and_loggerinfo(f"The operating system {platform} is not compatible with live searching.")
            return

        # Update style of the button
        self.update_button_live(state_live)

        if not self.h5:
            return

        if not state_live:

            self.h5.stop_live_mode()
            self.write_terminal_and_loggerinfo(f"LIVE Mode OFF")
            return

        # First search off the line
        self.update_all_files(None)

        # Start live mode
        self.start_live_mode(
            pattern=self.get_pattern(),
        )

    @log_info
    def start_live_mode(self, pattern=None):
        if pattern is None:
            logger.info(f"No pattern to search in live mode.")
            return

        # # If live is on, start the live searching engine, only for Linux
        platform = sys.platform
        if 'linux' in platform:
            self.timer_data = QTimer()

            # Start the loop each second
            self.timer_data.timeout.connect(
                lambda: (
                    self.search_live_files(pattern=pattern),
                )
            )

            # Get last file and update
            # self.update_widgets_to_last_file()

            self.timer_data.start(INTERVAL_SEARCH_DATA)
            logger.info("LIVE ON: Now, the script is looking for new files...")
        else:
            logger.info(f"The operating system {platform} is not compatible with live searching.")

    @log_info
    def stop_live_mode(self):
        # # If live is on, start the live searching engine, only for Linux
        if self.timer_data:
            self.timer_data.stop()
            logger.info("LIVE: OFF. The script stopped looking for new files.")
        else:
            logger.info(f"LIVE: OFF. The script stopped looking for new files.")

    def search_live_files(self, pattern=None) -> None:
        list_files_1s = []
        cmd = f"find {str(self.h5._root_dir)} -name {pattern} -newermt '-1 seconds'"
        try:
            list_files_1s = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True).stdout.decode().strip().split('\n')
            # Clean empty items
            list_files_1s = [item for item in list_files_1s if item]
        except:
            logger.info(f"Error while running the bash script.")

        if list_files_1s:
            logger.info(f"Found new files LIVE: {list_files_1s}")

            # Upload the new files to h5
            dict_files_1s = get_dict_files(list_files=list_files_1s, relative_root=None)
            self.h5.update_datafiles(          
                dict_new_files=dict_files_1s,
                search=False,
                relative_to_root=RELATIVE_TO_ROOT,
            )

            # Update list of samples
            self.update_listwidget_with_samples(
                listwidget=self.listwidget_samples,
                from_h5=True,
                reset=True,
                # relative_to_root=RELATIVE_TO_ROOT,
            )

            # Update table if needed
            # Get a Pandas.DataFrame to upload the table
            keys_to_display = self.combobox_metadata.currentData()
            dataframe = self.h5.get_metadata_dataframe(
                sample_name=self.sample_cache,
                list_keys=keys_to_display,
            )

            # Reset and feed the table widget with default metadata keys if needed
            self.update_table(
                dataframe=dataframe,
                reset=True,
            )

            # Go to the last file
            last_file = self.h5.get_last_file(list_files=list_files_1s)
            sample, index = self.h5.get_sample_index_from_filename(filename=last_file)
            self.sample_cache = sample
            self.cache_index = index
            self.update_cache_data(
                sample_name=sample,
                list_index=index,
            )
            self.update_label_displayed()
            self.update_graphs(
                graph_1D=True,
                graph_2D_q=True,
                graph_2D_raw=True,
                graph_2D_reshape=True,
            )
        else:
            return





    @log_info
    def update_h5_poni_and_files(self) -> None:
        """
        Searches new files and updates the data/metadata files in the h5 file

        Parameters:
        None

        Returns:
        None
        """
        if self.h5:
            # Search ponifiles and updates them in the .h5 file
            self.search_and_update_ponifiles_widgets()

            # Searches files and update the Data/Metadat in Groups and Datasets in the .h5 file
            self.h5.search_and_update_datafiles(
                pattern=self.get_pattern(),
            )
            self.write_terminal_and_loggerinfo(INFO_H5_UPDATED)
        else:
            self.write_terminal_and_loggerinfo(ERROR_H5_UPDATED)

    @log_info
    def save_h5_dict(self):
        if not self.h5:
            return

        # Get the output name for the .json
        name_json = self.h5._name.replace(".h5", ".json")
        filename_out = H5_FILES_PATH.joinpath(f"{name_json}")

        # Fetch the dictionary of attributes from the h5 instance
        dict_h5 = self.h5.h5_get_dict_attrs()

        # Save the dictionary as a .json file
        with open(filename_out, 'w+') as fp:
            json.dump(dict_h5, fp)

    @log_info
    def append_h5file(self, h5_path=str()) -> None:
        """
        Register the filename of the .h5 file into the .json file

        Parameters:
        h5_path(str, Path) : path of an existing .h5 file, that will be appended to the combobox

        Returns:
        None
        """
        # If no input, take the filename associated to the active H5Integrator instance
        # if not h5_path:
        #     try:
        #         h5_path = str(self.h5.filename_h5)
        #     except AttributeError:
        #         self.write_terminal_and_logger(ERROR_H5_NOTEXISTS)
        #         return
        # else:
        #     self.write_terminal_and_logger(ERROR_APPEND_H5)
        #     return
        # logger.info(f"New .h5 file to append {h5_path}")

        # Append to .txt file        
        if Path(JSON_FILE_H5).is_file():
            with open(JSON_FILE_H5, "a+") as fp:
                fp.write(f"{str(h5_path)}\n")
        else:
            with open(JSON_FILE_H5, "w+") as fp:
                fp.write(f"\n")
                fp.write(f"{str(h5_path)}\n")
        logger.info(f"Current list of .h5 files.")

        # Append to combobox if it's new
        filenames_from_cb = cb.all_items(self.combobox_h5_files)
        if h5_path in filenames_from_cb:
            return

        # Append to dictionary
        h5_path = Path(h5_path)
        short_name = str(Path(h5_path).name)
        self.dict_recent_h5[short_name] = str(h5_path)

        cb.insert(
            combobox=self.combobox_h5_files,
            item=short_name,
        )

    @log_info
    def update_widgets(self) -> None:
        """
        To be used after updating the .h5 file
        This method may update the list_widget of folders and the table_widget with files and metadata
        """
        if self.h5:
            # Main lineedit
            le.substitute(
                lineedit=self.lineedit_h5file,
                new_text=self.h5.filename_h5,
            )

            # Check if new folders to update the list_widget and reference folder combobox
            folders_in_list = set(lt.all_items(self.listwidget_samples))
            folders_in_h5 = set(self.h5.generator_samples())
            new_folders = [item for item in folders_in_h5.difference(folders_in_list)]
            new_folders.sort()

            if new_folders:
                # List widget
                lt.insert_list(
                    listwidget=self.listwidget_samples,
                    item_list=new_folders,
                    reset=False,
                )
                logger.info(INFO_LIST_FOLDERS_UPDATED)

                # Reference combobox
                cb.insert_list(
                    combobox=self.combobox_reffolder,
                    list_items=new_folders,
                    reset=False,
                )
            else:
                logger.info(INFO_LIST_NO_FOLDERS_TO_UPDATE)

            # Check if the table (click_folder) should be updated
            if not self.clicked_folder:
                return

            num_files_in_table = tm.get_row_count(self.table_files)
            num_files_in_h5 = self.h5.number_files_in_sample(self.clicked_folder)
            logger.info(f"There are {num_files_in_table} files in the table and {num_files_in_h5} files in the .h5")
            if num_files_in_h5 != num_files_in_table:
                self.update_comboboxes_metadata_items()
                self.update_table(
                    reset=True,
                )
            else:
                logger.info("The table was not updated.")
        else:
            self.write_terminal_and_loggerinfo(ERROR_H5_NOTEXISTS)

    def update_widgets_to_last_file(self, last_file=str()):
        """
        Updates atributes and graphs to the last detected file

        Parameters:
        last_file(str) : string of the file, if not, the last file will be detected

        Returns:
        None
        """
        if self.h5:
            if not last_file:
                last_file = self.h5.get_last_file()
            last_file_folder, last_file_index = self.h5.get_sample_index_from_filename(
                filename=last_file,
            )
            if last_file_folder and last_file_index:
                # self.clicked_folder = last_file_folder
                self.cache_index = last_file_index
                # logger.info(f"Updated clicked folder: {self.clicked_folder} and cache index: {self.cache_index}")
                self.update_cache_data(),
                self.update_1D_graph(),
                self.update_2D_raw(),
                self.update_2D_reshape_map(),
                self.update_2D_q(),
            else:
                logger.info("Last file was not updated.")
            
    @log_info
    def update_widgets_from_h5(self):

        if self.h5:
            # Update the main directory, files and folder attributes
            self.main_directory = self.h5.get_root_directory()
            # self.lineedit_maindir.setText(str(self.main_directory))
            self.write_terminal_and_loggerinfo(MSG_MAIN_DIRECTORY)
            self.write_terminal_and_loggerinfo(f"New main directory: {str(self.main_directory)}")

            # Update file and folder attributes
            self.list_folders = list(self.h5.generator_samples())
            self.write_terminal_and_loggerinfo(f"Added {len(self.list_folders)} folders.")

            # Feed the ponifile combobox
            ponifile_list = self.h5.get_ponifile_list()
            ponifile_list = [str(Path(item).relative_to(self.main_directory)) for item in ponifile_list]

            cb.insert_list(
                combobox=self.combobox_ponifile,
                list_items=ponifile_list,
                reset=True,
            )

            # Reset and fill the list widget with folders
            lt.insert_list(
                listwidget=self.listwidget_samples,
                item_list=list(self.h5.generator_samples()),
                reset=True,
            )

            # Feed the combobox of reference folder and masks
            cb.insert_list(
                combobox=self.combobox_reffolder,
                list_items=list(self.h5.generator_samples()),
            )

    @log_info
    def listsamples_clicked(self, clicked_sample_name, sample_relative_address=GET_RELATIVE_ADDRESS):
        if not self.h5:
            return
        
        # Fetch the name of the integration
        clicked_sample_name = clicked_sample_name.text()
        if clicked_sample_name:
            self.sample_cache = clicked_sample_name

        # Update the metadata combobox if needed
        self.check_and_update_cb_metadata(
            sample_name=clicked_sample_name,
            sample_relative_address=sample_relative_address,
        )

        # Get a Pandas.DataFrame to upload the table
        keys_to_display = self.combobox_metadata.currentData()
        dataframe = self.h5.get_metadata_dataframe(
            sample_name=clicked_sample_name,
            list_keys=keys_to_display,
        )

        # Reset and feed the table widget with default metadata keys if needed
        self.update_table(
            dataframe=dataframe,
            reset=True,
        )

    @log_info
    def cb_metadata_changed(self, _):
        # Get a Pandas.DataFrame to upload the table
        keys_to_display = self.combobox_metadata.currentData()
        dataframe = self.h5.get_metadata_dataframe(
            sample_name=self.sample_cache,
            list_keys=keys_to_display,
        )

        # Reset and feed the table widget with default metadata keys if needed
        self.update_table(
            dataframe=dataframe,
            reset=True,
        )

    @log_info
    def metadata_setup_keys(self):
        dict_metadata = self.fetch_dict_metadata()
        metadata_keys = dict_metadata.values()
        return metadata_keys
        
    @log_info
    def check_and_update_cb_metadata(
        self, 
        sample_name=str(),
        sample_relative_address=True,
        ):
        if not sample_name:
            sample_name = self.sample_cache

        # Fetch the list of metadata keys in that sample
        metadata_keys = self.h5.get_all_metadata_keys_from_sample(
            sample_name=sample_name,
            sample_relative_address=sample_relative_address,
        )

        # Update the comboboxes if it is different
        metadata_keys_displayed = cb.all_items(self.combobox_metadata)

        if metadata_keys != metadata_keys_displayed:
            self.update_comboboxes_metadata_items(
                metadata_keys=metadata_keys,
                reset=True,
            )

    @log_info
    def update_comboboxes_metadata_items(self, metadata_keys=list(), reset=True) -> None:
        self.combobox_metadata.addItems(texts=metadata_keys)
        self.combobox_headeritems_title.addItems(texts=metadata_keys)

        # Combobox for dict_setup keys
        self.combobox_angle.addItems(texts=metadata_keys)
        self.combobox_tilt_angle.addItems(texts=metadata_keys)
        self.combobox_normfactor.addItems(texts=metadata_keys)
        self.combobox_acquisition.addItems(texts=metadata_keys)

    @log_info
    def update_sample_orientation(self):
        active_sample = self.sample_cache

        if not active_sample or not self.cache_index:
            return

        incident_angle = self.h5.get_incident_angle(
            sample_name=active_sample,
            index_list=self.cache_index,
        )
        tilt_angle = self.h5.get_tilt_angle(
            sample_name=active_sample,
            index_list=self.cache_index,
        )
        self.h5.update_incident_tilt_angle(
            incident_angle=incident_angle,
            tilt_angle=tilt_angle,
        )




    @log_info
    def tab_graph_changed(self,_):
        self.update_graphs(
            graph_1D=True,
            graph_2D_raw=True,
            graph_2D_reshape=True,
            graph_2D_q=True,
        )


    @log_info
    def update_cache_data(self, sample_name=str(), list_index=list()):  
        # Take the new data from new folder/index
        data = self.get_data(
            sample_name=sample_name,
            list_index=list_index,
        )
        if data is None:
            return

        # Subtract the reference
        if self.spinbox_sub.value() != 0.0:
            data = self.get_subtracted_data(
                data=data,
            )
        
        # Filter the data
        data = self.filter_data(
            data=data,
        )        

        # Update the data cache
        self._data_cache = data

    @log_info
    def update_2D_q(self, new_data=True):

        if self.tab_graph_widget.currentIndex() != INDEX_TAB_Q_MAP:
            return

        try:
            self.update_q_matrix_cache(
                new_data=new_data,
            )
            self.plot_qcache_matrix()
            self.update_qmap_style()
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Error during updating q-map map.")

    @log_info
    def sub_factor_changed(self, scale_factor):
        self.update_cache_data(
            sample_name=self.sample_cache,
            list_index=self.cache_index,
        )

        self.update_graphs(
            graph_1D=True,
            graph_2D_raw=True,
            graph_2D_reshape=True,
            graph_2D_q=True,
        )

    @log_info
    def get_subtracted_data(self, data=None):

        if data is None:
            return
        if not self.h5:
            return

        reference_folder_name = cb.value(self.combobox_reffolder)
        logger.info(f"Reference folder: {reference_folder_name}")

        full_reference_filename, index_ref = self.get_reference_file(
            sample_reference=reference_folder_name,
            return_index=True,
        )

        if not full_reference_filename:
            return

        self.write_terminal_and_loggerinfo(f"Reference file: {full_reference_filename}.")

        reference_name = Path(full_reference_filename).name
        if self.checkbox_auto_reffile.isChecked():
            cb.clear(self.combobox_reffile)
            cb.insert(
                combobox=self.combobox_reffile,
                item=f"(Auto): {reference_name}",
            )

        data_ref = self.h5.get_Edf_data(
            full_filename=full_reference_filename,
            sample_name=reference_folder_name,
            index_list=index_ref,
            normalized=True,
        )
        reference_factor = self.spinbox_sub.value()
        logger.info(f"New reference factor: {reference_factor}")

        if data_ref is not None:
            data = data - reference_factor * data_ref

        return data

    @log_info
    def get_reference_file(self, sample_reference=str(), return_index=False) -> str:
        """
        Returns the full filename to be subtracted from the sample data
        """
        if not self.h5:
            return

        # Automatic searching of file through the acquisition time
        if self.checkbox_auto_reffile.isChecked():
            index = 0
            if not self.h5.get_acquisition_key():
                self.write_terminal_and_loggerinfo("There is no key for acquisition time. Reference subtraction is not possible.")
                return None, None

            acq_time_file = self.h5.get_acquisition_time(
                folder_name=self.sample_cache,
                index_list=self.cache_index,
            )
            logger.info(f"Acquisition time of the sample is {acq_time_file}.")

            acq_ref_dataset = self.h5.get_dataset_acquisition_time(
                sample_name=sample_reference,
            )
            logger.info(f"Acquisition dataset of the reference folder is {acq_ref_dataset}.")
            full_reference_filename = ""
            
            if (acq_time_file is not None) and (acq_ref_dataset is not None):
                for index, exp_ref in enumerate(acq_ref_dataset):
                    if exp_ref == acq_time_file:
                        full_reference_filename = self.h5.get_filename_from_index(
                            sample_name=sample_reference,
                            index_list=index,
                        )
                        logger.info(f"Auto reference file: {full_reference_filename}")
                        break
                if not full_reference_filename:
                    logger.info(f"There is no match in acquisition times.")
                
        # Specific reference file
        else:
            index = 0
            file_reference_name = cb.value(self.combobox_reffile)
            full_reference_filename = str(self.h5._root_dir.joinpath(Path(sample_reference), Path(file_reference_name)))
            logger.info(f"Chosen reference file: {full_reference_filename}.")

        if return_index:
            return full_reference_filename, index
        else:
            return full_reference_filename


    @log_info
    def filter_data(self, data=None):
        if data is None:
            return
        data=np.nan_to_num(data, nan=1e-9)
        data[data==0] = 1e-9
        data[data<0] = 1e-9
        data = np.nan_to_num(data, nan=1e-9)
        logger.info(f"Filtered negative, nan and zero values.")   
        return data

    @log_info
    def update_2D_raw(self, data=None):
        """
        Updates the graph with input Data, allows to use normalization factor

        Parameters:
        data(np.array) : array with the 2D detector map
        norm_factor(float) : value that will divide the whole array

        Returns:
        None
        """
        if data is None:
            data = self._data_cache

        if data is None:
            return

        if self.tab_graph_widget.currentIndex() != INDEX_TAB_RAW_MAP:
            return

        graph_2D_widget = self.graph_raw_widget
        # print(graph_2D_widget.getDefaultColormap())

        if graph_2D_widget.getGraphXLimits() == (0, 100) and graph_2D_widget.getGraphYLimits() == (0, 100):
            reset_zoom = True
        else:
            reset_zoom = False
        logger.info(reset_zoom)

        graph_2D_widget.setKeepDataAspectRatio(True)
        graph_2D_widget.setYAxisInverted(True)

        logger.info(f"Data extracted from cache. Data: {type(data)}")

        z_lims = np_weak_lims(
            data=data,
        )
        logger.info(z_lims)

        graph_2D_widget.setLimits(
                xmin=graph_2D_widget.getGraphXLimits()[0],
                xmax=graph_2D_widget.getGraphXLimits()[1],
                ymin=graph_2D_widget.getGraphYLimits()[0],
                ymax=graph_2D_widget.getGraphYLimits()[1],
            )

        if self.checkbox_mask_integration.isChecked():
            data = self.get_masked_integration_array(data=data)

        graph_2D_widget.addImage(
            data=data,
            colormap={
                'name': 'viridis',
                'normalization': 'log',
                'autoscale': False,
                'vmin': z_lims[0],
                'vmax': z_lims[1],
            },
            resetzoom=reset_zoom,
        )
        logger.info(f"Displayed data.")


    @log_info
    def update_label_displayed(self):
        """
        Updates the upper label with the name of the displayed data

        Parameters:
        None

        Returns:
        None
        """
        # if not self.clicked_folder or not self.cache_index:
        #     return

        new_label = self.h5.get_filename_from_index(
            sample_name=self.sample_cache,
            index_list=self.cache_index,
        )

        logger.info(f"New label: {new_label}")
        self.lineedit_filename.setText(f"{new_label}")

    @log_info
    def get_map_ticks(self):
        """
        Gets the ticks from the lineedits

        Parameters:
        None

        Returns:
        None
        """
        try:
            x_ticks = le.get_clean_lineedit(
                lineedit_widget=self.lineedit_xticks
            )
        except:
            x_ticks = None
        logger.info(f"X ticks for the generated map: {x_ticks}")
        try:
            y_ticks = le.get_clean_lineedit(
                lineedit_widget=self.lineedit_yticks
            )
        except:
            y_ticks = None
        logger.info(f"Y ticks for the generated map: {y_ticks}")
        try:
            return [float(tick) for tick in x_ticks], [float(tick) for tick in y_ticks]
        except:
            return None, None

    @log_info
    def get_color_lims(self):
        try:
            color_lims = gm.get_zlims(self.graph_raw_widget)
            return color_lims
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Error at taking color limits.")

    @log_info
    def get_norm_colors(self, color_lims=[], log=False):
        try:
            if color_lims:
                if log:
                    norm = colors.LogNorm(
                        vmax=color_lims[1],
                        vmin=color_lims[0],
                    )
                else:
                    norm = colors.Normalize(
                        vmax=color_lims[1],
                        vmin=color_lims[0],
                    )
            else:
                norm = None
        except:
            norm = None
        return norm

    @log_info
    def update_graphs(
        self,
        data=None,
        norm_factor=1.0,
        graph_1D=False,
        graph_2D_raw=False,
        graph_2D_reshape=False,
        graph_2D_q=False,
        ):
        if data is None:
            data = self._data_cache
        
        if data is None:
            return

        # Update 1D integration graph
        if graph_1D:
            self.update_1D_graph(
                data=data,
                norm_factor=norm_factor,
            )

        # Update 2D Raw Map
        if graph_2D_raw:
            self.update_2D_raw(
                data=data,
            )

        # Update 2D Reshape
        if graph_2D_reshape:
            self.update_2D_reshape_map(
                data=data,
            )

        # Update 2D q map
        if graph_2D_q:
            self.update_2D_q()

    @log_info
    def update_1D_graph(self, data=None, norm_factor=1.0, clear=True):
        """
        Updates the 1D chart with intensity profiles, after pygix-pyFAI integration protocols

        Parameters:
        data (np.array) : numpy array with the 2D detector map
        norm_factor(float) : value that will divide the whole array

        Returns:
        None
        """
        graph_1D_widget = self.graph_1D_widget

        if clear:
            graph_1D_widget.clear()


        if data is None:
            data = self._data_cache

        if data is None:
            return

        if self.tab_chart_widget.currentIndex() != INDEX_TAB_1D_INTEGRATION:
            return

        # logger.info(f"Ponifile: {self.h5.get_active_ponifile()}")
        # if not self.active_ponifile:
        #     return
            
        list_integration_names = self.combobox_integration.currentData()
        logger.info(f"Dictionaries of integration: {list_integration_names}")

        list_dict_integration = [get_dict_from_name(name=name, path_integration=INTEGRATION_PATH) for name in list_integration_names]
        logger.info(f"Dictionaries of integration: {list_dict_integration}")

        list_results = self.h5.raw_integration(
            data=data,
            norm_factor=norm_factor,
            list_dict_integration=list_dict_integration,
        )

        # Save in cache in case of saving
        self.list_dict_integration_cache = list_dict_integration        
        self.list_results_cache = list_results

        logger.info(f"New integration: {len(list_results)}")

        graph_1D_widget.setLimits(
            xmin=graph_1D_widget.getGraphXLimits()[0],
            xmax=graph_1D_widget.getGraphXLimits()[1],
            ymin=graph_1D_widget.getGraphYLimits()[0],
            ymax=graph_1D_widget.getGraphYLimits()[1],
        )

        for ind, result in enumerate(list_results):
            try:          
                graph_1D_widget.addCurve(
                    x=result[0],
                    y=result[1],
                    legend=f"{ind}",
                    resetzoom=True,
                )
                graph_1D_widget.setGraphXLabel(label=list_dict_integration[ind]["Unit"]),
                graph_1D_widget.setGraphYLabel(label='Intensity (arb. units)'),
            except:
                pass

    @log_info
    def save_plot_clicked(self, _):
        if not self.h5:
            return

        if not self.list_results_cache:
            self.write_terminal_and_loggerinfo("Nothing to save. Return.")
            return

        # Save the file
        if le.text(self.lineedit_savefolder):
            folder_output = Path(le.text(self.lineedit_savefolder))

            if not folder_output.exists():
                confirm_mkdir = QMessageBox.question(self, 'MessageBox', "A new folder will be created. Go'ed?", QMessageBox.Yes | QMessageBox.No)
                if confirm_mkdir == QMessageBox.Yes:
                    folder_output.mkdir()
                else:
                    self.write_terminal_and_loggerinfo(f"The .csv file could not be saved.")
                    return                  
        else:
            confirm_save = QMessageBox.question(self, 'MessageBox', "You are going to save in the same data folder. \
                Do you want to continue? You can change it in the blank square above.", QMessageBox.Yes | QMessageBox.No)
            if confirm_save == QMessageBox.Yes:
                folder_output = self.h5._root_dir.joinpath(self.clicked_folder)
            else:
                return

        if not Path(folder_output).exists:
            self.write_terminal_and_loggerinfo(f"The .csv file could not be saved.")
            return

        name_out = Path(le.text(self.lineedit_filename)).stem

        filename_out = folder_output.joinpath(name_out)
        filename_out = f"{filename_out}.csv"

        # Merged dictionary for the header
        merge_dict = merge_dictionaries(
            list_dicts=self.list_dict_integration_cache,
        )
        logger.info("Merged dictionary")
        str_header = dict_to_str(dictionary= merge_dict)
        logger.info("String header")

        # Merged pandas dataframe
        dict_results = {}
        for dict_int, res in zip(self.list_dict_integration_cache, self.list_results_cache):
            if dict_int[KEY_INTEGRATION] == CAKE_LABEL:
                dict_results[f"{dict_int[CAKE_KEY_UNIT]}_{dict_int[CAKE_KEY_SUFFIX]}"] = res[0]
            elif dict_int[KEY_INTEGRATION] == BOX_LABEL:
                dict_results[f"{dict_int[BOX_KEY_OUTPUT_UNIT]}_{dict_int[BOX_KEY_SUFFIX]}"] = res[0]

            dict_results[f"Intensity_{dict_int[CAKE_KEY_SUFFIX]}"] = res[1]
            filename_out += f"_{dict_int[CAKE_KEY_SUFFIX]}"
        filename_out += '.csv'
        self.write_terminal_and_loggerinfo(f"Output filename for the image: {filename_out}")
        dataframe = pd.DataFrame.from_dict(dict_results, orient='index')
        dataframe = dataframe.transpose()
        logger.info("Dataframe to be exported as .csv")

        mode = 'w' if Path(filename_out).is_file() else 'a'
        with open(filename_out, mode) as f:
            f.write(f'{str_header}\n')
        dataframe.to_csv(filename_out, sep=',', mode='a', index=False, header=True)


    @log_info
    def mark_metadata_keys(self, metadata_keys=list()):
        # Click the items
        self.combobox_metadata.markItems(metadata_keys)


    @log_info
    def table_clicked(self):
        if not self.h5:
            return

        # Save the clicked index of clicked data
        self.cache_index = tm.selected_rows(self.table_files)

        if not self.cache_index:
            return

        # Update data cache
        self.update_cache_data(
            sample_name=self.sample_cache,
            list_index=self.cache_index,
        )
        # Update grazing-incidence geometry
        self.h5.update_angles(
            sample_name=self.sample_cache,
            list_index=self.cache_index,
        )

        # Update label dislayed
        self.update_label_displayed()

        # Update graphs
        self.update_graphs(
            graph_1D=True,
            graph_2D_raw=True,
            graph_2D_reshape=True,
            graph_2D_q=True,
        )

    @log_info
    def update_table(self, dataframe=None, reset=True):

        if reset:
            tm.reset(
                table=self.table_files,
            )
            logger.info("Table was reseted.")
        if dataframe is None:
            return

        # Add columns for the displayed metadata keys
        tm.insert_columns(
            table=self.table_files,
            num=len(dataframe.columns),
            labels=list(dataframe.columns),
        )
        logger.info(f"Inserted columns: {len(dataframe.columns)}")

        # Add the rows for all the displayed files
        tm.insert_rows(
            table=self.table_files,
            num=len(dataframe),
        )
        logger.info(f"Inserted rows: {len(dataframe)}")

        # Add the new key values for every file
        for ind_row, _ in enumerate(dataframe[FILENAME_KEY]):
            for ind_column, key in enumerate(dataframe):
                try:
                    tm.update_cell(
                        table=self.table_files,
                        row_ind=ind_row,
                        column_ind=ind_column,
                        st=dataframe[key][ind_row],
                    )
                    logger.info(f"Updated cell [{ind_row},{ind_column}].")
                except:
                    pass

    @log_info
    def update_clicked_filenames(self) -> None:
        """
        Updates the value of the clicked files in the table (list of files) and stores them in cache

        Parameters:
        None

        Returns:
        None
        """
        self.cache_index = tm.selected_rows(self.table_files)
        self.cache_filenames = [
            self.filename_fromrow(index) for index in self.cache_index
        ]

        logger.info(f"New cache index: {self.cache_index}")
        self.write_terminal_and_loggerinfo(f"New cache filenames: {str(self.cache_filenames)}")


    @log_info
    def get_data(
        self, 
        sample_name=str(), 
        list_index=list(), 
        normalized=True,
        ) -> np.array:

        try:
            data = self.h5.get_Edf_data(
                sample_name=sample_name,
                index_list=list_index,
                normalized=normalized,
            )
            self.write_terminal_and_loggerinfo(f"Retrieved data. Sample_name:{sample_name}, index {str(list_index)}.")
        except Exception as e:
            logger.error(f"{e}: Data could not be retrieved with sample {sample_name} and index {str(list_index)}.")
            data = None

        return data

    @log_info
    def filename_fromrow(self, row_index) -> str:
        """
        Returns the filename according to clicked index

        Parameters:
        None

        Returns:
        None
        """
        clicked_filename = tm.item(
            table=self.table_files,
            row=row_index,
            column=0
        )
        return clicked_filename

    @log_info
    def update_2D_reshape_map(self, data=None, clear=True):
        if not self.h5:
            return

        if data is None:
            data = self._data_cache
        
        if data is None:
            return

        if self.tab_graph_widget.currentIndex() != INDEX_TAB_RESHAPE_MAP:
            return

        try:
            data_reshape, q, chi = self.h5.map_reshaping(
                data=data,
            )
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: Data could not be reshaped.")
            return

        canvas = self.canvas_reshape_widget
        z_lims = gm.get_zlims(self.graph_raw_widget)

        if clear:
            canvas.axes.cla()

        canvas.axes.imshow(
            data_reshape,
            origin="lower", 
            extent=[
                q.min(),
                q.max(), 
                chi.min(), 
                chi.max()], 
            aspect="auto",
            vmin=z_lims[0],
            vmax=z_lims[1],
        )
        canvas.axes.set_xlabel("q (nm-1)")
        canvas.axes.set_ylabel("Chi (deg)")     
        canvas.draw()   

        logger.info(f"Displayed reshape data.")

    @log_info
    def mirror_scat_matrix(self, data=None, scat_horz=None):
        if data is None or scat_horz is None:
            return

        sample_orientation = DICT_SAMPLE_ORIENTATIONS[(self.state_qz, self.state_qr)]

        if sample_orientation in (1,3):
            scat_horz = np.fliplr(scat_horz) * (-1)
            data = np.fliplr(data)
        elif sample_orientation in (2,4):
            scat_horz = np.flipud(scat_horz) * (-1)
            data = np.flipud(data)
        return data, scat_horz

    @log_info
    def zoom_matrix(self, mat=None, binning=1):
        if mat is None:
            return
    
        try:
            mat = ndimage.zoom(mat, 1/binning)
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}: There was an error during data binning.")
        return mat

    @log_info
    def update_q_matrix_cache(self, new_data=True):
        """
        WORKS WITH CACHE MATRIX
        Generates a pop-up window with a 2D map of the pattern transformed to q or theta units

        Parameters:
        None

        Returns:
        None
        """
        if not self.h5:
            return

        # Get cache versions of the scattering matrix
        scat_horz = self.scat_horz_cache
        scat_vert = self.scat_vert_cache
        data_bin = self.data_bin_cache

        # Check if the matrix needs to be redone
        qz_prev = self._dict_qmap_cache['qz_parallel']
        qr_prev = self._dict_qmap_cache['qr_parallel']
        mirror_prev = self._dict_qmap_cache['mirror']
        binning_prev = self._dict_qmap_cache['binning']
        iangle_prev = self._dict_qmap_cache['incident_angle']
        tangle_prev = self._dict_qmap_cache['tilt_angle']

        qz_current = self.state_qz
        qr_current = self.state_qr
        mirror_current = self.state_mirror
        binning_current = int(self.spinbox_binnning_data.value())
        iangle_current = self.h5.get_incident_angle(
            sample_name=self.clicked_folder,
            index_list=self.cache_index,
        )
        tangle_current = self.h5.get_tilt_angle(
            sample_name=self.clicked_folder,
            index_list=self.cache_index,
        )

        # Redone the data if new_data
        if new_data:
            data_bin = None

        # Redone everything if the binning is different
        if binning_prev != binning_current:
            scat_horz, scat_vert, data_bin = None, None, None

        # Redone the scattering matrix if the sample orientation is different
        if (qz_prev != qz_current) or (qr_prev != qr_current):
            scat_horz, scat_vert = None, None

        # Redone the scattering matrix if some GI angle is different
        if (iangle_prev != iangle_current) or (tangle_prev != tangle_current):
            scat_horz, scat_vert = None, None
        
        # If data_bin is None, zoom the data again
        if data_bin is None:
            data_bin = self._data_cache
            data_bin = self.zoom_matrix(
                mat=data_bin,
                binning=binning_current,
            )

        # If scat matrix are None, generate them again and zoom
        if (scat_horz is None) or (scat_vert is None):
            # Get the unit of the generated map
            unit = cb.value(self.combobox_units)
            unit = get_pyfai_unit(unit)

            scat_horz, scat_vert = self.h5.get_mesh_matrix(
                unit=unit,
                shape=self._data_cache.shape,
            )
            scat_horz = self.zoom_matrix(
                mat=scat_horz,
                binning=binning_current,
            )
            scat_vert = self.zoom_matrix(
                mat=scat_vert,
                binning=binning_current,
            )
            
        if (scat_horz is None) or (scat_vert is None) or (data_bin is None):
            self.write_terminal_and_loggerinfo("Scattering matrix are None.")
            return
        
        # Mirror if needed
        if mirror_prev != mirror_current:
            data_bin, scat_horz = self.mirror_scat_matrix(
                data=data_bin,
                scat_horz=scat_horz,
            )

        # Update all cache vars
        self.scat_horz_cache = scat_horz
        self.scat_vert_cache = scat_vert
        self.data_bin_cache = data_bin

        self.write_terminal_and_loggerinfo(f"Updated cache matrix.")
        logger.info(f"Updated scat_horz_cache with shape {scat_horz.shape}")
        logger.info(f"Updated scat_vert_cache with shape {scat_vert.shape}")
        logger.info(f"Updated data_bin_cache with shape {data_bin.shape}")

        self._dict_qmap_cache = {
            'qz_parallel' : qz_current,
            'qr_parallel' : qr_current,
            'mirror' : mirror_current,
            'binning' : binning_current,
            'incident_angle': iangle_current,
            'tilt_angle' : tangle_current,
        }
        logger.info(f"Updated cache dictionary: {str(self._dict_qmap_cache)}")


    @log_info
    def plot_qcache_matrix(self):
        scat_horz = self.scat_horz_cache
        scat_vert = self.scat_vert_cache
        data_bin = self.data_bin_cache

        canvas = self.canvas_2d_q

        # Return if there are no matrix or the shapes do not match
        if (scat_horz is None) or (scat_vert is None) or (data_bin is None):
            self.write_terminal_and_loggerinfo("Impossible to plot.")
        
        if not (scat_horz.shape == scat_vert.shape == data_bin.shape):
            self.write_terminal_and_loggerinfo("The shape of scat matrix do not match.")
            return
        
        # Get the size of the comma
        size_comma = self._scattersize_cache

        # Get the color normalization
        color_lims = self.get_color_lims()
        log = self._graph_log
        norm = self.get_norm_colors(
            color_lims=color_lims,
            log=log,
        )

        # Initial limits
        xlim = canvas.axes.get_xlim()
        ylim = canvas.axes.get_ylim()

        # Plot the scatter
        try:
            canvas.axes.cla()
            canvas.axes.scatter(
                scat_horz,
                scat_vert,
                c=data_bin,
                s=size_comma,
                norm=norm,
                edgecolors="None",
                marker=',',
                cmap="viridis",
            )
            canvas.axes.set_aspect('equal', 'box')

            if xlim != (0.0, 1.0):
                canvas.axes.set_xlim(xlim)
            if ylim != (0.0, 1.0):
                canvas.axes.set_ylim(ylim)

            canvas.draw()
        except Exception as e:
            self.write_terminal_and_loggererror(f"{e}: Impossible to scatter scat_horz with shape {scat_horz.shape} \
                , scat_vert with shape {scat_vert.shape} and data with shape {data_bin.shape}.")
            
    @log_info
    def update_qmap_style(self):
        canvas = self.canvas_2d_q
        
        # Get the title
        title = self.get_title()

        try:
            x_ticks = self.get_xticks()
            y_ticks = self.get_yticks()
        except Exception as e:
            x_ticks = canvas.axes.get_xticks()
            y_ticks = canvas.axes.get_yticks()            
            logger.error(f"{e}: Error at taking the graph ticks.")

        # Get the limits and ticks
        try:
            x_lims = self.get_xlims()
        except Exception as e:
            logger.error(f"{e}: Error at taking the x limits.")
            x_lims = canvas.axes.get_xlim()

        try:
            y_lims = self.get_ylims()
        except Exception as e:
            logger.error(f"{e}: Error at taking the y limits.")
            y_lims = canvas.axes.get_ylim()  

        # Get the font size
        font_size = self._fontsize_cache

        # Get the labels
        unit = cb.value(self.combobox_units)
        unit = get_pyfai_unit(unit)
        DICT_PLOT = DICT_UNIT_PLOTS.get(unit, DICT_PLOT_DEFAULT)
        x_label = DICT_PLOT.get('X_LABEL', 'x')
        y_label = DICT_PLOT.get('Y_LABEL', 'y')

        canvas.axes.set_xlabel(xlabel=x_label, fontsize=font_size)
        canvas.axes.set_ylabel(ylabel=y_label, fontsize=font_size)

        # x-ticks
        try:
            canvas.axes.set_xticks(x_ticks, x_ticks, fontsize=font_size)
        except Exception as e:
            x_ticks = canvas.axes.get_xticks()
            canvas.axes.set_xticks(x_ticks, x_ticks, fontsize=font_size)
        # y-ticks
        try:
            canvas.axes.set_yticks(y_ticks, y_ticks, fontsize=font_size)
        except Exception as e:
            y_ticks = canvas.axes.get_yticks()
            canvas.axes.set_yticks(y_ticks, y_ticks, fontsize=font_size)
        # x-lims
        try:
            canvas.axes.set_xlim(x_lims)
        except Exception as e:
            x_lims = canvas.axes.get_xlim()
            canvas.axes.set_xlim(x_lims)

        # x-lims
        try:
            canvas.axes.set_ylim(y_lims)
        except Exception as e:
            y_lims = canvas.axes.get_ylim()
            canvas.axes.set_ylim(y_lims)

        canvas.axes.set_title(title, fontsize=font_size)
        canvas.draw()

    @log_info
    def plot_q_map(
        self,
        mesh_horz=None,
        mesh_vert=None, 
        data=None, 
        unit='q_nm^-1', 
        auto_lims=True, 
        title='',
        norm=None,
        clear_axes=True,
        **kwargs):

        if not self.h5:
            return

        if (mesh_horz is None) or (mesh_vert is None) or (data is None):
            self.write_terminal_and_loggerinfo("There is a None in the input matrix")
            return

        canvas = self.canvas_reshape_widget
        if clear_axes:
            canvas.axes.cla()

        if not (mesh_horz.shape == mesh_vert.shape == data.shape):
            self.write_terminal_and_loggerinfo("The shape of the mesh matrix do not match.")
            self.write_terminal_and_loggerinfo(f"Mesh_horz.shape={mesh_horz.shape}.")
            self.write_terminal_and_loggerinfo(f"Mesh_vert.shape={mesh_vert.shape}.")
            self.write_terminal_and_loggerinfo(f"Data.shape={data.shape}.")
            return
        
        # Get the units and style parameters
        DICT_PLOT = DICT_UNIT_PLOTS.get(unit, DICT_PLOT_DEFAULT)
        x_label = kwargs.get('xlabel', DICT_PLOT['X_LABEL'])
        y_label = kwargs.get('ylabel', DICT_PLOT['Y_LABEL'])

        if not auto_lims:
            x_lims = kwargs.get('xlim', DICT_PLOT['X_LIMS'])
            if x_lims == '':
                x_lims = DICT_PLOT['X_LIMS']

            y_lims = kwargs.get('ylim', DICT_PLOT['Y_LIMS'])
            if y_lims == '':
                y_lims = DICT_PLOT['Y_LIMS']

            x_ticks = kwargs.get('xticks', DICT_PLOT['X_TICKS'])
            if x_ticks == '':
                x_ticks = DICT_PLOT['X_TICKS']

            y_ticks = kwargs.get('yticks', DICT_PLOT['Y_TICKS'])
            if y_ticks == '':
                y_ticks = DICT_PLOT['Y_TICKS']

            canvas.axes.set_xlim(x_lims)
            canvas.axes.set_ylim(y_lims)
        else:
            x_ticks = canvas.axes.get_xticks()
            y_ticks = canvas.axes.get_yticks()

        # Plot the scatter
        try:
            canvas.axes.scatter(
                mesh_horz,
                mesh_vert,
                c=data,
                s=self._scattersize_cache,
                norm=norm,
                edgecolors="None",
                marker=',',
                cmap="viridis",
            )
        except Exception as e:
            self.write_terminal_and_loggerinfo(f"{e}")
        canvas.axes.set_xlabel(xlabel=x_label)
        canvas.axes.set_ylabel(ylabel=y_label)
        canvas.axes.set_xticks(x_ticks)
        canvas.axes.set_yticks(y_ticks)
        canvas.axes.set_title(title)
        canvas.draw()

    @log_info
    def increase_font_clicked(self,_):
        self._fontsize_cache += 2
        self.update_qmap_style()

    @log_info
    def reduce_font_clicked(self,_):
        self._fontsize_cache -= 2
        self.update_qmap_style()
  
    @log_info
    def increase_scattersize(self,_):
        self._scattersize_cache += 1
        self.plot_qcache_matrix()
        self.update_qmap_style()

    @log_info
    def reduce_scattersize(self,_):
        self._scattersize_cache -= 1
        self.plot_qcache_matrix()
        self.update_qmap_style()
    
    @log_info
    def ticks_changed(self,_):
        self.update_qmap_style()

    @log_info
    def log_clicked(self,_):
        self.update_graph_log()
        self.plot_qcache_matrix()
        self.update_qmap_style()

    @log_info
    def scat_units_changed(self,scat_unit):
        self.scat_horz_cache = None
        self.scat_vert_cache = None
        self.update_lims_ticks()
        self.update_graphs(
            graph_2D_q=True,
        )

    @log_info
    def binning_changed(self,_):
        self.update_graphs(
            graph_2D_q=True,
        )




    @log_info
    def checkbox_mask_clicked(self,_):
        self.update_graphs(
            graph_2D_raw=True,
        )


    @log_info
    def cb_integration_changed(self,_):
        self.update_graphs(
            graph_2D_raw=True,
            graph_1D=True,
        )

    @log_info
    def clear_plot(self,_):
        self.graph_1D_widget.clear()

    @log_info
    def get_masked_integration_array(self, data):

        list_integration_names = self.combobox_integration.currentData()

        list_dict_integration = [get_dict_from_name(name=name, path_integration=INTEGRATION_PATH) for name in list_integration_names]
        
        if not list_dict_integration:
            return data

        dict_integration = list_dict_integration[0]
        logger.info(f"Dictionary of integration to be masked: {dict_integration}")
        shape = data.shape

        # Mask for Azimuthal or Radial integration
        if dict_integration[KEY_INTEGRATION] == CAKE_LABEL:
            try:
                unit = dict_integration[CAKE_KEY_UNIT]
                dict_plot = DICT_UNIT_PLOTS.get(unit, DICT_PLOT_DEFAULT)
                p0_range = dict_integration[CAKE_KEY_RRANGE]
                p1_range = dict_integration[CAKE_KEY_ARANGE]
                pos0_scale = dict_plot['SCALE']
                p0_range = tuple([i / pos0_scale for i in p0_range])
                p1_range = tuple([np.deg2rad(i) + np.pi for i in p1_range]) 

                logger.info(f"Parameters to mask the array. Shape: {shape}, unit: {unit}, \
                    p0_range: {p0_range}, p1_range: {p1_range}, pos0_scale: {pos0_scale}.")
                chi, pos0 = self.h5.giarray_from_unit(shape, "sector", "center", unit)
            except:
                logger.error(f"Chi and pos0 matrix could not be generated. The parameters were: \
                    Shape: {shape}, unit: {unit}, p0_range: {p0_range}, p1_range: {p1_range}, pos0_scale: {pos0_scale}.")
                return

            pos0 = np.where(((pos0 > p0_range[0]) & (pos0 < p0_range[1])), pos0, 0)
            pos0 = np.where(pos0 == 0, pos0, 1.0)
            pos0 = np.where(pos0 != 0, pos0, np.nan)

            chi = np.where(((chi > p1_range[0]) & (chi < p1_range[1])), chi, 0)
            chi = np.where(chi == 0, chi, 1.0)
            chi = np.where(chi != 0, chi, np.nan)

            mask = chi * pos0
            logger.info("The mask was generated.")   

        # Mask for Box integration
        elif dict_integration[KEY_INTEGRATION] == BOX_LABEL:
            try:
                unit = dict_integration[BOX_KEY_INPUT_UNIT]
                dict_plot = DICT_UNIT_PLOTS.get(unit, DICT_PLOT_DEFAULT)
                unit_gi = UNIT_GI[unit]                
                oop_range = dict_integration[BOX_KEY_OOPRANGE]
                ip_range = dict_integration[BOX_KEY_IPRANGE]
                q_scale = dict_plot['SCALE']
                oop_range = tuple([ii / q_scale for ii in oop_range])
                ip_range = tuple([ii / q_scale for ii in ip_range])

                logger.info(f"Parameters to mask the array. Shape: {shape}, unit: {unit}, \
                    oop_range: {oop_range}, ip_range: {ip_range}, q_scale: {q_scale}.")
                horz_q, vert_q = self.h5.giarray_from_unit(shape, "opbox", "center", unit_gi)
                print(self.h5._incident_angle)
                print(666)
            except Exception as e:
                logger.error(f"{e} horz_q and vert_q matrix could not be generated with {dict_integration} and shape {shape}")
                return

            horz_q = np.where(((horz_q > ip_range[0]) & (horz_q < ip_range[1])), horz_q, 0)
            horz_q = np.where(horz_q == 0, horz_q, 1.0)
            horz_q = np.where(horz_q != 0, horz_q, np.nan)

            vert_q = np.where(((vert_q > oop_range[0]) & (vert_q < oop_range[1])), vert_q, 0)
            vert_q = np.where(vert_q == 0, vert_q, 1.0)
            vert_q = np.where(vert_q != 0, vert_q, np.nan)

            mask = horz_q * vert_q

        else:
            return
        plt.plot(mask)
        data_mask = data * mask
        logger.info("The mask was completed.")        

        return data_mask

    @log_info
    def get_title(self) -> str:
        """
        Returns a string built up from the items in the lineedit_header

        Parameters:
        None

        Returns:
        str : title for the generated 2D map
        """
        try:
            keys_title = self.combobox_headeritems_title.currentData()
            title_str = ''
            for key in keys_title:
                metadata_value = self.h5.get_metadata_value(
                    sample_name=self.sample_cache,
                    sample_relative_address=True,
                    key_metadata=key,
                    index_list=self.cache_index,
                )
                title_str += f"{key}={metadata_value}; "
        except:
            title_str = ''
        logger.info(f"Title for the generated map: {title_str}")  
        return title_str

    @log_info
    def update_graph_log(self):
        """
        Changes the colorbar norm from log-linear

        Parameters:
        None

        Returns:
        None
        """
        if self._graph_log:
            self._graph_log = False
            self.button_log.setText("LINEAR")
        else:
            self._graph_log = True
            self.button_log.setText("LOG")

    @log_info
    def update_lims_ticks(self):
        """
        Updates the values of the lineedits with lims and ticks for the graph widget

        Parameters:
        None

        Returns:
        None
        """
        dict_units = DICT_UNIT_PLOTS[cb.value(self.combobox_units)]
        le.substitute(
            lineedit=self.lineedit_xticks,
            new_text=str(dict_units['X_TICKS'])[1:-1],
        )
        le.substitute(
            lineedit=self.lineedit_yticks,
            new_text=str(dict_units['Y_TICKS'])[1:-1],
        )

    @log_info
    def get_xticks(self):
        x_ticks = le.get_clean_lineedit(
            lineedit_widget=self.lineedit_xticks,
        )
        x_ticks = [float(tick) for tick in x_ticks]
        return x_ticks

    @log_info
    def get_yticks(self):
        y_ticks = le.get_clean_lineedit(
            lineedit_widget=self.lineedit_xticks,
        )
        y_ticks = [float(tick) for tick in y_ticks]
        return y_ticks

    @log_info
    def get_xlims(self):
        x_lims = le.get_clean_lineedit(
            lineedit_widget=self.lineedit_xlims,
        )
        x_lims = [float(lim) for lim in x_lims]
        return x_lims

    @log_info
    def get_ylims(self):
        y_lims = le.get_clean_lineedit(
            lineedit_widget=self.lineedit_ylims,
        )
        y_lims = [float(lim) for lim in y_lims]
        return y_lims

    @log_info
    def save_map_clicked(self,_):
        """
        Saves the popup map into a png file

        Parameters:
        None

        Returns:
        None
        """
        # Save the file
        if le.text(self.lineedit_savefolder):
            folder_output = Path(le.text(self.lineedit_savefolder))

            if not folder_output.exists():
                confirm_mkdir = QMessageBox.question(self, 'MessageBox', "A new folder will be created. Go'ed?", QMessageBox.Yes | QMessageBox.No)
                if confirm_mkdir == QMessageBox.Yes:
                    folder_output.mkdir()
                else:
                    self.write_terminal_and_loggerinfo(f"The image could not be saved.")
                    return                  
        else:
            confirm_save = QMessageBox.question(self, 'MessageBox', "You are going to save in the same data folder. \
                Do you want to continue? You can change it in the blank square above.", QMessageBox.Yes | QMessageBox.No)
            if confirm_save == QMessageBox.Yes:
                folder_output = Path(self.clicked_folder)
            else:
                return

        if not Path(folder_output).exists:
            self.write_terminal_and_loggerinfo(f"The image could not be saved.")
            return

        filename = Path(le.text(self.lineedit_filename)).stem
        filename_out = folder_output.joinpath(f"{filename}.png")
        self.write_terminal_and_loggerinfo(f"Output filename for the image: {filename_out}")
 
        try:
            print(filename_out)
            self.canvas_2d_q.savefig(filename_out)

            # self.update_q_map(show=False)
            # plt.savefig(filename_out)
            # plt.close()
            self.write_terminal_and_loggerinfo(f"Imaged was saved.")
        except:
            self.write_terminal_and_loggerinfo(f"The image could not be saved.")
            pass

    @log_info
    def feed_integration_widgets(self):
        """
        Feeds the combobox with the dictionary of integrations

        Parameters:
        None

        Returns:
        None
        """
        list_integration_cakes, list_integration_boxes = search_integration_names()
        list_integration = list_integration_cakes + list_integration_boxes

        # Update the listwidget for CAKE integration
        lt.insert_list(
            listwidget=self.list_cakes,
            item_list=list_integration_cakes,
            reset=True,
        )

        # Update the listwidget for BOX integration
        lt.insert_list(
            listwidget=self.list_box,
            item_list=list_integration_boxes,
            reset=True,
        )

        # Update the combobox with integrations
        integrations_in_cb = set(cb.all_items(self.combobox_integration))
        new_integrations = sorted(item for item in set(list_integration).difference(integrations_in_cb))
        new_integrations = [item for item in new_integrations if item]

        self.combobox_integration.addItems(texts=new_integrations)

    @log_info
    def open_fitting_form(self):
        self._write_output("Fitting form not available for the moment.")

    @log_info
    def batch_clicked(self, _):
        """
        Apply the integration that is in the chart to all the files in selected folder and save the files
        """
        self._write_output("Batch integration not available for the moment.")
        return
        # confirm_batch = QMessageBox.question(self, 'MessageBox', "Are you sure you want to run a batch integration? It may take some minutes+", QMessageBox.Yes | QMessageBox.No)
        # if confirm_batch == QMessageBox.Yes:
        #     files_in_selected_folder = []
        #     files_in_selected_folder += self._dict_files[self.clicked_folder]

        #     # Create folder to save the files
        #     dateprefix = date_prefix()
        #     if le.text(self.lineedit_savefolder):
        #         folder_output = join(
        #             le.text(self.lineedit_savefolder),
        #             f"{basename(self.clicked_folder)}_fittings_{dateprefix}",
        #         )
        #         makedir(folder_output)
        #     else:
        #         return

        #     for file in files_in_selected_folder:

        #         edf = self.get_Edf_instance(filename=file)

        #         for df in self.integrate_data(
        #             data=edf.get_data(),
        #             norm_factor=edf.normfactor,
        #             dicts_integration=le.get_clean_list(
        #                 lineedit=self.lineedit_integrations
        #             ),
        #         ):
        #             # Dict to string
        #             str_header = dict_to_str(dictionary= edf.get_dict() | self.dict_cache)

        #             filename_out = join(
        #                 folder_output, 
        #                 edf.basename.replace('.edf', f"_{le.text(lineedit=self.lineedit_integrations).replace(',','_')}.csv",
        #                 ),
        #             )

        #             mode = 'w' if exists(filename_out) else 'a'

        #             with open(filename_out, mode) as f:
        #                 f.write(f'{str_header}\n')
        #             df.to_csv(filename_out, sep='\t', mode='a', index=False, header=True)
        # else:
        #     return