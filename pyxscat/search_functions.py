# Other functions commonly used for data analysis, without classes nor style
from os.path import join, exists, splitext
from pathlib import Path
import json
import os

ERROR_NOFOUND_FOLDER = 'No directory was found, check the name.'



def search_files_recursively(directory=str(), extension='', wildcards='*') -> list:
    """
        Search files recursively in folder and subfolders, according to extension and wildcards
    """
    list_files = []
    for path in Path(directory).rglob(wildcards):
        if str(path).endswith(extension):
            list_files.append(str(path))
    return list_files

def search_files_directory(directory=str(), name_conds=['.edf']) -> list:
    """
        Search files under conditions inside a folder, no recursively
    """
    return [join(directory, file) for file in os.listdir(directory) if all(cond in file for cond in name_conds)]

# Save a list into a txt file separated in lines
def list_to_txt(ls=[], output_txt='output.txt'):
    with open(output_txt, '+w') as text:
        for file in ls:
            text.write(f"{file}\n")

# Open a txt with info in lines and return the list
def txt_to_list(input_txt):
    with open(input_txt) as text:
        ls = [line.strip('\n') for line in text.readlines()]
    return ls

# Return a list of folders inside a directory that match some file conditions
def search_folders_ng(directory, conds=['.edf']):
    # Check if the folders contain some file that matches all the conditions, generates a list
    list_folders = []
    if all(cond in os.listdir(directory) for cond in conds):
        list_folders.append(directory)
    for (root, dirs, files) in os.walk(directory):
        for file in files:
            if all(cond in file for cond in conds) and root not in list_folders:
                list_folders.append(root)
    return list_folders

# Generate a text file with all folder names within subdirectories under filename conditions
def generate_folders_txt(main_dir, save_path='pyxscat', output_name='folders', name_conds=['.edf'], save=True) -> None:
    # Check if path exists
    if exists(join(main_dir, save_path)) is False:
        os.mkdir(join(main_dir, save_path))

    # Build the names of the input and output txt
    output_txt = splitext(output_name)[0] + '.txt'
    full_output_txt = join(main_dir, save_path, output_txt)

    # Check if the folders contain some file that matches all the conditions, generates a list
    list_folders = search_folders_ng(main_dir, name_conds)
    # Save a txt or return a list
    if save:
        list_to_txt(list_folders, full_output_txt)
    else:
        return list_folders

# Generate a text file with all filenames within subdirectories under name conditions
def generate_files_txt(main_dir, save_path='pyxscat', folders='folders', output_name='files', name_conds=['.edf'], save=True) -> None:
    # Check if path exists
    if exists(join(main_dir, save_path)) is False:
        os.mkdir(join(main_dir, save_path))

    # Check if the folders input attribute is a list or a text file name
    if isinstance(folders, list):
        folder_list = folders
    elif isinstance(folders, str):
        # Create the full names for the input and the output text files
        full_folder_txt = join(main_dir, save_path, splitext(folders)[0] + '.txt')
        full_output_txt = join(main_dir, save_path, splitext(output_name)[0] + '.txt')
        # Open the existing folder txt, a take a list
        folder_list = txt_to_list(full_folder_txt)
    else:
        raise TypeError

    # Check if folder_list is correact and search files on every folder
    assert isinstance(folder_list, list), f"Cannot find a list with folders"
    files_list = []
    for folder in folder_list:
        for file in search_files_ng(folder, name_conds):
            files_list.append(file)
    # Save into txt or return a list
    if save:
        list_to_txt(files_list, full_output_txt)
    else:
        return files_list

def makedir(directory):
    if exists(directory):
        return
    else:
        os.mkdir(directory)

