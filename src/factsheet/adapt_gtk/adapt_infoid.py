"""
Defines GTK-based classes implementing abstract identification
information classes.

See :mod:`.abc_infoid`.

.. data:: AdaptEntry

   Adapts `Gtk.Entry`_ widget to display a text attribute.

.. _Gtk.Entry:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/
   Entry.html#Gtk.Entry

.. data:: AdaptTextView

   Adapts `Gtk.TextView`_ widget to display a text attribute.

.. _Gtk.TextView:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/
   TextView.html#Gtk.TextView
"""
import gi   # type: ignore[import]
import logging
import typing   # noqa

from factsheet.abc_types import abc_infoid as ABC_INFOID

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

AdaptEntry = typing.Union[Gtk.Entry]
AdaptTextView = typing.Union[Gtk.TextView]

logger = logging.getLogger('Main.adapt_text')


def str_adapt_textview(px_view: AdaptTextView) -> str:
    """Return AdaptTextView contents as a text.

    :param px_view: target view.
    """
    buffer = px_view.get_buffer()
    start, end = buffer.get_bounds()
    text = buffer.get_text(start, end, AdaptTextBuffer.INCLUDE_HIDDEN)
    return text


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

    def __init__(self, p_text: str = '') -> None:
        self._buffer = Gtk.EntryBuffer(text=p_text)
        self._state_transient()

    def __setstate__(self, px_state: typing.Dict) -> None:
        """Reconstruct model text attribute from state pickle loads.

        Reconstructed attribute is marked fresh and has no views.

        :param px_state: unpickled state of stored text attribute.
        """
        self.__dict__.update(px_state)
        self._buffer = Gtk.EntryBuffer(
            text=self.ex_text)   # type: ignore[attr-defined]
        del self.ex_text       # type: ignore[attr-defined]
        self._state_transient()

    def _state_transient(self) -> None:
        """Helper ensures __init__ and __setstate__ are consistent."""
        assert hasattr(self, '_buffer')
        _ = self._buffer.connect(
            'deleted-text', lambda *_a: self.set_stale())
        _ = self._buffer.connect(
            'inserted-text', lambda *_a: self.set_stale())
        self._stale = False
        self._views: typing.Dict[int, AdaptEntry] = dict()

    def __str__(self) -> str:
        """Return buffer contents as text."""
        return str(self._buffer.get_text())

    def attach_view(self, pm_view: AdaptEntry) -> None:
        """Add view to update display when text changes.

        :param pm_view: view to add.
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

    def detach_view(self, pm_view: AdaptEntry) -> None:
        """Remove view of changes to text.

        :param pm_view: view to remove
        """
        id_view = id(pm_view)
        try:
            _view = self._views.pop(id_view)
            # See Factsheet Project Issue #29 on GitHub
            pm_view.hide()
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

    def set_fresh(self) -> None:
        """Mark buffer in memory consistent with file contents."""
        self._stale = False

    def set_stale(self) -> None:
        """Mark buffer in memory changed from file contents."""
        self._stale = True


class AdaptTextBuffer(ABC_INFOID.AbstractTextModel):
    """Implements model text attribute :class:`.AbstractTextModel`
    using `Gtk.EntryBuffer`_.

    .. _Gtk.TextBuffer:
       https://lazka.github.io/pgi-docs/#Gtk-3.0/
       classes/TextBuffer.html#Gtk.TextBuffer

    :param p_text: initial buffer contents (default: empty)
    """
    INCLUDE_HIDDEN = True

    def __getstate__(self) -> typing.Dict:
        """Return model text attribute in form pickle can persist.

        Persistent form of text attribute consists of text only.
        """
        state = self.__dict__.copy()
        state['ex_text'] = str(self)
        del state['_buffer']
        del state['_stale']
        del state['_views']
        return state

    def __init__(self, p_text: str = '') -> None:
        self._buffer = Gtk.TextBuffer(text=p_text)
        self._state_transient()

    def __setstate__(self, px_state: typing.Dict) -> None:
        """Reconstruct model text attribute from state pickle loads.

        Reconstructed attribute is marked fresh and has no views.

        :param px_state: unpickled state of stored text attribute.
        """
        self.__dict__.update(px_state)
        self._buffer = Gtk.TextBuffer(
            text=self.ex_text)  # type: ignore[attr-defined]
        del self.ex_text       # type: ignore[attr-defined]
        self._state_transient()

    def _state_transient(self) -> None:
        """Helper ensures __init__ and __setstate__ are consistent."""
        assert hasattr(self, '_buffer')
        _ = self._buffer.connect('changed', lambda *_a: self.set_stale())
        self._stale = False
        self._views: typing.Dict[int, AdaptTextView] = dict()

    def __str__(self) -> str:
        """Return buffer contents as text."""
        start, end = self._buffer.get_bounds()
        text = str(self._buffer.get_text(start, end, self.INCLUDE_HIDDEN))
        return text

    def attach_view(self, pm_view: AdaptEntry) -> None:
        """Add view to update display when text changes.

        :param pm_view: view to add.
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

    def detach_view(self, pm_view: AdaptEntry) -> None:
        """Remove view of changes to text.

        :param pm_view: view to remove
        """
        id_view = id(pm_view)
        try:
            _view = self._views.pop(id_view)
            pm_view.set_buffer(Gtk.TextBuffer())
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

    def set_fresh(self) -> None:
        """Mark buffer in memory consistent with file contents."""
        self._stale = False

    def set_stale(self) -> None:
        """Mark buffer in memory changed from file contents."""
        self._stale = True
