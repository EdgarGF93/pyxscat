# PyXScat



## Description of the project

PyXScat is a module that allows a quick, straightforward visualization and reduction of 2D scattering patterns.
The main tool of PyXScat is its Graphical User Interface. The philosophy of PyXScat matches the following point:
    - Minimum learning curve for non-experienced users.
    - Live, tunable and quick subtraction of reference data.
    - Bridge between data collection and deep data analysis.
    - Abstraction of FabIO, pyFAI and pygix.

![alt text](https://gitlab.esrf.fr/xmas-bm28/data_analysis/pyxscat/-/raw/main/PyXScat_screenshot.png)




## 1) Clone the project into your directory (e.g. /user/Python/)

```
cd /user/Python
git clone https://gitlab.esrf.fr/xmas-bm28/data_analysis/pyxscat.git
```

## 2) Once you have clone the project into your directory, install the module into your environment (conda, etc):
```
pip install .
```

## 3) Once the module is installed in the path of your environment, open the GUI:
```
python pyxscat/gui.py
```

## 4) Tutorial of the GUI. You have a .ppt file in the PyXScat folder, to learn a minimum set of steps to start handlind your data:
```
pyxscat/pyxscat_tutorial.ppt
```


