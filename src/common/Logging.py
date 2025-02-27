import coloredlogs
import logging
from static.file_paths import Paths as path
import datetime


class Log:
    def __init__(self):
        self.is_start: bool = False

    def start(self):
        path.file_check(path.log_path)
        current_time = datetime.datetime.now().strftime("%y-%m-%d_%H:%M")
        fmt = "%(asctime)s - %(levelname)s - %(message)s"
        logging.basicConfig(
            filename=path.log_path + f"{current_time}_qsp.log",
            encoding="utf-8",
            level=logging.DEBUG,
            format=fmt,
        )
        # Coloredlogs configuration
        coloredlogs.install(level="DEBUG", fmt=fmt)
        # Logger
        self.logger = logging.getLogger(__name__)

    def log(self, msg, level="i"):
        """
        d:   debug | i:   info | w:   warning | e:   error | c:   critical
        """
        
        # Dont generate a log file every time the program starts
        if not self.is_start:
            self.start()

        if level == "d":  # debug
            self.logger.debug(msg)
        elif level == "i":  # info
            self.logger.info(msg)
        elif level == "w":  # warning
            self.logger.warning(msg)
        elif level == "e":  # error
            self.logger.error(msg)
        elif level == "c":  # critical
            self.logger.critical(msg)
