"""
Defines bridge classes to display and edit text with `Pango markup`_

.. _Pango markup:
    https://docs.gtk.org/Pango/pango_markup.html

.. data:: ButtonEdit

    Type alias for visual element to show/hide editor in view duo.  See
    `Gtk.MenuButton`_.

.. _Gtk.MenuButton:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/MenuButton.html

.. data:: DisplayTextMarkup

    Type alias for visual element to display a text attribute.  The
    element supports `Pango markup`_ but is not editable.  See
    `Gtk.Label`_.

.. _Gtk.Label:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Label.html

.. data:: EditorTextMarkup

    Type alias for visual element to edit a text attribute.  The
    element is editable and supports embedding `Pango markup`_.  See
    `Gtk.Entry`_.

.. _Gtk.Entry:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Entry.html

.. data:: UiTextMarkup

    Type alias for element to store text formatted with `Pango markup`_.
    See `Gtk.EntryBuffer`_ and :data:`EditorTextMarkup`.

.. _Gtk.EntryBuffer:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/EntryBuffer.html

.. data:: ViewDuoTextMarkup

    Type alias for visual element with components to both display and
    edit a text attribute.  See :data:`.DisplayTextMarkup` and
    :data:`.EditorTextMarkup`.

"""
import gi  # type: ignore[import]
import logging
import typing

import factsheet.bridge_gtk.bridge_text as BTEXT
import factsheet.view.ui as VUI

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk   # type: ignore[import]  # noqa: E402
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # noqa: E402

logger = logging.getLogger('Main.bridge_text_markup')

ButtonEdit = typing.Union[Gtk.MenuButton]
DisplayTextMarkup = typing.Union[Gtk.Label]
EditorTextMarkup = typing.Union[Gtk.Entry]
UiTextMarkup = typing.Union[Gtk.EntryBuffer]
ViewDuoTextMarkup = typing.Union[Gtk.Box]


class PairViewDuoTextMarkup:
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

        :class:`.PairViewDuoTextMarkup` makes pairing a distinct action
        independent from view duo collection management.  Collection
        management may be implemented separately as needed.
    """

    def __init__(self, p_model: BTEXT.ModelTextMarkup,
                 p_label: str = 'Item') -> None:
        """Initialize internal components and their connections.

        :param p_model: model containing markup text.
        :param p_label: text to identify view duo to user (such as, 'Title').
        """
        self._model = p_model
        self._text_restore = ''

        get_object = VUI.GetUiElementByStr(p_string_ui=self._DEF_VIEW_DUO)
        self._ui_view = get_object('ui_view')

        self.fill_display(get_object)
        self.fill_label(get_object, p_label)
        self.fill_popup_editor(get_object)

    def fill_display(self, p_get_object: VUI.GetUiElementByStr) -> None:
        """Populate display component of view duo.

        Override this method to change the format of the display.

        :param p_get_object: method to get visual element from user
            interface description.
        """
        factory_display = BTEXT.FactoryDisplayTextMarkup(self._model)
        display = factory_display()
        display.show()
        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 6
        site_display = p_get_object('site_display')
        site_display.pack_start(display, EXPAND_OKAY, FILL_OKAY, N_PADDING)

    def fill_label(
            self, p_get_object: VUI.GetUiElementByStr, p_label: str) -> None:
        """Populate label component identifying view duo.

        Override this method to change the format of label.

        :param p_get_object: method to get visual element from user
            interface description.
        :param p_label: text to identify view duo to user (such as, 'Title').
        """
        label_duo = p_get_object('label_duo')
        label_duo.set_label('<b>{}</b>:'.format(p_label))

    def fill_popup_editor(self, p_get_object: VUI.GetUiElementByStr) -> None:
        """Populate popup editor component of view duo.

        Popup includes editor along with button to show/hide editor..

        Override this method to change the format of the editor.

        :param p_get_object: method to get visual element from user
            interface description.
        """
        factory_editor = BTEXT.FactoryEditorTextMarkup(self._model)
        editor = factory_editor()
        editor.show()
        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 6
        site_editor = p_get_object('site_editor')
        site_editor.pack_start(editor, EXPAND_OKAY, FILL_OKAY, N_PADDING)

        button_edit = p_get_object('button_edit')
        _ = button_edit.connect('toggled', self.on_toggled, editor)

        _ = editor.connect('activate', lambda _: button_edit.clicked())
        _ = editor.connect('icon-press', self.on_icon_press)

    def on_icon_press(self, p_editor: BTEXT.EditorTextMarkup,
                      p_icon: Gtk.EntryIconPosition, _event: Gdk.Event,
                      p_button_edit: ButtonEdit
                      ) -> None:
        """End edit and if user cancels edit, restore text.

        Primary icon accepts edits.  Secondary icon cancels edits.

        :param p_editor: editor view.
        :param p_icon: identifies icon user clicked.
        :param _event: user interface event (unused).
        :param p_button_edit: button to show/hide editor.
        """
        if Gtk.EntryIconPosition.SECONDARY == p_icon:
            p_editor.set_text(self._text_restore)
        p_button_edit.clicked()

    def on_toggled(
            self, p_button: Gtk.Button, p_editor: EditorTextMarkup) -> None:
        """Record restore text before edit begins and clear after edit ends.

        :param p_button: button user clicked.
        :param p_editor: editor associated with button user clicked.
        """
        if p_button.get_active():
            self._text_restore = p_editor.get_text()
        else:
            self._text_restore = ''

    @property
    def model(self) -> UiTextMarkup:
        """Return model of view duo."""
        return self._model

    @property
    def ui_view(self) -> ViewDuoTextMarkup:
        """Return visual element of view duo."""
        return self._ui_view

    _DEF_VIEW_DUO = """<?xml version="1.0" encoding="UTF-8"?>
        <!-- Generated with glade 3.38.2 -->
        <interface>
          <requires lib="gtk+" version="3.20"/>
          <object class="GtkPopover" id="ui_editor">
            <property name="can-focus">False</property>
            <property name="relative-to">button_edit</property>
            <property name="position">bottom</property>
            <property name="constrain-to">none</property>
            <child>
              <object class="GtkBox">
                <property name="visible">True</property>
                <property name="can-focus">False</property>
                <child>
                  <object class="GtkLabel" id="label_duo">
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
                <child>
                  <object class="GtkBox" id="site_editor">
                    <property name="visible">True</property>
                    <property name="can-focus">False</property>
                    <child>
                      <placeholder/>
                    </child>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">True</property>
                    <property name="position">1</property>
                  </packing>
                </child>
              </object>
            </child>
          </object>
          <object class="GtkBox" id="ui_view">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
            <child>
              <object class="GtkMenuButton" id="button_edit">
                <property name="visible">True</property>
                <property name="can-focus">True</property>
                <property name="receives-default">True</property>
                <property name="popover">ui_editor</property>
                <child>
                  <object class="GtkImage">
                    <property name="visible">True</property>
                    <property name="can-focus">False</property>
                    <property name="icon-name">document-edit-symbolic
                        </property>
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
            <child>
              <object class="GtkBox" id="site_display">
                <property name="visible">True</property>
                <property name="can-focus">False</property>
                <child>
                  <placeholder/>
                </child>
              </object>
              <packing>
                <property name="expand">True</property>
                <property name="fill">True</property>
                <property name="position">1</property>
              </packing>
            </child>
          </object>
        </interface>
        """
