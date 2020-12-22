import datetime
from colorlog import ColoredFormatter
from config import *
import os
from importlib import import_module


def logger(name):
    """
    Usage:
    from logger import Logger
    logger = Logger(name)
    """
    filename = datetime.datetime.now().strftime(LOG_NAME_FORMAT)
    try:
        logging.basicConfig(filename=filename, level=LOG_LEVEL, format='%(asctime)s: %(name)s - %(levelname)s  | %(message)s')
    except BaseException as e:
        print("Base except logger {}".format(e))

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    logging.root.setLevel(LOG_LEVEL)
    formatter = ColoredFormatter(LOG_FORMAT)
    stream = logging.StreamHandler()
    stream.setLevel(LOG_LEVEL)
    stream.setFormatter(formatter)
    logger.addHandler(stream)
    return logger


