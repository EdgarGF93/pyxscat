from pathlib import Path
from silx.io import fabioh5, convert


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

def search_files(root_directory='', wildcards='*edf', generator=True, as_str=False, recursively=False):
    """Searches files inside the root directory filtering using the wildcards, can be recursively

    Args:
        root_directory (str, Path): path of the folder where to search
        wildcards (str): filtering wildcards, search by name
        generator (bool): if True, returns generator of Path instances
        as_str (bool): if True, returns list of strings 
        recursively (bool): if True, searches recursively in subfolders inside root_directory

    Raises:
        FileNotFoundError: _description_

    Returns:
        list, generator: contains the searched files
    """
    root_directory = Path(root_directory)

    if not root_directory.exists():
        raise FileNotFoundError
    
    if recursively:
        generator_files = root_directory.rglob(wildcards)
        list_files = sorted(root_directory.rglob(wildcards))
    else:
        generator_files = root_directory.glob(wildcards)

    if generator:
        return generator_files
    else:
        list_files = sorted(generator_files)

    if as_str:
        list_files = [str(item) for item in list_files]

    return list_files



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


