#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 14:31:00 2022

PyXScat is a tool developed by Edgar Gutierrez Fernandez, post-doctoral researcher at BM28-XMaS beamline. The European Synchrotron.
@author: edgar1993a

PyXScat is a graphical user interface, python-based, designed to visualize and handle .edf data in a straightforward way.
PyXScat allows visualization of 2D scattering maps through silx tools, reduction of data through pyFAI integration methods; it incorporates grazing incidence corrections through pygix module.

"""
__author__ = "E. Gutierrez-Fernandez"
__contact__ = "edgar.gutierrez-fernandez@esrf.fr"
__license__ = ""
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"
__version__ = "0.7"

@property
def version():
    return __version__