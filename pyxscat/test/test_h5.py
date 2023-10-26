from pyxscat.h5_integrator import H5GIIntegrator
from pyxscat.h5_integrator import ROOT_DIRECTORY_KEY, FILENAME_H5_KEY, SAMPLE_GROUP_KEY, PONI_GROUP_KEY
from pyxscat.h5_integrator import PONIFILE_DATASET_KEY
from silx.io.h5py_utils import File
from pathlib import Path
import fabio
import pytest
from pyFAI.io.ponifile import PoniFile
from pyxscat.other.integrator_methods import get_dict_from_name
from pyxscat.gui import INTEGRATION_PATH

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


@pytest.fixture(
        scope='session', 
        params=[
            # From Root Directory
            (GLOBAL_PATH, '', ''),
            (NCD_EXAMPLE_PATH, '', ''),
            (XMAS_EXAMPLE_PATH, '', ''),
            (DUBBLE_EXAMPLE_PATH, '', ''),
            # From input h5 filename
            ('', GLOBAL_INIT_H5, ''),
            ('', NCD_INIT_H5, ''),
            ('', XMAS_INIT_H5, ''),
            ('', DUBBLE_INIT_H5, ''),

        ]
    )
def h5(request):
    root_directory, input_h5_filename, output_filename_h5 = request.param
    print(f'Setting up H5GI instance with root_dir:{root_directory}, input_file:{input_h5_filename}, output_h5:{output_filename_h5}')
    return H5GIIntegrator(
            root_directory=root_directory,
            input_h5_filename=input_h5_filename,
            output_filename_h5=output_filename_h5,
        ) 


