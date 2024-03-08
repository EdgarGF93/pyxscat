
from PyQt5.QtWidgets import QApplication
from pyxscat.gui.gui_mainwindow import GUIMainWindow
import sys

def main():
    from argparse import ArgumentParser
    description = """PyXScat tool to open the GUI"""
    usage = "pyxscat [options]"
    parser = ArgumentParser(
        usage=usage,
        description=description,
    )

    parser.add_argument(
        "-f" "--file-json",
        dest="file",
        help="Import a .json file with already stored Metadata",
        default=None,
    )

    parser.add_argument(
        "-d", "--directory",
        dest="directory",
        help="Import a root directory to search files recursively",
        default=None,
    )

    parser.add_argument(
        "-p", "--pattern",
        default="*.edf",
        dest="pattern",
        help="Use a file-matching pattern to search for data files",
    )

    parser.add_argument(
        "-n", "--normalization",
        default="",
        dest="normalization",
        help="Key to find the normalization factor in the file",
    )

    parser.add_argument(
        "-t", "--time",
        default="",
        dest="acquisition",
        help="Key to find the acquisition time in the file",
    )

    parser.add_argument(
        "-ia", "--incident",
        default="",
        dest="incident",
        help="Key to find the incident angle in the file",
    )

    parser.add_argument(
        "-ta", "--tilt",
        default="",
        dest="tilt",
        help="Key to find the tilt angle in the file",
    )
    options = parser.parse_args()

    _main(
        options=options,
    )

def _main(options):

    app = QApplication(sys.argv)
    main_window = GUIMainWindow()
    main_window.show()
    main_window._guiwidget.browser._init_browser(
        root_directory=options.directory,
        pattern=options.pattern,
        json_file=options.file,
    )
    main_window._guiwidget.browser.set_normalizationfactor_key(key=options.normalization)
    main_window._guiwidget.browser.set_acquisitiontime_key(key=options.acquisition)
    main_window._guiwidget.browser.set_incidentangle_key(key=options.incident)
    main_window._guiwidget.browser.set_tiltangle_key(key=options.tilt)


    app.exec_()    

if __name__ == "__main__":
    sys.exit(main())