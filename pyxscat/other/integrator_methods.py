from pathlib import Path
import json
# DIRECTORY_INTEGRATIONS = Path(__file__).parent.joinpath("integration")


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

def search_integration_names(path_integration=str()) -> list:
    list_json_files = Path(path_integration).rglob('*.json')
    list_integration_cakes = []
    list_integration_boxes = []
    for file_json in list_json_files:
        dict_json = open_json(file_json)
        if dict_json["Type"] in ("Azimuthal", "Radial"):
            list_integration_cakes.append(dict_json["Name"])
        elif dict_json["Type"] in ("Horizontal", "Vertical"):
            list_integration_boxes.append(dict_json["Name"])

    return list_integration_cakes, list_integration_boxes

def get_dict_from_name(name=str(), path_integration=str()) -> dict:
    """
    Open a json file and return a dictionary
    """
    json_file = path_integration.joinpath(f"{name}.json")
    dict_json = open_json(json_file)
    return dict_json

