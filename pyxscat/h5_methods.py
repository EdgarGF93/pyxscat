from collections import defaultdict
from datetime import datetime
from pathlib import Path

import fabio
import h5py
import json
import numpy as np

DESCRIPTION_HDF5 = "HDF5_XMaS_Beamline"
COMMENT_NEW_FILE = ""

def date_prefix():
    return f"{(now := datetime.now()).hour:02d}:{now.minute:02d}:{now.second:02d}_{now.day:02d}-{now.month:02d}-{now.year}"

def int_float_str(value=str()):
        try:
            return int(value)
        except:
            pass
        try:
            return float(value)
        except:
            pass
        return str(value)


class H5_container():
    """
    Creates an HDF5 and provides methods to read/write the file following the hierarchy of XMaS-BM28 
    """

    def __init__(self, filename_h5=str(), description=DESCRIPTION_HDF5, comment=COMMENT_NEW_FILE) -> None:

        if Path(filename_h5).exists:
            self._file_h5 = filename_h5
            self.create_h5_file(
                file_name=self._file_h5,
                description=description,
                comment=comment,
            )
        else:
            return

    def create_h5_file(self, file_name=str(), description=DESCRIPTION_HDF5, comment=COMMENT_NEW_FILE, **kwargs):
        """
        Creates a new .h5 file, after a file path and some attributes
        """
        f = h5py.File(file_name, 'w')
        f.attrs['Description'] = description
        f.attrs['Datetime'] = date_prefix()
        f.attrs['Comment'] = comment
        for k,v in kwargs.items():
            f.attrs[k] = v
        f.close()
        
    def update_setup_keys(self, iangle_key=str(), exposure_key=str(), norm_key=str(), tilt_key=str()):
        with h5py.File(self._file_h5, 'r+') as f:
            f.attrs['iangle_key'] = iangle_key
            f.attrs['exposure_key'] = exposure_key
            f.attrs['norm_key'] = norm_key
            f.attrs['tilt_key'] = tilt_key
            
    def h5_new_sample(self, sample_index=int(), digits=3, name=str(), printable=True):
        with h5py.File(self._file_h5, 'r+') as f:
                
            sample_name = self.get_sample_name(sample_index, digits)
            
            if f.__contains__(sample_name):
                if printable:
                    return f"The group {sample_name} already exists. Returns."
                else:
                    return
                
            f.create_group(sample_name)
            f[sample_name].attrs['Class'] = 'Sample'
            f[sample_name].attrs['Index'] = int(sample_index)
            f[sample_name].attrs['Datetime'] = date_prefix()
            f[sample_name].attrs['Name'] = name
            
            if printable:
                return f"The group {sample_name} was created successfully."        
            
    def h5_new_scan(self, scan_address=str(), sample_index=int(), digits_sample=3, scan_index=int(), digits_scan=3, name=str(), printable=True):
        with h5py.File(self._file_h5, 'r+') as f:
            
            if not scan_address:
                scan_address = self.get_scan_address(sample_index, digits_sample, scan_index, digits_scan)
            
            if f.__contains__(scan_address):
                if printable:
                    return f"The group {scan_address} already exists. Returns."
                else:
                    return
                
            f.create_group(scan_address)
            f[scan_address].attrs['Class'] = 'Scan'
            f[scan_address].attrs['Scan Index'] = int(scan_index)
            f[scan_address].attrs['Sample Index'] = int(sample_index)
            f[scan_address].attrs['Datetime'] = date_prefix()
            f[scan_address].attrs['Name'] = name
        
            if printable:
                return f"The group {scan_address} with subgroups Scan_info, Metadata, Filenames and Data were created successfully."     
            
    def get_sample_name(self, sample_index=int(), digits_sample=3):
        return f"sample_{str(sample_index).zfill(digits_sample)}"
        
    def get_scan_name(self, scan_index=int(), digits_scan=3):
        return f"scan_{str(scan_index).zfill(digits_scan)}"

    def get_scan_address(self, sample_index=int(), digits_sample=3, scan_index=int(), digits_scan=3):
        sample_name = self.get_sample_name(sample_index, digits_sample)
        scan_name = self.get_scan_name(scan_index, digits_scan)
        return f"{sample_name}/{scan_name}"

    def merge_dictionaries(list_dicts=[]):
        merge_dict = defaultdict(list)
        for d in list_dicts:
            for key in d.keys():
                merge_dict[key].append(d[key])
        return merge_dict

    def folder_to_scan(self, folder_path=str(), wildcards='*.edf', sample_index=int(), digits_sample=3, scan_index=int(), digits_scan=3, save_data=True):
        """
        Search files inside folder, filtered with wildcards and wrap them into a scan inside h5 file
        
        """
        scan_address = self.get_scan_address(sample_index, digits_sample, scan_index, digits_scan)
        with h5py.File(self._file_h5, 'r+') as f:
            
            if not f.__contains__(scan_address):
                self.h5_new_scan(
                    scan_address=scan_address,
                )
        
            filenames_list = [str(item) for item in Path(folder_path).glob(wildcards)]    
            merge_dataset, merge_metadata = self.wrap_files(filenames_list, save_data)
        
            f[scan_address].create_dataset('Data', data=merge_dataset)
            f[scan_address].create_dataset('Metadata_str', data=json.dumps(merge_metadata).encode('utf-8'))
            f[scan_address].create_group('Metadata')
            for key,value in merge_metadata.items():
                try:
                    f[scan_address]['Metadata'].create_dataset(key, data=np.array(value))
                except:
                    pass
            
    def wrap_files(self, filenames=[], save_data=True):
        length = len(list(filenames))
        merge_dataset = np.array([])
        merge_header = defaultdict(list)
        
        for index_file, (data, header) in enumerate(self.generator_fabio_data_header(filenames, save_data)):
            
            if index_file == 0:
                merge_dataset = np.empty((length, data.shape[0], data.shape[1]))
                
                
            
            merge_dataset[index_file,:,:] = data
            for key,value in header.items():
                value = int_float_str(value)
                merge_header[key].append(value)

        return merge_dataset, merge_header

    def generator_fabio_data_header(self, filenames=[], generate_data=True):
        for file in filenames:
            with fabio.open(file) as edf:
                if generate_data:
                    yield edf.data, edf.header
                else:
                    yield np.empty((1,1)), edf.header