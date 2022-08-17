import logging as _logging
from logging.handlers import RotatingFileHandler as _RotFileHandler

log_formatter = _logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
_handler = _RotFileHandler(f"logs/PyScratchLog.log", mode='a', maxBytes=5*1024*1024, 
                                 backupCount=5, encoding=None, delay=False)
_handler.setFormatter(log_formatter)
_handler.setLevel(_logging.INFO)

def _get_logger(name: str) -> _logging.Logger:
    logger = _logging.getLogger(name)
    logger.addHandler(_handler)
    logger.setLevel(_logging.INFO)


import pygame as _pygame

_pygame.init()




