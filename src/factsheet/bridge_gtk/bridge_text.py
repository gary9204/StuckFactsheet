"""
Defines bridge classes that encapsulate widget toolkit text classes.

.. data:: ModelTextTagged

    Type hint for GTK element to store text formatted with
    externally-defined tags.  See :data:`ViewTextTagged` and
    `Gtk.TextBuffer`_.

.. _Gtk.TextBuffer:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TextBuffer.html

.. data:: ModelTextMarkup

    Type hint for GTK element to store text formatted with
    `Pango markup`_.  See :data:`ViewTextMarkup` `Gtk.EntryBuffer`_.

.. _Gtk.EntryBuffer:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/EntryBuffer.html

    .. _Pango markup:
        https://developer.gnome.org/pygtk/stable/pango-markup-language.html

.. data:: ModelTextOpaque

    Type hint for placeholder GTK element to store a text attribute.

.. data:: ViewTextTagged

    Type hint for GTK element to display a text attribute.  The element
    supports rich, tag-based formatting.  The element may be editable or
    display-only.  See `Gtk.TextView`_.

.. _Gtk.TextView:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TextView.html

.. data:: ViewTextMarkup

    Type hint for GTK element to display a text attribute.  The element
    is editable and supports `Pango markup`_.  See `Gtk.Entry`_.

.. _Gtk.Entry:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Entry.html

.. data:: ViewTextOpaque

    Type hint for placeholder GTK display element for an editable text
    attribute.

.. data:: ViewTextOpaquePassive

    Type hint for placeholder GTK display element for a display-only
    text attribute.

.. data:: ViewTextDisplay

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
import factsheet.bridge_gtk.bridge_base as BBASE

gi.require_version('Gtk', '3.0')
from gi.repository import GLib   # type: ignore[import]    # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402
from gi.repository import Pango    # type: ignore[import]    # noqa: E402

ModelTextTagged = typing.Union[Gtk.TextBuffer]
ModelTextMarkup = typing.Union[Gtk.EntryBuffer]
ModelTextOpaque = typing.TypeVar('ModelTextOpaque')
# ModelTextStatic = str

PersistText = str

ViewTextTagged = typing.Union[Gtk.TextView]
ViewTextMarkup = typing.Union[Gtk.Entry]
ViewTextOpaque = typing.TypeVar('ViewTextOpaque')
ViewTextOpaquePassive = typing.TypeVar('ViewTextOpaquePassive')
ViewTextDisplay = typing.Union[Gtk.Label]

logger = logging.getLogger('Main.bridge_text')


class BridgeText(
        ABC_STALE.InterfaceStaleFile,
        BBASE.BridgeBase[ModelTextOpaque, PersistText, ViewTextOpaque],
        typing.Generic[ModelTextOpaque, ViewTextOpaque, ViewTextOpaquePassive
                       ],):
    """Common ancestor of bridge classes for text.

    Text bridge objects have transient data for attached views in
    addition to persistant text content.
    """

    def __getstate__(self) -> typing.Dict:
        """Return text bridge model in form pickle can persist.

        Persistent form of text bridge consists of text only.
        """
        state = super().__getstate__()
        del state['_stale']
        return state

    def __init__(self) -> None:
        """Extend initialization with change state."""
        super().__init__()
        self._stale = False

    def __setstate__(self, p_state: typing.MutableMapping) -> None:
        """Extend text bridge reconstruction with change state.

        Reconstructed text bridge is marked unchanged.

        :param p_state: unpickled content.
        """
        super().__setstate__(p_state)
        self._stale = False

    def is_fresh(self) -> bool:
        """Return True when there are no unsaved changes to content."""
        return not self.is_stale()

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to
        content.
        """
        return self._stale

    @abc.abstractmethod
    def new_view_passive(self) -> ViewTextOpaquePassive:
        """Return toolkit-specific object to display, but not edit, text."""
        raise NotImplementedError

    def set_fresh(self) -> None:
        """Mark attribute in memory consistent with file."""
        self._stale = False

    def set_stale(self) -> None:
        """Mark attribute in memory changed from file."""
        self._stale = True

    @property
    def text(self) -> str:
        """Return model text."""
        return self._get_persist()

    @text.setter
    def text(self, p_text: str) -> None:
        """Set model text.

        :param p_text: new content for model.
        """
        self._set_persist(p_text)
        self.set_stale()


