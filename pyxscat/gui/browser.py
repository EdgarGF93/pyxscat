
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSignal

from . import SRC_PATH
from pyxscat.gui.browserlayout import BrowserLayout
from pyxscat.logger_config import setup_logger
from pyxscat.metadata import MetadataBase
from pyxscat.gui import lineedit_methods as le
from pyxscat.gui import listwidget_methods as lt
from pyxscat.gui import combobox_methods as cb
from pyxscat.gui import table_methods as tm
from pyxscat.observer import RootDirObserver
from pyxscat.gui.data_handler import DataHandler

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
from pathlib import Path
from pyFAI.io.ponifile import PoniFile
from pyFAI import load
import numpy as np
import fabio
from collections import defaultdict
import os
import json
import sys

JSON_DIR = Path(SRC_PATH).joinpath('METADATA_FILES')
JSON_DIR.mkdir(exist_ok=True)
INTEGRATIONS_DIRECTORY = Path(__file__).parent.parent.joinpath("integration_dicts")


logger = setup_logger()
def log_info(func):
    def wrapper(*args, **kwargs):
        logger.info(f'_________OPEN FUNCTION: {func.__name__}_________')
        return func(*args, **kwargs)
    return wrapper


class Browser(BrowserLayout):
    new_files_detected = pyqtSignal()
    active_files_changed = pyqtSignal()
    reference_folder_changed = pyqtSignal()
    reference_file_changed = pyqtSignal()
    poni_changed = pyqtSignal()
    integration_requested = pyqtSignal()
    data_changed = pyqtSignal()

    def __init__(self):
        super(Browser, self).__init__()
        self.data_handler = DataHandler(pattern=self.get_pattern())
        self._init_attributes()
        self._init_callbacks()
        self.update_integration_cb()

    def _init_attributes(self):
        self.active_entry = ''
        self.active_index = []
        self.active_files = []
        self.poni = None
        self.meta = None
        self.new_file = ""
        self.reference_directory = ""
        self.reference_file = ""
    
    def _init_callbacks(self):
        self.button_pick_jsonfile.clicked.connect(self._slot_jsonfile_clicked)
        self.button_pick_rootdir.clicked.connect(self._slot_rootdirectory_clicked)
        self.lineedit_pattern.textEdited.connect(self._slot_lineedit_pattern)
        self.button_update.clicked.connect(self._slot_button_update)
        self.button_save.clicked.connect(self._slot_button_save)
        
        self.combobox_ponifile.currentTextChanged.connect(self._slot_poni_changed)
        self.button_pyfaicalib.clicked.connect(self._slot_pyfai_calib)
         
        self.combobox_integration.currentTextChanged.connect(self._slot_combobox_integration)
        self.checkbox_mask_integration.stateChanged.connect(self._slot_mask_integration)
          
        self.combobox_reference_folder.currentTextChanged.connect(self._slot_reffolder_changed)
        self.spinbox_subtraction_scale.valueChanged.connect(self._slot_spinboxsub_changed)

        self.checkbox_auto_reference_file.stateChanged.connect(self._slot_checkbox_auto)
        self.combobox_reference_file.currentTextChanged.connect(self._slot_combobox_reference_file)

        self.button_mask_file.clicked.connect(self._slot_button_mask)
        
        self.lineedit_savefolder.textEdited.connect(self._slot_lineedit_savefolder)
        self.button_saveplot.clicked.connect(self._slot_button_saveplot)
        self.button_batch.clicked.connect(self._slot_button_batch)
        
        self.button_mirror.clicked.connect(self._slot_button_mirror)
        self.button_qz.clicked.connect(self._slot_button_qz)
        self.button_qr.clicked.connect(self._slot_button_qr)
        
        self.lineedit_acquisition.textEdited.connect(self._slot_le_acquisition_changed)
        self.lineedit_normfactor.textEdited.connect(self._slot_le_normalization_changed)
        self.lineedit_iangle.textEdited.connect(self._slot_le_iangle_changed)
        self.lineedit_tilt_angle.textEdited.connect(self._slot_le_tangle_changed)
        
        # self.lineedit_name_cake.textEdited.connect(self._slot_cake)
        # self.combobox_type_cake.textEdited.connect(self._slot_cake)
        # self.spinbox_azimbins_cake.textEdited.connect(self._slot_cake)
        # self.spinbox_radialbins_cake.textEdited.connect(self._slot_cake)
        # self.spinbox_radialmin_cake.textEdited.connect(self._slot_cake)
        # self.spinbox_radialmax_cake.textEdited.connect(self._slot_cake)
        # self.spinbox_azimmin_cake.textEdited.connect(self._slot_cake)
        # self.spinbox_azimmax_cake.textEdited.connect(self._slot_cake)
        # self.combobox_units_cake.textEdited.connect(self._slot_cake)
        # self.list_cakes.itemClicked.connect(self._slot_list_cakes)

        # self.lineedit_name_box.textEdited.connect(self._slot_box)
        # self.combobox_direction_box.textEdited.connect(self._slot_box)
        # self.spinbox_box_bins.textEdited.connect(self._slot_box)
        # self.combobox_units_box.textEdited.connect(self._slot_box)
        # self.spinbox_ipmin_box.textEdited.connect(self._slot_box)
        # self.spinbox_ipmax_box.textEdited.connect(self._slot_box)
        # self.spinbox_oopmin_box.textEdited.connect(self._slot_box)
        # self.spinbox_oopmax_box.textEdited.connect(self._slot_box)
        # self.combobox_outputunits_box.textEdited.connect(self._slot_box)
        # self.list_box.itemClicked.connect(self._slot_list_boxes)
        
        # self.button_update_old_poni_parameters.clicked.connect(self._slot_retrieve_poni)
        # self.button_update_poni_parameters.clicked.connect(self._slot_update_poni)
        # self.button_save_poni_parameters.clicked.connect(self._slot_save_poni)

        self.listwidget_samples.itemClicked.connect(self._slot_active_entry_changed)
        self.table_files.itemSelectionChanged.connect(self._slot_active_index_changed)

        self.new_files_detected.connect(self._update_new_files)







    def _init_watchdog(self):
        class NewFileHandler(FileSystemEventHandler):
            def __init__(self, parent, pattern="*.edf"):
                self._pattern = pattern
                self.parent = parent
                
                
            def on_any_event(self, event):
                if event.event_type == "created" and event.is_directory == False:
                    filename = event.src_path
                    if Path(filename).match(self._pattern):
                        self.parent.new_file = filename
                        self.parent.new_files_detected.emit()
                                                
        self._observer = Observer()
        self._event_handler = NewFileHandler(
            parent=self,
            pattern=self.get_pattern(),
        )
        self._observer.schedule(
            event_handler=self._event_handler, 
            path=self.meta.directory, 
            recursive=True,
        )
        self._observer.start()

    def update_integration_cb(self):
        combobox = self.combobox_integration
        combobox.clear()
        json_files = [file.stem for file in INTEGRATIONS_DIRECTORY.glob("*.json")]
        combobox.addItems(texts=json_files)

    ######################
    ##### SETTERS ########
    ######################
    
    @property
    def acquisitiontime_key(self):
        return self._acquisitiontime_key
    
    @acquisitiontime_key.setter
    def acquisitiontime_key(self, value):
        if isinstance(value, str):
            self._acquisitiontime_key = value
        else:
            self._acquisitiontime_key = ""
        if self._acquisitiontime_key != self.lineedit_acquisition.text():
            self.lineedit_acquisition.setText(self._acquisitiontime_key)
        self.data_handler.set_acquisitiontime_key(key=self._acquisitiontime_key)
        
    def set_acquisitiontime_key(self, key=""):
        self.acquisitiontime_key = key
    
    @property
    def normalizationfactor_key(self):
        return self._normalizationfactor_key
    
    @normalizationfactor_key.setter
    def normalizationfactor_key(self, value):
        if isinstance(value, str):
            self._normalizationfactor_key = value
        else:
            self._normalizationfactor_key = ""
        if self._normalizationfactor_key != self.lineedit_normfactor.text():
            self.lineedit_normfactor.setText(self._normalizationfactor_key)
        self.data_handler.set_normalizationfactor_key(key=self._normalizationfactor_key)
        
    def set_normalizationfactor_key(self, key=""):
        self.normalizationfactor_key = key
        
    @property
    def incidentangle_key(self):
        return self._incidentangle_key
    
    @incidentangle_key.setter
    def incidentangle_key(self, value):
        if isinstance(value, str):
            self._incidentangle_key = value
        else:
            self._incidentangle_key = ""
        if self._incidentangle_key != self.lineedit_iangle.text():
            self.lineedit_iangle.setText(self._incidentangle_key)
        self.data_handler.set_incidentangle_key(key=self._incidentangle_key)
    
    def set_incidentangle_key(self, key=""):
        self.incidentangle_key = key
    
    @property
    def tiltangle_key(self):
        return self._tiltangle_key
    
    @tiltangle_key.setter
    def tiltangle_key(self, value):
        if isinstance(value, str):
            self._tiltangle_key = value
        else:
            self._tiltangle_key = ""
        if self._tiltangle_key != self.lineedit_tilt_angle.text():
            self.lineedit_tilt_angle.setText(self._tiltangle_key)
        self.data_handler.set_incidentangle_key(key=self._tiltangle_key)
    
    def set_tiltangle_key(self, key=""):
        self.tiltangle_key = key
    
    
    
    
    
    @property
    def active_entry(self):
        return self._active_entry
    
    @active_entry.setter
    def active_entry(self, value):
        self._active_entry = value
        self._active_entry_changed()

    @property
    def active_index(self):
        return self._active_index
    
    @active_index.setter
    def active_index(self, value):
        self._active_index = value
        if self._active_index:
            self._active_index_changed()
            
    @property
    def active_files(self):
        return self._active_files
    
    @active_files.setter
    def active_files(self, value):
        if isinstance(value, str):
            active_files = [value]
        elif isinstance(value, list):
            active_files = value
        else:
            active_files = []
        
        if active_files:
            _active_files = active_files.copy()
            for index, file in enumerate(active_files):
                if not Path(file).is_file():
                    _active_files.pop(index)
            self._active_files = _active_files
            self._active_files_changed()
                    
    @property
    def poni(self):
        return self._poni
    
    @poni.setter
    def poni(self, value):
        self._poni = value
        self._poni_instance_changed()
        
    @property
    def reference_directory(self):
        return self._reference_directory
    
    @reference_directory.setter
    def reference_directory(self, value):
        self._reference_directory = value
        if self._reference_directory:
            self.data_handler.set_reference_directory(reference_directory=self._reference_directory)
            # Fill the combobox with files
            files_in_reference_folder = self.meta.get_files_in_entry(entry_name=self._reference_directory, relative_path=True)
            self.combobox_reference_file.clear()
            cb.insert_list(
                combobox=self.combobox_reference_file,
                list_items=files_in_reference_folder,
            )        
            
    ######################
    ####### SLOTS ########
    ######################
        
    @log_info
    def _slot_jsonfile_clicked(self, _):
        """
        Chain of events after pressing the json file button
        """
        self._init_browser_from_pick_file()

    @log_info
    def _slot_rootdirectory_clicked(self,_):
        """
        Chain of events after pressing the folder button
        """
        self._init_browser_from_pick_dir()
        
    def _slot_lineedit_pattern(self, pattern):
        self.meta._pattern = pattern
        self.data_handler.pattern = pattern
    
    def _slot_button_update(self, _):
        pass
    
    def _slot_button_save(self, _):
        pass
    
    @log_info
    def _slot_poni_changed(self, poni_name):
        """
        Updates the .poni parameters from a changed value of .poni filename

        Arguments:
            poni_name -- string of .poni filename
        """
        poni_filename = self.meta._get_absolute_path_of_entry(relative_path=poni_name)
        self.poni = PoniFile(data=poni_filename)

    def _slot_pyfai_calib(self, _):
        os.system("pyFAI-calib2")
        self.meta.update()
        
    def _slot_combobox_integration(self, list_integrations):
        print(list_integrations)
        
    def _slot_mask_integration(self, _):
        pass
        
    @log_info
    def _slot_reffolder_changed(self, reference_folder):
        reference_folder = self.meta._get_absolute_path_of_entry(relative_path=reference_folder)
        self.reference_directory = reference_folder
        

    @log_info
    def _slot_spinboxsub_changed(self, value):
        self.data_handler.set_reference_factor(reference_factor=value)
        self.data_changed.emit()
    
    def _slot_checkbox_auto(self, state):
        if state:
            self.data_handler.set_reference_file(reference_file="")
            self.combobox_reference_file.setEnabled(False)
            self.data_handler.update_reference()
        else:
            self.combobox_reference_file.setEnabled(True)
            
    def _slot_combobox_reference_file(self, reference_file):
        if not self.checkbox_auto_reference_file.checkState():
            reference_file = self.meta._get_absolute_path_of_file(
                relative_path=reference_file,
                entry_name=self._reference_directory,
            )
            self.data_handler.set_reference_file(reference_file=reference_file)

    def _slot_button_mask(self, _):
        pass
    
    def _slot_lineedit_savefolder(self, save_path):
        pass
    
    def _slot_button_saveplot(self, _):
        pass
    
    def _slot_button_batch(self, _):
        pass
    
    def _slot_button_mirror(self, _):
        pass
    
    def _slot_button_qz(self, _):
        pass
    
    def _slot_button_qr(self, _):
        pass
    
    def _slot_le_acquisition_changed(self, new_key):
        self.acquisition_key = new_key

    def _slot_le_normalization_changed(self, new_key):
        self.normalization_key = new_key

    def _slot_le_iangle_changed(self, new_key):
        self.incidentangle_key = new_key

    def _slot_le_tangle_changed(self, new_key):
        self.tiltangle_key = new_key










    @log_info
    def _slot_active_entry_changed(self, new_entry):
        self.active_entry = new_entry.text()
        
    @log_info
    def _slot_active_index_changed(self):
        self.active_index = tm.selected_rows(self.table_files)
        

        
            
            

    #################################
    #### INIT BROWSER METHODS #######
    #################################

    @log_info
    def _init_browser_from_pick_dir(self):
        # Get the address of a root directory
        root_directory = self._pick_root_directory()
        if not root_directory:
            return
        
        # Parse root_directory and pattern
        root_directory = Path(root_directory)
        pattern = self.get_pattern()

        self._init_browser(
            root_directory=root_directory,
            pattern=pattern,
            json_file="",
        )

    @log_info
    def _init_browser_from_pick_file(self):
        json_file = self._pick_json_file()

        if not json_file:
            return
        
        if not Path(json_file).is_file():
            return
        
        self._init_browser(
            root_directory="",
            pattern=self.get_pattern(),
            json_file=json_file,
        )

    @log_info
    def _init_browser(
        self, 
        root_directory: str = '', 
        pattern: str = '',
        json_file="",
        ):
        """Instanciate the MetadataBase class and updates the widgets of the browser

        Params:
            root_directory (str) : path of the directory where to search files recursively
            pattern (str) : pattern to find data files
        """
        if not self._init_metadatabase(
            root_directory=root_directory,
            pattern=pattern,
            json_file=json_file,
            ):
            return
        self._init_watchdog()
        self.update_jsonfile_lineedit()
        self.update_rootdir_lineedit()
        self.update_listwidget(init=True)
        self.update_referencecb(init=True)
        self.update_ponicb(init=True)

    @log_info
    def _init_metadatabase(
        self,
        root_directory="", 
        pattern="", 
        output_directory: str = '',
        json_file="",
        ) -> bool:
        
        if root_directory:
            try:
                self.meta = MetadataBase(
                    directory=root_directory,
                    pattern=pattern,
                    update_metadata=True,
                    json_file="",
                )
                self._save_meta_file(output_directory=output_directory)
                
                return True
            except Exception as e:
                logger.error(f'{e}: MetadataBase could not be initialized with directory: {root_directory}')
                return False
        elif json_file:
            try:
                self.meta = MetadataBase(
                    directory="",
                    pattern=pattern,
                    update_metadata=True,
                    json_file=json_file,
                )
                return True
            except Exception as e:
                logger.error(f"{e}: MetadataBase could not be initialized with json file: {json_file}")

    def _save_meta_file(self, output_directory: str = ''):
        self.meta.save(output_directory=output_directory)


    @log_info
    def update_jsonfile_lineedit(self):
        lineedit = self.lineedit_jsonfile
        new_text = Path(self.meta._json_file).name
        self._update_jsonfile_lineedit(
            lineedit=lineedit,
            new_text=new_text,
        )

    @log_info
    def _update_jsonfile_lineedit(self, lineedit, new_text: str):
        le.substitute(
            lineedit=lineedit,
            new_text=new_text,
        )

    @log_info
    def update_rootdir_lineedit(self):
        lineedit = self.lineedit_root_dir
        new_text = self.meta.directory
        self._update_rootdir_lineedit(
            lineedit=lineedit,
            new_text=new_text,
        )

    @log_info
    def _update_rootdir_lineedit(self, lineedit, new_text: str):
        le.substitute(
            lineedit=lineedit,
            new_text=new_text,
        )
        
    @log_info
    def update_listwidget(self, init=False):
        if init:
            self._init_listwidget()
        else:
            self._update_listwidget()

    @log_info
    def _init_listwidget(self):
        listwidget = self.listwidget_samples

        # Reset listwidget
        lt.clear(listwidget=listwidget)

        # Feed listwidget
        for entry in self.meta._generate_entries(relative_path=True):
            lt.insert(
                listwidget=listwidget,
                item=entry,
                repeat_file=False,
            )

    @log_info
    def _update_listwidget(self):
        listwidget = self.listwidget_samples
        for entry in self.meta._generate_new_entries(relative_path=True):
            lt.insert(
                listwidget=listwidget,
                item=entry,
                repeat_file=False,
            )

    @log_info
    def update_referencecb(self, init=False):
        if init:
            self._init_referencecb()
        else:
            self._update_referencecb()

    @log_info
    def _init_referencecb(self):
        combobox = self.combobox_reference_folder
        cb.clear(combobox=combobox)
        for entry in self.meta._generate_entries(relative_path=True):
            cb.insert(
                combobox=combobox,
                item=entry,
            )

    @log_info
    def _update_referencecb(self):
        combobox = self.combobox_reference_folder
        for entry in self.meta._generate_new_entries(relative_path=True):
            cb.insert(
                combobox=combobox,
                item=entry,
            )

    @log_info
    def update_ponicb(self, init=True):
        if init:
            self._init_ponicb()
        else:
            self._update_ponicb()

    @log_info
    def _init_ponicb(self):
        combobox = self.combobox_ponifile
        cb.clear(combobox=combobox)
        cb.insert_list(
            combobox=combobox,
            list_items=self.meta.get_ponifiles(relative_path=True),
        )

    @log_info
    def _update_ponicb(self):
        combobox = self.combobox_ponifile
        for ponifile in self.meta.get_new_ponifiles(relative_path=True):
            cb.insert(
                combobox=combobox,
                item=ponifile,
            )

    @log_info
    def _update_poni(self, poni):
        self._poni = poni

    @log_info
    def updated_acquisition_key(self):
        self.lineedit_acquisition.clear()
        self.lineedit_acquisition.setText(str(self.acquisition_key))

    @log_info
    def updated_normalization_key(self):
        self.lineedit_normfactor.clear()
        self.lineedit_normfactor.setText(str(self.normalization_key))

    @log_info
    def updated_incidentangle_key(self):
        self.lineedit_iangle.clear()
        self.lineedit_iangle.setText(str(self.incidentangle_key))


    @log_info
    def updated_tiltangle_key(self):
        self.lineedit_tilt_angle.clear()
        self.lineedit_tilt_angle.setText(str(self.tiltangle_key))

    @log_info
    def update_poni_widgets(self):
        """
        Update the ponifile widgets from a valid PoniFile instance

        Keyword Arguments:
            poni -- instance of PoniFile (default: {None})
        """        
        self._update_detector_widget()
        self._update_wavelength_widget()
        self._update_dist_widget()
        self._update_poni1_widget()
        self._update_poni2_widget()
        self._update_rot1_widget()
        self._update_rot2_widget()
        self._update_rot3_widget()

    @log_info
    def _update_detector_widget(self):
        """
        Update the widget with detector information

        Keyword Arguments:
            poni -- instance of PoniFile (default: {None})
        """        
        widget = self.lineedit_detector

        try:
            detector_name = self._poni.detector.name
        except Exception as e:
            logger.error(f"{e}: Detector name could not be retrieved from {self._poni}.")
            detector_name = ''

        try:
            detector_bin = self._poni.detector.binning
        except Exception as e:
            logger.error(f"{e}: Detector binning could not be retrieved from {self._poni}.")
            detector_bin = ('x','x')

        try:
            shape = self._poni.detector.shape
            shape = (shape[0], shape[1])
        except Exception as e:
            logger.error(f"{e}: Shape could not be retrieved from {self._poni}.")
            shape = (0,0)         

        detector_info = f'{str(detector_name)} / {str(detector_bin)} / {str(shape)}'

        le.substitute(
                lineedit=widget,
                new_text=detector_info,
            )
  
    @log_info
    def _update_wavelength_widget(self):
        """
        Update the widget with wavelength parameter

        Keyword Arguments:
            poni -- instance of PoniFile (default: {None})
        """ 
        widget = self.lineedit_wavelength

        try:
            wave = self._poni.wavelength
        except Exception as e:
            logger.error(f"{e}: Wavelength could not be retrieved from {self._poni}.")
            wave = 0.0

        le.substitute(
                lineedit=widget,
                new_text=wave,
            )

    @log_info
    def _update_dist_widget(self):
        """
        Update the widget with sample-detector distance parameter

        Keyword Arguments:
            poni -- instance of PoniFile (default: {None})
        """ 
        widget = self.lineedit_distance

        try:
            dist = self._poni.dist
        except Exception as e:
            logger.error(f"{e}: Distance could not be retrieved from {self._poni}.")
            dist = 0.0

        le.substitute(
                lineedit=widget,
                new_text=dist,
            )

    @log_info
    def _update_poni1_widget(self):
        """
        Update the widget with PONI 1 parameter

        Keyword Arguments:
            poni -- instance of PoniFile (default: {None})
        """ 
        widget = self.lineedit_poni1

        try:
            poni1 = self._poni.poni1
        except Exception as e:
            logger.error(f"{e}: PONI1 could not be retrieved from {self._poni}.")
            poni1 = 0.0

        le.substitute(
                lineedit=widget,
                new_text=poni1,
            )

    @log_info
    def _update_poni2_widget(self):
        """
        Update the widget with PONI 2 parameter

        Keyword Arguments:
            poni -- instance of PoniFile (default: {None})
        """ 
        widget = self.lineedit_poni2

        try:
            poni2 = self._poni.poni2
        except Exception as e:
            logger.error(f"{e}: PONI2 could not be retrieved from {self._poni}.")
            poni2 = 0.0

        le.substitute(
                lineedit=widget,
                new_text=poni2,
            )

    @log_info
    def _update_rot1_widget(self):
        """
        Update the widget with rotation_1 parameter

        Keyword Arguments:
            poni -- instance of PoniFile (default: {None})
        """ 
        widget = self.lineedit_rot1

        try:
            rot1 = self._poni.rot1
        except Exception as e:
            logger.error(f"{e}: ROT1 could not be retrieved from {self._poni}.")
            rot1 = 0.0

        le.substitute(
                lineedit=widget,
                new_text=rot1,
            )

    @log_info
    def _update_rot2_widget(self):
        """
        Update the widget with rotation_2 parameter

        Keyword Arguments:
            poni -- instance of PoniFile (default: {None})
        """ 
        widget = self.lineedit_rot2

        try:
            rot2 = self._poni.rot2
        except Exception as e:
            logger.error(f"{e}: ROT2 could not be retrieved from {self._poni}.")
            rot2 = 0.0

        le.substitute(
                lineedit=widget,
                new_text=rot2,
            )

    @log_info
    def _update_rot3_widget(self):
        """
        Update the widget with rotation_3 parameter

        Keyword Arguments:
            poni -- instance of PoniFile (default: {None})
        """ 
        widget = self.lineedit_rot3

        try:
            rot3 = self._poni.rot3
        except Exception as e:
            logger.error(f"{e}: ROT3 could not be retrieved from {self._poni}.")
            rot3 = 0.0

        le.substitute(
                lineedit=widget,
                new_text=rot3,
            )
        
    @log_info
    def update_active_entry(self, new_entry):
        self._update_active_entry(new_entry=new_entry)


    @log_info
    def _update_active_entry(self, new_entry: str):
        self._active_entry =new_entry

    @log_info
    def _active_entry_changed(self):
        if not self._active_entry:
            return
        self.update_cbs_metadata()
        self.update_table()        

    @log_info
    def _active_index_changed(self):
        if not self._active_index:
            return
        self.active_files = self.get_active_filenames()

    @log_info
    def _active_files_changed(self):
        self.data_handler.set_filenames(list_filenames=self._active_files)
        self.active_files_changed.emit()

    @log_info
    def _poni_instance_changed(self):
        if not self._poni:
            return
        self.data_handler.set_poni(poni=self._poni)
        self.update_poni_widgets()

    @log_info
    def get_active_filenames(self):
        if not self.meta:
            return []
        return self.meta.get_filenames(
            entry_name=self._active_entry,
            index=self._active_index,
            relative_path=False,
        )

    @log_info
    def update_cbs_metadata(self):
        if not self._active_entry:
            return
        
        metadata_keys = self.meta.get_all_metadata_in_entry(
            entry_name=self._active_entry,
        )
        self._update_cbs_metadata(
            metadata_keys=metadata_keys,
        )

    @log_info
    def _update_cbs_metadata(self, metadata_keys:list):
        self.combobox_metadata.addItems(texts=metadata_keys)
        self.combobox_iangle.addItems(texts=metadata_keys)
        self.combobox_tilt_angle.addItems(texts=metadata_keys)
        self.combobox_normfactor.addItems(texts=metadata_keys)
        self.combobox_acquisition.addItems(texts=metadata_keys)

    @log_info
    def update_table(self):
        if not self._active_entry:
            return
        
        keys_to_display = self.combobox_metadata.currentData()
        dataframe = self.meta.get_dataframe_metadata(
            entry_name=self.active_entry,
            list_keys=keys_to_display,
            relative_path=True,
        )
        self._update_table(
            dataframe=dataframe,
        )

    @log_info
    def _update_table(self, dataframe, reset=True):
        table = self.table_files

        # Clean table if required
        if reset:
            tm.reset(table=self.table_files)
        if dataframe is None:
            return

        # Add columns for the displayed metadata keys
        n_columns = len(dataframe.columns)
        labels_columns = list(dataframe.columns)
        tm.insert_columns(
            table=table,
            num=n_columns,
            labels=labels_columns,
        )

        # Add the rows for all the displayed files
        n_rows = len(dataframe)
        tm.insert_rows(
            table=table,
            num=n_rows,
        )

        # Add the new key values for every file
        for ind_row, _ in enumerate(dataframe["filenames"]):
            for ind_column, key in enumerate(dataframe):
                try:
                    tm.update_cell(
                        table=table,
                        row_ind=ind_row,
                        column_ind=ind_column,
                        st=dataframe[key][ind_row],
                    )
                except Exception as e:
                    logger.error(f'{e}. The key {key} could not be displayed in table.')


    # # INTEGRATION METHOD
    # @log_info
    # def update_data_cache(self):
    #     list_filenames = self.get_active_filenames()
    #     if not list_filenames:
    #         return
    #     self._update_data_cache(
    #         list_filenames=list_filenames,
    #     )
        
    # # @log_info
    # # def _update_data_cache(self, list_filenames):
    # #     data = self._open_data(list_filenames=list_filenames)
    #     if self.spinbox_subtraction_scale.value() != 0.0:
    #         self.update_reference_file()
    #         if self.reference_data is not None:
    #             data = data - self.spinbox_subtraction_scale.value() * self.reference_data
    #     self.data_cache = self._clean_data(data=data)        

    # @log_info
    # def _open_data(self, list_filenames:list):
    #     if len(list_filenames) > 1:
    #         data = self._average_data(list_filenames=list_filenames)
    #     else:
    #         data = fabio.open(list_filenames[0]).data
    #     return data
    
    # @log_info
    # def _average_data(self, list_filenames:list):
    #     return np.average([fabio.open(file).data for file in list_filenames], axis=0)
    

    
    # @log_info
    # def _data_cache_changed(self):
    #     self.data_cache_changed.emit()
    #     self.update_integration()

    # @log_info
    # def update_integration(self):
    #     if self.data_cache is None:
    #         return
        
    #     list_integrations = self.combobox_integration.currentData()
    #     self.results = []

    #     if not list_integrations:
    #         res1d = self._do_azimuthal_integration(config=None)
    #         self.results.append(res1d)

    #     for integration_name in list_integrations:
    #         config = self._get_json_config(integration_name=integration_name)
    #         if config["integration"] == "cake":
    #             res1d = self._do_azimuthal_integration(config=config)
    #             self.results.append(res1d)

    #     self.results1d_updated.emit()
                


    
    # @log_info
    # def _do_azimuthal_integration(self, config:dict={}):
    #     try:
    #         if not config:
    #             return self.ai.integrate1d(data=self._data_cache, npt=1000)

    #         npt = 2000 if config["azim_bins"] == 0 else config["azim_bins"]
    #         res1d = self.ai.integrate1d(
    #             data=self._data_cache, 
    #             npt=npt,
    #             radial_range=config["radial_range"],
    #             azimuth_range=config["azimuth_range"],
    #             unit=config["unit"],
    #         )
    #         return res1d
    #     except Exception as e:
    #         logger.error(f"AzimuthalIntegration did not work, check poni file?")

    # @log_info
    # def _integration_complete(self):
    #     self.results1d_updated.emit()





    #####################
    # REFERENCE METHODS #
    #####################
        
    # def update_reference_file(self):
    #     acquisition_key = self.acquisition_key
    #     if not acquisition_key:
    #         return
        
    #     if not self.active_entry:
    #         return
        
    #     if not self.active_index:
    #         return
                
    #     acquisition_time = self.meta.get_metadata(
    #         entry_name=self.active_entry, 
    #         index=self.active_index[0],
    #         metadata_key=acquisition_key,
    #     )

    #     self._search_reference_file(
    #         acquisition_time=acquisition_time,
    #         reference_folder=self.reference_folder,
    #     )
        
    # def _search_reference_file(self, acquisition_time, reference_folder):
    #     if acquisition_time == self.reference_acqtime:
    #         return
        
    #     for ind, metadata in enumerate(self.meta._generate_metadata_in_entry(entry_name=reference_folder, metadata_key=self.acquisition_key)):
    #         if metadata == acquisition_time:
    #             reference_filename = self.meta.get_filenames(entry_name=reference_folder, index=[ind])[0]
    #             self.reference_data = fabio.open(reference_filename).data
    #             self.reference_acqtime = acquisition_time
    #             return
    #     self.reference_data = None
    #     self.reference_acqtime = None
            

        




    ##################
    # DIALOG METHODS #
    ##################
        
    @log_info
    def _pick_root_directory(self) -> Path:
        """
        Picks a folder as root directory, where the data files are searched recursively

        Returns:
            Path instance with the root directory
        """        
        # Pick the folder after pop-up browser window
        self.dialog_json = QFileDialog()
        get_directory = self.dialog_json.getExistingDirectory(self, 'Choose main directory', os.getcwd())

        # Returns if is not valid, or the dialog was cancelled
        if not get_directory:
            root_directory = ""
            logger.info("No root directory was picked.")
        else:
            try:
                root_directory = Path(get_directory)
                logger.info(f'New root directory: {root_directory}')
            except NotImplementedError as e:
                logger.error(f'The root directory ({root_directory}) is not valid for Path instance: {e}')
                root_directory = ""
        return root_directory

    @log_info
    def _pick_json_file(self) -> Path:
        self.dialog_json = QFileDialog()
        get_json = self.dialog_json.getOpenFileNames(self, 'Pick .json file', '.', "*.json")

        # Returns if is not valid, or the dialog was cancelled
        if not get_json:
            json_file = ""
            logger.info("No file was picked.")
        else:
            try:
                json_file = Path(get_json[0][0])
                logger.info(f'New root directory: {json_file}')
            except NotImplementedError as e:
                logger.error(f'The root directory ({json_file}) is not valid for Path instance: {e}')
                json_file = ""
        return json_file



    # METHODS NEW FILES
    def _update_new_files(self):
        new_file = self.new_file
        entry_name = Path(new_file).parent
        self.meta._update_entry(
            entry_name=entry_name,
            file_iterator=[new_file],
        )

        if str(entry_name) == str(self.meta._get_absolute_path_of_entry(relative_path=self.active_entry)):
            self.update_table()
            self._update_data_cache(
                list_filenames=[new_file],
            )




def main():
    from argparse import ArgumentParser
    description = """PyXScat tool to open the GUI of the Browser"""
    usage = "pyxscat [options]"
    parser = ArgumentParser(
        usage=usage,
        description=description,
    )

    parser.add_argument(
        "-f" "--file-json",
        dest="file",
        help="Import a .json file with already stored Metadata",
        default=None,
    )

    parser.add_argument(
        "-d", "--directory",
        dest="directory",
        help="Import a root directory to search files recursively",
        default=None,
    )

    parser.add_argument(
        "-p", "--pattern",
        default="*.edf",
        dest="pattern",
        help="Use a file-matching pattern to search for data files",
    )
    options = parser.parse_args()

    _main(
        directory=options.directory,
        pattern=options.pattern,
        file_json=options.file,
    )

def _main(directory="", pattern="*.edf", file_json=""):
    app = QApplication(sys.argv)
    mw = QMainWindow()
    browser = Browser()
    mw.setCentralWidget(browser)
    mw.show()
    browser._init_browser(
        root_directory=directory,
        pattern=pattern,
        json_file=file_json,
    )    
    app.exec_()

if __name__ == "__main__":
    main()