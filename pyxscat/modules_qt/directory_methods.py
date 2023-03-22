
from os.path import dirname, exists, join
import os

ERROR_MAIN_DIRECTORY = "The main directory does not exist. Check the path."

def get_fulldirectory(maindir='', subfolder='', cwd_default=True):
    """
        Build, search, create and returns the main directory
    """
    if cwd_default and (exists(maindir) is False):
        maindir = os.getcwd()

    assert exists(maindir), ERROR_MAIN_DIRECTORY

    # Check if the subfolder string is a full path
    full_directory = subfolder if maindir in dirname(subfolder) else join(maindir, subfolder)

    # Check if the folder exists, if not, create
    create_folder(full_directory)

    return full_directory


def create_folder(folder=str()) -> None:
    """
        Create a folder if it does not exist
    """
    if exists(folder):
        pass
    else:
        os.mkdir(folder)


def join_directory(maindir='', subfolder=''):
    """
        Join or full directory
    """
    # Check if the subfolder string is a full path
    full_directory = subfolder if maindir in dirname(subfolder) else join(maindir, subfolder)

    return full_directory