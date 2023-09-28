from collections import defaultdict
from pathlib import Path
from pyFAI import load
from pyFAI.io.ponifile import PoniFile
from pygix.transform import Transform
from pygix.grazing_units import TTH_DEG, TTH_RAD, Q_A, Q_NM
from os.path import getctime

from pyxscat.edf import EdfClass
from pyxscat.other.other_functions import date_prefix, float_str, get_dict_files
from pyxscat.gui import GLOBAL_PATH, LOGGER_PATH
from pyxscat.other.units import *

import functools
import h5py
import logging
import numpy as np
import pandas as pd
import random
import silx.io.commonh5 as h5c
import silx.io.h5py_utils as h5u
import silx.io.utils as utils
from silx.io import open
from silx.io.commonh5 import Group, Dataset, Node
from silx.io.h5py_utils import File

ENCODING_FORMAT = "UTF-8"

DESCRIPTION_HDF5 = "HDF5 file with Scattering methods."
BEAMLINE = "BM28-XMaS"
COMMENT_NEW_FILE = ""

NAME_H5_KEY = "name"
ROOT_DIRECTORY_KEY = "root_directory"
DATETIME_KEY = "datetime"
SAMPLE_KEY = "sample"
CLASS_KEY = "class"
INDEX_KEY = "index"
DATA_KEY = "data"
METADATA_KEY = "metadata"
FILENAME_KEY = "filename"

INCIDENT_ANGLE_KEY = 'iangle_key'
TILT_ANGLE_KEY = 'tilt_key'
ACQUISITION_KEY = 'acq_key'
NORMALIZATION_KEY = 'norm_key'

ADDRESS_METADATA_KEYS = '.'
ADDRESS_PONIFILE = '.'

PONIFILE_KEY = "ponifiles"
PONIFILE_ACTIVE_KEY = "active_ponifile"

DEFAULT_INCIDENT_ANGLE = 0.0
DEFAULT_TILT_ANGLE = 0.0

DIGITS_SAMPLE = 4
DIGITS_FILE = 4

POLARIZATION_FACTOR = 0.99
NPT_RADIAL = int(100)

DICT_SAMPLE_ORIENTATIONS = {
    (True,True) : 1,
    (True,False) : 2,
    (False,True) : 3,
    (False,False) : 4,
}

PONI_KEY_VERSION = "poni_version"
PONI_KEY_BINNING = "binning"
PONI_KEY_DISTANCE = "dist"
PONI_KEY_WAVELENGTH = "wavelength"
PONI_KEY_SHAPE1 = "shape1"
PONI_KEY_SHAPE2 = "shape2"
PONI_KEY_DETECTOR = "detector"
PONI_KEY_DETECTOR_CONFIG = "detector_config"
PONI_KEY_PIXEL1 = "pixelsize1"
PONI_KEY_PIXEL2 = "pixelsize2"
PONI_KEY_PONI1 = "poni1"
PONI_KEY_PONI2 = "poni2"
PONI_KEY_ROT1 = "rot1"
PONI_KEY_ROT2 = "rot2"
PONI_KEY_ROT3 = "rot3"

DICT_BOX_ORIENTATION = {
    'Horizontal' : 'ipbox',
    'Vertical' : 'opbox',
}

AZIMUTH_NAME = 'Azimuthal'
RADIAL_NAME = 'Radial'
HORIZONTAL_NAME = 'Horizontal'
VERTICAL_NAME = 'Vertical'

ERROR_RAW_INTEGRATION = "Failed at detect integration type."
MSG_LOGGER_INIT = "Logger was initialized."


INFO_H5_PONIFILES_DETECTED = "New ponifiles detected."
INFO_H5_NO_PONIFILES_DETECTED = "No ponifiles detected."
INFO_H5_NEW_FILES_DETECTED = "New files were detected."
INFO_H5_NEW_DICTIONARY_FILES = "Got dictionary of folders and files"
INFO_H5_FILES_UPDATED = "Finished the update of all the new files."

ERROR_MAIN_DIRECTORY = "No main directory was detected."

 # Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

if not Path(LOGGER_PATH).exists():
    Path(LOGGER_PATH).mkdir()

logger_file = Path(LOGGER_PATH).joinpath(f'pyxscat_h5_logger_{date_prefix()}.txt')
file_handler = logging.FileHandler(logger_file)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)
logger.info(MSG_LOGGER_INIT)

def log_info(func):
    def wrapper(*args, **kwargs):
        logger.info(f'We entered into function: {func.__name__}')
        return func(*args, **kwargs)
    return wrapper


