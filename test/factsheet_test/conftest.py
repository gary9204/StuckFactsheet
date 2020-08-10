"""
Test fixtures for Factsheet as a whole.
"""
import dataclasses as DC
import pytest   # type: ignore[import]
import typing

from factsheet.model import element as MELEMENT
from factsheet.model import setindexed as MSET
from factsheet.model import table as MTABLE

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
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


@DC.dataclass
class ArgsInfoId:
    """Convenience class for assembling arguments to
    :class:`.InfoId` method ``__init__``.
    """
    p_name: str
    p_summary: str
    p_title: str


@pytest.fixture
def patch_args_infoid():
    """Pytest fixture returns set of argument values to construct a
    stock :class:`InfoId` object.
    """
    return ArgsInfoId(
        p_name='Parrot',
        p_summary='The parrot is a Norwegian Blue.',
        p_title='The Parrot Sketch',
        )


@DC.dataclass
class ArgsArray:
    """Convenience class for assembling arguments to
    :class:`.Array` constructor expression.
    """
    p_rows: Gtk.ListStore
    p_cols: typing.Sequence
    p_styles: typing.Sequence[MELEMENT.Style]
    p_title: str
    p_symbol_row: str
    p_symbol_col: str
    p_symbol_entry: str


@pytest.fixture
def patch_args_array():
    """Pytest fixture returns argument list to construct a stock
    :class:`.Array` object.
    """
    Set = MSET.SetIndexed[int]
    Element = MELEMENT.ElementGeneric[int]
    N_ROWS = 3
    N_COLUMNS = 4
    size = N_ROWS * N_COLUMNS
    range_r = range(0, size, N_COLUMNS)
    range_c = range(0, size, N_ROWS)
    ROWS = Gtk.ListStore(*[GO.TYPE_PYOBJECT]*(1+N_COLUMNS))
    for i, r in enumerate(range_r):
        row = [Element(p_member=r, p_index=i)]
        entries = Set([(r+c) % size for c in range_c])
        row.extend(entries)
        ROWS.append(row)
    set_cols = Set(range_c)
    COLS = list(set_cols)
    STYLES = [MELEMENT.Style('Label'), MELEMENT.Style('Element'),
              MELEMENT.Style('Index'), MELEMENT.Style('Member'),
              MELEMENT.Style('Plain'), MELEMENT.Style('Oops!'),
              ]
    TITLE = 'Array'
    SYMBOL_ROW = 'r'
    SYMBOL_COL = 'c'
    SYMBOL_ENTRY = 'e'
    return ArgsArray(
        p_rows=ROWS,
        p_cols=COLS,
        p_styles=STYLES,
        p_title=TITLE,
        p_symbol_row=SYMBOL_ROW,
        p_symbol_col=SYMBOL_COL,
        p_symbol_entry=SYMBOL_ENTRY,
        )


@DC.dataclass
class ArgsTable:
    """Convenience class assembles arguments to
    :meth:`.TableElements.__init__` for pytest fixture.
    """
    rows: Gtk.ListStore
    columns: typing.Sequence[MTABLE.InfoColumn]


@pytest.fixture
def patch_args_table():
    """Pytest fixture returns arguments for
    :meth:`.TableElements.__init__`.
    """
    set_int = MSET.SetIndexed[int]([0, 2, 4, 6, 8])
    set_str = MSET.SetIndexed[str](['a', 'e', 'i', 'o', 'u'])
    list_mix = [MELEMENT.ElementGeneric('x', 0), None,
                MELEMENT.ElementGeneric('y', 1), None,
                MELEMENT.ElementGeneric('z', 2)]
    rows = Gtk.ListStore(GO.TYPE_PYOBJECT, GO.TYPE_PYOBJECT, GO.TYPE_PYOBJECT)
    for e_int, e_str, e_mix in zip(set_int, set_str, list_mix):
        rows.append([e_int, e_str, e_mix])
    info_int = MTABLE.InfoColumn(title='Integers', symbol='i', styles=[
        'Label', 'Element', 'Index', 'Member', 'Plain'])
    info_str = MTABLE.InfoColumn(title='Strings', symbol='s', styles=[
        'Label', 'Element', 'Index', 'Member', 'Plain', 'Oops'])
    info_mix = MTABLE.InfoColumn(title='Mixed', symbol='m', styles=[
        'Label', 'Element', 'Index', 'Member', 'Plain'])
    columns = [info_int, info_str, info_mix]
    return ArgsTable(
        rows=rows,
        columns=columns,
        )


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
