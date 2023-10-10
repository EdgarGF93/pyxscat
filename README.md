# PyXScat



## Description of the project

PyXScat is a module that allows a quick, straightforward visualization and reduction of 2D scattering patterns.
The main tool of PyXScat is its Graphical User Interface. The philosophy of PyXScat matches the following point:<br />
    - Abstraction of FabIO, pyFAI and pygix. Visualization of 2D patterns, 1D integrations, transform to reciprocal (Q) maps.<br />
    - Minimum learning curve for non-experienced users.<br />
    - Live, tunable and quick subtraction of reference data.<br />
    - Bridge between data collection and deep data analysis.<br />

<br />
![alt text](https://gitlab.esrf.fr/xmas-bm28/data_analysis/pyxscat/-/raw/main/Tutorial/PyXScat_screenshot.png)
<br /><br />
![alt text](https://gitlab.esrf.fr/xmas-bm28/data_analysis/pyxscat/-/raw/main/Tutorial/PyXScat_screenshot_4.png)
<br /><br />
![alt text](https://gitlab.esrf.fr/xmas-bm28/data_analysis/pyxscat/-/raw/main/Tutorial/PyXScat_screenshot_3.png)
<br /><br />
![alt text](https://gitlab.esrf.fr/xmas-bm28/data_analysis/pyxscat/-/raw/main/Tutorial/PyXScat_screenshot_2.png)

<br />


## 0) From scratch using conda environment
```
conda create --name my_env
conda activate my_env
conda install python=3.10
```

# Install using clone
## 1) Clone the project into your directory (e.g. /user/Python/)

```
cd /user/Python
git clone -b main_matplotlit_3 https://gitlab.esrf.fr/xmas-bm28/data_analysis/pyxscat.git
```

## 2) Install locally the package, including all its sub-packages
```
cd pyxscat
pip install -e .
```

# Install through requirements.txt

## 1) Download the requirements.txt file from the GitLab

## 2) Go to your python destinated directory and install the required packages (where the requirements.txt is stored)
```
cd /user/Python
pip install -r requirements.txt
```

# Run pyxscat

## 1) Once the module is installed in the path of your environment, open the GUI:
```
pyxscat
```

## 2) Tutorial of the GUI. You have a .ppt file in the PyXScat folder, to learn a minimum set of steps to start handlind your data:
```
Tutorial/pyxscat_tutorial.ppt
```
<!-- ## 5) The fundamental steps are summarized in the following video:

![](Tutorial/PyXSCat_steps.mp4) -->
