
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

from pathlib import Path
from pyFAI.io.ponifile import PoniFile
from pyFAI import load
import os
import sys

JSON_DIR = Path(SRC_PATH).joinpath('METADATA_FILES')
JSON_DIR.mkdir(exist_ok=True)

logger = setup_logger()
def log_info(func):
    def wrapper(*args, **kwargs):
        logger.info(f'_________OPEN FUNCTION: {func.__name__}_________')
        return func(*args, **kwargs)
    return wrapper


class Browser(BrowserLayout):
    browser_index = pyqtSignal()
    poni_changed = pyqtSignal()

    def __init__(self):
        super(Browser, self).__init__()
        self._init_attributes()
        self._init_callbacks()

    def _init_attributes(self):
        self.active_entry = ''
        self.active_index = []
        self.poni = None
        self.ai = None
        self.meta = None
    
    def _init_callbacks(self):
        self.button_pick_jsonfile.clicked.connect(self._slot_jsonfile_clicked)
        self.button_pick_rootdir.clicked.connect(self._slot_rootdirectory_clicked)
        self.combobox_ponifile.currentTextChanged.connect(self._slot_poni_changed)
        self.listwidget_samples.itemClicked.connect(self._slot_active_entry_changed)
        self.table_files.itemSelectionChanged.connect(self._slot_active_index_changed)

        #########################
        # Setup dictionary callback
        #########################
        # self.combobox_setup.currentTextChanged.connect(self.cb_setup_changed)
        # self.combobox_angle.currentTextChanged.connect(self.cb_iangle_changed)
        # self.combobox_tilt_angle.currentTextChanged.connect(self.cb_tangle_changed)
        # self.combobox_normfactor.currentTextChanged.connect(self.cb_normfactor_changed)
        # self.combobox_acquisition.currentTextChanged.connect(self.cb_acquisition_changed)
        # self.button_pick_json.clicked.connect(self.pick_json_clicked)
        # self.button_metadata_update.clicked.connect(self.metadata_update_clicked)
        # self.button_metadata_save.clicked.connect(self.metadata_save_clicked)

    ######################
    ##### SETTERS ########
    ######################
    
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
        self._active_index_changed()

    @property
    def poni(self):
        return self._poni
    
    @poni.setter
    def poni(self, value):
        self._poni = value
        self._poni_instance_changed()

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
    
    @log_info
    def _slot_poni_changed(self, poni_name):
        """
        Updates the .poni parameters from a changed value of .poni filename

        Arguments:
            poni_name -- string of .poni filename
        """
        poni_filename = self.meta._get_absolute_path(relative_path=poni_name)
        self.poni = PoniFile(data=poni_filename)
        self.ai = load(self.poni)

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
        combobox = self.combobox_reffolder
        cb.clear(combobox=combobox)
        for entry in self.meta._generate_entries(relative_path=True):
            cb.insert(
                combobox=combobox,
                item=entry,
            )

    @log_info
    def _update_referencecb(self):
        combobox = self.combobox_reffolder
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

    # @log_info
    # def update_active_poni(self, poni_data):
    #     if isinstance(poni_data, (str, Path)):
    #         poni_data = Path(poni_data)
    #         if not poni_data.absolute() == poni_data:
    #             poni_data = self.meta._get_absolute_path(relative_path=poni_data)
    #         if not Path(poni_data).is_file():
    #             logger.error(f'Ponifile {poni_data} does not exists??')
    #             return
    #     elif isinstance(poni_data, PoniFile):
    #         pass
    #     else:
    #         logger.error(f'Poni_data {poni_data} (type: {type(poni_data)}) is not a valid type')
    #         return
                
    #     try:
    #         poni = PoniFile(data=poni_data)
    #     except Exception as e:
    #         logger.error(f'Poni instance could not be created using {poni_data}: {e}')
    #         return

    #     self._update_poni(poni=poni)
    #     self._update_poni_widgets()

    @log_info
    def _update_poni(self, poni):
        self._poni = poni

    @log_info
    def _update_poni_widgets(self):
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
        self.browser_index.emit()


    @log_info
    def _poni_instance_changed(self):
        if not self._poni:
            return
        self._update_poni_widgets()








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
        self.combobox_angle.addItems(texts=metadata_keys)
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










    # DIALOG METHODS
    
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