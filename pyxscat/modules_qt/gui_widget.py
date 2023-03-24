
from . import *
from edf import DICT_SAMPLE_ORIENTATIONS
from modules_qt.gui_layout import GUIPyX_Widget_layout
from os.path import basename, dirname, exists, getctime, join
from pathlib import Path
from plots import plot_mesh

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog, QSplashScreen
from PyQt5.QtGui import QPixmap

from pyxscat.edf import EdfClass
from pyxscat.integrator import Integrator
from pyxscat.other_functions import np_weak_lims, dict_to_str, create_folder
from pyxscat.plots import *
from pyxscat.search_functions import search_files_recursively, list_files_to_dict, get_subfolder

from integration.integrator_methods import DIRECTORY_INTEGRATIONS
from setup.setup_methods import DIRECTORY_SETUPS
from setup.setup_methods import get_dict_setup

from modules_qt import lineedit_methods as le
from modules_qt import combobox_methods as cb
from modules_qt import listwidget_methods as lt
from modules_qt import table_methods as tm
from modules_qt import graph_methods as gm

import json
import numpy as np
import subprocess
import sys
import os

MSG_SETUP_UPDATED = "New setup dictionary was updated."
MSG_SETUP_ERROR = "The setup dictionary could not be updated."
MSG_ROTATED_UPDATED = "Rotation state was updated."
MSG_QZ_DIRECTION_UPDATED = "The qz direction was updated."
MSG_QR_DIRECTION_UPDATED = "The qr direction was updated."
MSG_MAIN_DIRECTORY = "New main directory updated."
MSG_MAIN_DIRECTORY_ERROR = "No main directory was detected."
MSG_EXTENSION_UPDATED = "The file extension was updated."
MSG_WILDCARDS_UPDATED = "The wildcards were updated."
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


