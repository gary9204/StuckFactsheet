"""
Defines bridge classes to display and edit text with `Pango markup`_

.. _Pango markup:
    https://docs.gtk.org/Pango/pango_markup.html

.. data:: UIButtonTrigger

    Type alias for visual element to show/hide editor in view duo.  See
    `Gtk.MenuButton`_.

.. _Gtk.MenuButton:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/MenuButton.html

.. data:: UiDisplayTextMarkup

    Type alias for visual element to display a text attribute.  The
    element supports `Pango markup`_ but is not editable.  See
    `Gtk.Label`_.

.. _Gtk.Label:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Label.html

.. data:: UiAnchor

    Type alias for visual element that anchors a :class:`.EditorTextMarkup`.
    See `Gtk.Widget`_.

.. _Gtk.Widget:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Widget.html

.. data:: UiEditorTextMarkup

    Type alias for visual element to edit a text attribute.  The
    element is editable and supports embedding `Pango markup`_.  See
    `Gtk.Entry`_.

.. _Gtk.Entry:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Entry.html

.. data:: UiTextMarkup

    Type alias for element to store text formatted with `Pango markup`_.
    See `Gtk.EntryBuffer`_ and :data:`UiEditorTextMarkup`.

.. _Gtk.EntryBuffer:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/EntryBuffer.html

.. data:: ViewDuoTextMarkup

    Type alias for visual element with components to both display and
    edit a text attribute.  See :data:`.UiDisplayTextMarkup` and
    :data:`.UiEditorTextMarkup`.

"""
import gi  # type: ignore[import]
import logging
import typing

import factsheet.bridge_gtk.bridge_text as BTEXT
import factsheet.view.ui as VUI

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk   # type: ignore[import]  # noqa: E402
from gi.repository import GLib  # noqa: E402
from gi.repository import GObject as GO  # noqa: E402
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # noqa: E402
from gi.repository import Pango    # noqa: E402

logger = logging.getLogger('Main.bridge_text_markup')

UiDisplayTextMarkup = typing.Union[Gtk.Label]
UiAnchor = typing.Union[Gtk.Widget]
UiEditorTextMarkup = typing.Union[Gtk.Entry]
UiLabel = typing.Union[Gtk.Label]
UiPopoverEditorMarkup = typing.Union[Gtk.Popover]
UiSite = typing.Union[Gtk.Box]
UiTextMarkup = typing.Union[Gtk.EntryBuffer]
UiButtonTrigger = typing.Union[Gtk.MenuButton]
UiViewDuoMarkup = typing.Union[Gtk.Box]


def x_b_tm_escape_text_markup(p_markup: str) -> str:
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


class DisplayTextMarkup:
    """Editor for text stored in a given :class:`.x_b_tm_ModelTextMarkup`.

    Provides visual element that support editing both text and embedded
    `Pango markup`_.

    .. attribute:: _UI_DEFINITION

        Constant that defines layout and format of visual element for
        the markup text editor.  Visual element property (that is,
        ``ui_view``) can change the layout and format of individual
        editors.

    .. warning:: Treat a :class:`.EditorTextMarkup` object like a GTK
        widget.  In particular, use the editor's visual element only in
        one GTK container and drop all references to the visual
        element when destroying the element.
    """

    def __init__(self, p_model: 'x_b_tm_ModelTextMarkup') -> None:
        """Initialize store for text and collection of displays.

        :param p_model: model that contains storage for displays.
        """
        """Initialize visual element of editor.

        :param p_model: model that contains storage for editor.
        """
        # self._ui_model = p_model.ui_model
        get_object = VUI.GetUiElementByStr(p_string_ui=self._UI_DEFINITION)
        self._ui_view = get_object('ui_view')

        markup = x_b_tm_escape_text_markup(p_model.text)
        self._ui_view.set_label(markup)

        _ = self._ui_view.connect('destroy', self.on_destroy, p_model.ui_model)
        self._id_delete = (
            p_model.ui_model.connect('deleted-text', self.on_change))
        self._id_insert = (
            p_model.ui_model.connect('inserted-text', self.on_change))

    def on_change(self, p_ui_model: UiTextMarkup, *_args):
        """Refresh display views when text is inserted or deleted."""
        markup = x_b_tm_escape_text_markup(p_ui_model.get_text())
        self._ui_view.set_markup(markup)

    def on_destroy(self, _ui_view: UiDisplayTextMarkup,
                   p_ui_model: UiTextMarkup) -> None:
        """Stop refreshing display view that is being destroyed.

        :param _ui_view: visual element of display being destroyed. (Unused)
        :param p_ui_model: storage element of display being destroyed.
        """
        if hasattr(self, 'ui_view'):  # Guard: duplicate destruction.
            del self._ui_view
            ID_INVALID = 0
            GO.signal_handler_disconnect(p_ui_model, self._id_delete)
            self._id_delete = ID_INVALID
            GO.signal_handler_disconnect(p_ui_model, self._id_insert)
            self._id_insert = ID_INVALID

    @property
    def ui_view(self) -> UiDisplayTextMarkup:
        """Return editor for text and markup formatting."""
        return self._ui_view

    _UI_DEFINITION = """<?xml version="1.0" encoding="UTF-8"?>
        <!-- Generated with glade 3.38.2 -->
        <interface>
          <requires lib="gtk+" version="3.24"/>
          <object class="GtkLabel" id="ui_view">
            <property name="visible">True</property>
            <property name="halign">start</property>
            <property name="use-markup">True</property>
            <property name="selectable">True</property>
            <property name="ellipsize">end</property>
            <property name="width-chars">15</property>
            <property name="xalign">0</property>
          </object>
        </interface>
        """


