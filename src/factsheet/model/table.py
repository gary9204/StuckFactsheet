"""
Defines stub class for table of elements.  See :mod:`element`.
"""
import dataclasses as DC
import gi   # type: ignore[import]
import typing

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@DC.dataclass
class InfoColumn:
    """Stub column information class."""
    title: str
    symbol: str
    styles: typing.Sequence[str]


@DC.dataclass
class TableElements:
    """Stub table of elements value class."""
    rows: Gtk.ListStore
    columns: typing.Sequence[InfoColumn]
