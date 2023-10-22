
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
from pyFAI.io.ponifile import PoniFile
from pygix.transform import Transform
from pygix.grazing_units import TTH_DEG, TTH_RAD, Q_A, Q_NM
from pyxscat.other.integrator_methods import *
from pyxscat.other.setup_methods import *
from pathlib import Path
from pyxscat.other.units import *


import numpy as np
import pandas as pd

from pyxscat.logger_config import setup_logger
logger = setup_logger()

PONI_KEY_VERSION = "poni_version"
PONI_KEY_BINNING = "binning"
PONI_KEY_DISTANCE = "dist"
PONI_KEY_WAVELENGTH = "wavelength"
PONI_KEY_SHAPE1 = "shape1"
PONI_KEY_SHAPE2 = "shape2"
PONI_KEY_DETECTOR = "detector"
PONI_KEY_DETECTOR_CONFIG = "detector_config"
PONI_KEY_PIXEL1 = "pixelsize1"
PONI_KEY_PIXEL2 = "pixelsize2"
PONI_KEY_PONI1 = "poni1"
PONI_KEY_PONI2 = "poni2"
PONI_KEY_ROT1 = "rot1"
PONI_KEY_ROT2 = "rot2"
PONI_KEY_ROT3 = "rot3"

DICT_BOX_ORIENTATION = {
    'horizontal' : 'ipbox',
    'vertical' : 'opbox',
}

AZIMUTH_NAME = 'azimuthal'
RADIAL_NAME = 'radial'
HORIZONTAL_NAME = 'horizontal'
VERTICAL_NAME = 'vertical'

DICT_SAMPLE_ORIENTATIONS = {
    (True,True) : 1,
    (True,False) : 2,
    (False,True) : 3,
    (False,False) : 4,
}

UNIT_GI = {
    'q_nm^-1' : Q_NM,
    'q_A^-1' : Q_A,
    '2th_deg' : TTH_DEG,
    '2th_rad' : TTH_RAD,
}

POLARIZATION_FACTOR = 0.99
NPT_RADIAL = int(100)

ERROR_RAW_INTEGRATION = "Failed at detect integration type."

def logger_info(func):
    def wrapper(*args, **kwargs):
        logger.info(f'We entered into function: {func.__name__}')
        return func(*args, **kwargs)
    return wrapper

