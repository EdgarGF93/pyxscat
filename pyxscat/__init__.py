#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 14:31:00 2022

@author: edgar1993a
"""

# This is a project to manage .edf files. You can plot a result, plot an image with fabio, integrate in batch mode with pyFAI and many other methods.

# First of all, you have to create a .json file that includes all the names of the files you want to analyse and a .poni file, previously generated with pyFAI-calib2 GUI.

# This script will open two jupyter notebooks in the web browser, one is to create the json file, and the second one is to manage the data.

__author__ = "E. Gutierrez-Fernandez"
__contact__ = "edgar.gutierrez-fernandez@esrf.fr"
__license__ = ""
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"
__version__ = "0.3"

@property
def version():
    return __version__


