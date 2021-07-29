import logging,os
from Common.handle_path import logs_dir
from Common.handle_config import conf

class HandleLog:

    def __init__(self, name, path):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.stream_handler = logging.StreamHandler()
        self.file_handler = logging.FileHandler(path,encoding="utf-8")
        fmt = "%(asctime)s-%(name)s-%(levelname)s-%(filename)s-%(lineno)dline-日志信息: %(message)s"
        self.stream_handler.setFormatter(logging.Formatter(fmt))
        self.file_handler.setFormatter(logging.Formatter(fmt))
        self.logger.addHandler(self.stream_handler)
        self.logger.addHandler(self.file_handler)

    def get_logger(self):
        return self.logger

    def __del__(self):
        self.logger.removeHandler(self.stream_handler)
        self.logger.removeHandler(self.file_handler)
        self.stream_handler.close()
        self.file_handler.close()

if conf.getboolean("log", "file_ok"):
    file_path = os.path.join(logs_dir, conf.get("log","file_name"))
else:
    file_path = None

mlogger = HandleLog(conf.get("log","name"), file_path)
logger = mlogger.get_logger()
