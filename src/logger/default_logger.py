import sys
import logging

class CustomFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[36m',   # Cyan
        'INFO': '\033[32m',    # Green
        'WARNING': '\033[33m', # Yellow
        'ERROR': '\033[31m',   # Red
        'CRITICAL': '\033[41m' # Red background
    }
    RESET = '\033[0m'

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.msg = f"{log_color}{record.msg}{self.RESET}"
        return super().format(record)

def get_logger():
    logger = logging.getLogger("default_logger")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(CustomFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

logger = get_logger()