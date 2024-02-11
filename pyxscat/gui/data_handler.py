from pathlib import  Path
from pyFAI import load
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
from pygix.transform import Transform
from pygix.grazing_units import TTH_DEG, TTH_RAD, Q_A, Q_NM
from pyFAI.io.ponifile import PoniFile
import logging
import numpy as np
import fabio
from pydantic import BaseModel, ValidationError, confloat, constr, conlist
from pyxscat.edf import FullHeader

logger = logging.getLogger(__name__)

POLARIZATION_FACTOR = 0.99
DICT_BOX_ORIENTATION = {
    'horizontal' : 'ipbox',
    'vertical' : 'opbox',
}
QNM_ALIAS = ('q_nm^-1', 'q_nm^-1', 'nm', 'nm-1', 'qnm', 'q_nm')
QA_ALIAS = ('q_A^-1', 'q_A', 'q_a^-1', 'q_a^-1', 'a', 'a-1', 'qa', 'q_a')
Q_ALIAS = QNM_ALIAS + QA_ALIAS
RAD_ALIAS = ('2th_rad', 'rad', '2thrad', 'thrad', 'tth_rad', 'tthrad')
DEG_ALIAS = ('2th_deg', 'deg', '2thdeg', 'thdeg', 'tth_deg', 'tthdeg')
UNIT_GI = {
    'q_nm^-1' : Q_NM,
    'q_A^-1' : Q_A,
    '2th_deg' : TTH_DEG,
    '2th_rad' : TTH_RAD,
}
# Define a Pydantic model
class ConfigIntegrationCake(BaseModel):
    name: str
    unit : str
    radial_range: list
    azimuth_range : list
    npt_azim : int
    npt_rad : int
    integration_type : str

class ConfigIntegrationBox(BaseModel):
    name: str
    input_unit : str
    output_unit : str
    ip_range: list
    oop_range : list
    npt : int
    integration_type : str
    direction : str


