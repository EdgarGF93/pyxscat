import json
import matplotlib.pyplot as plt
import numpy as np
import os
from os.path import join, exists
from os import mkdir
from os.path import getmtime as gettm
from datetime import datetime

messages = ['ALL ANIMALS CAN SCREAM',
            'EN ESTE PUEBLO HAY VERDADERA DEVOCIÓN POR FULKNER',
            'HOY TENGO CUERPO DE GÓNGORA',
            'CALABAZA, YO TE LLEVO EN EL CORAZÓN',
            ]

def print_percent_done(index, total, bar_len=50, title='Processing'):
    '''
    index is expected to be 0 based index. 
    0 <= index < total
    '''
    # print(f"{index},{total}")
    percent_done = (index)/total*100
    percent_done = round(percent_done, 1)

    done = round(percent_done/(100/bar_len))
    togo = bar_len-done

    done_str = '█'*int(done)
    togo_str = '░'*int(togo)

    prog_bar = f'\u231B{title}: [{done_str}{togo_str}] {percent_done}% done'

    if round(percent_done) == 100:
        prog_bar = f'\u2705{title}: [{done_str}{togo_str}] {percent_done}%'

    return prog_bar

def mergeDictionary(dict_1, dict_2):
   dict_3 = {**dict_1, **dict_2}
   for key, value in dict_3.items():
       if key in dict_1 and key in dict_2:
               dict_3[key] = [value , dict_1[key]]
   return dict_3

def value_from_dict(dictionary, number):
    keys = list(dictionary.keys())
    return dictionary[keys[number]]

# Input a list of file path, return the last created
def last_file_ng(ls):
    list_times = [os.path.getmtime(file) for file in ls]
    max_time = max(list_times)
    ind = list_times.index(max_time)
    return ls[ind]

def last_file(directory, conds):
    tm_cache = 0
    for file, tm in iterator_files(directory, conds):
        if tm > tm_cache:
            tm_cache, last_file = tm, file
    return last_file

def iterator_files(directory, conds):
    for (root,__,files) in os.walk(directory):
        for file in files:
            if all(cond in file for cond in conds):
                fullname = join(root,file)
                yield fullname, gettm(fullname)


def create_figure():
    plt.figure(figsize=(5,5), dpi=100)


def dict_to_str(dictionary):
        space = '*'*100
        str_ = f'{space}\n'
        for key, value in dictionary.items():
            str_ += f'{str(key)} = {str(value)} \n'
        str_ += f'{space}\n'
        return str_


# Return a ROI from a numpy array, lim is a list with four coordinates: [limx1, limx2, limy1, limy2]
def np_roi(data, lim, roi=False) -> np.array:
    if roi:
        data = data[lim[0]:lim[1],lim[2]:lim[3]]
    else:
        pass
    return data

# Return a numpy array, after logarithm base 10
def np_log(data, log=False) -> np.array:
    if log:
        data[data <=0] =  1
        data = np.log10(data)
        data[data == -np.nan] = 0
        data[data == -np.inf] = 0
    else:
        pass
    return data

# Return the weak peak limits of a numpy array
def np_weak_lims(data, min=0, max=3, weak_lims=True) -> np.array:
    if weak_lims:
        data[data < 0] = np.nan
        mn = np.nanmean(data)
        sd = np.nanstd(data)
    else:
        pass
    return (mn+min*sd, mn+max*sd)

def save_run_parameters(main_dir, conditions=['.edf'], ponifile='', reference=''):
    """
    Save a json file with a dictionary and the parameters needed to run the live Dashboard
    """
    
    save_folder = join(main_dir, 'pyxscat')
    name_run_parameters = join(save_folder, 'run_parameters.json')

    dict_run_parameters = {
        'Directory':main_dir,
        'Conditions':conditions,
        'Ponifile':ponifile,
        'Reference':reference,
    }

    if exists(save_folder):
        pass
    else:
        mkdir(save_folder)
    
    with open(name_run_parameters, 'w') as fp:
        json.dump(dict_run_parameters, fp)

def date_prefix():
    return f"{(now := datetime.now()).year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}"

def create_folder(folder_name):
    if exists(folder_name):
        return
    else:
        mkdir(folder_name)

def add_value_ifnot(value, default_value):
    if value:
        return value
    else:
        return default_value

def open_json(json_file=str()) -> dict:
    """
        Return a dictionary after importing a json file
    """
    if exists(json_file):
        import json
        return json.load(json_file)
    else:
        return