class BridgeTextMarkup(
        BridgeText[ModelTextMarkup, ViewTextMarkup, ViewTextDisplay]):
    """Text bridge with support for editing and `Pango markup`_.  See
    `Gtk.EntryBuffer`_.

    Text bridge objects have transient data for attached views in
    addition to persistant text content.

    .. admonition:: About Equality

        Two text bridge objects are equivalent when they have the equal
        text.  Transient aspects of the attributes are not compared and
        may be different.

    .. _Gtk.EntryBuffer:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/EntryBuffer.html

    .. data:: N_WIDTH_DISPLAY

        Minimum width in characters of display view.

    .. data:: N_WIDTH_EDIT

        Minimum width in characters of edit view.
    """

    N_WIDTH_DISPLAY = 15
    N_WIDTH_EDIT = 45

    def _destroy_view(self, p_view: ViewTextDisplay) -> None:
        """Stop updating display view that is being destroyed.

        :param p_view: display view being destroyed.
        """
        id_view = id(p_view)
        try:
            _ = self._views.pop(id_view)
        except KeyError:
            logger.warning(
                'Missing view: {} ({}.{})'.format(
                    hex(id_view),
                    self.__class__.__name__, self._destroy_view.__name__))

    def _get_persist(self) -> PersistText:
        """Return text storage element in form suitable for persistent
        storage.
        """
        return self._model.get_text()

    def _new_model(self) -> ModelTextMarkup:
        """Return toolkit-specific object to store text."""
        model = ModelTextMarkup()
        _ = model.connect('deleted-text', lambda *_a: self.on_change())
        _ = model.connect('inserted-text', lambda *_a: self.on_change())
        self._views: typing.MutableMapping[int, ViewTextDisplay] = dict()
        return model

    def new_view(self) -> ViewTextMarkup:
        """Return view to display and edit text with mark up formatting."""
        NAME_ICON_PRIMARY = 'emblem-default-symbolic'
        NAME_ICON_SECONDARY = 'edit-delete-symbolic'
        TOOLTIP_PRIMARY = 'Click to accept changes.'
        TOOLTIP_SECONDARY = 'Click to cancel changes.'
        view = ViewTextMarkup.new_with_buffer(self._model)
        view.set_halign(Gtk.Align.START)
        view.set_icon_from_icon_name(
            Gtk.EntryIconPosition.PRIMARY, NAME_ICON_PRIMARY)
        view.set_icon_from_icon_name(
            Gtk.EntryIconPosition.SECONDARY, NAME_ICON_SECONDARY)
        view.set_icon_tooltip_markup(
            Gtk.EntryIconPosition.PRIMARY, TOOLTIP_PRIMARY)
        view.set_icon_tooltip_markup(
            Gtk.EntryIconPosition.SECONDARY, TOOLTIP_SECONDARY)
        view.set_width_chars(self.N_WIDTH_EDIT)
        return view

    def new_view_passive(self) -> ViewTextDisplay:
        """Return view to display text with mark up formatting."""
        view = ViewTextDisplay(label=self._get_persist())
        _ = view.connect('destroy', self._destroy_view)
        self._views[id(view)] = view

        XALIGN_LEFT = 0.0
        view.set_ellipsize(Pango.EllipsizeMode.END)
        view.set_halign(Gtk.Align.START)
        view.set_selectable(True)
        view.set_use_markup(True)
        view.set_width_chars(self.N_WIDTH_DISPLAY)
        view.set_xalign(XALIGN_LEFT)
        return view

    def on_change(self):
        """Refresh display views when text is inserted or deleted."""
        self.set_stale()
        text_new = self._model.get_text()
        is_valid_markup = True
        try:
            _, _, _, _ = Pango.parse_markup(text_new, -1, '0')
        except GLib.Error as err:
            if err.matches(GLib.markup_error_quark(), GLib.MarkupError.PARSE):
                is_valid_markup = False
            else:
                raise
        for view in self._views.values():
            if is_valid_markup:
                view.set_markup(text_new)
            else:
                view.set_text(text_new)

    def _set_persist(self, p_persist: PersistText) -> None:
        """Set text storage element from content in persistent form.

        :param p_persist: persistent form for text storage element
            content.
        """
        ALL = -1
        self._model.set_text(p_persist, ALL)


