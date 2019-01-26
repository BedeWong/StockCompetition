#coding=utf-8
import  logging


class LoggerHandler(object):

    logger = None
    def __init__(self):
        if self.__class__.logger is None:
            self.__class__.logger = logging.getLogger('mylogger')
            self.__class__.logger.setLevel(logging.DEBUG)

    @staticmethod
    def get_logger():
        return __class__.logger

def main():
    pass


if __name__ == '__main__':
    main()