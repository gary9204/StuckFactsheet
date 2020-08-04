"""
Unit tests for stub table classes.  See :mod:`.table`.
"""
import dataclasses as DC
import gi   # type: ignore[import]
import pytest   # type: ignore[import]
import typing

from factsheet.model import table as MTABLE
from factsheet.model import setindexed as MSET

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@DC.dataclass
class ArgsInfoColumn:
    """TBD"""
    title: str
    symbol: str
    styles: typing.Sequence[str]


@pytest.fixture
def patch_args_column():
    """TBD"""
    return ArgsInfoColumn(
        title='Cheeses',
        symbol='c',
        styles=['Label', 'Element', 'Index', 'Member', 'Plain', 'Oops!'],
        )


@DC.dataclass
class ArgsTable:
    """TBD"""
    rows: Gtk.ListStore
    columns: typing.Sequence[MTABLE.InfoColumn]


@pytest.fixture
def patch_args_table():
    """TBD"""
    Set = MSET.SetIndexed[int]
    set_even = Set([0, 2, 4, 6])
    set_odd = Set([1, 3, 5, 7])
    rows = Gtk.ListStore(GO.TYPE_PYOBJECT, GO.TYPE_PYOBJECT)
    for e_even, e_odd in zip(set_even, set_odd):
        rows.append([e_even, e_odd])
    info_even = MTABLE.InfoColumn(title='Evens', symbol='e', styles=[
        'Label', 'Element'])
    info_odd = MTABLE.InfoColumn(title='Odds', symbol='o', styles=[
        'Index', 'Member', 'Plain'])
    columns = [info_even, info_odd]
    return ArgsTable(
        rows=rows,
        columns=columns,
        )


class TestInfoColumn:
    """Unit tests for :class:`.InfoColumn`."""

    def test_init(self, patch_args_column):
        """Confirm initialization."""
        # Setup
        ARGS = patch_args_column
        # Test
        target = MTABLE.InfoColumn(**DC.asdict(ARGS))
        assert ARGS.title == target.title
        assert ARGS.symbol == target.symbol
        assert ARGS.styles == target.styles


class TestTableElements:
    """Unit tests for :class:`TableElements`."""

    def test_init(self, patch_args_table):
        """Confirm initialization."""
        # Setup
        ARGS = patch_args_table
        target = MTABLE.TableElements(rows=ARGS.rows, columns=ARGS.columns)
        # Test
        assert target.rows is ARGS.rows
        assert target.columns is ARGS.columns
