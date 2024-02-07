
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
    options = parser.parse_args()

    _main(
        directory=options.directory,
        pattern=options.pattern,
        file_json=options.file,
    )

def _main(directory="", pattern="*.edf", file_json=""):

    app = QApplication(sys.argv)
    main_window = GUIMainWindow()
    main_window.show()
    main_window._guiwidget.browser._init_browser(
        root_directory=directory,
        pattern=pattern,
        json_file=file_json,
    )    
    app.exec_()    

if __name__ == "__main__":
    sys.exit(main())