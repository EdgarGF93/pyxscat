from pathlib import Path
from silx.io import fabioh5, convert
from other.search_functions import search_files

EXTENSION_H5 = '.h5'

def create_h5_from_folder(folder='', wildcards='*.edf', h5_file=''):

    folder = Path(folder)

    if not folder.exists():
        raise FileNotFoundError
    
    fabio_series = get_fabio_serie_from_folder(
        path_of_files=folder,
        wildcards=wildcards,
    )

    if not h5_file:
        h5_file = folder.joinpath(f'{folder.name}{EXTENSION_H5}')
    
    convert.write_to_h5(
        infile=fabio_series,
        h5file=h5_file,
        h5path=folder,
        mode='a',
        overwrite_data=True,
    )

def get_fabio_serie_from_folder(folder=str(), wildcards='*.edf'):
    """
    Args:
        path_of_files (_type_, optional): _description_. Defaults to str().
        wildcards (str, optional): _description_. Defaults to '*.edf'.
    """
    folder = Path(folder)

    if not folder.exists():
        raise FileNotFoundError
    
    list_files = search_files(
        root_directory=folder,
        wildcards=wildcards,
        generator=False,
        as_str=True,
        recursively=False,
    )

    input_group = fabioh5.File(file_series=list_files)

    return input_group


