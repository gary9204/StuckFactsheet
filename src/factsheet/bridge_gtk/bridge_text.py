"""
Defines bridge classes that encapsulate widget toolkit text classes.

Constants and Type Hints
========================

.. data:: DisplayTextMarkup

    Type variable for visual element to display a text attribute.  The
    element supports `Pango markup`_ but is not editable.  See
    `Gtk.Label`_.

.. _Pango markup:
    https://docs.gtk.org/Pango/pango_markup.html

.. _Gtk.Label:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Label.html

.. data:: DisplayTextStyled

    Type variable for visual element to display a text attribute.  The
    element supports rich, tag-based formatting but is not editable.
    See `Gtk.TextView`_.

.. _Gtk.TextView:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TextView.html

.. data:: EditorTextMarkup

    Type variable for visual element to display a text attribute.  The
    element is editable and supports embedding `Pango markup`_.  See
    `Gtk.Entry`_.

.. _Gtk.Entry:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Entry.html

.. data:: EditorTextStyled

    Type variable for viaual element to display a text attribute.  The
    element is editable and supports rich, tag-based formatting.  See
    `Gtk.TextView`_.

.. data:: ModelTextOpaque

    Placeholder type variable for visual element to store a text
    attribute.

.. data:: UiTextMarkup

    Type variable for visual element to store text formatted with
    `Pango markup`_.  See :data:`EditorTextMarkup` `Gtk.EntryBuffer`_.

.. _Gtk.EntryBuffer:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/EntryBuffer.html

.. data:: UiTextStyled

    Type variable for visual element to store text formatted with
    externally-defined tags.  See :data:`EditorTextStyled` and
    `Gtk.TextBuffer`_.

.. _Gtk.TextBuffer:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TextBuffer.html

Classes and Functions
=====================
"""
import gi   # type: ignore[import]
import logging
import typing   # noqa

import factsheet.abc_types.abc_stalefile as ABC_STALE
import factsheet.bridge_gtk.bridge_base as BBASE

gi.require_version('Gtk', '3.0')
from gi.repository import GLib   # type: ignore[import]    # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402
from gi.repository import Pango    # type: ignore[import]    # noqa: E402

IdDisplay = typing.NewType('IdDisplay', int)
ModelTextOpaque = typing.TypeVar('ModelTextOpaque')
PersistText = str

UiTextMarkup = typing.Union[Gtk.EntryBuffer]
DisplayTextMarkup = typing.Union[Gtk.Label]
EditorTextMarkup = typing.Union[Gtk.Entry]

UiTextStyled = typing.Union[Gtk.TextBuffer]
DisplayTextStyled = typing.Union[Gtk.TextView]
EditorTextStyled = typing.Union[Gtk.TextView]

logger = logging.getLogger('Main.bridge_text')


def escape_text_markup(p_markup: str) -> str:
    """Return text without markup errors.

    Escape `Pango markup`_ errors.  Raise other GLib errors.

    :param p_markup: text that may contain markup errors.
    """
    ALL = -1
    NO_ACCEL_CHAR = '0'
    try:
        _, _, _, _ = Pango.parse_markup(p_markup, ALL, NO_ACCEL_CHAR)
    except GLib.Error as err:
        if 'g-markup-error-quark' == err.domain:
            p_markup = GLib.markup_escape_text(p_markup, ALL)
        else:
            raise
    return p_markup


class FactoryEditorTextMarkup(BBASE.FactoryUiViewAbstract[EditorTextMarkup]):
    """Editor factory for text stored in a given :class:`.ModelTextMarkup`.

    Views support editing both text and embedded `Pango markup`_.
    """

    def __init__(self, p_model: 'ModelTextMarkup') -> None:
        """Initialize store for text.

        :param p_model: model that contains storage for editors.
        """
        self._ui_model = p_model.ui_model

    def __call__(self) -> EditorTextMarkup:
        """Return editor for text and markup formatting."""
        view = Gtk.Entry(buffer=self._ui_model)
        NAME_ICON_PRIMARY = 'emblem-default-symbolic'
        NAME_ICON_SECONDARY = 'edit-delete-symbolic'
        TOOLTIP_PRIMARY = 'Click to accept changes.'
        TOOLTIP_SECONDARY = 'Click to cancel changes.'
        N_WIDTH_EDIT = 45
        view.set_halign(Gtk.Align.START)
        view.set_icon_from_icon_name(
            Gtk.EntryIconPosition.PRIMARY, NAME_ICON_PRIMARY)
        view.set_icon_from_icon_name(
            Gtk.EntryIconPosition.SECONDARY, NAME_ICON_SECONDARY)
        view.set_icon_tooltip_markup(
            Gtk.EntryIconPosition.PRIMARY, TOOLTIP_PRIMARY)
        view.set_icon_tooltip_markup(
            Gtk.EntryIconPosition.SECONDARY, TOOLTIP_SECONDARY)
        view.set_width_chars(N_WIDTH_EDIT)
        return view


