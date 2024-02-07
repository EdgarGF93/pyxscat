from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, pyqtSignal

from . import ICON_DIRECTORY
from pyxscat.gui.guilayout import GUILayout
from pyxscat.logger_config import setup_logger

from pathlib import Path
import sys
import fabio
import numpy as np

ICON_SPLASH = str(Path(ICON_DIRECTORY).joinpath('pyxscat_new_logo.png'))

logger = setup_logger()
def log_info(func):
    def wrapper(*args, **kwargs):
        logger.debug(f'_________OPEN FUNCTION: {func.__name__}_________')
        return func(*args, **kwargs)
    return wrapper


class GUI(GUILayout):
    """
    Class to create a GUI widget, with methods and callbacks
    """
    def __init__(self):
        super(GUI, self).__init__()
        logger.debug("GUIPyX_Widget was created.")

        self._splash()
        self._init_connections()

    def _splash(self):
        pixmap = QPixmap(ICON_SPLASH)
        splash = QSplashScreen(pixmap)
        splash.show()
        splash.finish(self)

    def _init_connections(self):
        self.browser.browser_index.connect(self._update_graphs)
        self.browser.poni_changed.connect(self._update_graphs)
        self.browser.new_files_detected.connect(self._update_new_files)
    
    def _update_graphs(self, raw=True, reshape=True, q=True, integration=True):
        list_filenames = self.browser.get_active_filenames()
        if not list_filenames:
            return
        data = self._open_data(list_filenames=list_filenames)

        if raw:
            z_lims = self.weak_lims(data=data)
            self.graphs._update_raw_graph(data=data, z_lims=z_lims)
        
        if integration:
            res = self.browser.ai.integrate1d(data=data, npt=1000)
            self.graphs._update_integration_graph(result=res)
            
    def _update_new_files(self):
        print(f"new file: {self.browser._event_handler.new_files}")

    def _open_data(self, list_filenames:list):
        if len(list_filenames) > 1:
            data = self._average_data(list_filenames=list_filenames)
        else:
            data = fabio.open(list_filenames[0]).data
        return data

    def _average_data(self, list_filenames:list):
        return np.mean([fabio.open(file).data for file in list_filenames], axis=2)

    def weak_lims(self, data):
        mn = np.nanmean(data)
        sd = np.nanstd(data)
        return (mn+0*sd, mn+3*sd)



def main():
    app = QApplication(sys.argv)
    mw = QMainWindow()
    gui = GUI()
    mw.setCentralWidget(gui)
    mw.show()
    app.exec_()





if __name__ == "__main__":
    main()