def json_from_textfile(main_dir, save_path='pyxscat', name_json='files', files='files', files_ref='', ponifile='', beamline='xmas', rotated=True):
    """"
    Generate a .json file after input of files to analyze and characteristics
    """
    # Build the name of the future .json file
    name_json = join(main_dir, save_path, splitext(name_json)[0] + '.json')

    # Locate the ponifile (if exists)
    if ponifile:
        path_ponifile = join(main_dir, ponifile)

    # Check if save path exists
    makedir(join(main_dir, save_path))

    # LIST OF (SAMPLE) FILES
    # Check if the files comes in list or .txt file
    if isinstance(files, list):
        list_files = [join(main_dir, file) for file in files]
        # full_output_json = join(main_dir, save_path, splitext(name_json)[0] + '.json')
    elif isinstance(files, str):
        # Define the fullname for the input text file, the output json file and the calibrant path
        full_txt_file = join(main_dir, save_path, splitext(files)[0] + '.txt')
        list_files = txt_to_list(full_txt_file)
        # full_output_json = full_txt_file.replace('.txt', '.json')

    # Define a dictionary that will include the file names
    dict_files = list_files_to_dict(list_files)

    # LIST OF REFERENCE FILES
    if files_ref:
    # Check the files for the reference: Reference comes in a list of files or a full directory
        if isinstance(files_ref, list):
            list_files_ref = files_ref
        elif isinstance(files_ref, str):
            full_txt_file_ref = join(main_dir, save_path, splitext(files_ref)[0] + '.txt')
            list_files_ref = txt_to_list(full_txt_file_ref)
        dict_files_ref = list_files_to_dict(list_files_ref)
    else:
        dict_files_ref = {}

    # Create a global dictionary with all the required information and save it as a json file, that will be opened with method 'open_json'
    dict_total = {
        'Main_dir': main_dir,
        'json_file': name_json,
        'N_files': sum(len(v) for _,v in dict_files.items()),
        'Beamline':beamline, 
        'Rotated':rotated,
        'Calibrant':path_ponifile,
        'Folders':dict_files,
        'Folders_reference': dict_files_ref,
    }
    # Export the dictionary as a json file
    with open(name_json, 'w') as fp:
        json.dump(dict_total, fp)
    # print(f'The output json file is: {full_output_json}. This is a info file with all the info needed to integrate in batch mode.')


def json_from_conditions(main_dir=str(), files_list=[],save_path='pyxscat', name_json='files', subfolder_samples='',  subfolder_references='', conditions=['.edf'], ponifile_path='', rotated=True):
    """"
    Generate a .json file after input of files to analyze and characteristics
    """
    # Build the name of the future .json file
    name_json = join(main_dir, save_path, splitext(name_json)[0] + '.json')

    # Locate the ponifile (if exists)
    if exists(ponifile):
        path_ponifile = ponifile
    elif ponifile and exists(join(main_dir, ponifile)):
        path_ponifile = join(main_dir, ponifile)
    else:
        path_ponifile = ''

    # LIST OF SAMPLES FILES
    if exists(subfolder_samples):
        list_files = search_files_recursive(subfolder_samples, conditions)
    elif exists(join(main_dir, subfolder_samples)):
        list_files = search_files_recursive(join(main_dir, subfolder_samples), conditions)
    else:
        list_files = []
        print("No folder detected")
        return
    dict_files = list_files_to_dict(list_files)

    # LIST OF REFERENCE FILES FROM A FOLDER
    if exists(subfolder_references):
        list_files_ref = search_files_recursive(subfolder_references, conditions)
    elif subfolder_references and exists(join(main_dir, subfolder_references)):
        list_files_ref = search_files_recursive(join(main_dir, subfolder_references), conditions)
    else:
        list_files_ref = []
    dict_files_ref = list_files_to_dict(list_files_ref)

    # Check if save path exists
    makedir(join(main_dir, save_path))

    # Create a global dictionary with all the required information and save it as a json file, that will be opened with method 'open_json'
    dict_total = {'Main_dir': main_dir,
                'json_file': name_json,
                'N_files': sum(len(v) for _,v in dict_files.items()),
                'Beamline':beamline, 
                'Rotated':rotated,
                'Calibrant':path_ponifile,
                'Folders':dict_files,
                'Folders_reference': dict_files_ref,
                }
    # Export the dictionary as a json file
    with open(name_json, 'w') as fp:
        json.dump(dict_total, fp)
        print(f"The file was saved as: {name_json}")
        print(f"The json file contains {len(list_files)} files for samples and {len(list_files_ref)} files for reference.")
    return name_json

