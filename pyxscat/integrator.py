import matplotlib.pyplot as plt
from setup.setup_methods import get_dict_setup
from integration.integrator_methods import *
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
from pygix.transform import Transform
import numpy as np
import json
from os.path import exists, join, dirname
from save import *
from plots import *
from decorators import *
from other_functions import *
from edf import EdfClass
from search_functions import dict_from_conditions, check_subfolder, list_files_to_dict, search_files_recursively
from integration.integrator_methods import get_dict_integration

PATH_INTEGRATOR = dirname(__file__)

ERROR_INPUT_JSON = "Integrator could not be init from json. Continue."
ERROR_INIT_FILES = "The dictionary of files could not be init."
ERROR_INIT_FILES_REF = "The dictionary of reference files could not be init."
NO_SETUP_INFORMATION = "Integrator instance was created without any setup information."

DICT_SAMPLE_ORIENTATIONS = {
    (True,True) : 1,
    (True,False) : 2,
    (False,True) : 3,
    (False,False) : 4,
}

DICT_BOX_ORIENTATION = {
    'Horizontal' : 'ipbox',
    'Vertical' : 'opbox',
}

OUTPUT_FOLDER = 'PyXScat'
LOGFILE_NAME = 'Logging'
ERROR_RAW_INTEGRATION = "Failed at detect integration type."

POLARIZATION_FACTOR = 0.99

NAMES_RADIAL_RANGE = ['Radial_range','Rad_range','qrange','radial_range','q_range', 'Radial']
NAMES_AZIMUTH_RANGE = ['Azimuth_range', 'azimuth_range', 'azim_range', 'Azim_range', 'Azimuth', 'Azim']
NAMES_QNM_UNIT = ['q_nm^-1', 'qnm-1', 'qnm', 'nm', 'q']
NAMES_QA_UNIT = ['q_A', 'qA', 'A']
NAMES_2THETA = ['2th_deg', '2theta', '2th', 'theta', 'th', 'deg', 'degrees']

NPT_RADIAL = int(100)

NAMES_UNIT_CORRESPONDENCE = {
    'q_nm^-1' : NAMES_QNM_UNIT,
    'q_A^-1' : NAMES_QA_UNIT,
    '2th_deg' : NAMES_2THETA,
}

AZIMUTH_NAME = 'Azimuthal'
RADIAL_NAME = 'Radial'
HORIZONTAL_NAME = 'Horizontal'
VERTICAL_NAME = 'Vertical'

DEFAULT_UNIT = 'q_nm^-1'

SORTED_PARAMETERS = ['Folder', 'Pitch']

SCALAR_RANGE = np.linspace(0,1,10)
SUBTRACT_VALUE = 0.1
DEFAULT_METHOD_SUBTRACTION = 'mean'

LIMS_X_IMAGE = [-2,20]
LIMS_Y_IMAGE = [0,20]
TICKS_X = [0,5,10,15,20]
TICKS_Y = [0,5,10,15,20]
WEAK_LIMIT_VALUES = [0,4]
FONT_SIZE_TICKS = 20
FONT_SIZE_LABELS = 30
FONT_SIZE_TITLE = 20
LABEL_X = r'$q_{r}$ $(nm^{-1})$'
LABEL_Y = r'$q_{z}$ $(nm^{-1})$'
COLORBAR = False

