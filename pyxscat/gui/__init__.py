from pathlib import Path

GUI_PATH = Path(__file__).parent
SRC_PATH = GUI_PATH.parent
GLOBAL_PATH = SRC_PATH.parent
LOGGER_PATH = GLOBAL_PATH.joinpath('logger')
INTEGRATION_PATH = SRC_PATH.joinpath('integration_dicts')
SETUP_PATH = SRC_PATH.joinpath('setup_dicts')
SYMBOL_CHECK = '\u2705'
SYMBOL_X = '\u274C'
SEPARATOR_CONDITIONS = ','
SEPARATOR_LINEEDIT = ','
INTERVAL_SEARCH_DATA = 1000
OUTPUT_FOLDER = 'PyXScat'
BASH_FILE_1S = 'last_file_1s.sh'
BASH_FILE_NOTIME = 'last_file_notime.sh'
ERROR_OS = "Unkown operating system."
PLOT_SELECTED_TABLE = False
ROTATED_ERROR = 'Error on arrays shape correspondende. Check rotation.'
DEFAULT_UNIT = 'q_nm^-1'