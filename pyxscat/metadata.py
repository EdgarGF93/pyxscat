
from collections import defaultdict
from threading import Thread
from pathlib import Path
from typing import List, Any
import logging
import fabio
import json
from pyxscat.edf import FullHeader
import os
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

FILENAMES = 'filenames'
NAMES = 'names'

PATTERNS = ['*.edf', '*.cbf', '*.tif', '*.tiff']
DEFAULT_PATTERN = '*.edf'
DIR_PATTERN = '**/'

class MetadataBase:
    def __init__(
            self, 
            directory="", 
            pattern=DEFAULT_PATTERN, 
            update_metadata=True,
            json_file="",
        ):
        self._init_containers()

        # Init database using a json_file or a directory path (+ pattern)
        if json_file:
            self._open_metadatabase(json_file=json_file)
            self._init_attributes(
                directory=os.path.commonprefix(self.get_entries()),
                pattern=pattern,
                json_file=json_file,
            )
        elif directory:
            self._init_attributes(
                directory=directory,
                pattern=pattern,
                json_file="",
            )
        else:
            return
        
        if update_metadata:
            self._update_metadata()
    
    def __repr__(self):
        repr = f"""
        MetadataBase associated to {self._directory}
        Pattern to search files: {self._pattern}
        Number of entries: {self.nbentries}
        Total number of files: {self.nfiles}
        """
        return repr
    
    def _init_containers(self):
        self._container_metadata = defaultdict(lambda : defaultdict(list))
        self._container_metadata_newfiles = defaultdict(lambda : defaultdict(list))
        self._container_ponifiles = list()
        self._container_ponifiles_new = list()

    def _open_metadatabase(self, json_file=""):
        if not Path(json_file).is_file():
            return
        
        with open(json_file) as f:
            metadatabase = json.load(f)
        self._container_metadata = defaultdict(lambda : defaultdict(list), metadatabase)     
    
    def _init_attributes(self, directory="", pattern="", json_file=""):
        self._directory = Path(directory)
        self._pattern = pattern
        if not json_file:
            self._json_file = self._get_json_file()
        else:
            self._json_file = json_file

    def _get_json_file(self):
        return Path(__file__).parent.joinpath("metadatabases", f'{self._directory.name}_pyxscat_mdb.json')

    @property
    def nbentries(self):
        return len(list(self._container_metadata.keys()))
    
    @property
    def nfiles(self):
        files = 0
        for entry in self._generate_entries():
            files += len(list(self._container_metadata[entry][FILENAMES]))
        return files

    @property
    def container(self):
        return self._container_metadata
    
    @property
    def container_newfiles(self):
        return self._container_metadata_newfiles 

    @property
    def directory(self):
        return str(self._directory)
    
    def _reset_container(self):
        self._container_metadata = defaultdict(lambda : defaultdict(list))

    def __iter__(self):
        for subdirectory in self._container_metadata.keys():
            for filename in self._container_metadata[subdirectory][FILENAMES]:
                yield filename

    def _get_relative_path(self, absolute_path: str = '', entry_name: str = ''):
        if entry_name:
            entry_name = self._validate_entry(entry_name=entry_name)
            return str(Path(absolute_path).relative_to(entry_name)) 
        return str(Path(absolute_path).relative_to(self._directory))
    
    def _get_absolute_path(self, relative_path : str = ''):
        return str(self._directory.joinpath(relative_path))

    def _validate_entry(self, entry_name:str):
        if Path(self.directory) in Path(entry_name).parents:
            entry_name = str(entry_name)
        else:
            entry_name = str(Path(self.directory).joinpath(entry_name))
        if entry_name not in self.get_entries():
            return
        return entry_name

    def _get_metadata_values_from_entry(self, entry: str, metadata_key: str):
        entry = self._validate_entry(entry_name=entry)
        if not entry:
            return
        return self.container[entry][metadata_key]

    def _get_all_metadata_in_entry(self, entry: str):
        entry = self._validate_entry(entry_name=entry)
        if not entry:
            return
        return self.container[entry].keys()

    def _append(self, entry_name: str, metadata_key: str, metadata_value: Any):
        self._container_metadata[entry_name][metadata_key].append(metadata_value)

    def _get_header(self, filename: str):
        try:
            header = FullHeader(filename=str(filename)).get_header()
            return header
        except Exception as e:
            print(f'Full header of {str(filename)} could not be accessed.\{e}')
        
        try:
            header = fabio.open(filename=str(filename)).header
            return header
        except Exception as e:
            print(f'Fabio header of {str(filename)} could not be accessed anyway.\{e}')
            return

    def _update_entry_single(self, entry_name: Path, filename: Path):
        if self._is_file_in_entry(
            entry_name=str(entry_name),
            filename=str(filename),
            ):
            logger.warning(f"The file {filename} is already in the MetadataBase.")
            return

        # Filename/Name metadata
        self._append(entry_name=str(entry_name), metadata_key=FILENAMES, metadata_value=str(filename))
        self._append(entry_name=str(entry_name), metadata_key=NAMES, metadata_value=str(Path(filename).name))
        logger.info(f"Updated filename: {str(filename)}")
    
        # Get Fabio header
        header = self._get_header(filename=filename)
        for metadata_key,metadata_value in header.items():
            try:
                metadata_value = float(metadata_value)
            except:
                metadata_value = str(metadata_value)
            self._append(entry_name=str(entry_name), metadata_key=metadata_key, metadata_value=metadata_value)

    def _update_entry_single_thread(self, entry_name, filename):
        Thread(target=self._update_entry_single, args=(entry_name, filename)).start()

    def _update_entry(self, entry_name, file_iterator, threading=False):
        iter_empty = True
        for filename in sorted(file_iterator):
            iter_empty = False
            if threading:
                self._update_entry_single_thread(entry_name=entry_name, filename=filename)
            else:
                self._update_entry_single(entry_name=entry_name, filename=filename)
        return iter_empty
    
    def _search_files(self) -> dict:
        return {str(subdir) : subdir.glob(self._pattern) for subdir in self._directory.rglob(DIR_PATTERN)}

    def _search_new_files(self) -> dict:
        dict_new_files = defaultdict(list)
        for subdir in self._directory.rglob(DIR_PATTERN):
            if str(subdir) not in self._container_metadata.keys():
                dict_new_files[str(subdir)] = subdir.glob(self._pattern)
            else:
                dict_new_files[str(subdir)].extend([str(file) for file in subdir.glob(self._pattern) if str(file) not in self._container_metadata[str(subdir)][FILENAMES]])
        return dict_new_files

    def _search_ponifiles(self) -> list:
        return [str(ponifile) for ponifile in self._directory.rglob("*.poni")]

    def _update_metadata(self):
        if self._container_metadata == defaultdict(lambda : defaultdict(list)):
            self._update_metadatabase(dict_new_files=self._search_files())
        else:
            self._update_metadatabase(dict_new_files=self._search_new_files())
        self.update_ponidatabase()

    def _is_file_in_entry(self, entry_name: Path, filename: Path):
        if filename in self._generate_files_in_entry(entry_name=entry_name):
            return True
        return False
    
    def _remove_metadata(self):
        dict_removed_files = defaultdict(list)
        for entry in self._generate_entries():
            for index, filename in enumerate(self._generate_files_in_entry(entry_name=entry)):
                if not Path(filename).is_file():
                    dict_removed_files[entry].append(index)

        for entry, index_list in dict_removed_files.items():
            index_list.reverse()
            for index in index_list:
                self._remove_metadata_in_entry(
                    entry_name=entry,
                    index=index,
                )

    def _remove_metadata_in_entry(self, entry_name:str, index:int):
        for metadata_key in self._container_metadata[entry_name]:
            del self._container_metadata[entry_name][metadata_key][index]

    def _get_element(self, entry_name:str, index:int, metadata_key:str):
        try:
            return self._container_metadata[entry_name][metadata_key][index]
        except Exception as e:
            return

    def _get_metadata_container(self, entry_name:str, metadata_key: str):
        try:
            return self._container_metadata[entry_name][metadata_key]
        except Exception as e:
            return

    def _generate_files(self, relative_path=False):
        for filename in self.__iter__():
            if relative_path:
                yield self._get_relative_path(absolute_path=filename)
            else:
                yield filename

    def _generate_new_files(self, relative_path=False):
        for entry in self._container_metadata_newfiles.keys():
            for filename in self._container_metadata_newfiles[entry][FILENAMES]:
                if relative_path:
                    yield self._get_relative_path(absolute_path=filename)
                else:
                    yield filename

    def _generate_entries(self, relative_path=False):
        for entry in self._container_metadata.keys():
            if relative_path:
                yield self._get_relative_path(absolute_path=entry)
            else:
                yield entry

    def _generate_new_entries(self, relative_path=False):
        for entry in self._container_metadata_newfiles.keys():
            if relative_path:
                yield self._get_relative_path(absolute_path=entry)
            else:
                yield entry

    def _generate_metadata_in_entry(self, entry_name:str, metadata_key=False):
        entry_name = self._validate_entry(entry_name=entry_name)
        if not entry_name:
            return
    
        metadata_dataset = self._get_metadata_container(entry_name=entry_name, metadata_key=metadata_key)
        if not metadata_dataset:
            return
        
        for metadata in metadata_dataset:
            yield metadata

    def _generate_files_in_entry(self, entry_name:str, relative_path=False):
        entry_name = self._validate_entry(entry_name=entry_name)
        if not entry_name:
            return

        for filename in self._container_metadata[entry_name][FILENAMES]:
            if relative_path:
                yield self._get_relative_path(absolute_path=filename, entry_name=entry_name)
            else:
                yield filename

    def _update_metadatabase(self, dict_new_files:dict):
        dict_new_files_clear = dict_new_files.copy()
        for entry_name, file_iterator in dict_new_files.items():
            if self._update_entry(
                entry_name=entry_name,
                file_iterator=file_iterator,
            ):
                del dict_new_files_clear[entry_name]
        self._container_metadata_newfiles = dict_new_files_clear
        return dict_new_files_clear

    def _update_ponidatabase(self, list_new_ponifiles:list):
        new_ponifiles = []
        for ponifile in list_new_ponifiles:
            if ponifile not in self._container_ponifiles:
                self._container_ponifiles.append(ponifile)
                new_ponifiles.append(ponifile)
        self._container_ponifiles_new = new_ponifiles

    ####################
    #### PUBLIC API ####
    ####################

    def update(self, update_ponifiles: bool=True, return_dict: bool=False, removed_files: bool=False) -> dict:
        dict_new_files = self.get_new_files()
        dict_new_files_clear = self._update_metadatabase(
            dict_new_files=dict_new_files,
        )
        if update_ponifiles:
            self.update_ponidatabase()

        if removed_files:
            self._remove_metadata()

        if return_dict:
            return dict_new_files_clear
    
    def update_ponidatabase(self):
        self._update_ponidatabase(list_new_ponifiles=self._search_ponifiles())

    def get_new_files(self) -> dict:
        if self._container_metadata == defaultdict(lambda : defaultdict(list)):
            dict_new_files = self._search_files()
        else:
            dict_new_files = self._search_new_files()
        return dict_new_files

    def get_entries(self, relative_path=False) -> list:
        return [entry for entry in self._generate_entries(relative_path=relative_path)]

    def get_files_in_entry(self, entry_name:str, relative_path=False):
        return [filename for filename in self._generate_files_in_entry(entry_name=entry_name, relative_path=relative_path)]        

    def get_filenames(self, entry_name:str, index:list, relative_path=False):
        list_filenames = []
        for ind, filename in enumerate(self._generate_files_in_entry(entry_name=entry_name, relative_path=relative_path)):
            if ind in index:
                list_filenames.append(filename)
        return list_filenames        
    
    def get_metadata(self, entry_name:str, index:int, metadata_key: str):
        for ind, metadata in enumerate(self._generate_metadata_in_entry(entry_name=entry_name, metadata_key=metadata_key)):
            if ind == index:
                return metadata


    def get_metadata_in_entry(self, entry_name:str, metadata_key: str):
        return self._get_metadata_values_from_entry(entry=entry_name, metadata_key=metadata_key)
    
    def get_all_metadata_in_entry(self, entry_name:str):
        return self._get_all_metadata_in_entry(entry=entry_name)

    def get_dataframe_metadata(self, entry_name:str, list_keys:list, relative_path=False):
        list_files = self.get_files_in_entry(
            entry_name=entry_name,
            relative_path=relative_path,
        )
        if not list_files:
            return
        
        short_metadata = defaultdict(list)

        for filename in list_files:
            short_metadata[FILENAMES].append(filename)

            for metadata_key in list_keys:
                try:
                    dataset = self.get_metadata_in_entry(
                        entry_name=entry_name,
                        metadata_key=metadata_key,
                    )
                    short_metadata[metadata_key] = dataset
                except:
                    logger.warning(f"Error during acceeding to Metadata dataset with key: {metadata_key}")
        dataframe = pd.DataFrame(short_metadata)
        return dataframe

    def get_ponifiles(self, relative_path=False):
        if relative_path:
            return [str(Path(ponifile).relative_to(self._directory)) for ponifile in self._container_ponifiles]
        else:
            return self._container_ponifiles

    def get_new_ponifiles(self, relative_path=False):
        if relative_path:
            return [str(Path(ponifile).relative_to(self._directory)) for ponifile in self._container_ponifiles_new]
        else:
            return self._container_ponifiles_new

    def search_files(self) -> dict:
        return self._search_files()

    def save(self, output_directory: str = ''):
        if not output_directory:
            out_folder = Path(__file__).parent.joinpath("metadatabases")
            out_folder.mkdir(exist_ok=True)            
            output_filename = out_folder.joinpath(f'{self._directory.name}_pyxscat_mdb.json')
        else:
            output_directory = Path(output_directory)
            output_filename = output_directory.joinpath(f'{self._directory.name}_pyxscat_mdb.json')

        with open(output_filename, 'w') as fp:
            json.dump(self._container_metadata, fp)


class EdfMetadata(MetadataBase):

    def __init__(self, directory):
        super().__init__(directory=directory, pattern="*.edf")



class PoniMetadata(MetadataBase):
    def __init__(self, directory):
        super().__init__(directory=directory, pattern="*.poni")

    def _update_entry_single(self, entry_name: Path, filename: Path):
        filename = Path(filename)

        # ADDITIONAL METADATA
        self._append(entry_name=str(entry_name), metadata_key=FILENAMES, metadata_value=str(filename))
        self._append(entry_name=str(entry_name), metadata_key=NAMES, metadata_value=str(filename.name))

    def save(self, output_filename: str = ''):
        if not output_filename:
            output_filename = self._get_json_file()
        else:
            output_filename = Path(output_filename).with_suffix('.json')

        with open(output_filename, 'w') as fp:
            json.dump(self._container_metadata, fp)
