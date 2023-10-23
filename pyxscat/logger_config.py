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
    logger.setLevel(logging.WARNING)
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_filename = LOGGER_PATH.joinpath(f'pyxscat_logger_{date_prefix()}.log')

    if not logger.handlers:



        # logging_config = {
        #     "version": 1,
        #     'disable_existing_loggers': False,
        #     "formatters": {
        #         'standard': {
        #             'format': log_formatter
        #         }
        #     },
        #     "handlers": {
        #         'default': {
        #             'class': 'logging.StreamHandler',
        #             'formatter': 'standard',
        #             'level': logging.INFO,
        #             'stream': 'ext://sys.stdout'
        #         },
        #         'file': {
        #             'class': 'logging.handlers.TimedRotatingFileHandler',
        #             'when': 'midnight',
        #             'utc': True,
        #             'backupCount': 5,
        #             'level': logging.DEBUG,
        #             'filename': log_filename,
        #             'formatter': 'standard',
        #         },
        #     },
        #     "loggers": {
        #         "": {
        #             'handlers': ['default', 'file'],
        #             'level': logging.DEBUG,
        #         },
        #     }
        # }

        # logging.config.dictConfig(logging_config)






        # Console Handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)        
        stream_handler.setLevel(logging.WARNING)

        # File Handler

        file_handler = RotatingFileHandler(
           log_filename,
           maxBytes=10*1024*1024,
           backupCount=10,
        )
        file_handler.setFormatter(log_formatter)        
        file_handler.setLevel(logging.WARNING)

        logger.addHandler(stream_handler)        
        logger.addHandler(file_handler)

    return logger

def cleanup_old_logs(log_dir=LOGGER_PATH, retention_days=14):
    now = datetime.datetime.now()
    for log_file in log_dir.glob('*.log'):
        file_mod_time = datetime.datetime.fromtimestamp(log_file.stat().st_mtime)
        if (now.day - file_mod_time.day) > retention_days:
            log_file.unlink()
