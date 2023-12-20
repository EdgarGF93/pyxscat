
from collections import defaultdict
from multiprocessing import Pool
from threading import Thread
from pathlib import Path
from typing import List, Any

import fabio
from pyxscat.edf import EdfClass


FILENAMES = 'filenames'
NAMES = 'names'

PATTERNS = ['*.edf', '*.cbf', '*.tif', '*.tiff']
DEFAULT_PATTERN = '*.edf'
DIR_PATTERN = '**/'

def get_entry_dict(file_iter):
    d_entry = defaultdict(list)

    for filename in file_iter:
        filename = Path(filename)

        d_entry[FILENAMES].append(str(filename))
        d_entry[NAMES].append(str(filename.name))

        header = EdfClass(filename=str(filename)).get_header()
        for metadata_key,metadata_value in header.items():
            try:
                metadata_value = float(metadata_value)
            except:
                metadata_value = str(metadata_value)
            d_entry[metadata_key].append(metadata_value)
    return d_entry


def get_single_dict(filename):
    d_entry = defaultdict(list)
    filename = Path(filename)

    d_entry[FILENAMES].append(str(filename))
    d_entry[NAMES].append(str(filename.name))

    header = EdfClass(filename=str(filename)).get_header()
    for metadata_key,metadata_value in header.items():
        try:
            metadata_value = float(metadata_value)
        except:
            metadata_value = str(metadata_value)
        d_entry[metadata_key].append(metadata_value)

    return d_entry



class MetadataBase:
    def __init__(self, directory, pattern: str = DEFAULT_PATTERN):
        self._directory = Path(directory)
        self.pattern = pattern
        self.container = defaultdict(lambda : defaultdict(list))
        self._empty = True

    @property
    def directory(self):
        return str(self._directory)
    
    def _reset_container(self):
        self.container = defaultdict(lambda : defaultdict(list))

    def __iter__(self):
        for subdirectory in self.container.keys():
            for filename in self.container[subdirectory]:
                yield filename

    def _get_files(self) -> dict:
        return {str(subdir) : subdir.glob(self.pattern) for subdir in self._directory.rglob(DIR_PATTERN)}

    def _get_new_files(self) -> dict:
        new_metadata = defaultdict(list)
        for subdir in self._directory.rglob(DIR_PATTERN):
            if str(subdir) not in self.container.keys():
                new_metadata[str(subdir)] = subdir.glob(self.pattern)
            else:
                new_metadata[str(subdir)].extend([str(file) for file in subdir.glob(self.pattern) if str(file) not in self.container[str(subdir)][FILENAMES]])
        return new_metadata

    def get_new_files(self):
        if self._empty == True:
            dict_new_files = self._get_files()
        else:
            dict_new_files = self._get_new_files()

        return dict_new_files

    def _update_entry_single(self, entry_name, filename):
        filename = Path(filename)

        self.container[str(entry_name)][FILENAMES].append(str(filename))
        self.container[str(entry_name)][NAMES].append(str(filename.name))

        header = EdfClass(filename=str(filename)).get_header()
        for metadata_key,metadata_value in header.items():
            try:
                metadata_value = float(metadata_value)
            except:
                metadata_value = str(metadata_value)
            self.container[str(entry_name)][metadata_key].append(metadata_value)

    def update_entry_single(self, entry_name, filename):
        Thread(target=self._update_entry_single, args=(entry_name, filename)).start()

    def update_entry(self, entry_name, file_iter):
        for filename in file_iter:
            self.update_entry_single(entry_name=entry_name, filename=filename)

    def update_new_metadata(self, return_dict=True) -> dict:
        dict_new_files = self.get_new_files()

        for subdirectory, file_iterator in dict_new_files.items():
            self.update_entry(
                entry_name=subdirectory,
                file_iter=file_iterator,
            )
        if return_dict:
            return dict_new_files