class EditorTextMarkup:
    """Editor for text stored in a given :class:`.x_b_tm_ModelTextMarkup`.

    Provides visual element that support editing both text and embedded
    `Pango markup`_.

    .. attribute:: _UI_DEFINITION

        Constant that defines layout and format of visual element for
        the markup text editor.  Visual element property (that is,
        ``ui_view``) can change the layout and format of individual
        editors.

    .. warning:: Treat a :class:`.EditorTextMarkup` object like a GTK
        widget.  In particular, use the editor's visual element only in
        one GTK container and drop all references to the visual
        element when destroying the element.
    """

    _UI_DEFINITION = """<?xml version="1.0" encoding="UTF-8"?>
        <!-- Generated with glade 3.38.2 -->
        <interface>
          <requires lib="gtk+" version="3.24"/>
          <object class="GtkEntry" id="ui_view">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="halign">start</property>
            <property name="width-chars">45</property>
            <property name="primary-icon-name"
                >emblem-default-symbolic</property>
            <property name="secondary-icon-name"
                >edit-delete-symbolic</property>
            <property name="primary-icon-tooltip-text"
                translatable="yes">Click to accept changes.</property>
            <property name="secondary-icon-tooltip-text"
                translatable="yes">Click to cancel changes.</property>
          </object>
        </interface>
        """

    def __init__(self, p_model: 'x_b_tm_ModelTextMarkup') -> None:
        """Initialize visual element of editor.

        :param p_model: model that contains storage for editor.
        """
        self._ui_view = UiEditorTextMarkup(buffer=p_model.ui_model)

    @property
    def ui_view(self) -> UiEditorTextMarkup:
        """Return editor for text and markup formatting."""
        return self._ui_view


def format_editor_markup(p_editor: EditorTextMarkup) -> None:
    """Apply formatting to visual element of editor.

    Set editor width and add icons to accept and cancel editing.
    Include tooltips for icons.

    :param p_editor: editor to format.
    """
    p_editor.ui_view.set_halign(Gtk.Align.START)
    N_WIDTH_EDIT = 45
    p_editor.ui_view.set_width_chars(N_WIDTH_EDIT)
    NAME_ICON_PRIMARY = 'emblem-default-symbolic'
    p_editor.ui_view.set_icon_from_icon_name(
        Gtk.EntryIconPosition.PRIMARY, NAME_ICON_PRIMARY)
    TOOLTIP_PRIMARY = 'Click to accept changes.'
    p_editor.ui_view.set_icon_tooltip_markup(
        Gtk.EntryIconPosition.PRIMARY, TOOLTIP_PRIMARY)
    NAME_ICON_SECONDARY = 'edit-delete-symbolic'
    p_editor.ui_view.set_icon_from_icon_name(
        Gtk.EntryIconPosition.SECONDARY, NAME_ICON_SECONDARY)
    TOOLTIP_SECONDARY = 'Click to cancel changes.'
    p_editor.ui_view.set_icon_tooltip_markup(
        Gtk.EntryIconPosition.SECONDARY, TOOLTIP_SECONDARY)