class GUIPyX_Widget(GUIPyX_Widget_layout):

    def __init__(self):
        super(GUIPyX_Widget, self).__init__()

        # Splash screen
        pixmap = QPixmap(join(GLOBAL_PATH_QT, 'pyxscat_logo_thumb.png'))
        splash = QSplashScreen(pixmap)
        splash.show()
        splash.finish(self)

        # Declare instance for Integrator class
        self._integrator = None

        # Initialize attributes and callbacks
        self.init_callbacks()        
        self.init_attributes()
        self.update_setup_info()
        self.update_lims_ticks(text=DEFAULT_UNIT)

    def init_callbacks(self) -> None:
        """
            Updates the callbacks to initiate main attributes
        """
        #####################################################################
        ##################  MAIN ATTRIBUTES CALLBACKS  ######################
        #####################################################################

        #########################
        # Setup dictionary callback
        #########################
        self.combobox_setup.currentTextChanged.connect(self.update_setup_info)
        self.combobox_angle.currentTextChanged.connect(self.update_angle_parameter)
        self.combobox_tilt_angle.currentTextChanged.connect(self.update_tiltangle_parameter)
        self.combobox_normfactor.currentTextChanged.connect(self.update_normfactor_parameter)
        self.combobox_exposure.currentTextChanged.connect(self.update_exposure_parameter)
        self.lineedit_angle.returnPressed.connect(self.update_setup_parameter)
        self.lineedit_tilt_angle.returnPressed.connect(self.update_setup_parameter)
        self.lineedit_normfactor.returnPressed.connect(self.update_setup_parameter)
        self.lineedit_exposure.returnPressed.connect(self.update_setup_parameter)
        self.button_setup_save.clicked.connect(self.save_new_setup)
        self.button_setup.clicked.connect(self.pick_json_file)

        #########################
        # Callbacks for rotation and parallel/antiparallel axis
        #########################
        self.button_qz.clicked.connect(
            self.update_qz,
        )
        self.button_qr.clicked.connect(
            self.update_qr,
        )

        #########################
        # Main directory callback
        #########################
        self.lineedit_maindir.returnPressed.connect(
            self.update_maindir,
        )

        self.button_pick_maindir.clicked.connect(
            self.pick_folder,
        )

        #########################
        # Extension and wildcards callback
        #########################
        self.combobox_extension.currentTextChanged.connect(
            self.update_extension,
        )
        self.lineedit_wildcards.returnPressed.connect(
            self.update_wildcards,
        )

        #########################
        # Ponifile callbacks
        #########################
        self.combobox_ponifile.currentTextChanged.connect(
            self.update_ponifile,
        )
        self.button_add_ponifile.clicked.connect(
            self.pick_new_ponifile,
        )

        #########################
        # Reference callbacks
        #########################
        self.combobox_reffolder.currentTextChanged.connect(
            self.update_reference_files,
        )
        self.button_add_reference.clicked.connect(
            self.pick_new_reference,
        )

        #####################################################################
        ##################  MAIN BUTTONS CALLBACKS  #########################
        #####################################################################

        #########################
        # Button to open pyFAI-calib2
        #########################
        self.button_pyfaicalib.clicked.connect(
            self.open_pyFAI_calib2,
        )

        #########################
        # Button to search and update files
        #########################
        self.button_start.clicked.connect(
            lambda : (
                self.create_integrator(),
                self.search_and_update_files(),
            )
        )

        #####################################################################
        ##################  BROWSER CALLBACKS  ##############################
        #####################################################################

        #########################
        # List_widget folder callback
        #########################
        self.listwidget_folders.clicked.connect(
            self.update_clicked_folder,
        )

        #########################
        # Combobox header items updates its lineedit
        #########################
        self.combobox_headeritems.currentTextChanged.connect(
            lambda: le.insert(
                self.lineedit_headeritems,
                cb.value(self.combobox_headeritems)
            )
        )

        # Updates the columns on the table upon changes in the lineedit_headeritems
        self.combobox_headeritems.currentTextChanged.connect(
            self.update_header_items,
        )

        # Click on the table updates the chart
        self.table_files.clicked.connect(
            lambda: self.update_cache(
                filename = self.selected_filename_table(),
                plot=PLOT_SELECTED_TABLE,
            )
        )

        # Combobox_integrations, updates its corresponding lineedit
        self.combobox_integration.currentTextChanged.connect(
            lambda: le.insert(
                self.lineedit_integrations,
                cb.value(self.combobox_integration)
            )
        )
        # Button clear plot clears the chart
        self.button_clearplot.clicked.connect(
            lambda: self.chart_widget.clear()
        )
        # Click on average button to generate average data
        self.button_average.clicked.connect(
            lambda: self.average_data(
                list_files=self.selected_list_filename_table()
            )
        )

        # Button plot to update the chart with cache data
        self.button_plot.clicked.connect(
            self.plot_data_cache,
        )

        # Callback for subtraction widgets
        # self.checkbox_sub.stateChanged.connect(
        #     lambda: self.update_cache(
        #         filename = self.selected_filename_table(),
        #         plot=PLOT_SELECTED_TABLE,
        #     )
        # )

        self.spinbox_sub.valueChanged.connect(
            lambda: self.update_cache(
                filename = self.selected_filename_table(),
                plot=PLOT_SELECTED_TABLE,
            )
        )

        # Button to generate a matplotlib map
        self.button_map.clicked.connect(
            lambda: self.popup_map(
                show=True,
            )
        )
        
        self.combobox_units.currentTextChanged.connect(
            self.update_lims_ticks,
        )

        # Button to save the generated map
        self.button_savemap.clicked.connect(
            self.save_popup_map,
        )

        # Button to save the dataframe in the chart
        self.button_saveplot.clicked.connect(
            self.save_df_chart,
        )

        # Combobox_title, updates its lineedit
        self.combobox_headeritems_title.currentTextChanged.connect(
            lambda: le.insert(
                self.lineedit_headeritems_title,
                cb.value(self.combobox_headeritems_title)
            )
        )

        # Button to visually check the integration parameters
        # self.button_checkmap.clicked.connect(
        #     lambda : (
        #         self.check_integration(),
        #     )
        # )
        self.button_savefit.clicked.connect(
            self.open_fitting_form,
        )

    def init_attributes(self) -> None:
        """
            Initialize main attributes to control to the GUI.
        """
        # Attributes to init the Integrator instance

        self.update_maindir()
        self.update_ponifile()
        self._extension = '.edf'
        self._wildcards = '*'
        self._qz_parallel = True
        self._qr_parallel = True
        self._write_output(f"Now, the qz positive axis goes with the detector axis. Pygix orientation: {DICT_SAMPLE_ORIENTATIONS[(self._qz_parallel, self._qr_parallel)]}")

        self._dict_files = {}
        self._dict_files_reference = {}    

        # Variables for data processing
        self.set_files = []
        self.set_folders = []        
        
        self.filename_cache = ''
        self.sample_data_cache = None
        self._reference_file = ''
        self.reference_data_cache = None
        self.Edf_sample_cache = None
        self.Edf_reference_cache = None
        self.dict_cache = {}
        self.chart_df_cache = None

    # #########################
    # # Update self attributes
    # #########################

    def get_empty_dict_setup(self) -> dict:
        """
            Return an emtpy setup dictionary
        """
        return {
            "Name":str(), "Angle":str(), "Tilt angle":str(), "Norm":str(), "Exposure":str(),
        }

    def collect_setup_parameters(self) -> list:
        """
            Retrieve four names from the lineedits of setup information tab
        """
        return [
            le.text(self.lineedit_setup_name),
            le.text(self.lineedit_angle),
            le.text(self.lineedit_tilt_angle),
            le.text(self.lineedit_normfactor),
            le.text(self.lineedit_exposure),
        ]

    def read_dict_setup(self) -> dict:
        """
            Return a dict setup with the values from the lineedits
        """
        dict_setup = self.get_empty_dict_setup()
        values_setup = self.collect_setup_parameters()

        for key, value in zip(dict_setup.keys(), values_setup):
            dict_setup[key] = value

        return dict_setup

    def update_setup_info(self, name_setup=str(), new_dict=dict()) -> None:
        """
            Declare the dictionary with the counter/motor names used for data visualization/reduction
        """
        # Search for a .json file with the name_setup string
        if name_setup:
            new_dict_setup = get_dict_setup(
                name_setup=name_setup,
            )
        elif new_dict:
            new_dict_setup = new_dict
        else:
            self._dict_setup = dict()
            return

        try:
            self._dict_setup = new_dict_setup
            self._write_output(MSG_SETUP_UPDATED)
            self._write_output(self._dict_setup)

            # Fill the lineedits
            le.substitute(self.lineedit_setup_name, self._dict_setup['Name'])
            le.substitute(self.lineedit_angle, self._dict_setup['Angle'])
            le.substitute(self.lineedit_tilt_angle, self._dict_setup['Tilt angle'])
            le.substitute(self.lineedit_normfactor, self._dict_setup['Norm'])
            le.substitute(self.lineedit_exposure, self._dict_setup['Exposure'])

            # Reset integrator
            if self._integrator:
                self.reset_integrator()
        except:
            self._dict_setup = dict()
            self._write_output(MSG_SETUP_ERROR)

    def update_angle_parameter(self, text=str()) -> None:
        """
            Update the incident angle parameter
        """
        if text:
            le.substitute(self.lineedit_angle, text)

 
    def update_tiltangle_parameter(self, text=str()) -> None:
        """
            Update the tilt angle parameter
        """
        if text:
            le.substitute(self.lineedit_tilt_angle, text)

    def update_normfactor_parameter(self, text=str()) -> None:
        """
            Update the normalization factor parameter
        """
        if text:
            le.substitute(self.lineedit_normfactor, text)

    def update_exposure_parameter(self, text=str()) -> None:
        """
            Update the exposition time parameter
        """
        if text:
            le.substitute(self.lineedit_exposure, text)

    def update_setup_parameter(self) -> None:
        """
            Update the dictionary of setup information from changing the lineedits
        """
        new_dict_info = self.read_dict_setup()
        for key, value in new_dict_info.items():
            if self._dict_setup[key] != value:
                self._dict_setup[key] = value
                self._write_output(MSG_SETUP_UPDATED)
                self._write_output(self._dict_setup)


    def save_new_setup(self) -> None:
        """
            Collect the dictionary and save a .json file
        """
        new_dict_info = self.read_dict_setup()
        file_json = join(DIRECTORY_SETUPS, f"{new_dict_info['Name']}.json")
        with open(file_json, 'w+') as fp:
            json.dump(new_dict_info, fp)
        cb.insert(
            combobox=self.combobox_setup,
            item=new_dict_info['Name'],
        )

    def pick_json_file(self) -> None:
        """
            Open a browser to pick a .json file with setup information
        """
        if self._main_directory:
            json_file = QFileDialog.getOpenFileNames(self, 'Pick .json file', self._main_directory, "*.json")
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

        if self._integrator:
            self._integrator.update_orientation(
                qz_parallel=self._qz_parallel,
                qr_parallel=self._qr_parallel,
            )
        if self.Edf_sample_cache:
            self.Edf_sample_cache.update_orientations(
                qz_parallel=self._qz_parallel,
                qr_parallel=self._qr_parallel,
            )
        if self.Edf_reference_cache:
            self.Edf_reference_cache.update_orientations(
                qz_parallel=self._qz_parallel,
                qr_parallel=self._qr_parallel,
            )

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

        if self._integrator:
            self._integrator.update_orientation(
                qz_parallel=self._qz_parallel,
                qr_parallel=self._qr_parallel,
            )
        if self.Edf_sample_cache:
            self.Edf_sample_cache.update_orientations(
                qz_parallel=self._qz_parallel,
                qr_parallel=self._qr_parallel,
            )
        if self.Edf_reference_cache:
            self.Edf_reference_cache.update_orientations(
                qz_parallel=self._qz_parallel,
                qr_parallel=self._qr_parallel,
            )

    def update_maindir(self, main_dir_text=str()) -> None:
        """
            Take the main directory from lineedit and update the main attribute
        """
        if main_dir_text:
            le.substitute(
                lineedit=self.lineedit_maindir,
                new_text=main_dir_text,
            )
        else:
            main_dir_text = le.text(self.lineedit_maindir).strip()

        # Get the main directory
        if main_dir_text:
            try:
                if exists(main_dir_text):
                    self._main_directory = main_dir_text
                    self._write_output(MSG_MAIN_DIRECTORY)
                    self._write_output(f"New main directory: {self._main_directory}")

                    # Feed the combobox of ponifiles
                    self.update_combobox_ponifile()

                else:
                    self._main_directory = ''
                    self._write_output(MSG_MAIN_DIRECTORY_ERROR)

                if self._integrator:
                    self.reset_integrator()
            except:
                self._main_directory = ''
                self._write_output(MSG_MAIN_DIRECTORY_ERROR)
        else:
            self._main_directory = ''
            pass

    def pick_folder(self) -> None:
        """
            Pick a folder as main directory
        """
        main_dir = Path(QFileDialog.getExistingDirectory(self, 'Choose main directory', "."))
        if main_dir and (main_dir != Path(".")):
            self.update_maindir(rf"{main_dir}")
        else:
            self._main_directory = ''
            pass
        
    def update_combobox_ponifile(self) -> None:
        """
            Search .poni files and feed the combobox
        """
        if self._main_directory:
            try:
                # Search any file with .poni extension inside the main directory
                list_ponifiles = search_files_recursively(
                    directory=self._main_directory,
                    extension='.poni',
                )
                if list_ponifiles:
                    # Reverse the list subtracting the main directory

                    list_ponifiles = [
                        get_subfolder(
                            full_directory = file,
                            main_directory = self._main_directory,
                        ) for file in list_ponifiles
                    ]
                    self._write_output(MSG_COMBOBOX_PONIFILE)

                    # Feed the combobox of ponifiles
                    cb.insert_list(
                        combobox=self.combobox_ponifile,
                        reset=True,
                        list_items=list_ponifiles,
                    )
            except:
                self._write_output(MSG_COMBOBOX_PONIFILE_ERROR)
        else:
            self._write_output(MSG_COMBOBOX_PONIFILE_ERROR)

    def update_extension(self, extension=str()) -> None:
        """
            Update the extension to search files
        """
        self._extension = extension
        self._write_output(MSG_EXTENSION_UPDATED)
        self._write_output(f"The new file extension is {self._extension}")

    def update_wildcards(self, wildcards_text=str()) -> None:
        """
            Update the wildcards to filter files to search
        """
        wildcards_text = le.text(self.lineedit_wildcards).strip()

        # Get the wildcards
        try:
            if wildcards_text:
                self._wildcards = wildcards_text
                self._write_output(MSG_WILDCARDS_UPDATED)
                self._write_output(f"New wildcards: {self._wildcards}")
        except:
            self._wildcards = ''
        
    def update_ponifile(self, ponifile_path=str()) -> None:
        """
            Update the ponifile from the combobox
        """
        try:
            if ponifile_path:
                if exists(ponifile_path):
                    self._ponifile = ponifile_path
                elif self._main_directory and exists(join(self._main_directory, ponifile_path)):
                    self._ponifile = join(self._main_directory, ponifile_path)
                else:
                    self._ponifile = ''
                    self._write_output(MSG_PONIFILE_ERROR)
                    return
                self._write_output(MSG_PONIFILE_UPDATED)
                self._write_output(f"New ponifile: {self._ponifile}")
                if self._integrator:
                    self.reset_integrator()
                return
            else:
                self._ponifile = ''
                self._write_output(MSG_PONIFILE_ERROR)
        except:
            self._ponifile = ''
            self._write_output(MSG_PONIFILE_ERROR)

    def pick_new_ponifile(self) -> None:
        """
            Pick a file as a new ponifile
        """
        if self._main_directory:
            ponifile_path = QFileDialog.getOpenFileNames(self, 'Pick .poni file', self._main_directory, "*.poni")
        else:
            ponifile_path = QFileDialog.getOpenFileNames(self, 'Pick .poni file', '.', "*.poni")

        if ponifile_path:
            try:
                self.update_ponifile(ponifile_path[0][0])
            except:
                pass
        else:
            pass

    def update_ponifile_path(self, ponifile_path=str()) -> None:
        """
            Take the ponifile from lineedit and update the ponifile
        """
        ponifile_path = le.text(self.lineedit_ponifile_path).strip()

        # Get the main directory
        try:
            if ponifile_path and exists(ponifile_path):
                self._ponifile = ponifile_path
                self.label_maindircheck.setText(SYMBOL_CHECK)
                self._write_output(MSG_PONIFILE_UPDATED)
                self._write_output(f"New ponifile: {self._ponifile}")

                if self._integrator:
                    self.reset_integrator()
            else:
                pass
        except:
            pass
        
    def update_reference_files(self, reference_folder=str(), list_files=[]) -> None:
        """
            Search inside the reference folder and take reference files
        """
        if reference_folder and self._main_directory:
            reference_folder = join(self._main_directory, reference_folder)
            try:
                if exists(reference_folder):
                    self._dict_files_reference = list_files_to_dict(
                        list_files=search_files_recursively(
                            directory=reference_folder,
                            extension=self._extension,
                            wildcards=self._wildcards,
                        )
                    )
                    self._write_output(MSG_REFERENCE_FILES_UPDATED)
                else:
                    self._write_output(MSG_REFERENCE_FILES_ERROR)
                    self._dict_files_reference = dict()
            except:
                self._write_output(MSG_REFERENCE_FILES_ERROR)
                self._dict_files_reference = dict()
        elif list_files:
            try:
                self._dict_files_reference = list_files_to_dict(list_files)
                self._write_output(MSG_REFERENCE_FILES_UPDATED)
            except:
                self._write_output(MSG_REFERENCE_FILES_ERROR)
                self._dict_files_reference = dict()
        else:
            self._dict_files_reference = dict()

    def update_reference_file(self, reference_path=str()) -> None:
        """
            Take the reference file from lineedit and update the attribute
        """
        if reference_path:
            pass
        else:
            return

        # Get the reference file
        try:
            if reference_path and exists(reference_path):
                self._reference_file = reference_path
                self._write_output(MSG_REFERENCE_FILE_UPDATED)
                

                if self._integrator:
                    # Update the reference attribute of the self.integrator
                    # self.reset_integrator()
                    pass
            else:
                pass
        except:
            pass

    def pick_new_reference(self) -> None:
        """
            Pick a file as a new reference file
        """
        extension = f"*{cb.value(self.combobox_extension)}"
        try:
            if self._main_directory:
                ref_file = QFileDialog.getOpenFileNames(self, 'Pick reference file', self._main_directory, extension)
            else:
                ref_file = QFileDialog.getOpenFileNames(self, 'Pick reference file', '.', extension)
        except:
            return

        if ref_file:
            try:
                self._reference_file = ref_file[0][0]
                self.update_reference_files(list_files=[self._reference_file])
                self._write_output(f"New reference file: {self._reference_file}")
            except:
                self._reference_file = ''
                return
        else:
            return

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

    def open_pyFAI_calib2_linux(self) -> None:
        """
            If the OS is linux, open pyFAI-calib2 GUI
        """
        if self._main_directory and exists(self._main_directory):
            try:
                subprocess.run([join(os.getcwd(), 'modules_qt', 'bash_files', 'open_calib2.sh'), self._main_directory])
            except:
                pass
        else:
            try:
                subprocess.run([join(os.getcwd(), 'modules_qt', 'bash_files', 'open_calib2.sh'), os.getcwd()])
            except:
                pass

    def open_pyFAI_calib2_windows(self) -> None:
        """
            If the OS is Windows, open pyFAI-calib2 GUI
        """
        if self._main_directory and exists(self._main_directory):
            try:
                os.system(f"cd {self._main_directory}")
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
    # # Create or update integrator instances
    # #########################

    def reset_integrator(self) -> None:
        """
            If exists, remove the previous integrator and create a new one
        """
        if self._integrator:
            self._integrator = None
            try:
                self.create_integrator()
                self._write_output(MSG_RESET_INTEGRATOR)
            except:
                pass
        else:
            pass

    def create_integrator(self) -> None:
        """
            Updates the self._integrator linked to the global dictionary and main attributes
        """
        if self._integrator:
            return
        
        if self._main_directory and self._ponifile:
            try:
                self._integrator = Integrator(
                    main_dir=self._main_directory,
                    dict_files=self._dict_files,
                    dict_files_ref=self._dict_files_reference,
                    dict_setup=self._dict_setup,
                    ponifile_path=self._ponifile,
                    extension=self._extension,
                    wildcards=self._wildcards,
                    qz_parallel=self._qz_parallel,
                    qr_parallel=self._qr_parallel,
                    search_files=False,
                )
                self._write_output(MSG_NEW_INTEGRATOR)
            except:
                self._write_output(MSG_NEW_INTEGRATOR_ERROR)
                self._integrator = None
                return
        else:
            self._integrator = None
            return
        
    def update_integrator_files(self) -> None:
        """
            Update the dictionary of files with new detected ones
        """
        if self._integrator:
            try:
                self._integrator.dict_files = self._dict_files
                self._write_output(MSG_INTEGRATOR_NEW_FILES)
            except:
                return
        else:
            return
            
    # #########################
    # # Search engines
    # #########################

    def search_and_update_files(self) -> None:
        """
            Search the list of detected files and update the widgets
        """
        # First, run the search static mode
        list_files_static = self.search_static_files()

        # Update new files
        self.update_files(
            new_files=list_files_static,
        )

        # If live is on, start the live searching engine, only for Linux
        if self.checkbox_live.isChecked() and ('linux' in sys.platform):
            self.timer_data = QTimer()
            self.timer_data.timeout.connect(
                lambda: self.update_files(
                    new_files=self.search_live_files(),
                )
            )
            self.timer_data.start(INTERVAL_SEARCH_DATA)

    def search_static_files(self) -> list:
        """
            Search new files once, until next push_button event
        """
        if self._main_directory:
            try:
                if exists(self._main_directory):
                    list_files = search_files_recursively(
                        directory=self._main_directory,
                        extension=self._extension,
                        wildcards=self._wildcards,
                    )
                    new_files = list(set(list_files).difference(self.set_files))
                    return new_files
                else:
                    pass
            except:
                pass
        else:
            pass

    def search_live_files(self) -> list:
        """
            Run bash script to find newly created files
        """
        list_files_1s = subprocess.run([join(os.getcwd(), 'modules_qt', 'bash_files', BASH_FILE_1S), self._main_directory, f"{self._wildcards}{self._extension}"],
                                stdout=subprocess.PIPE).stdout.decode().strip().split('\n')
        new_files = list(set(list_files_1s).difference(self.set_files))
        if new_files:
            return new_files
        else:
            pass   

    # #########################
    # # Updating widgets
    # #########################

    def update_files(self, new_files=[]) -> None:
        """
            Search the list of detected files and update the widgets
        """
        if new_files:
            self._write_output(MSG_NEW_DETECTED_FILES)
            sorted(new_files)

            # Check if the new files come from new folders
            new_folders = sorted(list(set([dirname(file) for file in new_files]).difference(self.set_folders)))
            sorted(new_folders)

            # If they are the first detected values, initialize the table with the header keys of the first file
            if not self.set_files:
                cb.set_text(
                    combobox=self.combobox_headeritems,
                    text='Folder',
                )

                cb.set_text(
                    combobox=self.combobox_headeritems,
                    text='Filename',
                )

            # Update the global sets of files and folders
            self.set_files += new_files
            self.set_folders += new_folders

            # Update the global dictionary of folders-files
            self.update_dictionary_files(
                new_folders=new_folders,
                new_files=new_files,
            )
            self.update_integrator_files()

            if new_folders:
                self.updatings_new_folders(list(new_folders))
                    
            # Do the updates regarding last file (or not)
            if self.checkbox_live.isChecked() and ('linux' in sys.platform):
                last_file = self.get_last_file(new_files)
                self.update_cache(
                    filename=last_file,
                    plot=True,
                )
                self.update_table(
                    list_files=self._dict_files[dirname(last_file)],
                )
            else:
                return
        else:
            return

    def update_header_items(self):
        """
            Update the list of header items with the combobox
        """
        try:
            labels = set(
                le.get_list(
                    lineedit=self.lineedit_headeritems,
                ).insert(0,'Filename')
            )
            tm.update_column_names(
                table=self.table_files,
                labels=labels,
                reset=False,
            )
        except:
            pass

    def updatings_new_folders(self, new_folders):
        """
            Update widgets with the new detected folders
        """
        subfolder_list = [
            get_subfolder(
                full_directory=item,
                main_directory=self._main_directory,
            ) for item in new_folders
        ]


        lt.insert_list(
            listwidget=self.listwidget_folders,
            item_list=subfolder_list,
            reset=True,
        )

        cb.insert_list(
            combobox=self.combobox_reffolder,
            list_items=subfolder_list,
        )

    def update_clicked_folder(self) -> None:
        """
            Return the list of files upon the clicked folder in the listwidget
        """
        clicked_folder = lt.click_values(self.listwidget_folders)[0]
        if self._main_directory:
            try:
                path_folder = join(self._main_directory, clicked_folder)
                if exists(path_folder):
                    self._write_output(F"Clicked folder: {clicked_folder}")
                    list_files = self._dict_files[path_folder]
                    self.update_table(
                        list_files=list_files,
                        reset=True,
                    )
            except:
                self._write_output(MSG_CLICKED_FLODER_ERROR)
        else:
            self._write_output(MSG_CLICKED_FLODER_ERROR)
            pass

    def update_cache(self, data=None, filename='', plot=False):
        """
            Update attributes and widgets with the last detected file
        """
        if data is not None:
            self.sample_data_cache = data
        elif filename:
            try:
                self.Edf_sample_cache = EdfClass(
                    filename=filename,
                    ponifile_path=self._ponifile,
                    dict_setup=self._dict_setup,
                    qz_parallel=self._qz_parallel,
                    qr_parallel=self._qr_parallel,
                )
                self._write_output(f"Updated cache with new file: {filename}")
                self.sample_data_cache = self.Edf_sample_cache.get_data()
            except:
                pass
        else:
            return

        if self.spinbox_sub.value() != 0.0:
        # if self.checkbox_sub.isChecked():
            # Try to create an Edf instance of a reference file
            if self._reference_file:
                self.Edf_reference_cache = EdfClass(
                    filename=self._reference_file,
                    ponifile_path=self._ponifile,
                    dict_setup=self._dict_setup,
                    qz_parallel=self._qz_parallel,
                    qr_parallel=self._qr_parallel,
                )
            else:
                try:
                    self.Edf_reference_cache = self.search_reference_file(self.Edf_sample_cache)
                except:
                    self.Edf_reference_cache = None

            # If a reference instance has been created, do the subtraction
            if self.Edf_reference_cache:
                try:
                    self.sample_data_cache = self.sample_data_cache - \
                    self.spinbox_sub.value() * self.Edf_reference_cache.get_data()
                except:
                    pass

        self.filename_cache = filename
        if plot:
            self.plot_data_cache()

    def update_label_display(self, filename):
        """
            Update the label above the graph with the name of the displayed file
        """
        self.lineedit_filename.setText(f"{filename}")

    def update_dictionary_files(self, new_folders=set(), new_files=set()):
        """
            Update the global dictionary with new folders and files
        """
        if new_folders:
            for folder in sorted(new_folders):
                self._dict_files[folder] = []
        else:
            pass

        if new_files:
            for file in sorted(new_files):
                self._dict_files[dirname(file)].append(file)
        else:
            pass

    def get_last_file(self, set_files=[]):
        """
            Returns the file with the highest epoch, time of creation
        """
        return set_files[
            np.argmax(
                [getctime(file) for file in set_files]
            )
        ]

    def plot_data_cache(self):
        """
            Update the plot2d and plo1d with the data stored in cache and the spinbox
        """
        if self.sample_data_cache is None:
            return

        # Update the label with displayed file
        self.update_label_display(
            filename=self.filename_cache
        )

        # Update the graph pattern plot
        self.update_graph_widget(
            graph_widget=self.graph_widget,
            data=self.sample_data_cache,
        )

        # Update the chart plot
        if self._integrator:
            for df in self.integrate_data(
                    data=self.sample_data_cache,
                    dicts_integration=le.get_clean_list(
                        lineedit=self.lineedit_integrations
                    )
                ):
                self.update_chart_widget(
                    chart_widget=self.chart_widget,
                    dataframe=df,
                )

    def update_graph_widget(self, graph_widget, data):
        """
            Update the graph with data
        """
        # print(graph_widget.getDefaultColormap())

        if graph_widget.getGraphXLimits() == (0, 100) and graph_widget.getGraphYLimits() == (0, 100):
            reset_zoom = True
        else:
            reset_zoom = False

        graph_widget.setKeepDataAspectRatio(True)
        graph_widget.setYAxisInverted(True)

        z_lims = np_weak_lims(
                        data=data,
                    )

        graph_widget.setLimits(
                xmin=graph_widget.getGraphXLimits()[0],
                xmax=graph_widget.getGraphXLimits()[1],
                ymin=graph_widget.getGraphYLimits()[0],
                ymax=graph_widget.getGraphYLimits()[1],
            )

        data=np.nan_to_num(data, nan=1e-9)
        data[data==0] = 1e-9

        graph_widget.addImage(
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

    def get_map_limits(self):
        """
            Get the limits from the lineedits
        """
        x_lims = [le.text(lineedit=self.lineedit_xmin), le.text(lineedit=self.lineedit_xmax)]
        y_lims = [le.text(lineedit=self.lineedit_ymin), le.text(lineedit=self.lineedit_ymax)]
        return x_lims, y_lims

    def get_map_ticks(self):
        """
            Get the ticks from the lineedits
        """
        x_ticks = self.get_clean_lineedit(
            lineedit_widget=self.lineedit_xticks
        )
        y_ticks = self.get_clean_lineedit(
            lineedit_widget=self.lineedit_yticks
        )
        return [float(tick) for tick in x_ticks], [float(tick) for tick in y_ticks]

    def integrate_data(self, data, dicts_integration=[]):
        """
            Generate a dataframe for every integration
        """
        for index, (dataframe, data, dict_integration, name) in enumerate(self._integrator.raw_integration_iterator(
            list_data=[data],
            list_integrations=dicts_integration,
            title='',
            x_label='Unit',
            y_label='Suffix',
            sorted=True,
            remove_redundant_x=False,
            )):
            self.df_cache = dataframe
            self.dict_cache = dict_integration

            yield dataframe

    def update_chart_widget(self, chart_widget, dataframe):
        """
            Update the chart window (integrations)
        """
        chart_widget.setLimits(
            xmin=chart_widget.getGraphXLimits()[0],
            xmax=chart_widget.getGraphXLimits()[1],
            ymin=chart_widget.getGraphYLimits()[0],
            ymax=chart_widget.getGraphYLimits()[1],
        )
        print(dataframe)
        if dataframe is not None:
            for index,(x,y) in enumerate(zip([*range(0,len(dataframe.columns),2)],[*range(1,len(dataframe.columns),2)])):
                try:          
                    chart_widget.addCurve(
                        x=dataframe.iloc[:, x],
                        y=dataframe.iloc[:, y],
                        legend=f"{index}",
                        resetzoom=True,
                    )
                except:
                    pass
        else:
            return

    def save_df_chart(self):
        """
            Save the dataframe stored in cache
        """
        try:
            # Dict to string
            str_header = dict_to_str(dictionary= self.Edf_sample_cache.get_dict() | self.dict_cache)

            # Save the file
            if le.text(self.lineedit_savefolder):
                folder_output = le.text(self.lineedit_savefolder)
            else:
                folder_output = join(dirname(self.filename_cache), OUTPUT_FOLDER)

            create_folder(folder_output)

            filename_out = join(folder_output, basename(self.filename_cache).replace(
                '.edf', f"_{le.text(lineedit=self.lineedit_integrations).replace(',','_')}.dat"
                )
            )

            mode = 'w' if exists(filename_out) else 'a'
            with open(filename_out, mode) as f:
                f.write(f'{str_header}\n')
            self.df_cache.to_csv(filename_out, sep='\t', mode='a', index=False, header=True)
        except:
            pass

    def get_clean_lineedit(self, lineedit_widget, separator=','):
        return [item for item in lineedit_widget.text().strip().split(separator) if item]

    def init_table_and_cbs(self, list_files=[]):
        """
            Reset and initiate the table with a first column of filenames and two comboboxes
        """
        if list_files:
            # Reset the table
            tm.reset(
                table=self.table_files
            )

            # Then, introduce all the needed rows for the files
            tm.insert_rows(
                table=self.table_files,
                num=len(list_files)
            )

            # Add one column
            tm.insert_columns(
                table=self.table_files,
                num=1,
                labels=['Filename'],
            )

            for row_ind, file in enumerate(list_files):
                try:
                    tm.update_cell(
                        table=self.table_files,
                        row_ind=row_ind,
                        column_ind=0,
                        st=basename(file),
                    )
                except:
                    pass

            # Feed two comboboxes with the headers of these files
            try:
                new_header_keys = list(EdfClass(
                    filename=list_files[0],
                    dict_setup=self._dict_setup,
                ).get_header().keys())
                new_header_keys.insert(0,'')
            except:
                return
                
            cb.insert_list(
                combobox=self.combobox_headeritems,
                list_items=new_header_keys,
                reset=True,
            )

            cb.insert_list(
                combobox=self.combobox_headeritems_title,
                list_items=new_header_keys,
                reset=True,
            )

            cb.insert_list(
                combobox=self.combobox_angle,
                list_items=new_header_keys,
                reset=True,
            )
            cb.insert_list(
                combobox=self.combobox_tilt_angle,
                list_items=new_header_keys,
                reset=True,
            )
            cb.insert_list(
                combobox=self.combobox_normfactor,
                list_items=new_header_keys,
                reset=True,
            )
            cb.insert_list(
                combobox=self.combobox_exposure,
                list_items=new_header_keys,
                reset=True,
            )
        else:
            return

    def update_table(self, list_files=[], reset=False):
        """
            Update the table upon the selected folders in the list
        """
        if reset:
            self.init_table_and_cbs(
                list_files=list_files,
            )

        labels_header = list(
            set(
                le.get_list(
                    lineedit=self.lineedit_headeritems,
                )
            )
        )

        # Add new columns upon labels_header
        tm.insert_columns(
            table=self.table_files,
            num=len(labels_header),
            labels=labels_header,
        )

        # Feed the table
        if self._integrator:
            for ind_row, Edf in enumerate(self._integrator.edf_iterator(list_files)):
                header_edf = Edf.get_header()
                for ind_column, label in enumerate(labels_header):
                    try:
                        tm.update_cell(
                            table=self.table_files,
                            row_ind=ind_row,
                            column_ind=ind_column+1,
                            st=header_edf[label],
                        )
                    except:
                        pass

    def selected_list_filename_table(self):
        """
            Return a list of full filen ames from selected items
        """
        return [
            self.filename_fromrow(coord[0]) for coord in tm.selected_items(self.table_files) 
            ]

    def selected_filename_table(self):
        """
            Return the filename according to clicked index
        """
        try:
            return join(
                self._main_directory,
                lt.click_values(
                    listwidget=self.listwidget_folders
                )[0],
                tm.item(
                    table=self.table_files,
                    row=tm.row(self.table_files),
                    column=0
                )
            )
        except:
            return

    def filename_fromrow(self, row_index):
        """
            Return the filename according to clicked index
        """
        try:
            return join(
                self._main_directory,
                lt.click_values(
                    listwidget=self.listwidget_folders
                )[0],
                tm.item(
                    table=self.table_files,
                    row=row_index,
                    column=0
                )
            )
        except:
            return

    def average_data(self, list_files):
        """
            Average a list of files and updates the charts
        """
        try:
            self.update_cache(
                data=sum(
                    [
                        Edf.get_data() for Edf in self.iterator_edf_data(list_files)
                    ]
                ) / len(list_files),
                filename=list_files[-1].replace('.edf', '_average.edf'),
                plot=True
            )
        except:
            pass

    # def check_integration(self):
    #     """
    #         Launch a popup map to visualize the integration parameters
    #     """
    #     if self._integrator:
    #         try:
    #             self._integrator.check_integration(
    #                 Edf=self.Edf_sample_cache,
    #                 dict_integration=self.get_dict_integration(
    #                     name=cb.value(
    #                         combobox=self.combobox_integration,
    #                     ),
    #                 ),
    #             )
    #         except:
    #             return
    #     else:
    #         return

    def popup_map(self, show=True):
        """
            Generates a pop-up window with a map of the pattern in cache
        """
        unit = cb.value(self.combobox_units)
        unit = get_pyfai_unit(unit)
        if self._integrator and self.Edf_sample_cache:
            try:
                data = gm.get_array(self.graph_widget)
                scat_x, scat_z, data = self.Edf_sample_cache.get_mesh_matrix(unit=unit, data=data)
            except:
                return
            x_lims, y_lims = self.get_map_limits()
            x_ticks, y_ticks = self.get_map_ticks()
            plot_mesh(
                mesh_horz=scat_x,
                mesh_vert=scat_z,
                data=data, 
                unit=unit,
                auto_lims=False,
                xlim=x_lims,
                ylim=y_lims,
                xticks=x_ticks,
                yticks=y_ticks,
            )

    def update_lims_ticks(self, text=str()):
        """
            Update the values of the lineedits with lims and ticks for the graph widget
        """
        unit = text
        unit = get_pyfai_unit(unit)
        dict_units = DICT_UNIT_PLOTS[unit]
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

    def save_popup_map(self):
        """
            Save the popup map into a png file
        """
        # Save the file
        try:
            if le.text(self.lineedit_savefolder):
                folder_output = le.text(self.lineedit_savefolder)
            else:
                folder_output = join(dirname(self.filename_cache), OUTPUT_FOLDER)

            create_folder(folder_output)
            filename_out = join(folder_output, basename(self.filename_cache).replace(
                '.edf', f"_{le.text(lineedit=self.lineedit_integrations).replace(',','_')}.png"
                )
            )
        except:
            return

        try:
            plt.savefig(filename_out)
        except:
            self.popup_map(
                show=False,
            )
            plt.savefig(filename_out)
            plt.close()

    def search_reference_file(self, Edf):
        """
            If CheckBox_sub is True, search the reference file with the same exposition time as Edf
        """
        if (self.spinbox_sub.value() != 0.0) and self._dict_files_reference:
            for folder_ref in self._dict_files_reference.keys():
                for Edf_ref in self._integrator.edf_iterator(self._dict_files_reference[folder_ref]):
                    if Edf_ref.exposure == Edf.exposure:
                        return Edf_ref
                    else:
                        pass
        else:
            return

    def get_dictionaries_integration(self) -> list:
        """
            Return a list with the dictionaries of all the available integrations
        """
        import json
        list_dicts = []
        for file in os.listdir(DIRECTORY_INTEGRATIONS):
            if file.endswith('json'):
                with open(join(DIRECTORY_INTEGRATIONS, file), 'r') as fp:
                    list_dicts.append(
                        json.load(fp)
                    )
        return list_dicts

    def get_dict_integration(self, name=str()) -> dict:
        """
            Return a dictionary of integration giving a name
        """
        for d in self.get_dictionaries_integration():
            if name == d['Name']:
                return d
        return

    def open_fitting_form(self):
        self._write_output("Fitting form not available for the moment.")