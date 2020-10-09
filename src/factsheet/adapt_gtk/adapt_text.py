"""
Defines GTK-based interfaces and adapters for Factsheet component
identification information.  See :mod:`.abc_infoid`.

.. data:: TextFormatGtk

    Type hint for GTK element to store :data:`ViewTextFormat`.  See
    `Gtk.TextBuffer`_.

.. _Gtk.TextBuffer:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TextBuffer.html

.. data:: TextMarkupGtk

    Type hint for GTK element to store :data:`ViewTextMarkup`.  See
    `Gtk.EntryBuffer`_.

.. _Gtk.EntryBuffer:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/EntryBuffer.html

.. data:: TextStaticGtk

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
import abc
import gi   # type: ignore[import]
import logging
import typing   # noqa

import factsheet.abc_types.abc_stalefile as ABC_STALE

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

TextFormatGtk = Gtk.TextBuffer
TextMarkupGtk = Gtk.EntryBuffer
TextStaticGtk = str
ViewTextFormat = typing.Union[Gtk.TextView]
ViewTextMarkup = typing.Union[Gtk.Entry]
ViewTextOpaque = typing.TypeVar('ViewTextOpaque')
ViewTextStatic = typing.Union[Gtk.Label]

logger = logging.getLogger('Main.adapt_infoid')


class AdaptText(typing.Generic[ViewTextOpaque],
                ABC_STALE.InterfaceStaleFile):
    """Common ancestor of model text attributes.

    Text attributes have transient data for attached views in addition
    to persistant text content.
    """

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when other is equivalent text attribute.

        :param p_other: object to test for equality.
        """
        if not isinstance(p_other, AdaptText):  # Accept descemdemts
            return False

        if self.text != p_other.text:
            return False

        return True

    def __getstate__(self) -> typing.Dict:
        """Return model text attribute in form pickle can persist.

        Persistent form of text attribute consists of text only.
        """
        state = self.__dict__.copy()
        del state['_stale']
        del state['_views']
        return state

    def __init__(self) -> None:
        self.__init_transient()

    def __init_transient(self) -> None:
        """Local helper initializes content common to __init__ and
        __setstate__.
        """
        self._stale = False
        self._views: typing.MutableMapping[int, ViewTextOpaque] = dict()

    def __setstate__(self, p_state: typing.MutableMapping) -> None:
        """Reconstruct model text attribute from state pickle loads.

        Reconstructed attribute is marked fresh and has no views.

        :param p_state: unpickled state of stored text attribute.
        """
        self.__dict__.update(p_state)
        self.__init_transient()

    def __str__(self) -> str:
        """Return attribute content."""
        return self.text

    @abc.abstractmethod
    def attach_view(self, p_view: ViewTextOpaque) -> None:
        """Add GTK display element to show content.

        :param p_view: view to add.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def detach_view(self, p_view: ViewTextOpaque) -> None:
        """Remove GTK display element.

        :param p_view: view to removes.
        """
        raise NotImplementedError

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
    @abc.abstractmethod
    def text(self) -> str:
        """Return attribute content."""
        raise NotImplementedError

    @text.setter
    def text(self, p_text: str) -> None:
        """Set attribute content.

        :param p_text: new content for attribute.
        """
        raise NotImplementedError


class AdaptTextMarkup(AdaptText[ViewTextMarkup]):
    """Implements editable model text attribute with support for markup.
    See `Gtk.EntryBuffer`_.

    Text attributes have transient data for attached views in addition
    to persistant text content.

    .. admonition:: About Equality

        Two text attributes are equivalent when they have the equal
        content.  Transient aspects of the attributes are not compared
        and may be different.

    .. _Gtk.EntryBuffer:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/EntryBuffer.html
    """

    def __getstate__(self) -> typing.Dict:
        """Return model text attribute in form pickle can persist.

        Persistent form of text attribute consists of text only.
        """
        state = super().__getstate__()
        state['ex_text'] = self.text
        del state['_text_gtk']
        return state

    def __init__(self) -> None:
        super().__init__()
        self._text_gtk = TextMarkupGtk()
        self.__init_transient()

    def __init_transient(self) -> None:
        """Local helper initializes content common to __init__ and
        __setstate__.
        """
        assert hasattr(self, '_text_gtk')
        _ = self._text_gtk.connect('deleted-text',
                                   lambda *_a: self.set_stale())
        _ = self._text_gtk.connect('inserted-text',
                                   lambda *_a: self.set_stale())

    def __setstate__(self, p_state: typing.MutableMapping) -> None:
        """Reconstruct model text attribute from state pickle loads.

        Reconstructed attribute is marked fresh and has no views.

        :param p_state: unpickled state of stored text attribute.
        """
        super().__setstate__(p_state)
        self._text_gtk = TextMarkupGtk(
            text=self.ex_text)   # type: ignore[attr-defined]
        del self.ex_text       # type: ignore[attr-defined]
        self.__init_transient()

    def attach_view(self, p_view: ViewTextMarkup) -> None:
        """Add view to display content.

        :param p_view: view to add.
        """
        id_view = id(p_view)
        if id_view in self._views:
            logger.warning('Duplicate view: {} ({}.{})'
                           ''.format(hex(id_view), type(self).__name__,
                                     self.attach_view.__name__))
            return

        p_view.set_buffer(self._text_gtk)
        self._views[id_view] = p_view

    def detach_view(self, p_view: ViewTextMarkup) -> None:
        """Remove GTK display element element.

        :param p_view: view to removes.
        """
        id_view = id(p_view)
        try:
            view_detached = self._views.pop(id_view)
            # See Factsheet Project Issue #29 on GitHub
            view_detached.hide()
        except KeyError:
            logger.warning('Missing view: {} ({}.{})'
                           ''.format(hex(id_view), type(self).__name__,
                                     self.detach_view.__name__))

    @property
    def text(self) -> str:
        """Return attribute content."""
        return self._text_gtk.get_text()

    @text.setter
    def text(self, p_text: str) -> None:
        """Set attribute content.

        :param p_text: new content for attribute.
        """
        ALL = -1
        self._text_gtk.set_text(p_text, ALL)
        self.set_stale()


class AdaptTextFormat(AdaptText[ViewTextFormat]):
    """Implements editable model text attribute with support for markup.
    See `Gtk.EntryBuffer`_.

    Text attributes have transient data for attached views in addition
    to persistant text content.

    .. admonition:: About Equality

        Two text attributes are equivalent when they have the equal
        content.  Transient aspects of the attributes are not compared
        and may be different.

    .. _Gtk.EntryBuffer:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/EntryBuffer.html
    """

    def __getstate__(self) -> typing.Dict:
        """Return model text attribute in form pickle can persist.

        Persistent form of text attribute consists of text only.
        """
        state = super().__getstate__()
        state['ex_text'] = self.text
        del state['_text_gtk']
        return state

    def __init__(self) -> None:
        super().__init__()
        self._text_gtk = TextFormatGtk()
        self.__init_transient()

    def __init_transient(self) -> None:
        """Local helper initializes content common to __init__ and
        __setstate__.
        """
        assert hasattr(self, '_text_gtk')
        _ = self._text_gtk.connect('changed', lambda *_a: self.set_stale())

    def __setstate__(self, p_state: typing.MutableMapping) -> None:
        """Reconstruct model text attribute from state pickle loads.

        Reconstructed attribute is marked fresh and has no views.

        :param p_state: unpickled state of stored text attribute.
        """
        super().__setstate__(p_state)
        self._text_gtk = TextFormatGtk(
            text=self.ex_text)   # type: ignore[attr-defined]
        del self.ex_text       # type: ignore[attr-defined]
        self.__init_transient()

    def attach_view(self, p_view: ViewTextMarkup) -> None:
        """Add view to display content.

        :param p_view: view to add.
        """
        id_view = id(p_view)
        if id_view in self._views:
            logger.warning('Duplicate view: {} ({}.{})'
                           ''.format(hex(id_view), type(self).__name__,
                                     self.attach_view.__name__))
            return

        p_view.set_buffer(self._text_gtk)
        self._views[id_view] = p_view

    def detach_view(self, p_view: ViewTextMarkup) -> None:
        """Remove GTK display element element.

        :param p_view: view to removes.
        """
        id_view = id(p_view)
        try:
            view_detached = self._views.pop(id_view)
            # See Factsheet Project Issue #29 on GitHub
            view_detached.hide()
        except KeyError:
            logger.warning('Missing view: {} ({}.{})'
                           ''.format(hex(id_view), type(self).__name__,
                                     self.detach_view.__name__))

    @property
    def text(self) -> str:
        """Return attribute content."""
        NO_HIDDEN = False
        start, end = self._text_gtk.get_bounds()
        return self._text_gtk.get_text(start, end, NO_HIDDEN)

    @text.setter
    def text(self, p_text: str) -> None:
        """Set attribute content.

        :param p_text: new content for attribute.
        """
        ALL = -1
        self._text_gtk.set_text(p_text, ALL)
        self.set_stale()


class AdaptTextStatic(AdaptText[ViewTextStatic]):
    """Implements model text attribute with support for markup.
    See `Gtk.Label`_.

    The text attribute content cannot be changed through the user
    interface.

    Text attributes have transient data for attached views in addition
    to persistant text content.

    .. admonition:: About Equality

        Two text attributes are equivalent when they have the equal
        content.  Transient aspects of the attributes are not compared
        and may be different.

    .. _Gtk.Label:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Label.html
    """

    def __init__(self) -> None:
        super().__init__()
        self._text_gtk = ''

    def attach_view(self, p_view: ViewTextStatic) -> None:
        """Add view to display content.

        :param p_view: view to add.
        """
        id_view = id(p_view)
        if id_view in self._views:
            logger.warning('Duplicate view: {} ({}.{})'
                           ''.format(hex(id_view), type(self).__name__,
                                     self.attach_view.__name__))
            return

        p_view.set_label(self._text_gtk)
        self._views[id_view] = p_view

    def detach_view(self, p_view: ViewTextStatic) -> None:
        """Remove GTK display element element.

        :param p_view: view to removes.
        """
        id_view = id(p_view)
        try:
            view_detached = self._views.pop(id_view)
            view_detached.hide()
        except KeyError:
            logger.warning('Missing view: {} ({}.{})'
                           ''.format(hex(id_view), type(self).__name__,
                                     self.detach_view.__name__))

    @property
    def text(self) -> str:
        """Return attribute content."""
        return self._text_gtk

    @text.setter
    def text(self, p_text: str) -> None:
        """Set attribute content.

        :param p_text: new content for attribute.
        """
        self._text_gtk = p_text
        self.set_stale()
