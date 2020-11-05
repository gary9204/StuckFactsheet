"""
Defines model bridge classes that encapsulate widget toolkit text
classes.

.. data:: ModelTextFormat

    Type hint for GTK element to store :data:`ViewTextFormat`.  See
    `Gtk.TextBuffer`_.

.. _Gtk.TextBuffer:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TextBuffer.html

.. data:: ModelTextMarkup

    Type hint for GTK element to store :data:`ViewTextMarkup`.  See
    `Gtk.EntryBuffer`_.

.. _Gtk.EntryBuffer:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/EntryBuffer.html

.. data:: ModelTextStatic

    Type alias for ``str``. Used to store content for
    :data:`ViewTextStatic`.

.. data:: ViewTextFormat

    Type hint for GTK element to display a text attribute.  The element
    is editable and supports rich formatting.  See `Gtk.TextView`_.

.. _Gtk.TextView:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TextView.html

.. data:: ViewTextMarkup

    Type hint for GTK element to display a text attribute.  The element
    is editable and supports markup.  See `Gtk.Entry`_.

.. _Gtk.Entry:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Entry.html

.. data:: ViewTextOpaque

    Type hint for placeholder GTK element to display a text attribute.

.. data:: ViewTextStatic

    Type hint for GTK element to display a text attribute.  The element
    supports markup but is not editable.  See `Gtk.Label`_.

.. _Gtk.Label:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Label.html
"""
import gi   # type: ignore[import]
import logging
import typing   # noqa

import factsheet.abc_types.abc_stalefile as ABC_STALE
import factsheet.bridge_gtk.bridge_base as BBASE

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

ModelTextOpaque = typing.TypeVar('ModelTextOpaque')
ModelTextFormat = typing.Union[Gtk.TextBuffer]
ModelTextMarkup = typing.Union[Gtk.EntryBuffer]
ModelTextStatic = str

PersistText = str

ViewTextFormat = typing.Union[Gtk.TextView]
ViewTextMarkup = typing.Union[Gtk.Entry]
ViewTextOpaque = typing.TypeVar('ViewTextOpaque')
ViewTextStatic = typing.Union[Gtk.Label]

logger = logging.getLogger('Main.bridge_text')


