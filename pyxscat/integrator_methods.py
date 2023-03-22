from os.path import join, dirname
import os

DIRECTORY_INTEGRATIONS = join(dirname(__file__), 'integration_dictionaries')



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