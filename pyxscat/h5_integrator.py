from collections import defaultdict
from pathlib import Path
from pyxscat.gi_integrator import GIIntegrator
from os.path import getctime

from pyFAI.io.ponifile import PoniFile
from pyxscat.edf import EdfClass
from pyxscat.other.other_functions import date_prefix, get_dict_files, get_dict_difference
from pyxscat.other.units import *

import h5py
import numpy as np
import pandas as pd
from silx.io.h5py_utils import File
# from silx.io.nxdata import save_NXdata
from pyxscat.other.integrator_methods import *
from pyxscat.other.setup_methods import *
import os

ENCODING_FORMAT = "UTF-8"
FORMAT_STRING = h5py.string_dtype(ENCODING_FORMAT)
FORMAT_FLOAT = 'float64'

DEFAULT_SHAPE_1D = (0,)
MAXSHAPE_1D_RESIZE = (None,)
DEFAULT_H5_PATH = '.'



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
ABS_ADDRESS_KEY = "absolute_address"
REL_ADDRESS_KEY = "relative_address"

DATAFILE_KEY = "data_filename"
DATANAME_KEY = "data_name"
SAMPLEPATH_KEY = "sample_address"

ENTRY_PONIFILE_KEY = 'entry_ponifiles'


ADDRESS_METADATA_KEYS = '.'
ADDRESS_PONIFILE = '.'

MODE_OVERWRITE = "w"
MODE_READ = "r"
MODE_WRITE = "r+"

PONIFILE_DATASET_KEY = "ponifiles"
PONIFILE_ACTIVE_KEY = "active_ponifile"
WILDCARDS_PONI = '*.poni'

DEFAULT_INCIDENT_ANGLE = 0.0
DEFAULT_TILT_ANGLE = 0.0

DIGITS_SAMPLE = 4
DIGITS_FILE = 4

ENTRY_ZEROS = 4
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

