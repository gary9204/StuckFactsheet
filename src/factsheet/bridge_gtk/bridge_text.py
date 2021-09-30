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
import gi   # type: ignore[import]
import logging
import typing   # noqa

import factsheet.abc_types.abc_stalefile as ABC_STALE
import factsheet.bridge_gtk.bridge_base as BBASE

gi.require_version('Gtk', '3.0')
from gi.repository import GLib   # type: ignore[import]    # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402
from gi.repository import Pango    # type: ignore[import]    # noqa: E402

# ModelTextTagged = typing.Union[Gtk.TextBuffer]
# ModelTextMarkup = typing.Union[Gtk.EntryBuffer]
ModelTextOpaque = typing.TypeVar('ModelTextOpaque')
# ModelTextStatic = str

PersistText = str

IdDisplay = typing.NewType('IdDisplay', int)

ViewTextTagged = typing.Union[Gtk.TextView]
ViewTextMarkup = typing.Union[Gtk.Entry]
ViewTextOpaque = typing.TypeVar('ViewTextOpaque')
ViewTextOpaquePassive = typing.TypeVar('ViewTextOpaquePassive')
ViewTextDisplay = typing.Union[Gtk.Label]

logger = logging.getLogger('Main.bridge_text')


class FactoryGtkEntry(BBASE.FactoryUiViewAbstract[Gtk.Entry]):
    """Editor factory for text stored in a given :class:`.ModelGtkEntryBuffer`.

    Views support editing both text and embedded `Pango markup`_.
    """

    def __init__(self, p_model: 'ModelGtkEntryBuffer') -> None:
        """Initialize store for text.

        :param p_model: model that contains storage for editors.
        """
        self._ui_model = p_model.ui_model

    def __call__(self) -> Gtk.Entry:
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


class FactoryGtkLabelBuffered(BBASE.FactoryUiViewAbstract[Gtk.Label]):
    """Display factory for text stored in a given :class:`.ModelGtkEntryBuffer`.

    Views support text display formated from embedded `Pango markup`_.
    """

    def __call__(self) -> Gtk.Label:
        """Return view to display text with markup formatting."""
        markup = self.filter_text_markup()
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

    def __init__(self, p_model: 'ModelGtkEntryBuffer') -> None:
        """Initialize store for text and collection of displays.

        :param p_model: model that contains storage for displays.
        """
        self._ui_model = p_model.ui_model
        self._displays: typing.MutableMapping[IdDisplay, Gtk.Label] = dict()

    def filter_text_markup(self) -> str:
        """Return text without markup errors.

        Escape Pango markup errors.  Raise GLib errors.
        """
        markup = self._ui_model.get_text()
        ALL = -1
        NO_ACCEL_CHAR = '0'
        try:
            _, _, _, _ = Pango.parse_markup(markup, ALL, NO_ACCEL_CHAR)
        except GLib.Error as err:
            if 'g-markup-error-quark' == err.domain:
                markup = GLib.markup_escape_text(markup, len(markup))
            else:
                raise
        return markup

    def on_change(self, _entry_buffer, _position, _n_chars):
        """Refresh display views when text is inserted or deleted."""
        markup = self.filter_text_markup()
        for display in self._displays.values():
            display.set_markup(markup)

    def on_destroy(self, p_display: Gtk.Label) -> None:
        """Stop updating display view that is being destroyed.

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


class FactoryGtkTextView(BBASE.FactoryUiViewAbstract[Gtk.TextView]):
    """Editor factory for text stored in a given :class:`.ModelGtkTextBuffer`.

    Views support editing text.

    .. note::
       Editing and applying format tags is planned but not implemented yet.
    """

    def __init__(self, p_model: 'ModelGtkTextBuffer') -> None:
        """Initialize store for text.

        :param p_model: model that contains storage for editors.
        """
        self._ui_model = p_model.ui_model

    def __call__(self) -> Gtk.TextView:
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


class FactoryGtkTextViewDisplay(BBASE.FactoryUiViewAbstract[Gtk.TextView]):
    """Display factory for text stored in a given :class:`.ModelGtkTextBuffer`.

    Views support displaying text.

    .. note::
       Applying format tags is planned but not implemented yet.  Class
       :class:`.FactoryGtkTextViewDisplay` is a wrapper for
       :class:`.FactoryGtkTextView` until formatting is implemented.
    """

    def __init__(self, p_model: 'ModelGtkTextBuffer') -> None:
        """Initialize store for text.

        :param p_model: model that contains storage for editors.
        """
        self._factory_source = FactoryGtkTextView(p_model)

    def __call__(self) -> Gtk.TextView:
        """Return view to display text with tag-based formatting."""
        view = self._factory_source()
        view.set_editable(False)
        return view


def id_display(p_display: Gtk.Label) -> IdDisplay:
    """Return unique identifier for a display view.

    :param p_display: display to identify.
    """
    return IdDisplay(id(p_display))


class ModelGtkText(ABC_STALE.InterfaceStaleFile,
                   BBASE.BridgeBase[ModelTextOpaque, PersistText],
                   typing.Generic[ModelTextOpaque]):
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
        """Extend initialization with text and change state."""
        super().__init__()
        self._set_persist('')
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


class ModelGtkEntryBuffer(ModelGtkText[Gtk.EntryBuffer]):
    """Text storage with support for editing and `Pango markup`_.  See
    `Gtk.EntryBuffer`_.

    Text bridge objects have transient data for attached views in
    addition to persistant text content.

    .. admonition:: About Equality

        Two text bridge objects are equivalent when they have the equal
        text.  Transient aspects of the attributes are not compared and
        may be different.

    .. _Gtk.EntryBuffer:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/EntryBuffer.html
    """

    def _get_persist(self) -> PersistText:
        """Return text storage element in form suitable for persistent
        storage.
        """
        return self._ui_model.get_text()

    def _new_gtk_model(self) -> Gtk.EntryBuffer:
        """Return `GTK.EntryBuffer`_ with signal connections."""
        ui_model = Gtk.EntryBuffer()
        _ = ui_model.connect('deleted-text', lambda *_a: self.set_stale())
        _ = ui_model.connect('inserted-text', lambda *_a: self.set_stale())
        return ui_model

    def _set_persist(self, p_persist: PersistText) -> None:
        """Set text storage element from content in persistent form.

        :param p_persist: persistent form for text storage element
            content.
        """
        if not hasattr(self, '_ui_model'):
            self._ui_model = self._new_gtk_model()
        ALL = -1
        self._ui_model.set_text(p_persist, ALL)


class ModelGtkTextBuffer(ModelGtkText[Gtk.TextBuffer]):
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
        start, end = self._ui_model.get_bounds()
        return self._ui_model.get_text(start, end, NO_HIDDEN)

    def _new_gtk_model(self) -> Gtk.TextBuffer:
        """Return `GTK.TextBuffer`_ with signals connections."""
        model = Gtk.TextBuffer()
        _ = model.connect('changed', lambda *_a: self.set_stale())
        return model

    def _set_persist(self, p_persist: PersistText) -> None:
        """Set text storage element from content in persistent form.

        :param p_persist: persistent form for text storage element
            content.
        """
        if not hasattr(self, '_ui_model'):
            self._ui_model = self._new_gtk_model()
        ALL = -1
        self._ui_model.set_text(p_persist, ALL)
