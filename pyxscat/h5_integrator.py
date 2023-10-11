from collections import defaultdict
from pathlib import Path
from pyFAI import load
from pyFAI.io.ponifile import PoniFile
from pygix.transform import Transform
from pygix.grazing_units import TTH_DEG, TTH_RAD, Q_A, Q_NM
from os.path import getctime

from pyxscat.edf import EdfClass
from pyxscat.other.other_functions import date_prefix, get_dict_files, get_dict_difference
from pyxscat.gui import LOGGER_PATH
from pyxscat.other.units import *

import h5py
import logging
import numpy as np
import pandas as pd
from silx.io.h5py_utils import File
from pyxscat.other.integrator_methods import *
from pyxscat.other.setup_methods import *
import os

ENCODING_FORMAT = "UTF-8"
FORMAT_STRING = h5py.string_dtype(ENCODING_FORMAT)
FORMAT_FLOAT = 'float64'

DEFAULT_SHAPE_1D = (0,)
MAXSHAPE_1D_RESIZE = (None,)
DEFAULT_H5_PATH = '.'

UNIT_GI = {
    'q_nm^-1' : Q_NM,
    'q_A^-1' : Q_A,
    '2th_deg' : TTH_DEG,
    '2th_rad' : TTH_RAD,
}

DESCRIPTION_HDF5 = "HDF5 file with Scattering methods."
BEAMLINE = "BM28-XMaS"
COMMENT_NEW_FILE = ""

FILENAME_H5_KEY = "h5_filename"
NAME_H5_KEY = "name"
ROOT_DIRECTORY_KEY = "root_directory"
DATETIME_KEY = "datetime"
SAMPLE_KEY = "sample"
CLASS_KEY = "class"
INDEX_KEY = "index"
DATA_KEY = "data"
METADATA_KEY = "metadata"
FILENAME_KEY = "filename"
SAMPLE_GROUP_KEY = "samples"
PONI_GROUP_KEY = "ponifiles"
ABS_ADDRESS_KEY = "abs_address"
REL_ADDRESS_KEY = "rel_address"

ADDRESS_METADATA_KEYS = '.'
ADDRESS_PONIFILE = '.'

MODE_OVERWRITE = "w"
MODE_READ = "r"
MODE_WRITE = "r+"

PONIFILE_DATASET_KEY = "ponifiles"
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
    'horizontal' : 'ipbox',
    'vertical' : 'opbox',
}

AZIMUTH_NAME = 'azimuthal'
RADIAL_NAME = 'radial'
HORIZONTAL_NAME = 'horizontal'
VERTICAL_NAME = 'vertical'

ERROR_RAW_INTEGRATION = "Failed at detect integration type."
MSG_LOGGER_INIT = "Logger was initialized."


INFO_H5_PONIFILES_DETECTED = "New ponifiles detected."
INFO_H5_NO_PONIFILES_DETECTED = "No ponifiles detected."
INFO_H5_NEW_FILES_DETECTED = "New files were detected."
INFO_H5_NEW_DICTIONARY_FILES = "Got dictionary of folders and files"
INFO_H5_FILES_UPDATED = "Finished the update of all the new files."

ERROR_MAIN_DIRECTORY = "No main directory was detected."

INPUT_FILE_NOT_VALID = 'The input file does not exist.'
ROOT_DIR_NOT_VALID = 'The root directory is not valid.'
ROOT_DIR_NOT_ACCESIBLE = 'The access to root directory is not available.'
INPUT_ROOT_DIR_NOT_VALID = 'There is no valid root directory nor input file.'
H5_FILENAME_NOT_VALID = 'No valid path for the .h5 file'

from pyxscat.logger_config import setup_logger
logger = setup_logger()


def logger_info(func):
    def wrapper(*args, **kwargs):
        logger.info(f'We entered into function: {func.__name__}')
        return func(*args, **kwargs)
    return wrapper

