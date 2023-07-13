
from . import GUI_PATH
# from pyxscat.other.integrator_methods import DIRECTORY_INTEGRATIONS
# from pyxscat.gui.gui_widget import GUIPyX_Widget
# from pyxscat.gui.gui_widget_about import AboutForm

# from other.integrator_methods import DIRECTORY_INTEGRATIONS
from gui.gui_widget import GUIPyX_Widget
from gui.gui_widget_about import AboutForm


from PyQt5.QtWidgets import QMainWindow, QMenu, QMenuBar, QAction
from PyQt5 import QtGui, QtCore
from os.path import join
import os

class GUIPyX_Window(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self._build_menubar()
        self._guiwidget = GUIPyX_Widget()
        self.setCentralWidget(self._guiwidget)
        self.setWindowTitle("PyXScat")

        app_icon = QtGui.QIcon()
        icon_path = str(GUI_PATH.joinpath("pyxscat_icon.png"))
        app_icon.addFile(icon_path, QtCore.QSize(256,256))
        self.setWindowIcon(app_icon)

        self._guiwidget.update_combobox_h5()
        self._guiwidget.update_combobox_setups()
        self._guiwidget.update_integration_widgets()

    def _build_menubar(self):
        menubar = QMenuBar()
        aboutmenu = QMenu("&About", self)
        menubar.addMenu(aboutmenu)
            

        aboutaction = QAction("&About PyXScat", self)
        aboutaction.triggered.connect(
            lambda : (
                self._open_about_form(),
            )
        )

        aboutmenu.addAction(aboutaction)
        self.setMenuBar(menubar)

    def _open_about_form(self):
        self.about_form = AboutForm()
        self.about_form.show()

    # def get_dictionaries_integration(self) -> list:
    #     """
    #         Return a list with the dictionaries of all the available integrations
    #     """
    #     import json
    #     list_dicts = []
    #     for file in os.listdir(DIRECTORY_INTEGRATIONS):
    #         if file.endswith('json'):
    #             with open(join(DIRECTORY_INTEGRATIONS, file), 'r') as fp:
    #                 list_dicts.append(
    #                     json.load(fp)
    #                 )
    #     return list_dicts