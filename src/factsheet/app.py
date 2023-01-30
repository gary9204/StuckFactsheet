"""
Defines AppFactsheet application and entry point.
"""
import logging   # type: ignore[import]
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

# Establish base logger before importing any Factsheet modules
logger = logging.getLogger('Main')
logger.setLevel(logging.INFO)

path_log = Path('factsheet.log')
formatter = logging.Formatter(
    '[%(asctime)-8s.%(msecs)03d] | %(levelname)-8s | %(name)s | '
    '%(funcName)-20s | %(message)s', datefmt='%H:%M:%S')
file_handler = RotatingFileHandler(path_log, backupCount=2)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
if path_log.exists() and path_log.stat().st_size > 0:
    file_handler.doRollover()

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

import factsheet.view.view_sheet as VSHEET  # noqa: #402


if __name__ == '__main__':
    VSHEET.g_app.run(sys.argv)