class H5GIIntegrator():
# class H5GIIntegrator(Transform):
    """
    Creates an HDF5 file and provides methods to read/write the file following the hierarchy of XMaS-BM28
    """
    def __init__(
        self,
        input_h5_filename='',        
        root_directory='',
        output_filename_h5='',
        ) -> None:

        logger.info("H5GIIntegrator instance was created.")

        if input_h5_filename:

            self.input_file_exists(
                input_filename=input_h5_filename,
            )

            self.init_root_h5_attributes(
                input_h5_filename=input_h5_filename,
                root_directory=root_directory,
                output_filename_h5=output_filename_h5,
            )

            self.init_metadata_attrs()

        elif root_directory:

            self.directory_valid(
                directory=root_directory,
            )

            output_filename_h5 = self.get_h5_output_filename(
                h5_output_file=output_filename_h5,
                root_directory=root_directory,
            )

            self.init_root_h5_attributes(
                input_h5_filename=input_h5_filename,
                root_directory=root_directory,
                output_filename_h5=output_filename_h5,
            )

            self.init_metadata_attrs()

            self.create_h5_file(
                h5_filename=output_filename_h5,
            )

            self.write_root_attributes(
                root_directory=root_directory,
                h5_filename=output_filename_h5,
            )     

            self.init_h5_groups()

        else:
            raise Exception(INPUT_ROOT_DIR_NOT_VALID) 

    def init_root_h5_attributes(
        self,
        input_h5_filename='',
        root_directory='',
        output_filename_h5='',
    ):
        if input_h5_filename:

            self.set_h5_filename(
                h5_filename=input_h5_filename
            )            

            root_directory = self.h5_get_attr(
                attr_key=ROOT_DIRECTORY_KEY,
                group_address=DEFAULT_H5_PATH,
            )

            self.directory_valid(
                directory=root_directory,
            )

            self.set_root_directory(
                root_directory=root_directory,
            )

        elif root_directory:

            self.set_root_directory(root_directory=root_directory)

            output_filename_h5 = self.get_h5_output_filename(
                h5_output_file=output_filename_h5,
                root_directory=root_directory,
            )

            self.set_h5_filename(h5_filename=output_filename_h5)

        else:
            raise Exception(INPUT_ROOT_DIR_NOT_VALID)
        
        self._transform = Transform()
                    

    def set_root_directory(self, root_directory=''):
        self._root_dir = Path(root_directory)

    def set_h5_filename(self, h5_filename=''):
        self._h5_filename = Path(h5_filename)
        self._name = self._h5_filename.name

    def filename_valid(self, filename=''):
        parent_path = Path(filename).parent
        if parent_path.exists() and os.access(parent_path, os.W_OK):
            return True
        else:
            return False

    def input_file_exists(self, input_filename=''):
        if not Path(input_filename).is_file():
            raise Exception(f'{INPUT_FILE_NOT_VALID}: {input_filename}')

    def directory_valid(self, directory=''):
        if directory:
            directory = Path(directory)

            if not directory.exists():
                raise Exception(ROOT_DIR_NOT_VALID)

            if not os.access(directory, os.W_OK):
                raise Exception(ROOT_DIR_NOT_ACCESIBLE)

            return True
        else:
            return

    def get_h5_output_filename(self, h5_output_file='', root_directory=''):
        if h5_output_file:
            if self.filename_valid(filename=h5_output_file):
                return h5_output_file
            else:
                logger.info(f"{h5_output_file} is not a valid filename.")
                pass
        
        if root_directory:
            name = Path(root_directory).name
            h5_output_file = Path(root_directory).joinpath(name).with_suffix(".h5")
            if self.filename_valid(filename=h5_output_file):
                return h5_output_file
            else:
                raise Exception(H5_FILENAME_NOT_VALID)

    @logger_info
    def create_h5_file(self, h5_filename=''):
        if not h5_filename:
            h5_filename = self._h5_filename

        if not self.filename_valid(filename=h5_filename):
            logger.error(f"{e}: The file {h5_filename} is not valid to create an .h5 file.")
            self._file = None
            return
        
        try:
            self._file = File(h5_filename, MODE_OVERWRITE)
            self._file.close()
            logger.debug(f"The file {h5_filename} was created ")
        except Exception as e:
            self._file = None
            logger.error(f"{e}: The file {h5_filename} could not be created.")

    @logger_info
    def init_h5_groups(self, h5_filename=''):
        self.create_group_samples(h5_filename=h5_filename)
        self.create_group_ponifiles(h5_filename=h5_filename)

    @logger_info
    def write_root_attributes(
        self,
        root_directory='',
        h5_filename='',
        ):
        # Write the attributes into the .h5 file
        dict_attrs = {
            NAME_H5_KEY : Path(h5_filename).name,
            ROOT_DIRECTORY_KEY : Path(root_directory).as_posix(),
            DATETIME_KEY : date_prefix(),
            FILENAME_H5_KEY : Path(h5_filename).as_posix(),
        }

        with File(h5_filename, 'r+') as f:
            for k, v in dict_attrs.items():
                f.attrs[k] = v

    @property
    def _open_r(self):
        """
        Opens the h5 file with reading permises
        """   
        # self._file = File(str(self._h5_filename), MODE_READ)
        self._open_w

    @property
    def _open(self):
        self._open_w
        
    @property
    def _open_w(self):
        """
        Opens the h5 file with reading/writing permises
        """        
        self._file = File(str(self._h5_filename), MODE_WRITE)
        logger.info("H5 OPEN TO READ/WRITE")

    @property
    def _close(self):
        """
        Closes the h5 file
        """
        self._file.close()
        logger.info("H5 CLOSED")

    @property
    def is_open(self):
        return bool(self._file)

    @property
    def get_mode(self):
        if self.is_open:
            return self._file.mode
        else:
            return False

    @logger_info
    def h5_write_attrs_in_group(self, dict_attrs=dict(), group_address='.'):
        """
        Write the key-values from a dictionary as attributes at the root level of h5 file

        Keyword Arguments:
            dict_attrs -- dictionary with root attribute information (default: {dict()})
            address -- path of the Group inside the h5 File (default: {'.'})
        """
        for k, v in dict_attrs.items():
            self.h5_write_attr_in_group(
                key=k,
                value=v,
                group_address=group_address,
            )

    @logger_info
    def init_metadata_attrs(self) -> None:
        """
        Declare attributes to easy access
        """
        self._iangle_key = ''
        self._tangle_key = ''
        self._norm_key = ''
        self._acq_key = ''

    @logger_info
    def h5_write_attr_in_group(self, key=str(), value=str(), group_address='.'):
        """
        Write a key-value attribute into a specific h5 address

        Keyword Arguments:
            key -- name of the attribute (default: {str()})
            value -- value of the attribute (default: {str()})
            address -- address of Group in the h5 file (default: {'/'})
        """        
        # Encode the string
        # value = value.encode(ENCODING_FORMAT)     

        # Try to write directly
        with File(self._h5_filename, 'r+') as f:
            f[group_address].attrs[key] = value

    @logger_info
    def h5_get_attr(self, attr_key=str(), group_address='.') -> str:
        """
        Returns the attribute value from a specific Group

        Keyword Arguments:
            attr_key -- name of the attribute (default: {str()})
            group_address -- address of the H5 Group (default: {'.'})

        Returns:
            value of the attribute
        """
        with File(self._h5_filename, 'r+') as f:
            try:
                attr = f[group_address].attrs[attr_key]
            except Exception as e:
                logger.error(f"{e}: attr {attr_key} does not exists in {group_address}")
        return attr

    @logger_info
    def h5_get_dict_attrs(self, group_address='.') -> dict:
        """
        Returns a dictionary with the key-value attributes of a Group

        Keyword Arguments:
            group_address -- address of the Group inside the H5 File (default: {'.'})

        Returns:
            dictionary with the key-value attributes
        """
        with File(self._h5_filename, 'r+') as f:
            dict_attrs = {k:v for k,v in f[group_address].attrs.items()}
        return dict_attrs

    #########################################################
    ######### METHODS FOR KEY METADATA ######################
    #########################################################

    @logger_info
    def update_metadata_keys(
        self, 
        dict_metadata_keys=dict(), 
        iangle_key=str(), 
        tangle_key=str(), 
        norm_factor=str(), 
        acq_key=str(),
        ):
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
        
        self._iangle_key = dict_metadata_keys[INCIDENT_ANGLE_KEY]
        self._tangle_key = dict_metadata_keys[TILT_ANGLE_KEY]
        self._norm_key = dict_metadata_keys[NORMALIZATION_KEY]
        self._acq_key = dict_metadata_keys[ACQUISITION_KEY]

    @logger_info
    def get_iangle_key(self):
        """
        Returns the string of the stored key for incident angle
        """
        iangle_key = self._iangle_key
        return iangle_key

    @logger_info
    def get_tiltangle_key(self):
        """
        Returns the string of the stored key for tilt angle
        """
        tangle_key = self._tangle_key
        return tangle_key

    @logger_info
    def get_norm_key(self):
        """
        Returns the string of the stored key for normalization factor
        """
        norm_key = self._norm_key
        return norm_key

    @logger_info
    def get_acquisition_key(self):
        """
        Returns the string of the stored key for acquisition time
        """
        acq_key = self._acq_key
        return acq_key

    @logger_info
    def get_metadata_dict(self) -> dict:
        """
        Returns a dictionary with the key-value metadata information

        Keyword Arguments:
            group_address -- address of the Group inside the H5 File (default: {'.'})

        Returns:
            dictionary with the metadata key-values
        """
        dict_metadata = dict()
        dict_metadata[INCIDENT_ANGLE_KEY] = self._iangle_key
        dict_metadata[TILT_ANGLE_KEY] = self._tangle_key
        dict_metadata[NORMALIZATION_KEY] = self._norm_key
        dict_metadata[ACQUISITION_KEY] = self._acq_key
        return dict_metadata

    @logger_info
    def get_dataset_acquisition_time(
        self, 
        sample_name=str(),
        sample_relative_address=True,
        ) -> np.array:
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
                sample_name=sample_name,
                key_metadata=key_acq,
                sample_relative_address=sample_relative_address,
            )
        except:
            dataset = None
        return dataset

    @logger_info
    def get_dataset_incident_angle(
        self, 
        sample_name=str(), 
        sample_relative_address=True,
        ) -> np.array:
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
                sample_name=sample_name,
                sample_relative_address=sample_relative_address,
                key_metadata=key_iangle,
            )
        except:
            dataset = None
        return dataset

    @logger_info
    def get_dataset_tilt_angle(
        self, 
        sample_name=str(), 
        sample_relative_address=True,
        ) -> np.array:
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
                sample_name=sample_name,
                sample_relative_address=sample_relative_address,
                key_metadata=key_tangle,
            )
        except:
            dataset = None
        return dataset

    @logger_info
    def get_dataset_norm_factor(
        self, 
        sample_name=str(),
        sample_relative_address=True,
        ) -> np.array:
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
                sample_name=sample_name,
                sample_relative_address=sample_relative_address,
                key_metadata=key_norm,
            )
        except:
            dataset = None
        return dataset

    @logger_info
    def get_acquisition_time(
        self, 
        folder_name=str(), 
        index_list=int(),
        sample_relative_address=True,
        ) -> float:
        """
        Returns the acquisition time of a file or the average from a list of files (index)

        Parameters:
        folder_name(str) : name of the folder(Group) in the first hierarchical level of h5 file
        index_list(list, int) : integer or list of integers which are the index of the files inside the group

        Returns
        float : the acquisition time of one file or the average of different from the same Group
        """
        dataset = self.get_dataset_acquisition_time(
            sample_name=folder_name,
            sample_relative_address=sample_relative_address,
        )

        if dataset is not None:
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

    @logger_info
    def get_incident_angle(
        self, 
        sample_name=str(),
        sample_relative_address=True,
        index_list=int(),
        ) -> float:
        """
        Returns the incident angle of a file or the average from a list of files (index)

        Parameters:
        folder_name(str) : name of the folder(Group) in the first hierarchical level of h5 file
        index_list(list, int) : integer or list of integers which are the index of the files inside the group

        Returns
        float : the incident angle of one file or the average of different from the same Group
        """
        dataset = self.get_dataset_incident_angle(
            sample_name=sample_name,
            sample_relative_address=sample_relative_address,
        )

        if dataset is not None:
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

    @logger_info
    def get_tilt_angle(
        self, 
        sample_name=str(),
        sample_relative_address=True,
        index_list=int(),
        ) -> float:
        """
        Returns the tit angle of a file or the average from a list of files (index)

        Parameters:
        folder_name(str) : name of the folder(Group) in the first hierarchical level of h5 file
        index_list(list, int) : integer or list of integers which are the index of the files inside the group

        Returns
        float : the tilt angle of one file or the average of different from the same Group
        """
        dataset = self.get_dataset_tilt_angle(
            sample_name=sample_name,
            sample_relative_address=sample_relative_address,
        )

        if dataset is not None:
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

    @logger_info
    def get_norm_factor(
        self, 
        sample_name=str(), 
        sample_relative_address=True,
        index_list=int()) -> float:
        """
        Returns the normalization factor of a file or the average from a list of files (index)

        Parameters:
        folder_name(str) : name of the folder(Group) in the first hierarchical level of h5 file
        index_list(list, int) : integer or list of integers which are the index of the files inside the group

        Returns
        float : the normalization factor of one file or the average of different from the same Group
        """
        dataset = self.get_dataset_norm_factor(
            sample_name=sample_name,
            sample_relative_address=sample_relative_address,
        )

        if dataset is not None:
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
            logger.error("Failed while getting norm factor. Norm. factor set to 1.0.")
            norm_factor = 1.0

        logger.info(f"Norm factor: {norm_factor}")
        return norm_factor


    #########################################################
    ######### METHODS FOR PONIFILES ######################
    #########################################################

    @logger_info
    def search_ponifiles(self, new_files=True) -> list:
        """
        Searches for .poni files in the root directory

        Returns:
            list of .poni files recursively in the root directory
        """                
        if not self._root_dir:
            return
        try:
            searched_ponifiles = [file.as_posix() for file in self._root_dir.rglob("*.poni")]

            if new_files:
                stored_ponifiles = self.get_all_ponifiles(get_relative_address=False)
                searched_ponifiles = [file for file in searched_ponifiles if file not in stored_ponifiles]

            logger.info(f"Found {len(searched_ponifiles)} .poni files in {self._root_dir}")
        except Exception as e:
            logger.error(f"{e}: there was an error during searching ponifiles in {self._root_dir}.")
            return

        return searched_ponifiles

    # @log_info
    # def update_ponifiles(
    #     self,
    #     group_address=PONI_GROUP_KEY,
    #     ponifile_list=list(), 
    #     search=False,
    #     relative_to_root=True,
    #     ):
    #     self._open
    #     self._update_ponifiles(
    #         group_address=group_address,
    #         ponifile_list=ponifile_list,
    #         search=search,
    #         relative_to_root=relative_to_root,
    #     )
    #     self._close




    def create_data_dset(self, sample_name=str()):
        self.create_dataset_path(
            group_address=f"{SAMPLE_GROUP_KEY}/{sample_name}",
            dset_name=DATA_KEY,
        )

    def create_metadata_group(self, sample_name=str()):
        self.create_group(
            root_group_address=f"{SAMPLE_GROUP_KEY}/{sample_name}",
            group_name=METADATA_KEY,
        )

    def create_metadata_dset_str(self, sample_name=str(), metadata_key=str()):
        self.create_dataset_path(
            group_address=f"{SAMPLE_GROUP_KEY}/{sample_name}/{METADATA_KEY}",
            dset_name=metadata_key,
        )

    def create_metadata_dset_float(self, sample_name=str(), metadata_key=str()):
        self.create_dataset_float(
            group_address=f"{SAMPLE_GROUP_KEY}/{sample_name}/{METADATA_KEY}",
            dset_name=metadata_key,
        )

    @logger_info
    def update_ponifiles(self):

        # Creates the dataset for ponifiles if needed
        self.create_ponifile_dset()

        # Search new files if requested
        ponifile_list = self.search_ponifiles(new_files=True)

        if not ponifile_list:
            logger.info("No ponifiles to be updated. Return.")
            return

        # Return if no new ponifiles
        if not ponifile_list:
            logger.info(f"No ponifiles to update.")
            return

        self.append_ponifile_list(
            ponifile_list=ponifile_list,
        )

    @logger_info
    def append_metadata_values(self, sample_name=str(), metadata_key=str(), value_list=list()):
    
        
        
        self.append_stringlist_to_dataset(
            group_address=f"{SAMPLE_GROUP_KEY}/{sample_name}/{METADATA_KEY}",
            dataset_name=metadata_key,
            list_to_append=value_list,
        )


    @logger_info
    def append_datafile_list(self, sample_name=str(), datafile_list=list()):

        self.append_stringlist_to_dataset(
            group_address=f"{SAMPLE_GROUP_KEY}/{sample_name}",
            dataset_name=DATA_KEY,
            list_to_append=datafile_list,
        )


    @logger_info
    def append_ponifile_list(self, ponifile_list=list()):
        self.append_stringlist_to_dataset(
            group_address=PONI_GROUP_KEY,
            dataset_name=PONIFILE_DATASET_KEY,
            list_to_append=ponifile_list,
        )

    @logger_info
    def append_stringlist_to_dataset(self, group_address='.', dataset_name=str(), list_to_append=list()):
        if isinstance(list_to_append, str):
            list_to_append = [list_to_append]

        with File(self._h5_filename, 'r+') as f:
            if not f[group_address].__contains__(dataset_name):
                logger.info(f"{dataset_name} does not exist in {group_address}. Create it before appending.")
            else:
                try:
                    dataset = f[group_address][dataset_name]
                    dataset.resize((dataset.shape[0] + len(list_to_append),))
                    dataset[-len(list_to_append):] = list_to_append
                    logger.debug(f"{str(list_to_append)} was appended to {group_address}/{dataset}")
                except Exception as e:
                    logger.error(f"{str(list_to_append)} could not be appended to {group_address}/{dataset}")



    # @log_info
    # def get_active_ponifile(self) -> Path:
    #     """
    #     Returns the active ponifile string from the dataset at the first level of hierarchy

    #     Returns:
    #         Path of the active ponifile
    #     """        
    #     try:
    #         ponifile_active = self._file[PONI_GROUP_KEY][PONIFILE_ACTIVE_KEY][()][0]
    #     except Exception as e:
    #         logger.info(f"{e}: active ponifile could not be retrieved. Trying to open the file...")
    #         ponifile_active =None
        
    #     # Try after opening the h5 File
    #     if ponifile_active is None:
    #         try:
    #             self._open_r
    #             ponifile_active = self._file[PONI_GROUP_KEY][PONIFILE_ACTIVE_KEY][()][0]
    #             self._close
    #         except Exception as e:
    #             logger.info(f"{e}: active ponifile could not be retrieved anyway.")
    #             return
        
    #     # Decode if necessary
    #     if isinstance(ponifile_active, bytes):
    #         ponifile_active = bytes.decode(ponifile_active, encoding=ENCODING_FORMAT)
        
    #     # Use Path instance
    #     ponifile_active = Path(ponifile_active)
    #     return ponifile_active

    @logger_info
    def update_ponifile_parameters(self, dict_poni=dict()) -> None:
        """
        Changes manually the functional poni parameters of pygix
        """
        if not self._transform:
            return
        
        try:
            new_poni = PoniFile(data=dict_poni)
            self._transform._init_from_poni(new_poni)
        except Exception as e:
            logger.error(e)

    @logger_info
    def generate_ponifiles(self, get_relative_address=True) -> str:
        with File(self._h5_filename, 'r+') as f:
            dataset = f[PONI_GROUP_KEY][PONIFILE_DATASET_KEY]
            for ponifile in dataset:
                ponifile = ponifile.decode(ENCODING_FORMAT)
                ponifile = Path(ponifile).as_posix()
                if get_relative_address:
                    ponifile = Path(ponifile).relative_to(self._root_dir).as_posix()
                yield ponifile
        
    @logger_info
    def get_all_ponifiles(self, get_relative_address=True) -> list:
        ponifile_list = list(self.generate_ponifiles(get_relative_address=get_relative_address))
        return ponifile_list

    @logger_info
    def activate_ponifile(self, poni_filename=str()) -> None:    
        if not poni_filename:
            self.active_ponifile = None
            return
        
        poni_filename = Path(poni_filename)

        try:
            if poni_filename.is_absolute():
                poni_filename = poni_filename.as_posix()            
            else:
                poni_filename = self._root_dir.joinpath(poni_filename).as_posix()
        except Exception as e:
            self.active_ponifile = None
            return    

        # Proceed only if the requested ponifiles is already stored
        stored_ponifiles = self.get_all_ponifiles(get_relative_address=False)

        if poni_filename in stored_ponifiles:

            self.active_ponifile = poni_filename

            self.update_grazinggeometry()


        else:
            logger.info(f"Ponifile {poni_filename} is not stored in the .h5")
            self.active_ponifile = None
            return           

        # Update the GrazingGeometry instance
        # self.update_grazinggeometry()

    @logger_info
    def get_poni_dict(self):
        try:
            detector = self._transform.detector
        except Exception as e:
            logger.error(f"{e}: Detector could not be retrieved.")
            return
        try:
            detector_config = self._transform.detector.get_config()
        except Exception as e:
            logger.error(f"{e}: Detector could not be retrieved.")
            return
        try:
            wave = self._transform._wavelength
        except Exception as e:
            logger.error(f"{e}: Wavelength could not be retrieved.")
            return
        try:
            dist = self._transform._dist
        except Exception as e:
            logger.error(f"{e}: Distance could not be retrieved.")
            return
        
        # Pixel 1
        try:
            pixel1 = self._transform.pixel1
        except Exception as e:
            pixel1 = None
            logger.error(f"{e}: Pixel 1 could not be retrieved.")
            return
        if not pixel1:
            try:
                pixel1 = detector_config.pixel1
            except Exception as e:
                logger.error(f"{e}: Pixel 1 could not be retrieved.")
                return
        # Pixel 2
        try:
            pixel2 = self._transform.pixel2
        except Exception as e:
            pixel2 = None
            logger.error(f"{e}: Pixel 2 could not be retrieved.")
            return
        if not pixel2:
            try:
                pixel2 = detector_config.pixel2
            except Exception as e:
                logger.error(f"{e}: Pixel 2 could not be retrieved.")
                return

        # Shape
        try:
            shape = self._transform.detector.max_shape
        except Exception as e:
            shape = None
            logger.error(f"{e}: Shape could not be retrieved from detector.")
        if not shape:
            try:
                shape = detector_config.max_shape
            except Exception as e:
                logger.error(f"{e}: Shape could not be retrieved from detector-config.")
                return

        try:
            poni1 = self._transform._poni1
        except Exception as e:
            logger.error(f"{e}: PONI 1 could not be retrieved from h5.")
            return
        try:
            poni2 = self._transform._poni2
        except Exception as e:
            logger.error(f"{e}: PONI 2 could not be retrieved from h5.")
            return
        try:
            rot1 = self._transform._rot1
        except Exception as e:
            logger.error(f"{e}: Rotation 1 could not be retrieved from h5.")
            return
        try:
            rot2 = self._transform._rot2
        except Exception as e:
            logger.error(f"{e}: Rotation 2 could not be retrieved from h5.")
            return
        try:
            rot3 = self._transform._rot3
        except Exception as e:
            logger.error(f"{e}: Rotation 3 could not be retrieved from h5.")
            return
        
        poni_dict = {
            PONI_KEY_VERSION : 2,
            PONI_KEY_DETECTOR : detector.name,
            PONI_KEY_BINNING : detector._binning,
            PONI_KEY_DETECTOR_CONFIG : detector_config,
            PONI_KEY_WAVELENGTH : wave,
            PONI_KEY_DISTANCE : dist,
            PONI_KEY_PIXEL1 : pixel1,
            PONI_KEY_PIXEL2 : pixel2,
            PONI_KEY_SHAPE1 : shape[0],
            PONI_KEY_SHAPE2 : shape[1],
            PONI_KEY_PONI1 : poni1,
            PONI_KEY_PONI2 : poni2,
            PONI_KEY_ROT1 : rot1,
            PONI_KEY_ROT2 : rot2,
            PONI_KEY_ROT3 : rot3,
        }
        return poni_dict

    #########################################################
    ######### PYGIX CONNECTIONS ######################
    #########################################################

    @logger_info
    def update_grazinggeometry(self, poni_filename='') -> None:
        """
        If there is an active ponifile, inherits the methods from Transform class (pygix module)
        """        
        if not poni_filename:
            poni_filename = self.active_ponifile

        if not poni_filename:
            logger.info(f"No active ponifile. GrazingGeometry was not updated")            
            return
        if not Path(poni_filename).is_file():
            logger.info(f"The .poni file {poni_filename} does not exist.")
            return

        # Load the ponifile
        try:
            self._transform.load(poni_filename)
            self.load(poni_filename)
            logger.info(f"Loaded poni file: {poni_filename}")
        except Exception as e:
            logger.error(f"{e}: Ponifile could not be loaded to GrazingGeometry")
        
        # Update default incident and tilt angles
        try:
            self.update_incident_tilt_angle()
        except Exception as e:
            logger.error(f"{e}: angles could not be updated.")

    @logger_info
    def update_angles(self, sample_name=str(), list_index=list()):
        iangle = self.get_incident_angle(
            sample_name=sample_name,
            sample_relative_address=True,
            index_list=list_index,
        )
        tangle = self.get_tilt_angle(
            sample_name=sample_name,
            sample_relative_address=True,
            index_list=list_index,
        )
        self.update_incident_tilt_angle(
            incident_angle=iangle,
            tilt_angle=tangle,
        )

    @logger_info
    def update_incident_tilt_angle(self, incident_angle=0.0, tilt_angle=0.0):
        """
        Update the incident and tilt angles inherited from GrazingGeometry

        Keyword Arguments:
            incident_angle -- (default: {0.0})
            tilt_angle --  (default: {0.0})
        """        
        # Incident angle
        try:
            self._transform.set_incident_angle(
                incident_angle=incident_angle,
            )
            logger.info(f"Incident angle set at {incident_angle}")
        except Exception as e:
            logger.error(f"{e}: Incident angle could not be updated.")

        # Tilt angle
        try:
            self._transform.set_tilt_angle(
                tilt_angle=tilt_angle,
            )
            logger.info(f"Tilt angle set at {tilt_angle}")
        except Exception as e:
            logger.error(f"{e}: Tilt angle could not be updated.")

    @logger_info
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
            self._transform.set_sample_orientation(
                sample_orientation=sample_orientation,
            )
            logger.info(f"The sample orientation (pygix) is set at {sample_orientation}.")
        except Exception as e:
            logger.error(f"The sample orientation (pygix) could not be updated.")

    #####################################
    ###### HDF5 METHODS #################
    #####################################

    @logger_info
    def create_group(
        self,
        h5_filename='',
        root_group_address='.', 
        group_name=str(),
        ):
        if not h5_filename:
            h5_filename = self._h5_filename

        print(000000)
        print(group_name)
        

        with File(self._h5_filename, 'r+') as f:
            # Returns if it contains the dataset already
            if f[root_group_address].__contains__(group_name):
                logger.debug(f"{group_name} exists already in {root_group_address}.")
                return
            else:
                try:
                    f[root_group_address].create_group(
                        name=str(group_name),
                    )
                    logger.debug(f"{group_name} was created in {root_group_address}.")
                except Exception as e:
                    logger.error(f"{e}: {group_name} could not be created in {root_group_address}.")

    @logger_info
    def create_dataset_path(self, group_address='.', dset_name=str(), dtype=FORMAT_STRING, shape=DEFAULT_SHAPE_1D, maxshape=MAXSHAPE_1D_RESIZE,):
        with File(self._h5_filename, 'r+') as f:
            # Returns if it contains the dataset already
            if f[group_address].__contains__(dset_name):
                logger.debug(f"{dset_name} exists already in {group_address}.")
                return
            else:
                try:
                    f[group_address].create_dataset(
                        name=dset_name,
                        shape=shape,
                        maxshape=maxshape,
                        dtype=dtype,
                    )
                    logger.debug(f"{dset_name} was created in {group_address}")
                except Exception as e:
                    logger.error(f"{e}: {dset_name} could not be created in {group_address}")


    @logger_info
    def create_dataset_float(self, group_address='.', dset_name=str(), dtype=FORMAT_FLOAT, shape=DEFAULT_SHAPE_1D, maxshape=MAXSHAPE_1D_RESIZE,):
        with File(self._h5_filename, 'r+') as f:
            # Returns if it contains the dataset already
            if f[group_address].__contains__(dset_name):
                logger.debug(f"{dset_name} exists already in {group_address}.")
                return
            else:
                try:
                    f[group_address].create_dataset(
                        name=dset_name,
                        shape=shape,
                        maxshape=maxshape,
                        dtype=dtype,
                    )
                    logger.debug(f"{dset_name} was created in {group_address}")
                except Exception as e:
                    logger.error(f"{e}: {dset_name} could not be created in {group_address}")

    @logger_info
    def create_group_samples(self, h5_filename=''):
        self.create_group(
            h5_filename=h5_filename,
            group_name=SAMPLE_GROUP_KEY,
        )

    @logger_info
    def create_group_ponifiles(self, h5_filename):
        self.create_group(
            h5_filename=h5_filename,
            group_name=PONI_GROUP_KEY,
        )
        self.create_ponifile_dset()


    @logger_info
    def create_ponifile_dset(self):
        self.create_dataset_path(
            group_address=PONI_GROUP_KEY,
            dset_name=PONIFILE_DATASET_KEY,
        )


    @logger_info
    def create_sample(self, sample_name=str()):

        # Define the name, absolute and relative
        sample_name = Path(sample_name)

        if sample_name.is_absolute():
            abs_address = sample_name.as_posix()
            rel_address = sample_name.relative_to(self._root_dir).as_posix()
        else:
            abs_address = self._root_dir.joinpath(sample_name).as_posix()
            rel_address = sample_name.as_posix()

        # Write some attributes
        dict_init_sample = {
            CLASS_KEY : SAMPLE_KEY,
            DATETIME_KEY : date_prefix(),
            ABS_ADDRESS_KEY : abs_address,
            REL_ADDRESS_KEY : rel_address,
        }

        sample_name = sample_name.as_posix().replace('/', '\\')
        self.create_group(
            root_group_address=SAMPLE_GROUP_KEY,
            group_name=sample_name,
        )
        self.h5_write_attrs_in_group(
            dict_attrs=dict_init_sample,
            group_address=f"{SAMPLE_GROUP_KEY}/{sample_name}",
        )

        self.create_data_dset(sample_name=sample_name)
        self.create_metadata_group(sample_name=sample_name)




    # @logger_info
    # def new_sample(self, sample_name=str()):
    #     # sample_name = sample_name.replace('/', '_')
    #     sample_name = Path(sample_name)     


    #     if sample_name.is_absolute():
    #         abs_address = sample_name.as_posix()
    #         rel_address = sample_name.relative_to(self._root_dir).as_posix()
    #     else:
    #         abs_address = self._root_dir.joinpath(sample_name).as_posix()
    #         rel_address = sample_name.as_posix()

    #     # Write some attributes
    #     dict_init_sample = {
    #         CLASS_KEY : SAMPLE_KEY,
    #         DATETIME_KEY : date_prefix(),
    #         ABS_ADDRESS_KEY : abs_address,
    #         REL_ADDRESS_KEY : rel_address,
    #     }

    #     # Define relative and absolute addresses
    #     # 
    #     sample_name = sample_name.as_posix().replace('/', '\\')

    #     # Check if the sample does exist
    #     self.create_sample(
    #         sample_name=sample_name,
    #     )

    #     self.h5_write_attrs_in_group(
    #         dict_attrs=dict_init_sample,
    #         group_address=f"{SAMPLE_GROUP_KEY}/{sample_name}",
    #     )

    #     self.create_data_dset(sample_name=sample_name)
    #     self.create_metadata_group(sample_name=sample_name)


    # @debug_info
    # def contains_group(self, sample_name=str(), group_address='.') -> bool:
    #     """
    #     Checks if the folder already exist in a specific address

    #     Keyword Arguments:
    #         folder_name -- name of the new folder (Group) (default: {str()})
    #         group_address -- address of the Group inside the H5 file (default: {str()})

    #     Returns:
    #         exists (True) or not (False)
    #     """
    #     try:
    #         is_inside = self._file[group_address].__contains__(str(sample_name))
    #         return is_inside
    #     except Exception as e:
    #         logger.error(f"{e}Error while opening Group {group_address} to check {sample_name} Group. Trying to opening the file")
    #     try:
    #         self._open
    #         is_inside = self._file[group_address].__contains__(str(sample_name))
    #         self._close
    #         return is_inside
    #     except Exception as e:
    #         logger.error(f"{e}Error while opening Group {group_address} to check {sample_name} Group again.")

    # @debug_info
    # def append_to_dataset(self, group_address='.', sample_name=str(), dataset_name='Data', new_data=np.array([])) -> None:
    #     """
    #     Append new data to 'Data' dataset, inside a specific folder

    #     Keyword Arguments:
    #         folder_name -- name of the new folder (Group) (default: {str()})
    #         dataset_name -- 'Data' is the name of the dataset where the 2D maps or just the addresses of the files are stored (default: {'Data'})
    #         new_data -- list of data to be iterated and appended in the dataset (default: {np.array([])})
    #     """      
    #     self._open

    #     # Get the current shape of the dataset
    #     initial_shape = np.array(self._file[group_address][sample_name][dataset_name].shape)
    #     expanded_shape = np.copy(initial_shape)
    #     num_files = initial_shape[0]

    #     # How many new layers should we add
    #     new_layers = new_data.shape[0]
    #     expanded_shape[0] += new_layers
    #     expanded_shape = tuple(expanded_shape)
        
    #     #Resizing
    #     try:
    #         self._file[group_address][sample_name][dataset_name].resize((expanded_shape))
    #         logger.info(f"Shape of dataset reseted from {tuple(initial_shape)} to {expanded_shape}")
    #     except Exception as e:
    #         logger.error(f"{e} Error during reshaping the dataset {dataset_name} from {tuple(initial_shape)} to {expanded_shape}")

    #     # Appending
    #     for ind in range(new_layers):
    #         try:
    #             self._file[group_address][sample_name][dataset_name][num_files + ind] = new_data[ind]
    #             logger.info(f"Appended data with index {ind} successfully.")
    #         except Exception as e:
    #             logger.error(f"{e}: Error while appending {new_data[ind]}.")

    # @log_info
    # def update_sample(self, sample_name=str(), data_filenames=list(), get_2D_array=False, relative_to_root=True) -> None:
    #     """
    #     Creates or updates a folder (Group) with data and metadata from a list of files

    #     Keyword Arguments:
    #         folder_name -- name of the folder (Group) where the data/metadata will be stored (default: {str()})
    #         filename_list -- list of path filenames where the data/metadata will be extracted (default: {list()})
    #         get_2D_array -- yields a packed array with the 2D maps if True, yields a packed array with the encoded filenames if False (default: {True})
    #     """
    #     self._open
    #     self._update_sample(
    #         sample_name=sample_name,
    #         data_filenames=data_filenames,
    #         relative_to_root=relative_to_root,
    #         get_2D_array=get_2D_array,
    #     )
    #     self._close

    @logger_info
    def update_sample(self, sample_name=str(), data_filenames=list(), get_2D_array=False) -> None:
        """
        Creates or updates a folder (Group) with data and metadata from a list of files

        Keyword Arguments:
            folder_name -- name of the folder (Group) where the data/metadata will be stored (default: {str()})
            filename_list -- list of path filenames where the data/metadata will be extracted (default: {list()})
            get_2D_array -- yields a packed array with the 2D maps if True, yields a packed array with the encoded filenames if False (default: {True})
        """
        # Create the sample first
        print(1111)
        print(sample_name)
        self.create_sample(
            sample_name=sample_name,
        )

        sample_name = self.get_sample_address(
            sample_name=sample_name,
            sample_relative_address=False,
        )
        print(333333)
        print(sample_name)


        # Append Data filenames
        if get_2D_array:
            return
        else:
            self.append_datafile_list(
                sample_name=sample_name,
                datafile_list=data_filenames,
            )
        
        # Append MetaData values
        dict_metadata = defaultdict(list)

        for header in self.generator_file_header(filenames=data_filenames):
            for k,v in header.items():
                try:
                    v = float(v)
                except Exception as e:
                    v = str(v)
                finally:
                    dict_metadata[k].append(v)

        # print(dict_metadata)
        for k,v in dict_metadata.items():

            if isinstance(v[0], float):
                self.create_metadata_dset_float(
                        sample_name=sample_name,
                        metadata_key=k,
                    )
            elif isinstance(v[0], str):
                self.create_metadata_dset_str(
                        sample_name=sample_name,
                        metadata_key=k,
                    )
            else:
                continue

            self.append_metadata_values(
                    sample_name=sample_name,
                    metadata_key=k,
                    value_list=v,
                )                


        # First, get the packed data and metadata for every filename
        # merged_data, merged_metadata = self.get_merged_data_and_metadata(
        #     filename_list=data_filenames, 
        #     get_2D_array=get_2D_array,
        #     # relative_to_root=relative_to_root,
        # )

        # # Get the names of samples and files to write in the .h5 file
        # if relative_to_root:
        #     sample_name = Path(sample_name)
        #     data_filenames = [str(Path(file).relative_to(sample_name)) for file in data_filenames]            
        #     sample_name = str(sample_name.relative_to(self._root_dir))



        # Create the DataSet 'data'
        # self.h5_create_data_dset(sample_name=sample_name)
        # # if not self._file[SAMPLE_GROUP_KEY][sample_name].__contains__(DATA_KEY):
        # #     self._file[SAMPLE_GROUP_KEY][sample_name].create_dataset(
        # #         DATA_KEY, 
        # #         data=merged_data, 
        # #         chunks=True, 
        # #         maxshape=(None, None, None,),
        # #         # dtype=h5py.string_dtype(encoding='utf-8'),
        # #     )
        # #     logger.info(f"Data dataset in {sample_name} group created.")
        # #     logger.info(f"Added in {sample_name}-Data shape: {merged_data.shape}")
        # # else:
        # #     logger.info(f"Data dataset in {sample_name} group already existed. Go to append.")
        # #     self.append_to_dataset(
        # #         group_address=SAMPLE_GROUP_KEY,
        # #         sample_name=sample_name,
        # #         new_data=merged_data,
        # #         dataset_name=DATA_KEY,
        # #     )

        # # Create or update METADATA group with datasets
        # self.h5_create_metadata_dset()

        # if not self._file[SAMPLE_GROUP_KEY][sample_name].__contains__(METADATA_KEY):
        #     self._file[SAMPLE_GROUP_KEY][sample_name].create_group(METADATA_KEY)
        #     logger.info(f"Metadata group in {sample_name} group created.")
        # else:
        #     logger.info(f"Metadata group in {sample_name} group already existed. Continue.")

        # for key,value in merged_metadata.items():
        #     # Value is a list here! Convert to np.array
        #     value = np.array(value)

        #     # Creates dataset for the key
        #     if not self._file[SAMPLE_GROUP_KEY][sample_name][METADATA_KEY].__contains__(key):

        #         # Try to create dataset with the standard format (floats)
        #         try:
        #             self._file[SAMPLE_GROUP_KEY][sample_name][METADATA_KEY].create_dataset(key, data=np.array(value), chunks=True, maxshape=(None,))
        #             logger.info(f"Dataset {key} in {sample_name}-Metadata was created.")
        #             continue
        #         except:
        #             logger.info(f"Dataset could not be created with the standard format for the key {key}, value {value}.")

        #         # If it did not work, try to create dataset encoding the dataset as bytes format
        #         try:
        #             logger.info("Trying to create dataset with encoded data.")
        #             bytes_array = np.array([str(item).encode() for item in value])
        #             self._file[SAMPLE_GROUP_KEY][sample_name][METADATA_KEY].create_dataset(key, data=bytes_array, chunks=True, maxshape=(None,))
        #             logger.info(f"Dataset {key} in {sample_name}-Metadata was created. Encoding worked.")
        #             continue
        #         except:
        #             logger.info(f"Dataset could not be created with the encoded format for the key {key}, value {value}.")

        #     # Appends dataset for the key if the dataset already existed
        #     else:
        #         subfolder = f"{sample_name}/{METADATA_KEY}"
        #         # Try to append dataset with the standard format (floats)

        #         try:
        #             self.append_to_dataset(
        #                 group_address=SAMPLE_GROUP_KEY,
        #                 sample_name=subfolder,
        #                 new_data=value, 
        #                 dataset_name=key,
        #             )
        #             logger.info(f"Dataset {key} in {subfolder} was appended.")
        #             continue
        #         except:
        #             logger.info(f"Dataset could not be appended with the standard format for the key {key}, value {value}.")

        #         # If it did not work, try to append dataset encoding the dataset as bytes format
        #         try:
        #             logger.info("Trying to append dataset with encoded data.")
        #             bytes_array = np.array([str(item).encode() for item in value])
        #             self.append_to_dataset(
        #                 group_address=SAMPLE_GROUP_KEY,
        #                 sample_name=subfolder, 
        #                 new_data=bytes_array, 
        #                 dataset_name=key,
        #             )
        #             logger.info(f"Dataset {key} in {sample_name}-Metadata was appended. Encoding worked.")
        #             continue
        #         except:
        #             logger.info(f"Dataset could not be appended with the encoded format for the key {key}, value {value}.")












    # @debug_info
    # def get_merged_data_and_metadata(
    #     self, 
    #     filename_list=list(), 
    #     get_2D_array=True, 
    #     absolute_address=True,
    #     ):
    #     """
    #     Use FabIO module to get the data (arrays) and metadata from 2D detector patterns
    #     If not get_2D_array, it yields the encoded name of the file, not the real 2D array

    #     Keyword Arguments:
    #         filenames -- list of strings with the full address of the data files (default: {list()})
    #         get_2D_array -- yields a packed array with the 2D maps if True, yields a packed array with the encoded filenames if False (default: {True})

    #     Returns:
    #         _description_
    #     """
    #     # Init dataset and header
    #     merged_dataset = np.array([])
    #     merged_header = defaultdict(list)            
        
    #     for index_file, (data, header) in enumerate(
    #         self.generator_fabio_data_header(
    #             filename_list=filename_list,
    #             get_2D_array=get_2D_array,
    #             relative_to_root=absolute_address,
    #         )):
    #         # Pack data
    #         try:
    #             if index_file == 0:
    #                 merged_dataset = np.array([data])
    #             else:
    #                 merged_dataset = np.concatenate((merged_dataset, [data]), axis=0)
    #             logger.info(f"Merged Data dataset was extracted.")
    #         except Exception as e:
    #             logger.error(f"{e}: Error while packing data at {index_file}")
            
    #         # Pack metadata
    #         for key,value in header.items():
    #             try:
    #                 value = float_str(value)
    #                 merged_header[key].append(value)
    #             except Exception as e:
    #                 logger.error(f"{e}: Error while packing metadata at key: {key}, value {value}")
    #         logger.info(f"Merged all Metadata datasets.")
    #     return merged_dataset, merged_header



    @logger_info
    def generator_file_header(self, filenames=list()):
        for file in filenames:
            # Open a EdfClass instance
            try:
                edf = EdfClass(
                    filename=file,
                )
                logger.debug(f"EdfClass with filename {file} was created.")
            except Exception as e:
                logger.error(f"{e}: EdfClass instance with filename {file} could not be created.")
                continue
        
            # Yield data or data addresses and header
            try:
                header = edf.get_header()
                logger.debug(f"Data and header extracted successfully.")
            except Exception as e:
                logger.error(f"{e}: Error while fabio handling at {file}")
                header = None, None
            yield header


    # @debug_info
    # def generator_fabio_data_header(self, filename_list=[], get_2D_array=True, relative_to_root=True):
    #     """
    #     Use FabIO module to generate the data and metadata from a list of files
    #     If not get_2D_array, it yields the encoded name of the file, not the real 2D array

    #     Keyword Arguments:
    #         filenames -- list of strings with the full address of the data files (default: {[]})
    #         get_2D_array -- yields a packed array with the 2D maps if True, yields a packed array with the encoded filenames if False (default: {True})

    #     Yields:
    #         np.array : 2D map or encoded filename
    #         dict : header dictionary from FabIO
    #     """
    #     for file in filename_list:
    #         # Open a EdfClass instance
    #         try:
    #             edf = EdfClass(
    #                 filename=file,
    #             )
    #             logger.info(f"EdfClass with filename {file} was created.")
    #         except Exception as e:
    #             logger.error(f"{e}: EdfClass instance with filename {file} could not be created.")
    #             continue

    #         # Yield data or data addresses and header
    #         try:
    #             if get_2D_array:
    #                 data, header = edf.get_data(), edf.get_header()
    #             else:
    #                 if relative_to_root:
    #                     filename = Path(file)
    #                     sample_name = filename.parent
    #                     filename = filename.relative_to(sample_name)
    #                 else:
    #                     filename = file
    #                 data, header = np.array(([[str(filename).encode()]])), edf.get_header()
    #             logger.info(f"Data and header extracted successfully.")
    #         except Exception as e:
    #             logger.error(f"{e}: Error while fabio handling at {filename}")
    #             data, header = None, None
    #         yield data, header

    @logger_info
    def generator_samples(self, get_group_name=True, get_relative_address=False) -> str:
        with File(self._h5_filename, 'r+') as f:
            for sample in  f[SAMPLE_GROUP_KEY].keys():
                if get_group_name:
                    yield sample
                else:
                    if get_relative_address:
                        sample_name = f[SAMPLE_GROUP_KEY][sample].attrs[REL_ADDRESS_KEY]
                    else:
                        sample_name = f[SAMPLE_GROUP_KEY][sample].attrs[ABS_ADDRESS_KEY]        
                    yield sample_name

    @logger_info
    def get_all_samples(self, get_relative_address=True) -> list:
        list_samples = sorted(
            self.generator_samples(
                get_group_name=False,
                get_relative_address=get_relative_address,
            ),
        )
        return list_samples

    @logger_info
    def generator_all_files(self) -> str:
        """
        Yields the names of every file stored in the .h5 file

        Parameters:
        None

        Yields:
        str : fullpath of stored filenames
        """
        for sample in self.generator_samples(get_group_name=True):
            for file in self.generator_files_in_sample(
                sample_name=sample,
                is_group_name=True,
                get_relative_address=False,
                ):
                yield file

    @logger_info
    def get_dict_files(self, relative_address=True):
        dict_files = defaultdict(set)
        for file in self.generator_all_files():
            sample_name = Path(file).parent
            if relative_address:
                file = Path(file).relative_to(sample_name).as_posix()
                sample_name = sample_name.relative_to(self._root_dir).as_posix()
            else:
                file = Path(file).as_posix()
                sample_name = sample_name.as_posix()

            dict_files[sample_name].add(file)
        return dict_files

    @logger_info
    def get_all_files(self) -> list:
        """
        Returns a list with all the stored files in the h5 File

        Keyword Arguments:
            decode -- _description_ (default: {True})

        Returns:
            _description_
        """
        list_files = sorted(self.generator_all_files())
        return list_files

    ##################################################
    ############# SAMPLES/FILES METHODS ##############
    ##################################################

    @logger_info
    def set_pattern(self, pattern=".edf"):
        self._pattern = pattern

    @logger_info
    def search_new_datafiles(
        self, 
        pattern="*.edf",
        ):
        # searched_files = [file.as_posix() for file in self._root_dir.rglob(pattern) if file.parent != self._root_dir]
        searched_files = self._root_dir.rglob(pattern)
        dict_files = get_dict_files(
            list_files=searched_files,
        )

        # Filter only the new data
        dict_files_in_h5 = self.get_dict_files(relative_address=False)

        dict_new_files = get_dict_difference(
            large_dict=dict_files,
            small_dict=dict_files_in_h5,
        )

        return dict_new_files

    @logger_info
    def update_datafiles(
        self, 
        dict_new_files=dict(), 
        pattern='*.edf', 
        search=False,
        ):

        # Search for new files
        if dict_new_files:
            dict_new_files = dict_new_files
        elif search:
            dict_new_files = self.search_new_datafiles(
                pattern=pattern,
            )
        logger.info(f"{INFO_H5_NEW_DICTIONARY_FILES}: {str(dict_new_files)}")

        # Store in the .h5 file by folder and its own list of files
        for sample_name, file_list in dict_new_files.items():
            data_filenames = sorted(file_list)

            self.update_sample(
                sample_name=sample_name,
                data_filenames=data_filenames,
                get_2D_array=False,
            )

            logger.info(f"Finished with folder: {sample_name}.")
        logger.info(INFO_H5_FILES_UPDATED)

    @logger_info
    def get_all_files_from_sample(
        self, 
        sample_name=str(),
        is_group_name=True,
        sample_relative_address=True, 
        get_relative_address=True,
        ):
        list_files = sorted(
            self.generator_files_in_sample(
                sample_name=sample_name,
                is_group_name=is_group_name,
                sample_relative_address=sample_relative_address,
                get_relative_address=get_relative_address,
            ))
        return list_files

    @logger_info
    def get_sample_address(
        self, 
        sample_name='', 
        sample_relative_address=True,
        ):
        with File(self._h5_filename, 'r+') as f:
            if sample_relative_address:
                for sample in f[SAMPLE_GROUP_KEY].keys():
                    if f[SAMPLE_GROUP_KEY][sample].attrs[REL_ADDRESS_KEY] == sample_name:
                        return sample
                logger.info(f"There is no sample with rel. address {sample_name}.")
                return
            else:
                for sample in f[SAMPLE_GROUP_KEY].keys():
                    if f[SAMPLE_GROUP_KEY][sample].attrs[ABS_ADDRESS_KEY] == sample_name:
                        return sample
                logger.info(f"There is no sample with abs. address {sample_name}.")
                return

    @logger_info
    def generator_files_in_sample(
        self, 
        sample_name=str(),
        is_group_name=True,
        sample_relative_address=True, 
        get_relative_address=True,
        ):

        if is_group_name:
            sample_name=sample_name
        else:
            sample_name = self.get_sample_address(
                sample_name=sample_name,
                sample_relative_address=sample_relative_address,
            )

        if not sample_name:
            return

        with File(self._h5_filename, 'r+') as f:
            dataset = f[SAMPLE_GROUP_KEY][sample_name][DATA_KEY]
            for filename in dataset:
                filename = filename.decode(ENCODING_FORMAT)
                if get_relative_address:
                    # sample_name = f[SAMPLE_GROUP_KEY][sample_name].attrs[ABS_ADDRESS_KEY]
                    # print(5555)
                    # print(filename)
                    # print(sample_name)
                    # filename = Path(filename).relative_to(Path(sample_name).as_posix()).as_posix()
                    filename = Path(filename).name
                yield filename

    @logger_info
    def get_metadata_dataset(
        self, 
        sample_name=str(), 
        sample_relative_address=True,
        key_metadata=str(),
        ) -> np.array:

        sample_name = self.get_sample_address(
            sample_name=sample_name,
            sample_relative_address=sample_relative_address,
        )

        if not sample_name:
            return

        with File(self._h5_filename, 'r+') as f:
            try:
                dataset = f[SAMPLE_GROUP_KEY][sample_name][METADATA_KEY][key_metadata][()]
            except Exception as e:
                logger.error(f"{e}: dataset {key_metadata} could not be accessed.")
                return
            return dataset

    @logger_info
    def get_metadata_value(
        self, 
        sample_name=str(),
        sample_relative_address=True,
        key_metadata=str(), 
        index_list=list(),
        ) -> float:
        """
        Returns the metadata value of a specific folder and file (associated to index)

        Parameters:
        folder_name(str) : name of the folder (Group) in the first level of hierarchy
        key_metadata(str) : key(name) of the asked counter/motor
        index_list(int, list) : integer or list of integers which are the file index inside the folder (Group)

        Returns:
        float, str : value of the counter/motor inside the metadata
        """
        dataset = self.get_metadata_dataset(
            sample_name=sample_name,
            sample_relative_address=sample_relative_address,
            key_metadata=key_metadata,
        )

        if dataset is None:
            return

        if isinstance(index_list, int):
            value = dataset[index_list]
        elif isinstance(index_list, list):
            if dataset.dtype == FORMAT_FLOAT:
                value = np.mean(
                    np.array(
                        [dataset[index] for index in index_list]
                    )
                )
            else:
                value = dataset[index_list[-1]]
        return value

    @logger_info
    def get_metadata_dataframe(
        self, 
        sample_name=str(),
        sample_relative_address=True,
        list_keys=list(),
        ) -> pd.DataFrame:

        list_files_in_sample = self.get_all_files_from_sample(
            sample_name=sample_name,
            is_group_name=False,
            sample_relative_address=sample_relative_address,
        )

        if not list_files_in_sample:
            return

        short_metadata = defaultdict(list)

        for filename in list_files_in_sample:
            short_name = Path(filename).name
            # Always append the name of the file
            short_metadata[FILENAME_KEY].append(short_name)

            for key in list_keys:
                try:
                    dataset_key = self.get_metadata_dataset(
                        sample_name=sample_name,
                        sample_relative_address=sample_relative_address,
                        key_metadata=key,
                    )
                    short_metadata[key] = list(dataset_key)
                except:
                    logger.error(f"Error during acceeding to Metadata dataset with key: {key}")
        dataframe = pd.DataFrame(short_metadata)
        logger.info(f"The dataframe has size {dataframe.size}.")
        return dataframe

    @logger_info
    def get_all_metadata_keys_from_sample(
        self, 
        sample_name=str(), 
        sample_relative_address=True,
        ):
        list_keys = sorted(
            self.generator_metadata_keys_from_sample(
                sample_name=sample_name,
                sample_relative_address=sample_relative_address,
                ))
        return list_keys

    @logger_info
    def generator_metadata_keys_from_sample(
        self, 
        sample_name=str(), 
        sample_relative_address=True,
        ):
        sample_name = self.get_sample_address(
            sample_name=sample_name,
            sample_relative_address=sample_relative_address,
        )

        if not sample_name:
            return
        
        with File(self._h5_filename, 'r+') as f:
            list_keys = f[SAMPLE_GROUP_KEY][sample_name][METADATA_KEY].keys()
            for key in list_keys:
                yield key

    @logger_info
    def get_filename_from_index(
        self, 
        sample_name=str(),
        sample_relative_address=True,
        index_list=list(),
        ):
        print(sample_name)
        print(sample_relative_address)
        print(index_list)
        sample_name = self.get_sample_address(
            sample_name=sample_name,
            sample_relative_address=sample_relative_address,
        )

        if not sample_name:
            return

        with File(self._h5_filename, 'r+') as f:
            if isinstance(index_list, int):
                index_list = [index_list]
            if len(index_list) == 1:
                filename = bytes.decode(f[SAMPLE_GROUP_KEY][sample_name][DATA_KEY][index_list[0]])
            else:
                filename = bytes.decode(f[SAMPLE_GROUP_KEY][sample_name][DATA_KEY][index_list[-1]])
                filename = filename.replace(".edf", "_average.edf")
        return filename

    @logger_info
    def get_sample_index_from_filename(self, filename=str()):
        """
        Searches the filename in the .h5 Groups and returns the name of the folder and the index of the file in the Group

        Parameters:
        filename(str) : string of the filename to be searched

        Returns:
        str : string with the name of the folder in the .h5 file
        int : index of the filename inside the folder
        """
        # sample_name = str(Path(filename).parent.relative_to(self._root_dir))
        sample_name_abs = Path(filename).parent.as_posix()

        sample_address = self.get_sample_address(
            sample_name=sample_name_abs,
            sample_relative_address=False,
        )

        if not sample_address:
            return

        # if not self.contains_group(sample_name=sample_name, group_address=SAMPLE_GROUP_KEY):
        #     logger.info(f"There is no Group with the name {sample_name}. Returns.")
        #     return

        for index, file in enumerate(
            self.generator_files_in_sample(
                sample_name=sample_address,
                is_group_name=True,
            )):
            if file == filename:
                logger.info(f"Found match with the filename at index {index}")
                return sample_name, index
        logger.info(f"No matches were found with the filename {filename}")
        return None, None

    #####################################
    ###### EDF METHODS ##########
    #####################################

    @logger_info
    def get_Edf_instance(
        self, 
        full_filename=str(),
        sample_name=str(),
        sample_relative_address=True,
        index_file=int(),
        ):

        # Take the full filename
        if full_filename:
            filename = full_filename
        else:
            try:
                filename = self.get_filename_from_index(
                    sample_name=sample_name,
                    sample_relative_address=sample_relative_address,
                    index_list=index_file,
                )

                logger.info(f"Trying to open sample name {filename}")
            except Exception as e:
                logger.error(f"{e}: file could not be found in the repository. Sample name {sample_name}, index {index_file}.")

        # Open the Edf instance
        try:
            Edf_instance = EdfClass(
                filename=filename,
            )
        except Exception as e:
            logger.error(f"{e}: Edf instance could not be created.")
            Edf_instance = None
        return Edf_instance

    @logger_info
    def get_Edf_data(
        self, 
        sample_name=str(),
        sample_relative_address=True,
        index_list=list(), 
        full_filename=str(),
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
                        full_filename=full_filename,
                        sample_name=sample_name,
                        sample_relative_address=sample_relative_address,
                        index_file=index,
                    ).get_data() for index in index_list
                ]
            ) / len(index_list)
            logger.info(f"New data sample with shape: {data_sample.shape}")
        except Exception as e:
            data_sample = None
            logger.error(f"{e}: Data sample could not be uploaded.")
            return

        if normalized:
            norm_factor = self.get_norm_factor(
                sample_name=sample_name,
                index_list=index_list,
            )
            data_sample = data_sample.astype('float32') / norm_factor

        return data_sample

    #####################################
    ###### INTEGRATION METHODS ##########
    #####################################

    @logger_info
    def map_reshaping(
        self,
        data=None,
    ):
        # ponifile = self.get_active_ponifile()
        try:
            ai = load(self.active_ponifile)
            data_reshape, q, chi = ai.integrate2d(
                data=data,
                npt_rad=1000,
                unit="q_nm^-1",
            )
            logger.info(f"Reshaped map.")
        except Exception as e:
            logger.error(f"Impossible to reshape map with shapes: data {data.shape}.")
            return

        return data_reshape, q, chi

    @logger_info
    def raw_integration(
        self,
        sample_name=str(),
        sample_relative_address=True,
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
                sample_name=sample_name,
                sample_relative_address=sample_relative_address,
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
                sample_name=sample_name,
                index_list=index_list,
            )

        array_compiled = []

        for dict_integration in list_dict_integration:
            if dict_integration[KEY_INTEGRATION] == CAKE_LABEL:
                if dict_integration[CAKE_KEY_TYPE] == CAKE_KEY_TYPE_AZIM:
                    res = self.raw_integration_azimuthal(
                        data=data,
                        norm_factor=norm_factor,
                        dict_integration=dict_integration,
                    )

                elif dict_integration[CAKE_KEY_TYPE] == CAKE_KEY_TYPE_RADIAL:
                    res = self.raw_integration_radial(
                        data=data,
                        norm_factor=norm_factor,
                        dict_integration=dict_integration,
                    )
            elif dict_integration[KEY_INTEGRATION] == BOX_LABEL:
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

    @logger_info
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
        
        p0_range=dict_integration[CAKE_KEY_RRANGE]
        p1_range=dict_integration[CAKE_KEY_ARANGE]
        unit=dict_integration[CAKE_KEY_UNIT]
        npt = dict_integration[CAKE_KEY_ABINS]

        if npt == 0:
            npt=self.calculate_bins(
                radial_range=p0_range,
                unit=unit,
            )

        # Do the integration with pygix/pyFAI
        try:
            logger.info(f"Trying azimuthal integration with: data-shape={data.shape} bins={npt}, p0_range={p0_range}, p1_range={p1_range}, unit={unit}")
            y_vector, x_vector = self._transform.integrate_1d(
                process='sector',
                data=data,
                npt=npt,
                p0_range=p0_range,
                p1_range=p1_range,
                unit=UNIT_GI[unit],
                normalization_factor=float(norm_factor),
                polarization_factor=POLARIZATION_FACTOR,
            )
            logger.info("Integration performed.")
        except Exception as e:
            logger.error(f"{e}: Error during azimuthal integration.")
            return

        return np.array([x_vector, y_vector])

    @logger_info
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
        npt  = int(dict_integration[CAKE_KEY_ABINS])
        p0_range = dict_integration[CAKE_KEY_RRANGE]
        p1_range = dict_integration[CAKE_KEY_ARANGE]

        
        unit = UNIT_GI[dict_integration[CAKE_KEY_UNIT]]
        
        try:
            logger.info(f"Trying radial integration with: npt={npt}, p0_range={p0_range}, p1_range={p1_range}, unit={unit}")
            y_vector, x_vector = self._transform.integrate_1d(
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

    @logger_info
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
        process = DICT_BOX_ORIENTATION[dict_integration[BOX_KEY_DIRECTION]]
        unit=dict_integration[BOX_KEY_INPUT_UNIT]
        try:
            if process == 'opbox':
                p0_range, p1_range = dict_integration[BOX_KEY_OOPRANGE], dict_integration[BOX_KEY_IPRANGE]
                npt = self.calculate_bins(
                    radial_range=dict_integration[BOX_KEY_OOPRANGE],
                    unit=unit,
                )
            elif process == 'ipbox':
                p0_range, p1_range = dict_integration[BOX_KEY_IPRANGE], dict_integration[BOX_KEY_OOPRANGE]
                npt = self.calculate_bins(
                    radial_range=dict_integration[BOX_KEY_IPRANGE],
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
            direction=dict_integration[BOX_KEY_DIRECTION],
        ) for position in p0_range]

        p1_range = [self.get_q_nm(
            value=position,
            input_unit=unit,
            direction=dict_integration[BOX_KEY_DIRECTION],
        ) for position in p1_range]

        # Do the integration with pygix/pyFAI
        try:
            logger.info(f"Trying box integration with: process={process}, npt={npt}, p0_range={p0_range}, p1_range={p1_range}, unit={unit}")
            y_vector, x_vector = self._transform.integrate_1d(
                process=process,
                data=data,
                npt=npt,
                p0_range=p0_range,
                p1_range=p1_range,
                unit=UNIT_GI[unit],
                normalization_factor=float(norm_factor),
                polarization_factor=POLARIZATION_FACTOR,
                # method='bbox',
            )
            x_vector = self.transform_q_units(
                x_vector=x_vector,
                input_unit=dict_integration[BOX_KEY_INPUT_UNIT],
                output_unit=dict_integration[BOX_KEY_OUTPUT_UNIT],
                direction=dict_integration[BOX_KEY_DIRECTION],
            )

            logger.info("Integration performed.")
        except:
            logger.info("Error during box integration.")
            return

        return np.array([x_vector, y_vector])

    @logger_info
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
        return int(round(self._transform._dist / self._transform.get_pixel1() * (np.tan(twotheta2) - np.tan(twotheta1))))

    @logger_info
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
            twotheta = 2 * np.arcsin((q*self._transform._wavelength * 1e9)/(4*np.pi))
        elif unit == 'q_A^-1':
            twotheta = 2 * np.arcsin((q*self._transform._wavelength * 1e10)/(4*np.pi))
        else:
            return
        return np.rad2deg(twotheta) if degree else twotheta

    @logger_info
    def get_q_nm(self, value=0.0, direction='Vertical', input_unit='q_nm^-1') -> float:
        """
            Return a q(nm-1) value from another unit
        """
        if input_unit == 'q_nm^-1':
            return value
        elif input_unit == 'q_A^-1':
            return value
        elif input_unit == '2th_deg':
            return self.twotheta_to_q(twotheta=value, direction=direction, deg=True)
        elif input_unit == '2th_rad':
            return self.twotheta_to_q(twotheta=value, deg=False)
        else:
            return None

    @logger_info
    def twotheta_to_q(self, twotheta=0.0, direction='vertical', deg=True) -> float:
        """
            Returns the q(nm-1) from the 2theta value
        """
        if deg:
            twotheta = np.radians(twotheta)
        try:
            wavelength_nm = self._transform._wavelength * 1e9
        except:
            return
        
        try:
            alpha_inc = np.radians(self._transform._incident_angle)
        except:
            alpha_inc = 0.0
        
        q_horz = 2 * np.pi / wavelength_nm * (np.cos(alpha_inc) * np.sin(twotheta))
        q_vert = 2 * np.pi / wavelength_nm * (np.sin(twotheta) + np.sin(alpha_inc))

        if direction == BOX_KEY_TYPE_VERT:
            return q_horz
        elif direction == BOX_KEY_TYPE_HORZ:
            return q_vert
        else:
            return


    @logger_info
    def transform_q_units(
        self, 
        x_vector=None, 
        input_unit=None, 
        output_unit=None, 
        direction='vertical',
        ):

        if x_vector is None:
            return

        if input_unit == output_unit:
            return x_vector
        
        # From Q
        if input_unit in UNITS_Q:
            if output_unit in UNITS_Q:
                if output_unit in QNM_ALIAS:
                    x_vector *= 10
                elif output_unit in QA_ALIAS:
                    x_vector /= 10
                return x_vector

            elif output_unit in UNITS_THETA:
                if output_unit in DEG_ALIAS:
                    x_vector = self.q_to_twotheta(
                        q=x_vector,
                        unit=input_unit,
                        degree=True,
                    )
                    return x_vector
                elif output_unit in RAD_ALIAS:
                    x_vector = self.q_to_twotheta(
                        q=x_vector,
                        unit=input_unit,
                        degree=False,
                    )
                    return x_vector
        # From TTH
        elif input_unit in UNITS_THETA:
            if output_unit in UNITS_THETA:
                if output_unit in DEG_ALIAS:
                    return x_vector*180/np.pi
                elif output_unit in RAD_ALIAS:
                    return x_vector*np.pi/180
            elif output_unit in UNITS_Q:
                if input_unit in DEG_ALIAS:
                    vector_nm = self.twotheta_to_q(
                        twotheta=x_vector,
                        direction=direction,
                        deg=True,
                    )
                elif input_unit in RAD_ALIAS:
                    vector_nm = self.twotheta_to_q(
                        twotheta=x_vector,
                        direction=direction,
                        deg=False,
                    )

                if output_unit in QNM_ALIAS:
                    return vector_nm
                elif output_unit in QA_ALIAS:
                    return vector_nm/10










    @logger_info
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
                shape = self._transform.get_shape()

            logger.info(f"Shape of the detector: {shape}")
            d2,d1 = np.meshgrid(
                np.linspace(1,shape[1],shape[1]),
                np.linspace(1,shape[0],shape[0]),
            )
            out = np.array([d1,d2])
            return out
        except:
            return None

    @logger_info
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
                scat_z, scat_xy = self._transform.calc_q(
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
                scat_z, scat_xy = self._transform.calc_angles(
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


    @logger_info
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
            