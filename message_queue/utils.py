from enum import Enum
import os
import logging

os.environ.setdefault('REDIS_ADDRESS', 'localhost')

redis_config = {
    'host': os.environ.get('REDIS_ADDRESSS'),
    'port': 6379
}


class NotifType(Enum):
    LIKE = 1
    FOLLOW = 2
    FOLLOW_REQUEST = 3
    COMMENT = 4
    UNLIKE = 5
    UNFOLLOW = 6
    UNREQUEST = 7
    OTHER_FOLLOW = 8


_logger = logging.getLogger('root')
FORMAT = " %(levelname)s %(asctime)s %(message)s"
logging.basicConfig(format=FORMAT)
_logger.setLevel(logging.DEBUG)


class LogWrapper():

    def __init__(self, logger):
        self.logger = logger

    def info(self, *args, sep=' '):
        self.logger.info(sep.join("{}".format(a) for a in args))

    def debug(self, *args, sep=' '):
        self.logger.debug(sep.join("{}".format(a) for a in args))

    def warning(self, *args, sep=' '):
        self.logger.warning(sep.join("{}".format(a) for a in args))

    def error(self, *args, sep=' '):
        self.logger.error(sep.join("{}".format(a) for a in args))

    def critical(self, *args, sep=' '):
        self.logger.critical(sep.join("{}".format(a) for a in args))

    def exception(self, *args, sep=' '):
        self.logger.exception(sep.join("{}".format(a) for a in args))

    def log(self, *args, sep=' '):
        self.logger.log(sep.join("{}".format(a) for a in args))