class DataHandler(Transform):
    def __init__(
        self, 
        filename_list:list=[],
        ai:AzimuthalIntegrator=None, 
        poni:PoniFile=None, 
        config:dict=None,
        pattern:str="*.edf",
        ):
        super().__init__()
        
        self.list_filenames = filename_list
        self.list_headers = []
        self.ai = ai
        self.poni = poni
        self.config = config
        
        self.acquisitiontime_key = ""
        self.normalizationfactor_key = ""
        self.incidentangle_key = ""
        self.tiltangle_key = ""
        
        self.acquisition_time = None
        self.normalization_factor = 0.0
        self.incident_angle = 0.0
        self.tilt_angle = 0.0
        self.sample_orientation = 1
        
        self.reference_directory = ""
        self.reference_file = ""
        self.reference_acquisition_time = None
        self.pattern = pattern
        
        self.data = None
        self.data_reference = None
        self.reference_factor = 0.0
        
    def __repr__(self):
        return f"PyXScat Data Handler\n{super().__repr__()}"
        
    @property
    def list_filenames(self):
        return self._list_filenames
    
    @list_filenames.setter
    def list_filenames(self, value):
        if not isinstance(value, (str, list, tuple)):
            self._list_filenames = []
            return
            
        if isinstance(value, str):
            value = [value]
        
        for filename in value:
            if not Path(filename).is_file():
                self._list_filenames = []
                break
        self._list_filenames = value
        
        if self._list_filenames:
            self.update_data()
            self.update_header()
            
    def set_filenames(self, list_filenames:list):
        self.list_filenames = list_filenames
            
    @property
    def ai(self):
        return self._ai
    
    @ai.setter
    def ai(self, value):
        if not isinstance(value, AzimuthalIntegrator):
            self._ai = None
        else:
            self._ai = value
            
        if not self._ai:
            logger.warning(f"Azimuthal integrator is set to None")
    
    def set_ai(self, ai:AzimuthalIntegrator):
        self.ai = ai
        
    @property
    def poni(self):
        return self._poni
    
    @poni.setter
    def poni(self, value):
        if isinstance(value, PoniFile):
            self._poni = value
        elif isinstance(value, (str, dict)):
            try:
                self._poni = PoniFile(value)
            except Exception as e:
                self._poni = None
        else:
            self._poni = None
            
        if self._poni:
            self.ai = load(self._poni)
            self._init_from_poni(poni=self._poni)
        else:
            logger.warning(f"{value} is not valid for a Poni instance (ai was not changed).")
            
    def set_poni(self, poni:PoniFile):
        self.poni = poni
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        if isinstance(value, np.ndarray):
                self._data = value
        else:
            logger.warning(f"{value} is not a np.array but {type(value)}")
            
    @property
    def list_headers(self):
        return self._list_headers
    
    @list_headers.setter
    def list_headers(self, value):
        self._list_headers = value
        if self._list_headers:
            self.update_metadata_values()
            
    @property
    def acquisitiontime_key(self):
        return self._acquisitiontime_key
    
    @acquisitiontime_key.setter
    def acquisitiontime_key(self, value):
        self._acquisitiontime_key = str(value)
        if self._acquisitiontime_key:
            self.update_acquisition_time()
    
    def set_acquisitiontime_key(self, key):
        self.acquisitiontime_key = key

    @property
    def normalizationfactor_key(self):
        return self._normalizationfactor_key
    
    @normalizationfactor_key.setter
    def normalizationfactor_key(self, value):
        self._normalizationfactor_key = str(value)
        if self._normalizationfactor_key:
            self.update_normalization_factor()
        
    def set_normalizationfactor_key(self, key):
        self.normalizationfactor_key = key

    @property
    def incidentangle_key(self):
        return self._incidentangle_key
    
    @incidentangle_key.setter
    def incidentangle_key(self, value):
        self._incidentangle_key = str(value)
        if self._incidentangle_key:
            self.update_incident_angle()
        
    def set_incidentangle_key(self, key):
        self.incidentangle_key = key

    @property
    def tiltangle_key(self):
        return self._tiltangle_key
    
    @tiltangle_key.setter
    def tiltangle_key(self, value):
        self._tiltangle_key = str(value)
        if self._tiltangle_key:
            self.update_tilt_angle()
        
    def set_tiltangle_key(self, key):
        self.tiltangle_key = key
        
    @property
    def acquisition_time(self):
        return self._acquisition_time

    @acquisition_time.setter
    def acquisition_time(self, value):
        if isinstance(value, float):
            self._acquisition_time = value
            self.set_automatic_reference_file()
            
    @property
    def normalization_factor(self):
        return self._normalization_factor
    
    @normalization_factor.setter
    def normalization_factor(self, value):
        if isinstance(value, float):
            self._normalization_factor = value
            self.update_data()
            
    @property
    def incident_angle(self):
        return self._incident_angle
    
    @incident_angle.setter
    def incident_angle(self, value):
        if isinstance(value, float):
            self._incident_angle = value
            self.change_incident_angle()

    @property
    def tilt_angle(self):
        return self._tilt_angle
    
    @tilt_angle.setter
    def tilt_angle(self, value):
        if isinstance(value, float):
            self._tilt_angle = value
            self.change_incident_angle()
            
    @property
    def sample_orientation(self):
        return self._sample_orientation
    
    @sample_orientation.setter
    def sample_orientation(self, value):
        if isinstance(value, int):
            if value in (1,2,3,4):
                self._sample_orientation = value
                self.change_sample_orientation(sample_orientation=self._sample_orientation)
                

    @property
    def reference_directory(self):
        return self._reference_directory
    
    @reference_directory.setter
    def reference_directory(self, value):
        if Path(value).exists():
            self._reference_directory = value
            self.set_automatic_reference_file()
            
    def set_reference_directory(self, reference_directory:str):
        self.reference_directory = reference_directory

    @property
    def reference_file(self):
        return self._reference_file
    
    @reference_file.setter
    def reference_file(self, value):
        if Path(value).is_file():
            self._reference_file = value
            self.update_reference_data()
            
    @property
    def data_reference(self):
        return self._data_reference
    
    @data_reference.setter
    def data_reference(self, value):
        if isinstance(value, np.ndarray):
            if self._data is not None:
                if self._data.shape == value.shape:
                    self._data_reference = value
                    self.update_data()
                    return
        self._data_reference = None
                    
    @property
    def reference_factor(self):
        return self._reference_factor
    
    @reference_factor.setter
    def reference_factor(self, value):
        if isinstance(value, float):
            self._reference_factor = value
            self.update_data()
    
    def set_reference_factor(self, reference_factor:float):
        self.reference_factor = reference_factor
        
    def set_automatic_reference_file(self):
        if self._acquisitiontime_key and self._acquisition_time:
            reference_directory = self._reference_directory
            if reference_directory:
                reference_files = Path(reference_directory).glob(self.pattern)
                for reference_file in reference_files:
                    acq_time_reference = self._get_acquisitiontime_from_file(filename=reference_file)
                    if acq_time_reference == self._acquisition_time:
                        self.reference_acquisition_time = acq_time_reference
                        self.reference_file = str(reference_file)
                        return
        self.reference_file = ""
        
    def set_reference_file(self, reference_file:str):
        self.reference_file = reference_file
        
    def update_data(self):
        filename_list = self._list_filenames
        if filename_list:
            data = self._open_data(list_filenames=filename_list)
            if (self.data_reference is not None) and self._reference_factor != 0.0:
                self._data = data - self._reference_factor * self._data_reference
            else:
                self._data = data

    def _open_data(self, list_filenames:list):
        if isinstance(list_filenames, str):
            list_filenames = [list_filenames]
            
        if len(list_filenames) > 1:
            data = self._average_data(list_filenames=list_filenames)
        else:
            data = fabio.open(list_filenames[0]).data
        return data
            
    def _average_data(self, list_filenames:list):
        return np.average([fabio.open(file).data for file in list_filenames], axis=0)
    
    def update_reference_data(self):
        if self._reference_file:
            data = self._open_data(list_filenames=self._reference_file)
            self.data_reference = data
    
    def update_header(self):
        filename_list = self._list_filenames
        if filename_list:
            list_headers = []
            for filename in filename_list: 
                try:
                    header = FullHeader(filename=str(filename)).get_header()
                    list_headers.append(header)
                except:
                    pass
        self._list_headers = list_headers
            
    def _get_metadata_value(self, key):
        if len(self._list_headers):
            return self._get_one_metadata_value(key=key)
        else:
            return self._get_multiple_metadata_value(key=key)
            
    def _get_one_metadata_value(self, key):
        header = self._list_headers[0]
        try:
            value = header.get(key)
            return value
        except:
            return
        
    def _get_acquisitiontime_from_file(self, filename):
        if self._acquisitiontime_key:
            header = FullHeader(filename=str(filename)).get_header()
            try:
                value = float(header.get(self._acquisitiontime_key))
                return value
            except:
                return
        
    def _get_multiple_metadata_value(self, key):
        value_list = []
        for header in self._list_headers:
            try:
                value = header.get(key)
            except:
                pass
            value_list.append(value)
        try:
            avg_value = np.mean(np.array(value_list))
            return avg_value
        except:
            return value_list
        
    def update_metadata_values(self):
        self.update_acquisition_time()
        self.update_normalization_factor()
        self.update_incident_angle()
        self.update_tilt_angle()
    
    def update_acquisition_time(self):
        if self._acquisitiontime_key:
            acq_time = self._get_metadata_value(key=self._acquisitiontime_key)
            self.acquisition_time = acq_time
            try:
                self.acquisition_time = float(acq_time)
            except:
                self.acquisition_time = None
            
    def update_normalization_factor(self):
        if self._normalizationfactor_key:
            norm_factor = self._get_metadata_value(key=self._normalizationfactor_key)
            self.normalization_factor = norm_factor
            try:
                self.normalization_factor = float(norm_factor)
            except:
                self.normalization_factor = 1.0
            
    def update_incident_angle(self):
        if self._incidentangle_key:
            iangle = self._get_metadata_value(key=self._incidentangle_key)
            self.incident_angle = iangle
            try:
                self.incident_angle = float(iangle)
            except:
                self.incident_angle = 0.0
            
    def update_tilt_angle(self):
        if self._tiltangle_key:
            tangle = self._get_metadata_value(key=self._tiltangle_key)
            try:
                self.tilt_angle = float(tangle)
            except:
                self.tilt_angle = 0.0
            
    def change_incident_angle(self):
        if self._incident_angle:
            try:
                self.set_incident_angle(self._incident_angle)
            except Exception as e:
                logger.warning(f"Incident angle could not be updated.")
        
    def change_tilt_angle(self):
        if self._tilt_angle:
            try:
                self.set_tilt_angle(self._tilt_angle)
            except Exception as e:
                logger.warning(f"Tilt angle could not be updated.")
            
    def change_sample_orientation(self, sample_orientation:int):
        self.set_sample_orientation(sample_orientation)
            
            
            
            
    def validate_config_cake(self, config):
        if not isinstance(config, dict):
            return
        try:
            validated_config = ConfigIntegrationCake.parse_obj(config)
            return validated_config
        except ValidationError as e:
            logger.warning(f"{e}. Not valid config dictionary for cake integration.")
            return
            
    def validate_config_box(self, config):
        if not isinstance(config, dict):
            return
        try:
            validated_config = ConfigIntegrationBox.parse_obj(config)
            return validated_config
        except ValidationError as e:
            logger.warning(f"{e}. Not valid config dictionary for box integration.")
            return
          
    def do_integration(self, config:dict, dim=1):
        if not self._data:
            return
        if self._ai:
            if self._poni:
                if dim == 1:
                    if config.get("integration_type") in ("azimuthal", "radial"):
                        res1d = self._do_integrate1d_cake(config=config)
                    elif config.get("integration_type") == "box":
                        res1d = self._do_integrate1d_box(config=config)
                    else:
                        res1d = None
                    return res1d
                elif dim == 2:
                    return self._do_integration2d(config=config)
                else:
                    return  
            else:
                logger.warning(f"Poni {self._poni} is not valid to integrate.")
        else:
            logger.warning(f"AI {self._ai} is not valid to integrate.")
    
    def _do_integrate1d_cake(self, config:dict):
        config_validated = self.validate_config_cake(config=config)
        if config_validated:
            if config_validated.get("integration_type") == "azimuthal":
                res1d = self._do_integrate1d_azimuthal(config=config_validated)
            elif config_validated.get("integration_type") == "radial":
                res1d = self._do_integrate1d_radial(config=config_validated)
            else:
                res1d = None
            return res1d
        else:
            return
        
    def _do_integrate1d_azimuthal(self, config:dict):
        try:
            res1d = self.integrate_1d(
                process='sector',
                data=self._data,
                npt=config.get("npt_rad"),
                p0_range=config.get("radial_range"),
                p1_range=config.get("azimuth_range"),
                unit=config.get("unit"),
                # method=("bbox", "csr", "cython"),
                normalization_factor=self._normalization_factor,
                polarization_factor=POLARIZATION_FACTOR,
            )
            return res1d
        except Exception as e:
            logger.warning(f"{e}: Azimuthal integration failed with config: {config}")
                
    def _do_integrate1d_radial(self, config:dict):
        try:
            res1d = self.integrate_1d(
                process='chi',
                data=self._data,
                npt=config.get("npt_rad"),
                p0_range=config.get("azimuth_range"),
                p1_range=config.get("radial_range"),
                unit=config.get("unit"),
                # method=("bbox", "csr", "cython"),
                normalization_factor=self._normalization_factor,
                polarization_factor=POLARIZATION_FACTOR,
            )
            return res1d
        except Exception as e:
            logger.warning(f"{e}: Radial integration failed with config: {config}")
    
    def _do_integrate1d_box(self, config:dict):
        config_box = self.prepare_config_box(config=config)
        try:
            res1d = self.integrate_1d(
                process=config_box.get("process"),
                data=self._data,
                npt=config_box.get("npt_rad"),
                p0_range=config_box.get("p0_range"),
                p1_range=config_box.get("p1_range"),
                unit=UNIT_GI[config_box.get("output_unit"),],
                normalization_factor=self._normalization_factor,
                polarization_factor=POLARIZATION_FACTOR,
                # method=("bbox", "csr", "cython"),
            )
            return res1d
        except Exception as e:
            logger.warning(f"{e}: Radial integration failed with config: {config_box}")
                
    def prepare_config_box(self, config:dict):
        process = DICT_BOX_ORIENTATION[config.get("direction")]
        unit=config.get("input_unit")
        if process == 'opbox':
            p0_range = config.get("oop_range")
            p1_range = config.get("ip_range")
        elif process == 'ipbox':
            p0_range = config.get("ip_range")
            p1_range = config.get("oop_range")    
                
        p0_range = [self.get_q_nm(
            value=position,
            input_unit=unit,
            direction=config.get("direction"),
        ) for position in p0_range]

        p1_range = [self.get_q_nm(
            value=position,
            input_unit=unit,
            direction=config.get("direction"),
        ) for position in p1_range]
        
        config["p0_range"] = p0_range
        config["p1_range"] = p1_range
        config["process"] = process
        return config
                  
                
    def _do_integration2d(self, config:dict):
        pass
            

    
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
            wavelength = self._ai._wavelength
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

        if direction == "vertical":
            return q_horz
        elif direction == "horizontal":
            return q_vert
        else:
            return