class BridgeTextTagged(
        BridgeText[ModelTextTagged, ViewTextTagged, ViewTextTagged]):
    """Text bridge with support for editing and format tagging.  See
    `Gtk.TextBuffer`_.

    Text bridge objects have transient data for attached views in
    addition to persistant text content.

    .. admonition:: About Equality

        Two text bridge objects are equivalent when they have equal
        text.  Transient aspects of the attributes are not compared
        and may be different.

    .. _Gtk.TextBuffer:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TextBuffer.html
    """

    def _get_persist(self) -> PersistText:
        """Return text storage element in form suitable for persistent
        storage.
        """
        NO_HIDDEN = False
        start, end = self._model.get_bounds()
        return self._model.get_text(start, end, NO_HIDDEN)

    def _new_model(self) -> ModelTextTagged:
        """Return toolkit-specific object to store text."""
        model = ModelTextTagged()
        _ = model.connect('changed', lambda *_a: self.set_stale())
        return model

    def new_view(self) -> ViewTextTagged:
        """Return view to display and edit text with tag-based formatting."""
        N_MARGIN_LEFT_RIGHT = 6
        N_MARGIN_TOP_BOTTOM = 6
        view = ViewTextTagged.new_with_buffer(self._model)
        view.set_bottom_margin(N_MARGIN_TOP_BOTTOM)
        view.set_left_margin(N_MARGIN_LEFT_RIGHT)
        view.set_right_margin(N_MARGIN_LEFT_RIGHT)
        view.set_top_margin(N_MARGIN_TOP_BOTTOM)
        view.set_vexpand(True)
        view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        return view

    def new_view_passive(self) -> ViewTextTagged:
        """Return view to display text with tag-based formatting."""
        view = self.new_view()
        view.set_editable(False)
        return view

    def _set_persist(self, p_persist: PersistText) -> None:
        """Set text storage element from content in persistent form.

        :param p_persist: persistent form for text storage element
            content.
        """
        ALL = -1
        self._model.set_text(p_persist, ALL)


# class BridgeTextStatic(BridgeText[ModelTextStatic, ViewTextDisplay]):
#     """Text bridge with support for `Pango markup`_ but not editing.
#     See `Gtk.Label`_.
#
#     Text content cannot be changed through the user interface.
#
#     Text bridge objects have transient data for attached views in
#     addition to persistant text content.
#
#     .. admonition:: About Equality
#
#         Two text bridge objects are equivalent when they have the equal
#         content.  Transient aspects of the attributes are not compared
#         and may be different.
#
#     .. _Gtk.Label:
#         https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Label.html
#     """
#
#     def _destroy_view(self, p_view: ViewTextDisplay) -> None:
#         """Stop updating view that is being destroyed.
#
#         :param p_view: view being destroyed.
#         """
#         id_view = id(p_view)
#         try:
#             _ = self._views.pop(id_view)
#         except KeyError:
#             logger.warning(
#                 'Missing view: {} ({}.{})'.format(
#                     hex(id_view),
#                     self.__class__.__name__, self._destroy_view.__name__))
#
#     def __getstate__(self) -> typing.Dict:
#         """Return content of storage element in form pickle can store.
#
#         Each descendant class defines its persistent contents.
#         """
#         state = super().__getstate__()
#         del state['_views']
#         return state
#
#     def _get_persist(self) -> PersistText:
#         """Return text storage element in form suitable for persistent
#         storage.
#         """
#         return self._model
#
#     def _new_model(self) -> ModelTextStatic:
#         """Return toolkit-specific object to store text."""
#         model = ModelTextStatic()
#         self._views: typing.MutableMapping[int, ViewTextDisplay] = dict()
#         return model
#
#     def new_view(self) -> ViewTextDisplay:
#         """Return toolkit-specific object to display text."""
#         view = ViewTextDisplay(label=self._model)
#         self._views[id(view)] = view
#         _ = view.connect('destroy', self._destroy_view)
#         return view
#
#     def _set_persist(self, p_persist: PersistText) -> None:
#         """Set text storage element from content in persistent form.
#
#         :param p_persist: persistent form for text storage element
#             content.
#         """
#         self._model = p_persist
#         for view in self._views.values():
#             view.set_label(self._model)
