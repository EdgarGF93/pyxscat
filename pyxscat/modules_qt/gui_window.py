
from . import GLOBAL_PATH_QT
from pyxscat.integrator_methods import DIRECTORY_INTEGRATIONS
from pyxscat.modules_qt.gui_widget import GUIPyX_Widget
from pyxscat.modules_qt.gui_widget_about import AboutForm
from pyxscat.modules_qt.integration_form_methods import IntegrationForm
from pyxscat.modules_qt.setup_form_methods import SetUpForm
from pyxscat.modules_qt import combobox_methods as cb
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
        app_icon.addFile(join(GLOBAL_PATH_QT, "pyxscat_icon.png"), QtCore.QSize(256,256))
        self.setWindowIcon(app_icon)

        self._guiwidget.update_combobox_setups()
        self._guiwidget.update_combobox_integrations()

    def _build_menubar(self):
        menubar = QMenuBar()
        toolsmenu = QMenu("&Tools", self)
        aboutmenu = QMenu("&About", self)
        menubar.addMenu(toolsmenu)
        menubar.addMenu(aboutmenu)
            
        setupaction = QAction("&Add setup", self)
        integrationaction = QAction("&Add integration", self)
        aboutaction = QAction("&About PyXScat", self)

        setupaction.triggered.connect(
            lambda : (
                self._open_setup_form(),
            )
        )

        integrationaction.triggered.connect(
            lambda : (
                self._open_integration_form(),
            )
        )

        aboutaction.triggered.connect(
            lambda : (
                self._open_about_form(),
            )
        )

        toolsmenu.addAction(setupaction)
        toolsmenu.addAction(integrationaction)
        aboutmenu.addAction(aboutaction)
        self.setMenuBar(menubar)

    def _open_setup_form(self):
        self.setup_form = SetUpForm()
        self.setup_form.show()
        self.setup_form.button_input_setup.clicked.connect(self._guiwidget.update_combobox_setups) 

    def _open_integration_form(self):
        self.integration_form = IntegrationForm()
        self.integration_form.show()
        self.integration_form.button_azrad_add.clicked.connect(self._guiwidget.update_combobox_integrations)
        self.integration_form.button_proj_add.clicked.connect(self._guiwidget.update_combobox_integrations) 
              

    def _open_about_form(self):
        self.about_form = AboutForm()
        self.about_form.show()

    # def update_combobox_integrations(self):
    #     """
    #         Feed the combobox with the dictionary of integrations
    #     """
    #     cb.insert_list(
    #         combobox=self._guiwidget.combobox_integration,
    #         list_items=[
    #             d['Name'] for d in self.get_dictionaries_integration()
    #         ],
    #         reset=True,
    #     )

    def get_dictionaries_integration(self) -> list:
        """
            Return a list with the dictionaries of all the available integrations
        """
        import json
        list_dicts = []
        for file in os.listdir(DIRECTORY_INTEGRATIONS):
            if file.endswith('json'):
                with open(join(DIRECTORY_INTEGRATIONS, file), 'r') as fp:
                    list_dicts.append(
                        json.load(fp)
                    )
        return list_dicts