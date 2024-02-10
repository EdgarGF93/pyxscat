from pathlib import  Path
from pyFAI import load
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
from pygix.transform import Transform
from pyFAI.io.ponifile import PoniFile
import logging
import numpy as np
import fabio
from pydantic import BaseModel, ValidationError, confloat, constr, conlist
from pyxscat.edf import FullHeader

logger = logging.getLogger(__name__)




# Define a Pydantic model
class ConfigIntegration(BaseModel):
    name: str
    suffix: str
    unit : str
    radial_range: list
    azimuth_range : list
    azim_bins : int
    integration : str



class DataHandler(Transform):
    def __init__(
        self, 
        filename_list:list=[], 
        ai:AzimuthalIntegrator=None, 
        poni:PoniFile=None, 
        config:dict=None,
        ):
        super().__init__()
        
        self.list_filenames = filename_list
        self.list_headers = []
        self.ai = ai
        self.poni = poni
        self.config = config
        self.geo = None
        
        self.acquisitiontime_key = ""
        self.normalizationfactor_key = ""
        self.incidentangle_key = ""
        self.tiltangle_key = ""
        
        self.acquisition_time = None
        self.normalization_factor = 0.0
        self.incident_angle = 0.0
        self.tilt_angle = 0.0
        
        self.reference_directory = ""
        self.reference_file = ""
        self.reference_acquisition_time = None
        self.pattern = "*.edf"
        
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
            if self._ai:
                if self._ai.detector.shape == value:
                    self._data = value
                else:
                    logger.warning(f"shape of value is {value.shape}, different from detector shape: {self._ai.detector.shape}!")
            else:
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
    def config(self):
        return self._config
    
    @config.setter
    def config(self, value):
        if not isinstance(value, dict):
            return
        try:
            validated_config = ConfigIntegration.parse_obj(value)
            self._config = validated_config
        except ValidationError as e:
            logger.warning(f"{e}. Not valid config dictionary.")

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
        self.normalization_factor = key

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
                    return
        self._data_reference = ""
                    
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
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    def do_integration(self, config:dict):
        self.config = config
        
        if self._config:
            self._do_integrate1d()
    
    def _do_integrate1d(self):
        try:
            res1d = self._ai.integrate1d(
                data=self._data,
                npt=self._config["azim_bins"],
                
            )
            self.res1d = res1d
        except:
            pass
            
        
        
