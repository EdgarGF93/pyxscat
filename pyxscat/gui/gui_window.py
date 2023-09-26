
from . import ICON_DIRECTORY
from pyxscat.gui.gui_widget_alternative import GUIPyX_Widget
from pyxscat.gui.gui_widget_about import AboutForm


from PyQt5.QtWidgets import QMainWindow, QMenu, QMenuBar, QAction
from PyQt5 import QtGui, QtCore

PYXSCAT_LOGO = "pyxscat_icon.png"
WIDTH = 1280
HEIGHT = 720

class GUIPyX_Window(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self._build_menubar()
        self._guiwidget = GUIPyX_Widget()
        self.setCentralWidget(self._guiwidget)
        self.setWindowTitle("PyXScat")

        self.setMinimumWidth(WIDTH)
        self.setMinimumHeight(HEIGHT)

        app_icon = QtGui.QIcon()
        icon_path = str(ICON_DIRECTORY.joinpath(PYXSCAT_LOGO))
        app_icon.addFile(icon_path, QtCore.QSize(256,256))
        self.setWindowIcon(app_icon)

        self._guiwidget.update_combobox_h5()
        self._guiwidget.update_combobox_metadata()
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