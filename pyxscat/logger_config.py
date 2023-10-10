import logging
import logging.config
from pyxscat.gui import LOGGER_PATH
from pyxscat.other.other_functions import date_prefix

def setup_logger():

    if not LOGGER_PATH.exists():
        LOGGER_PATH.mkdir()

    logger = logging.getLogger('PyXScatLogger')

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(LOGGER_PATH.joinpath(f'pyxscat_logger_{date_prefix()}.log'))
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger

