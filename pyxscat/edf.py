from datetime import datetime
from setup.setup_methods import get_dict_setup
from os.path import basename, dirname, exists, getctime, splitext
from other_functions import np_weak_lims
from plots import plot_mesh, plot_image
from pygix.transform import Transform
from units import *
import fabio
import numpy as np
import warnings
warnings.filterwarnings("ignore")

PATH_EDF = dirname(__file__)

#########
# Message errors
########
ERROR_NEMONIC_MSG = "Careful, there is no full correspondence between nemonic and position keys"
ERROR_FILENAME = "The filename does not exists. Check path."
ERROR_BEAMLINE = "No beamline detected. Check the name of the attribute."
ERROR_SETUP_ENCAPSULATION = "The input instance is not an instance of Setup."
ERROR_SETUP_CREATION = "The setup instance could not be created. Check the ponifile path."
NO_SETUP_INFORMATION = "Edf instance was created without any setup information."

########
## DEFAULT AND UNACCEPTABLE VALUES
#######
NORMALIZATION_UNACCEPTABLE_VALUES = [0.0]
RETURN_ERROR_GENERIC = None
RETURN_ERROR_NORMALIZATION = 1.0
RETURN_ERROR_INCIDENT_ANGLE = 0.0
RETURN_ERROR_TILT_ANGLE = 0.0
RETURN_ERROR_EXPOSITION_TIME = 1.0
RETURN_ERROR_MOTOR_X = 0.0

DICT_SAMPLE_ORIENTATIONS = {
    (True,True) : 1,
    (True,False) : 2,
    (False,True) : 3,
    (False,False) : 4,
}

######
## POS-MNE NAMES
#####
MNE_NAME = ['mne']
POS_NAME = ['pos']

