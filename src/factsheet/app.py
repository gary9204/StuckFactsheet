"""
Defines Factsheet application and entry point.
"""
import logging   # type: ignore[import]
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys
import typing   # noqa

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

# Establish base logger before importing any Factsheetmodules
logger = logging.getLogger('Main')
logger.setLevel(logging.INFO)

path_log = Path('factsheet.log')
formatter = logging.Formatter(
    '[%(asctime)-8s.%(msecs)03d] | %(levelname)-8s | %(name)s | '
    '%(funcName)-20s | %(message)s', datefmt='%H:%M:%S')
file_handler = RotatingFileHandler(path_log, backupCount=9)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
if path_log.exists() and path_log.stat().st_size > 0:
    file_handler.doRollover()

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

from factsheet.view import page_sheet as VSHEET  # noqa: #402


class Factsheet(Gtk.Application):
    """Defines Factsheet application representation.

    :param args: superclass positional parameters
    :param kwargs: superclass keyword parameters
    """

    def __init__(self, *args: typing.Tuple, **kwargs: typing.Dict):
        """Register application with GTK."""
        super().__init__(application_id='com.novafolks.g2alpha',
                         flags=Gio.ApplicationFlags.FLAGS_NONE,
                         *args, **kwargs)

    def do_activate(self):
        """Create and display an initial factsheet with default content."""
        _ = VSHEET.PageSheet.new_factsheet(self)

    def do_shutdown(self):
        """Application teardown. """
        Gtk.Application.do_shutdown(self)
        logger.info('Factsheet application shutdown.')

    def do_startup(self):
        """Application setup within GTK. """
        Gtk.Application.do_startup(self)
        logger.info('Factsheet application startup.')


def run_app():
    """Start application and show initial window."""
    app = Factsheet()
    app.run(sys.argv)


if __name__ == '__main__':
    run_app()
