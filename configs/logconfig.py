#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging.handlers

class FinalLogger():
    """
    日志文件类
    """
    logger = None

    levels = {"n": logging.NOTSET,
              "d": logging.DEBUG,
              "i": logging.INFO,
              "w": logging.WARN,
              "e": logging.ERROR,
              "c": logging.CRITICAL}

    log_level = "d"
    log_file = "data.log"
    log_max_byte = 10 * 1024 * 1024
    log_backup_count = 10
    fmt = "[%(name)s][%(levelname)s][%(funcName)s][%(asctime)s]%(message)s"


    @staticmethod
    def getLogger(loggingname, fmt, log_file=None, maxBytes=None, backup_count=None):
        """
        获取一个日志打印对象
        :param loggingname: 日志打印对象名称
        :param fmt: 日志打印格式
        :param log_file: 日志打印路径
        :param maxBytes: 日志文件存储最大值
        :param backup_count: 日志文件的保留个数
        :return:
        """
        if not log_file:
            log_file = FinalLogger.log_file
        if not maxBytes:
            maxBytes = FinalLogger.log_max_byte
        if not backup_count:
            backup_count = FinalLogger.log_backup_count

        FinalLogger.logger = logging.Logger(loggingname)
        log_handler = logging.handlers.RotatingFileHandler(filename=log_file,
                                                           maxBytes=maxBytes,
                                                           backupCount=backup_count)
        log_fmt = logging.Formatter(fmt)
        log_handler.setFormatter(log_fmt)
        FinalLogger.logger.addHandler(log_handler)
        FinalLogger.logger.setLevel(FinalLogger.levels.get(FinalLogger.log_level))
        return FinalLogger.logger


# if __name__ == "__main__":
#     from os.path import join
#     log_path = config.configs.get("logfile")
#     logger = FinalLogger.getLogger(loggingname="text", fmt="[%(name)s][%(levelname)s][%(funcName)s][%(asctime)s]%(message)s",
#                                    log_file=join(log_path, "text.log"))
#
#     logger.debug("this is a debug msg!")
#     logger.info("this is a info msg!")
#     logger.warn("this is a warn msg!")
#     logger.error("this is a error msg!")
#     logger.critical("this is a critical msg!")
