# coding=utf8

import threading
import logging
import logging.config
import logging.handlers
from conf.setting import logfile
from conf.setting import log_level

levelmap = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


def singleton(cls):
    """单例模式装饰器"""
    instances = {}
    lock = threading.Lock()

    def _singleton(*args, **kwargs):
        with lock:
            fullkey = str((cls.__name__, tuple(args), tuple(kwargs.items())))
            if fullkey not in instances:
                instances[fullkey] = cls(*args, **kwargs)
        return instances[fullkey]

    return _singleton


@singleton
def logsetup():
    filename = logfile
    handler = logging.handlers.RotatingFileHandler(filename=filename, maxBytes=200 * 1024 * 1024, backupCount=3)
    logging.getLogger(filename).setLevel(levelmap.get(log_level, logging.INFO))
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logging.getLogger(filename).addHandler(handler)


def get_logger():
    logsetup()
    return logging.getLogger(logfile)


logger = get_logger()