class Integrator(Transform):
    def __init__(
        self,
        main_dir=str(),
        yaml_json_file=str(), 
        dict_files=dict(),
        dict_files_ref=dict(),
        list_files=list(), 
        list_files_ref=list(), 
        list_subfolder_ref=list(),
        extension='.edf',
        wildcards='*',
        dict_setup=dict(),
        name_setup=str(),
        ponifile_path=str(),
        # rotated=False, 
        qz_parallel=True, 
        qr_parallel=True,
        search_files=True,
    ):
        """
            Integrator class inherits the data from Geometry and contains methods to integrate through PyFAI
        """
        # Get the main directory
        self.update_main_directory(
            main_dir=main_dir,
        )

        # Get/search the dictionary of files
        self.update_dict_files(
            yaml_json_file=yaml_json_file,
            dict_files=dict_files,
            list_files=list_files,
            extension=extension,
            wildcards=wildcards,
            search_files=search_files,
        )

        # Get/search the dictionary of files for reference
        self.update_dict_ref_files(
            dict_files_ref=dict_files_ref,
            list_files_ref=list_files_ref,
            list_subfolder_ref=list_subfolder_ref,
        )

        # Get the dictionary, information of the setup
        self._dict_setup = get_dict_setup(
            dict_setup=dict_setup,
            name_setup=name_setup
        )

        # Get a ponifile
        self.update_ponifile(
            ponifile_path=ponifile_path,
        )
        # Get attributes from Transform class (pygix module)
        self.update_transformQ()

        # Update rotation, orientation parameters
        self.update_orientation(
            qz_parallel=qz_parallel,
            qr_parallel=qr_parallel,
        )


    def update_main_directory(self, main_dir=str()) -> None:
        """
            Update the main directory attribute
        """
        if main_dir:
            try:
                if exists(main_dir):
                    self._main_directory = main_dir
                else:
                    self._main_directory = ''
            except:
                self._main_directory = ''
        else:
            self._main_directory = ''

    def update_dict_files(
        self,
        yaml_json_file=str(),
        dict_files=dict(), 
        list_files=[], 
        extension='.edf', 
        wildcards='*', 
        search_files=True,
    ) -> None:
        """
            Update the dictionary of folders and files
        """
        # Get directly an input dictionary of files
        if dict_files:
            self._dict_files = dict_files
            return
        # Try to init from a list of files
        elif list_files:
            try:
                self._dict_files = list_files_to_dict(
                    list_files=list_files,
                )
                return
            except:
                pass

        # Elif get the list by searching in main_dir using extension and wildcards
        elif self._main_directory and search_files:
            try:
                list_files = search_files_recursively(
                    directory=self._main_directory,
                    extension=extension,
                    wildcards=wildcards,
                )
                self._dict_files = list_files_to_dict(
                    list_files=list_files,
                )
                return
            except:
                pass
        else:
            self._dict_files = dict()

    def update_dict_ref_files(
        self,
        dict_files_ref=dict(),
        list_files_ref=[], 
        list_subfolder_ref=[],
    ) -> None:
        """
            Update the dictionary of folders and files used for reference
        """
        # Get directly a dictionary with reference files
        if dict_files_ref:
            self._dict_files_ref = dict_files_ref
            return
        # Try to init from a list of files
        elif list_files_ref:
            try:
                self._dict_files_ref = list_files_to_dict(
                    list_files=list_files_ref,
                )
                return
            except:
                self._dict_files_ref = dict()
                pass
        # Try to get the files directly from the general dictionary of files
        elif self._main_directory and list_subfolder_ref:
            try:
                self._dict_files_ref = {
                    k:v for k,v in self._dict_files.items() if any(list_subfolder_ref) in k
                }
                return
            except:
                self._dict_files_ref = dict()
                pass
        else:
            self._dict_files_ref = dict()
        
    def update_ponifile(self, ponifile_path=str()) -> None:
        """
            Get, update the ponifile path
        """

        if self._main_directory and ponifile_path:
            try:
                ponifile_path_full = check_subfolder(
                    main_directory=self._main_directory,
                    subfolder=ponifile_path
                )
                self._ponifile_path = ponifile_path_full
                return
            except:
                self._ponifile_path = ''
        else:
            self._ponifile_path = ''

    def update_transformQ(self) -> None:
        """
            If there is a ponifile, inherit the methods from Transform class (pygix module)
        """
        if self._ponifile_path:
            try:
                super().__init__()
                self.load(self._ponifile_path)
                self.set_incident_angle(
                    incident_angle=0.0,
                )
                self.set_sample_orientation(
                    sample_orientation=1,
                )
            except:
                pass
        else:
            pass

    def update_orientation(self, qz_parallel=True, qr_parallel=True) -> None:
        """
            Update three parameters to define the rotation of the detector and the orientation of the sample axis
        """
        # self._rotated = rotated
        self._qz_parallel = qz_parallel
        self._qr_parallel = qr_parallel
        try:
            self.set_sample_orientation(
                sample_orientation=DICT_SAMPLE_ORIENTATIONS[(self._qz_parallel, self._qr_parallel)]
            )
        except:
            pass

    ########################################
    ### Iterators and methods to select files or info from the integrator
    ########################################

    def file_iterator(self, list_files=[], reference=False) -> str():
        """
            Generates all the file inside a file list or within the self.dictionary
        """
        if list_files:
            for file in list_files:
                yield file
        else:
            if reference:
                for folder_ref, files in self._dict_files_ref.items():
                    for file_ref in files:
                        yield file_ref
            else:
                for folder, files in self._dict_files.items():
                    for file in files:
                        yield file

    def edf_iterator(self, list_files=list(), reference=False) -> EdfClass:
        """
            Generates an Edf instance for every file in list_files
        """
        for file in self.file_iterator(list_files=list_files, reference=reference):
            try:
                yield EdfClass(
                        filename=file,
                        dict_setup=self._dict_setup,
                        # rotated=self._rotated,
                        qz_parallel=self._qz_parallel,
                        qr_parallel=self._qr_parallel,
                )
            except:
                pass

    def integrations_iterator(self, list_integration=[]) -> dict:
        """
            Iterates over a list of dictionaries with the integration parameters
        """
        for item in list_integration:
            if isinstance(item, dict):
                yield item
            elif isinstance(item, str):
                try:
                    yield get_dict_integration(
                        name_integration=item,
                    )
                except:
                    yield None

    # def get_pandas_files(self, sorting_parameters=SORTED_PARAMETERS) -> pd.DataFrame:
    #     pandas_files = pd.DataFrame()
    #     for Edf in self.edf_iterator():
    #         pandas_files = pd.concat(
    #             [
    #                 pandas_files,
    #                 Edf.get_dataframe()
    #             ]
    #         )
    #     return pandas_files.sort_values(sorting_parameters)

    # def pandas_files_iterator(self) -> str:
    #     for file in self.get_pandas_files()['Fullname'].to_numpy().tolist():
    #         yield file

    def get_list_files(self) -> list:
        """
            Wrap all the files contained in the json and return a list
        """
        list_files = []
        for file in self.file_iterator():
            list_files.append(file)
        return list_files

    def Edf_random(self) -> EdfClass:
        """
            Return an Edf instance from a random file inside the dictionary of files
        """
        import random
        return EdfClass(
            filename=random.sample(
                self.get_list_files(), 1
            )[0],
            dict_setup=self._dict_setup,
            ponifile_path=self._ponifile_path,
            # rotated=self._rotated,
            qz_parallel=self._qz_parallel,
            qr_parallel=self._qr_parallel,
        )

    def get_Edf(self, filename) -> EdfClass:
        """
            Return an Edf instance from a filename (partial) inside the dictionary of files
        """
        for file in self.get_list_files():
            if filename in file:
                return EdfClass(
                    filename=file,
                    dict_setup=self._dict_setup,
                    ponifile_path=self._ponifile_path,
                    # rotated=self._rotated,
                    qz_parallel=self._qz_parallel,
                    qr_parallel=self._qr_parallel,
                )

    #################################################################################################################
    ### Batch and raw methods for integration
    #################################################################################################################

    def raw_integration_iterator(
        self, 
        list_files=[], 
        list_data=[], 
        list_integrations=[], 
        title=date_prefix(),
        x_label='x', 
        y_label='y', 
        dummy_integration=False, 
        remove_redundant_x=True, 
        sorted=True,
    ):
        """
            Yield a dataframe with the integration using raw_integration
        """
        df_unified = pd.DataFrame([])
        dict_unified = {}
        if list_data:
            index_integration = 0
            for data in list_data:
                data_cache = None
                for dict_integration in self.integrations_iterator(list_integration=list_integrations):
                    if dummy_integration:
                        yield None, data, dict_integration
                    else:
                        if not dict_integration:
                            return

                        try:
                            dataframe = self.raw_integration(
                                data=data,
                                dict_integration=dict_integration,
                                x_label=x_label,
                                y_label=y_label,
                            )
                        except:
                            continue

                        if not sorted:
                            yield dataframe, data, dict_integration, f"Data_{index_integration:03}"
                        else:
                            if data_cache is None:
                                # Initiate unified variables and change data_cache
                                data_cache = data
                                df_unified = dataframe
                                dict_unified = {key : [value] for key,value in dict_integration.items()}
                                continue
                            else:
                                # Check if the x-column is redundant
                                if remove_redundant_x:
                                    try:
                                        x_label = dict_integration[x_label]
                                    except:
                                        x_label = x_label
                                    if dataframe.iloc[:,0].equals(df_unified.loc[:,[x_label]].iloc[:,-1]):
                                        dataframe = dataframe.drop(columns=[x_label])
                                # Add the new DataFrame
                                try:
                                    df_unified = pd.concat(
                                        [df_unified, dataframe],
                                        axis=1
                                    )
                                    # Add the new dictionary
                                    for key, value in dict_integration.items():
                                        dict_unified[key].append(value)
                                except:
                                    pass

                yield df_unified, data, dict_unified, f"Data_{index_integration:03}_{title}"

        elif list_files:
            for Edf in self.edf_iterator(list_files=list_files):
                Edf_cache = None
                for dict_integration in self.integrations_iterator(list_integration=list_integrations):
                    if dummy_integration:
                        yield None, Edf, dict_integration
                    else:

                        # Update the Transform pygix instance with the incident and tilt angles
                        self.update_incident_tilt_angles(
                            Edf=Edf,
                        )

                        # Get the dataframe from pygix/pyFAI integration
                        dataframe = self.raw_integration(
                            data=Edf.get_data(),
                            dict_integration=dict_integration,
                            x_label=x_label,
                            y_label=y_label,
                        )

                        if not sorted:
                            yield dataframe, Edf, dict_integration, Edf.name
                        else:
                            if Edf_cache is None:
                                # Initiate unified variables and change Edf_cache
                                Edf_cache = Edf
                                df_unified = dataframe
                                dict_unified = {key : [value] for key,value in dict_integration.items()}
                                continue
                            elif Edf_cache:
                                # Check if the x-column is redundant
                                if remove_redundant_x:
                                    try:
                                        x_label = dict_integration[x_label]
                                    except:
                                        x_label = x_label
                                    if dataframe.iloc[:,0].equals(df_unified.loc[:,[x_label]].iloc[:,-1]):
                                        dataframe = dataframe.drop(columns=[x_label])
                                # Add the new DataFrame
                                df_unified = pd.concat(
                                    [df_unified, dataframe],
                                    axis=1
                                )
                                # Add the new dictionary
                                for key, value in dict_integration.items():
                                    dict_unified[key].append(value)
                                Edf_cache = Edf
                yield df_unified, Edf_cache, dict_unified, f"{Edf_cache.name}_{title}"
        else:
            return

    @random_message
    @timer
    @st_end_message(st_msg=f'Batch processing started.', end_msg=f'Batch processing is over.')
    def integration(
        self,
        list_files=[], 
        list_integrations=[],
        title=date_prefix(),
        sorted=False, 
        x_label='Unit',
        y_label='Suffix', 
        dummy_integration=False, 
        logging=True,
        print_progress_bar=True,
        ):
        """
            Perform a batch integration over a list of files with conditions
        """
        # Log file to register all the integrations
        if logging:
            create_folder(
                folder_name= join(self._main_directory, OUTPUT_FOLDER)
            )
            log_file = join(self._main_directory, OUTPUT_FOLDER, f"{LOGFILE_NAME}_{title}_{date_prefix()}.txt") if logging else ''
            save_log(log_file, 'Start batch integration', True)

        # Total number of steps
        if sorted:
            total_steps = len(list(self.edf_iterator(list_files)))
        else:
            total_steps = len(list(self.edf_iterator(list_files))) * len(list_integrations)

        # Iterate through all the edf files and dictionaries of integration
        for index, (dataframe, Edf, dict_integration, name) in enumerate(self.raw_integration_iterator(
            list_files=list_files, 
            list_integrations=list_integrations, 
            x_label=x_label,
            y_label=y_label,
            dummy_integration=dummy_integration,
            sorted=sorted,
            title=title,
            )):
            # Create folder or not
            create_folder(
                folder_name= join(Edf.folder, OUTPUT_FOLDER)
            )
            
            filename_out = join(Edf.folder, OUTPUT_FOLDER, f"{name}.dat")
            save_dat(
                dataframe=dataframe,
                header=dict_to_str(
                    dictionary={
                        'Name_output': filename_out,
                    } | Edf.get_dict() | dict_integration 
                ),
                filename_out=filename_out,
            )

            # Print for progress bar
            if print_progress_bar:
                end_mode = '\n' if (index+1) == total_steps else '\r'
                print(print_percent_done(index=index+1,total=total_steps), end=end_mode)
                
            # Logging the file
            if logging:
                input_line = f"Index: {index+1} / {len(list(self.edf_iterator(list_files)))}. Integrated file: {Edf.filename}. Integration: {dict_integration['Suffix']}"
                save_log(
                    log_name=log_file,
                    input_line=input_line,
                )
        if logging:
            save_log(log_file, 'Finished batch integration')

    # def get_dictionaries_integration(self) -> list:
    #     """
    #         Return a list with the dictionaries of all the available integrations
    #     """
    #     import json
    #     list_dicts = []
    #     for file in os.listdir(DIRECTORY_INTEGRATIONS):
    #         if file.endswith('json'):
    #             with open(join(DIRECTORY_INTEGRATIONS, file), 'r') as fp:
    #                 list_dicts.append(
    #                     json.load(fp)
    #                 )
    #     return list_dicts



    def update_incident_tilt_angles(self, Edf=EdfClass, filename=str()) -> None:
        """
            Updates the transform Q module with the incident and tilt angles from the Edf
        """
        if Edf:
            try:
                self.set_incident_angle(
                    incident_angle=Edf.incident_angle_edf,
                )
                self.set_tilt_angle(
                    tilt_angle=Edf.tilt_angle_edf,
                )
            except:
                self.set_incident_angle(
                    incident_angle=0.0,
                )
                self.set_tilt_angle(
                    tilt_angle=0.0,
                )
        elif filename and exists(filename):
            try:
                Edf = EdfClass(
                    filename=filename,
                    dict_setup=self._dict_setup,
                    # rotated=self._rotated,
                    qz_parallel=self._qz_parallel,
                    qr_parallel=self._qr_parallel,
                )
                self.set_incident_angle(
                    incident_angle=Edf.incident_angle_edf,
                )
                self.set_tilt_angle(
                    tilt_angle=Edf.tilt_angle_edf,
                )
            except:
                self.set_incident_angle(
                    incident_angle=0.0,
                )
                self.set_tilt_angle(
                    tilt_angle=0.0,
                )
        else:
            self.set_incident_angle(
                incident_angle=0.0,
            )
            self.set_tilt_angle(
                tilt_angle=0.0,
            )

    #################################################################################################################
    ### Methods for integration
    #################################################################################################################

    @try_or_continue('Check the dictionary of integration.')
    def raw_integration(
        self, 
        filename=str(), 
        data=None,
        dict_integration=dict(), 
        name_integration=str(), 
        x_label='x',
        y_label='y',
    ) -> pd.DataFrame:
        """
            Decide which integration is going to be performed: azimuthal (pyFAI), radial (pyFAI) or projection (self method)
        """
            
        # Get the data
        if filename:
            try:
                Edf = EdfClass(
                    filename=filename,
                    dict_setup=self._dict_setup,
                    # rotated=self._rotated,
                    qz_parallel=self._qz_parallel,
                    qr_parallel=self._qr_parallel,
                )
                # Take the data
                data = Edf.get_data()
                
                # Define the incident/tilt angles
                self.update_incident_tilt_angles(
                    Edf=Edf,
                )
            except:
                pass
        elif data is not None:
            data = data
        else:
            return

        # Get the dictionary with the integration parameters
        if dict_integration and isinstance(dict_integration, dict):
            dict_integration = dict_integration
        elif name_integration and isinstance(name_integration, str):
            dict_integration = self.get_dict_integration(
                name=name_integration,
            )
        else:
            return
    
        if dict_integration['Type'] == AZIMUTH_NAME:
            df = self.raw_integration_azimuthal(
                data=data,
                dict_integration=dict_integration,
                x_label=x_label,
                y_label=y_label,
            )

        elif dict_integration['Type'] == RADIAL_NAME:
            df = self.raw_integration_radial(
                data=data,
                dict_integration=dict_integration,
                x_label=x_label,
                y_label=y_label,
            )

        elif dict_integration['Type'] in (HORIZONTAL_NAME, VERTICAL_NAME):
            df = self.raw_integration_projection(
                filename=filename,
                data=data,
                dict_integration=dict_integration,
                x_label=x_label,
                y_label=y_label,
            )

        else:
            print(ERROR_RAW_INTEGRATION)
            df = None

        return df

    @try_or_continue('pyFAI: integrate1d, error with integration parameters?')
    def raw_integration_azimuthal(
        self, 
        filename=str(),
        data=None, 
        dict_integration=dict(), 
        name_integration=str(), 
        x_label='x', 
        y_label='y',
    ) -> pd.DataFrame:

        """
        Launch the azimuthal integration of PyFAI
        Returns a pandas dataframe
        """
        # Take the array of intensity
        if filename:
            try:
                Edf = EdfClass(
                    filename=filename,
                    dict_setup=self._dict_setup,
                    # rotated=self._rotated,
                    qz_parallel=self._qz_parallel,
                    qr_parallel=self._qr_parallel,
                )
                # Take the data
                data = Edf.get_data()
                
                # Define the incident/tilt angles
                self.update_incident_tilt_angles(
                    Edf=Edf,
                )
            except:
                pass
        elif data is not None:
            data=data
        else:
            return

        # Get the dictionary with the integration parameters
        dict_integration = get_dict_integration(
            dict_integration=dict_integration,
            name_integration=name_integration,
        )

        # Do the integration with pygix/pyFAI
        try:
            y_vector, x_vector = self.integrate_1d(
                process='sector',
                data=data,
                npt=self.calculate_bins(
                    radial_range=dict_integration['Radial_range'],
                    unit=dict_integration['Unit'],
                ),
                p0_range=dict_integration['Radial_range'],
                p1_range=dict_integration['Azimuth_range'],
                unit=dict_integration['Unit'],
                normalization_factor=None,
                polarization_factor=POLARIZATION_FACTOR,
                method='bbox',
            )
        except:
            return

        # Get labels for dataframe
        try:
            x_label = dict_integration[x_label]
        except:
            x_label = x_label
        try:
            y_label = dict_integration[y_label]
        except:
            y_label = y_label

        return pd.DataFrame(
            {
                x_label:x_vector,
                f'Int_{y_label}':y_vector,
            }
        )

    def raw_integration_radial(
        self, 
        filename=str(),
        data=None,
        dict_integration=dict(),
        name_integration=str(),
        x_label='x', 
        y_label='',
    ) -> pd.DataFrame:
        """
        Launch the radial integration of PyFAI
        Returns a pandas dataframe
        """
        # Take the array of intensity
        if filename:
            try:
                Edf = EdfClass(
                    filename=filename,
                    dict_setup=self._dict_setup,
                    # rotated=self._rotated,
                    qz_parallel=self._qz_parallel,
                    qr_parallel=self._qr_parallel,
                )
                # Take the data
                data = Edf.get_data()
                
                # Define the incident/tilt angles
                self.update_incident_tilt_angles(
                    Edf=Edf,
                )
            except:
                pass
        elif data is not None:
            data=data
        else:
            return

        # Get the dictionary with the integration parameters
        dict_integration = get_dict_integration(
            dict_integration=dict_integration,
            name_integration=name_integration,
        )

        # Do the integration with pygix/pyFAI
        try:
            y_vector, x_vector = self.integrate_1d(
                process='chi',
                data=data,
                npt=dict_integration['Bins_azimut'],
                p0_range=dict_integration['Azimuth_range'],
                p1_range=dict_integration['Radial_range'],
                unit=dict_integration['Unit'],
                normalization_factor=None,
                polarization_factor=POLARIZATION_FACTOR,
                method='bbox',
            )
        except:
            return

        # Get labels for dataframe
        try:
            x_label = dict_integration[x_label]
        except:
            x_label = x_label
        try:
            y_label = dict_integration[y_label]
        except:
            y_label = y_label
            
        return pd.DataFrame(
            {
                x_label:x_vector,
                f'Int_{y_label}':y_vector,
            }
        )

    def raw_integration_projection(
        self, 
        filename=str(),
        data=None, 
        dict_integration=dict(),
        name_integration=str(),
        x_label='x', 
        y_label='',
    ) -> pd.DataFrame:
        """
            Start the protocol for horizontal or vertical integration (projection)
        """
        # Take data and incident angle
        # Take the array of intensity
        if filename:
            try:
                Edf = EdfClass(
                    filename=filename,
                    dict_setup=self._dict_setup,
                    # rotated=self._rotated,
                    qz_parallel=self._qz_parallel,
                    qr_parallel=self._qr_parallel,
                )
                # Take the data
                data = Edf.get_data()
                
                # Define the incident/tilt angles
                self.update_incident_tilt_angles(
                    Edf=Edf,
                )
            except:
                pass
        elif data is not None:
            data=data
        else:
            return

        # Get the dictionary with the integration parameters
        dict_integration = get_dict_integration(
            dict_integration=dict_integration,
            name_integration=name_integration,
        )

        # Get the direction of the box
        process = DICT_BOX_ORIENTATION[dict_integration['Type']]
        try:
            if process == 'opbox':
                p0_range, p1_range = dict_integration['Oop_range'], dict_integration['Ip_range']
                npt = self.calculate_bins(
                    radial_range=dict_integration['Oop_range'],
                    unit=dict_integration['Unit_input'],
                )
            elif process == 'ipbox':
                p0_range, p1_range = dict_integration['Ip_range'], dict_integration['Oop_range']
                npt = self.calculate_bins(
                    radial_range=dict_integration['Ip_range'],
                    unit=dict_integration['Unit_input'],
                )
            else:
                return
        except:
            p0_range, p1_range, npt = None, None, NPT_RADIAL

        # Transform input units if necessary
        p0_range = [self.get_q_nm(
            value=position,
            input_unit=dict_integration['Unit_input']
        ) for position in p0_range]

        p1_range = [self.get_q_nm(
            value=position,
            input_unit=dict_integration['Unit_input']
        ) for position in p1_range]

        try:
            y_vector, x_vector = self.integrate_1d(
                process=process,
                data=data,
                npt=npt,
                p0_range=p0_range,
                p1_range=p1_range,
                unit=dict_integration['Unit'],
                normalization_factor=None,
                polarization_factor=POLARIZATION_FACTOR,
                method='bbox',
            )
        except:
            return

        # Get labels for dataframe
        try:
            x_label = dict_integration[x_label]
        except:
            x_label = x_label
        try:
            y_label = dict_integration[y_label]
        except:
            y_label = y_label
            
        return pd.DataFrame(
            {
                x_label:x_vector,
                f'Int_{y_label}':y_vector,
            }
        )

    ########################
    ### Subtraction methods
    ########################

    def search_reference_file(self, Edf):
        """
            Return a Edf instance of the proper file for subtraction, if not return None
        """
        # Search reference file in cache
        Edf_ref = self.search_reference_from_cache(Edf)

        # If not, search in the json dictionary for references
        if Edf_ref:
            return Edf_ref
        else:
            Edf_ref = self.search_reference_from_json(Edf)

        if Edf_ref:
            return Edf_ref
        else:
            return None

    # def scalar_subtraction_meanvalue(self, Edf_sample, Edf_reference, escalar_range=SCALAR_RANGE):
    #     """
    #         Return the escalar to get a subtracted image
    #     """

    #     for ind, escalar in enumerate(escalar_range):
    #         data_sub = Edf_sample.get_data() - escalar * Edf_reference.get_data()
    #         if self.average_negative_values(data_sub) > np.average(data_sub)*SUBTRACT_VALUE:
    #             return escalar_range[ind]
    #         else:
    #             pass
    #     return 0.0

    def scalar_subtraction(self, Edf_sample, Edf_reference, method='Photo'):
        """
            Calls a method to obtain the scalar number for subtraction
        """
        if Edf_reference:
            pass
        else:
            Edf_reference = self.search_reference_file(Edf=Edf_sample)

        if method == 'Photo':
            return self.scalar_subtraction_photovalue(
                Edf_sample=Edf_sample,
                Edf_reference=Edf_reference
            )
        else:
            return self.scalar_subtraction_meanvalue(
                Edf_sample=Edf_sample,
                Edf_reference=Edf_reference,
            )

    def get_subtracted_data(self, Edf_sample, method=DEFAULT_METHOD_SUBTRACTION):
        """
            Return the numpy array already subtracted based on located reference files and method
        """
        Edf_reference = self.search_reference_file(Edf=Edf_sample)

        if Edf_reference:
            if method == 'Photo':
                scalar = self.scalar_subtraction_photovalue(
                    Edf_sample=Edf_sample,
                    Edf_reference=Edf_reference,
                )
            else:
                scalar = self.scalar_subtraction_meanvalue(
                    Edf_sample=Edf_sample,
                    Edf_reference=Edf_reference,
                    escalar_range=SCALAR_RANGE,
                )

            Edf_sample.dict_edf['Reference file'] = Edf_reference.filename
            Edf_sample.dict_edf['Reference scalar'] = scalar

            return Edf_sample.get_data() - scalar * Edf_reference.get_data()
        else:
            return Edf_sample.get_data()
   
    # def average_negative_values(self, data):
    #     return abs(np.average([k for k in data.ravel() if k <= 0]) )

    def search_reference_from_cache(self, Edf):
        """
            Take the reference from file if saved before in cache
        """
        if self.edf_cache:
            for edf_cache in self.edf_cache:
                if Edf.exposure == edf_cache.exposure:
                    return edf_cache
                else:
                    pass
            return None
        else:
            return None

    def search_reference_from_json(self, Edf):
        """
            Search for a proper ref. file in the json dictionary
        """
        for ref_file in self.edf_iterator(reference=True):
            Edf_ref = EdfClass(
                filename=ref_file,
                dict_setup=self._dict_setup,
            )
            if Edf.exposure == Edf_ref.exposure:
                self.edf_cache.append(Edf_ref)
                return Edf_ref
            else:
                pass
        return None

    def update_avg_parameters(self, current_parameters={}, new_parameters={}):
        for key, value in new_parameters.items():
            if isinstance(value, str) and value == current_parameters[key]:
                pass
            elif isinstance(value, float) and value < current_parameters[key]*1.01:
                pass
            else:
                return True
        return False

    #########################
    ### Save methods
    #########################

    def plot_Qmap(self, filename, subtraction=False, xlims=[0,20], ylims=[0,20], vmin=0, vmax=10):
        Edf = self.search_edf(filename)

        if subtraction:
            data = self.get_data_subtracted(Edf)
        else:
            data = Edf.get_data()

        data, QR, QZ = self.mesh_qrqz(
            spitch=Edf.incident_angle,
            data=data,
        )
        
        self.plot_qcolormesh(
            data=data,
            x_grid=QR,
            y_grid=QZ,
            xlims=xlims,
            ylims=ylims,
            vmin=vmin,
            vmax=vmax,
        )
        
    def plot_qcolormesh(self, data, x_grid, y_grid, xlims=[0,20], ylims=[0,20], vmin=0, vmax=10):
        plt.figure(figsize=(10,10), dpi=100)
        # plt.rc('axes', titlesize=30) 
        plt.pcolormesh(x_grid, y_grid, data, cmap='viridis', vmin=vmin, vmax=vmax)
        plt.xlim(xlims)
        plt.ylim(ylims)
        plt.xlabel(r'$q_{r}$ $(nm^{-1})$', fontsize=30)
        plt.ylabel(r'$q_{z}$ $(nm^{-1})$', fontsize=30)
        plt.xticks(ticks=[0,5,10,15,20], fontsize=20)
        plt.yticks(ticks=[0,5,10,15,20], fontsize=20)
        plt.gca().set_aspect('equal')
        plt.colorbar()
        plt.plot()

    def save_plot(self, grid_x, grid_y, data, fileout, title, xlims=[0,20], ylims=[0,20], vmin=0, vmax=10):
        # plt.rcParams['font.size'] = FONT_SIZE
        plt.figure(figsize=(10,10), dpi=100)
        plt.pcolormesh(grid_x, grid_y, data, cmap='viridis', vmin=vmin, vmax=vmax)
        plt.xlim(xlims)
        plt.ylim(ylims)
        plt.xlabel(LABEL_X, fontsize=FONT_SIZE_LABELS)
        plt.ylabel(LABEL_Y, fontsize=FONT_SIZE_LABELS)
        plt.xticks(TICKS_X, fontsize=FONT_SIZE_TICKS)
        plt.yticks(TICKS_Y, fontsize=FONT_SIZE_TICKS)
        plt.title(title, fontsize=FONT_SIZE_TITLE)
        plt.gca().set_aspect('equal')
        if COLORBAR:
            plt.colorbar()
        plt.savefig(fileout)
        plt.close()

    # Plot a random pattern
    @clear_plt
    def image_random(self, subtraction=False, log=False, weak_lims=True):
        Edf_random = self.Edf_random()
        plot_image(Edf_data=Edf_random.get_data(), log=log, weak_lims=weak_lims)

    # Show a random or specific pattern only with the values to be integrated in dict_parameters
    def check_parameters(self, edf_file='', dict_parameters={}, log=False, weak_lims=True):
        if edf_file:
            # Take a specific Edf class
            Edf = self.search_edf(edf_file=edf_file)
        else:
            # Take a random Edf class
            Edf = self.Edf_random()

        # Generate a new numpy array with only the requested values
        new_Edfdata = self.new_Edfdata(Edf=Edf, dict_parameters=dict_parameters)

        # Call to create an overlap of two arrays
        plot_images_overlap(edf1_data=Edf.get_data(), edf2_data=new_Edfdata, log=log, weak_lims=weak_lims)
    
    def check_integration(self, Edf=None, dict_integration=dict()):
        """
            Overlap the integration map on the ploted graph
        """
        if not Edf:
            Edf = self.Edf_random()

        self.plot_images_overlap(
            edf1_data=Edf.get_data(),
            edf2_data=self.new_Edfdata(
                Edf=Edf,
                dict_parameters=dict_integration,
            ),
        )

    def plot_images_overlap(self, edf1_data, edf2_data, title='', log=False, weak_lims=True):
        edf1_data = np_log(edf1_data, log)
        edf2_data = np_log(edf2_data, log)

        plt.figure(
            frameon=False, 
            figsize=(5,5), 
            # dpi=10,
        )

        im1 = plt.imshow(
            edf1_data, 
            cmap=plt.cm.gray, 
            interpolation='nearest',
        )

        plt.clim(
            np_weak_lims(
                edf1_data, 
                weak_lims,
            )
        )

        im2 = plt.imshow(
            edf2_data, 
            cmap=plt.cm.viridis, 
            alpha=0.9, 
            interpolation='bilinear',
        )

        plt.clim(
            np_weak_lims(
                edf2_data, 
                weak_lims
            )
        )
        
        plt.title(title)
        plt.show()

    # Input part of the edf filename and returns the full filename in the json
    def search_edf(self, edf_file, return_class=True):
        for full_edf_file in self.edf_iterator():
            if edf_file in full_edf_file:
                # If you want the instance already built
                if return_class:
                    return EdfClass(
                        filename=full_edf_file,
                        dict_setup=self._dict_setup,
                    )
                else:
                    # If not, just return the strings: filename and folder name
                    return full_edf_file
            else:
                pass
        
            ('No Edf was found in the json database. Try to change the name.')

    def new_Edfdata(self, Edf, dict_parameters):
        if dict_parameters['Type'] in (AZIMUTH_NAME, RADIAL_NAME):
            return self.new_Edfdata_cake(Edf=Edf, dict_parameters=dict_parameters)
        elif dict_parameters['Type'] in (HORIZONTAL_NAME, VERTICAL_NAME):
            return self.new_Edfdata_projection(Edf=Edf, dict_integration=dict_parameters)

    def new_Edfdata_cake(self, Edf, dict_parameters) -> np.array:
        """
            Return an intensity array only with the values within the integration parameters
        """
        # Create new list
        new_list = []

        # Azimuth to radians
        azimuth_range = np.radians(dict_parameters['Azimuth_range'])
        
        # Iterate through all numpy array
        for ind1,row in enumerate(Edf.get_data()):
            for ind2,num in enumerate(row):
                cond1 = dict_parameters['Radial_range'][0] < self.calibrant.qArray()[ind1,ind2] < dict_parameters['Radial_range'][1]
                cond2 = azimuth_range[0] < self.calibrant.chiArray()[ind1,ind2] < azimuth_range[1]
                if (cond1 and cond2):
                    new_list.append(num)
                else:
                    new_list.append(np.nan)

        return np.array(new_list).reshape(np.shape(Edf.get_data()))

    def new_Edfdata_projection(self, Edf=None, dict_integration=dict()):
        """
            Return an array modified according to parameters of integration (projection)
        """
        # Get the limits to cut the matrix
        projection_limits = self.get_projection_limits(
            dict_integration=dict_integration,
            incident_angle=Edf.incident_angle_edf,
        )

        type_cut = dict_integration['Type']

        # if (dict_integration['Type'] == HORIZONTAL_NAME and self.rotated) or (dict_integration['Type'] == VERTICAL_NAME and not self.rotated):
        #     type_cut = VERTICAL_NAME
        # elif (dict_integration['Type'] == VERTICAL_NAME and self.rotated) or (dict_integration['Type'] == HORIZONTAL_NAME and not self.rotated):
        #     type_cut = HORIZONTAL_NAME
        # else:
        #     return

        data = Edf.get_data()
        if type_cut == HORIZONTAL_NAME:
            data[0:min(projection_limits)] = np.nan
            data[max(projection_limits)::] = np.nan
        elif type_cut == VERTICAL_NAME:
            data[:, 0:min(projection_limits)] = np.nan
            data[:, max(projection_limits)::] = np.nan
        return data

    def q_to_twotheta(self, q, unit='q_nm^-1', degree=False) -> float:
        """
        Transform from q to 2theta (rad)
        """
        if unit == 'q_nm^-1':
            twotheta = 2 * np.arcsin((q*self._wavelength * 1e9)/(4*np.pi))
        elif unit == 'q_A^-1':
            twotheta = 2 * np.arcsin((q*self._wavelength * 1e10)/(4*np.pi))
        else:
            return
        return np.rad2deg(twotheta) if degree else twotheta

    def twotheta_to_q(self, twotheta=0.0, deg=True) -> float:
        """
            Returns the q(nm-1) from the 2theta value
        """
        if deg:
            return 4*np.pi / self._wavelength * np.sin(np.radians(twotheta) / 2) / 1e9
        else:
            return 4*np.pi / self._wavelength * np.sin(twotheta / 2) / 1e9

    def calculate_bins(self,radial_range=[], unit='q_nm^-1') -> int:
        """
        Calculate the bins between two q values
        """
        if unit in ('q_nm^-1' or 'q_A^-1'):
            twotheta1 = self.q_to_twotheta(
                q=radial_range[0],
                unit=unit,
            )

            twotheta2 = self.q_to_twotheta(
                q=radial_range[1],
                unit=unit,
            )
        elif unit == '2th_deg':
            twotheta1, twotheta2 = np.radians(radial_range[0]), np.radians(radial_range[1])
        elif unit == '2th_rad':
            twotheta1, twotheta2 = radial_range[0], radial_range[1]
        else:
            return

        return int(round(self._dist / self.get_pixel1() * (np.tan(twotheta2) - np.tan(twotheta1))))

    def get_q_nm(self, value=0.0, input_unit='q_nm^-1') -> float:
        """
            Return a q(nm-1) value from another unit
        """
        if input_unit == 'q_nm^-1':
            return value
        elif input_unit == 'q_A^-1':
            return value * 10
        elif input_unit == '2th_deg':
            return self.twotheta_to_q(twotheta=value, deg=True)
        elif input_unit == '2th_rad':
            return self.twotheta_to_q(twotheta=value, deg=False)
        else:
            return None
        
def loadjson (json_file) -> Integrator:
    """Import a json file with all the set-up information"""

    # Check if the json file exist
    assert exists(json_file), "No json file was detected."

    # Load the json file and return an instance of class Setup
    with open(json_file) as jf:
        from .integrator import Integrator
        return Integrator(dict_info=json.load(jf))