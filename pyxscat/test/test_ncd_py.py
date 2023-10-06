from pyxscat.h5_integrator import H5GIIntegrator
from pathlib import Path
import fabio
from pyxscat import PATH_PYXSCAT
import pytest
# ROOT_DIRECTORY = r'C:\Users\edgar1993a\Work Folders\Documents\Python\pyxscat\edf_examples\test_NCD'
# SAMPLE1 = r'C:\Users\edgar1993a\Work Folders\Documents\Python\pyxscat\edf_examples\test_NCD\A1'
# OUTPUT_H5_FILENAME = r'C:\Users\edgar1993a\Work Folders\Documents\Python\pyxscat\edf_examples\test_NCD\test_NCD.h5'
# PONIFILE = r'C:\Users\edgar1993a\Work Folders\Documents\Python\pyxscat\edf_examples\test_NCD\Cr2O3.poni'

EDF_EXAMPLES_PATH = 'edf_examples'
NCD_PATH = 'test_NCD'
XMAS_PATH = 'test_xmas'

NCD_EXAMPLE_PATH = PATH_PYXSCAT.joinpath(EDF_EXAMPLES_PATH, NCD_PATH).as_posix()
XMAS_EXAMPLE_PATH = PATH_PYXSCAT.joinpath(EDF_EXAMPLES_PATH, XMAS_PATH).as_posix()


def test_invalid_root_dir():
    root_dir = 'wrong_directory'

    with pytest.raises(Exception):
        H5GIIntegrator(root_directory=root_dir)

def test_invalid_input_h5_file():
    input_h5_filename = 'wrong_path'

    with pytest.raises(Exception):
        H5GIIntegrator(input_h5_filename=input_h5_filename)

def test_invalid_root_dir_and_input_file():
    input_h5_filename = 'wrong_path'
    root_dir = 'wrong_directory'

    with pytest.raises(Exception):
        H5GIIntegrator(
            input_h5_filename=input_h5_filename,
            root_directory=root_dir,
        )

import requests


@pytest.fixture
def from_root_dir():
    return [
        H5GIIntegrator(root_directory=NCD_EXAMPLE_PATH),
    ]
    
    
    


# @pytest.mark.parametrize(
#     'root_directory',
#     [
#         NCD_EXAMPLE_PATH,
#         # XMAS_EXAMPLE_PATH,
#     ]
# )
class TestFromRootDir:

    @pytest.fixture(autouse=True)
    def _request(self, from_root_dir):
        self.h5 = from_root_dir


    # @classmethod
    # @pytest.fixture(autouse=True, scope='module')
    # def setup_class(cls, request, root_directory):
    #     cls.instance = H5GIIntegrator(root_directory=root_directory)

    # def test_get_value(self):
    #     assert self.h5.get_value() == root_directory

    # def setup_method(self, root_directory):
    #     # root_directory = NCD_EXAMPLE_PATH
    #     self.h5 = H5GIIntegrator(
    #         root_directory=root_directory,
    #     )

    def test_init_root_dir_var(self):
        assert hasattr(self.instance, '_root_dir')

    def test_init_h5_filename_var(self):    
        assert hasattr(self.instance, '_h5_filename')

    # def test_valid_h5_creation(self):
    #     output_h5_filename = self.h5._h5_filename

    #     assert output_h5_filename.is_file()
    #     assert output_h5_filename.suffix == '.h5'

    #     output_h5_filename.unlink()













    # def setUp(self) -> None:
    #     self.h5 = H5GIIntegrator(
    #         root_directory=NCD_EXAMPLE_PATH,
    #         input_filename_h5="",
    #         output_filename_h5="",
    #     )

    # def test_h5_file_creation(self):


        

        # h5.update_ponifiles(search=True)
        # h5.update_datafiles(search=True)