EXTENSION_H5 = '.h5'

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
    def __init__(self, input_h5_filename='', root_directory='', output_filename_h5=''):

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
        else:
            raise Exception(INPUT_ROOT_DIR_NOT_VALID) 

    def init_root_h5_attributes(self, input_h5_filename='', root_directory='', output_filename_h5=''):
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
        
        self.gi = GIIntegrator()                    

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
            h5_output_file = Path(root_directory).joinpath(name).with_suffix(EXTENSION_H5)
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
    def write_root_attributes(self, root_directory='', h5_filename=''):
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
            )
        except:
            dataset = None
        return dataset

    @logger_info
    def get_dataset_incident_angle(
        self, 
        sample_name=str(), 
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
                key_metadata=key_iangle,
            )
        except:
            dataset = None
        return dataset

    @logger_info
    def get_dataset_tilt_angle(
        self, 
        sample_name=str(), 
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
                key_metadata=key_tangle,
            )
        except:
            dataset = None
        return dataset

    @logger_info
    def get_dataset_norm_factor(
        self, 
        sample_name=str(),
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
        """Searches for .poni files in the root directory

        Returns:
            list with sorted strings of poni filename
        """                    
        if not self._root_dir:
            logger.error('No root directory to search .poni files.')
            return
        
        try:
            # Absolute paths of .poni files in the root folder
            searched_ponifiles = sorted(file.as_posix() for file in self._root_dir.rglob(WILDCARDS_PONI))
            if new_files:
                # Filter only the new files
                ponifiles_in_h5 = self.get_all_ponifiles(get_relative_address=False)
                searched_ponifiles = [file for file in searched_ponifiles if file not in ponifiles_in_h5]  
            
            logger.info(f"Found {len(searched_ponifiles)} .poni files in {self._root_dir}")
            return searched_ponifiles
        
        except Exception as e:
            logger.error(f"{e}: there was an error during searching ponifiles in {self._root_dir}.")
            return

    @logger_info
    def update_ponifiles(self):
        """
        Searches .poni files in the root directory and updates
        the entry_ponifiles
        """        
        searched_ponifiles = self.search_ponifiles()

        if not searched_ponifiles:
            logger.info('No ponifiles to be updated.')
            return
        
        else:
            if not self.check_ponifile_entry():
                # Create ponifile entry and dataset
                self.create_entry_ponifile(
                    ponifile_list=searched_ponifiles,
                )                   
                # self.delete_nx_group(entry=ENTRY_PONIFILE_KEY)
            else:
                try:
                    # Resize and append
                    self.append_ponifiles(
                        ponifile_list=searched_ponifiles,
                    )

                    # save_NXdata(
                    #     filename=self._h5_filename,
                    #     signal_name=PONI_GROUP_KEY,
                    #     signal=searched_ponifiles,
                    #     interpretation='spectrum',
                    #     nxentry_name=ENTRY_PONIFILE_KEY,
                    #     nxdata_name=PONI_GROUP_KEY,
                    # )
                    logger.info(f'Saved NXdata: {ENTRY_PONIFILE_KEY}')
                except Exception as e:
                    logger.error(f'{e}: Error during saving NXdata {ENTRY_PONIFILE_KEY}')

    @logger_info
    def generate_ponifiles(self, get_relative_address=True) -> str:
        """Yields a string with the relative or absolute address of .poni files

        Keyword Arguments:
            get_relative_address -- if True, yields the basename of .poni file

        Yields:
            string of .poni file
        """
        if not self.check_ponifile_entry():
            logger.info('There is no entry_ponifiles.')
            return []
        
        with File(self._h5_filename, 'r+') as f:
            dataset = f[ENTRY_PONIFILE_KEY][PONI_GROUP_KEY][PONI_GROUP_KEY]

            for ponifile in dataset:
                ponifile = ponifile.decode(ENCODING_FORMAT)
                ponifile = Path(ponifile).as_posix()

                if get_relative_address:
                    ponifile = Path(ponifile).relative_to(self._root_dir).as_posix()

                yield ponifile
        
    @logger_info
    def get_all_ponifiles(self, get_relative_address=True) -> list:
        """Gets a sorted list with the stored .poni files

        Keyword Arguments:
            get_relative_address -- if True, returns a list of .poni file basenames

        Returns:
            list with strings of .poni files
        """        
        ponifile_list = sorted(self.generate_ponifiles(get_relative_address=get_relative_address))
        return ponifile_list

    @logger_info
    def get_ponifile(self, poni_name='') -> str:
        poni_name = Path(poni_name)

        if poni_name.is_absolute():
            poni_name = poni_name.as_posix()
        else:
            poni_name = self._root_dir.joinpath(poni_name).as_posix()
        
        return poni_name

    @logger_info
    def update_poni(self, poni=None) -> None:

        if isinstance(poni, str) or isinstance(poni, Path):
            poni = self.get_ponifile(poni_name=poni)

        self.gi.update_poni(poni=poni)
    
    @logger_info
    def get_poni(self):
        poni = self.gi._poni
        return poni


    @logger_info
    def update_orientation(self, qz_parallel=True, qr_parallel=True):
        self.gi.update_orientation(
            qz_parallel=qz_parallel,
            qr_parallel=qr_parallel,
        )


    @logger_info
    def update_angles(self, sample_name='', list_index=0):
        iangle = self.get_incident_angle(
            sample_name=sample_name,
            index_list=list_index,
        )
        tangle = self.get_tilt_angle(
            sample_name=sample_name,
            index_list=list_index,
        )

        self.gi.update_incident_angle(
            incident_angle=iangle,
        )
        self.gi.update_tilt_angle(
            tilt_angle=tangle,
        )


    # @logger_info
    # def append_stringlist_to_dataset(self, group_address='.', dataset_name=str(), list_to_append=list()):
    #     if isinstance(list_to_append, str):
    #         list_to_append = [list_to_append]

    #     with File(self._h5_filename, 'r+') as f:
    #         if not f[group_address].__contains__(dataset_name):
    #             logger.info(f"{dataset_name} does not exist in {group_address}. Create it before appending.")
    #         else:
    #             try:
    #                 dataset = f[group_address][dataset_name]
    #                 dataset.resize((dataset.shape[0] + len(list_to_append),))
    #                 dataset[-len(list_to_append):] = list_to_append
    #                 logger.debug(f"{str(list_to_append)} was appended to {group_address}/{dataset}")
    #             except Exception as e:
    #                 logger.error(f"{str(list_to_append)} could not be appended to {group_address}/{dataset}")



    #####################################
    ###### HDF5 METHODS #################
    #####################################

    @logger_info
    def create_entry_ponifile(self, ponifile_list=[]):
        with File(self._h5_filename, 'r+') as f:
            f.create_group(name='entry_ponifiles')
            f['entry_ponifiles'].attrs['NX_class'] ='NXentry'
            f['entry_ponifiles'].create_group(name='ponifiles')     
            f['entry_ponifiles']['ponifiles'].attrs['NX_class'] ='NXdata'
            	
            f['entry_ponifiles']['ponifiles'].create_dataset(
                name='ponifiles',
                data=ponifile_list,
                maxshape=(None,),
                dtype=FORMAT_STRING,
            )
        
    @logger_info
    def append_ponifiles(self, ponifile_list=[]):
        with File(self._h5_filename, 'r+') as f:
            # Resize dataset
            initial_size = f['entry_ponifiles']['ponifiles']['ponifiles'].shape[0]
            future_size = (initial_size + len(ponifile_list),)
            f['entry_ponifiles']['ponifiles']['ponifiles'].resize(future_size)
            # Add new data
            f['entry_ponifiles']['ponifiles']['ponifiles'][initial_size:] = ponifile_list


    @logger_info
    def create_group_metadata(self, entry_name='', metadata_key='', data_values=[]):
        with File(self._h5_filename, 'r+') as f:
            f[entry_name].create_group(name=metadata_key)
            f[entry_name][metadata_key].attrs['NX_class'] ='NXdata'
            f[entry_name][metadata_key].create_dataset(
                name=metadata_key,
                data=data_values,
                maxshape=(None,),
                # dtype=FORMAT_STRING,
            )
            
    @logger_info
    def append_metadata_value(self, entry_name='', metadata_key='', data_values=[]):
        with File(self._h5_filename, 'r+') as f:
            # Resize dataset
            initial_size = f[entry_name][metadata_key][metadata_key].shape[0]
            future_size = (initial_size + len(data_values),)
            f[entry_name][metadata_key][metadata_key].resize(future_size)
            # Add new data
            f[entry_name][metadata_key][metadata_key][initial_size:] = data_values
            
        
    # @logger_info
    # def create_group(
    #     self,
    #     h5_filename='',
    #     root_group_address='.', 
    #     group_name=str(),
    #     ):
    #     if not h5_filename:
    #         h5_filename = self._h5_filename
        
    #     with File(self._h5_filename, 'r+') as f:
    #         # Returns if it contains the dataset already
    #         if f[root_group_address].__contains__(group_name):
    #             logger.debug(f"{group_name} exists already in {root_group_address}.")
    #             return
    #         else:
    #             try:
    #                 f[root_group_address].create_group(
    #                     name=str(group_name),
    #                 )

    #                 logger.debug(f"{group_name} was created in {root_group_address}.")
    #             except Exception as e:
    #                 logger.error(f"{e}: {group_name} could not be created in {root_group_address}.")

    @logger_info
    def get_new_nx_entry_name(self):
        entry_name = f'entry_{str(self.get_nx_entries()).zfill(ENTRY_ZEROS)}'
        return entry_name

    # @logger_info
    # def create_dataset_path(self, group_address='.', dset_name=str(), dtype=FORMAT_STRING, shape=DEFAULT_SHAPE_1D, maxshape=MAXSHAPE_1D_RESIZE,):
    #     with File(self._h5_filename, 'r+') as f:
    #         # Returns if it contains the dataset already
    #         if f[group_address].__contains__(dset_name):
    #             logger.debug(f"{dset_name} exists already in {group_address}.")
    #             return
    #         else:
    #             try:
    #                 f[group_address].create_dataset(
    #                     name=dset_name,
    #                     shape=shape,
    #                     maxshape=maxshape,
    #                     dtype=dtype,
    #                 )
    #                 logger.debug(f"{dset_name} was created in {group_address}")
    #             except Exception as e:
    #                 logger.error(f"{e}: {dset_name} could not be created in {group_address}")


    # @logger_info
    # def create_dataset_float(self, group_address='.', dset_name=str(), dtype=FORMAT_FLOAT, shape=DEFAULT_SHAPE_1D, maxshape=MAXSHAPE_1D_RESIZE,):
    #     with File(self._h5_filename, 'r+') as f:
    #         # Returns if it contains the dataset already
    #         if f[group_address].__contains__(dset_name):
    #             logger.debug(f"{dset_name} exists already in {group_address}.")
    #             return
    #         else:
    #             try:
    #                 f[group_address].create_dataset(
    #                     name=dset_name,
    #                     shape=shape,
    #                     maxshape=maxshape,
    #                     dtype=dtype,
    #                 )
    #                 logger.debug(f"{dset_name} was created in {group_address}")
    #             except Exception as e:
    #                 logger.error(f"{e}: {dset_name} could not be created in {group_address}")

    # @logger_info
    # def create_group_samples(self, h5_filename=''):
    #     self.create_group(
    #         h5_filename=h5_filename,
    #         group_name=SAMPLE_GROUP_KEY,
    #     )

    # @logger_info
    # def create_group_ponifiles(self, h5_filename):
    #     self.create_group(
    #         h5_filename=h5_filename,
    #         group_name=PONI_GROUP_KEY,
    #     )
    #     self.create_ponifile_dset()


    # @logger_info
    # def create_ponifile_dset(self):
    #     self.create_dataset_path(
    #         group_address=PONI_GROUP_KEY,
    #         dset_name=PONIFILE_DATASET_KEY,
    #     )


    # @logger_info
    # def create_sample(self, sample_name=str()):

    #     # Define the name, absolute and relative
    #     sample_name = Path(sample_name)

    #     self.create_group(
    #         root_group_address=SAMPLE_GROUP_KEY,
    #         group_name=sample_name,
    #     )

    def get_full_dict_metadata(self, list_filenames=[]):
        header_dict = defaultdict(list)
        list_filenames = list(list_filenames)
        list_filenames.sort()
        for file in list_filenames:
            header = self.get_Edf_instance(
                full_filename=file,
            ).get_header()
            for key, value in header.items():
                try:
                    value = float(value)
                except:
                    value = str(value).encode()
                header_dict[key].append(value)
            header_dict[DATAFILE_KEY].append(file.encode())
            header_dict[DATANAME_KEY].append(Path(file).name)
        return header_dict

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

    @logger_info
    def generator_samples(self, get_group_name=True, get_relative_address=False) -> str:
        with File(self._h5_filename, 'r+') as f:
            for entry in  f.keys():
                if entry == ENTRY_PONIFILE_KEY:
                    continue

                if get_group_name:
                    yield entry
                else:
                    if get_relative_address:
                        sample_name = f[entry].attrs[REL_ADDRESS_KEY]
                    else:
                        sample_name = f[entry].attrs[ABS_ADDRESS_KEY]        
                    yield sample_name

    @logger_info
    def get_all_entries(self, get_relative_address=True) -> list:
        list_entries = sorted(
            self.generator_samples(
                get_group_name=False,
                get_relative_address=get_relative_address,
            ),
        )
        return list_entries

    @logger_info
    def generator_all_filenames(self) -> str:
        """
        Yields the names of every file stored in the .h5 file

        Parameters:
        None

        Yields:
        str : fullpath of stored filenames
        """
        for sample in self.generator_samples(get_group_name=True):
            for file in self.generator_filenames_in_sample(
                sample_address=sample,
                ):
                yield file

    @logger_info
    def get_dict_files(self):
        dict_files = defaultdict(set)
        for filename in self.generator_all_filenames():
            sample_name = Path(filename).parent.as_posix()
            file = Path(filename).as_posix()
            dict_files[sample_name].add(filename)
        return dict_files

    @logger_info
    def get_all_filenames(self) -> list:
        """
        Returns a list with all the stored files in the h5 File

        Keyword Arguments:
            decode -- _description_ (default: {True})

        Returns:
            _description_
        """
        list_files = list(self.generator_all_filenames())
        return list_files

    ##################################################
    ############# DATAFILE METHODS ##############
    ##################################################

    @logger_info
    def search_datafiles(self, pattern='*.edf', new_files=True) -> dict:
        """Searches the data files in the root directory that match with a pattern

        Keyword Arguments:
            pattern -- filename string pattern (default: {'*.edf'})

        Returns:
            dictionary with folder addresses as keys and list of data addresses as values
        """        
        searched_files = self._root_dir.rglob(pattern)

        dict_files = get_dict_files(
            list_files=searched_files,
        )

        if new_files:
            # Identify the new files
            dict_files_in_h5 = self.get_dict_files()
            dict_files = get_dict_difference(
                large_dict=dict_files,
                small_dict=dict_files_in_h5,
            )
            logger.info(f"{INFO_H5_NEW_DICTIONARY_FILES}: {str(dict_files)}")

        return dict_files

    @logger_info
    def update_datafiles(self, dict_files=dict(), search=False, pattern='*.edf', new_files=True,):

        """Updates the data filenames as NXentries

        Keyword Arguments:
            dict_files -- input dictionary of folder-filenames (default: {dict()})
            search -- if True, searches in the root dictionary (default: {False})
            pattern -- filename string pattern (default: {'*.edf'})
            new_files -- if True, update only the new files (default: {True})
        """        

        # Search for new files
        if dict_files:
            dict_files = dict_files
        elif search:
            dict_files = self.search_datafiles(
                pattern=pattern,
                new_files=new_files,
            )

        # Write the new files
        for sample_address in dict_files.keys():

            # Rewrite group if it exists
            existing_entry = self.get_entry_name(sample_address=sample_address)
            if not existing_entry:
                group_name = self.get_new_nx_entry_name()
                self.create_entry(entry_name=group_name)
            else:
                group_name = existing_entry
            # if existing_entry:
            #     group_name = existing_entry
            #     data_files = dict_files.get(sample_address)
            #     self.delete_nx_group(entry=group_name)
            # else:
            #     group_name = self.get_new_nx_entry_name()
            #     self.create_entry(entry_name=group_name)
            #     data_files = dict_files.get(sample_address)
            
            data_files = dict_files.get(sample_address)
            dict_metadata = self.get_full_dict_metadata(
                list_filenames=data_files,
            )

            for key, value in dict_metadata.items():
                if not self.check_metadata_group(entry_name=group_name, metadata_key=key):
                    # Create group/dataset
                    self.create_group_metadata(
                        entry_name=group_name,
                        metadata_key=key,
                        data_values=value,
                    )              
                else:
                    self.append_metadata_value(
                        entry_name=group_name,
                        metadata_key=key,
                        data_values=value,
                    )
                    # Resize and append
                

                # save_NXdata(
                #     filename=self._h5_filename,
                #     signal_name=key,
                #     signal=value,
                #     interpretation='spectrum',
                #     nxentry_name=group_name,
                #     nxdata_name=key,
                # )

                self.write_sample_address(
                    group_name=group_name,
                    sample_address=sample_address,
                )

    @logger_info
    def get_entry_name(self, sample_address=''):

        # Check if its an entry name
        with File(self._h5_filename, 'r+') as f:
            for entry in f.keys():
                if sample_address == entry:
                    return sample_address

        # Check if its an absolute or relative path address
        sample_address = Path(sample_address)

        if sample_address.is_absolute():
            absolute_address = sample_address
            relative_address = ''
        else:
            relative_address = sample_address
            absolute_address = ''

        if absolute_address:
            absolute_address = Path(absolute_address).as_posix()

            with File(self._h5_filename, 'r+') as f:
                for entry in f.keys():
                    if entry == ENTRY_PONIFILE_KEY:
                        continue

                    if absolute_address == f[entry].attrs[ABS_ADDRESS_KEY]:
                        return entry

        elif relative_address:
            relative_address = Path(relative_address).as_posix()

            with File(self._h5_filename, 'r+') as f:
                for entry in f.keys():
                    if entry == ENTRY_PONIFILE_KEY:
                        continue

                    if relative_address == f[entry].attrs[REL_ADDRESS_KEY]:
                        return entry

        return None


    @logger_info
    def create_entry(self, entry_name=''):
        with File(self._h5_filename, 'r+') as f:
            f.create_group(name=entry_name)
            f[entry_name].attrs['NX_class'] ='NXentry'
            
    @logger_info
    def check_entry(self, entry_name=''):
        with File(self._h5_filename, 'r+') as f:
            if entry_name in f.keys():
                return True
            else:
                return False        
            
    @logger_info
    def check_ponifile_entry(self):
        return self.check_entry(entry_name=ENTRY_PONIFILE_KEY)
            
    @logger_info
    def check_metadata_group(self, entry_name, metadata_key):
        h5_path = f'{entry_name}/{metadata_key}'
        return self.check_entry(entry_name=h5_path)
        
    @logger_info
    def delete_nx_group(self, entry=''):
        with File(self._h5_filename, 'r+') as f:
            del f[entry]
            logger.info(f'Deleted {entry}.')

    @logger_info
    def write_sample_address(self, group_name='', sample_address=''):
        absolute_address = Path(sample_address).as_posix()
        relative_address = Path(sample_address).relative_to(self._root_dir).as_posix()

        with File(self._h5_filename, 'r+') as f:
            f[group_name].attrs[ABS_ADDRESS_KEY] = absolute_address
            f[group_name].attrs[REL_ADDRESS_KEY] = relative_address

    @logger_info
    def get_nx_entries(self):
        with File(self._h5_filename, 'r+') as f:
            return f.__len__()

    @logger_info
    def get_all_filenames_from_sample(
        self, 
        sample_name=str(),
        ):
        list_files = list(
            self.generator_filenames_in_sample(
                sample_address=sample_name,
            ))
        return list_files

    @logger_info
    def get_all_names_from_sample(
        self, 
        sample_name=str(),
        ):
        list_files = list(
            self.generator_names_in_sample(
                sample_address=sample_name,
            ))
        return list_files

    @logger_info
    def get_sample_address(
        self, 
        entry_name='',
        get_relative_address=False,
        ):
        with File(self._h5_filename, 'r+') as f:
            for entry in f.keys():
                if entry_name == entry:
                    if get_relative_address:
                        address = f[entry].attrs[REL_ADDRESS_KEY]
                    else:
                        address = f[entry].attrs[ABS_ADDRESS_KEY]
                    return address
            return ''

    @logger_info
    def generator_filenames_in_sample(
        self, 
        sample_address=str(),
        ):

        data_filenames = self.get_metadata_dataset(
            sample_name=sample_address,
            key_metadata=DATAFILE_KEY,
        )

        for filename in data_filenames:
            filename = bytes.decode(filename)
            yield filename

    @logger_info
    def generator_names_in_sample(
        self, 
        sample_address=str(),
        ):

        data_filenames = self.get_metadata_dataset(
            sample_name=sample_address,
            key_metadata=DATANAME_KEY,
        )

        for name in data_filenames:
            name = bytes.decode(name)
            yield name

    @logger_info
    def get_metadata_dataset(
        self, 
        sample_name=str(), 
        key_metadata=str(),
        ) -> np.array:

        entry_name = self.get_entry_name(
            sample_address=sample_name,
        )

        if not entry_name:
            return

        with File(self._h5_filename, 'r+') as f:
            try:
                dataset = f[entry_name][key_metadata][key_metadata][()]
            except Exception as e:
                logger.error(f"{e}: dataset {key_metadata} could not be accessed.")
                return
            return dataset

    @logger_info
    def get_metadata_value(
        self, 
        sample_name=str(),
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
        list_keys=list(),
        ) -> pd.DataFrame:

        list_files_in_sample = self.get_all_filenames_from_sample(
            sample_name=sample_name,
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
        ):
        list_keys = sorted(
            self.generator_metadata_keys_from_sample(
                sample_name=sample_name,
                ))
        return list_keys

    @logger_info
    def generator_metadata_keys_from_sample(
        self, 
        sample_name=str(), 
        ):

        entry_name = self.get_entry_name(sample_address=sample_name)


        if not entry_name:
            return
        
        with File(self._h5_filename, 'r+') as f:
            for key in f[entry_name].keys():
                yield key

    @logger_info
    def get_filename_from_index(
        self, 
        sample_name=str(),
        index_list=list(),
        ):

        entry_name = self.get_entry_name(sample_address=sample_name)

        if not entry_name:
            return

        with File(self._h5_filename, 'r+') as f:

            if isinstance(index_list, int):
                index_list = [index_list]

            filename = f[entry_name][DATAFILE_KEY][DATAFILE_KEY][index_list[0]]
            filename = bytes.decode(filename)

            if len(index_list) > 1:
                filename = filename.replace(".edf", "_average.edf")

        return filename

    @logger_info
    def get_name_from_index(
        self, 
        sample_name=str(),
        index_list=list(),
        ):

        entry_name = self.get_entry_name(sample_address=sample_name)

        if not entry_name:
            return

        with File(self._h5_filename, 'r+') as f:

            if isinstance(index_list, int):
                index_list = [index_list]

            filename = f[entry_name][DATANAME_KEY][DATANAME_KEY][index_list[0]]
            filename = bytes.decode(filename)

            if len(index_list) > 1:
                filename = filename.replace(".edf", "_average.edf")

        return filename

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
            list_files = [getctime(file) for file in self.generator_all_filenames()]
        try:
            last_file = list_files[np.argmax(list_files)]
            logger.info(f"Found last file: {last_file}")
        except:
            logger.info("The last file could not be found.")
        return last_file
            

    @logger_info
    def get_Edf_instance(
        self, 
        full_filename=str(),
        sample_name=str(),
        index_file=int(),
        ):

        # Take the full filename
        if full_filename:
            filename = full_filename
        else:
            try:
                filename = self.get_filename_from_index(
                    sample_name=sample_name,
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
        index=(), 
        full_filename=str(),
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
        if isinstance(index, int):
            index = (index,)

        # Get the sample data
        try:
            data_sample = sum(
                [
                    self.get_Edf_instance(
                        full_filename=full_filename,
                        sample_name=sample_name,
                        index_file=index,
                    ).get_data() for index in index
                ]
            ) / len(index)
            logger.info(f"New data sample with shape: {data_sample.shape}")
        except Exception as e:
            data_sample = None
            logger.error(f"{e}: Data sample could not be uploaded.")
            return

        if normalized:
            norm_factor = self.get_norm_factor(
                sample_name=sample_name,
                index_list=index,
            )
            data_sample = data_sample.astype('float32') / norm_factor

        return data_sample
    
    @logger_info
    def generate_integration(self, data=None, norm_factor=1.0, list_dict_integration=[]):
        for res in self.gi.generate_integration(
            data=data,
            norm_factor=norm_factor,
            list_dict_integration=list_dict_integration,
            ):
            yield res

    @logger_info
    def map_reshaping(self, data=None):
        if data is None:
            return
        data_reshape, q, chi = self.gi.map_reshaping(data=data)
        return data_reshape, q, chi

    @logger_info
    def get_mesh_matrix(self, unit='q_nm^-1', shape=()):
        scat_horz, scat_vert = self.gi.get_mesh_matrix(
                unit=unit,
                shape=shape,
        )
        return scat_horz, scat_vert