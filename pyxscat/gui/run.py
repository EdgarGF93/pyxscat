
from PyQt5.QtWidgets import QApplication
from pyxscat.gui.gui_window import GUIPyXMWindow
from pyxscat.gui.gui_widget import ICON_SPLASH
import pyxscat
from pathlib import Path
from PIL import Image
from pyxscat.other.other_functions import date_prefix

import argparse
import os
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
TEST_TIME_FILE = Path(pyxscat.__file__).parent.joinpath('test', 'test_time.py')


def _main(argv=None):
    import pytest


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
    test_time = subparsers.add_parser('test_time', help='Time the H5 methods')    
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
    elif args.command == 'test_time':
        exit_code = pytest.main(["--profile-svg", "-v", TEST_H5_FILE])
        prof_folder = Path(os.getcwd()).joinpath('prof')
        svg_folder = Path(os.getcwd()).joinpath('prof_svg')
        svg_folder.mkdir(exist_ok=True)
        
        prof_file = str(prof_folder.joinpath('combined.prof'))
        dp = date_prefix()
        out_dot = str(svg_folder.joinpath(f'profile_{dp}.dot'))
        out_png = str(svg_folder.joinpath(f'profile_{dp}.png'))

        os.system(f'gprof2dot -f pstats --node-label total-time "{prof_file}" -o "{out_dot}"')
        os.system(f'dot -Tpng "{out_dot}" -o "{out_png}"')
        return exit_code
    else:
        run()
        # print(f"Unrecognized command: {args.command}")
        # parser.print_help()

def main():
    run()

def run():
    app = QApplication(sys.argv)
    main_window = GUIPyXMWindow()
    main_window.show()
    print(CATO)         
    app.exec_()


if __name__ == "__main__":
    sys.exit(main())