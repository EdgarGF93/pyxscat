from pathlib import Path
import json
from pyxscat.gui import INTEGRATION_PATH

KEY_INTEGRATION = "integration"
CAKE_LABEL = "cake"
CAKE_KEY_NAME = "name"
CAKE_KEY_SUFFIX = "suffix"
CAKE_KEY_UNIT = "unit"
CAKE_KEY_TYPE = "type"
CAKE_KEY_RRANGE = "radial_range"
CAKE_KEY_ARANGE = "azimuth_range"
CAKE_KEY_ABINS = "azim_bins"

CAKE_KEY_TYPE_AZIM = "azimuthal"
CAKE_KEY_TYPE_RADIAL = "radial"

CAKE_KEY_TYPES = {
    KEY_INTEGRATION : str(),
    CAKE_KEY_NAME : str(),
    CAKE_KEY_SUFFIX : str(),
    CAKE_KEY_UNIT : str(),
    CAKE_KEY_TYPE : str(),
    CAKE_KEY_RRANGE : list(),
    CAKE_KEY_ARANGE : list(),
    CAKE_KEY_ABINS : int(),
}

BOX_LABEL = "box"
BOX_KEY_NAME = "name"
BOX_KEY_SUFFIX = "suffix"
BOX_KEY_DIRECTION = "direction"
BOX_KEY_INPUT_UNIT = "input_unit"
BOX_KEY_OUTPUT_UNIT = "output_unit"
BOX_KEY_IPRANGE = "ip_range"
BOX_KEY_OOPRANGE = "oop_range"

BOX_KEY_TYPE_HORZ = "horizontal"
BOX_KEY_TYPE_VERT = "vertical"

BOX_KEY_TYPES = {
    KEY_INTEGRATION : str(),
    BOX_KEY_NAME : str(),
    BOX_KEY_SUFFIX : str(),
    BOX_KEY_DIRECTION : str(),
    BOX_KEY_INPUT_UNIT : str(),
    BOX_KEY_OUTPUT_UNIT : str(),
    BOX_KEY_OOPRANGE : list(),
    BOX_KEY_IPRANGE : list(),
}

def open_json(json_path=str()) -> dict:
    """
    Opens a json and returns a dict
    """

    json_file = Path(json_path)
    with open(json_file, 'r') as fp:
        dict_json = json.load(fp)
    return dict_json


def search_dictionaries_integration(path_integration=str()) -> list:
    """
    Return a list with the dictionaries of all the available integration
    """
    list_json_files = Path(path_integration).rglob('*.json')
    list_dict_integration = [open_json(file_json) for file_json in list_json_files]

    return list_dict_integration

def search_integration_names(path_integration=INTEGRATION_PATH) -> list:
    list_json_files = Path(path_integration).rglob('*.json')
    list_integration_cakes = []
    list_integration_boxes = []

    for file_json in list_json_files:
        dict_integration = open_json(file_json)
        if dict_integration[KEY_INTEGRATION] == CAKE_LABEL:
            name = dict_integration[CAKE_KEY_NAME]
            list_integration_cakes.append(name)
        elif dict_integration[KEY_INTEGRATION] == BOX_LABEL:
            name = dict_integration[BOX_KEY_NAME]
            list_integration_boxes.append(name)
        else:
            pass

    return list_integration_cakes, list_integration_boxes

def get_dict_from_name(name=str(), path_integration=str()) -> dict:
    """
    Open a json file and return a dictionary
    """
    json_file = path_integration.joinpath(f"{name}.json")
    dict_json = open_json(json_file)
    return dict_json

def fetch_dictionary_from_json(filename_json=str()) -> dict:
    """
    Open a json file and return a dictionary
    """
    filename_json = Path(filename_json)
    dict_json = open_json(filename_json)
    return dict_json

def locate_integration_file(name_integration=str()):
    full_filename = Path(INTEGRATION_PATH).joinpath(f"{name_integration}.json")
    if full_filename.is_file():
        return full_filename
    else:
        return
    
def save_integration_dictionary(dict_integration=dict()):
    output_filename = Path(INTEGRATION_PATH).joinpath(f"{dict_integration[CAKE_KEY_NAME]}.json")
    with open(output_filename, 'w+') as fp:
        json.dump(dict_integration, fp)

def is_cake_dictionary(dict_integration=dict()) -> bool:
    # Check if both dicts have the same keys
    if dict_integration.keys() != CAKE_KEY_TYPES.keys():
        return False

    # Check that the values are the same types
    for key, value in CAKE_KEY_TYPES.items():
        if type(value) != type(dict_integration[key]):
            return False
    return True

def is_box_dictionary(dict_integration=dict()) -> bool:
    # Check if both dicts have the same keys
    if dict_integration.keys() != BOX_KEY_TYPES.keys():
        return False

    # Check that the values are the same types
    for key, value in BOX_KEY_TYPES.items():
        if type(value) != type(dict_integration[key]):
            return False
    return True
