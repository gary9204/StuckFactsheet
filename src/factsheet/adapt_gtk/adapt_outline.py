"""
Defines GTK-based classes implementing abstract outline classes.  See
:mod:`.abc_outline`.
"""
import gi   # type: ignore[import]
import typing

from factsheet.abc_types import abc_outline as ABC_OUTLINE

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

AdaptIndex = typing.Union[Gtk.TreeIter]
TypeItem = typing.TypeVar('TypeItem')


class AdaptTreeStore(ABC_OUTLINE.AbstractOutline[AdaptIndex, TypeItem]):
    """Implements abstract :class:`.AbstractOutline` using
    `Gtk.TreeStore`_.

    .. _Gtk.TreeStore:
       https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/
       TreeStore.html#Gtk.TreeStore
    """

    def __init__(self) -> None:
        self._store = Gtk.TreeStore(GO.TYPE_PYOBJECT)

    def get_item(self, i: AdaptIndex) -> TypeItem:
        """Return item at index."""
        return self._store[i][0]

    def insert_before(self, px_item: TypeItem, i: AdaptIndex) -> AdaptIndex:
        """Insert item before index and return index of new item."""
        return self._store.insert_before(None, i, [px_item])


class AdaptTreeView(ABC_OUTLINE.AbstractViewOutline):
    """TBD"""

    def set_model(  # type: ignore[override]
            self, pm_model: AdaptTreeStore) -> None:
        """TBD"""
        raise NotImplementedError
