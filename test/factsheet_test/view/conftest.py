"""
factsheet_test.view.conftest - test fixtures for View classes.
"""


import pytest   # type: ignore[import]

from factsheet.types_abstract import abc_sheet as ASHEET

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@pytest.fixture
def patch_factsheet():
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
