import logging.handlers
import os
import sys


def script_path():
    path = os.path.realpath(sys.argv[0])
    if os.path.isfile(path):
        path = os.path.dirname(path)
    return os.path.abspath(path)


# 设置日志格式与输出文件
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=LOGGING_DATE_FORMAT)

logger_path = os.path.join(script_path(), 'logs')
if not os.path.exists(logger_path):
    os.makedirs(logger_path)

logger_file = os.path.join(logger_path, 'trace.log')

logger = logging.getLogger('_logger')
ch = logging.handlers.RotatingFileHandler(logger_file, maxBytes=1024 * 20, backupCount=40)
ch = logging.handlers.TimedRotatingFileHandler(logger_file, 'midnight', 1)
ch.setFormatter(logging.Formatter(LOG_FORMAT))

logger.addHandler(ch)
