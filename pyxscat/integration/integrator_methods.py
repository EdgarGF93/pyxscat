from os.path import join, dirname
import os

DIRECTORY_INTEGRATIONS = dirname(__file__)


def get_dict_integration(dict_integration=dict(), name_integration=str()) -> dict:
    """
        Return a dictionary of integration giving a name
    """
    # Get the dictionary with the integration parameters
    if dict_integration and isinstance(dict_integration, dict):
        return dict_integration
    elif name_integration and isinstance(name_integration, str):
        for d in get_dictionaries_integration():
            if name_integration == d['Name']:
                return d
    return


def get_dictionaries_integration() -> list:
    """
        Return a list with the dictionaries of all the available integrations
    """
    import json
    list_dicts = []
    for file in os.listdir(DIRECTORY_INTEGRATIONS):
        if file.endswith('json'):
            with open(join(DIRECTORY_INTEGRATIONS, file), 'r') as fp:
                list_dicts.append(
                    json.load(fp)
                )
    return list_dicts