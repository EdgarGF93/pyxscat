from pyxscat.h5_integrator import H5GIIntegrator
from pathlib import Path
import fabio
from pyxscat import PATH_PYXSCAT
import pytest
# ROOT_DIRECTORY = r'C:\Users\edgar1993a\Work Folders\Documents\Python\pyxscat\edf_examples\test_NCD'
# SAMPLE1 = r'C:\Users\edgar1993a\Work Folders\Documents\Python\pyxscat\edf_examples\test_NCD\A1'
# OUTPUT_H5_FILENAME = r'C:\Users\edgar1993a\Work Folders\Documents\Python\pyxscat\edf_examples\test_NCD\test_NCD.h5'
# PONIFILE = r'C:\Users\edgar1993a\Work Folders\Documents\Python\pyxscat\edf_examples\test_NCD\Cr2O3.poni'

EDF_EXAMPLES_PATH = "edf_examples"
NCD_PATH = "test_NCD"
NCD_EXAMPLE_PATH = PATH_PYXSCAT.joinpath(EDF_EXAMPLES_PATH, NCD_PATH)

# class TestNCDHandler(unittest.TestCase):

def test_invalid_root_dir():
    root_dir = "wrong_directory"

    with pytest.raises(Exception):
        H5GIIntegrator(root_directory=root_dir)

def test_invalid_input_h5_file():
    input_h5_filename = "wrong_path"

    with pytest.raises(Exception):
        H5GIIntegrator(input_h5_filename=input_h5_filename)

def test_invalid_root_dir_and_input_file():
    input_h5_filename = "wrong_path"
    root_dir = "wrong_directory"

    with pytest.raises(Exception):
        H5GIIntegrator(
            input_h5_filename=input_h5_filename,
            root_directory=root_dir,
        )

    # def setUp(self) -> None:
    #     self.h5 = H5GIIntegrator(
    #         root_directory=NCD_EXAMPLE_PATH,
    #         input_filename_h5="",
    #         output_filename_h5="",
    #     )

    # def test_h5_file_creation(self):


        

        # h5.update_ponifiles(search=True)
        # h5.update_datafiles(search=True)

