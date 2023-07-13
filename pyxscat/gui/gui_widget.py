
from . import *
from collections import defaultdict
from os.path import dirname, exists, join
from pathlib import Path

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog, QSplashScreen, QMessageBox
from PyQt5.QtGui import QPixmap

from edf import DICT_SAMPLE_ORIENTATIONS
from other.other_functions import np_weak_lims, dict_to_str, date_prefix, merge_dictionaries
from other.plots import *
from other.search_functions import makedir
from other.integrator_methods import search_integration_names, open_json, get_dict_from_name
from other.setup_methods import search_dictionaries_setup, get_empty_setup_dict, get_dict_setup_from_name, filter_dict_setup
from gui import lineedit_methods as le
from gui import combobox_methods as cb
from gui import listwidget_methods as lt
from gui import table_methods as tm
from gui import graph_methods as gm
from gui.gui_layout import GUIPyX_Widget_layout
from h5_integrator import H5Integrator

import json
import logging
import numpy as np
import subprocess
import sys
import os
import pandas as pd

MSG_SETUP_UPDATED = "New setup dictionary was updated."
MSG_SETUP_ERROR = "The setup dictionary could not be updated."
MSG_ROTATED_UPDATED = "Rotation state was updated."
MSG_QZ_DIRECTION_UPDATED = "The qz direction was updated."
MSG_QR_DIRECTION_UPDATED = "The qr direction was updated."
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


MSG_LOGGER_INIT = "Logger was initialized."
MSG_LOGGER_UPDATE_CB_SETUPS = "The combobox of setups was updated."

MSG_H5_FOUNDFILE = "Imported .hdf5 file"
MSG_H5Integrator = "HDF5 container was created."
MSG_H5Integrator_ERROR = "HDF5 container could not be created."

DESCRIPTION_HDF5 = "HDF5_XMaS_Beamline"
COMMENT_NEW_FILE = ""