class EdfClass(Transform):
    
    def __init__(
        self,
        filename=str(),
        name_setup=str(),
        dict_setup=dict(),
        transform_q=None,
        ponifile_path=str(),
        qz_parallel=True,
        qr_parallel=True,
    ):
        """
            Initialize variables associated with the .edf file itself
        """
        # Filename must exist
        assert exists(filename), ERROR_FILENAME

        # Update the main name attributes
        self.update_names(
            filename=filename,
        )


        # Update the dictionary with setup information
        self._dict_setup = get_dict_setup(
            dict_setup=dict_setup,
            name_setup=name_setup
        )

        # Get timestamps
        self.epoch = getctime(self.filename)
        self.date = datetime.fromtimestamp(self.epoch).strftime('%Y-%m-%d %H:%M:%S')

        # Update Transform instance from pygix-pyFAI modules
        self.update_q_properties(
            transform_q=transform_q,
            ponifile_path=ponifile_path,
        )

        # Update orientation attributes
        self.update_orientations(
            # rotated=rotated,
            qz_parallel=qz_parallel,
            qr_parallel=qr_parallel,
        )
        self._transform_q = transform_q


    def update_names(self, filename=str()) -> None:
        """
            Init the main name attributes
        """
        try:
            self.filename = filename
            self.folder = dirname(filename)
            self.basename = basename(self.filename)
            self.name = splitext(self.basename)[0]
        except:
            return


    def update_q_properties(self, transform_q=None, ponifile_path=str()) -> None:
        """
            Take instance or inherit methods from Transform class from pygix package
        """

        # Upload an instance of transform_q
        if transform_q and isinstance(transform_q, Transform):
            try:
                self._transform_q = transform_q
                self.tranform_bool = True
                return
            except:
                self._transform_q = None
                self.tranform_bool = False
                pass

        # Most likely option, inherit from Transform using ponifile_path
        elif ponifile_path:
            try:
                self.update_ponifile(
                    ponifile_path=ponifile_path,
                )
                if self._ponifile_path:
                    super().load(self._ponifile_path)
                    self.useqx = True
                    self.tranform_bool = True

                    # Define the incident angle
                    try:
                        self.set_incident_angle(
                            incident_angle=self.incident_angle_edf,
                        )
                    except:
                        self.set_default_incident_angle()

                    # Define the tilting angle
                    try:
                        self.set_tilt_angle(
                            tilt_angle=self.tilt_angle_edf,
                        )
                    except:
                        self.set_default_tilt_angle()                   
                else:
                    self.set_default_incident_angle()
                    self.set_default_tilt_angle()

                # Define the sample orientation
                try:
                    self.set_sample_orientation(
                        sample_orientation=DICT_SAMPLE_ORIENTATIONS[(self._qz_parallel, self._qr_parallel)],
                    )
                except:
                    self.set_sample_orientation(
                        sample_orientation=DICT_SAMPLE_ORIENTATIONS[(True, True)],
                    )
   
            except:
                self.tranform_bool = False
                pass
        else:
            self.tranform_bool = False
            pass

    def set_default_incident_angle(self) -> None:
        """
            Set incident angle to 0.0
        """
        if self.tranform_bool:
            try:
                self.set_incident_angle(
                incident_angle=0.0,
            )
            except:
                pass
        else:
            return

    def set_default_tilt_angle(self) -> None:
        """
            Set tilt angle to 0.0
        """
        if self.tranform_bool:
            try:
                self.set_tilt_angle(
                incident_angle=0.0,
            )
            except:
                pass
        else:
            return


    def update_orientations(self, qz_parallel=True, qr_parallel=True) -> None:
        """
            Update the three parameters of orientations
            IMPORTANT: change PONI1, PONI2 AND SHAPE upon rotated bool
        """
        self._qz_parallel = qz_parallel
        self._qr_parallel = qr_parallel
        if self.tranform_bool:
            try:
                self.set_sample_orientation(
                    sample_orientation=self.sample_orientation_edf
                )
            except:
                pass
        else:
            pass

    def update_ponifile(self, ponifile_path=str()) -> None:
        """
            Get, update the ponifile path
        """
        if ponifile_path:
            try:
                if exists(ponifile_path):
                    self._ponifile_path = ponifile_path
                return
            except:
                self._ponifile_path = ''
        else:
            self._ponifile_path = ''

    def set_qz_parallel(self, qz_parallel=True) -> None:
        """
            Set the direction of qz axis positive
        """
        self._qz_parallel = qz_parallel

    def set_qr_parallel(self, qr_parallel=True) -> None:
        """
            Set the direction of qr axis positive
        """
        self._qr_parallel = qr_parallel

    @property
    def sample_orientation_edf(self) -> None:
        """
            Returns an int between 1 and 4, according to both qz and qr parallel
        """
        return DICT_SAMPLE_ORIENTATIONS[(self._qz_parallel, self._qr_parallel)]

    def get_data(self, normalized=True) -> np.array:
        """
            Return the numpy array of data opened with Fabio, already normalized or not
        """
        try:
            if normalized:
                return np.divide(fabio.open(self.filename).data.astype(np.int32), self.normfactor)
            else:
                return fabio.open(self.filename).data.astype(np.int32)
        except:
            return None

    def get_detector_array(self) -> np.array:
        """
            Return an array with detector shape and rotated, according to self._rotated
        """
        # shape = self.get_shape()
        # if self._rotated:
        #     shape = [shape[1], shape[0]]
        try:
            shape = self.get_shape()
            d2,d1 = np.meshgrid(
                np.linspace(1,shape[1],shape[1]),
                np.linspace(1,shape[0],shape[0]),
            )

            out = np.array([d1,d2])
            return out
        except:
            return None

    def plot_data(self, log=False, weak_lims=True) -> None:
        """
            Plot the pixel map
        """
        try:
            plot_image(
                data=self.get_data(),
                log=log,
                weak_lims=weak_lims,
            )
        except:
            pass

    def get_mesh_matrix(self, unit='q_nm^-1', data=None):
        """
            Return both horizontal and vertical mesh matrix, ready to plot, returns also the corrected data without the missing wedge
        """
        if self.tranform_bool:
            unit = get_pyfai_unit(unit)
            det_array = self.get_detector_array()

            if unit in UNITS_Q:
                # scat_z, scat_x = qz, qxy
                if self._transform_q:
                    try:
                        scat_z, scat_x = self._transform_q.calc_q(
                            d1=det_array[0,:,:],
                            d2=det_array[1,:,:],
                        )
                    except:
                        scat_z, scat_x = None, None
                else:
                    try:
                        scat_z, scat_x = self.calc_q(
                            d1=det_array[0,:,:],
                            d2=det_array[1,:,:],
                        )
                    except:
                        scat_z, scat_x = None, None

            elif unit in UNITS_THETA:
                # scat_z, scat_x = alpha, tth
                if self._transform_q:
                    try:
                        scat_z, scat_x = self._transform_q.calc_angles(
                            d1=det_array[0,:,:],
                            d2=det_array[1,:,:],
                        )
                    except:
                        scat_z, scat_x = None, None
                else:
                    try:
                        scat_z, scat_x = self.calc_angles(
                            d1=det_array[0,:,:],
                            d2=det_array[1,:,:],
                        )
                    except:
                        scat_z, scat_x = None, None
            else:
                scat_z, scat_x = None, None
            
            # Transform units
            if (scat_z is not None) and (scat_x is not None):
                DICT_PLOT = DICT_UNIT_PLOTS.get(unit, DICT_PLOT_DEFAULT)
                scat_z *= DICT_PLOT['SCALE']
                scat_x *= DICT_PLOT['SCALE']

                if data is None:
                    data = self.get_data()

                if unit in UNITS_Q:
                    ind = np.unravel_index(np.argmin(abs(scat_x), axis=None), scat_z.shape)
                    if self.sample_orientation_edf in (1,3):
                        data[:, ind[1] - 2: ind[1] + 2] = np.nan
                    elif self.sample_orientation_edf in (2,4):
                        data[ind[0] - 2: ind[0] + 2, :] = np.nan

            return scat_x, scat_z, data

    def plot_Qmesh(self, data=None, unit='q_nm^-1', auto_lims=True, **kwargs) -> None:
        """
            Plot the Q map only if the EdfClass instance contains a Geometry instance (with ponifile information)
        """
        unit = get_pyfai_unit(unit)
        if self.tranform_bool:
            scat_x, scat_z, data = self.get_mesh_matrix(unit=unit)
            plot_mesh(
                mesh_horz=scat_x,
                mesh_vert=scat_z,
                data=data,
                unit=unit,
                auto_lims=auto_lims,
                **kwargs,
            )
        else:
            return

    def get_header(self, search_nmemonics=True, to_float=True) -> dict:
        """
            Return the header read with Fabio and modified if necessary
        """

        # First, take the original header using fabio
        try:
            header = dict(fabio.open(self.filename).header)
        except:
            return

        # Include folder and filename in the header
        header['Folder'] = self.folder
        header['Filename'] = self.basename

        # Check for nemonic values (list/strings inside keys)
        if search_nmemonics:
            nemonic_keys = self.search_keys_in_header(header, MNE_NAME)
            position_keys = self.search_keys_in_header(header, POS_NAME)

            if nemonic_keys:
                header = self.get_header_with_nmemonics(header, nemonic_keys, position_keys, remove=True)
        else:
            pass

        # Convert the values to float if possible
        if to_float:
            for key, value in header.items():
                try:
                    header[key] = float(value)
                except:
                    pass
        else:
            pass

        return header

    def search_keys_in_header(self, header={}, key_list=[]) -> list:
        """
            Returns a list with the keys of the header that matches some string in key_list
        """
        return [k for k in header.keys() if any(name in k for name in key_list)]

    def get_header_with_nmemonics(self, header={}, nemonic_keys=[], position_keys=[], remove=True) -> dict:
        """
            Returns a dictionary with the values inside nemonic counters
        """
        # Get the dictionary with the extracted values and keys
        header_nmenomics = self.header_extract_nemonics(header, nemonic_keys, position_keys)

        # Add the new dictionary to the original one
        header = {**header, **header_nmenomics}

        # Remove the nemonic items
        if remove:
            for nme_key, pos_key in zip(nemonic_keys, position_keys):
                del header[nme_key]
                del header[pos_key]
        else:
            pass

        return header

    def header_extract_nemonics(self, header={}, nemonic_keys=[], position_keys=[]) -> dict:
        """
            Returns a dictionary with the extracted nemonic counters
        """
        assert len(nemonic_keys) == len(position_keys), ERROR_NEMONIC_MSG

        new_dict = {}

        for nm_key, pos_key in zip(nemonic_keys, position_keys):
            for nm_key_name, pos_key_value in zip(header[nm_key].split(' '), header[pos_key].split(' ')):
                try:
                    new_dict[nm_key_name] = float(pos_key_value)
                except:
                    new_dict[nm_key_name] = str(pos_key_value)

        return new_dict

    def get_value_header(self, keys=[], unacceptable_values=[], return_error=RETURN_ERROR_GENERIC) -> float:
        """
            Search inside the self.header for a the value of a key that matches, if not, return a value
        """
        if isinstance(keys, str):
            keys = [keys]

        for key in keys:
            if '*' in key:
                # It is a product of keys
                return np.product([self.get_header()[item]] for item in key.split('*'))

            elif '/' in key:
                list_keys = key.split('/')
                # It is a relation between two keys
                return np.divide(self.get_header()[list_keys[0]], self.get_header()[list_keys[1]])

            else:
                try:
                    if self.get_header()[key] in unacceptable_values:
                        pass
                    else:
                        return self.get_header()[key]
                except:
                    pass
        return return_error

    def get_dict(self) -> dict:
        """
            Return a dictionary with information of edf file
        """
        return {'Date':self.date,
                'Epoch':self.epoch,
                'Folder': self.folder,
                'Filename':self.basename,
                'Fullname':self.filename,
                'Monitor':self.normfactor,
                'Exposition':self.exposure,
                'Pitch':self.incident_angle_edf,
                'Tilt':self.tilt_angle_edf,
        }

    # def get_dataframe(self) -> DataFrame:
    #     """
    #         Returns a pandas dataframe with the information from the edf file
    #     """
    #     return DataFrame.from_dict({key:[value] for (key,value) in self.get_dict().items()})

    @property
    def normfactor(self):
        """
            Return the normalization factor, depends on the beamline
        """        
        try:
            return self.get_value_header(keys=self._dict_setup['Norm'], 
                                        unacceptable_values=NORMALIZATION_UNACCEPTABLE_VALUES, 
                                        return_error=RETURN_ERROR_NORMALIZATION)

        except:
            return RETURN_ERROR_NORMALIZATION

    @property
    def incident_angle_edf(self):
        """
            Return the incident angle of the beam, depends on the beamline
        """
        try:
            return self.get_value_header(keys=self._dict_setup['Angle'], return_error=RETURN_ERROR_INCIDENT_ANGLE)
        except:
            return RETURN_ERROR_INCIDENT_ANGLE

    @property
    def tilt_angle_edf(self):
        """
            Return the tilt angle of the sample, called chi angle, roll, etc
        """
        try:
            return self.get_value_header(keys=self._dict_setup['Tilt angle'], return_error=RETURN_ERROR_TILT_ANGLE)
        except:
            return RETURN_ERROR_INCIDENT_ANGLE

    @property
    def exposure(self):
        """
            Return the exposition time, depends on the beamline
        """
        try:
            return self.get_value_header(keys=self._dict_setup['Exposure'], return_error=RETURN_ERROR_EXPOSITION_TIME)
        except:
            return RETURN_ERROR_EXPOSITION_TIME

    def sum_data(self, roi=[], name='roi1'):
        """
            Return the integration inside a region of interest, if no roi, full data
        """
        return np.sum(self.roi(roi))
        
    def max_data(self, roi=[], name='roi1'):
        """
            Returns the maximum value of intensity inside a region of interest, if no roi, full data
        """
        return np.amax(self.roi(roi))

    def average_data(self, roi=[], name='roi1'):
        """
            Returns the average data inside a region of interest, if no roi, full data
        """
        return np.average(self.roi(roi))

    def weak_lims(self, roi=[]):
        """
            Returns a list of two values with the weak limits of data or roi
        """
        return np_weak_lims(data=self.roi(roi))

    def roi(self, roi=[]):
        """
            Returns a numpy array, which is the region of interest of the full edf data
        """
        if roi:
            return self.get_data()[roi[0]:roi[1],roi[2]:roi[3]]
        else:
            return self.get_data()