class BridgeText(
        ABC_STALE.InterfaceStaleFile,
        BBASE.BridgeBase,
        typing.Generic[ModelTextOpaque, ViewTextOpaque],):
    """Common ancestor of bridge classes for text.

    Text bridge objects have transient data for attached views in
    addition to persistant text content.
    """

    def __getstate__(self) -> typing.Dict:
        """Return model text bridge in form pickle can persist.

        Persistent form of text bridge consists of text only.
        """
        state = super().__getstate__()
        del state['_stale']
        return state

    def _init_transients(self) -> None:
        """Helper ensures initialization and pickling are consistent."""
        super()._init_transients()
        self._stale = False

    def is_fresh(self) -> bool:
        """Return True when there are no unsaved changes to content."""
        return not self.is_stale()

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to
        content.
        """
        return self._stale

    def set_fresh(self) -> None:
        """Mark attribute in memory consistent with file."""
        self._stale = False

    def set_stale(self) -> None:
        """Mark attribute in memory changed from file."""
        self._stale = True

    @property
    def text(self) -> str:
        """Return attribute content."""
        return self._get_persist()

    @text.setter
    def text(self, p_text: str) -> None:
        """Set attribute content.

        :param p_text: new content for attribute.
        """
        self._set_persist(p_text)


class BridgeTextFormat(BridgeText[ModelTextFormat, ViewTextFormat]):
    """Text bridge with support for editing and format tagging.  See
    `Gtk.TextBuffer`_.

    Text bridge objects have transient data for attached views in
    addition to persistant text content.

    .. admonition:: About Equality

        Two text bridge objects are equivalent when they have the equal
        text.  Transient aspects of the attributes are not compared
        and may be different.

    .. _Gtk.TextBuffer:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TextBuffer.html
    """

    def _init_transients(self) -> None:
        """Helper ensures initialization and pickling are consistent."""
        super()._init_transients()
        _ = self._model.connect('changed', lambda *_a: self.set_stale())

    def _bind(self, p_view: ViewTextMarkup):
        """Form toolkit-specific connection between text view element and
        text storage element.

        :param p_view: view to bind.
        """
        p_view.set_buffer(self._model)

    def _get_persist(self) -> PersistText:
        """Return text storage element in form suitable for persistent
        storage.
        """
        NO_HIDDEN = False
        start, end = self._model.get_bounds()
        return self._model.get_text(start, end, NO_HIDDEN)

    def _loose(self, p_view: ViewTextMarkup):
        """Break toolkit-specific connection between text view element
        and text storage element.

        :param p_view: view to separate.
        """
        p_view.set_buffer(None)

    def _new_model(self) -> ModelTextMarkup:
        """Return toolkit-specific object to store text."""
        return ModelTextFormat()

    def _set_persist(self, p_persist: PersistText) -> None:
        """Set text storage element from content in persistent form.

        :param p_persist: persistent form for text storage element
            content.
        """
        ALL = -1
        self._model.set_text(p_persist, ALL)
        self.set_stale()


class BridgeTextMarkup(BridgeText[ModelTextMarkup, ViewTextMarkup]):
    """Text bridge with support for editing and `Pango markup`_.  See
    `Gtk.EntryBuffer`_.

    .. _Pango markup:
        https://developer.gnome.org/pango/stable/pango-Markup.html

    Text bridge objects have transient data for attached views in
    addition to persistant text content.

    .. admonition:: About Equality

        Two text bridge objects are equivalent when they have the equal
        text    .  Transient aspects of the attributes are not compared
        and may be different.

    .. _Gtk.EntryBuffer:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/EntryBuffer.html
    """

    def _init_transients(self) -> None:
        """Helper ensures initialization and pickling are consistent."""
        super()._init_transients()
        _ = self._model.connect('deleted-text', lambda *_a: self.set_stale())
        _ = self._model.connect('inserted-text', lambda *_a: self.set_stale())

    def _bind(self, p_view: ViewTextMarkup):
        """Form toolkit-specific connection between text view element and
        text storage element.

        :param p_view: view to bind.
        """
        p_view.set_buffer(self._model)

    def _get_persist(self) -> PersistText:
        """Return text storage element in form suitable for persistent
        storage.
        """
        return self._model.get_text()

    def _loose(self, p_view: ViewTextMarkup):
        """Break toolkit-specific connection between text view element
        and text storage element.

        :param p_view: view to separate.
        """
        store_empty = ModelTextMarkup()
        p_view.set_buffer(store_empty)

    def _new_model(self) -> ModelTextMarkup:
        """Return toolkit-specific object to store text."""
        return ModelTextMarkup()

    def _set_persist(self, p_persist: PersistText) -> None:
        """Set text storage element from content in persistent form.

        :param p_persist: persistent form for text storage element
            content.
        """
        ALL = -1
        self._model.set_text(p_persist, ALL)
        self.set_stale()


class BridgeTextStatic(BridgeText[ModelTextStatic, ViewTextStatic]):
    """Text bridge with support for `Pango markup`_ but not editing.
    See `Gtk.Label`_.

    Text content cannot be changed through the user interface.

    Text bridge objects have transient data for attached views in
    addition to persistant text content.

    .. admonition:: About Equality

        Two text bridge objects are equivalent when they have the equal
        content.  Transient aspects of the attributes are not compared
        and may be different.

    .. _Gtk.Label:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Label.html
    """

    def _bind(self, p_view: ViewTextStatic):
        """Form toolkit-specific connection between text view element and
        text storage element.

        The text bridge updates each bound view manually.  See also
        :meth:`~.BridgeTextStatic._set_persist`.

        :param p_view: view to bind.
        """
        p_view.set_label(self._model)

    def _get_persist(self) -> PersistText:
        """Return text storage element in form suitable for persistent
        storage.
        """
        return self._model

    def _loose(self, p_view: ViewTextStatic):
        """Break toolkit-specific connection between text view element
        and text storage element.

        :param p_view: view to separate.
        """
        p_view.set_label('')

    def _new_model(self) -> ModelTextMarkup:
        """Return toolkit-specific object to store text."""
        return ModelTextStatic()

    def _set_persist(self, p_persist: PersistText) -> None:
        """Set text storage element from content in persistent form.

        :param p_persist: persistent form for text storage element
            content.
        """
        self._model = p_persist
        self.set_stale()
        for view in self._views.values():
            view.set_label(self._model)
