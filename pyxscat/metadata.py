
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path
from typing import List, Any

import fabio
from pyxscat.edf import EdfClass


FILENAMES = 'filenames'
NAMES = 'names'

PATTERNS = ['*.edf', '*.cbf', '*.tif', '*.tiff']
DEFAULT_PATTERN = '*.edf'
DIR_PATTERN = '**/'
# def get_dict_entry(pattern, entry):
#     d_entry = defaultdict(list)

#     for file in entry.glob(pattern):
#         d_entry['filenames'].append(str(file))
#         d_entry['names'].append(str(file.name))

#         header = EdfClass(filename=str(file)).get_header()
#         for metadata_key,metadata_value in header.items():
#             try:
#                 metadata_value = float(metadata_value)
#             except:
#                 metadata_value = str(metadata_value)
#             d_entry[metadata_key].append(metadata_value)
    
#     return d_entry

def get_dict_entry(file_generator):
    d_entry = defaultdict(list)

    for filename in file_generator:
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
        self.directory = directory
        self.pattern = pattern
        self.container = defaultdict(lambda : defaultdict(list))
    
    def _reset_container(self):
        self.container = defaultdict(lambda : defaultdict(list))

    def __iter__(self):
        pass

    def update_data(self):
        if self.container == defaultdict(lambda : defaultdict(list)):
            new_metadata = {str(subdir) : subdir.glob(self.pattern) for subdir in self.directory.rglob(DIR_PATTERN)}
        else:
            for subdir in self.directory.rglob(DIR_PATTERN):
                if str(subdir) not in self.container.keys():
                    new_metadata[str(subdir)] = subdir.glob(self.pattern)
                else:
                    new_metadata[str(subdir)] += [str(file) for file in subdir.glob(self.pattern) if file not in self.container[str(subdir)][FILENAMES]]