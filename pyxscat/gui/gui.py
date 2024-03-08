from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, pyqtSignal

from . import ICON_DIRECTORY
from pyxscat.gui.guilayout import GUILayout
from pyxscat.logger_config import setup_logger
from pyxscat.gui.data_handler import DataHandler

from pathlib import Path
import sys

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
        # self.browser.active_files_changed.connect(self.update_all_graphs)
        # self.browser.new_files_detected.connect(self._update_new_files)
        
        self.browser.data_changed.connect(self.update_all_graphs)
        # self.browser.data_changed.connect(self.update_cb_reference_file)
        self.browser.update_integrations.connect(self.update_graph_integration)
    
    def update_cb_reference_file(self):
        reference_file = self.browser.data_handler._reference_file
        reference_file = str(Path(reference_file).name)
        self.browser.combobox_reference_file.setCurrentText(reference_file)
    
    def update_data(self, raw=False, reshape=False, qmap=False, integration=False):
        if self.browser.data_handler._data is None:
            return
        if raw:
            self.update_graph_raw()
        if integration:
            self.update_graph_integration()
            
    def update_all_graphs(self):
        self.update_data(
            raw=True,
            reshape=True,
            qmap=True,
            integration=True,
        )

    def update_graph_raw(self):
        data = self.browser.data_handler._data
        self.graphs._update_raw_graph(data=data)    

    def update_graph_integration(self):
        results = self.browser.data_handler._results1d
        self.graphs._update_integration_graph(results=results)

    def _update_new_files(self):
        pass
    



def main():
    app = QApplication(sys.argv)
    mw = QMainWindow()
    gui = GUI()
    mw.setCentralWidget(gui)
    mw.show()
    app.exec_()





if __name__ == "__main__":
    main()