class FactoryDisplayTextMarkup(BBASE.FactoryUiViewAbstract[DisplayTextMarkup]):
    """Display factory for text stored in a given :class:`.ModelTextMarkup`.

    Views support text display formatted from embedded `Pango markup`_.
    """

    def __call__(self) -> DisplayTextMarkup:
        """Return view to display text with markup formatting."""
        markup = escape_text_markup(self._ui_model.get_text())
        display = Gtk.Label(label=markup)
        self._displays[id_display(display)] = display
        _ = display.connect('destroy', self.on_destroy)
        _ = self._ui_model.connect('deleted-text', self.on_change)
        _ = self._ui_model.connect('inserted-text', self.on_change)
        XALIGN_LEFT = 0.0
        N_WIDTH_DISPLAY = 15
        display.set_ellipsize(Pango.EllipsizeMode.END)
        display.set_halign(Gtk.Align.START)
        display.set_selectable(True)
        display.set_use_markup(True)
        display.set_width_chars(N_WIDTH_DISPLAY)
        display.set_xalign(XALIGN_LEFT)
        return display

    def __init__(self, p_model: 'ModelTextMarkup') -> None:
        """Initialize store for text and collection of displays.

        :param p_model: model that contains storage for displays.
        """
        self._ui_model = p_model.ui_model
        self._displays: typing.MutableMapping[
            IdDisplay, DisplayTextMarkup] = dict()

    def on_change(self, *_args):
        """Refresh display views when text is inserted or deleted."""
        markup = escape_text_markup(self._ui_model.get_text())
        for display in self._displays.values():
            display.set_markup(markup)

    def on_destroy(self, p_display: DisplayTextMarkup) -> None:
        """Stop refreshing display view that is being destroyed.

        :param p_display: display view being destroyed.
        """
        id_destroy = id_display(p_display)
        try:
            _ = self._displays.pop(id_destroy)
        except KeyError:
            logger.warning(
                'Missing display: {} ({}.{})'.format(
                    hex(id_destroy),
                    self.__class__.__name__, self.on_destroy.__name__))


class FactoryEditorTextStyled(BBASE.FactoryUiViewAbstract[EditorTextStyled]):
    """Editor factory for text stored in a given :class:`.ModelTextStyled`.

    Views support editing text.

    .. note::
       Editing and applying format tags is planned but not implemented yet.
    """

    def __init__(self, p_model: 'ModelTextStyled') -> None:
        """Initialize store for text.

        :param p_model: model that contains storage for editors.
        """
        self._ui_model = p_model.ui_model

    def __call__(self) -> EditorTextStyled:
        """Return editor for text with tag-based formatting."""
        N_MARGIN_LEFT_RIGHT = 6
        N_MARGIN_TOP_BOTTOM = 6
        view = Gtk.TextView(buffer=self._ui_model)
        view.set_bottom_margin(N_MARGIN_TOP_BOTTOM)
        view.set_left_margin(N_MARGIN_LEFT_RIGHT)
        view.set_right_margin(N_MARGIN_LEFT_RIGHT)
        view.set_top_margin(N_MARGIN_TOP_BOTTOM)
        view.set_vexpand(True)
        view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        return view


