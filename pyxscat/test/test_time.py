from pyxscat.h5_integrator import H5GIIntegrator
from pyxscat.h5_integrator import ROOT_DIRECTORY_KEY, FILENAME_H5_KEY, SAMPLE_GROUP_KEY, PONI_GROUP_KEY
from pyxscat.h5_integrator import PONIFILE_DATASET_KEY
from silx.io.h5py_utils import File
from pathlib import Path
import fabio
import pytest
from pyFAI.io.ponifile import PoniFile
from pyxscat.other.integrator_methods import get_dict_from_name
from pyxscat.other.other_functions import date_prefix
from pyxscat.gui import INTEGRATION_PATH
import cProfile
import pstats
from pstats import SortKey
import time

TEST_PATH = Path(__file__).parent

EDF_EXAMPLES_PATH = 'test_edf'
NCD_PATH = 'test_NCD'
XMAS_PATH = 'test_xmas'
DUBBLE_PATH = 'test_DUBBLE'

NCD_EXAMPLE_PATH = TEST_PATH.joinpath(EDF_EXAMPLES_PATH, NCD_PATH).as_posix()
XMAS_EXAMPLE_PATH = TEST_PATH.joinpath(EDF_EXAMPLES_PATH, XMAS_PATH).as_posix()
DUBBLE_EXAMPLE_PATH = TEST_PATH.joinpath(EDF_EXAMPLES_PATH, DUBBLE_PATH).as_posix()

NCD_INIT_H5 = TEST_PATH.joinpath(EDF_EXAMPLES_PATH, NCD_PATH, f"{NCD_PATH}.h5").as_posix()
XMAS_INIT_H5 = TEST_PATH.joinpath(EDF_EXAMPLES_PATH, XMAS_PATH, f"{XMAS_PATH}.h5").as_posix()
DUBBLE_INIT_H5 = TEST_PATH.joinpath(EDF_EXAMPLES_PATH, DUBBLE_PATH, f"{DUBBLE_PATH}.h5").as_posix()

GLOBAL_PATH = TEST_PATH.joinpath(EDF_EXAMPLES_PATH).as_posix()
GLOBAL_INIT_H5 = TEST_PATH.joinpath(EDF_EXAMPLES_PATH, f"{EDF_EXAMPLES_PATH}.h5").as_posix()

@pytest.fixture(
        scope='session', 
        params=[
            # From Root Directory
            # (GLOBAL_PATH, '', ''),
            (NCD_EXAMPLE_PATH, '', ''),
            # (XMAS_EXAMPLE_PATH, '', ''),
            # (DUBBLE_EXAMPLE_PATH, '', ''),
            # # From input h5 filename
            # ('', GLOBAL_INIT_H5, ''),
            # ('', NCD_INIT_H5, ''),
            # ('', XMAS_INIT_H5, ''),
            # ('', DUBBLE_INIT_H5, ''),
        ]
    )
def h5(request):
    root_directory, input_h5_filename, output_filename_h5 = request.param
    print(f'Setting up H5GI instance with root_dir:{root_directory}, input_file:{input_h5_filename}, output_h5:{output_filename_h5}')
    timer_file = f'profile_results_{date_prefix()}.txt'
    return H5GIIntegrator(
            root_directory=root_directory,
            input_h5_filename=input_h5_filename,
            output_filename_h5=output_filename_h5,
        ), timer_file



# def ctimer(func):
#     def wrapper(*args, **kwargs):
#         # Create a Profile object
#         profiler = cProfile.Profile()
#         # Enable the profiler
#         profiler.enable()

#         res = func(args, kwargs)

#         profiler.disable()

#         # Save the stats to a file
#         profiler.dump_stats('profile_stats')
#         with open('profile_results.txt', 'w') as f:
#             p = pstats.Stats('profile_stats', stream=f)
#             p.sort_stats(SortKey.TIME)
#             p.print_stats()        
#         return res
        
#     return wrapper





class TestH5Time:

    def test_time_init_cprofile(self, h5):
        # Create a Profile object
        # profiler = cProfile.Profile()
        # # Enable the profiler
        # profiler.enable()

        time.sleep(1)

        # profiler.disable()

        # # Save the stats to a file
        # profiler.dump_stats('profile_stats')
        # with open(f'profile_results_{date_prefix()}.txt', 'w') as f:
        #     p = pstats.Stats('profile_stats', stream=f)
        #     p.sort_stats(SortKey.TIME)
        #     p.print_stats()