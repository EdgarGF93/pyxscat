
from . import ICON_PATH
from pyxscat.gui.gui_widget import GUIPyX_Widget
from pyxscat.gui.gui_widget_about import AboutForm


from PyQt5.QtWidgets import QMainWindow, QMenu, QMenuBar, QAction
from PyQt5 import QtGui, QtCore

PYXSCAT_LOGO = "pyxscat_icon.png"

class GUIPyX_Window(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self._build_menubar()
        self._guiwidget = GUIPyX_Widget()
        self.setCentralWidget(self._guiwidget)
        self.setWindowTitle("PyXScat")

        app_icon = QtGui.QIcon()
        icon_path = str(ICON_PATH.joinpath(PYXSCAT_LOGO))
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