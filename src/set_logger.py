import logging


class ColoredFormat(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m', 'INFO': '\033[92m', 'WARNING': '\033[93m',
        'ERROR': '\033[91m', 'CRITICAL': '\033[95m'
    }

    def format(self, record) -> str:
        log_format = f"[%(levelname)s] | [%(funcName)s] | %(message)s"
        formatter = logging.Formatter(log_format)
        return formatter.format(record)