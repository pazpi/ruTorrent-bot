# log.py
import logging, coloredlogs
#import auxiliary_module
from logging.handlers import RotatingFileHandler

#logger = {}


def SetLogger():
    #global logger
    logger = logging.getLogger(__name__)
    # NOSET DEBUG INFO WARNING ERROR CRITICAL
    logger.setLevel(logging.DEBUG)
    # Create a file handler where log is located
    handler = RotatingFileHandler('rutorrent.log', mode='a', maxBytes=5 * 1024 * 1024,
                                  backupCount=5, encoding=None, delay=0)
    handler.setLevel(logging.DEBUG)
    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s(%(lineno)d) %(message)s')
    handler.setFormatter(formatter)
    # Add the handlers to the logger
    logger.addHandler(handler)
    logger.info('Log inizialized')
# #global logger
# logger = logging.getLogger(__name__)
# # NOSET DEBUG INFO WARNING ERROR CRITICAL
# logger.setLevel(logging.DEBUG)
# # Create a file handler where log is located
# handler = RotatingFileHandler('rutorrent.log', mode='a', maxBytes=5 * 1024 * 1024,
#                               backupCount=5, encoding=None, delay=0)
# handler.setLevel(logging.DEBUG)
# # Create a logging format
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s(%(lineno)d) %(message)s')
# handler.setFormatter(formatter)
# # Add the handlers to the logger
# logger.addHandler(handler)
# logger.info('Log inizialized')