class H5GIIntegrator(Transform):
    """
    Creates an HDF5 file and provides methods to read/write the file following the hierarchy of XMaS-BM28
    """

    def __init__(
        self,
        root_directory=str(),
        output_filename_h5=str(),
        input_filename_h5=str(),
    ) -> None:

        # If there is no imported .h5 file
        if not input_filename_h5:
            self.create_h5_file(
                root_directory=root_directory,
                output_h5_filename=output_filename_h5,
            )
            self.filename_h5 = output_filename_h5
        else:
            self.filename_h5 = input_filename_h5
        
        logger.info("H5Integrator instance was initialized")
        self._number_samples = 0
        # self._number_dataset = 0
        # self._number_data_images = 0
        
        logger.info(f"The filename is {self.filename_h5}.")

        # self.open_h5
        # self.close_h5
        # self._is_open = False
        # self.close_at_end = True

        # Update the ponifile path
        # self.update_group_ponifile(
        #     group_address=ADDRESS_PONIFILE,
        #     ponifile_list=ponifile_list,
        # )

        # Update the dictionary with keys
        # self.update_setup_keys(
        #     dict_keys=dict_keys_metadata,
        #     key_incident_angle=key_incident_angle,
        #     key_tilt_angle=key_tilt_angle,
        #     key_acquisition_time=key_acquisition_time,
        #     key_normalization_factor=key_normalization_factor,
        # )

        # Get attributes from Transform class (pygix module)
        super().__init__()
        logger.info("Inherited methods from pygix.transform")
        # self.update_transformQ()

        # Update rotation, orientation parameters
        # self.update_orientation(
        #     qz_parallel=qz_parallel,
        #     qr_parallel=qr_parallel,
        # )

    # @property
    # def open_h5(self):
    #     """
    #     Open the .h5 file with reading and writing permissions

    #     Parameters:
    #     None

    #     Returns:
    #     None
    #     """
    #     self._file = h5py.File(self.filename_h5, 'r+')
    #     self._is_open = True

    # @property
    # def close_h5(self):
    #     """
    #     Closes the .h5 file

    #     Parameters:
    #     None

    #     Returns:
    #     None
    #     """
    #     self._file.close()
    #     self._is_open = False


    @property
    def _open_r(self):
        """
        Opens the h5 file with reading permises
        """   
        self._file = File(self.filename_h5, 'r')

    @property
    def _open(self):
        self._open_w
        
    @property
    def _open_w(self):
        """
        Opens the h5 file with reading/writing permises
        """        
        self._file = File(self.filename_h5, 'r+')

    @property
    def _close(self):
        """
        Closes the h5 file
        """        
        self._file.close()

    def generate_all_samples(self):
        for sample in h5u.top_level_names(self.filename_h5):
            yield sample

    def check_if_open(func):
        """
        To be used as decorator, opens the .h5 file if it is closed, do not do anything if it is open

        Parameters:
        None

        Returns:
        None
        """
        pass
        # @functools.wraps(func)
        # def wrapper(self, *args, **kwargs):

        #     if self._is_open:
        #         self.close_at_end = False
        #     else:
        #         self.open_h5
        #         self.close_at_end = True

        #     res = func(self, *args, **kwargs)

        #     if self.close_at_end:
        #         self.close_h5

        #     return res
        # return wrapper

    @log_info
    def create_h5_file(
        self,
        root_directory=str(),
        output_h5_filename=str(),
        ):
        """
        Creates (overwrites if needed) an .h5 file with some initial attributes

        Keyword Arguments:
            root_directory -- string to be saved as attribute (default: {str()})
            output_h5_filename -- string to be saved as attribute (default: {str()})
        """        
        try:
            self._file = File(output_h5_filename, 'w')
            self._file.close()
            self.filename_h5 = output_h5_filename
            logger.info(f"The file {output_h5_filename} was created ")
        except Exception as e:
            logger.info(f"{e}: The file {output_h5_filename} could not be created. Return.")
            return

        self.write_attrs(
            dict_attrs={
                NAME_H5_KEY : Path(output_h5_filename).name,
                ROOT_DIRECTORY_KEY : root_directory,
                DATETIME_KEY : date_prefix(),
            }
        )

    @log_info
    def write_attrs(self, dict_attrs=dict(), address='.'):
        """
        Write the key-values from a dictionary as attributes at the root level of h5 file

        Keyword Arguments:
            dict_attrs -- dictionary with root attribute information (default: {dict()})
            address -- path of the Group inside the h5 File (default: {'.'})
        """        
        self._open_w
        for k, v in dict_attrs.items():
            self.write_attr(
                key=k,
                value=v,
                address=address,
            )
        self._close

    @log_info
    def write_attr(self, key=str(), value=str(), address='/'):
        """
        Write a key-value attribute into a specific h5 address

        Keyword Arguments:
            key -- name of the attribute (default: {str()})
            value -- value of the attribute (default: {str()})
            address -- address of Group in the h5 file (default: {'/'})
        """        
        # Encode the string
        value = value.encode(ENCODING_FORMAT)     

        # Try to write directly
        try:
            self._file[address].attrs[key] = value
            logger.info(f"{e}: The key-value {key}:{value} was written.")
            return
        except Exception as e:
            logger.info(f"{e}: The key-value {key}:{value} could not be written. Trying to open the h5 File...")
        
        # Try to open the File and write then
        try:
            self._open_w
            self._file[address].attrs[key] = value
            logger.info(f"{e}: The key-value {key}:{value} was written.")
        except Exception as e:
            logger.info(f"{e}: The key-value {key}:{value} could not be written anyway.")
        finally:
            self._close

    @log_info
    def update_metadata_keys(self, dict_metadata_keys=dict(), iangle_key=str(), tangle_key=str(), norm_factor=str(), acq_key=str()):
        """
        Write important metadata keys as attributes at the root level of the .h5 File

        Keyword Arguments:
            dict_metadata_keys -- dictionary with metadata keys (default: {dict()})
            iangle_key -- name of the motor for incident angle (default: {str()})
            tangle_key -- name of the motor for tilt angle (default: {str()})
            norm_factor -- name of the counter for normalization factor (default: {str()})
            acq_key -- name of the counter for the acquisition time (default: {str()})
        """        
        if dict_metadata_keys:
            pass
        else:
            dict_metadata_keys = {
                INCIDENT_ANGLE_KEY : iangle_key,
                TILT_ANGLE_KEY : tangle_key,
                NORMALIZATION_KEY : norm_factor,
                ACQUISITION_KEY : acq_key,
            }

        # Write the dictionary as attributes
        self.write_attrs(
            dict_attrs=dict_metadata_keys,
        )

    @log_info
    def get_root_directory(self) -> Path:
        """
        Returns the root_directory stored as attribute at the root level during the creation of the .h5 File

        Returns:
            Path with the root directory where data files are searched
        """        
        root_dir = Path(self.get_attr(attr_key=ROOT_DIRECTORY_KEY))
        return root_dir

    @log_info
    def get_name(self) -> str:
        """
        Returns the name stored as attribute at the root level during the creation of the .h5 File

        Returns:
            name of the .h5 file, without the directories, with the extension
        """
        name = self.get_attr(attr_key=NAME_H5_KEY)
        return name

    @log_info
    def get_attr(self, attr_key=str(), group_address='.') -> str:
        """
        Returns the attribute value from a specific Group

        Keyword Arguments:
            attr_key -- name of the attribute (default: {str()})
            group_address -- address of the H5 Group (default: {'.'})

        Returns:
            value of the attribute
        """
        try:
            attr = self._file[group_address].attrs[attr_key]
        except Exception as e:
            attr = None
            logger.info(f"{e}: attribute {attr} could not be read. Trying to open the file...")

        # Try to access after opening the File
        if not attr:
            try:
                self._open_r
                attr = self._file[group_address].attrs[attr_key]
                self._close
            except Exception as e:
                logger.info(f"{e}: attribute {attr} could not be read anyway.")
                return
        
        # Retrieve decoded string
        if isinstance(attr, bytes):
            attr = bytes.decode(attr, encoding=ENCODING_FORMAT)
        return attr

    @log_info
    def get_dict_attrs(self, group_address='.') -> dict:
        """
        Returns a dictionary with the key-value attributes of a Group

        Keyword Arguments:
            group_address -- address of the Group inside the H5 File (default: {'.'})

        Returns:
            dictionary with the key-value attributes
        """
        try:
            dict_attrs = {k:v for k,v in self._file[group_address].attrs.items()}
            return dict_attrs
        except Exception as e:
            logger.info(f"{e}: Attributes could not be retrieved. Trying to open the File...")
        
        try:
            self._open_r
            dict_attrs = {k:v for k,v in self._file[group_address].attrs.items()}
            self._close
            return dict_attrs
        except Exception as e:
            logger.info(f"{e}: Attributes could not be retrieved anyway.")
        return

    @log_info
    def get_iangle_key(self):
        """
        Returns the string of the stored key for incident angle
        """
        iangle_key = self.get_attr(attr_key=INCIDENT_ANGLE_KEY)
        return iangle_key

    @log_info
    def get_tiltangle_key(self):
        """
        Returns the string of the stored key for tilt angle
        """
        tangle_key = self.get_attr(attr_key=TILT_ANGLE_KEY)
        return tangle_key

    @log_info
    def get_norm_key(self):
        """
        Returns the string of the stored key for normalization factor
        """
        norm_key = self.get_attr(attr_key=NORMALIZATION_KEY)
        return norm_key

    @log_info
    def get_acquisition_key(self):
        """
        Returns the string of the stored key for acquisition time
        """
        acq_key = self.get_attr(attr_key=ACQUISITION_KEY)
        return acq_key

    @log_info
    def get_metadata_dict(self) -> dict:
        """
        Returns a dictionary with the key-value metadata information

        Keyword Arguments:
            group_address -- address of the Group inside the H5 File (default: {'.'})

        Returns:
            dictionary with the metadata key-values
        """
        dict_attrs = self.get_dict_attrs(group_address=ADDRESS_METADATA_KEYS)
        dict_metadata = {}
        dict_metadata[INCIDENT_ANGLE_KEY] = dict_attrs[INCIDENT_ANGLE_KEY]
        dict_metadata[TILT_ANGLE_KEY] = dict_attrs[TILT_ANGLE_KEY]
        dict_metadata[NORMALIZATION_KEY] = dict_attrs[NORMALIZATION_KEY]
        dict_metadata[ACQUISITION_KEY] = dict_attrs[ACQUISITION_KEY]
        return dict_metadata

    #########################################################
    ######### METHODS FOR KEY METADATA ######################
    #########################################################

    @log_info
    def get_dataset_acquisition_time(self, folder_name=str()) -> np.array:
        """
        Returns the numpy array which is the dataset of acquistion times associated with the files of a folder (Group)

        Parameters:
        folder_name(str) : name of the folder(Group) in the first hierarchical level of h5 file

        Returns:
        np.array : dataset of acquisition times of every file inside the Group
        """
        key_acq = self.get_acquisition_key()
        try:
            dataset = self.get_metadata_dataset(
                group_address=folder_name,
                key_metadata=key_acq,
            )
        except:
            dataset = None
        return dataset

    @log_info
    def get_dataset_incident_angle(self, folder_name=str()) -> np.array:
        """
        Returns the numpy array which is the dataset of incident angles associated with the files of a folder (Group)

        Parameters:
        folder_name(str) : name of the folder(Group) in the first hierarchical level of h5 file

        Returns:
        np.array : dataset of incident angles of every file inside the Group
        """
        key_iangle = self.get_iangle_key()
        try:
            dataset = self.get_metadata_dataset(
                group_address=folder_name,
                key_metadata=key_iangle,
            )
        except:
            dataset = None
        return dataset

    @log_info
    def get_dataset_tilt_angle(self, folder_name=str()) -> np.array:
        """
        Returns the numpy array which is the dataset of tilt angles associated with the files of a folder (Group)

        Parameters:
        folder_name(str) : name of the folder(Group) in the first hierarchical level of h5 file

        Returns:
        np.array : dataset of tilt angles of every file inside the Group
        """
        key_tangle = self.get_tiltangle_key()
        try:
            dataset = self.get_metadata_dataset(
                group_address=folder_name,
                key_metadata=key_tangle,
            )
        except:
            dataset = None
        return dataset

    @log_info
    def get_dataset_norm_factor(self, folder_name=str()) -> np.array:
        """
        Returns the numpy array which is the dataset of normalization factors associated with the files of a folder (Group)

        Parameters:
        folder_name(str) : name of the folder(Group) in the first hierarchical level of h5 file

        Returns:
        np.array : dataset of normalization factors of every file inside the Group
        """
        key_norm = self.get_norm_key()
        try:
            dataset = self.get_metadata_dataset(
                group_address=folder_name,
                key_metadata=key_norm,
            )
        except:
            dataset = None
        return dataset

    @log_info
    def get_acquisition_time(self, folder_name=str(), index_list=int()) -> float:
        """
        Returns the acquisition time of a file or the average from a list of files (index)

        Parameters:
        folder_name(str) : name of the folder(Group) in the first hierarchical level of h5 file
        index_list(list, int) : integer or list of integers which are the index of the files inside the group

        Returns
        float : the acquisition time of one file or the average of different from the same Group
        """
        dataset = self.get_dataset_acquisition_time(
            folder_name=folder_name,
        )

        if dataset:
            if isinstance(index_list, int):
                index_list = [index_list]
            acq = np.mean(
                np.array(
                    [dataset[index] for index in index_list]
                )
            )
        else:
            logger.info("Failed while getting acquisition time.")
            acq = 1.0
        logger.info(f"Got acquistion time: {acq}")
        return acq

    @log_info
    def get_incident_angle(self, folder_name=str(), index_list=int()) -> float:
        """
        Returns the incident angle of a file or the average from a list of files (index)

        Parameters:
        folder_name(str) : name of the folder(Group) in the first hierarchical level of h5 file
        index_list(list, int) : integer or list of integers which are the index of the files inside the group

        Returns
        float : the incident angle of one file or the average of different from the same Group
        """
        dataset = self.get_dataset_incident_angle(
            folder_name=folder_name,
        )

        if dataset:
            if isinstance(index_list, int):
                index_list = [index_list]
            iangle = np.mean(
                np.array(
                    [dataset[index] for index in index_list]
                )
            )
        else:
            logger.info("Failed while getting incident angle.")
            iangle = 0.0
        logger.info(f"Got incident angle: {iangle}")
        return iangle

    @log_info
    def get_tilt_angle(self, folder_name=str(), index_list=int()) -> float:
        """
        Returns the tit angle of a file or the average from a list of files (index)

        Parameters:
        folder_name(str) : name of the folder(Group) in the first hierarchical level of h5 file
        index_list(list, int) : integer or list of integers which are the index of the files inside the group

        Returns
        float : the tilt angle of one file or the average of different from the same Group
        """
        dataset = self.get_dataset_tilt_angle(
            folder_name=folder_name,
        )

        if dataset:
            if isinstance(index_list, int):
                index_list = [index_list]
            tilt = np.mean(
                np.array(
                    [dataset[index] for index in index_list]
                )
            )
        else:
            logger.info("Failed while getting tilt angle.")
            tilt = 0.0

        logger.info(f"Got tilt angle: {tilt}")
        return tilt

    @log_info
    def get_norm_factor(self, folder_name=str(), index_list=int()) -> float:
        """
        Returns the normalization factor of a file or the average from a list of files (index)

        Parameters:
        folder_name(str) : name of the folder(Group) in the first hierarchical level of h5 file
        index_list(list, int) : integer or list of integers which are the index of the files inside the group

        Returns
        float : the normalization factor of one file or the average of different from the same Group
        """
        dataset = self.get_dataset_norm_factor(
            folder_name=folder_name,
        )

        if dataset:
            if isinstance(index_list, int):
                index_list = [index_list]
            norm_factor = np.mean(
                np.array(
                    [dataset[index] for index in index_list]
                )
            )

            # NORM FACTOR CANNOT BE 0.0
            if norm_factor == 0.0:
                logger.info("Extracted norm factor is 0.0. Return 1.0.")
                norm_factor = 1.0

        else:
            logger.info("Failed while getting norm factor.")
            norm_factor = 1.0

        logger.info(f"Got norm factor: {norm_factor}")
        return norm_factor


    #########################################################
    ######### METHODS FOR PONIFILES ######################
    #########################################################

    @log_info
    def search_ponifiles(self) -> list:
        """
        Searches for .poni files in the root directory

        Returns:
            list of .poni files recursively in the root directory
        """        
        
        root_directory = self.get_root_directory()
        if not root_directory:
            return
        searched_ponifiles = root_directory.rglob("*.poni")
        searched_ponifiles = [str(file) for file in searched_ponifiles]
        searched_ponifiles.sort()
        return searched_ponifiles

    @log_info
    def update_ponifiles(self, group_address='.', ponifile_list=list(), search=False):
        """
        Creates/updates the dataset of ponifiles at the first level of hierarchy

        Parameters:
        ponifile_list(list) : string or list of strings for the ponifiles associated with the current experiment

        Returns:
        None
        """
        # Opens the h5 File
        self._open_w

        # Creates the dataset for ponifiles if needed
        if not self._file[group_address].__contains__(PONIFILE_KEY):
            self._file[group_address].create_dataset(
                PONIFILE_KEY, 
                data=np.array([str().encode()]), 
                # compression="gzip", 
                # chunks=True, 
                maxshape=(None,),
                # dtype=h5py.string_dtype(encoding='utf-8'),
                dtype=h5py.string_dtype(),
            )
            logger.info("Ponifile dataset was created.")

        # Creates the dataset for active ponifile if needed
        if not self._file[group_address].__contains__(PONIFILE_ACTIVE_KEY):
            self._file[group_address].create_dataset(
                PONIFILE_ACTIVE_KEY, 
                data=np.array([str().encode()]), 
                # compression="gzip", 
                # chunks=True, 
                maxshape=(None,),
                # dtype=h5py.string_dtype(encoding='utf-8'),
                dtype=h5py.string_dtype(),
            )
            logger.info("Active_ponifile dataset was created.")

        # Searches if requested
        if search:
            searched_ponifiles = self.search_ponifiles()
            ponifile_list += searched_ponifiles

        if not ponifile_list:
            logger.info("No ponifiles to be updated. Return.")
            return

        # Make a list if there is only one item
        if isinstance(ponifile_list, str):
            ponifile_list = [ponifile_list]

        # Take only the new files
        stored_ponifiles = list(self.generate_ponifiles())
        new_ponifiles = [file for file in ponifile_list if file not in stored_ponifiles]

        # Return if no new ponifiles
        if not new_ponifiles:
            logger.info(f"No new ponifiles to append.")
            return

        # Append the new .poni files
        for ponifile in new_ponifiles:
            dataset = self._file[group_address][PONIFILE_KEY]
            try:
                # Encode the string
                ponifile = str(ponifile).encode(ENCODING_FORMAT)
                # Append the encoded string into the dataset and enlarge
                ind = dataset.len()
                dataset[ind - 1] = ponifile
                dataset.resize((ind + 1,))
                logger.info(f"Ponifile {ponifile} was appended to dataset.")
            except:
                logger.info(f"Ponifile {ponifile} could not be updated.")

        # Close the h5
        self._close

    @log_info
    def activate_ponifile(self, poni_filename=str()) -> None:
        """
        Updates the dataset with the active ponifile.

        Keyword Arguments:
            poni_filename -- full path of the ponifile that will be activated (default: {str()})
        """        
        if not poni_filename:
            return
        
        # Open the h5 File
        self._open_w

        # Proceed only if the requested ponifiles is already stored
        stored_ponifiles = list(self.generate_ponifiles())
        if poni_filename not in stored_ponifiles:
            logger.info(f"Ponifile {poni_filename} is not stored in the .h5")
            return

        try:
            poni_filename = str(poni_filename).encode(ENCODING_FORMAT)
            self._file[PONIFILE_ACTIVE_KEY][0] = poni_filename
            logger.info(f"Ponifile {poni_filename} activated successfully.")
        except Exception as e:
            logger.info(f"{e}: Ponifile {poni_filename} could not be activated.")

        # Close the h5 file
        self._close

        # Update the GrazingGeometry instance
        self.update_grazinggeometry()

    @log_info
    def get_active_ponifile(self) -> Path:
        """
        Returns the active ponifile string from the dataset at the first level of hierarchy

        Returns:
            Path of the active ponifile
        """        
        try:
            ponifile_active = self._file[PONIFILE_ACTIVE_KEY][()][0]
        except Exception as e:
            logger.info(f"{e}: active ponifile could not be retrieved. Trying to open the file...")
            ponifile_active =None
        
        # Try after opening the h5 File
        if ponifile_active is None:
            try:
                self._open_r
                ponifile_active = self._file[PONIFILE_ACTIVE_KEY][()][0]
                self._close
            except Exception as e:
                logger.info(f"{e}: active ponifile could not be retrieved anyway.")
                return
        
        # Decode if necessary
        if isinstance(ponifile_active, bytes):
            ponifile_active = bytes.decode(ponifile_active, encoding=ENCODING_FORMAT)
        
        # Use Path instance
        ponifile_active = Path(ponifile_active)
        return ponifile_active

    @log_info
    def update_ponifile_parameters(self, dict_poni=dict()) -> None:
        """
        Changes manually the functional poni parameters of pygix
        """
        new_poni = PoniFile(data=dict_poni)
        self._init_from_poni(new_poni)

    @log_info
    def generate_ponifiles(self, decoded=True) -> str:
        """
        Yields the names of ponifiles stored in the Ponifile Group, at the first level of .h5 file

        Parameters:
        None

        Yields:
        str : str with the address of the stored .poni files
        """
        try:
            dataset_ponifile = self._file[PONIFILE_KEY][()]
        except Exception as e:
            dataset_ponifile = None
            logger.info(f"{e}: Dataset ponifiles could not be accessed. Trying to open the file...")
        
        # Try after opening the file
        if dataset_ponifile is None:
            try:
                self._open_r
                dataset_ponifile = self._file[PONIFILE_KEY][()]
                self._close
            except Exception as e:
                logger.info(f"{e}: Dataset ponifiles could not be accessed anyway.")
                return

        # Generate data
        for data in dataset_ponifile:
            if decoded:
                data = bytes.decode(data, encoding=ENCODING_FORMAT)
            yield data

    #########################################################
    ######### PYGIX CONNECTIONS ######################
    #########################################################

    @log_info
    def update_grazinggeometry(self) -> None:
        """
        If there is an active ponifile, inherits the methods from Transform class (pygix module)
        """        
        # Fetch the active ponifile
        ponifile_active = str(self.get_active_ponifile())

        if not ponifile_active:
            logger.info(f"No active ponifile. GrazingGeometry was not updated")
            return

        # Load the ponifile        
        try:
            self.load(ponifile_active)
            logger.info("Loaded poni file")
        except Exception as e:
            logger.info(f"{e}: Ponifile could not be loaded to GrazingGeometry")
        
        # Update default incident and tilt angles
        try:
            self.update_incident_tilt_angle(
                incident_angle=DEFAULT_INCIDENT_ANGLE,
                tilt_angle=DEFAULT_TILT_ANGLE,
            )
        except Exception as e:
            logger.info(f"{e}: angles could not be updated.")

    @log_info
    def update_incident_tilt_angle(self, incident_angle=0.0, tilt_angle=0.0):
        """
        Update the incident and tilt angles inherited from GrazingGeometry

        Keyword Arguments:
            incident_angle -- (default: {0.0})
            tilt_angle --  (default: {0.0})
        """        
        # Incident angle
        try:
            self.set_incident_angle(
                incident_angle=incident_angle,
            )
            logger.info(f"Incident angle set at {incident_angle}")
        except Exception as e:
            logger.info(f"{e}: Incident angle could not be updated.")

        # Tilt angle
        try:
            self.set_tilt_angle(
                tilt_angle=tilt_angle,
            )
            logger.info(f"Tilt angle set at {tilt_angle}")
        except Exception as e:
            logger.info(f"{e}: Tilt angle could not be updated.")

    # @log_info
    # def update_qz(self, qz_parallel=True):
    #     self._qz_parallel = qz_parallel
    #     logger.info(f"qz parallel is {qz_parallel}")
    #     try:
    #         self.set_sample_orientation(
    #             sample_orientation=DICT_SAMPLE_ORIENTATIONS[(self._qz_parallel, self._qr_parallel)]
    #         )
    #         logger.info(f"The sample orientation (pygix) is set at {DICT_SAMPLE_ORIENTATIONS[(self._qz_parallel, self._qr_parallel)]}")
    #     except:
    #         pass

    # @log_info
    # def update_qr(self, qr_parallel=True):
    #     self._qr_parallel = qr_parallel
    #     logger.info(f"qz parallel is {qr_parallel}")
    #     try:
    #         self.set_sample_orientation(
    #             sample_orientation=DICT_SAMPLE_ORIENTATIONS[(self._qz_parallel, self._qr_parallel)]
    #         )
    #         logger.info(f"The sample orientation (pygix) is set at {DICT_SAMPLE_ORIENTATIONS[(self._qz_parallel, self._qr_parallel)]}")
    #     except:
    #         pass 

    @log_info
    def update_orientation(self, qz_parallel=True, qr_parallel=True) -> None:
        """
        Updates two parameters to define the rotation of the detector and the orientation of the sample axis
        Pygix defined a sample orientation upon 1-4 values

        Keyword Arguments:
            qz_parallel -- inversion of the qz axis (default: {True})
            qr_parallel -- inversion of the qr axis (default: {True})
        """
        try:
            sample_orientation = DICT_SAMPLE_ORIENTATIONS[(qz_parallel, qr_parallel)]
            self.set_sample_orientation(
                sample_orientation=sample_orientation,
            )
            logger.info(f"The sample orientation (pygix) is set at {sample_orientation}.")
        except Exception as e:
            logger.info(f"The sample orientation (pygix) could not be updated.")

    #####################################
    ###### HDF5 METHODS #################
    #####################################

    @log_info
    def new_sample(self, folder_index=int(), name=str(), **kwargs):
        """
        Creates a new folder (Group) at the first level of hierarchy in the h5 file

        Keyword Arguments:
            folder_index -- associated index with the new folder (default: {int()})
            name -- name of the new folder (Group) (default: {str()})
        """
        self._open_w

        # If not index, append to the end
        if not folder_index:
            folder_index = self._number_samples
        
        # Check if the sample does exist
        if not self.contains_group(
            folder_name=name,
            ):
            logger.info(f"The folder {name} already exists.")
            self._close
            return
        
        # Create new Group
        self._file.create_group(name)
        logger.info(f"The folder {name} was successfully created.")   

        # Write some attributes     
        dict_init_sample = {
            CLASS_KEY : SAMPLE_KEY,
            INDEX_KEY : int(folder_index),
            DATETIME_KEY : date_prefix(),
            NAME_H5_KEY : name,
        }
        self.write_attrs(
            dict_attrs=dict_init_sample,
            address=name,
        )
        for k,v in kwargs.items():
            self.write_attr(key=k, value=v)

        # Increase the number of samples
        self._number_samples += 1

    @log_info
    def contains_group(self, folder_name=str(), group_address='.') -> bool:
        """
        Checks if the folder already exist in a specific address

        Keyword Arguments:
            folder_name -- name of the new folder (Group) (default: {str()})
            group_address -- address of the Group inside the H5 file (default: {str()})

        Returns:
            exists (True) or not (False)
        """
        try:
            is_inside = self._file.__contains__(str(folder_name))
            return is_inside
        except Exception as e:
            logger.info(f"{e}")
        
        try:
            self._open_r
            is_inside = self._file.__contains__(str(folder_name)):
            self._close
            return is_inside
        except Exception as e:
            logger.info(f"{e}")

    @log_info
    def append_to_dataset(self, folder_name=str(), dataset_name='Data', new_data=np.array([])) -> None:
        """
        Append new data to 'Data' dataset, inside a specific folder

        Keyword Arguments:
            folder_name -- name of the new folder (Group) (default: {str()})
            dataset_name -- 'Data' is the name of the dataset where the 2D maps or just the addresses of the files are stored (default: {'Data'})
            new_data -- list of data to be iterated and appended in the dataset (default: {np.array([])})
        """
        # Open the File
        self._open_w
        
        # Get the current shape of the dataset
        initial_shape = np.array(self._file[folder_name][dataset_name].shape)
        expanded_shape = np.copy(initial_shape)
        num_files = initial_shape[0]

        # How many new layers should we add
        new_layers = new_data.shape[0]
        expanded_shape[0] += new_layers
        expanded_shape = tuple(expanded_shape)
        
        #Resizing
        try:
            self._file[folder_name][dataset_name].resize((expanded_shape))
            logger.info(f"Shape of dataset reseted from {tuple(initial_shape)} to {expanded_shape}")
        except Exception as e:
            logger.info(f"{e} Error during reshaping the dataset {dataset_name} from {tuple(initial_shape)} to {expanded_shape}")

        # Appending
        for ind in range(new_layers):
            try:
                self._file[folder_name][dataset_name][num_files + ind] = new_data[ind]
                logger.info(f"Appended data with index {ind} successfully.")
            except Exception as e:
                logger.info(f"{e}: Error while appending {new_data[ind]}.")

        # Close
        self._close

    @log_info
    def update_folder_from_files(self, folder_name=str(), filename_list=list(), get_2D_array=True) -> None:
        """
        Creates or updates a folder (Group) with data and metadata from a list of files

        Keyword Arguments:
            folder_name -- name of the folder (Group) where the data/metadata will be stored (default: {str()})
            filename_list -- list of path filenames where the data/metadata will be extracted (default: {list()})
            get_2D_array -- yields a packed array with the 2D maps if True, yields a packed array with the encoded filenames if False (default: {True})
        """


        # Create the group if needed
        self.new_sample(
            name=folder_name,
        )

        # Get the packed data and metadata for every filename
        merged_data, merged_metadata = self.get_merged_data_and_metadata(
            filenames=filename_list, 
            get_2D_array=get_2D_array,
        )  

        # Create or update DATA dataset
        if not self._file[folder_name].__contains__('Data'):
            self._file[folder_name].create_dataset(
                'Data', 
                data=merged_data, 
                chunks=True, 
                maxshape=(None, None, None),
                # dtype=h5py.string_dtype(encoding='utf-8'),
            )
            logger.info(f"Data dataset in {folder_name} group created.")
            logger.info(f"Added in {folder_name}-Data shape: {merged_data.shape}")
        else:
            logger.info(f"Data dataset in {folder_name} group already existed. Go to append.")
            self.append_to_dataset(folder_name=folder_name, new_data=merged_data)


        # Create or update METADATA group with datasets
        if not self._file[folder_name].__contains__('Metadata'):
            self._file[folder_name].create_group('Metadata')
            logger.info(f"Metadata group in {folder_name} group created.")
        else:
            logger.info(f"Metadata group in {folder_name} group already existed. Continue.")

        for key,value in merged_metadata.items():
            # Value is a list here! Convert to np.array
            value = np.array(value)

            # Creates dataset for the key
            if not self._file[folder_name]['Metadata'].__contains__(key):

                # Try to create dataset with the standard format (floats)
                try:
                    self._file[folder_name]['Metadata'].create_dataset(key, data=np.array(value), chunks=True, maxshape=(None,))
                    logger.info(f"Dataset {key} in {folder_name}-Metadata was created.")
                    continue
                except:
                    logger.info(f"Dataset could not be created with the standard format for the key {key}, value {value}.")

                # If it did not work, try to create dataset encoding the dataset as bytes format
                try:
                    logger.info("Trying to create dataset with encoded data.")
                    bytes_array = np.array([str(item).encode() for item in value])
                    self._file[folder_name]['Metadata'].create_dataset(key, data=bytes_array, chunks=True, maxshape=(None,))
                    logger.info(f"Dataset {key} in {folder_name}-Metadata was created. Encoding worked.")
                    continue
                except:
                    logger.info(f"Dataset could not be created with the encoded format for the key {key}, value {value}.")

            # Appends dataset for the key if the dataset already existed
            else:
                subfolder = f"{folder_name}/{'Metadata'}"
                # Try to append dataset with the standard format (floats)

                try:
                    self.append_to_dataset(folder_name=subfolder, new_data=value, dataset_name=key)
                    logger.info(f"Dataset {key} in {subfolder} was appended.")
                    continue
                except:
                    logger.info(f"Dataset could not be appended with the standard format for the key {key}, value {value}.")

                # If it did not work, try to append dataset encoding the dataset as bytes format
                try:
                    logger.info("Trying to append dataset with encoded data.")
                    bytes_array = np.array([str(item).encode() for item in value])
                    self.append_to_dataset(folder_name=subfolder, new_data=bytes_array, dataset_name=key)
                    logger.info(f"Dataset {key} in {folder_name}-Metadata was appended. Encoding worked.")
                    continue
                except:
                    logger.info(f"Dataset could not be appended with the encoded format for the key {key}, value {value}.")
                    
    @log_info
    def get_merged_data_and_metadata(self, filenames=list(), get_2D_array=True):
        """
        Use FabIO module to get the data (arrays) and metadata from 2D detector patterns
        If not get_2D_array, it yields the encoded name of the file, not the real 2D array

        Keyword Arguments:
            filenames -- list of strings with the full address of the data files (default: {list()})
            get_2D_array -- yields a packed array with the 2D maps if True, yields a packed array with the encoded filenames if False (default: {True})

        Returns:
            _description_
        """
        # Init dataset and header
        merged_dataset = np.array([])
        merged_header = defaultdict(list)            
        
        for index_file, (data, header) in enumerate(self.generator_fabio_data_header(filenames, get_2D_array)):
            # Pack data
            try:
                if index_file == 0:
                    merged_dataset = np.array([data])
                else:
                    merged_dataset = np.concatenate((merged_dataset, [data]), axis=0)
            except Exception as e:
                logger.info(f"{e}: Error while packing data at {index_file}")
            
            # Pack metadata
            for key,value in header.items():
                try:
                    value = float_str(value)
                    merged_header[key].append(value)
                except Exception as e:
                    logger.info(f"{e}: Error while packing metadata at key: {key}, value {value}")
        return merged_dataset, merged_header

    @log_info
    def generator_fabio_data_header(self, filenames=[], get_2D_array=True):
        """
        Use FabIO module to generate the data and metadata from a list of files
        If not get_2D_array, it yields the encoded name of the file, not the real 2D array

        Keyword Arguments:
            filenames -- list of strings with the full address of the data files (default: {[]})
            get_2D_array -- yields a packed array with the 2D maps if True, yields a packed array with the encoded filenames if False (default: {True})

        Yields:
            np.array : 2D map or encoded filename
            dict : header dictionary from FabIO
        """
        for file in filenames:
            # Open a EdfClass instance
            try:
                edf = EdfClass(file)
            except Exception as e:
                logger.info(f"{e}: EdfClass instance could not be created.")
                continue

            # Yield data or data addresses and header
            try:
                if get_2D_array:
                    data, header = edf.get_data(), edf.get_header()
                else:
                    data, header = np.array(([[str(file).encode()]])), edf.get_header()
            except Exception as e:
                logger.info(f"{e}: Error while fabio handling at {file}")
                data, header = None, None
            yield data, header

    @check_if_open
    def generator_samples(self) -> str:
        """
        Yields the folder_name of every data Group at the first level of hierarchy

        Parameters:
        None

        Yields:
        str : folder_name of the Group
        """
        try:
            list_samples = [item for item in self._file.keys() if item[CLASS_KEY] == SAMPLE_KEY]
        except Exception as e:
            list_samples = None
            logger.info(f"{e}: List of samples could not be retrieved. Trying to open the file...")
        
        # Try to open the h5 File
        if list_samples is None:
            try:
                self._open_r
                list_samples = [item for item in self._file.keys() if item[CLASS_KEY] == SAMPLE_KEY]
                self._close
            except Exception as e:
                logger.info(f"{e}: List of samples could not be retrieved anyway.")
                return
        
        # Generate the name of the samples
        for sample in list_samples:
            yield sample

    
        # self.open_h5
        # for sample_name in self._file.keys():
        #     try:
        #         if not isinstance(self._file[sample_name], h5py.Group):
        #             continue
        #         elif sample_name == 'Metadata':
        #             continue
        #         else:
        #             yield sample_name
        #     except:
        #         logger.info(f"Error while generating folder: {sample_name}")

    @check_if_open
    def generator_all_files(self, yield_decode=True) -> str:
        """
        Yields the names of every file stored in the .h5 file

        Parameters:
        None

        Yields:
        str : fullpath of stored filenames
        """
        for folder in self.generator_samples():
            for file in self.generator_filenames_in_folder(folder_name=folder, yield_decode=yield_decode):
                yield file

    @check_if_open
    def generator_folder_group(self) -> h5py.Group:
        """
        Yields every Group at the first level of hierarchy of the h5 file

        Parameters:
        None

        Yields:
        h5py.Group
        """
        for sample_name in np.array([item for item in self._file.keys() if 'Metadata' not in item]):
            yield self._file[sample_name]

    @log_info
    @check_if_open
    def number_samples(self) -> float:
        """
        Returns the number of samples (folders) already in the h5 file

        Parameters:
        None

        Returns:
        float : number of folders
        """
        n_samples = len(list(self._file.keys()))
        logger.info(f"Number of sample: {n_samples}")
        return n_samples

    @log_info
    @check_if_open
    def number_files_in_sample(self, sample_name=str()):
        """
        Returns the number of files inside a sample (folder)

        Parameters:
        sample_name(str) : name of the folder (Group) at the first level of hierarchy

        Returns:
        float : number of files in the folder
        """
        n_files = len(list(self._file[sample_name].keys()))
        logger.info(f"There are {n_files} in {sample_name}")
        return n_files


    ##################################################
    ############# SAMPLES/FILES METHODS ##############
    ##################################################

    @log_info
    @check_if_open
    def search_and_update_datafiles(self, pattern='*.edf'):
        """
        Run the search engine, get new files and folders taken the pattern and stored main directory, and update the storage

        Parameters:
        pattern(str) : wildcards used in method Path.rglob to search files recursively

        Returns:
        None
        """
        # Get the list of new files and new folders
        new_files = self.search_new_files_folders(
            pattern=pattern,
        )

        # If there are new detected files, updates the memory of the h5 file
        if new_files:
            self.update_datafiles(
                new_files=new_files,
            )

    @log_info
    @check_if_open
    def search_new_files_folders(self, pattern='*.edf') -> list:
        """
        Search new files inside the main directory, according to the pattern and returns both lists of new files and new folders

        Parameters:
        None

        Returns:
        list : list of strings with the full directions of the new detected filenames
        #list : if there are new detected filenames, list of strings with the new detected folders (could be empty)
        """
        main_directory = Path(self.get_root_directory())
        if main_directory and main_directory.exists():

            # Global search according to pattern
            set_searched_files = set(str(item).encode() for item in main_directory.rglob(pattern) if str(item.parent) != str(main_directory))

            # Filter for new files
            set_stored_files = set(self.generator_all_files(yield_decode=False))
            new_files = [bytes.decode(item) for item in set_searched_files.difference(set_stored_files)]
            logger.info(f"{len(new_files)} {INFO_H5_NEW_FILES_DETECTED}")

            if new_files:
                new_files.sort()

            return new_files
        else:
            logger.info(ERROR_MAIN_DIRECTORY)

    @log_info
    def update_datafiles(self, new_files=list(), search=False):
        """
        Updates the h5 file with new Groups associated with the folders and new Data/Metadata associated with the files
        This method can be used with any new file list,
        In case of new folders, they will be created
        In case of new files in existing folders, the new data/metadata will be appended

        Parameters:
        list_files(list) : list of strings with the full path of new files to be stored in the h5 file

        Returns:
        None
        """
        # Get a dictionary from the list of files
        dict_new_files = get_dict_files(
            list_files=new_files,
        )
        logger.info(INFO_H5_NEW_DICTIONARY_FILES)

        # Store in the .h5 file by folder and its own list of files
        for folder, file_list in dict_new_files.items():
            folder_name = str(Path(folder).relative_to(self.get_root_directory())) 
            self.update_folder_from_files(
                folder_name=folder_name,
                filename_list=file_list,
                get_2D_array=False,
            )
            logger.info(f"Finished with folder: {folder_name}.")
        logger.info(INFO_H5_FILES_UPDATED)

    @check_if_open
    def get_base_filename(self, filename_full_path=str()) -> str:
        """
        Returns the basename from a full address filename
        """
        basename = Path(filename_full_path).name
        return basename

    @check_if_open
    def generator_filenames_in_folder(self, folder_name=str(), yield_decode=True, basename=False):
        """
        Yields the name of every file stored in a specific folder

        Parameters:
        folder_name(str) : name of the folder (Group) at the first level of hierarchy
        full_path(bool) : yields the fullpath of the file (True) or just the basename (False)
        """
        try:
            dataset = self._file[folder_name]['Data']
        except:
            logger.info(f"The dataset Data with name: {folder_name} could not be read. Return.")
            return
        
        for data in dataset:
            if yield_decode:
                try:
                    item = bytes.decode(data.item())
                    if basename:
                        item = self.get_base_filename(item)
                except:
                    logger.info(f"Error during decoding of {data.item()}. Return")
                    return
            else:
                item = data.item()
            yield item

    @log_info
    def get_metadata_dataset(self, group_address=str(), key_metadata=str()) -> np.array:
        """
        Returns the dataset (np.array like) of metadata inside a specific folder (Group)

        Keyword Arguments:
            group_address -- name of the folder (Group) in the first level of hierarchy (default: {str()})
            key_metadata -- key(name) of the asked counter/motor (default: {str()})

        Returns:
            np.array : HDF5 dataset
        """
        try:
            dataset = self._file[group_address][METADATA_KEY][key_metadata]
            return dataset
        except Exception as e:
            logger.info(f"{e}: dataset {key_metadata} could not be accessed. Trying to open the file...")
        
        try:
            self._open_r
            dataset = self._file[group_address][METADATA_KEY][key_metadata]
            self._close
            return dataset
        except Exception as e:
            logger.info(f"{e}: dataset {key_metadata} could not be accessed anyway.")
        return

    @log_info
    def get_metadata_value(self, folder_name=str(), key_metadata=str(), index_list=list()) -> float:
        """
        Returns the metadata value of a specific folder and file (associated to index)

        Parameters:
        folder_name(str) : name of the folder (Group) in the first level of hierarchy
        key_metadata(str) : key(name) of the asked counter/motor
        index_list(int, list) : integer or list of integers which are the file index inside the folder (Group)

        Returns:
        float, str : value of the counter/motor inside the metadata
        """
        try:
            dataset = self.get_metadata_dataset(
                group_address=folder_name,
                key_metadata=key_metadata,
            )
        except:
            dataset = None
            return

        if isinstance(index_list, int):
            index_list = [index_list]

        if isinstance(dataset[0], float):
            avg_value = np.mean(
                np.array(
                    [dataset[index] for index in index_list]
                )
            )
        else:
            avg_value = [str(dataset[index]) for index in index_list]

        return avg_value

    @log_info
    @check_if_open
    def get_metadata_dataframe(self, folder_name=str(), list_keys=list()) -> pd.DataFrame:
        """
        Gather the dataset in a specific folder (Group) and builds a pandas dataframe

        Parameters:
        folder_name(str) : name of the folder (Group) in the first level of hierarchy
        list_keys(list) : list of metadata keys that will be stored in the dataframe as new columns

        Returns:
        pandas.DataFrame : dataframe with filenames as rows and metadata keys as columns
        """
        short_metadata = defaultdict(list)

        for filename in self.generator_filenames_in_folder(folder_name=folder_name):
            # Always append the name of the file
            short_metadata[FILENAME_KEY].append(str(Path(filename).name))

            for key in list_keys:
                try:
                    dataset_key = self.get_metadata_dataset(
                        group_address=folder_name,
                        key_metadata=key,
                    )
                    short_metadata[key] = dataset_key
                    # short_metadata[key] = list(self._file[folder_name]['Metadata'][key][()])
                except:
                    logger.info(f"Error during acceeding to Metadata dataset with key: {key}")
        dataframe = pd.DataFrame(short_metadata)
        logger.info(f"This is the dataframe: {dataframe}")
        return dataframe

    @log_info
    def generator_keys_in_folder(self, folder_name=str()):
        """
        Returns the generator of the metadata key that is stored in the Metadata Group inside a specific folder (Group)

        Parameters:
        folder_name(str) : name of the folder (Group) in the first level of hierarchy

        Returns:
        Generator of metadata keys
        """
        try:
            list_keys = self._file[folder_name][METADATA_KEY].keys()
        except Exception as e:
            list_keys = None
            logger.info(f"{e}: List of keys could not be retrieved. Trying to open the file...")
        
        # Try to open the h5 file
        if list_keys is None:
            try:
                list_keys = self._file[folder_name][METADATA_KEY].keys()
            except Exception as e:
                logger.info(f"{e}: List of keys could not be retrieved anyway.")
                return

        # Generate keys
        for key in list_keys:
            yield key   

    @log_info
    def get_filename_from_index(self, folder_name=str(), index_list=list()):
        try:
            if isinstance(index_list, int):
                index_list = [index_list]

            if len(index_list) == 1:
                filename = bytes.decode(self._file[folder_name]['Data'][()][index_list[0]][0][0])

            elif len(index_list) > 1:
                filename = bytes.decode(self._file[folder_name]['Data'][()][index_list[-1]][0][0])
                new_extension = f"{Path(filename).stem}_average.edf"
                filename = Path(filename).parent.joinpath(new_extension)
        except Exception as e:
            filename = None
            logger.info(f"{e}")
        
        if filename is None:
            try:
                if isinstance(index_list, int):
                    index_list = [index_list]

                if len(index_list) == 1:
                    filename = bytes.decode(self._file[folder_name]['Data'][()][index_list[0]][0][0])

                elif len(index_list) > 1:
                    filename = bytes.decode(self._file[folder_name]['Data'][()][index_list[-1]][0][0])
                    new_extension = f"{Path(filename).stem}_average.edf"
                    filename = Path(filename).parent.joinpath(new_extension)
            except Exception as e:
                logger.info(f"{e}")
                return
        return filename

    @log_info
    @check_if_open
    def get_folder_index_from_filename(self, filename=str()):
        """
        Searches the filename in the .h5 Groups and returns the name of the folder and the index of the file in the Group

        Parameters:
        filename(str) : string of the filename to be searched

        Returns:
        str : string with the name of the folder in the .h5 file
        int : index of the filename inside the folder
        """
        folder_name = str(Path(filename).relative_to(self.get_root_directory()))

        if not self._file.__contains__(folder_name):
            logger.info("There is no Group with the name {folder_name}. Returns.")
            return

        for index, file in enumerate(self.generator_filenames_in_folder(folder_name=folder_name)):
            if file == filename:
                logger.info(f"Found match with the filename at index {index}")
                return folder_name, index
        logger.info(f"No matches were found with the filename {filename}")
        return None, None

    #####################################
    ###### EDF METHODS ##########
    #####################################

    @log_info
    def get_Edf_instance(self, full_filename=str(), folder_name=str(), index_file=int()):

        # Take the full filename
        if full_filename:
            filename = full_filename
        else:
            try:
                filename = self.get_filename_from_index(
                    folder_name=folder_name,
                    index_list=index_file,
                )
            except Exception as e:
                logger.info(f"{e}: file could not be found in the repository.")

        # Open the Edf instance
        try:
            Edf_instance = EdfClass(
                filename=filename,
                ponifile_path=self.get_active_ponifile(),
                qz_parallel=self._qz_parallel,
                qr_parallel=self._qr_parallel,
            )
        except Exception as e:
            logger.info(f"{e}: Edf instance could not be created.")
            Edf_instance = None
        return Edf_instance

    @log_info
    def get_Edf_data(
        self, 
        folder_name=str(), 
        index_list=list(), 
        folder_reference_name=str(),
        file_reference_name=str(),
        reference_factor=0.0,
        normalized=False,
        ) -> np.array:
        """
        Returns the data array from a file stored in the h5 file.
        The data can be subtracted using the files in another folder as reference files

        Parameters:
        folder_name(str) : name of the folder(Group) in the first level of hierarchy
        index_list(list or int) : integer or list of integers of the file inside the Group
        folder_reference_name(str) : name of the folder (Group) that can be used as reference
        reference_factor(float) : scale factor that multiplies the reference file

        Returns:
        np.array : data of the file (subtracted or not)
        """
        if isinstance(index_list, int):
            index_list = [index_list]

        # Get the sample data
        try:
            data_sample = sum(
                [
                    self.get_Edf_instance(
                        folder_name=folder_name,
                        index_file=index,
                    ).get_data() for index in index_list
                ]
            ) / len(index_list)
            logger.info(f"New data sample with shape: {data_sample.shape}")
        except:
            data_sample = None
            logger.info(f"Data sample could not be uploaded.")

        if normalized:
            norm_factor = self.get_norm_factor(
                folder_name=folder_name,
                index_list=index_list,
            )
            data_sample = data_sample.astype('float32') / norm_factor

        return data_sample

    # @log_info
    # @check_if_open
    # def get_Edf_random(self):
    #     """
    #     Returns a Edf instance from a random folder and random index

    #     Parameters:
    #     None

    #     Returns:
    #     None
    #     """
    #     random_sample_index = int(random.random() * self.number_samples())
    #     random_sample = list(self.generator_samples())[random_sample_index]

    #     random_file_index = int(random.random() * self.number_files_in_sample(random_sample))
    #     return self.get_Edf_instance(
    #         folder_name=random_sample,
    #         index_file=random_file_index,
    #     )

    #####################################
    ###### INTEGRATION METHODS ##########
    #####################################

    @log_info
    def map_reshaping(
        self,
        data=None,
    ):
        ponifile = self.get_active_ponifile()
        ai = load(ponifile)
        data_reshape, q, chi = ai.integrate2d(
            data=data,
            npt_rad=1000,
            unit="q_nm^-1",
        )
        return data_reshape, q, chi

    @log_info
    def raw_integration(
        self,
        folder_name=str(),
        index_list=list(),
        data=None,
        norm_factor=1.0,
        list_dict_integration=list(),
    ) -> list:
        """
        Chooses which integration is going to be performed: azimuthal (pyFAI), radial (pyFAI) or box (self method)

        Parameters:
        folder_name(str) : name of the folder(Group) in the first level of hierarchy
        index_list(list or int) : integer of list of integers for the files inside the folder
        data(np.array) : data can be uploaded directly
        norm_factor(float) : this value will be used by the pygix-pyFAI integration engine
        list_dict_integration(list) : list of dictionaries with key-values that will be read by the pygix-pyFAI integration engine
        
        Returns:
        list : list of numpy arrays with the result of the integration
        """
        # Get the data
        if data is None:
            data = self.get_Edf_data(
                folder_name=folder_name,
                index_list=index_list,
            )

        # # Updates the incident and tilt angle
        # incident_angle = self.get_incident_angle(
        #     folder_name=folder_name,
        #     index_list=index_list,
        # )
        # tilt_angle = self.get_tilt_angle(
        #     folder_name=folder_name,
        #     index_list=index_list,
        # )
        # self.update_incident_tilt_angle(
        #     incident_angle=incident_angle,
        #     tilt_angle=tilt_angle,
        # )

        # Get the normalization factor
        if norm_factor == 1.0:
            norm_factor = self.get_norm_factor(
                folder_name=folder_name,
                index_list=index_list,
            )

        array_compiled = []
        for dict_integration in list_dict_integration:
            if dict_integration['Type'] == AZIMUTH_NAME:
                res = self.raw_integration_azimuthal(
                    data=data,
                    norm_factor=norm_factor,
                    dict_integration=dict_integration,
                )

            elif dict_integration['Type'] == RADIAL_NAME:
                res = self.raw_integration_radial(
                    data=data,
                    norm_factor=norm_factor,
                    dict_integration=dict_integration,
                )

            elif dict_integration['Type'] in (HORIZONTAL_NAME, VERTICAL_NAME):
                res = self.raw_integration_box(
                    data=data,
                    norm_factor=norm_factor,
                    dict_integration=dict_integration,
                )
            else:
                print(ERROR_RAW_INTEGRATION)
                res = None

            array_compiled.append(res)
        return array_compiled

    @log_info
    def raw_integration_azimuthal(
        self, 
        data=None,
        norm_factor=1.0,
        dict_integration=dict(),
    ) -> np.array:
        """
        Performs an azimuthal integration using the pygix-pyFAI engine

        Parameters:
        data(np.array) : data to be integrated
        norm_factor(float) : this value will be used by the pygix-pyFAI integration engine
        dict_integration(dict) : dictionary with key-values that will be read by the pygix-pyFAI integration engine
        
        Returns:
        np.array : result of the integration
        """
        # Take the array of intensity
        if (data is None) or (not dict_integration):
            return
        p0_range=dict_integration['Radial_range']
        p1_range=dict_integration['Azimuth_range']
        unit=dict_integration['Unit']
        npt=self.calculate_bins(
                    radial_range=p0_range,
                    unit=unit,
        )

        # Do the integration with pygix/pyFAI
        try:
            logger.info(f"Trying azimuthal integration with: bins={npt}, p0_range={p0_range}, p1_range={p1_range}, unit={unit}")
            y_vector, x_vector = self.integrate_1d(
                process='sector',
                data=data,
                npt=npt,
                p0_range=p0_range,
                p1_range=p1_range,
                unit=unit,
                normalization_factor=float(norm_factor),
                polarization_factor=POLARIZATION_FACTOR,
            )
            logger.info("Integration performed.")
        except:
            logger.info("Error during azimuthal integration.")
            return

        return np.array([x_vector, y_vector])

    @log_info
    def raw_integration_radial(
        self, 
        data=None,
        norm_factor=1.0,
        dict_integration=dict(),
    ) -> np.array:
        """
        Performs a radial integration using the pygix-pyFAI engine

        Parameters:
        data(np.array) : data to be integrated
        norm_factor(float) : this value will be used by the pygix-pyFAI integration engine
        dict_integration(dict) : dictionary with key-values that will be read by the pygix-pyFAI integration engine
        
        Returns:
        np.array : result of the integration
        """
        # Take the array of intensity
        if (data is None) or (not dict_integration):
            return

        # Do the integration with pygix/pyFAI
        npt  = int(dict_integration['Bins_azimut'])
        p0_range = dict_integration['Radial_range']
        p1_range = dict_integration['Azimuth_range']

        unit_gi = {
            'q_nm^-1' : Q_NM,
            'q_A^-1' : Q_A,
            '2th_deg' : TTH_DEG,
            '2th_rad' : TTH_RAD,
        }
        unit = unit_gi[dict_integration['Unit']]
        
        try:
            logger.info(f"Trying radial integration with: npt={npt}, p0_range={p0_range}, p1_range={p1_range}, unit={unit}")
            y_vector, x_vector = self.integrate_1d(
                process='chi',
                data=data,
                npt=npt,
                p0_range=p1_range,
                p1_range=p0_range,
                unit=unit,
                normalization_factor=float(norm_factor),
                polarization_factor=POLARIZATION_FACTOR,
            )
            logger.info("Integration performed.")
        except:
            logger.info("Error during radial integration.")
            return
        return np.array([x_vector, y_vector])

    @log_info
    def raw_integration_box(
        self, 
        data=None,
        norm_factor=1.0,
        dict_integration=dict(),
    ) -> pd.DataFrame:
        """
        Performs a box integration using the pygix-pyFAI engine

        Parameters:
        data(np.array) : data to be integrated
        norm_factor(float) : this value will be used by the pygix-pyFAI integration engine
        dict_integration(dict) : dictionary with key-values that will be read by the pygix-pyFAI integration engine
        
        Returns:
        np.array : result of the integration
        """
        # Take the array of intensity
        if (data is None) or (not dict_integration):
            return

        # Get the direction of the box
        process = DICT_BOX_ORIENTATION[dict_integration['Type']]
        unit=dict_integration['Unit_input']
        try:
            if process == 'opbox':
                p0_range, p1_range = dict_integration['Oop_range'], dict_integration['Ip_range']
                npt = self.calculate_bins(
                    radial_range=dict_integration['Oop_range'],
                    unit=unit,
                )
            elif process == 'ipbox':
                p0_range, p1_range = dict_integration['Ip_range'], dict_integration['Oop_range']
                npt = self.calculate_bins(
                    radial_range=dict_integration['Ip_range'],
                    unit=unit,
                )
            else:
                return
        except:
            p0_range, p1_range, npt = None, None, NPT_RADIAL

        # Transform input units if necessary
        p0_range = [self.get_q_nm(
            value=position,
            input_unit=unit,
            direction=dict_integration['Type'],
        ) for position in p0_range]

        p1_range = [self.get_q_nm(
            value=position,
            input_unit=unit,
            direction=dict_integration['Type'],
        ) for position in p1_range]

        # Do the integration with pygix/pyFAI
        try:
            logger.info(f"Trying box integration with: process={process}, npt={npt}, p0_range={p0_range}, p1_range={p1_range}, unit={unit}")
            y_vector, x_vector = self.integrate_1d(
                process=process,
                data=data,
                npt=npt,
                p0_range=p0_range,
                p1_range=p1_range,
                unit=unit,
                normalization_factor=float(norm_factor),
                polarization_factor=POLARIZATION_FACTOR,
                # method='bbox',
            )
            logger.info("Integration performed.")
        except:
            logger.info("Error during box integration.")
            return

        return np.array([x_vector, y_vector])

    @log_info
    def calculate_bins(self, radial_range=[], unit='q_nm^-1') -> int:
        """
        Calculates the bins between two q values

        Parameters:
        radial_range(list, tuple) : two components with the minimum and maximum radial position to be integrated
        unit(str) : 'q_nm^-1', 'q_A^-1', '2th_deg' or '2th_rad'

        Returns:
        int : number of counts to be generated
        """
        if unit in ('q_nm^-1', 'q_A^-1'):
            twotheta1 = self.q_to_twotheta(
                q=radial_range[0],
                unit=unit,
            )

            twotheta2 = self.q_to_twotheta(
                q=radial_range[1],
                unit=unit,
            )
        elif unit == '2th_deg':
            twotheta1, twotheta2 = np.radians(radial_range[0]), np.radians(radial_range[1])
        elif unit == '2th_rad':
            twotheta1, twotheta2 = radial_range[0], radial_range[1]
        else:
            return
        return int(round(self._dist / self.get_pixel1() * (np.tan(twotheta2) - np.tan(twotheta1))))

    @log_info
    def q_to_twotheta(self, q=0.0, unit='q_nm^-1', degree=False) -> float:
        """
        Transforms from q to 2theta (rad)

        Parameters:
        q(float) : modulus of q, scattering vector
        unit(str) : 'q_nm^-1' or 'q_A^-1'
        degree(bool) : the result will be in degrees (True) or radians (False)

        Returns:
        float : twotheta value
        """
        if unit == 'q_nm^-1':
            twotheta = 2 * np.arcsin((q*self._wavelength * 1e9)/(4*np.pi))
        elif unit == 'q_A^-1':
            twotheta = 2 * np.arcsin((q*self._wavelength * 1e10)/(4*np.pi))
        else:
            return
        return np.rad2deg(twotheta) if degree else twotheta

    @log_info
    def get_q_nm(self, value=0.0, direction='Vertical', input_unit='q_nm^-1') -> float:
        """
            Return a q(nm-1) value from another unit
        """
        if input_unit == 'q_nm^-1':
            return value
        elif input_unit == 'q_A^-1':
            return value * 10
        elif input_unit == '2th_deg':
            return self.twotheta_to_q(twotheta=value, direction=direction, deg=True)
        elif input_unit == '2th_rad':
            return self.twotheta_to_q(twotheta=value, deg=False)
        else:
            return None

    @log_info
    def twotheta_to_q(self, twotheta=0.0, direction='Vertical', deg=True) -> float:
        """
            Returns the q(nm-1) from the 2theta value
        """
        if deg:
            twotheta = np.radians(twotheta)
        try:
            wavelength_nm = self._wavelength * 1e9
        except:
            return
        
        try:
            alpha_inc = np.radians(self.incident_angle)
        except:
            alpha_inc = 0.0
        
        q_horz = 2 * np.pi / wavelength_nm * (np.cos(alpha_inc) * np.sin(twotheta))
        q_vert = 2 * np.pi / wavelength_nm * (np.sin(twotheta) + np.sin(alpha_inc))

        if direction == 'Vertical':
            return q_horz
        elif direction == 'Horizontal':
            return q_vert
        else:
            return

    @log_info
    def get_detector_array(self, shape=()) -> np.array:
        """
        Returns an array with detector shape and rotated, according to sample orientation (pygix-pyFAI)

        Parameters:
        None

        Returns:
        np.array : 2D array with the shape of the detector registered in the active ponifile
        """
        try:
            # This method does not work with ALBA_NCD_Nov2022
            if not shape:
                shape = self.get_shape()

            logger.info(f"Shape of the detector: {shape}")
            d2,d1 = np.meshgrid(
                np.linspace(1,shape[1],shape[1]),
                np.linspace(1,shape[0],shape[0]),
            )
            out = np.array([d1,d2])
            return out
        except:
            return None

    @log_info
    @check_if_open
    def get_mesh_matrix(self, unit='q_nm^-1', shape=()):
        """
        Returns both horizontal and vertical mesh matrix for Grazing-Incidence geometry, returns also the corrected data without the missing wedge
        
        Parameters:
        unit(str) : 'q_nm^-1', 'q_A^-1', '2th_deg' or '2th_rad'
        data(np.array) : 2D map data

        Returns:
        np.array(QX)
        np.array(QZ)
        np.array(data)
        """
        if not shape:
            logger.info(f"Shape is None. Returns.")
            return

        # Get the detector array, it is always the same shape (RAW MATRIX SHAPE!), no rotations yet
        # shape = data.shape
        det_array = self.get_detector_array(shape=shape)

        # Get the mesh matrix
        if unit in UNITS_Q:
            try:
                # calc_q will take into account the sample_orientation in GrazingGeometry instance
                scat_z, scat_xy = self.calc_q(
                    d1=det_array[0,:,:],
                    d2=det_array[1,:,:],
                )
                logger.info(f"Shape of the scat_z matrix: {scat_z.shape}")
                logger.info(f"Shape of the scat_x matrix: {scat_xy.shape}")
            except:
                scat_z, scat_xy = None, None
                logger.info(f"Scat_z matrix could not be generated.")
                logger.info(f"Scat_x matrix could not be generated.")
        elif unit in UNITS_THETA:
            try:
                scat_z, scat_xy = self.calc_angles(
                    d1=det_array[0,:,:],
                    d2=det_array[1,:,:],
                )
                logger.info(f"Shape of the scat_z matrix: {scat_z.shape}")
                logger.info(f"Shape of the scat_x matrix: {scat_xy.shape}")
            except:
                scat_z, scat_xy = None, None
                logger.info(f"Scat_z matrix could not be generated.")
                logger.info(f"Scat_x matrix could not be generated.")

        # Transform units
        if (scat_z is not None) and (scat_xy is not None):
            DICT_PLOT = DICT_UNIT_PLOTS.get(unit, DICT_PLOT_DEFAULT)
            scat_z *= DICT_PLOT['SCALE']
            scat_xy *= DICT_PLOT['SCALE']
            logger.info(f"Changing the scale of the matriz q units. Scale: {DICT_PLOT['SCALE']}")
        else:
            return
        return scat_xy, scat_z


    @log_info
    @check_if_open
    def get_last_file(self, list_files=list()) -> str:
        """
        Returns the file with the highest epoch, time of creation

        Parameters:
        list_files(list) : list of files among the the last created will be found, if not, all the files in the .h5 file

        Returns:
        str : string with the full path of the file with the highest time of creation
        """
        if not list_files:
            list_files = [getctime(file) for file in self.generator_all_files()]
        try:
            last_file = list_files[np.argmax(list_files)]
            logger.info(f"Found last file: {last_file}")
        except:
            logger.info("The last file could not be found.")
        return last_file
            