class TestH5GI:

    # @classmethod
    # def setup_class(cls, example_path):
    #     print("Setting up setup class")
    #     cls.h5 = H5GIIntegrator(
    #         root_directory=example_path,
    #         input_h5_filename='',
    #         output_filename_h5='',
    #     ) 

    def test_init_root_dir_var(self, h5):
        print("testing the creation of self._root_dir")
        assert hasattr(h5, '_root_dir')

    def test_init_h5_filename_var(self, h5): 
        print("testing the creation of self._h5_filename")  
        assert hasattr(h5, '_h5_filename')

    def test_init_metadata_keys(self, h5): 
        print("testing the creation of key attributes")  
        assert hasattr(h5, '_iangle_key')
        assert hasattr(h5, '_tangle_key')
        assert hasattr(h5, '_norm_key')
        assert hasattr(h5, '_acq_key')

    def test_valid_h5_creation(self, h5):
        print("testing the creation of the h5 file") 
        output_h5_filename = h5._h5_filename

        assert output_h5_filename.is_file()
        assert output_h5_filename.suffix == '.h5'

        # output_h5_filename.unlink()

    def test_root_dir_attribute(self, h5):
        print("testing the root_dir attribute")
        h5_filename = h5._h5_filename
        with File(h5_filename, 'r+') as f:
            assert ROOT_DIRECTORY_KEY in f['.'].attrs

    def test_root_dir_attribute_valid(self, h5):
        print("testing the root_dir attribute is valid")
        h5_filename = h5._h5_filename
        with File(h5_filename, 'r+') as f:

            root_dir = f['.'].attrs[ROOT_DIRECTORY_KEY]
            assert h5.directory_valid(directory=root_dir)

    def test_root_dir_attribute_equal(self, h5):
        print("testing the root_dir attribute is equal to instance attribute")
        h5_filename = h5._h5_filename
        with File(h5_filename, 'r+') as f:
            root_dir = f['.'].attrs[ROOT_DIRECTORY_KEY]
            assert Path(root_dir).as_posix() == h5._root_dir.as_posix()

    def test_h5_filename_attribute(self, h5):
        print("testing the h5_filename attribute")
        h5_filename = h5._h5_filename
        with File(h5_filename, 'r+') as f:
            assert FILENAME_H5_KEY in f['.'].attrs

    def test_h5_filename_dir_attribute_valid(self, h5):
        print("testing the h5_filename attribute is valid")
        h5_filename = h5._h5_filename
        with File(h5_filename, 'r+') as f:
            h5_filename = f['.'].attrs[FILENAME_H5_KEY]
            assert Path(h5_filename).is_file()

    def test_h5_filename_attribute_equal(self, h5):
        print("testing the h5_filename attribute is equal to instance attribute")
        h5_filename = h5._h5_filename
        with File(h5_filename, 'r+') as f:
            _h5_filename = f['.'].attrs[FILENAME_H5_KEY]
            assert Path(_h5_filename).as_posix() == h5_filename.as_posix()

    def test_upload_ponifiles(self, h5):
        print('testing the uploading of .poni files')
        h5.update_ponifiles()

    def test_generate_ponifiles(self, h5):
        print('testing the retrieving of .poni files')
        ponifiles_in_h5 = h5.get_all_ponifiles(get_relative_address=False)

    def test_upload_ponifiles_valid(self, h5):
        print('testing the effective uploading of .poni files')
        ponifiles_in_dir = [f.as_posix() for f in h5._root_dir.rglob('*.poni')]
        ponifiles_in_h5 = h5.get_all_ponifiles(get_relative_address=False)
        assert set(ponifiles_in_dir) == set(ponifiles_in_h5)
        
    def test_no_repeat_ponifiles(self, h5):
        print('testing that the ponifiles are not repeated')
        h5.update_ponifiles()
        ponifiles_1 = h5.get_all_ponifiles(get_relative_address=False)
        h5.update_ponifiles()
        ponifiles_2 = h5.get_all_ponifiles(get_relative_address=False)
        assert len(ponifiles_1) == len(ponifiles_2)

    def test_activate_ponifiles_wrong(self, h5):
        print('testing the activation of a poni file')
        ponifile = 'not_stored_ponifile'
        h5.update_poni(poni=ponifile)
        assert h5.gi._poni == None

    def test_activate_abs_ponifile_valid(self, h5):
        print('testing the activation of a poni file')
        ponifile = [f.as_posix() for f in h5._root_dir.rglob('*.poni')][0]
        h5.update_poni(poni=ponifile)
        assert h5.gi._poni != None

    def test_activate_rel_ponifile_valid(self, h5):
        print('testing the activation of a poni file')
        ponifile = [f for f in h5._root_dir.rglob('*.poni')][0]
        ponifile_rel = ponifile.relative_to(h5._root_dir).as_posix()
        h5.update_poni(poni=ponifile_rel)
        assert h5.gi._poni != None

    def test_validate_poni_parameters(self, h5):
        print('testing the poni parameters')
        ponifile = [f.as_posix() for f in h5._root_dir.rglob('*.poni')][0]

        h5.update_poni(poni=ponifile)
        poni_instance = PoniFile(data=ponifile)

        assert poni_instance.dist == h5.gi._poni._dist
        assert poni_instance.wavelength == h5.gi._poni._wavelength
        assert poni_instance.poni1 == h5.gi._poni._poni1
        assert poni_instance.poni2 == h5.gi._poni._poni2
        assert poni_instance.rot1 == h5.gi._poni._rot1
        assert poni_instance.rot2 == h5.gi._poni._rot2
        assert poni_instance.rot3 == h5.gi._poni._rot3

        assert poni_instance.detector.name == h5.gi._poni.detector.name
        assert poni_instance.detector.binning == h5.gi._poni.detector.binning
        assert poni_instance.detector.shape == h5.gi._poni.detector.shape
        assert poni_instance.detector.pixel1 == h5.gi._poni.detector.pixel1
        assert poni_instance.detector.pixel2 == h5.gi._poni.detector.pixel2
    
    def test_upload_datafiles(self, h5):
        h5.update_datafiles(
            pattern='*.edf',
            search=True,
        )

    def test_generate_samples(self, h5):
        print('testing the sample-generator method')
        samples_in_h5 = h5.get_all_entries()
        
    def test_upload_samples_valid(self, h5):
        print('testing a valid uploading of samples')
        samples_in_root = set(h5.get_all_entries(get_relative_address=False))
        samples_in_h5 = set(h5.get_all_entries(get_relative_address=False))

        assert samples_in_root == samples_in_h5

    def test_generate_datafiles(self, h5):
        print('testing the datafile-generator method')
        files_in_h5 = h5.get_all_filenames()

    def test_upload_datafiles_valid(self, h5):
        print('testing a valid storage of sample-datafiles')
        dict_files_in_h5 = h5.get_dict_files()
        dict_files = h5.search_datafiles()

        samples = set(dict_files.keys())

        for s in samples:
            datafiles_in_h5 = set(dict_files_in_h5.get(s))
            datafiles_in_subdir = set(dict_files.get(s))

            assert datafiles_in_h5 == datafiles_in_subdir

    def test_no_repeat_datafiles(self, h5):
        print('testing that the datafiles are not repeated')
        h5.update_datafiles(
            pattern='*.edf',
            search=True,
        )
        dict_files_1 = h5.get_dict_files()
        h5.update_datafiles(
            pattern='*.edf',
            search=True,
        )
        dict_files_2 = h5.get_dict_files()

        samples = set(dict_files_1.keys())

        for s in samples:
            datafiles_1 = dict_files_1.get(s)
            datafiles_2 = dict_files_2.get(s)

            assert len(datafiles_1) == len(datafiles_2)


    def test_retrieve_filenames(self, h5):
        print('testing the valid retrieving of data filenames using relative or absolute address')

        rel_samples_in_h5 = h5.get_all_entries(get_relative_address=True)

        filename_from_relative = h5.get_filename_from_index(
            sample_name=rel_samples_in_h5[0],
            index_list=0,
        )

        abs_samples_in_h5 = h5.get_all_entries(get_relative_address=False)

        filename_from_absolute = h5.get_filename_from_index(
            sample_name=abs_samples_in_h5[0],
            index_list=0,
        )

        assert filename_from_relative == filename_from_absolute

    def test_retrieve_data(self, h5):
        print('testing the valid retrieving of data using relative or absolute address')
        rel_samples_in_h5 = h5.get_all_entries(get_relative_address=True)

        data_from_rel = h5.get_Edf_data(
            sample_name=rel_samples_in_h5[0],
            index_list=0,
        )

        abs_samples_in_h5 = h5.get_all_entries(get_relative_address=False)

        data_from_abs = h5.get_Edf_data(
            sample_name=abs_samples_in_h5[0],
            sample_relative_address=False,
            index_list=0,
        )

        assert data_from_rel.all() == data_from_abs.all()

    def test_retrieve_data_valid(self, h5):
        print('testing the valid retrieving of data')
        samples_in_h5 = h5.get_all_entries(get_relative_address=True)

        data_filename = h5.get_filename_from_index(
            sample_name=samples_in_h5[0],
            index_list=0,
        )
        data_from_fabio = fabio.open(data_filename).data

        data_from_h5 = h5.get_Edf_data(
            sample_name=samples_in_h5[0],
            index_list=0,
        )

        assert data_from_fabio.all() == data_from_h5.all()


    def test_radial_integration(self, h5):
        rel_samples_in_h5 = h5.get_all_entries(get_relative_address=True)
        list_integration_names = ['radial', 'radial_2']

        list_dict_integration = [get_dict_from_name(name=name, path_integration=INTEGRATION_PATH) for name in list_integration_names]

        data = h5.get_Edf_data(
            sample_name=rel_samples_in_h5[0],
            index_list=0,
        )

        for ind, res in enumerate(h5.raw_integration(
            data=data,
            norm_factor=1.0,
            list_dict_integration=list_dict_integration,
            )):
            assert res is not None

    def test_box_integration(self, h5):
        rel_samples_in_h5 = h5.get_all_entries(get_relative_address=True)
        list_integration_names = ['vertical_rod', 'horizontal_cut']

        list_dict_integration = [get_dict_from_name(name=name, path_integration=INTEGRATION_PATH) for name in list_integration_names]

        data = h5.get_Edf_data(
            sample_name=rel_samples_in_h5[0],
            index_list=0,
        )

        for res in h5.raw_integration(
            data=data,
            norm_factor=1.0,
            list_dict_integration=list_dict_integration,
            ):
            assert res is not None

    def test_azim_integration(self, h5):
        rel_samples_in_h5 = h5.get_all_entries(get_relative_address=True)
        list_integration_names = ['azim_complete', 'azim_oop']

        list_dict_integration = [get_dict_from_name(name=name, path_integration=INTEGRATION_PATH) for name in list_integration_names]

        data = h5.get_Edf_data(
            sample_name=rel_samples_in_h5[0],
            index_list=0,
        )

        for res in h5.raw_integration(
            data=data,
            norm_factor=1.0,
            list_dict_integration=list_dict_integration,
            ):
            assert res is not None