def json_from_setfiles(main_dir, set_files_samples=set(), set_files_reference=set(), save_path='pyxscat', name_json='files', ponifile='', beamline='xmas', rotated=True):
    """"
    Generate a .json file after input of files to analyze and characteristics
    """
    # Build the name of the future .json file
    name_json = join(main_dir, save_path, splitext(name_json)[0] + '.json')

    # Locate the ponifile (if exists)
    if exists(ponifile):
        path_ponifile = ponifile
    elif ponifile and exists(join(main_dir, ponifile)):
        path_ponifile = join(main_dir, ponifile)
    else:
        path_ponifile = ''

    # LIST OF SAMPLES FILES
    dict_files = list_files_to_dict(set_files_samples)

    # LIST OF REFERENCE FILES FROM A FOLDER
    dict_files_ref = list_files_to_dict(set_files_reference)

    # Check if save path exists
    makedir(join(main_dir, save_path))

    # Create a global dictionary with all the required information and save it as a json file, that will be opened with method 'open_json'
    dict_total = {'Main_dir': main_dir,
                'json_file': name_json,
                'N_files': sum(len(v) for _,v in dict_files.items()),
                'Beamline':beamline, 
                'Rotated':rotated,
                'Calibrant':path_ponifile,
                'Folders':dict_files,
                'Folders_reference': dict_files_ref,
                }

    # Export the dictionary as a json file
    with open(name_json, 'w') as fp:
        json.dump(dict_total, fp)
        print(f"The file was saved as: {name_json}")
        print(f"The json file contains {len(set_files_samples)} files for samples and {len(set_files_reference)} files for reference.")
    return name_json


def json_from_textfile(main_dir, save_path='pyxscat', name_json='files', files='files', files_ref='', ponifile='', beamline='xmas', rotated=True):
    """"
    Generate a .json file after input of files to analyze and characteristics
    """
    # Build the name of the future .json file
    name_json = join(main_dir, save_path, splitext(name_json)[0] + '.json')

    # Locate the ponifile (if exists)
    if ponifile:
        path_ponifile = join(main_dir, ponifile)

    # Check if save path exists
    makedir(join(main_dir, save_path))

    # LIST OF (SAMPLE) FILES
    # Check if the files comes in list or .txt file
    if isinstance(files, list):
        list_files = [join(main_dir, file) for file in files]
        # full_output_json = join(main_dir, save_path, splitext(name_json)[0] + '.json')
    elif isinstance(files, str):
        # Define the fullname for the input text file, the output json file and the calibrant path
        full_txt_file = join(main_dir, save_path, splitext(files)[0] + '.txt')
        list_files = txt_to_list(full_txt_file)
        # full_output_json = full_txt_file.replace('.txt', '.json')

    # Define a dictionary that will include the file names
    dict_files = list_files_to_dict(list_files)

    # LIST OF REFERENCE FILES
    if files_ref:
    # Check the files for the reference: Reference comes in a list of files or a full directory
        if isinstance(files_ref, list):
            list_files_ref = files_ref
        elif isinstance(files_ref, str):
            full_txt_file_ref = join(main_dir, save_path, splitext(files_ref)[0] + '.txt')
            list_files_ref = txt_to_list(full_txt_file_ref)
        dict_files_ref = list_files_to_dict(list_files_ref)
    else:
        dict_files_ref = {}

    # Create a global dictionary with all the required information and save it as a json file, that will be opened with method 'open_json'
    dict_total = {
        'Main_dir': main_dir,
        'json_file': name_json,
        'N_files': sum(len(v) for _,v in dict_files.items()),
        'Beamline':beamline, 
        'Rotated':rotated,
        'Calibrant':path_ponifile,
        'Folders':dict_files,
        'Folders_reference': dict_files_ref,
    }
    # Export the dictionary as a json file
    with open(name_json, 'w') as fp:
        json.dump(dict_total, fp)
    # print(f'The output json file is: {full_output_json}. This is a info file with all the info needed to integrate in batch mode.')


def check_subfolder(main_directory=str(), subfolder=str(), return_something=False):
    """
        Check an existing directory by itself or inside a main directory
    """
    if exists(subfolder):
        return subfolder
    elif subfolder and exists(join(main_directory, subfolder)):
        return join(main_directory, subfolder)
    else:
        if return_something:
            return main_directory
        else:
            return None

