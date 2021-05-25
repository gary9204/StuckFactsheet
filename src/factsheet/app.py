"""
Defines AppFactsheet application and entry point.
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

from factsheet.control import control_sheet as CSHEET  # noqa: #402
from factsheet.view import view_sheet as VSHEET  # noqa: #402


class AppFactsheet(Gtk.Application):
    """Defines AppFactsheet application representation.

    :param args: superclass positional parameters
    :param kwargs: superclass keyword parameters
    """

    def __init__(self, *args: typing.Tuple, **kwargs: typing.Any):
        """Register application with GTK."""
        super().__init__(application_id='com.novafolks.g2alpha',
                         flags=Gio.ApplicationFlags.FLAGS_NONE,
                         *args, **kwargs)

    def do_activate(self):
        """Create and display an initial factsheet with default content."""
        # sheets_active = CPOOL.PoolSheets()
        # _ = VSHEET.ViewSheet.new_factsheet(self, sheets_active)
        # _ = VSHEET.ViewSheet.new_factsheet(self)
        control = CSHEET.open_factsheet(None)
        _ = VSHEET.ViewSheet(p_app=self, p_control=control)

    def do_shutdown(self):
        """Application teardown. """
        Gtk.Application.do_shutdown(self)
        logger.info('AppFactsheet application shutdown.')

    def do_startup(self):
        """Application setup within GTK. """
        Gtk.Application.do_startup(self)
        logger.info('AppFactsheet application startup.')


def run_app():
    """Start application and show initial window."""
    app = AppFactsheet()
    app.run(sys.argv)


if __name__ == '__main__':
    run_app()