class GIIntegrator(Transform):

    def __init__(self) -> None:
        super().__init__()
        self.init_transform()
        self.init_ai()
        self.active_ponifile=''
        self._poni_instance = None

    
    def init_transform(self, incident_angle=0.0, tilt_angle=0.0):
        self.set_incident_angle(
            incident_angle=incident_angle,
        )
        self.set_tilt_angle(
            tilt_angle=tilt_angle,
        )
    
    def init_ai(self):
        self._ai = AzimuthalIntegrator()

    def update_poni(self, poni=None, ponifile='', dict_poni={}):        
        if poni:
            poni = poni

        elif ponifile:
            try:
                poni = PoniFile(data=ponifile)
            except Exception as e:
                logger.error(f'{e}: {ponifile} is not a valid .poni filename.')
                self._poni = None
                return

        elif dict_poni:
            try:
                poni = PoniFile(data=dict_poni)
            except Exception as e:
                logger.error(f'{e}: {dict_poni} is not a valid poni dictionary')
                self._poni = None
                return

        try:
            self._init_from_poni(poni=poni)
            self._ai._init_from_poni(poni=poni)
            self._poni = poni
            logger.info(f'Poni updated: {self._poni}.')
        except Exception as e:
            logger.error(f'{e}: Poni could not be updated: {self._poni}.')
            self._poni = None

    # @logger_info
    # def get_poni_dict(self):
    #     try:
    #         detector = self._transform.detector
    #     except Exception as e:
    #         logger.error(f"{e}: Detector could not be retrieved.")
    #         return
    #     try:
    #         detector_config = self._transform.detector.get_config()
    #     except Exception as e:
    #         logger.error(f"{e}: Detector could not be retrieved.")
    #         return
    #     try:
    #         wave = self._transform._wavelength
    #     except Exception as e:
    #         logger.error(f"{e}: Wavelength could not be retrieved.")
    #         return
    #     try:
    #         dist = self._transform._dist
    #     except Exception as e:
    #         logger.error(f"{e}: Distance could not be retrieved.")
    #         return
        
    #     # Pixel 1
    #     try:
    #         pixel1 = self._transform.pixel1
    #     except Exception as e:
    #         pixel1 = None
    #         logger.error(f"{e}: Pixel 1 could not be retrieved.")
    #         return
    #     if not pixel1:
    #         try:
    #             pixel1 = detector_config.pixel1
    #         except Exception as e:
    #             logger.error(f"{e}: Pixel 1 could not be retrieved.")
    #             return
    #     # Pixel 2
    #     try:
    #         pixel2 = self._transform.pixel2
    #     except Exception as e:
    #         pixel2 = None
    #         logger.error(f"{e}: Pixel 2 could not be retrieved.")
    #         return
    #     if not pixel2:
    #         try:
    #             pixel2 = detector_config.pixel2
    #         except Exception as e:
    #             logger.error(f"{e}: Pixel 2 could not be retrieved.")
    #             return

    #     # Shape
    #     try:
    #         shape = self._transform.detector.max_shape
    #     except Exception as e:
    #         shape = None
    #         logger.error(f"{e}: Shape could not be retrieved from detector.")
    #     if not shape:
    #         try:
    #             shape = detector_config.max_shape
    #         except Exception as e:
    #             logger.error(f"{e}: Shape could not be retrieved from detector-config.")
    #             return

    #     try:
    #         poni1 = self._transform._poni1
    #     except Exception as e:
    #         logger.error(f"{e}: PONI 1 could not be retrieved from h5.")
    #         return
    #     try:
    #         poni2 = self._transform._poni2
    #     except Exception as e:
    #         logger.error(f"{e}: PONI 2 could not be retrieved from h5.")
    #         return
    #     try:
    #         rot1 = self._transform._rot1
    #     except Exception as e:
    #         logger.error(f"{e}: Rotation 1 could not be retrieved from h5.")
    #         return
    #     try:
    #         rot2 = self._transform._rot2
    #     except Exception as e:
    #         logger.error(f"{e}: Rotation 2 could not be retrieved from h5.")
    #         return
    #     try:
    #         rot3 = self._transform._rot3
    #     except Exception as e:
    #         logger.error(f"{e}: Rotation 3 could not be retrieved from h5.")
    #         return
        
    #     poni_dict = {
    #         PONI_KEY_VERSION : 2,
    #         PONI_KEY_DETECTOR : detector.name,
    #         PONI_KEY_BINNING : detector._binning,
    #         PONI_KEY_DETECTOR_CONFIG : detector_config,
    #         PONI_KEY_WAVELENGTH : wave,
    #         PONI_KEY_DISTANCE : dist,
    #         PONI_KEY_PIXEL1 : pixel1,
    #         PONI_KEY_PIXEL2 : pixel2,
    #         PONI_KEY_SHAPE1 : shape[0],
    #         PONI_KEY_SHAPE2 : shape[1],
    #         PONI_KEY_PONI1 : poni1,
    #         PONI_KEY_PONI2 : poni2,
    #         PONI_KEY_ROT1 : rot1,
    #         PONI_KEY_ROT2 : rot2,
    #         PONI_KEY_ROT3 : rot3,
    #     }
    #     return poni_dict

    # @logger_info
    # def retrieve_poni_instance_from_file(self, poni_filename=''):
    #     poni_filename = Path(poni_filename)

    #     if not poni_filename.is_file():
    #         return

    #     poni = PoniFile(data=str(poni_filename))
    #     return poni


    # @logger_info
    # def update_ponifile_parameters(self, dict_poni=dict()) -> None:
    #     """
    #     Changes manually the functional poni parameters of pygix
    #     """
    #     if not self._transform:
    #         return

    #     if dict_poni:
    #         try:
    #             new_poni = PoniFile(data=dict_poni)
    #             self._transform._init_from_poni(new_poni)
    #         except Exception as e:
    #             logger.error(e)
    #     else:
    #         if self.active_ponifile:
    #             self._transform.load(self.active_ponifile)

    # @logger_info
    # def update_grazinggeometry(self, poni_filename='') -> None:
    #     """
    #     If there is an active ponifile, inherits the methods from Transform class (pygix module)
    #     """        
    #     if not poni_filename:
    #         poni_filename = self.active_ponifile

    #     if not poni_filename:
    #         logger.info(f"No active ponifile. GrazingGeometry was not updated")            
    #         return
    #     if not Path(poni_filename).is_file():
    #         logger.info(f"The .poni file {poni_filename} does not exist.")
    #         return

    #     # Load the ponifile
    #     try:
    #         self._transform.load(poni_filename)
    #         logger.info(f"Loaded poni file: {poni_filename}")
    #     except Exception as e:
    #         logger.error(f"{e}: Ponifile could not be loaded to GrazingGeometry")
        
    #     # Update default incident and tilt angles
    #     try:
    #         self.update_incident_tilt_angle()
    #     except Exception as e:
    #         logger.error(f"{e}: angles could not be updated.")

    # @logger_info
    # def update_angles(self, sample_name=str(), list_index=list()):
    #     iangle = self.get_incident_angle(
    #         sample_name=sample_name,
    #         index_list=list_index,
    #     )
    #     tangle = self.get_tilt_angle(
    #         sample_name=sample_name,
    #         index_list=list_index,
    #     )
    #     self.update_incident_tilt_angle(
    #         incident_angle=iangle,
    #         tilt_angle=tangle,
    #     )

    @logger_info
    def update_incident_tilt_angle(self, incident_angle=0.0, tilt_angle=0.0):
        """
        Update the incident and tilt angles inherited from GrazingGeometry

        Keyword Arguments:
            incident_angle -- (default: {0.0})
            tilt_angle --  (default: {0.0})
        """        
        # Incident angle
        try:
            self._transform.set_incident_angle(
                incident_angle=incident_angle,
            )
            logger.info(f"Incident angle set at {incident_angle}")
        except Exception as e:
            logger.error(f"{e}: Incident angle could not be updated.")

        # Tilt angle
        try:
            self._transform.set_tilt_angle(
                tilt_angle=tilt_angle,
            )
            logger.info(f"Tilt angle set at {tilt_angle}")
        except Exception as e:
            logger.error(f"{e}: Tilt angle could not be updated.")

    @logger_info
    def update_orientation(self, qz_parallel=True, qr_parallel=True) -> None:
        """
        Updates two parameters to define the rotation of the detector and the orientation of the sample axis
        Pygix defined a sample orientation upon 1-4 values

        Keyword Arguments:
            qz_parallel -- inversion of the qz axis (default: {True})
            qr_parallel -- inversion of the qr axis (default: {True})
        """
        try:
            sample_orientation = DICT_SAMPLE_ORIENTATIONS[(qz_parallel, qr_parallel)]
            self._transform.set_sample_orientation(
                sample_orientation=sample_orientation,
            )
            logger.info(f"The sample orientation (pygix) is set at {sample_orientation}.")
        except Exception as e:
            logger.error(f"The sample orientation (pygix) could not be updated.")


    #####################################
    ###### EDF METHODS ##########
    #####################################

    @logger_info
    def map_reshaping(
        self,
        data=None,
        # dict_poni=dict(),
        ):

        data_reshape, q, chi = self._ai.integrate2d(
            data=data,
            npt_rad=1000,
            unit="q_nm^-1",
        )
        logger.info(f"Reshaped map.")

        return data_reshape, q, chi
    



    @logger_info
    def raw_integration(
        self,
        sample_name=str(),
        sample_relative_address=True,
        index_list=list(),
        data=None,
        norm_factor=1.0,
        list_dict_integration=list(),
    ) -> list:
        """
        Chooses which integration is going to be performed: azimuthal (pyFAI), radial (pyFAI) or box (self method)

        Parameters:
        folder_name(str) : name of the folder(Group) in the first level of hierarchy
        index_list(list or int) : integer of list of integers for the files inside the folder
        data(np.array) : data can be uploaded directly
        norm_factor(float) : this value will be used by the pygix-pyFAI integration engine
        list_dict_integration(list) : list of dictionaries with key-values that will be read by the pygix-pyFAI integration engine
        
        Returns:
        list : list of numpy arrays with the result of the integration
        """
        # Get the data
        # if data is None:
        #     data = self.get_Edf_data(
        #         sample_name=sample_name,
        #         sample_relative_address=sample_relative_address,
        #         index_list=index_list,
        #     )

        # Get the normalization factor
        # if norm_factor == 1.0:
        #     norm_factor = self.get_norm_factor(
        #         sample_name=sample_name,
        #         index_list=index_list,
        #     )

        array_compiled = []

        for dict_integration in list_dict_integration:
            if dict_integration[KEY_INTEGRATION] == CAKE_LABEL:
                if dict_integration[CAKE_KEY_TYPE] == CAKE_KEY_TYPE_AZIM:
                    res = self.raw_integration_azimuthal(
                        data=data,
                        norm_factor=norm_factor,
                        dict_integration=dict_integration,
                    )

                elif dict_integration[CAKE_KEY_TYPE] == CAKE_KEY_TYPE_RADIAL:
                    res = self.raw_integration_radial(
                        data=data,
                        norm_factor=norm_factor,
                        dict_integration=dict_integration,
                    )
            elif dict_integration[KEY_INTEGRATION] == BOX_LABEL:
                res = self.raw_integration_box(
                    data=data,
                    norm_factor=norm_factor,
                    dict_integration=dict_integration,
                )
            else:
                print(ERROR_RAW_INTEGRATION)
                res = None

            array_compiled.append(res)
        return array_compiled

    @logger_info
    def raw_integration_azimuthal(
        self, 
        data=None,
        norm_factor=1.0,
        dict_integration=dict(),
    ) -> np.array:
        """
        Performs an azimuthal integration using the pygix-pyFAI engine

        Parameters:
        data(np.array) : data to be integrated
        norm_factor(float) : this value will be used by the pygix-pyFAI integration engine
        dict_integration(dict) : dictionary with key-values that will be read by the pygix-pyFAI integration engine
        
        Returns:
        np.array : result of the integration
        """
        # Take the array of intensity
        if (data is None) or (not dict_integration):
            return
        
        p0_range=dict_integration[CAKE_KEY_RRANGE]
        p1_range=dict_integration[CAKE_KEY_ARANGE]
        unit=dict_integration[CAKE_KEY_UNIT]
        npt = dict_integration[CAKE_KEY_ABINS]

        if npt == 0:
            npt=self.calculate_bins(
                radial_range=p0_range,
                unit=unit,
            )

        # Do the integration with pygix/pyFAI
        try:
            logger.info(f"Trying azimuthal integration with: data-shape={data.shape} bins={npt}, p0_range={p0_range}, p1_range={p1_range}, unit={unit}")
            y_vector, x_vector = self.integrate_1d(
                process='sector',
                data=data,
                npt=npt,
                p0_range=p0_range,
                p1_range=p1_range,
                unit=UNIT_GI[unit],
                normalization_factor=float(norm_factor),
                polarization_factor=POLARIZATION_FACTOR,
            )
            logger.info("Integration performed.")
        except Exception as e:
            logger.error(f"{e}: Error during azimuthal integration.")
            return

        return np.array([x_vector, y_vector])

    @logger_info
    def raw_integration_radial(
        self, 
        data=None,
        norm_factor=1.0,
        dict_integration=dict(),
    ) -> np.array:
        """
        Performs a radial integration using the pygix-pyFAI engine

        Parameters:
        data(np.array) : data to be integrated
        norm_factor(float) : this value will be used by the pygix-pyFAI integration engine
        dict_integration(dict) : dictionary with key-values that will be read by the pygix-pyFAI integration engine
        
        Returns:
        np.array : result of the integration
        """
        # Take the array of intensity
        if (data is None) or (not dict_integration):
            return

        # Do the integration with pygix/pyFAI
        npt  = int(dict_integration[CAKE_KEY_ABINS])
        p0_range = dict_integration[CAKE_KEY_RRANGE]
        p1_range = dict_integration[CAKE_KEY_ARANGE]

        
        unit = UNIT_GI[dict_integration[CAKE_KEY_UNIT]]
        
        try:
            logger.info(f"Trying radial integration with: npt={npt}, p0_range={p0_range}, p1_range={p1_range}, unit={unit}")
            y_vector, x_vector = self.integrate_1d(
                process='chi',
                data=data,
                npt=npt,
                p0_range=p1_range,
                p1_range=p0_range,
                unit=unit,
                normalization_factor=float(norm_factor),
                polarization_factor=POLARIZATION_FACTOR,
            )
            logger.info("Integration performed.")
        except:
            logger.info("Error during radial integration.")
            return
        return np.array([x_vector, y_vector])

    @logger_info
    def raw_integration_box(
        self, 
        data=None,
        norm_factor=1.0,
        dict_integration=dict(),
    ) -> pd.DataFrame:
        """
        Performs a box integration using the pygix-pyFAI engine

        Parameters:
        data(np.array) : data to be integrated
        norm_factor(float) : this value will be used by the pygix-pyFAI integration engine
        dict_integration(dict) : dictionary with key-values that will be read by the pygix-pyFAI integration engine
        
        Returns:
        np.array : result of the integration
        """
        # Take the array of intensity
        if (data is None) or (not dict_integration):
            return

        # Get the direction of the box
        process = DICT_BOX_ORIENTATION[dict_integration[BOX_KEY_DIRECTION]]
        unit=dict_integration[BOX_KEY_INPUT_UNIT]
        try:
            if process == 'opbox':
                p0_range, p1_range = dict_integration[BOX_KEY_OOPRANGE], dict_integration[BOX_KEY_IPRANGE]
                npt = self.calculate_bins(
                    radial_range=dict_integration[BOX_KEY_OOPRANGE],
                    unit=unit,
                )
            elif process == 'ipbox':
                p0_range, p1_range = dict_integration[BOX_KEY_IPRANGE], dict_integration[BOX_KEY_OOPRANGE]
                npt = self.calculate_bins(
                    radial_range=dict_integration[BOX_KEY_IPRANGE],
                    unit=unit,
                )
            else:
                return
        except:
            p0_range, p1_range, npt = None, None, NPT_RADIAL

        # Transform input units if necessary
        p0_range = [self.get_q_nm(
            value=position,
            input_unit=unit,
            direction=dict_integration[BOX_KEY_DIRECTION],
        ) for position in p0_range]

        p1_range = [self.get_q_nm(
            value=position,
            input_unit=unit,
            direction=dict_integration[BOX_KEY_DIRECTION],
        ) for position in p1_range]

        # Do the integration with pygix/pyFAI
        try:
            logger.info(f"Trying box integration with: process={process}, npt={npt}, p0_range={p0_range}, p1_range={p1_range}, unit={unit}")
            y_vector, x_vector = self.integrate_1d(
                process=process,
                data=data,
                npt=npt,
                p0_range=p0_range,
                p1_range=p1_range,
                unit=UNIT_GI[unit],
                normalization_factor=float(norm_factor),
                polarization_factor=POLARIZATION_FACTOR,
                # method='bbox',
            )
            x_vector = self.transform_q_units(
                x_vector=x_vector,
                input_unit=dict_integration[BOX_KEY_INPUT_UNIT],
                output_unit=dict_integration[BOX_KEY_OUTPUT_UNIT],
                direction=dict_integration[BOX_KEY_DIRECTION],
            )

            logger.info("Integration performed.")
        except:
            logger.info("Error during box integration.")
            return

        return np.array([x_vector, y_vector])

    @logger_info
    def calculate_bins(self, radial_range=[], unit='q_nm^-1') -> int:
        """
        Calculates the bins between two q values

        Parameters:
        radial_range(list, tuple) : two components with the minimum and maximum radial position to be integrated
        unit(str) : 'q_nm^-1', 'q_A^-1', '2th_deg' or '2th_rad'

        Returns:
        int : number of counts to be generated
        """
        if unit in ('q_nm^-1', 'q_A^-1'):
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

    @logger_info
    def q_to_twotheta(self, q=0.0, unit='q_nm^-1', degree=False) -> float:
        """
        Transforms from q to 2theta (rad)

        Parameters:
        q(float) : modulus of q, scattering vector
        unit(str) : 'q_nm^-1' or 'q_A^-1'
        degree(bool) : the result will be in degrees (True) or radians (False)

        Returns:
        float : twotheta value
        """
        if unit == 'q_nm^-1':
            twotheta = 2 * np.arcsin((q*self._wavelength * 1e9)/(4*np.pi))
        elif unit == 'q_A^-1':
            twotheta = 2 * np.arcsin((q*self._wavelength * 1e10)/(4*np.pi))
        else:
            return
        return np.rad2deg(twotheta) if degree else twotheta

    @logger_info
    def get_q_nm(self, value=0.0, direction='Vertical', input_unit='q_nm^-1') -> float:
        """
            Return a q(nm-1) value from another unit
        """
        if input_unit == 'q_nm^-1':
            return value
        elif input_unit == 'q_A^-1':
            return value
        elif input_unit == '2th_deg':
            return self.twotheta_to_q(twotheta=value, direction=direction, deg=True)
        elif input_unit == '2th_rad':
            return self.twotheta_to_q(twotheta=value, deg=False)
        else:
            return None

    @logger_info
    def twotheta_to_q(self, twotheta=0.0, direction='vertical', deg=True) -> float:
        """
            Returns the q(nm-1) from the 2theta value
        """
        if deg:
            twotheta = np.radians(twotheta)
        try:
            wavelength_nm = self._wavelength * 1e9
        except:
            return
        
        try:
            alpha_inc = np.radians(self._incident_angle)
        except:
            alpha_inc = 0.0
        
        q_horz = 2 * np.pi / wavelength_nm * (np.cos(alpha_inc) * np.sin(twotheta))
        q_vert = 2 * np.pi / wavelength_nm * (np.sin(twotheta) + np.sin(alpha_inc))

        if direction == BOX_KEY_TYPE_VERT:
            return q_horz
        elif direction == BOX_KEY_TYPE_HORZ:
            return q_vert
        else:
            return


    @logger_info
    def transform_q_units(
        self, 
        x_vector=None, 
        input_unit=None, 
        output_unit=None, 
        direction='vertical',
        ):

        if x_vector is None:
            return

        if input_unit == output_unit:
            return x_vector
        
        # From Q
        if input_unit in UNITS_Q:
            if output_unit in UNITS_Q:
                if output_unit in QNM_ALIAS:
                    x_vector *= 10
                elif output_unit in QA_ALIAS:
                    x_vector /= 10
                return x_vector

            elif output_unit in UNITS_THETA:
                if output_unit in DEG_ALIAS:
                    x_vector = self.q_to_twotheta(
                        q=x_vector,
                        unit=input_unit,
                        degree=True,
                    )
                    return x_vector
                elif output_unit in RAD_ALIAS:
                    x_vector = self.q_to_twotheta(
                        q=x_vector,
                        unit=input_unit,
                        degree=False,
                    )
                    return x_vector
        # From TTH
        elif input_unit in UNITS_THETA:
            if output_unit in UNITS_THETA:
                if output_unit in DEG_ALIAS:
                    return x_vector*180/np.pi
                elif output_unit in RAD_ALIAS:
                    return x_vector*np.pi/180
            elif output_unit in UNITS_Q:
                if input_unit in DEG_ALIAS:
                    vector_nm = self.twotheta_to_q(
                        twotheta=x_vector,
                        direction=direction,
                        deg=True,
                    )
                elif input_unit in RAD_ALIAS:
                    vector_nm = self.twotheta_to_q(
                        twotheta=x_vector,
                        direction=direction,
                        deg=False,
                    )

                if output_unit in QNM_ALIAS:
                    return vector_nm
                elif output_unit in QA_ALIAS:
                    return vector_nm/10

    @logger_info
    def get_detector_array(self, shape=()) -> np.array:
        """
        Returns an array with detector shape and rotated, according to sample orientation (pygix-pyFAI)

        Parameters:
        None

        Returns:
        np.array : 2D array with the shape of the detector registered in the active ponifile
        """
        try:
            # This method does not work with ALBA_NCD_Nov2022
            if not shape:
                shape = self.get_shape()

            logger.info(f"Shape of the detector: {shape}")
            d2,d1 = np.meshgrid(
                np.linspace(1,shape[1],shape[1]),
                np.linspace(1,shape[0],shape[0]),
            )
            out = np.array([d1,d2])
            return out
        except:
            return None

    @logger_info
    def get_mesh_matrix(self, unit='q_nm^-1', shape=()):
        """
        Returns both horizontal and vertical mesh matrix for Grazing-Incidence geometry, returns also the corrected data without the missing wedge
        
        Parameters:
        unit(str) : 'q_nm^-1', 'q_A^-1', '2th_deg' or '2th_rad'
        data(np.array) : 2D map data

        Returns:
        np.array(QX)
        np.array(QZ)
        np.array(data)
        """
        if not shape:
            logger.info(f"Shape is None. Returns.")
            return

        # Get the detector array, it is always the same shape (RAW MATRIX SHAPE!), no rotations yet
        # shape = data.shape
        det_array = self.get_detector_array(shape=shape)

        # Get the mesh matrix
        if unit in UNITS_Q:
            try:
                # calc_q will take into account the sample_orientation in GrazingGeometry instance
                scat_z, scat_xy = self.calc_q(
                    d1=det_array[0,:,:],
                    d2=det_array[1,:,:],
                )
                logger.info(f"Shape of the scat_z matrix: {scat_z.shape}")
                logger.info(f"Shape of the scat_x matrix: {scat_xy.shape}")
            except:
                scat_z, scat_xy = None, None
                logger.info(f"Scat_z matrix could not be generated.")
                logger.info(f"Scat_x matrix could not be generated.")
        elif unit in UNITS_THETA:
            try:
                scat_z, scat_xy = self.calc_angles(
                    d1=det_array[0,:,:],
                    d2=det_array[1,:,:],
                )
                logger.info(f"Shape of the scat_z matrix: {scat_z.shape}")
                logger.info(f"Shape of the scat_x matrix: {scat_xy.shape}")
            except:
                scat_z, scat_xy = None, None
                logger.info(f"Scat_z matrix could not be generated.")
                logger.info(f"Scat_x matrix could not be generated.")

        # Transform units
        if (scat_z is not None) and (scat_xy is not None):
            DICT_PLOT = DICT_UNIT_PLOTS.get(unit, DICT_PLOT_DEFAULT)
            scat_z *= DICT_PLOT['SCALE']
            scat_xy *= DICT_PLOT['SCALE']
            logger.info(f"Changing the scale of the matriz q units. Scale: {DICT_PLOT['SCALE']}")
        else:
            return
        return scat_xy, scat_z