def dict_from_conditions(main_dir=str(), list_files=[], subfolder_samples='', list_files_ref=[], subfolder_references='', conditions=['.edf'], \
    dict_setup=dict(), name_setup=str(), ponifile_path='', rotated=True) -> dict:
    """"
    Return a dictionary with all the information and files to integrate
    """
    assert exists(main_dir), ERROR_NOFOUND_FOLDER

    # Get the main directory with subfolder or not
    main_dir = check_subfolder(
        main_directory=main_dir,
        subfolder=subfolder_samples,
        return_something=True
    )

    # Get the directory of ponifile and subfolder with reference files
    path_ponifile = check_subfolder(
        main_directory=main_dir,
        subfolder=ponifile_path,
        return_something=False,
    )

    subfolder_references = check_subfolder(
        main_directory=main_dir,
        subfolder=subfolder_references,
        return_something=False,
    )

    # Get the samples files
    if list_files:
        dict_files_samples = list_files_to_dict(
            list_files=list_files,
        )
    else:
        dict_files_samples = list_files_to_dict(
            list_files=search_files_recursive(
                maindir=main_dir,
                name_conds=conditions
            ),
        )

    # Get the reference files
    if list_files_ref:
        dict_files_ref = list_files_to_dict(
            list_files=list_files_ref,
        )
    elif subfolder_references:
        dict_files_ref = list_files_to_dict(
            list_files=search_files_recursive(
                maindir=subfolder_references,
                name_conds=conditions
            ),
        )
    else:
        dict_files_ref = dict()

    return {'Main_dir': main_dir,
            'N_files': sum(len(v) for _,v in dict_files_samples.items()),
            'Folders':dict_files_samples,
            'Folders_reference': dict_files_ref,
            'Dict_setup': get_dict_setup(
                dict_setup=dict_setup,
                name_setup=name_setup,
            ),
            'Rotated':rotated,
            'Calibrant':path_ponifile,
            }


def get_dict_setup(dict_setup=dict(), name_setup=str()):
    """
        Return a dictionary with the setup information
    """
    # Introduce the setup information through dictionary or importing its .json file
    if dict_setup and isinstance(dict_setup, dict):
        return dict_setup
    elif name_setup and isinstance(name_setup, str):
        import json
        with open(join(DIRECTORY_SETUPS, f"{name_setup}.json"), 'r') as fp:
            return json.load(fp)
    else:
        return None

def list_files_to_dict(list_files = []) -> dict:
    """
        Take a list of files and return a dictionary with sorted files in folders
    """
    if list_files:
        dict_files = {}
        for ind,file in enumerate(list_files):
            # Initiate
            if ind == 0:
                partial_list = []
                folder = os.path.dirname(file)
            # If folder is different
            if os.path.dirname(file) != folder:
                dict_files[folder] = partial_list
                partial_list = []
                folder = os.path.dirname(file)
            partial_list.append(file)
            # If list is over
            if ind == len(list_files)-1:
                dict_files[folder] = partial_list
        return dict_files
    else:
        return {}

def txt_files_to_dict(filename):
    """
        Take a text file with filenames (full directory), return a dictionary with files sorted in folders
    """
    # Open the text file and fill the dictionaries
    with open(filename) as text:
        lines = text.readlines()
        files_list = [line.strip('\n') for line in lines]
        # Clean list
        files_list = [file for file in files_list if file != '']
        # Build up the dictionary
        dict_files = {}
        for ind,file in enumerate(files_list):
            # Initiate
            if ind == 0:
                partial_list = []
                folder = os.path.dirname(file)
            # If folder is different
            if os.path.dirname(file) != folder:
                dict_files[folder] = partial_list
                partial_list = []
                folder = os.path.dirname(file)
            partial_list.append(file)
            # If list is over
            if ind == len(files_list)-1:
                dict_files[folder] = partial_list
    return dict_files

# Returns a dictionary from a previously saved json file
def open_json(main_dir, filename) -> dict:
    with open(os.path.join(main_dir, filename)) as json_file:
        return json.load(json_file)

def input_json():
    print('There is no json file for reference subtraction. Do you want to input a json file? (y/n)\n')
    ans = input()
    if ans in ['y', 'Y', 'yes', 'Yes']:
        while True:
            print('Please, type the name of the json_file (with or w/o the .json extension). The file should be in the main dir\n')
            json_file = input()
            json_fullname = os.path.join(self.dict_info['main_dir'], os.path.splitext(json_file)[0] + '.json')
            if os.path.exists(json_fullname):
                print(f'The json file for reference subtraction is {json_file}\n')
                return json_fullname
            else:
                print('No json detected with that name. Do you want to try again? (y/n)\n')
                ans2 = input()
                if ans2 in ['y', 'Y', 'yes', 'Yes']:
                    pass
                else:
                    print('No json for reference was added. The integration will proceed without subtraction.\n')
                    break
    else:
        print('No json was found. No json, no party.\n Cheers!')
        return None

def get_subfolder(full_directory=str(), main_directory=str()) -> str:
    """
        Return the subfolder of a full_directory
    """
    return str(Path(full_directory).relative_to(Path(main_directory)))







    # if full_directory and exists(full_directory):
    #     if full_directory == main_directory:
    #         return full_directory
    #     subfolder_list = [item for item in full_directory.split(os.sep) if item not in main_directory.split(os.sep)]
    #     return os.path.join(*subfolder_list)
    # else:
    #     return