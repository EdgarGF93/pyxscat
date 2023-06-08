from .search_functions import search_files_recursively
from os.path import dirname, exists
from collections import defaultdict
import json

DIRECTORY_SETUPS = dirname(__file__)
KEYS_SETUP_DICTIONARY = ['Name', 'Angle', 'Tilt angle', 'Norm', 'Exposure']

def get_empty_setup_dict(list_keys=KEYS_SETUP_DICTIONARY) -> defaultdict:
    """
    Returns a default dict with the keys of a setup dictionary, default item = str

    Parameters:
    list_keys (list, set) : strings to be the keys of a dictionary that will identify important metadata during data processing

    Returns:
    defaultdict : default value (string)
    """
    new_dict = defaultdict(str)
    for key in list_keys:
        new_dict[key] = ''
    return new_dict

def filter_dict_setup(dictionary=dict()):
    """
    Takes a dictionary (or defaultdict), returns a default_dict with only the correct keys of a setup_dictionary

    Parameters:
    dictionary (dict, defaultdict) : dictionary with (in principle) the correct keys of a setup dictionary

    Returns:
    defaultdict : defaultdict with the correct keys and values of a setup dictionary, if there is an error with the key, the value is empty string
    """
    try:
        input_dict_setup = defaultdict(str, dictionary)
    except TypeError:
        return get_empty_setup_dict()

    new_dict_setup = get_empty_setup_dict()

    for key in KEYS_SETUP_DICTIONARY:
        new_dict_setup[key] = input_dict_setup[key]

    return new_dict_setup

def get_dict_setup_from_json(json_path=str()) -> defaultdict:
    """
    Reads a .json file, returns a defaultdict with the correct keys and values of a setup dictionary (with empty strings if error)

    Parameters:
    json_path(string) : path for the json_file

    Returns:
    defaultdict : with the correct keys and values, already filtered. None if error.
    """
    if exists(json_path):
        try:
            with open(json_path, 'r') as fp:
                imported_dict = json.load(fp)
                filtered_dict = filter_dict_setup(
                    dictionary=imported_dict,
                )
                return filtered_dict

        except OSError:
            return
    else:
        return

def get_dict_setup_from_name(name=str()) -> defaultdict:
    """
    Finds a .json file that matches with the key value 'Name'
    Returns a defaultdict with the correct keys and values for setup dictionary. None if there is no match.

    Parameters:
    name(str) : value of the key 'Name' for the desired setup dictionary

    Returns:
    defaultdict : matched defaultdict with the key 'Name', None if there is no match
    """
    list_dict_setups = search_dictionaries_setup()
    for d in list_dict_setups:
        if d['Name'] == name:
            filtered_dict = filter_dict_setup(
                    dictionary=d,
                )
            return filtered_dict
    return

def get_dict_setup(dict_setup=defaultdict, name_dict_setup=str(), path_json=str()) -> defaultdict:
    """
    Returns a defaultdict with correct keys/values for a setup dictionary searching the name of loading a .json file
    
    Parameters:
    dict(defaultdict) : (may) contains the correct pairs of key-values
    name_dict(str) : 'Name' key value to search
    path_json(str) : path of the json file to load a setup dictionary

    Returns:
    defaultdict : contains the correct pairs of key-value for a setup dictionary, empty if nothing works
    """
    if dict_setup:
        dict_setup = filter_dict_setup(
            dictionary=dict_setup,
        )
        return dict_setup

    if name_dict_setup:
        dict_setup = get_dict_setup_from_name(
            name=name_dict_setup,
        )

        if dict_setup:
            return dict_setup

    if path_json:
        dict_setup = get_dict_setup_from_json(
            json_path=path_json,
        )

        if dict_setup:
            return dict_setup

    return get_empty_setup_dict()

def search_dictionaries_setup(directory_setups=DIRECTORY_SETUPS) -> list:
    """
    Return a list with the dictionaries of all the available setups

    Parameters:
    directory_setups(str) : the path to find .json files

    Returns:
    list : contains the defaultdict with only correct keys and keys (already filtered)
    """
    list_dict_setups = []

    list_json_files = search_files_recursively(
        directory=directory_setups,
        extension='.json',
    )

    for json_file in list_json_files:
        dict_setup = get_dict_setup_from_json(json_file)

        if dict_setup:
            list_dict_setups.append(dict_setup)

    return list_dict_setups