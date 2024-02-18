from pathlib import  Path
from pyFAI import load
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
from pygix.transform import Transform
from pygix.grazing_units import TTH_DEG, TTH_RAD, Q_A, Q_NM
from pyFAI.io.ponifile import PoniFile
import logging
from pyxscat.edf import FullHeader
import numpy as np
import fabio
from pydantic import BaseModel, ValidationError
import json
from typing import Optional



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
INTEGRATIONS_DIRECTORY = Path(__file__).parent.parent.joinpath("integration_dicts")






# Define a Pydantic model

class ConfigIntegrationAzimuthal(BaseModel):
    name: str
    type : str
    npt_rad : int
    npt_azim : Optional[int] = 512
    radial_range : Optional[list] = None
    azimuth_range : Optional[list] = None
    unit : Optional[str] = "q_nm^-1"
    
class ConfigIntegrationBox(BaseModel):
    name: str
    type : str
    direction : str
    input_unit : Optional[str] = "q_nm^-1"
    output_unit : Optional[str] = "q_nm^-1"
    ip_range: Optional[list] = None
    oop_range : Optional[list] = None
    npt_rad : int

class DataHandler(Transform):
    def __init__(
        self, 
        filename_list:list=[],
        ai:AzimuthalIntegrator=None, 
        poni:PoniFile=None, 
        configs:list=[],
        pattern:str="*.edf",
        ):
        super().__init__()
                
        self.list_filenames = filename_list
        self.list_headers = []
        self.ai = ai
        self.poni = poni
        self.configs = configs
        
        self.data = None
        self.data_cache = None
        self.data_reference = None
        self.mask_data = None
        self.results1d = []
            
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
        self.mask_file = ""
        
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
            # self.update_metadata_values()
            self.update_header()
            self.update_new_data()
            
            
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
            self.update_integrations()
            
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
    def configs(self):
        return self._configs
    
    @configs.setter
    def configs(self, value):
        if isinstance(value, str):
            value = [value]
            
        if not isinstance(value, list):
            self._configs = []
        else:
            self._configs = value
            
        # if self._configs:
        #     self.update_integrations()
            
    def set_configs(self, configs):
        self.configs = configs
            
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        if isinstance(value, np.ndarray):
            self._data = value
        else:
            self._data = None
            logger.warning(f"{value} is not a np.array but {type(value)}")
            
        if self._data is not None:
            self.update_integrations()
            
    def set_data(self, data):
        self.data = data
            
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
        else:
            self._acquisition_time = None
            
        if self._acquisition_time:
            self.update_reference()
            
    @property
    def normalization_factor(self):
        return self._normalization_factor
    
    @normalization_factor.setter
    def normalization_factor(self, value):
        if isinstance(value, float):
            self._normalization_factor = value
        else:
            self._normalization_factor = 1.0
            
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
        else:
            self._reference_directory = ""
            
    def set_reference_directory(self, reference_directory:str):
        self.reference_directory = reference_directory

    @property
    def reference_file(self):
        return self._reference_file
    
    @reference_file.setter
    def reference_file(self, value):
        if value:
            if Path(value).is_file():
                self._reference_file = value
                self.update_data_reference()
                
            else:
                self._reference_file = ""
        else:
            self._reference_file  =""
                
    @property
    def data_reference(self):
        return self._data_reference
    
    @data_reference.setter
    def data_reference(self, value):
        if isinstance(value, np.ndarray):
            if self._data is not None:
                if self._data.shape == value.shape:
                    self._data_reference = value
                else:
                    self._data_reference = None
            else:
                self._data_reference = None
        else:
            self._data_reference = None
            
        if self._data_reference is not None:
            self.update_data()
                    
    @property
    def reference_factor(self):
        return self._reference_factor
    
    @reference_factor.setter
    def reference_factor(self, value):
        if isinstance(value, float):
            self._reference_factor = value
            self.update_data_reference()
            self.update_data()
            
    @property
    def mask_file(self):
        return self._mask_file
    
    @mask_file.setter
    def mask_file(self, value):
        if value:
            if Path(value).is_file():
                self._mask_file = value
            else:
                self._mask_file = ""
        else:
            self._mask_file = ""
            
        if self._mask_file:
            self.update_data_mask()
            
    def set_mask_file(self, mask_file=""):
        self.mask_file = mask_file
        
    @property
    def mask_data(self):
        return self.mask_data
    
    @mask_data.setter
    def mask_data(self, value):
        self._mask_data = value
        if self._mask_data is not None:
            self.update_data()
            
    @property
    def results1d(self):
        return self._results1d
    
    @results1d.setter
    def results1d(self, value):
        self._results1d = value
    
    def set_reference_factor(self, reference_factor:float):
        self.reference_factor = reference_factor
        
    def set_automatic_reference_file(self):
        if self._acquisitiontime_key and self._acquisition_time:
            reference_directory = self._reference_directory
            if reference_directory:
                reference_files = Path(reference_directory).glob(self.pattern)     
                _reference_file = ""           
                for reference_file in reference_files:
                    acq_time_reference = self._get_acquisitiontime_from_file(filename=reference_file)
                    
                    if not acq_time_reference:
                        return
                    
                    if float(acq_time_reference) == float(self._acquisition_time):
                        self.reference_acquisition_time = float(acq_time_reference)
                        _reference_file = str(reference_file)
                        break
                    
                self.set_reference_file(reference_file=_reference_file)
            else:
                self.set_reference_file(reference_file="")
        else:
            self.set_reference_file(reference_file="")

    def set_reference_file(self, reference_file:str):
        self.reference_file = reference_file
        
    def update_data(self, data=None):
        if data is None:
            data = self._data
        
        if data is None:
            self.set_data(data=None)
            return
            
        if (self._data_reference is not None) and self._reference_factor != 0.0:
            try:
                data = self.data_cache - self._data_reference
            except Exception as e:
                logger.warning(f"Shapes of data and mask do not match!")
                data = self.data_cache
        else:
            data = self.data_cache
            
        if data is not None:
            data_clean = self._clean_data(data=data)
            self.set_data(data=data_clean)
        else:
            self.set_data(data=None)
            
    def update_new_data(self):
        filename_list = self._list_filenames
        
        if filename_list:
            data = self._open_data(list_filenames=filename_list)
        else:
            data = None
            
        self.data_cache = data
        self.update_data(data=data)

    def _open_data(self, list_filenames:list):
        if isinstance(list_filenames, str):
            list_filenames = [list_filenames]
            
        if len(list_filenames) > 1:
            data = self._average_data(list_filenames=list_filenames)
        else:
            try:
                data = fabio.open(list_filenames[0]).data
            except Exception as e:
                logger.warning(f"{list_filenames[0]} could not be opened")
                data = None
        return data
            
    def _average_data(self, list_filenames:list):
        try:
            data_avg = np.average([fabio.open(file).data for file in list_filenames], axis=0)
        except:
            logger.warning(f"{list_filenames} not valid for data average")
            data_avg = None
        return data_avg
    
    def _clean_data(self, data):
        data[data < 0.0] = 0.0
        return data
    
    def update_reference(self, reference_file=""):
        # This method sets the reference_file only
        if reference_file:
            if self._reference_file == reference_file:
                return
            else:
                self.set_reference_file(reference_file=reference_file)
        else:
            # Auto
            # If there is already data reference stored and the act time is the same, its valid
            if self._data_reference is not None and self.reference_acquisition_time == self._acquisition_time:
                return
            
            if self._acquisitiontime_key and self._acquisition_time:
                self.set_automatic_reference_file()
                
            #     if self._reference_file and self._reference_factor != 0.0:
            #         data = self._open_data(list_filenames=self._reference_file)
            #         if data is not None:
            #             print(8888)
            #             self.data_reference = data * self._reference_factor
            #         else:
            #             self.data_reference = None
            #     else:
            #         self.data_reference = None
            # else:
            #     self.data_reference
    def update_data_reference(self):
        # if self._reference_file and self._reference_factor != 0.0:
        if self._reference_file:
            data_reference = self._open_data(list_filenames=self._reference_file)
            if data_reference is not None:
                self.data_reference = data_reference * self._reference_factor
            else:
                self.data_reference = None
        else:
            self.data_reference = None
            
    def update_data_mask(self):
        if self._mask_file:
            mask_data = self._open_data(list_filenames=[self._mask_file])
            if mask_data is not None:
                self.mask_data = mask_data
    
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
        self.list_headers = list_headers
            
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
        self.update_normalization_factor()
        self.update_incident_angle()
        self.update_tilt_angle()        
        self.update_acquisition_time()

    def update_acquisition_time(self):
        if not self._list_filenames:
            return
        
        if self._acquisitiontime_key:
            acq_time = self._get_metadata_value(key=self._acquisitiontime_key)
            try:
                self.acquisition_time = float(acq_time)
            except:
                self.acquisition_time = None
            
    def update_normalization_factor(self):
        if not self._list_filenames:
            return
        
        if self._normalizationfactor_key:
            norm_factor = self._get_metadata_value(key=self._normalizationfactor_key)
            self.normalization_factor = norm_factor
            
            try:
                self.normalization_factor = float(norm_factor)
            except:
                self.normalization_factor = 1.0
            
    def update_incident_angle(self):
        if not self._list_filenames:
            return
        
        if self._incidentangle_key:
            iangle = self._get_metadata_value(key=self._incidentangle_key)
            self.incident_angle = iangle
            try:
                self.incident_angle = float(iangle)
            except:
                self.incident_angle = 0.0
            
    def update_tilt_angle(self):
        if not self._list_filenames:
            return
        
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
            validated_config= ConfigIntegrationAzimuthal.parse_obj(config).dict()
            return validated_config
        except ValidationError as e:
            logger.warning(f"{e}. Not valid config dictionary for cake integration.")
            return
            
    def validate_config_box(self, config):
        if not isinstance(config, dict):
            return
        try:
            validated_config = ConfigIntegrationBox.parse_obj(config).dict() 
            return validated_config
        except ValidationError as e:
            logger.warning(f"{e}. Not valid config dictionary for box integration.")
            return
          
    def do_integration(self, config:dict, dim:int=1):
        if self._data is None:
            return
        if self._ai:
            if self._poni:
                if dim == 1:
                    if config.get("type") in ("azimuthal", "radial"):
                        res1d = self._do_integrate1d_cake(config=config)
                    elif config.get("type") == "box":
                        res1d = self._do_integrate1d_box(config=config)
                    else:
                        res1d = None
                    return res1d
                elif dim == 2:
                    return self.do_integration2d(config=config)
                else:
                    return  
            else:
                logger.warning(f"Poni {self._poni} is not valid to integrate.")
        else:
            logger.warning(f"AI {self._ai} is not valid to integrate.")
    
    def _do_integrate1d_cake(self, config:dict):
        config_validated = self.validate_config_cake(config=config)
        if config_validated:
            if config_validated.get("type") == "azimuthal":
                res1d = self._do_integrate1d_azimuthal(config=config_validated)
            elif config_validated.get("type") == "radial":
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
                mask=self._mask_data,
                npt=config.get("npt_rad"),
                p0_range=config.get("radial_range"),
                p1_range=config.get("azimuth_range"),
                unit=config.get("unit"),
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
                mask=self._mask_data,
                npt=config.get("npt_rad"),
                p0_range=config.get("azimuth_range"),
                p1_range=config.get("radial_range"),
                unit=config.get("unit"),
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
                mask=self._mask_data,
                npt=config_box.get("npt_rad"),
                p0_range=config_box.get("p0_range"),
                p1_range=config_box.get("p1_range"),
                unit=UNIT_GI[config_box.get("output_unit")],
                normalization_factor=self._normalization_factor,
                polarization_factor=POLARIZATION_FACTOR,
            )
            return res1d
        except Exception as e:
            logger.warning(f"{e}: Box integration failed with config: {config_box}")
                
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
                  
                
    def do_integration2d(self, config:dict):
        if self._data is None:
            return
        
        config_validated = self.validate_config_cake(config=config)
        if config_validated:
            if self._ai and self._poni:
                res2d = self._do_integration2d(config=config_validated)
                return res2d
        return
        
    def _do_integration2d(self, config:dict):
        try:
            res2d = self._ai.integrate2d(
                data=self._data,
                npt_rad=config.get("npt_rad"),
                npt_azim=config.get("npt_azim"),
                radial_range=config.get("radial_range"),
                azimuth_range=config.get("azimuth_range"),
                normalization_factor=self._normalization_factor,
            )
            return res2d
        except Exception as e:
            logger.warning(f"{e}: Integrate2d failed with config: {config}")
            return
        
    def _get_json_config(self, integration_name:str):
        full_filename = INTEGRATIONS_DIRECTORY.joinpath(f"{integration_name}.json")
        with open(full_filename) as f:
            config = json.load(f)
        return config
        
    def update_integrations(self):
        if self._data is None:
            return
        
        if self._ai is None:
            return
        
        if self._configs:
            self._update_integrations(list_configs=self._configs)
        
    def _update_integrations(self, list_configs:list):
        list_results = []
        for config in list_configs:
            res1d = self.do_integration(
                config=config,
                dim=1,
            )
            if res1d:
                list_results.append(res1d)
        self.results1d = list_results
                
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