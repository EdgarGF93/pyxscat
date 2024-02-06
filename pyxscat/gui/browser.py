
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

from . import SRC_PATH
from pyxscat.gui.browserlayout import BrowserLayout
from pyxscat.logger_config import setup_logger
from pyxscat.metadata import MetadataBase
from pyxscat.gui import lineedit_methods as le
from pyxscat.gui import listwidget_methods as lt
from pyxscat.gui import combobox_methods as cb


from pathlib import Path
from pyFAI.io.ponifile import PoniFile
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
    def __init__(self):
        super(Browser, self).__init__()
        self._init_attributes()
        self._init_callbacks()

    def _init_attributes(self):
        self._meta = None
        self._active_entry = ''
        self._active_index = []        
    
    def _init_callbacks(self):
        self.button_pick_rootdir.clicked.connect(self._slot_rootdir_clicked)
        # self.button_pick_hdf5.clicked.connect(self.pick_h5file_clicked)        
        #self.combobox_h5_files.currentTextChanged.connect(self.cb_h5_changed)
        self.combobox_ponifile.currentTextChanged.connect(self._slot_poni_changed)
        self.listwidget_samples.itemClicked.connect(self._slot_active_entry_changed)




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
    ##### SLOTS
    ######################
        
    @log_info
    def _slot_rootdir_clicked(self,_):
        """
        Chain of events after pressing the folder button
        """
        self.init_browser()
    
    @log_info
    def _slot_poni_changed(self, poni_name):
        """
        Updates the .poni parameters from a changed value of .poni filename

        Arguments:
            poni_name -- string of .poni filename
        """
        self.update_active_poni(poni_data=poni_name)

    @log_info
    def _slot_active_entry_changed(self, new_entry):
        self.update_active_entry(new_entry=new_entry.text())
        
    #################################
    ## BROWSER METHODS #######
    #################################

    @log_info
    def init_browser(self):
        # Get the address of a root directory
        root_directory = self.pick_root_directory()
        if not root_directory:
            return
        
        # Parse root_directory and pattern
        root_directory = Path(root_directory)
        pattern = self.get_pattern()

        self._init_browser(
            root_directory=root_directory,
            pattern=pattern,
        )

    @log_info
    def _init_browser(self, root_directory: str = '', pattern: str = ''):
        """Instanciate the MetadataBase class and updates the widgets of the browser

        Params:
            root_directory (str) : path of the directory where to search files recursively
            pattern (str) : pattern to find data files
        """
        if not self._init_metadatabase(
            root_directory=root_directory,
            pattern=pattern,
            output_directory=JSON_DIR,
            ):
            return
        self.update_rootdir_lineedit(new_text=root_directory)
        self.update_listwidget(init=True)
        self.update_referencecb(init=True)
        self.update_ponicb(init=True)

    @log_info
    def _init_metadatabase(self, root_directory, pattern, output_directory: str = '') -> bool:
        try:
            self.meta = MetadataBase(
                directory=root_directory,
                pattern=pattern,
                init_metadata=True,
            )
            self._save_meta_file(output_directory=output_directory)
            
            return True
        except Exception as e:
            logger.error(f'Metadata base instance could not be initialized: {e}')
            return False
    
    def _save_meta_file(self, output_directory: str = ''):
        self.meta.save(output_directory=output_directory)
        self._update_recentfiles_cb()

    @log_info
    def update_rootdir_lineedit(self, new_text: str):
        lineedit = self.lineedit_root_dir
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
            list_items=self.meta.get_ponifiles(
                relative_path=True,
            ),
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
    def update_active_poni(self, poni_data):
        if isinstance(poni_data, (str, Path)):
            poni_data = Path(poni_data)
            if not poni_data.absolute() == poni_data:
                poni_data = self.meta._get_absolute_path(relative_path=poni_data)
            if not Path(poni_data).is_file():
                logger.error(f'Ponifile {poni_data} does not exists??')
                return
        elif isinstance(poni_data, PoniFile):
            pass
        else:
            logger.error(f'Poni_data {poni_data} (type: {type(poni_data)}) is not a valid type')
            return
                
        try:
            poni = PoniFile(data=poni_data)
        except Exception as e:
            logger.error(f'Poni instance could not be created using {poni_data}: {e}')
            return

        self._update_poni(poni=poni)
        self._update_poni_widgets()
        # self._update_graphs(graph_1D=True, graph_2D_q=True, graph_2D_reshape=True)

    @log_info
    def _update_poni(self, poni):
        self._active_poni = poni

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
            detector_name = self._active_poni.detector.name
        except Exception as e:
            logger.error(f"{e}: Detector name could not be retrieved from {self._active_poni}.")
            detector_name = ''

        try:
            detector_bin = self._active_poni.detector.binning
        except Exception as e:
            logger.error(f"{e}: Detector binning could not be retrieved from {self._active_poni}.")
            detector_bin = ('x','x')

        try:
            shape = self._active_poni.detector.shape
            shape = (shape[0], shape[1])
        except Exception as e:
            logger.error(f"{e}: Shape could not be retrieved from {self._active_poni}.")
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
            wave = self._active_poni.wavelength
        except Exception as e:
            logger.error(f"{e}: Wavelength could not be retrieved from {self._active_poni}.")
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
            dist = self._active_poni.dist
        except Exception as e:
            logger.error(f"{e}: Distance could not be retrieved from {self._active_poni}.")
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
            poni1 = self._active_poni.poni1
        except Exception as e:
            logger.error(f"{e}: PONI1 could not be retrieved from {self._active_poni}.")
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
            poni2 = self._active_poni.poni2
        except Exception as e:
            logger.error(f"{e}: PONI2 could not be retrieved from {self._active_poni}.")
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
            rot1 = self._active_poni.rot1
        except Exception as e:
            logger.error(f"{e}: ROT1 could not be retrieved from {self._active_poni}.")
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
            rot2 = self._active_poni.rot2
        except Exception as e:
            logger.error(f"{e}: ROT2 could not be retrieved from {self._active_poni}.")
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
            rot3 = self._active_poni.rot3
        except Exception as e:
            logger.error(f"{e}: ROT3 could not be retrieved from {self._active_poni}.")
            rot3 = 0.0

        le.substitute(
                lineedit=widget,
                new_text=rot3,
            )

    @log_info
    def pick_root_directory(self) -> Path:
        """
        Picks a folder as root directory, where the data files are searched recursively

        Returns:
            Path instance with the root directory
        """        
        # Pick the folder after pop-up browser window
        self.dialog_maindir = QFileDialog()
        get_directory = self.dialog_maindir.getExistingDirectory(self, 'Choose main directory', os.getcwd())

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
    def update_active_entry(self, new_entry):
        self._update_active_entry(new_entry=new_entry)


    @log_info
    def _update_active_entry(self, new_entry: str):
        self._active_entry =new_entry



    @log_info
    def listsamples_clicked(self, clicked_sample_name):
        """
        Chain of events after cliking on one of the item from the listwidget

        Arguments:
            clicked_sample_name -- current clicked item on the listwidget
        """        

        if not self._active_h5:
            return
        
        # Fetch the name of the integration
        clicked_sample_name = clicked_sample_name.text()
        if clicked_sample_name:
            self.active_entry = clicked_sample_name

        # Update the metadata combobox if needed
        self.check_and_update_cb_metadata(
            sample_name=clicked_sample_name,
        )

        # Get a Pandas.DataFrame to upload the table
        keys_to_display = self.combobox_metadata.currentData()
        dataframe = self._active_h5.get_metadata_dataframe(
            sample_name=clicked_sample_name,
            list_keys=keys_to_display,
        )

        # Reset and feed the table widget with default metadata keys if needed
        self.update_table(
            dataframe=dataframe,
            reset=True,
        )





def main():
    app = QApplication(sys.argv)
    mw = QMainWindow()
    browser = Browser()
    mw.setCentralWidget(browser)
    mw.show()
    app.exec_()

if __name__ == "__main__":
    main()