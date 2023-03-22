from os.path import join, basename, splitext,dirname
from os import listdir

DIRECTORY_SETUPS = join(dirname(__file__), 'setup_dictionaries')
SETUP_EXTENSION = ('.json', '.yaml')
NO_SETUP_INFORMATION = "Edf instance was created without any setup information."

def get_dict_setup(dict_setup=dict(), name_setup=str()) -> None:
    """
        Return a dictionary with the setup information
    """
    # Introduce the setup information through dictionary or importing its .json file
    try:
        if dict_setup and isinstance(dict_setup, dict):
            return dict_setup
        elif name_setup and isinstance(name_setup, str):
            return import_dict_setup(name_setup=name_setup)
        else:
            return dict()
    except:
        return dict()

def import_dict_setup(name_setup=str()) -> dict:
    """
        Search a setup_info file and return a dictionary with the setup information
    """
    if name_setup:
        # Get the list of stored setup_info files
        list_setup_info_files = get_setup_info_files()

        # Search for a match in the name
        for setup_file in list_setup_info_files:
            if name_setup == splitext(basename(setup_file))[0]:
                return {
                    '.json' : get_dict_fromjson(
                        json_file=setup_file
                    ),
                    '.yaml' : get_dict_fromyaml(
                        yaml_file=setup_file
                    ),
                }.get(
                    splitext(setup_file)[1],
                    NO_SETUP_INFORMATION,
                )
        print(NO_SETUP_INFORMATION)
        return dict()
    else:
        print(NO_SETUP_INFORMATION)
        return dict()

def get_dict_fromjson(json_file=str()) -> dict:
    """
        Import a json file and returns its dictionary
    """
    import json
    try:
        with open(join(DIRECTORY_SETUPS, json_file), 'r') as fp:
            return json.load(fp)
    except:
        print(NO_SETUP_INFORMATION)
        return dict()

def get_dict_fromyaml(yaml_file=str()) -> dict:
    """
        Import a yaml file and returns its dictionary
    """
    import yaml
    try:
        with open(join(DIRECTORY_SETUPS, yaml_file), 'r') as fp:
            return yaml.safe_load(fp)
    except:
        print(NO_SETUP_INFORMATION)
        return dict()

def get_setup_info_files():
    """
        Return a list with all the stored files with setup information
    """
    return [
        join(DIRECTORY_SETUPS, file) for file in listdir(DIRECTORY_SETUPS) if file.endswith(SETUP_EXTENSION)
    ]