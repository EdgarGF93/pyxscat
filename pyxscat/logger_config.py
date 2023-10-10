import logging
import logging.config
from logging.handlers import RotatingFileHandler
from pyxscat.gui import LOGGER_PATH
from pyxscat.other.other_functions import date_prefix
import datetime

def setup_logger():

    if not LOGGER_PATH.exists():
        LOGGER_PATH.mkdir()

    cleanup_old_logs()

    logger = logging.getLogger('PyXScatLogger')

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        log_filename = LOGGER_PATH.joinpath(f'pyxscat_logger_{date_prefix()}.log')
        handler = RotatingFileHandler(
           log_filename,
           maxBytes=10*1024*1024,
           backupCount=3,
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger

def cleanup_old_logs(log_dir=LOGGER_PATH, retention_days=14):
    now = datetime.datetime.now()
    for log_file in log_dir.glob('*.log'):
        file_mod_time = datetime.datetime.fromtimestamp(log_file.stat().st_mtime)
        if (now.day - file_mod_time.day) > retention_days:
            log_file.unlink()