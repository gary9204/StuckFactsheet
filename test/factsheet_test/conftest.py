"""
Test fixtures for Factsheet as a whole.
"""


import pytest   # type: ignore[import]


import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@pytest.fixture
def patch_factsheet():
    """Pytest fixture returns stub :class:`.Factsheet`."""
    class Factsheet(Gtk.Application):
        def __init__(self, *args, **kwargs):
            super().__init__(application_id='com.novafolks.factsheet',
                             flags=Gio.ApplicationFlags.FLAGS_NONE,
                             *args, **kwargs)

        def do_activate(self):
            pass

        def do_startup(self):
            Gtk.Application.do_startup(self)

    return Factsheet


@pytest.fixture
def PatchLogger():
    """Pytest fixture returns stub `logging.logger <LoggingLogger_>`_.

    .. _LoggingLogger: https://docs.python.org/3.7/library/logging.html
       #logger-objects
    """
    class Logger:
        T_CRITICAL = 'critical'
        T_DEBUG = 'debug'
        T_NONE = 'none'
        T_WARNING = 'warning'

        def __init__(self):
            self.called = False
            self.level = self.T_NONE
            self.message = "No log call"

        def debug(self, p_message, *_args, **_kwargs):
            self.called = True
            self.level = self.T_DEBUG
            self.message = p_message

        def warning(self, p_message, *_args, **_kwargs):
            self.called = True
            self.level = self.T_WARNING
            self.message = p_message

        def critical(self, p_message, *_args, **_kwargs):
            self.called = True
            self.level = self.T_CRITICAL
            self.message = p_message

    return Logger
