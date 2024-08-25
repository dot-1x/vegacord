import logging
from datetime import datetime, timedelta, timezone
from colorama import Fore

from database.core.config import PROJECT_DIR


class CustomFormat(logging.Formatter):
    FORMAT = "[%(name)s | %(levelname)s] - %(message)s @ %(asctime)s"

    def __init__(self, noformat: bool = False) -> None:
        super().__init__(self.FORMAT)
        self.noformat = noformat

    def format(self, record):
        if self.noformat:
            return super().format(record)
        colors = {
            logging.DEBUG: Fore.WHITE,
            logging.INFO: Fore.GREEN,
            logging.WARNING: Fore.YELLOW,
            logging.ERROR: Fore.RED,
        }
        text = super().format(record)
        return colors.get(record.levelno, Fore.WHITE) + text + Fore.RESET

    def formatTime(self, _: logging.LogRecord, datefmt: str | None = None) -> str:
        return datetime.now(timezone(timedelta(hours=7))).strftime(
            datefmt or self.default_time_format
        )


console_hndl = logging.StreamHandler()
console_hndl.setFormatter(CustomFormat())


def get_logger(name: str, debug: bool = False):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG if debug else logging.INFO)
    fpath = f"{PROJECT_DIR}/logs/{name.replace(' ', '_').lower()}.log"
    if not log.handlers:
        file_handler = logging.FileHandler(fpath)
        file_handler.setFormatter(CustomFormat(noformat=True))
        log.addHandler(file_handler)
        log.addHandler(console_hndl)
    return log
