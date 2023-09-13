#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 14:31:00 2022

PyXScat is a tool developed by Edgar Gutierrez Fernandez, post-doctoral researcher at BM28-XMaS beamline. The European Synchrotron.
@author: edgar1993a

PyXScat is a graphical user interface, python-based, designed to visualize and handle .edf data in a straightforward way.
PyXScat allows visualization of 2D scattering maps through silx tools, reduction of data through pyFAI integration methods; it incorporates grazing incidence corrections through pygix module.

"""
from pathlib import Path
PATH_TOML = Path(".").parent.joinpath("pyproject.toml")

__author__ = "E. Gutierrez-Fernandez"
__contact__ = "edgar.gutierrez-fernandez@esrf.fr"
__license__ = ""
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"

def version():
    with open(PATH_TOML, 'r') as f:
        for line in f.readlines():
            if 'version' in line:
                return line.split()[-1]

__version__ = version()