class FactoryDisplayTextStyled(BBASE.FactoryUiViewAbstract[DisplayTextStyled]):
    """Display factory for text stored in a given :class:`.ModelTextStyled`.

    Views support displaying text.

    .. note::
       Applying format tags is planned but not implemented yet.  Class
       :class:`.FactoryDisplayTextStyled` is a wrapper for
       :class:`.FactoryEditorTextStyled` until formatting is implemented.
    """

    def __init__(self, p_model: 'ModelTextStyled') -> None:
        """Initialize store for text.

        :param p_model: model that contains storage for displays.
        """
        self._ui_model = p_model.ui_model
        self._factory_source = FactoryEditorTextStyled(p_model)

    def __call__(self) -> DisplayTextStyled:
        """Return view to display text with tag-based formatting."""
        view = self._factory_source()
        view.set_editable(False)
        return view


def id_display(p_display: DisplayTextMarkup) -> IdDisplay:
    """Return unique identifier for a display view.

    :param p_display: display to identify.
    """
    return IdDisplay(id(p_display))


class ModelText(ABC_STALE.InterfaceStaleFile,
                BBASE.BridgeBase[ModelTextOpaque, PersistText],
                typing.Generic[ModelTextOpaque]):
    """Common ancestor of bridge classes for text.

    Text bridge objects may have transient aspects associated with views in
    addition to persistant text content.
    Text bridge objects fhave persistent text content. In addition, a
    text bridge object may have transient aspects
    such as signal connections to views or change state with respect to file
    storage,

    .. admonition:: About Equality

        Each text bridge object has persistent text content.  In
        addition, a text bridge object may have transient aspects such
        as signal connections to views or change state with respect to
        file storage,

        Two text bridge objects are equivalent when their text content
        are equal.  Transient aspects of the objects are not compared
        and may be different.
    """

    def __getstate__(self) -> typing.Dict:
        """Return text bridge model in form pickle can persist.

        Persistent form of text bridge consists of text only.
        """
        state = super().__getstate__()
        del state['_stale']
        return state

    def __init__(self, p_text: str = '') -> None:
        """Extend initialization with text and change state.

        :param p_text: initial text content.
        """
        super().__init__()
        self._set_persist(p_text)
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

    def set_fresh(self) -> None:
        """Mark content in memory consistent with file."""
        self._stale = False

    def set_stale(self) -> None:
        """Mark content in memory changed from file."""
        self._stale = True

    @property
    def text(self) -> str:
        """Return model text."""
        return self._get_persist()

    @text.setter
    def text(self, p_text: str) -> None:
        """Set model text."""
        self._set_persist(p_text)


class ModelTextMarkup(ModelText[UiTextMarkup]):
    """Text storage with support for editing and `Pango markup`_.  See
    `Gtk.EntryBuffer`_.

    See :class:`.ModelText` regarding equality.

    .. _Gtk.EntryBuffer:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/EntryBuffer.html
    """

    def _get_persist(self) -> PersistText:
        """Return text storage element in form suitable for persistent
        storage.
        """
        return self._ui_model.get_text()

    def _new_ui_model(self) -> UiTextMarkup:
        """Return ``UiTextMarkup`` with signal connections."""
        ui_model = UiTextMarkup()
        _ = ui_model.connect('deleted-text', lambda *_a: self.set_stale())
        _ = ui_model.connect('inserted-text', lambda *_a: self.set_stale())
        return ui_model

    def _set_persist(self, p_persist: PersistText) -> None:
        """Set text storage element from content in persistent form.

        :param p_persist: persistent form for text storage element
            content.
        """
        ALL = -1
        self._ui_model.set_text(p_persist, ALL)


class ModelTextStyled(ModelText[UiTextStyled]):
    """Text bridge with support for editing and format tagging.  See
    `Gtk.TextBuffer`_.

    See :class:`.ModelText` regarding equality.

    .. _Gtk.TextBuffer:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TextBuffer.html
    """

    def _get_persist(self) -> PersistText:
        """Return text storage element in form suitable for persistent
        storage.
        """
        NO_HIDDEN = False
        start, end = self._ui_model.get_bounds()
        return self._ui_model.get_text(start, end, NO_HIDDEN)

    def _new_ui_model(self) -> UiTextStyled:
        """Return `GTK.TextBuffer`_ with signals connections."""
        model = Gtk.TextBuffer()
        _ = model.connect('changed', lambda *_a: self.set_stale())
        return model

    def _set_persist(self, p_persist: PersistText) -> None:
        """Set text storage element from content in persistent form.

        :param p_persist: persistent form for text storage element
            content.
        """
        ALL = -1
        self._ui_model.set_text(p_persist, ALL)
