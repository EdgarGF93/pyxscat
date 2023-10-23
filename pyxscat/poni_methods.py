from pyFAI.io.ponifile import PoniFile
from pathlib import Path

from pyxscat.logger_config import setup_logger
logger = setup_logger()

def logger_info(func):
    def wrapper(*args, **kwargs):
        logger.info(f'We entered into function: {func.__name__}')
        return func(*args, **kwargs)
    return wrapper

@logger_info
def open_poni(poni=None) -> PoniFile:
    """
    Opens an instance from pyFAI.io.PoniFile

    Keyword Arguments:
        poni -- PoniFile instance or ponifile string path (default: {None})

    Returns:
        PoniFile instance
    """
    if isinstance(poni, PoniFile):
        poni = poni
    elif isinstance(poni, str) or isinstance(poni, Path):
        poni = Path(poni)

        if not poni.is_file():
            logger.error(f'{poni} does not exist.')
            return None

        try:
            poni = str(poni)
            poni = PoniFile(data=poni)
        except Exception as e:
            logger.error(f'{e}: {poni} is not a valid poni_filename.')
            poni = None
    else:
        poni = None

    return poni