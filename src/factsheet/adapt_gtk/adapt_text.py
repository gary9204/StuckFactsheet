"""
Defines model classes that implement abstract text attribute.

See :class:`.AbstractTextModel`.
"""
import gi   # type: ignore[import]
import logging
import typing   # noqa

from factsheet.abc_types import abc_infoid as ABC_INFOID
from factsheet.adapt_gtk import adapt_view as AVIEW

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

logger = logging.getLogger('Main.adapt_text')


class AdaptEntryBuffer(ABC_INFOID.AbstractTextModel):
    """Implements model text attribute :class:`.AbstractTextModel`
    using `Gtk.EntryBuffer`_.

    .. _Gtk.EntryBuffer:
       https://lazka.github.io/pgi-docs/#Gtk-3.0/
       classes/EntryBuffer.html#Gtk.EntryBuffer

    :param p_text: initial buffer contents (default: empty)
    """

    def __getstate__(self) -> typing.Dict:
        """Return model text attribute in form pickle can persist.

        Persistent form of text attribute consists of text only.
        """
        state = self.__dict__.copy()
        state['ex_text'] = str(self._buffer.get_text())
        del state['_buffer']
        del state['_stale']
        del state['_views']
        return state

    def __init__(self, p_text: str = ''):
        self._buffer = Gtk.EntryBuffer(text=p_text)
        _ = self._buffer.connect(
            'deleted-text', lambda *_a: self.set_stale())
        _ = self._buffer.connect(
            'inserted-text', lambda *_a: self.set_stale())
        self._stale = False
        self._views: typing.Dict[int, Gtk.Entry] = dict()

    def __setstate__(self, px_state: typing.Dict):
        """Reconstruct model text attribute from state pickle loads.

        Reconstructed attribute is marked fresh and has no no views.

        :param px_state: unpickled state of stored text attribute.
        """
        self.__dict__.update(px_state)
        self._buffer = Gtk.EntryBuffer(
            text=self.ex_text)   # type: ignore[attr-defined]
        del self.ex_text       # type: ignore[attr-defined]
        _ = self._buffer.connect(
            'deleted-text', lambda *_a: self.set_stale())
        _ = self._buffer.connect(
            'inserted-text', lambda *_a: self.set_stale())
        self._stale = False
        self._views = dict()

    def __str__(self) -> str:
        """Return buffer contents as text."""
        return str(self._buffer.get_text())

    def attach_view(self, pm_view: AVIEW.AdaptEntry):
        """Add view to update display when text changes.

        :param pm_view: view to add
        """
        id_view = id(pm_view)
        if id_view in self._views:
            logger.warning(
                'Duplicate view: {} ({}.{})'.format(
                    hex(id_view),
                    self.__class__.__name__, self.attach_view.__name__))
            return

        pm_view.set_buffer(self._buffer)
        self._views[id_view] = pm_view

    def detach_view(self, pm_view: AVIEW.AdaptEntry):
        """Remove view of changes to text.

        :param pm_view: view to remove
        """
        id_view = id(pm_view)
        try:
            _ = self._views.pop(id_view)
            pm_view.set_buffer(Gtk.EntryBuffer())
        except KeyError:
            logger.warning(
                'Missing view: {} ({}.{})'.format(
                    hex(id_view),
                    self.__class__.__name__, self.detach_view.__name__))

    def is_fresh(self) -> bool:
        """Return True when there are no unsaved changes to buffer."""
        return not self._stale

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to buffer."""
        return self._stale

    def set_fresh(self):
        """Mark buffer in memory consistent with file contents."""
        self._stale = False

    def set_stale(self):
        """Mark buffer in memory changed from file contents."""
        self._stale = True