class x_b_tm_ModelTextMarkup(BTEXT.ModelText[UiTextMarkup]):
    """Text storage with support for editing and `Pango markup`_.  See
    `Gtk.EntryBuffer`_.

    See :class:`.ModelText` regarding equality.

    .. _Gtk.EntryBuffer:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/EntryBuffer.html
    """

    def _get_persist(self) -> BTEXT.PersistText:
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

    def _set_persist(self, p_persist: BTEXT.PersistText) -> None:
        """Set text storage element from content in persistent form.

        :param p_persist: persistent form for text storage element
            content.
        """
        ALL = -1
        self._ui_model.set_text(p_persist, ALL)


class PopupEditorMarkup:
    """Facade for visual element to pop up markup text editor.

    :class:`.PopupEditorMarkup` contains a visual element to pop
    up a markup text editor (:class:`.EditorTextMarkup`).  The element
    contains text to identify the editor's contents (such as Name or
    Title).  You may include `Pango markup`_ in the identifying text.
    An anchor visual element determines where the editor pops up.

    .. attribute:: _UI_DEFINITION

        Constant that defines layout and format of visual element that
        pops up for the markup text editor.

    .. admonition:: To maintainer

        Treat a :class:`.PopupEditorMarkup` object like a user
        interface toolkit element.  In particular, use the pop up editor
        only with one toolkit container and drop all references to the
        pop up editor when destroying the element.

    .. admonition:: To maintainer

        Each property with prefix ``ui_`` is a user interface toolkit
        element. Such properties should only be accessed in
        :mod:`.Element` or :mod:`.View` classes.  You can use toolkit
        element properties to change the layout and format of individual
        pop up editors.
    """

    def __init__(self, p_model: x_b_tm_ModelTextMarkup) -> None:
        """Initialize visual elements.

        :param p_model: model containing markup text.
        """
        get_object = VUI.GetUiElementByStr(p_string_ui=self._UI_DEFINITION)
        self._ui_view = get_object('ui_view')
        editor = EditorTextMarkup(p_model)
        self._ui_editor = editor.ui_view
        site_editor = get_object('site_editor')
        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 0
        site_editor.pack_start(
            self._ui_editor, EXPAND_OKAY, FILL_OKAY, N_PADDING)
        self._ui_label = get_object('ui_label')

    def set_anchor(self, p_anchor: UiAnchor) -> None:
        """Set anchor to determine editor pop up position.

        :param p_anchor: editor appears relative to this visual element.

        .. warning:: Gtk.MenuButton may use method set_popover in place
            of this method.
        """
        self._ui_view.set_relative_to(p_anchor)

    def set_label(self, p_text: str) -> None:
        """Set text to identify editor.


        :param p_test: identifying text, which may contain `Pango markup`_.
        """
        self._ui_label.set_label(p_text)

    @property
    def ui_editor(self) -> UiEditorTextMarkup:
        """Return visual element for markup text editor."""
        return self._ui_editor

    @property
    def ui_label(self) -> UiLabel:
        """Return visual element that identifies editor contents."""
        return self._ui_label

    @property
    def ui_view(self) -> UiPopoverEditorMarkup:
        """Return visual element to popup editor."""
        return self._ui_view

    _UI_DEFINITION = """<?xml version="1.0" encoding="UTF-8"?>
        <!-- Generated with glade 3.38.2 -->
        <interface>
          <requires lib="gtk+" version="3.20"/>
          <object class="GtkPopover" id="ui_view">
            <property name="can-focus">False</property>
            <property name="position">bottom</property>
            <property name="constrain-to">none</property>
            <child>
              <object class="GtkBox" id="site_editor">
                <property name="visible">True</property>
                <property name="can-focus">False</property>
                <property name="spacing">6</property>
                <child>
                  <object class="GtkLabel" id="ui_label">
                    <property name="visible">True</property>
                    <property name="can-focus">False</property>
                    <property name="label" translatable="yes"
                        >&lt;b&gt;Oops!&lt;/b&gt;</property>
                    <property name="use-markup">True</property>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">True</property>
                    <property name="position">0</property>
                  </packing>
                </child>
              </object>
            </child>
          </object>
        </interface>
        """