JSON_FILE_H5 = SRC_PATH.joinpath("h5_files.json")

 # Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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

    def __init__(self):
        super(GUIPyX_Widget, self).__init__()

        # Splash screen
        pixmap = QPixmap(join(GUI_PATH, 'pyxscat_logo_thumb.png'))
        splash = QSplashScreen(pixmap)
        splash.show()
        splash.finish(self)

        # Initialize attributes and callbacks
        self.h5 = None
        self._h5_path = str()
        self.main_directory = Path()
        self.active_ponifile = str()
        self.clicked_folder = str()
        self._pattern = '*.edf'
        self.list_results_cache = []
        self.list_dict_integration_cache = []
        self._qz_parallel = True
        self._qr_parallel = True
        self._auto_lims = True
        self._graph_log = True
        self._colorbar = False
        self._terminal_visible = True
        self._write_output(f"Now, the qz positive axis goes with the detector axis. Pygix orientation: {DICT_SAMPLE_ORIENTATIONS[(self._qz_parallel, self._qr_parallel)]}")

        self.reset_attributes_and_widgets()
        self.init_callbacks()
        
        self.update_setup_info()
        self.update_lims_ticks()

    def write_terminal_and_logger(self, msg=str()):
        """
        Types a message in the terminal of the GUI and register the message in the logger file as INFO

        Parameters:
        msg(str) : string to be written in the logger and the output terminal

        Returns:
        None
        """
        self._write_output(msg)
        logger.info(msg)

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
        self.combobox_h5_files.currentTextChanged.connect(
            lambda : (
                self.read_h5_file(filename_h5=cb.value(self.combobox_h5_files)),
                self.update_h5(),
                self.update_widgets(),
                self.update_setup_info(),
            )
        )

        #########################
        # Setup dictionary callback
        #########################
        self.combobox_setup.currentTextChanged.connect(lambda : self.update_setup_info())
        self.combobox_angle.currentTextChanged.connect(lambda : self.update_angle_parameter())
        self.combobox_tilt_angle.currentTextChanged.connect(lambda : self.update_tiltangle_parameter())
        self.combobox_normfactor.currentTextChanged.connect(lambda : self.update_normfactor_parameter())
        self.combobox_exposure.currentTextChanged.connect(lambda : self.update_exposure_parameter())
        self.button_setup_save.clicked.connect(lambda : self.save_new_setup())
        self.button_setup.clicked.connect(lambda : self.pick_json_file())
        self.button_setup_update.clicked.connect(lambda : self.update_setup_parameter())

        #########################
        # Integration dictionary callback
        #########################
        #### CAKES #####
        ################

        self.list_cakes.clicked.connect(lambda : self.update_cake_parameters())

        self.combobox_units_cake.currentTextChanged.connect(
            lambda : (
                self.add_integration_cake(),
                self.update_graphs(),         
            )
        )

        self.combobox_units_cake.currentTextChanged.connect(
            lambda : (
                self.add_integration_cake(),
                self.update_graphs(),         
            )
        )   

        self.spinbox_azimmin_cake.valueChanged.connect(
            lambda : (
                self.add_integration_cake(),
                self.update_graphs(),         
            )
        )
        self.spinbox_azimmax_cake.valueChanged.connect(
            lambda : (
                self.add_integration_cake(),
                self.update_graphs(),         
            )
        )
        self.spinbox_radialmin_cake.valueChanged.connect(
            lambda : (
                self.add_integration_cake(),
                self.update_graphs(),         
            )
        )
        self.spinbox_radialmax_cake.valueChanged.connect(
            lambda : (
                self.add_integration_cake(),
                self.update_graphs(),         
            )
        )

        self.spinbox_radialmax_cake.valueChanged.connect(
            lambda : (
                self.add_integration_cake(),
                self.update_graphs(),         
            )
        )

        self.lineedit_azimbins_cake.textChanged.connect(
            lambda : (
                self.add_integration_cake(),
                self.update_graphs(),         
            )
        )    

        # self.spinbox_azimbins_cake.valueChanged.connect(
        #     lambda : (
        #         self.add_integration_cake(),
        #         self.update_graphs(),         
        #     )
        # )

        ################
        #### BOXES #####
        ################
        self.list_boxs.clicked.connect(lambda : self.update_box_parameters())

        self.combobox_units_box.currentTextChanged.connect(
            lambda : (
                self.add_integration_box(),
                self.update_graphs(),         
            )
        )
        self.combobox_direction_box.currentTextChanged.connect(
            lambda : (
                self.add_integration_box(),
                self.update_graphs(),         
            )
        )
        self.combobox_outputunits_box.currentTextChanged.connect(
            lambda : (
                self.add_integration_box(),
                self.update_graphs(),         
            )
        )
        self.spinbox_ipmin_box.valueChanged.connect(
            lambda : (
                self.add_integration_box(),
                self.update_graphs(),         
            )
        )
        self.spinbox_ipmax_box.valueChanged.connect(
            lambda : (
                self.add_integration_box(),
                self.update_graphs(),         
            )
        )
        self.spinbox_oopmin_box.valueChanged.connect(
            lambda : (
                self.add_integration_box(),
                self.update_graphs(),         
            )
        )
        self.spinbox_oopmax_box.valueChanged.connect(
            lambda : (
                self.add_integration_box(),
                self.update_graphs(),         
            )
        )

        #########################
        # Callbacks for rotation and parallel/antiparallel axis
        #########################
        self.button_qz.clicked.connect(
            lambda : (
                self.update_qz(),
                self.update_graphs(),
            )
        )
        self.button_qr.clicked.connect(
            lambda : (
                self.update_qr(),
                self.update_graphs(),
            )
        )

        self.button_pick_maindir.clicked.connect(
            lambda : (
                self.pick_folder(),
                self.generate_hdf5(),
                self.update_h5(),
                self.append_and_activate_h5_file(self._h5_path),
            )
        )

        self.button_pick_hdf5.clicked.connect(
            lambda : (
                self.pick_and_activate_hdf5_file(),
                self.update_h5(),
                self.update_widgets(),   
                self.update_setup_info(),             
            )
        )

        #########################
        # Extension and wildcards callback
        #########################
        self.combobox_extension.currentTextChanged.connect(
            lambda : (
                self.update_pattern(),
            )            
        )
        self.lineedit_wildcards.textChanged.connect(
            lambda : (
                self.update_pattern(),
            )   
        )

        #########################
        # Ponifile callbacks
        #########################
        self.combobox_ponifile.currentTextChanged.connect(
            lambda : (
                self.activate_ponifile(),
                self.update_graphs(),
            )
        )
        self.button_add_ponifile.clicked.connect(
            lambda : (
                self.pick_new_ponifile_and_update(),
            )
        )
        self.button_update_ponifile.clicked.connect(
            lambda : (
                self.search_and_update_ponifiles_widgets(),
            )
        )

        #####################################################################
        ##################  MAIN BUTTONS CALLBACKS  #########################
        #####################################################################

        #########################
        # Button to open pyFAI-calib2
        #########################
        self.button_pyfaicalib.clicked.connect(
            lambda : self.open_pyFAI_calib2(),
        )

        #########################
        # Button to search and update files
        #########################
        self.button_start.clicked.connect(
            lambda : (
                self.update_h5(),
                self.update_widgets(),
            )
        )

        #########################
        # Checkbox to start live data searching
        #########################
        self.checkbox_live.stateChanged.connect(
            lambda : (
                self.update_h5(),
                self.update_widgets(),
                self.update_live_searching(),
            )
        ) 

        #####################################################################
        ##################  BROWSER CALLBACKS  ##############################
        #####################################################################

        #########################
        # List_widget folder callback
        #########################
        self.listwidget_folders.clicked.connect(
            lambda : (
                self.update_clicked_folder(),
                self.update_comboboxes_metadata(),
                self.update_table(
                    reset=True,
                ),
            )
        )

        #########################
        # Combobox header items updates its lineedit
        #########################
        self.combobox_headeritems.currentTextChanged.connect(
            lambda: (
                le.insert(
                    self.lineedit_headeritems,
                    cb.value(self.combobox_headeritems)
                ),
            )  
        )

        #########################
        # Lineedit_items header updates the table of files
        #########################

        self.lineedit_headeritems.textChanged.connect(
            lambda: self.update_table(
                reset=True,
            )
        )

        # Click on the table updates the chart
        self.table_files.itemSelectionChanged.connect(
            lambda : (
                self.update_clicked_filenames(),
                self.update_graphs(),
                self.update_label_displayed(),
            )

        )

        # Combobox_integrations, updates its corresponding lineedit
        self.combobox_integration.currentTextChanged.connect(
            lambda: le.insert(
                self.lineedit_integrations,
                cb.value(self.combobox_integration)
            )
        )

        self.lineedit_integrations.textChanged.connect(
            lambda : (
                self.update_graphs(),
            )
        )

        # Masked 2D for integrations
        self.checkbox_mask_integration.stateChanged.connect(
            lambda : (
                self.update_graphs(),
            )
        ) 

        # Button clear plot clears the chart
        self.button_clearplot.clicked.connect(
            lambda: self.graph_1D_widget.clear()
        )

        # Button fitting form
        self.button_fit.clicked.connect(
            lambda: self.open_fitting_form()
        )    

        self.spinbox_sub.valueChanged.connect(
            lambda: (
                self.update_graphs(),
            )
        )

        # Button to generate a matplotlib map
        self.button_map.clicked.connect(
            lambda: (
                self.generate_q_map(),
            )
        )

        self.button_log.clicked.connect(
            lambda : self.update_graph_log(),
        )

        self.button_colorbar.clicked.connect(
            lambda : (self.update_graph_colorbar())
        )

        self.button_default_graph.clicked.connect(
            lambda : (self.update_auto_lims())
        )
        
        self.combobox_units.currentTextChanged.connect(
            lambda : (
                self.update_lims_ticks(),
            )
        )

        # Button to save the generated map
        self.button_savemap.clicked.connect(
            lambda : (self.save_popup_map())
        )

        # Button to save the dataframe in the chart
        self.button_saveplot.clicked.connect(
            lambda : (self.save_plot())
        )

        # Combobox_title, updates its lineedit
        self.combobox_headeritems_title.currentTextChanged.connect(
            lambda: le.insert(
                self.lineedit_headeritems_title,
                cb.value(self.combobox_headeritems_title)
            )
        )

        self.button_batch.clicked.connect(
            lambda : (
                self.batch_and_save(),
            ) 
        )

        self.button_hide_terminal.clicked.connect(
            self.hide_show_plaintext,
        )

    @log_info
    def reset_attributes_and_widgets(self) -> None:
        """
        Resets data attributes after changing main directory

        Parameters:
        None

        Returns:
        None
        """
        self.metadata_keys = list()
        self.clicked_folder = str()
        self.cache_index = []
        self._h5_file = str()

        # Clear GUI widgets
        cb.clear(self.combobox_ponifile)
        cb.clear(self.combobox_reffolder)
        cb.clear(self.combobox_headeritems)
        cb.clear(self.combobox_headeritems_title)
        cb.clear(self.combobox_angle)
        cb.clear(self.combobox_tilt_angle)
        cb.clear(self.combobox_exposure)
        cb.clear(self.combobox_normfactor)
        lt.clear(self.listwidget_folders)
        tm.reset(self.table_files)
        le.clear(self.lineedit_headeritems)
        le.clear(self.lineedit_headeritems_title)
        self.graph_1D_widget.clear()
        self.graph_2D_widget.clear()

        self.write_terminal_and_logger(MSG_RESET_DATA)


    # #########################
    # # Update self attributes
    # #########################
    @log_info
    def update_combobox_h5(self) -> None:
        """
        Takes the .json files with the recently open .h5 files and feeds the combobox

        Parameters:
        None

        Returns:
        None
        """
        if not JSON_FILE_H5.is_file():
            with open(JSON_FILE_H5, 'w+') as fp:
                dict_h5 = {'H5_recent_files':[""]}
                json.dump(dict_h5, fp)

        with open(JSON_FILE_H5, 'r') as fp:
            dict_h5 = json.load(fp)

        h5_in_folder = [item for item in dict_h5['H5_recent_files'] if Path(item).is_file()]
        h5_in_folder.sort()

        # Empty value to avoid automatic trigger
        h5_in_folder.insert(0, '')

        cb.insert_list(
            combobox=self.combobox_h5_files,
            list_items=h5_in_folder,
            reset=True,
        )

    @log_info
    def update_combobox_setups(self) -> None:
        """
        Take the .json files from the setup directory and feed the combobox_setups

        Parameters:
        None

        Returns:
        None
        """
        combobox_setup = self.combobox_setup
        list_dict_setups = search_dictionaries_setup(directory_setups=SETUP_PATH)
        list_name_setups = [d['Name'] for d in list_dict_setups]

        cb.insert_list(
            combobox=combobox_setup,
            list_items=list_name_setups,
            reset=True,
        )

    @log_info
    def read_dict_setup(self) -> defaultdict:
        """
        Retrieves the values for the setup dictionary from the correct lineedits and returns a defaultdict

        Parameters:
        None

        Returns:
        defaultdict: with the correct keys for setup dictionary and values read from lineedits in GUI
        """
        new_setup_dict = get_empty_setup_dict()

        list_lineedits = [
            self.lineedit_setup_name,
            self.lineedit_angle,
            self.lineedit_tilt_angle,
            self.lineedit_normfactor,
            self.lineedit_exposure,
        ]

        for key, lineedit in zip(new_setup_dict.keys(), list_lineedits):
            new_setup_dict[key] = le.text(lineedit)

        return new_setup_dict

    @log_info
    def update_setup_info(self, new_name_setup=str(), new_dict=defaultdict) -> None:
        """
        Declare the setup dictionary of the GUI searching by name (string) or declaring a new one

        Parameters:
        new_name_setup(str) : key 'Name' of the (already saved) setup dictionary in a .json file
        new_dict(defaultdict) : contains the new values for the setup dictionary

        Returns:
        None
        """
        if not new_name_setup:
            new_name_setup = cb.value(self.combobox_setup)

        # Search for a .json file with the name_setup string
        if new_name_setup:
            new_dict_setup = get_dict_setup_from_name(
                name=new_name_setup,
                directory_setups=SETUP_PATH,
            )
        # Directly update with a defaultdict  
        elif new_dict:
            new_dict_setup = new_dict
        else:
            new_dict_setup = get_empty_setup_dict()

        new_dict_setup = filter_dict_setup(
            dictionary=new_dict_setup,
        )

        # Updates the instance variable
        self._dict_setup = new_dict_setup

        self.write_terminal_and_logger(MSG_SETUP_UPDATED)
        self.write_terminal_and_logger(self._dict_setup)

        # Fill the lineedits
        le.substitute(self.lineedit_setup_name, self._dict_setup['Name'])
        le.substitute(self.lineedit_angle, self._dict_setup['Angle'])
        le.substitute(self.lineedit_tilt_angle, self._dict_setup['Tilt angle'])
        le.substitute(self.lineedit_normfactor, self._dict_setup['Norm'])
        le.substitute(self.lineedit_exposure, self._dict_setup['Exposure'])

        # Reset and fill the lineedits of items
        le.clear(self.lineedit_headeritems)
        le.insert(self.lineedit_headeritems,self._dict_setup['Angle'])
        le.insert(self.lineedit_headeritems,self._dict_setup['Tilt angle'])
        le.insert(self.lineedit_headeritems,self._dict_setup['Norm'])
        le.insert(self.lineedit_headeritems,self._dict_setup['Exposure'])

    @log_info
    def update_angle_parameter(self, text=str()) -> None:
        """
            Update the incident angle parameter
        """
        if text:
            le.substitute(self.lineedit_angle, text)

    @log_info
    def update_tiltangle_parameter(self, text=str()) -> None:
        """
            Update the tilt angle parameter
        """
        if text:
            le.substitute(self.lineedit_tilt_angle, text)

    @log_info
    def update_normfactor_parameter(self, text=str()) -> None:
        """
            Update the normalization factor parameter
        """
        if text:
            le.substitute(self.lineedit_normfactor, text)

    @log_info
    def update_exposure_parameter(self, text=str()) -> None:
        """
            Update the exposition time parameter
        """
        if text:
            le.substitute(self.lineedit_exposure, text)

    @log_info
    def update_setup_parameter(self) -> None:
        """
            Update the dictionary of setup information from changing the lineedits
        """
        new_dict_info = self.read_dict_setup()
        for key, value in new_dict_info.items():
            if self._dict_setup[key] != value:
                self._dict_setup[key] = value
                self.write_terminal_and_logger(MSG_SETUP_UPDATED)
                self.write_terminal_and_logger(self._dict_setup)
        if self.h5:
            self.h5.update_setup_keys(
                dict_keys=self._dict_setup,
            )

    @log_info
    def save_new_setup(self) -> None:
        """
            Collect the dictionary and save a .json file
        """
        new_dict_info = self.read_dict_setup()
        file_json = join(SETUP_PATH, f"{new_dict_info['Name']}.json")
        with open(file_json, 'w+') as fp:
            json.dump(new_dict_info, fp)
        self.update_combobox_setups()

    @log_info
    def pick_json_file(self) -> None:
        """
            Open a browser to pick a .json file with setup information
        """
        if self.main_directory:
            json_file = QFileDialog.getOpenFileNames(self, 'Pick .json file', str(self.main_directory), "*.json")
        else:
            json_file = QFileDialog.getOpenFileNames(self, 'Pick .json file', '.', "*.json")

        if json_file:
            try:
                json_file = json_file[0][0]
                with open(json_file) as jf:
                    new_dict_setup = json.load(jf)
                self.update_setup_info(new_dict=new_dict_setup)
            except:
                pass
        else:
            return

    @log_info
    def update_cake_parameters(self):
        """
        Updates the widgets of integration after clicking on the list_cakes
        """
        clicked_integration = lt.click_values(self.list_cakes)[0]
        json_file = INTEGRATION_PATH.joinpath(f"{clicked_integration}.json")
        logger.info(f"Json file: {json_file}")
        dict_cake = open_json(json_file)
        le.substitute(self.lineedit_name_cake, dict_cake["Name"])
        le.substitute(self.lineedit_suffix_cake, dict_cake["Suffix"])
        cb.set_text(self.combobox_type_cake, dict_cake["Type"])
        self.spinbox_radialmin_cake.setValue(dict_cake["Radial_range"][0])
        self.spinbox_radialmax_cake.setValue(dict_cake["Radial_range"][1])
        self.spinbox_azimmin_cake.setValue(dict_cake["Azimuth_range"][0])
        self.spinbox_azimmax_cake.setValue(dict_cake["Azimuth_range"][1])
        cb.set_text(self.combobox_units_cake, dict_cake["Unit"])
        le.substitute(self.lineedit_azimbins_cake, dict_cake["Bins_azimut"])
        # self.spinbox_azimbins_cake.setValue(dict_cake["Bins_azimut"])
        logger.info(f"Updated widgets with cake integration values.")

    @log_info
    def update_box_parameters(self):
        """
        Updates the widgets of integration after clicking on the list_boxes
        """
        clicked_integration = lt.click_values(self.list_boxs)[0]
        json_file = INTEGRATION_PATH.joinpath(f"{clicked_integration}.json")
        logger.info(f"Json file: {json_file}")
        dict_box = open_json(json_file)
        le.substitute(self.lineedit_name_box, dict_box["Name"])
        le.substitute(self.lineedit_suffix_box, dict_box["Suffix"])
        cb.set_text(self.combobox_direction_box, dict_box["Type"])
        cb.set_text(self.combobox_units_box, dict_box["Unit_input"])
        self.spinbox_ipmin_box.setValue(dict_box["Ip_range"][0])
        self.spinbox_ipmax_box.setValue(dict_box["Ip_range"][1])
        self.spinbox_oopmin_box.setValue(dict_box["Oop_range"][0])
        self.spinbox_oopmax_box.setValue(dict_box["Oop_range"][1])

        cb.set_text(self.combobox_outputunits_box, dict_box["Unit"])
        logger.info(f"Updated widgets with box integration values.")

    @log_info
    def add_integration_cake(self):
        """
        Takes the parameters and save the CAKE integration as a .json file
        """
        compiled_dict = dict()
        name = le.text(self.lineedit_name_cake)
        if not name:
            return

        compiled_dict["Name"] = name
        compiled_dict["Suffix"] = le.text(self.lineedit_suffix_cake)
        compiled_dict["Type"] = cb.value(self.combobox_type_cake)
        rad_min = self.spinbox_radialmin_cake.value()
        rad_max = self.spinbox_radialmax_cake.value()
        compiled_dict["Radial_range"] = [rad_min, rad_max]
        az_min = self.spinbox_azimmin_cake.value()
        az_max = self.spinbox_azimmax_cake.value()
        compiled_dict["Azimuth_range"] = [az_min, az_max]
        compiled_dict["Unit"] = cb.value(self.combobox_units_cake)
        az_max = le.text(self.lineedit_azimbins_cake)
        # az_max = int(self.spinbox_azimbins_cake.value())
        compiled_dict["Bins_azimut"] = az_max
        # compiled_dict["Bins_azimut"] = le.text(self.lineedit_azimbins_cake)

        json_file = INTEGRATION_PATH.joinpath(f"{compiled_dict['Name']}.json")
        with open(json_file, 'w+') as fp:
            json.dump(compiled_dict, fp)
        self.update_integration_widgets()

    @log_info
    def add_integration_box(self):
        """
        Takes the parameters and save the BOX integration as a .json file
        """
        compiled_dict = dict()
        name = le.text(self.lineedit_name_box)
        if not name:
            return

        compiled_dict["Name"] = name
        compiled_dict["Suffix"] = le.text(self.lineedit_suffix_box)
        compiled_dict["Type"] = cb.value(self.combobox_direction_box)
        ip_min = self.spinbox_ipmin_box.value()
        ip_max = self.spinbox_ipmax_box.value()
        compiled_dict["Ip_range"] = [ip_min, ip_max]
        oop_min = self.spinbox_oopmin_box.value()
        oop_max = self.spinbox_oopmax_box.value()
        compiled_dict["Oop_range"] = [oop_min, oop_max]
        compiled_dict["Unit"] = cb.value(self.combobox_outputunits_box)
        compiled_dict["Unit_input"] = cb.value(self.combobox_units_box)

        json_file = INTEGRATION_PATH.joinpath(f"{compiled_dict['Name']}.json")
        with open(json_file, 'w+') as fp:
            json.dump(compiled_dict, fp)
        self.update_integration_widgets()

    @log_info
    def update_qz(self) -> None:
        """
            Update the state of qz (parallel or antiparallel to PONI)
        """
        if self._qz_parallel:
            self._qz_parallel = False
            self.button_qz.setText("qz \u2191\u2193")
            self._write_output(MSG_QZ_DIRECTION_UPDATED)
            self._write_output(f"Now, the qz negative axis goes with the detector axis. Pygix orientation: {DICT_SAMPLE_ORIENTATIONS[(self._qz_parallel, self._qr_parallel)]}")
        else:
            self._qz_parallel = True
            self.button_qz.setText("qz \u2191\u2191")
            self._write_output(MSG_QZ_DIRECTION_UPDATED)
            self._write_output(f"Now, the qz positive axis goes with the detector axis. Pygix orientation: {DICT_SAMPLE_ORIENTATIONS[(self._qz_parallel, self._qr_parallel)]}")

        if self.h5:
            self.h5.update_orientation(
                qz_parallel=self._qz_parallel,
                qr_parallel=self._qr_parallel,
            )

    @log_info
    def update_qr(self) -> None:
        """
            Update the state of qr (parallel or antiparallel to PONI)
        """
        if self._qr_parallel:
            self._qr_parallel = False       
            self.button_qr.setText("qr \u2191\u2193")
            self._write_output(MSG_QR_DIRECTION_UPDATED)
            self._write_output(f"Now, the qr negative axis goes with the detector axis. Pygix orientation: {DICT_SAMPLE_ORIENTATIONS[(self._qz_parallel, self._qr_parallel)]}")
        else:
            self._qr_parallel = True            
            self.button_qr.setText("qr \u2191\u2191")
            self._write_output(MSG_QR_DIRECTION_UPDATED)
            self._write_output(f"Now, the qr positiveS axis goes with the detector axis. Pygix orientation: {DICT_SAMPLE_ORIENTATIONS[(self._qz_parallel, self._qr_parallel)]}")        
        
        if self.h5:
            self.h5.update_orientation(
                qz_parallel=self._qz_parallel,
                qr_parallel=self._qr_parallel,
            )

    @log_info
    def generate_hdf5(self):
        """
        Creates an .h5 file as a container of the data within the directory

        Parameters:
        directory (str, Path) : path of the root directory where all the data/metadata will be located recursively

        Return:
        None
        """
        if not self.main_directory:
            return

        choice_hdf5 = QMessageBox.question(self, 'MessageBox', "An .h5 file will be created. Do you want to save it in the same directory?", QMessageBox.Yes | QMessageBox.No)
        
        if choice_hdf5 == QMessageBox.Yes:
            h5_dir = self.main_directory
        else:
            h5_dir = self.pick_hdf5_folder()

        h5_filename = h5_dir.joinpath(f"{self.main_directory.name}.h5")
        self._h5_path = h5_filename

        if Path(h5_filename).is_file():
            choice_hdf5_overwrite = QMessageBox.question(self, 'MessageBox', "There is an h5 file with the same name. Do you want to overwite it?", QMessageBox.Yes | QMessageBox.No)
            if choice_hdf5_overwrite == QMessageBox.Yes:
                overwrite = True
            else:
                overwrite = False
                h5_filename = h5_dir.joinpath(f"{self.main_directory.name}_{date_prefix()}.h5")
        else:
            overwrite = True

        if self.main_directory or self.h5:
            self.reset_attributes_and_widgets()

        self.h5 = H5Integrator(
            filename_h5=h5_filename,
            main_directory=str(self.main_directory),
            setup_keys_metadata=self._dict_setup,
            qz_parallel=self._qz_parallel,
            qr_parallel=self._qr_parallel,
            overwrite=overwrite,
        )
        
        logger.info(f"h5 instance created. Filename: {h5_filename}. Ponifile: {self.active_ponifile}. Keys_metadata: {self._dict_setup}. qz:{self._qz_parallel}, qr:{self._qr_parallel}")

    @log_info
    def pick_folder(self) -> None:
        """
            Pick a folder as main directory
        """
        main_dir = Path(QFileDialog.getExistingDirectory(self, 'Choose main directory', "."))
        if main_dir and (main_dir != Path(".")):
            if Path(main_dir).exists():
                if self.main_directory or self.h5:
                    self.reset_attributes_and_widgets()

                self.main_directory = Path(main_dir)
                self.label_maindir.setText('Main directory:')
                # self.lineedit_maindir.setText(str(self.main_directory))
                self.write_terminal_and_logger(MSG_MAIN_DIRECTORY)
                self.write_terminal_and_logger(f"New main directory: {str(self.main_directory)}")              
        else:
            self.main_directory = ''
            self.write_terminal_and_logger(MSG_MAIN_DIRECTORY_ERROR)

    @log_info
    def pick_hdf5_folder(self) -> None:
        """
        Picks a folder to save the .h5 file

        Parameters:
        None

        Returns:
        None
        """
        h5_dir = Path(QFileDialog.getExistingDirectory(self, 'Choose main directory', "."))
        if h5_dir and (h5_dir != Path(".")):
            return h5_dir
        else:
            return ''

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
            h5_file = h5_file[0][0]

            self.append_h5_file(
                h5_file=h5_file,
            )

            cb.set_text(
                combobox=self.combobox_h5_files,
                text=h5_file,
            )







        #     if self.main_directory or self.h5:
        #         self.reset_attributes_and_widgets()
        #     try:
        #         self._h5_file = 
        #         self.h5 = H5Integrator(
        #             filename_h5=self._h5_file,
        #             setup_keys_metadata=self._dict_setup,
        #             qz_parallel=self._qz_parallel,
        #             qr_parallel=self._qr_parallel,
        #         )
        #         self.main_directory = self.h5.get_main_directory()

        #         self.label_maindir.setText('H5 file:')

        #         self.write_terminal_and_logger(MSG_H5_FOUNDFILE)
        #         self.write_terminal_and_logger(self._h5_file)                
        #         self.write_terminal_and_logger(MSG_H5Integrator)
        #     except:
        #         self.write_terminal_and_logger(MSG_H5Integrator_ERROR)
        #         pass
        # else:
        #     return

    @log_info
    def read_h5_file(self, filename_h5=str()):
        if not Path(filename_h5).is_file():
            return

        if self.main_directory or self.h5:
            self.reset_attributes_and_widgets()
        
        self._h5_file = str(filename_h5)
        try:
            self.h5 = H5Integrator(
                filename_h5=self._h5_file,
                setup_keys_metadata=self._dict_setup,
                qz_parallel=self._qz_parallel,
                qr_parallel=self._qr_parallel,
            )
            self.main_directory = self.h5.get_main_directory()
            self.label_maindir.setText('H5 file:')

            self.write_terminal_and_logger(MSG_H5_FOUNDFILE)
            self.write_terminal_and_logger(self._h5_file)                
            self.write_terminal_and_logger(MSG_H5Integrator)
        except:
            self.write_terminal_and_logger(MSG_H5Integrator_ERROR)
            pass


    ##################################################
    ############# PONIFILE METHODS ###################
    ##################################################

    @log_info
    def search_and_update_ponifiles_widgets(self) -> None:
        """
        Runs the search engine in the .h5 file for ponifiles and updates the widgets if needed

        Parameters:
        None

        Returns:
        None
        """
        # Get the new ponifiles
        if self.h5:
            # Search and update the h5
            self.h5.search_and_update_ponifiles(return_list=False)

            ponifiles_in_cb = set(cb.all_items(self.combobox_ponifile))
            ponifiles_in_h5 = set(self.h5.generator_stored_ponifiles())

            new_ponifiles = [item for item in ponifiles_in_h5.difference(ponifiles_in_cb)]
            if new_ponifiles:
                new_ponifiles = [item for item in new_ponifiles if item]
                # Update combobox of ponifiles
                cb.insert_list(
                    combobox=self.combobox_ponifile,
                    list_items=new_ponifiles,
                    reset=False,
                )
                self.write_terminal_and_logger(f"Combobox of ponifiles was updated.")                
        else:
            self.write_terminal_and_logger("No .h5 file to store files.")

    @log_info
    def pick_new_ponifile_and_update(self) -> None:
        """
        Picks a new ponifile and updates combobox and h5 file

        Parameters:
        None

        Returns:
        None
        """
        if self.main_directory:
            ponifile_path = QFileDialog.getOpenFileNames(self, 'Pick .poni file', str(self.main_directory), "*.poni")
        else:
            ponifile_path = QFileDialog.getOpenFileNames(self, 'Pick .poni file', '.', "*.poni")
        try:
            ponifile_path = ponifile_path[0][0]

            if self.h5:
                self.h5.update_folder_from_files(
                    folder_name='Ponifiles',
                    filename_list=[ponifile_path],
                )
                cb.insert_list(
                    combobox=self.combobox_ponifile,
                    list_items=[ponifile_path],
                    reset=False,
                )
                self.write_terminal_and_logger(f"Combobox of ponifiles was updated.")
                self.write_terminal_and_logger("Picked ponifile was updated.")
                self.write_terminal_and_logger(ponifile_path)
        except:
            self.write_terminal_and_logger("Picked ponifile was not updated.")
            pass

    @log_info
    def activate_ponifile(self) -> None:
        """
        Activates the ponifile from the combobox

        Parameters:
        ponifile_path(str) : string with the full path of the poni file

        Returns:
        None
        """
        self.active_ponifile = cb.value(
            self.combobox_ponifile,
        )
        if self.h5:
            try:
                self.h5.activate_ponifile(
                    ponifile=self.active_ponifile,
                )
                self.write_terminal_and_logger(MSG_PONIFILE_UPDATED)
            except:
                self.write_terminal_and_logger(MSG_PONIFILE_ERROR)
        else:
            self.write_terminal_and_logger(MSG_PONIFILE_ERROR)

    @log_info
    def update_pattern(self) -> None:
        """
        Updates the pattern to search files

        Parameters:
        None

        Returns:
        None
        """
        wildcards = le.text(self.lineedit_wildcards).strip()
        extension = cb.value(self.combobox_extension)
        pattern = wildcards + extension
        pattern = pattern.replace('**', '*')
        self._pattern = pattern
        self.write_terminal_and_logger(MSG_PATTERN_UPDATED)
        self.write_terminal_and_logger(f"New pattern: {self._pattern}")

    @log_info
    def open_pyFAI_calib2(self) -> None:
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
        if self.main_directory and exists(self.main_directory):
            try:
                subprocess.run([join(GLOBAL_PATH, 'bash_files', 'open_calib2.sh'), self.main_directory])
            except:
                pass
        else:
            try:
                subprocess.run([join(GLOBAL_PATH, 'bash_files', 'open_calib2.sh'), os.getcwd()])
            except:
                pass

    @log_info
    def open_pyFAI_calib2_windows(self) -> None:
        """
            If the OS is Windows, open pyFAI-calib2 GUI
        """
        if self.main_directory and exists(self.main_directory):
            try:
                os.system(f"cd {self.main_directory}")
                import pyFAI                
                calib_path = join(
                    dirname(pyFAI.__file__),
                    'app',
                    'calib2.py',
                )
                cmd = f"{sys.executable} {calib_path}"
                os.system(cmd)
            except:
                pass
        else:
            try:
                os.system(f"cd {os.getcwd()}")
                import pyFAI                
                calib_path = join(
                    dirname(pyFAI.__file__),
                    'app',
                    'calib2.py',
                )
                cmd = f"{sys.executable} {calib_path}"
                os.system(cmd)
            except:
                pass
           
    # #########################
    # # Search engines
    # #########################

    def search_live_update_h5_and_widgets(self) -> None:
        """
        Run a bash script to find fresh files, and if there are new, updates the h5 and the widgets
        
        Parameters:
        None

        Returns:
        None
        """
        list_files_1s = []
        cmd = f"find {str(self.main_directory)} -name {self._pattern} -newermt '-1 seconds'"
        try:
            list_files_1s = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True).stdout.decode().strip().split('\n')
            # Clean empty items
            list_files_1s = [item for item in list_files_1s if item]
        except:
            logger.info(f"Error while running the bash script.")

        if list_files_1s:
            logger.info(f"Found new files LIVE: {list_files_1s}")
            self.h5.update_new_files(
                new_files=list_files_1s,
            )
            self.update_widgets()
            self.update_widgets_to_last_file(
                last_file=list_files_1s,
            )
        else:
            return

    @log_info
    def update_h5(self) -> None:
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
            self.h5.search_and_update_new_files(
                pattern=self._pattern,
            )
            self.write_terminal_and_logger(f"The H5 was updated. Not the Widgets yet.")

        else:
            self.write_terminal_and_logger(f"The H5 could not be updated.")



    @log_info
    def append_h5_file(self, h5_file=str()):
        """
        
        """
        h5_file = str(h5_file)
        if not JSON_FILE_H5.is_file():
            with open(JSON_FILE_H5, 'w+') as fp:
                dict_h5 = {'H5_recent_files':[""]}
                json.dump(dict_h5, fp)

        with open(JSON_FILE_H5, 'r') as fp:
            dict_h5 = json.load(fp)

        list_h5_files = dict_h5['H5_recent_files']
        list_h5_files.append(h5_file)
        list_h5_files = sorted(set(list_h5_files))
        dict_h5 = {'H5_recent_files':list_h5_files}

        with open(JSON_FILE_H5, 'w+') as fp:        
            json.dump(dict_h5, fp)

        self.update_combobox_h5()
            

    @log_info
    def append_and_activate_h5_file(self, h5_file=str()):
        """
        
        """
        h5_file = str(h5_file)

        if h5_file:
            self.append_h5_file(
                h5_file=h5_file,
            )

            cb.set_text(
                combobox=self.combobox_h5_files,
                text=h5_file,
            )

    @log_info
    def update_widgets(self) -> None:
        """
        To be used after updating the .h5 file
        This method may update the list_widget of folders and the table_widget with files and metadata
        """
        if self.h5:

            # Check if new folders to update the list_widget and reference folder combobox
            folders_in_list = set(lt.all_items(self.listwidget_folders))
            folders_in_h5 = set(self.h5.generator_folder_name())
            new_folders = [item for item in folders_in_h5.difference(folders_in_list)]
            new_folders.sort()

            if new_folders:

                # List widget
                lt.insert_list(
                    listwidget=self.listwidget_folders,
                    item_list=new_folders,
                    reset=False,
                )
                logger.info("Updated list widget.")

                # Reference combobox
                cb.insert_list(
                    combobox=self.combobox_reffolder,
                    list_items=new_folders,
                    reset=False,
                )
            else:
                logger.info("No new folders.")

            # Check if the table (click_folder) should be updated
            if not self.clicked_folder:
                return

            num_files_in_table = tm.get_row_count(self.table_files)
            num_files_in_h5 = self.h5.number_files_in_sample(self.clicked_folder)
            logger.info(f"There are {num_files_in_table} files in the table and {num_files_in_h5} files in the .h5")
            if num_files_in_h5 != num_files_in_table:
                self.update_comboboxes_metadata()
                self.update_table(
                    reset=True,
                )
            else:
                logger.info("The table was not updated.")
        else:
            self.write_terminal_and_logger("Nothing to be updated.")

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
            last_file_folder, last_file_index = self.h5.get_folder_index_from_filename(
                filename=last_file,
            )
            if last_file_folder and last_file_index:
                self.clicked_folder = last_file_folder
                self.cache_index = last_file_index
                logger.info(f"Updated clicked folder: {self.clicked_folder} and cache index: {self.cache_index}")
                self.update_graphs()
            else:
                logger.info("Last file was not updated.")
            
    @log_info
    def update_live_searching(self):
       # # If live is on, start the live searching engine, only for Linux
        if 'linux' in sys.platform:
            if self.checkbox_live.isChecked():
                self.timer_data = QTimer()

                # Get last file and update
                self.update_widgets_to_last_file()

                # Start the loop each second
                self.timer_data.timeout.connect(
                    lambda: (
                        self.search_live_update_h5_and_widgets(),
                    )
                )
                self.timer_data.start(INTERVAL_SEARCH_DATA)
                self.write_terminal_and_logger("LIVE ON: Now, the script is looking for new files...")
            else:
                self.timer_data.stop()
                self.write_terminal_and_logger("LIVE: OFF. The script stopped looking for new files.")
        else:
            self.write_terminal_and_logger("The operating system is not compatible with live searching.")

    @log_info
    def search_live_files(self) -> list:
        """
            Run bash script to find newly created files
        """
        try:
            list_files_1s = subprocess.run([join(GUI_PATH, 'bash_files', BASH_FILE_1S), self.main_directory, f"{self._wildcards}{self._extension}"],
                                    stdout=subprocess.PIPE).stdout.decode().strip().split('\n')
            # Clean empty items
            list_files_1s = [item for item in list_files_1s if item]
            new_files = list(set(list_files_1s).difference(self.set_files))

        except:
            new_files = list()
            self.timer_data.stop()
            self._write_output(MSG_ERROR_BASH)
            self._write_output("LIVE OFF. The script now is static.")

        if new_files:
            return new_files
        else:
            pass   

    # #########################
    # # Updating widgets
    # #########################

    @log_info
    def update_widgets_from_h5(self):
        """
        Updates some widgets and attributes taken from the .h5 file, instead of searching in main directory

        Parameters:
        None

        Returns:
        None
        """
        if self.h5:
            # Update the main directory, files and folder attributes
            self.main_directory = self.h5.get_main_directory()
            # self.lineedit_maindir.setText(str(self.main_directory))
            self.write_terminal_and_logger(MSG_MAIN_DIRECTORY)
            self.write_terminal_and_logger(f"New main directory: {str(self.main_directory)}")

            # Update file and folder attributes
            self.list_folders = list(self.h5.generator_folder_name())
            self.write_terminal_and_logger(f"Added {len(self.list_folders)} folders.")

            # Feed the ponifile combobox
            cb.insert_list(
                combobox=self.combobox_ponifile,
                list_items=self.h5.get_ponifile_list(),
                reset=True,
            )

            # Reset and fill the list widget with folders
            lt.insert_list(
                listwidget=self.listwidget_folders,
                item_list=list(self.h5.generator_folder_name()),
                reset=True,
            )

            # Feed the combobox of reference folder
            cb.insert_list(
                combobox=self.combobox_reffolder,
                list_items=list(self.h5.generator_folder_name()),
            )

    @log_info
    def update_clicked_folder(self) -> None:
        """
        Updates the value of the clicked folder and checks it in the H5 container

        Parameters:
        None

        Returns:
        None
        """
        # Take the folder from the clicked value
        folder_name = lt.click_values(self.listwidget_folders)[0]
        logger.info(f"Clicked folder: {folder_name}")

        if self.h5.contains_group(folder_name):
            if folder_name == self.clicked_folder:
                self.write_terminal_and_logger(F"Clicked folder, same as before: {folder_name}")
            else:
                self.write_terminal_and_logger(F"New clicked folder: {folder_name}")
                self.clicked_folder = folder_name
        else:
            self.write_terminal_and_logger(MSG_CLICKED_FLODER_ERROR)

    @log_info
    def update_comboboxes_metadata(self) -> None:
        """
        Feeds the comboboxes with the same metadata, stored in the clicked folder
        
        Parameters:
        None

        Returns:
        None
        """
        # Update the combobox with metadata keys
        metadata_keys = list(
            self.h5.generator_keys_in_folder(
                folder_name=self.clicked_folder,
            )
        )
        logger.info(f"Metadata keys: {metadata_keys}")

        # Is there are not different keys, do not change anything
        if metadata_keys == self.metadata_keys:
            return
        else:
            new_keys = sorted(set(metadata_keys).difference(set(self.metadata_keys)))
            logger.info(f"New metadata keys: {new_keys}")
            self.metadata_keys += new_keys
            self.metadata_keys.sort()
        
        # Combobox for table columns
        cb.insert_list(
            combobox=self.combobox_headeritems,
            list_items=new_keys,
            reset=True,
        )
        logger.info(f"Combobox header_items updated.")

        # Combobox for title
        cb.insert_list(
            combobox=self.combobox_headeritems_title,
            list_items=new_keys,
            reset=True,
        )
        logger.info(f"Combobox header_items title updated.")

        # Combobox for dict_setup keys
        cb.insert_list(
            combobox=self.combobox_angle,
            list_items=new_keys,
            reset=True,
        )
        logger.info(f"Combobox angle updated.")

        cb.insert_list(
            combobox=self.combobox_tilt_angle,
            list_items=new_keys,
            reset=True,
        )
        logger.info(f"Combobox tilt angle updated.")

        cb.insert_list(
            combobox=self.combobox_normfactor,
            list_items=new_keys,
            reset=True,
        )
        logger.info(f"Combobox norm updated.")

        cb.insert_list(
            combobox=self.combobox_exposure,
            list_items=new_keys,
            reset=True,
        )
        logger.info(f"Combobox exposure updated.")

    @log_info
    def update_graphs(self) -> None:
        """
        Updates both 2D and 1D graphs after the stored folder and index values in cache

        Parameters:
        None

        Returns:
        None
        """
        if not self.clicked_folder or not self.cache_index:
            return 

        # Get the data, subtracted if it is asked
        if (self.spinbox_sub.value() != 0.0):
            reference_folder = cb.value(self.combobox_reffolder)
            reference_factor = self.spinbox_sub.value()
            logger.info(f"New reference factor: {reference_factor}")
        else:
            reference_folder = ''
            reference_factor = 0.0

        # Get the data
        data = self.h5.get_Edf_data(
            folder_name=self.clicked_folder,
            index_list=self.cache_index,
            folder_reference_name=reference_folder,
            reference_factor=reference_factor,
        )

        # Get the normalization factor
        norm_factor = self.h5.get_norm_factor(
            folder_name=self.clicked_folder,
            index_list=self.cache_index,
        )
        
        # Update 2D graph
        try:
            self.update_2D_graph(
                data=data,
                norm_factor=norm_factor,
            )
        except:
            self.write_terminal_and_logger("Error during updating 2D graph")

        try:
            self.update_1D_graph(
                data=data,
                norm_factor=norm_factor,
            )
        except:
            self.write_terminal_and_logger("Error during updating 1D graph")


    @log_info
    def update_2D_graph(self, data, norm_factor=1.0):
        """
        Updates the graph with input Data, allows to use normalization factor

        Parameters:
        data(np.array) : array with the 2D detector map
        norm_factor(float) : value that will divide the whole array

        Returns:
        None
        """
        graph_2D_widget = self.graph_2D_widget
        # print(graph_2D_widget.getDefaultColormap())

        if graph_2D_widget.getGraphXLimits() == (0, 100) and graph_2D_widget.getGraphYLimits() == (0, 100):
            reset_zoom = True
        else:
            reset_zoom = False
        logger.info(reset_zoom)

        graph_2D_widget.setKeepDataAspectRatio(True)
        graph_2D_widget.setYAxisInverted(True)

        logger.info(f"Data extracted from cache. Data: {type(data)}")

        # Normalize data
        data = data/norm_factor

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

        data=np.nan_to_num(data, nan=1e-9)
        data[data==0] = 1e-9
        data[data<0] = 1e-9
        logger.info(f"Filtered negative, nan and zero values.")

        if self.checkbox_mask_integration.isChecked():
            data = self.get_masked_integration_array(data=data)

        graph_2D_widget.addImage(
            data=np.nan_to_num(data, nan=1e-9),
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
        if not self.clicked_folder or not self.cache_index:
            return
        new_label = self.h5.get_filename_from_index(
            folder_name=self.clicked_folder,
            index_list=self.cache_index,
        )
        logger.info(f"New label: {new_label}")
        self.lineedit_filename.setText(f"{new_label}")

    @log_info
    def get_map_limits(self):
        """
        Gets the limit values from the lineedits

        Parameters:
        None

        Returns:
        None
        """
        try:
            x_lims = [le.text(lineedit=self.lineedit_xmin), le.text(lineedit=self.lineedit_xmax)]
        except:
            x_lims = None
        logger.info(f"X limits for the generated map: {x_lims}")
        try:
            y_lims = [le.text(lineedit=self.lineedit_ymin), le.text(lineedit=self.lineedit_ymax)]
        except:
            y_lims = None
        logger.info(f"Y limits for the generated map: {y_lims}")
        return x_lims, y_lims

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
    def update_1D_graph(self, data=None, norm_factor=1.0):
        """
        Updates the 1D chart with intensity profiles, after pygix-pyFAI integration protocols

        Parameters:
        data (np.array) : numpy array with the 2D detector map
        norm_factor(float) : value that will divide the whole array

        Returns:
        None
        """
        graph_1D_widget = self.graph_1D_widget

        logger.info(f"Ponifile: {self.active_ponifile}")
        if not self.active_ponifile:
            return
            
        list_integration_names = le.get_clean_list(
            lineedit=self.lineedit_integrations,
        )
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
    def save_plot(self):
        """
        Saves the intensity profiles shown in graph 1D

        Parameters:
        None

        Returns:
        None
        """
        if not self.list_results_cache:
            self.write_terminal_and_logger("Nothing to save. Return.")
            return

        # Save the file
        if le.text(self.lineedit_savefolder):
            folder_output = Path(le.text(self.lineedit_savefolder))

            if not folder_output.exists():
                confirm_mkdir = QMessageBox.question(self, 'MessageBox', "A new folder will be created. Go'ed?", QMessageBox.Yes | QMessageBox.No)
                if confirm_mkdir == QMessageBox.Yes:
                    folder_output.mkdir()
                else:
                    self.write_terminal_and_logger(f"The .csv file could not be saved.")
                    return                  
        else:
            confirm_save = QMessageBox.question(self, 'MessageBox', "You are going to save in the same data folder. \
                Do you want to continue? You can change it in the blank square above.", QMessageBox.Yes | QMessageBox.No)
            if confirm_save == QMessageBox.Yes:
                folder_output = self.main_directory.joinpath(self.clicked_folder)
            else:
                return

        if not Path(folder_output).exists:
            self.write_terminal_and_logger(f"The .csv file could not be saved.")
            return

        name = Path(le.text(self.lineedit_filename)).stem
        filename_out = str(folder_output.joinpath(name))

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
            dict_results[f"{dict_int['Unit']}_{dict_int['Suffix']}"] = res[0]
            dict_results[f"Intensity_{dict_int['Suffix']}"] = res[1]
            filename_out += f"_{dict_int['Suffix']}"
        filename_out += '.csv'
        self.write_terminal_and_logger(f"Output filename for the image: {filename_out}")
        dataframe = pd.DataFrame.from_dict(dict_results, orient='index')
        dataframe = dataframe.transpose()
        logger.info("Dataframe to be exported as .csv")


        mode = 'w' if Path(filename_out).is_file() else 'a'
        with open(filename_out, mode) as f:
            f.write(f'{str_header}\n')
        dataframe.to_csv(filename_out, sep='\t', mode='a', index=False, header=True)

    @log_info
    def update_table(self, folder_to_display=str(), keys_to_display=list(), reset=True):
        """
        Updates the table with new files (rows) and keys (columns)

        Parameters:
        folder_to_display(str) : string with the name of the folder to display
        keys_to_display(list) : list of strings with the metadata keys to display
        reset(bool) : if True, clear the table before update

        Returns:
        None
        """
        if reset:
            tm.reset(
                table=self.table_files,
            )
            logger.info("Table was reseted.")

        if not folder_to_display:
            folder_to_display = self.clicked_folder

        if not folder_to_display:
            logger.info("No folder to display. Return.")
            return
        else:
            logger.info(f"Folder to display: {folder_to_display}.")

        # Take the list of keys from the lineedit widget
        if not keys_to_display:
            keys_to_display = le.get_clean_list(
                lineedit=self.lineedit_headeritems,
            )
        logger.info(f"Keys to display: {keys_to_display}.")       

        try:
            dataframe = self.h5.get_metadata_dataframe(
                folder_name=folder_to_display,
                list_keys=keys_to_display,
            )
            logger.info(f"Dataframe: {type(dataframe)}.")       
        except:
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
        for ind_row, _ in enumerate(dataframe['Filename']):
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
        self.write_terminal_and_logger(f"New cache filenames: {str(self.cache_filenames)}")

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

        full_filename = self.main_directory.joinpath(
            self.clicked_folder,
            clicked_filename,
        )

        if full_filename.is_file():
            return full_filename
        else:
            return

    @log_info
    def generate_q_map(self, show=True):
        """
        Generates a pop-up window with a 2D map of the pattern transformed to q or theta units

        Parameters:
        None

        Returns:
        None
        """
        # Get the map in the 2D graph widget
        try:
            data = gm.get_array(self.graph_2D_widget)
            logger.info(f"Data from the map. Shape: {data.shape}")
        except:
            return

        # Get the unit of the generated map
        unit = cb.value(self.combobox_units)
        unit = get_pyfai_unit(unit)
        logger.info(f"Unit of the map: {unit}")

        # Get the grid of scattering units
        scat_x, scat_z, data = self.h5.get_mesh_matrix(unit=unit, data=data)
        
        # Get the title using the key metadata from lineedit
        title = self.get_title()

        # Get the limits and ticks
        x_lims, y_lims = self.get_map_limits()
        x_ticks, y_ticks = self.get_map_ticks()        

        # Plot the 2D map
        error_mesh = plot_mesh(
            mesh_horz=scat_x,
            mesh_vert=scat_z,
            data=data, 
            unit=unit,
            auto_lims=self._auto_lims,
            xlim=x_lims,
            ylim=y_lims,
            xticks=x_ticks,
            yticks=y_ticks,
            title=title,
            log=self._graph_log,
            colorbar=self._colorbar,
            color_lims=gm.get_zlims(self.graph_2D_widget),
            show=show,
        )
        logger.info(error_mesh)


    @log_info
    def get_masked_integration_array(self, data):
        """
        Returns the data array masked by the integration parameters from first integration name in the lineedit_integration

        Parameters:
        data: 2D matrix to be corrected

        Returns:
        None
        """
        list_integration_names = le.get_clean_list(
            lineedit=self.lineedit_integrations,
        )
        list_dict_integration = [get_dict_from_name(name=name, path_integration=INTEGRATION_PATH) for name in list_integration_names]
        dict_integration = list_dict_integration[0]
        logger.info(f"Dictionary of integration to be masked: {dict_integration}")

        shape = data.shape

        # Mask for Azimuthal or Radial integration
        if dict_integration["Type"] in ("Azimuthal", "Radial"):
            try:
                unit = dict_integration["Unit"]
                dict_plot = DICT_UNIT_PLOTS.get(unit, DICT_PLOT_DEFAULT)
                p0_range = dict_integration["Radial_range"]
                p1_range = dict_integration["Azimuth_range"]
                pos0_scale = dict_plot['SCALE']
                p0_range = tuple([i / pos0_scale for i in p0_range])
                p1_range = tuple([np.deg2rad(i) + np.pi for i in p1_range]) 

                logger.info(f"Parameters to mask the array. Shape: {shape}, unit: {unit}, \
                    p0_range: {p0_range}, p1_range: {p1_range}, pos0_scale: {pos0_scale}.")  
                chi, pos0 = self.h5.giarray_from_unit(shape, "sector", "center", unit)
            except:
                logger.info("Chi and pos0 matrix could not be generated. The parameters were: \
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
        elif dict_integration["Type"] in ("Horizontal", "Vertical"):
            try:
                unit = dict_integration["Unit"]
                dict_plot = DICT_UNIT_PLOTS.get(unit, DICT_PLOT_DEFAULT)
                oop_range = dict_integration["Oop_range"]
                ip_range = dict_integration["Ip_range"]
                q_scale = dict_plot['SCALE']
                oop_range = tuple([i / q_scale for i in oop_range])
                ip_range = tuple([i / q_scale for i in ip_range])

                logger.info(f"Parameters to mask the array. Shape: {shape}, unit: {unit}, \
                    oop_range: {oop_range}, ip_range: {ip_range}, q_scale: {q_scale}.")
                horz_q, vert_q = self.h5.giarray_from_unit(shape, "opbox", "center", unit)
            except:
                logger.info("horz_q and vert_q matrix could not be generated. The parameters were: \
                    Shape: {shape}, unit: {unit}, oop_range: {oop_range}, ip_range: {ip_range}, q_scale: {q_scale}.")
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
            keys_title = le.get_clean_list(
                lineedit=self.lineedit_headeritems_title,
            )
            title_str = ''
            for key in keys_title:
                metadata_value = self.h5.get_metadata_value(
                    folder_name=self.clicked_folder,
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
    def update_graph_colorbar(self):
        """
        Makes the colorbar visible/unvisible in the popup map

        Parameters:
        None

        Returns:
        None
        """
        if self._colorbar:
            self._colorbar = False
            self.button_colorbar.setText("COLORBAR OFF")
        else:
            self._colorbar = True
            self.button_colorbar.setText("COLORBAR ON")

    @log_info
    def update_auto_lims(self):
        """
        Updates the lims, in auto mode or not, also updates the style of the button itself

        Parameters:
        None

        Returns:
        None
        """
        if self._auto_lims:
            self._auto_lims = False
            self.button_default_graph.setText("AUTO LIMITS OFF")
            self.write_terminal_and_logger(f"Now the auto limits are disabled.")
            self.lineedit_xmin.setEnabled(True)
            self.lineedit_xmax.setEnabled(True)
            self.lineedit_ymin.setEnabled(True)
            self.lineedit_ymax.setEnabled(True)
            self.lineedit_xticks.setEnabled(True)
            self.lineedit_yticks.setEnabled(True)
        else:
            self._auto_lims = True
            self.button_default_graph.setText("AUTO LIMITS ON")
            self._write_output(f"Now the auto limits are enabled.")
            self.lineedit_xmin.setEnabled(False)
            self.lineedit_xmax.setEnabled(False)
            self.lineedit_ymin.setEnabled(False)
            self.lineedit_ymax.setEnabled(False)
            self.lineedit_xticks.setEnabled(False)
            self.lineedit_yticks.setEnabled(False)

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
            lineedit=self.lineedit_xmin,
            new_text=dict_units['X_LIMS'][0],
        )
        le.substitute(
            lineedit=self.lineedit_xmax,
            new_text=dict_units['X_LIMS'][1],
        )
        le.substitute(
            lineedit=self.lineedit_ymin,
            new_text=dict_units['Y_LIMS'][0],
        )
        le.substitute(
            lineedit=self.lineedit_ymax,
            new_text=dict_units['Y_LIMS'][1],
        )
        le.substitute(
            lineedit=self.lineedit_xticks,
            new_text=str(dict_units['X_TICKS'])[1:-1],
        )
        le.substitute(
            lineedit=self.lineedit_yticks,
            new_text=str(dict_units['Y_TICKS'])[1:-1],
        )

    @log_info
    def save_popup_map(self):
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
                    self.write_terminal_and_logger(f"The image could not be saved.")
                    return                  
        else:
            confirm_save = QMessageBox.question(self, 'MessageBox', "You are going to save in the same data folder. \
                Do you want to continue? You can change it in the blank square above.", QMessageBox.Yes | QMessageBox.No)
            if confirm_save == QMessageBox.Yes:
                folder_output = Path(self.clicked_folder)
            else:
                return

        if not Path(folder_output).exists:
            self.write_terminal_and_logger(f"The image could not be saved.")
            return

        filename = Path(le.text(self.lineedit_filename)).stem
        filename_out = folder_output.joinpath(f"{filename}.png")
        self.write_terminal_and_logger(f"Output filename for the image: {filename_out}")
 
        try:
            self.generate_q_map(show=False)
            plt.savefig(filename_out)
            plt.close()
            self.write_terminal_and_logger(f"Imaged was saved.")
        except:
            self.write_terminal_and_logger(f"The image could not be saved.")
            pass

    @log_info
    def update_integration_widgets(self):
        """
        Feeds the combobox with the dictionary of integrations

        Parameters:
        None

        Returns:
        None
        """
        list_integration_cakes, list_integration_boxes = search_integration_names(INTEGRATION_PATH)
        list_integration = list_integration_cakes + list_integration_boxes

        # Update the listwidget for CAKE integration
        lt.insert_list(
            listwidget=self.list_cakes,
            item_list=list_integration_cakes,
            reset=True,
        )

        # Update the listwidget for BOX integration
        lt.insert_list(
            listwidget=self.list_boxs,
            item_list=list_integration_boxes,
            reset=True,
        )

        # Update the combobox with integrations
        integrations_in_cb = set(cb.all_items(self.combobox_integration))
        new_integrations = sorted(item for item in set(list_integration).difference(integrations_in_cb))
        new_integrations = [item for item in new_integrations if item]

        cb.insert_list(
            combobox=self.combobox_integration,
            list_items=new_integrations,
            reset=False,
        )

    @log_info
    def open_fitting_form(self):
        self._write_output("Fitting form not available for the moment.")

    @log_info
    def batch_and_save(self):
        """
        Apply the integration that is in the chart to all the files in selected folder and save the files
        """
        self._write_output("BAtch integration not available for the moment.")
        return
        confirm_batch = QMessageBox.question(self, 'MessageBox', "Are you sure you want to run a batch integration? It may take some minutes+", QMessageBox.Yes | QMessageBox.No)
        if confirm_batch == QMessageBox.Yes:
            files_in_selected_folder = []
            files_in_selected_folder += self._dict_files[self.clicked_folder]

            # Create folder to save the files
            dateprefix = date_prefix()
            if le.text(self.lineedit_savefolder):
                folder_output = join(
                    le.text(self.lineedit_savefolder),
                    f"{basename(self.clicked_folder)}_fittings_{dateprefix}",
                )
                makedir(folder_output)
            else:
                return

            for file in files_in_selected_folder:

                edf = self.get_Edf_instance(filename=file)

                for df in self.integrate_data(
                    data=edf.get_data(),
                    norm_factor=edf.normfactor,
                    dicts_integration=le.get_clean_list(
                        lineedit=self.lineedit_integrations
                    ),
                ):
                    # Dict to string
                    str_header = dict_to_str(dictionary= edf.get_dict() | self.dict_cache)

                    filename_out = join(
                        folder_output, 
                        edf.basename.replace('.edf', f"_{le.text(lineedit=self.lineedit_integrations).replace(',','_')}.csv",
                        ),
                    )

                    mode = 'w' if exists(filename_out) else 'a'

                    with open(filename_out, mode) as f:
                        f.write(f'{str_header}\n')
                    df.to_csv(filename_out, sep='\t', mode='a', index=False, header=True)
        else:
            return

    def hide_show_plaintext(self):
        """
        Hides/shows the output terminal
        """
        if self._terminal_visible:
            self._terminal_visible = False
            self.button_hide_terminal.setText("SHOW TERMINAL")
            self.plaintext_output.setVisible(False)
            self.grid_right.setRowStretch(1,1)
            self.grid_right.setRowStretch(2,1)
            self.grid_right.setRowStretch(3,20)
            self.grid_right.setRowStretch(4,1)
            self.grid_right.setRowStretch(5,0)
        else:
            self._terminal_visible = True
            self.button_hide_terminal.setText("HIDE TERMINAL")
            self.plaintext_output.setVisible(True)
            self.grid_right.setRowStretch(1,1)
            self.grid_right.setRowStretch(2,1)
            self.grid_right.setRowStretch(3,20)
            self.grid_right.setRowStretch(4,1)
            self.grid_right.setRowStretch(5,3)