
from PyQt5.QtWidgets import QApplication
from pyxscat.gui.gui_window import GUIPyXMWindow
from pyxscat.gui.gui_widget import ICON_SPLASH
import pyxscat
from pathlib import Path
from PIL import Image

import argparse
import os
import pytest
import sys
# Open the GUI
CATO = '''
                                                                           
                                               .(@@@@@@#.                  
                                          .@@@@@@@@@@@@@@@@@@.             
                                        #@@@@@@@@#/**(@@@@@@@@@*        .  
                                      .@@@@@@.           .@@@@@@@          
                                      @@@@@.               .@@@@@@         
                                      @@@@                  /@@@@@,        
                                                            .@@@@@(        
                                                            (@@@@@*        
                                                            @@@@@@         
      (@(                                                 *@@@@@@*         
       @@@@@@#                                          *@@@@&#&%          
     @@@@@@@@@@@@*                                 .(@@#@@#&@%#(  . .    . 
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@(@#%@#%(%@&(#%*        ... 
   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@(###((@@((&@@%(#@@@@        ..... 
   *@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@              .
          *@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@               
           ,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#(((#%&&&&&&%           ...
             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#&@@&%&@&#%@@@,       ..   
               .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#@&(&@%# .     . ..
                  (@@@@@@@@*               ,@@@@@@@@@@@@@@@@@@@(% .   .  ..
                   @@@@@@.                   *@@@@@@@*./&@@@@@@@@(       ..
                   @@@@@.                     ,@@@@@@        @@@@&       ..
                  *@@@@                       &@@@@*          @@@&        .
               .@@@@@@                    @@@@@@&           #@@@@/        .
                ***.                      ,**,              ,//,        .. 
'''



TEST_H5_FILE = Path(pyxscat.__file__).parent.joinpath('test', 'test_h5.py')
TEST_GUI_FILE = Path(pyxscat.__file__).parent.joinpath('test', 'test_gui.py')



def run(argv=None):


    if argv is None:
        argv=sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="PyXScat Software", 
        prog="pyxscat",
    )
    # parser.add_argument('cosas', help='CUAN GRITAN ESOS MALDITOS')
    subparsers = parser.add_subparsers(help='commands', dest='command')

    test_h5_parser = subparsers.add_parser('test_h5', help='Run the test method for H5Integrator')
    test_gui_parser = subparsers.add_parser('test_gui', help='Run the test method for GUI')
    logo_parser = subparsers.add_parser('logo', help='Show the logo of PyXScat')

    args = parser.parse_args(args=argv)

    if args.command == 'test_h5':
        exit_code = pytest.main(["-v", TEST_H5_FILE])
        return exit_code
    elif args.command == 'test_gui':
        exit_code = pytest.main(["-v", TEST_GUI_FILE])
        return exit_code
    elif args.command == 'logo':
        with Image.open(ICON_SPLASH) as img:
            img.show()
    else:
        app = QApplication(sys.argv)
        main_window = GUIPyXMWindow()
        main_window.show()
        print(CATO)         
        app.exec_()

        # print(f"Unrecognized command: {args.command}")
        # parser.print_help()

if __name__ == "__main__":
    sys.exit(run())