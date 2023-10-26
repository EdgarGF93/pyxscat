
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
from pygix.transform import Transform
from pygix.grazing_units import TTH_DEG, TTH_RAD, Q_A, Q_NM
from pyxscat.other.integrator_methods import *
from pyxscat.other.setup_methods import *
from pyxscat.other.units import *
from pyxscat.poni_methods import open_poni
import numpy as np

from pyxscat.logger_config import setup_logger
logger = setup_logger()

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

from pyxscat.logger_config import setup_logger
logger = setup_logger()

def logger_info(func):
    def wrapper(*args, **kwargs):
        logger.info(f'We entered into function: {func.__name__}')
        return func(*args, **kwargs)
    return wrapper

class GIIntegrator(Transform):
    """
    Class to handle .poni parameters, pyFAI reshapings and pygix (GI) transformations

    Arguments:
        Transform -- inherits the methods from Transform class (pygix)
    """    

    def __init__(self) -> None:
        super().__init__()
        self.init_transform()
        self.init_ai()
        self.active_ponifile=''
        self._poni = None

    @logger_info
    def init_transform(self):
        """
        Initiate as 0.0 both incident and tilt angles of the sample
        """
        self.update_incident_angle(incident_angle=0.0)
        self.update_tilt_angle(tilt_angle=0.0)

    @logger_info
    def update_incident_angle(self, incident_angle=0.0):
        """
        Updates the parameter incident_angle in GrazingGeometry instance

        Keyword Arguments:
            incident_angle -- pitch angle, projection of the beam into the surface-sample (default: {0.0})
        """
        if not isinstance(incident_angle, float):
            try:
                incident_angle = float(incident_angle)
            except Exception as e:
                logger.error(f'{e}: {incident_angle} is not a valid incident angle. Set up as 0.0')
                incident_angle = 0.0
        
        self.set_incident_angle(
            incident_angle=incident_angle,
        )
        logger.info(f'Incident angle set up as {incident_angle}.')

    @logger_info
    def update_tilt_angle(self, tilt_angle=0.0):
        """
        Updates the parameter tilt_angle in GrazingGeometry instance

        Keyword Arguments:
            tilt_angle -- roll angle of the sample surface (default: {0.0})
        """
        if not isinstance(tilt_angle, float):
            try:
                tilt_angle = float(tilt_angle)
            except Exception as e:
                logger.error(f'{e}: {tilt_angle} is not a valid tilt angle. Set up as 0.0')
                tilt_angle = 0.0
        
        self.set_tilt_angle(
            tilt_angle=tilt_angle,
        )
        logger.info(f'Tilt angle set up as {tilt_angle}.')

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
            self.set_sample_orientation(
                sample_orientation=sample_orientation,
            )
            logger.info(f"The sample orientation (pygix) is set at {sample_orientation}.")
        except Exception as e:
            logger.error(f"The sample orientation (pygix) could not be updated.")

    @logger_info
    def init_ai(self):
        self._ai = AzimuthalIntegrator()

    @logger_info
    def update_poni(self, poni=None):
        """
        Updates the .poni parameters in AzimuthalIntegrator and GrazingGeometry instances

        Keyword Arguments:
            poni -- PoniFile instance, taken from pyFAI.io.ponifile or ponifile string path (default: {None})
        """
        poni = open_poni(poni=poni)

        if poni is None:
            logger.error(f'poni instance could not be updated.')
            return

        self._update_gi(poni=poni)
        self._update_ai(poni=poni)
        self._set_poni(poni=poni)

    @logger_info
    def _update_gi(self, poni=None):
        """
        Update the .poni parameters of GrazingGeometry instance

        Keyword Arguments:
            poni -- pyFAI.io.PoniFile instance (default: {None})
        """        
        if poni is None:
            return
        
        try:
            self._init_from_poni(poni=poni)
            logger.info(f'GrazingGeometry instance was updated.')
        except Exception as e:
            logger.error(f'{e}: GrazingGeometry could not be updated.')

    @logger_info
    def _update_ai(self, poni=None):
        """
        Update the .poni parameters of pyFAI.AzimuthalIntegrator instance

        Keyword Arguments:
            poni -- pyFAI.io.PoniFile instance (default: {None})
        """    
        if poni is None:
            return

        try:
            self._ai._init_from_poni(poni=poni)
            logger.info(f'GrazingGeometry instance was updated.')
        except Exception as e:
            logger.error(f'{e}: GrazingGeometry could not be updated.')

    @logger_info
    def _set_poni(self, poni=None):
        """
        Set the poni instance

        Keyword Arguments:
            poni -- pyFAI.io.PoniFile instance (default: {None})
        """        
        self._poni = poni
        
    #####################################
    ###### INTEGRATION METHODS ##########
    #####################################

    @logger_info
    def generate_integration(self, data=None, norm_factor=1.0, list_dict_integration=list()) -> list:
        """
        Yields an integration: azimuthal (pyFAI), radial (pyFAI) or box (pygix)

        Keyword Arguments:
            data -- 2D array to be integrated (default: {None})
            norm_factor -- normalization factor to be used during integration (default: {1.0})
            list_dict_integration -- list of dictionaries with integration instructions (default: {list()})

        Yields:
            numpy array with the results of the integration
        """        

        for dict_integration in list_dict_integration:
            if dict_integration[KEY_INTEGRATION] == CAKE_LABEL:
                if dict_integration[CAKE_KEY_TYPE] == CAKE_KEY_TYPE_AZIM:

                    res = self.integration_azimuthal(
                        data=data,
                        norm_factor=norm_factor,
                        dict_integration=dict_integration,
                    )

                elif dict_integration[CAKE_KEY_TYPE] == CAKE_KEY_TYPE_RADIAL:

                    res = self.integration_radial(
                        data=data,
                        norm_factor=norm_factor,
                        dict_integration=dict_integration,
                    )

            elif dict_integration[KEY_INTEGRATION] == BOX_LABEL:

                res = self.integration_box(
                    data=data,
                    norm_factor=norm_factor,
                    dict_integration=dict_integration,
                )

            else:
                logger.info(ERROR_RAW_INTEGRATION)
                res = None

            yield res

    @logger_info
    def integration_azimuthal(self, data=None, norm_factor=1.0, dict_integration=dict()) -> np.array:
        """
        Performs an azimuthal integration using the pyFAI engine

        Keyword Arguments:
            data -- 2D array to be integrated (default: {None})
            norm_factor -- normalization factor to be used during integration (default: {1.0})
            dict_integration -- dictionary with integration instructions (default: {dict()})

        Returns:
            result of the integration
        """

        if data is None:
            logger.error(f'Data is None. No integration to be done.')
            return

        if not dict_integration:
            logger.error(f'No dict integration.')
            return

        if not is_cake_dictionary(dict_integration=dict_integration):
            logger.error(f'{dict_integration} is not a valid dict for cake integration.')
            return
        
        p0_range=dict_integration[CAKE_KEY_RRANGE]
        p1_range=dict_integration[CAKE_KEY_ARANGE]
        unit=dict_integration[CAKE_KEY_UNIT]
        npt = dict_integration[CAKE_KEY_ABINS]

        if npt == 0:
            try:
                npt=self.calculate_bins(
                    radial_range=p0_range,
                    unit=unit,
                )
            except Exception as e:
                logger.error(f'{e} Error during calculating bins. p0_range:{p0_range}, unit: {unit}')
                npt = 1000
                logger.info(f'npt set to 1000')

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
            logger.info("Azimuthal integration performed.")
        except Exception as e:
            logger.error(f"{e}: Error during azimuthal integration.")
            return

        return np.array([x_vector, y_vector])

    @logger_info
    def integration_radial(self, data=None, norm_factor=1.0, dict_integration=dict()) -> np.array:
        """
        Performs a radial integration using the pyFAI engine

        Keyword Arguments:
            data -- 2D array to be integrated (default: {None})
            norm_factor -- normalization factor to be used during integration (default: {1.0})
            dict_integration -- dictionary with integration instructions (default: {dict()})

        Returns:
            result of the integration
        """

        if data is None:
            logger.error(f'Data is None. No integration to be done.')
            return

        if not dict_integration:
            logger.error(f'No dict integration.')
            return

        if not is_cake_dictionary(dict_integration=dict_integration):
            logger.error(f'{dict_integration} is not a valid dict for cake integration.')
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
            logger.info("Radial integration performed.")
        except:
            logger.info("Error during radial integration.")
            return

        return np.array([x_vector, y_vector])

    @logger_info
    def integration_box(self, data=None, norm_factor=1.0, dict_integration=dict()) -> np.array:
        """
        Performs a box integration using the pygix engine

        Keyword Arguments:
            data -- 2D array to be integrated (default: {None})
            norm_factor -- normalization factor to be used during integration (default: {1.0})
            dict_integration -- dictionary with integration instructions (default: {dict()})

        Returns:
            result of the integration
        """
        
        if data is None:
            logger.error(f'Data is None. No integration to be done.')
            return

        if not dict_integration:
            logger.error(f'No dict integration.')
            return

        if not is_box_dictionary(dict_integration=dict_integration):
            logger.error(f'{dict_integration} is not a valid dict for box integration.')
            return

        # Get the direction of the box
        process = DICT_BOX_ORIENTATION[dict_integration[BOX_KEY_DIRECTION]]
        unit=dict_integration[BOX_KEY_INPUT_UNIT]

        if process == 'opbox':
            p0_range, p1_range = dict_integration[BOX_KEY_OOPRANGE], dict_integration[BOX_KEY_IPRANGE]
            try:
                npt = self.calculate_bins(
                    radial_range=dict_integration[BOX_KEY_OOPRANGE],
                    unit=unit,
                )
            except Exception as e:
                logger.error(f'{e}: error during calculating bins. Rad.range: {dict_integration[BOX_KEY_OOPRANGE]}, unit:{unit}')
                npt = 1000
                logger.info(f'npt set to 1000')
        elif process == 'ipbox':
            p0_range, p1_range = dict_integration[BOX_KEY_IPRANGE], dict_integration[BOX_KEY_OOPRANGE]
            try:
                npt = self.calculate_bins(
                    radial_range=dict_integration[BOX_KEY_IPRANGE],
                    unit=unit,
                )                
            except Exception as e:
                logger.error(f'{e}: error during calculating bins. Rad.range: {dict_integration[BOX_KEY_IPRANGE]}, unit:{unit}')
                npt = 1000
                logger.info(f'npt set to 1000')
        else:
            return

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

    #####################################
    ###### UNIT-TRANSFORMATION METHODS ##
    #####################################

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
        if unit in Q_ALIAS:
            
            twotheta1 = self.q_to_twotheta(
                q=radial_range[0],
                unit=unit,
            )

            twotheta2 = self.q_to_twotheta(
                q=radial_range[1],
                unit=unit,
            )
        elif unit == DEG_ALIAS:

            twotheta1, twotheta2 = np.radians(radial_range[0]), np.radians(radial_range[1])

        elif unit == RAD_ALIAS:

            twotheta1, twotheta2 = radial_range[0], radial_range[1]

        else:
            return

        return int(round(self._dist / self.get_pixel1() * (np.tan(twotheta2) - np.tan(twotheta1))))

    @logger_info
    def q_to_twotheta(self, q=0.0, unit='q_nm^-1', degree=False) -> float:
        """
        Transforms q into 2theta

        Keyword Arguments:
            q -- modulus of q, scattering vector (default: {0.0})
            unit -- 'q_nm^-1' or 'q_A^-1' (default: {'q_nm^-1'})
            degree -- the result will be in degrees (True) or radians (False) (default: {False})

        Returns:
            twotheta value
        """
        try:
            wavelength = self._wavelength
        except Exception as e:
            logger.error(f'{e} There is no wavelength to transform q into 2theta')
            return

        if unit in QNM_ALIAS:
            twotheta = 2 * np.arcsin((q * wavelength * 1e9) / (4 * np.pi))
        elif unit in QA_ALIAS:
            twotheta = 2 * np.arcsin((q * wavelength * 1e10) / (4 * np.pi))
        else:
            return

        if degree:
            twotheta = np.rad2deg(twotheta)

        return twotheta

    @logger_info
    def twotheta_to_q(self, twotheta=0.0, degree_input=True, direction='vertical', output_unit='q_nm^-1',) -> float:
        """
        Transforms 2theta into q

        Keyword Arguments:
            twotheta -- exit angle (default: {0.0})
            degree_input -- if True, the input twotheta is degrees, if not, radians (default: {True})
            direction -- if vertical, q is taken as qz, if horizontal, is taken as qxy (default: {'vertical'})
            output_unit -- 'q_nm^-1' or 'q_A^-1' (default: {'q_nm^-1'})

        Returns:
            modulus of q, scattering vector
        """        
        try:
            wavelength = self._wavelength
            wavelength_nm = wavelength * 1e9
        except Exception as e:
            logger.error(f'{e} There is no wavelength to transform 2theta into q.')
            return

        if degree_input:
            twotheta = np.radians(twotheta)
        
        try:
            alpha_inc = np.radians(self._incident_angle)
        except:
            alpha_inc = 0.0
        
        q_horz = 2 * np.pi / wavelength_nm * (np.cos(alpha_inc) * np.sin(twotheta))
        q_vert = 2 * np.pi / wavelength_nm * (np.sin(twotheta) + np.sin(alpha_inc))

        if output_unit in QNM_ALIAS:
            pass
        elif output_unit in QA_ALIAS:
            q_horz /= 10
            q_vert /= 10

        if direction == BOX_KEY_TYPE_VERT:
            return q_horz
        elif direction == BOX_KEY_TYPE_HORZ:
            return q_vert
        else:
            return

    @logger_info
    def get_q_nm(self, value=0.0, direction='vertical', input_unit='q_nm^-1') -> float:
        """
            Return a q(nm-1) value from another unit
        """
        if input_unit in QNM_ALIAS:
            return value
        elif input_unit in Q_ALIAS:
            return value
        elif input_unit in DEG_ALIAS:
            return self.twotheta_to_q(twotheta=value, direction=direction, degree_input=True)
        elif input_unit in RAD_ALIAS:
            return self.twotheta_to_q(twotheta=value, degree_input=False)
        else:
            return None

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
                        degree_input=True,
                    )
                elif input_unit in RAD_ALIAS:
                    vector_nm = self.twotheta_to_q(
                        twotheta=x_vector,
                        direction=direction,
                        degree_input=False,
                    )

                if output_unit in QNM_ALIAS:
                    return vector_nm
                elif output_unit in QA_ALIAS:
                    return vector_nm/10

    #####################################
    ###### DETECTOR-ARRAY TRANSFORMATION METHODS ##
    #####################################

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

    @logger_info
    def map_reshaping(self, data=None):

        """
        Generates the reshaped map according to .poni parameters

        Keyword Arguments:
            data -- 2D matrix to be reshaped (default: {None})

        Returns:
            data_reshape -- 2D matrix with transformed coordinates (polar-q)
            q -- Azimuthal grid
            chi -- Polar grid
        """        
        try:
            data_reshape, q, chi = self._ai.integrate2d(
                data=data,
                npt_rad=1000,
                unit="q_nm^-1",
            )
        except Exception as e:
            logger.error(f'{e}: Reshaped_map could not retrieved.')
            data_reshape, q, chi = None, None, None

        return data_reshape, q, chi


