
from collections import defaultdict
from threading import Thread
from pathlib import Path
from typing import List, Any

import fabio
import json
from pyxscat.edf import FullHeader


FILENAMES = 'filenames'
NAMES = 'names'

PATTERNS = ['*.edf', '*.cbf', '*.tif', '*.tiff']
DEFAULT_PATTERN = '*.edf'
DIR_PATTERN = '**/'

class MetadataBase:
    def __init__(self, directory, pattern, json_file=None, update_metadata=True):
        self._directory = Path(directory)
        self.pattern = pattern
        self._container = defaultdict(lambda : defaultdict(list))
        self._container_newfiles = defaultdict(lambda : defaultdict(list))

        if update_metadata:
            self.update_new_metadata(return_dict=False)
    
    @property
    def container(self):
        return self._container
    
    @property
    def container_newfiles(self):
        return self._container_newfiles 

    @property
    def directory(self):
        return str(self._directory)
    
    def _reset_container(self):
        self._container = defaultdict(lambda : defaultdict(list))

    def __iter__(self):
        for subdirectory in self._container.keys():
            for filename in self._container[subdirectory][FILENAMES]:
                yield filename

    def get_relative_path(self, absolute_path: str = ''):
        return str(Path(absolute_path).relative_to(self._directory))
    
    def get_absolute_path(self, relative_path : str = ''):
        return str(self._directory.joinpath(relative_path))

    def gen_entries(self, relative_path=True):
        for entry in self._container.keys():
            if relative_path:
                yield self.get_relative_path(absolute_path=entry)
            else:
                yield entry

    def gen_new_entries(self, relative_path=True):
        for entry in self._container_newfiles.keys():
            if relative_path:
                yield str(Path(entry).relative_to(self._directory))
            else:
                yield entry

    def gen_files(self, relative_path=True):
        for filename in self.__iter__():
            if relative_path:
                yield self.get_relative_path(absolute_path=filename)
            else:
                yield filename

    def gen_new_files(self, relative_path=True):
        for entry in self._container_newfiles.keys():
            for filename in self._container_newfiles[entry][FILENAMES]:
                if relative_path:
                    yield self.get_relative_path(absolute_path=filename)
                else:
                    yield filename

    def _get_files(self) -> dict:
        return {str(subdir) : subdir.glob(self.pattern) for subdir in self._directory.rglob(DIR_PATTERN)}

    def _get_new_files(self) -> dict:
        new_metadata = defaultdict(list)
        for subdir in self._directory.rglob(DIR_PATTERN):
            if str(subdir) not in self._container.keys():
                new_metadata[str(subdir)] = subdir.glob(self.pattern)
            else:
                new_metadata[str(subdir)].extend([str(file) for file in subdir.glob(self.pattern) if str(file) not in self._container[str(subdir)][FILENAMES]])
        return new_metadata

    def get_new_files(self) -> dict:
        if self._container == defaultdict(lambda : defaultdict(list)):
            dict_new_files = self._get_files()
        else:
            dict_new_files = self._get_new_files()

        return dict_new_files
    
    def append(self, entry_name: str, metadata_key: str, metadata_value: Any):
        self._container[entry_name][metadata_key].append(metadata_value)

    def get_header(self, filename: str):
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
        filename = Path(filename)

        # ADDITIONAL METADATA
        self.append(entry_name=str(entry_name), metadata_key=FILENAMES, metadata_value=str(filename))
        self.append(entry_name=str(entry_name), metadata_key=NAMES, metadata_value=str(filename.name))

        # Get Fabio header
        header = self.get_header(filename=filename)
        for metadata_key,metadata_value in header.items():
            try:
                metadata_value = float(metadata_value)
            except:
                metadata_value = str(metadata_value)
            self.append(entry_name=str(entry_name), metadata_key=metadata_key, metadata_value=metadata_value)

    def update_entry_single(self, entry_name, filename):
        Thread(target=self._update_entry_single, args=(entry_name, filename)).start()

    def update_entry(self, entry_name, file_iter, threading=False):
        iter_empty = True

        for filename in file_iter:
            iter_empty = False
            if threading:
                self.update_entry_single(entry_name=entry_name, filename=filename)
            else:
                self._update_entry_single(entry_name=entry_name, filename=filename)
        return iter_empty

    def update_new_metadata(self, threading=False, return_dict=True) -> dict:
        dict_new_files = self.get_new_files()

        dict_new_files_clear = dict_new_files.copy()
        for subdirectory, file_iterator in dict_new_files.items():
            if self.update_entry(
                entry_name=subdirectory,
                file_iter=file_iterator,
                threading=threading,
                ):
                del dict_new_files_clear[subdirectory]

        self._container_newfiles = dict_new_files_clear
        if return_dict:
            return dict_new_files_clear
        
    def save(self, output_filename: str = ''):
        if not output_filename:
            output_filename = self._directory.joinpath(f'{self._directory.name}_pyxscat_mdb.json')
        else:
            output_filename = Path(output_filename).with_suffix('.json')

        with open(output_filename, 'w') as fp:
            json.dump(self._container, fp)


class EdfMetadata(MetadataBase):

    def __init__(self, directory):
        super().__init__(directory=directory, pattern="*.edf")



class PoniMetadata(MetadataBase):
    def __init__(self, directory):
        super().__init__(directory=directory, pattern="*.poni")

    def _update_entry_single(self, entry_name: Path, filename: Path):
        filename = Path(filename)

        # ADDITIONAL METADATA
        self.append(entry_name=str(entry_name), metadata_key=FILENAMES, metadata_value=str(filename))
        self.append(entry_name=str(entry_name), metadata_key=NAMES, metadata_value=str(filename.name))

    def save(self, output_filename: str = ''):
        if not output_filename:
            output_filename = self._directory.joinpath(f'{self._directory.name}_pyxscat_poni.json')
        else:
            output_filename = Path(output_filename).with_suffix('.json')

        with open(output_filename, 'w') as fp:
            json.dump(self._container, fp)