class ViewDuoMarkup:
    """View-model pair of visual elements to display and edit markup text.

    A view duo contains a display and a popup editor for markup text.
    Display shows formatted text when markup is valid.  It shows text
    with embedded markup when there is a markup error.  User can popup
    editor to edit both text and embedded markup.  The formatted text in
    the display updates as the user edits the markup text.  User can
    cancel edit and discard changes.

    Class :class:`.PariViewDuoTextMarkup` creates a view duo and pairs
    the view duo with a given markup text model.  When the app destroys
    a component visual element of view duo, view duo stops updating the
    component.  The view duo holds a reference to its top-level visual
    element until the view duo is destroyed.

    .. admonition:: To maintainer

        An alternative way to pair view duos with a markup text model is
        to implement a factory that produces paired view duos from a
        markup text model.  The factory maintains the collection of view
        duos paired with the markup text model.  This was the initial
        approach used with markup text display and editor views.

        * Pro: centralizes collection of view duos for a model

        * Con: combines pairing with management of view duo collection

        * Con: no guarantee of one factory per model

        :class:`.ViewDuoMarkup` makes pairing a distinct action
        independent from view duo collection management.  Collection
        management may be implemented separately as needed.
    """

    def __init__(self, p_model: x_b_tm_ModelTextMarkup, p_label: str = 'Item'
                 ) -> None:
        """Initialize internal components and their connections.

        :param p_model: model containing markup text.
        :param p_label: text to identify view duo to user (such as, 'Title').
        """
        # self._model = p_model
        self._text_restore = ''

        get_object = VUI.GetUiElementByStr(p_string_ui=self._UI_DEFINITION)
        self._ui_view = get_object('ui_view')
        self._ui_button = get_object('ui_button_edit')
        self._display = DisplayTextMarkup(p_model)
        self._popup = PopupEditorMarkup(p_model)
        self._popup.set_label(p_label)

        self.fill_display()
        self.link_popup()

    def fill_display(self) -> None:
        """Populate display component of view duo.

        Override this method to change the format of the display.
        """
        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 6
        self._ui_view.pack_start(
            self._display.ui_view, EXPAND_OKAY, FILL_OKAY, N_PADDING)

    def link_popup(self) -> None:
        """Link popup editor to view duo components.

        Popup includes editor along with button to show/hide editor..
        """
        self._ui_button.set_popover(self._popup.ui_view)
        _ = self._ui_button.connect(
            'toggled', self.on_toggled, self._popup.ui_editor)

        _ = self._popup.ui_editor.connect(
            'activate', lambda _: self._ui_button.clicked())
        _ = self._popup.ui_editor.connect('icon-press', self.on_icon_press)

    def on_icon_press(self, p_ui_editor: UiEditorTextMarkup,
                      p_icon: Gtk.EntryIconPosition, _event: Gdk.Event
                      ) -> None:
        """End edit and if user cancels edit, restore text.

        Primary icon accepts edits.  Secondary icon cancels edits.

        :param p_ui_editor: editor visual element.
        :param p_icon: identifies icon user clicked.
        :param _event: user interface event (unused).
        """
        if Gtk.EntryIconPosition.SECONDARY == p_icon:
            p_ui_editor.set_text(self._text_restore)
        self._ui_button.clicked()

    def on_toggled(self, p_ui_button: UiButtonTrigger,
                   p_ui_editor: UiEditorTextMarkup) -> None:
        """Record restore text before edit begins and clear after edit ends.

        :param p_ui_button: button user clicked.
        :param p_ui_editor: editor visual element.
        """
        if p_ui_button.get_active():
            self._text_restore = p_ui_editor.get_text()
        else:
            self._text_restore = ''

    @property
    def ui_button(self) -> UiViewDuoMarkup:
        """Return visual element of view duo."""
        return self._ui_button

    @property
    def ui_view(self) -> UiViewDuoMarkup:
        """Return visual element of view duo."""
        return self._ui_view

    _UI_DEFINITION = """<?xml version="1.0" encoding="UTF-8"?>
        <!-- Generated with glade 3.38.2 -->
        <interface>
          <requires lib="gtk+" version="3.20"/>
          <object class="GtkBox" id="ui_view">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
            <property name="spacing">6</property>
            <child>
              <object class="GtkMenuButton" id="ui_button_edit">
                <property name="visible">True</property>
                <property name="can-focus">True</property>
                <property name="receives-default">True</property>
                <child>
                  <object class="GtkImage">
                    <property name="visible">True</property>
                    <property name="can-focus">False</property>
                    <property name="icon-name"
                        >document-edit-symbolic</property>
                    <property name="icon_size">2</property>
                  </object>
                </child>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">True</property>
                <property name="position">0</property>
              </packing>
            </child>
          </object>
        </interface>
        """
