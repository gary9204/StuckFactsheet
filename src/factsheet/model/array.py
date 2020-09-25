"""
Defines stub class for array of elements.  See :mod:`.element`.
"""
# import dataclasses as DC
import gi   # type: ignore[import]
import typing

from factsheet.model import element as MELEMENT

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


# @DC.dataclass
# class InfoColumn:
#     """Stub column information class."""
#     title: str
#     symbol: str
#     styles: typing.Sequence[str]


Entry = MELEMENT.ElementOpaque[MELEMENT.MemberOpaque]
IdStyle = MELEMENT.IdStyle
Style = MELEMENT.Style


class Array:
    """Defines fact value that is an array elements.

    An array is a rectangular arrangment of entries into rows and
    columns.  An array includes labels for each row, each column, and
    the array as a whole.  It identifies symbols and styles for
    converting labels and entries to text.

    :param p_rows: rows of the array as row label followed by entries..
    :param p_cols: labels for each column of entries.
    :param p_styles: styles for converting labels and entries to text.
    :param p_title: title to identify array.
    :param p_symbol_row: symbol used in text for row labels.
    :param p_symbol_col: symbol used in text for column labels.
    :param p_symbol_entry: symbol used in text for entries.
    """

    def __init__(self, p_rows: Gtk.ListStore, p_cols: typing.Sequence[Entry],
                 p_styles: typing.Sequence[Style], p_title: str = 'G',
                 p_symbol_row: str = 'g', p_symbol_col: str = 'g',
                 p_symbol_entry: str = 'g') -> None:
        self._rows = p_rows
        self._cols = p_cols
        self._styles = p_styles
        self._title = p_title
        self._symbol_row = p_symbol_row
        self._symbol_col = p_symbol_col
        self._symbol_entry = p_symbol_entry

    @property
    def rows(self) -> Gtk.ListStore:
        """Return rows of the array."""
        return self._rows

    @property
    def cols(self) -> typing.Sequence[Entry]:
        """Return column labels."""
        return self._cols

    @property
    def styles(self) -> typing.Sequence[Style]:
        """Return styles for labels and entries."""
        return self._styles

    @property
    def title(self) -> str:
        """Return title of array."""
        return self._title

    @property
    def symbol_row(self) -> str:
        """Return symbol for row labels."""
        return self._symbol_row

    @property
    def symbol_col(self) -> str:
        """Return symbol for column labels."""
        return self._symbol_col

    @property
    def symbol_entry(self) -> str:
        """Return symbol for entries."""
        return self._symbol_entry
