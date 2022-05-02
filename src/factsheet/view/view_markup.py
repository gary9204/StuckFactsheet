"""
Defines view classes for identity information.
"""
import gi

import factsheet.bridge_ui as BUI

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk   # noqa: E402
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # noqa: E402


class ViewMarkup:
    """Provides capability to display and edit text with `Pango markup`_.

    The view contains a display and an editor. Display shows formatted
    text when markup is valid.  It shows text with embedded markup when
    there is a markup error.  User can popup editor to edit both text
    and embedded markup.  The formatted text in the display updates as
    the user edits the markup text.  User can cancel edit and discard
    changes.

    .. _Pango markup:
        https://developer.gnome.org/pygtk/stable/pango-markup-language.html
    """

    _UI_VIEW_MARKUP = """<?xml version="1.0" encoding="UTF-8"?>
        <!-- Generated with glade 3.22.1 -->
        <interface>
          <requires lib="gtk+" version="3.20"/>
          <object class="GtkBox" id="view">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <child>
              <object class="GtkMenuButton" id="button_edit">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="popover">editor</property>
                <child>
                  <object class="GtkImage">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property
                        name="icon_name">document-edit-symbolic</property>
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
                <property name="can_focus">False</property>
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
          <object class="GtkPopover" id="editor">
            <property name="can_focus">False</property>
            <property name="relative_to">button_edit</property>
            <property name="position">bottom</property>
            <property name="constrain_to">none</property>
            <child>
              <object class="GtkBox">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <child>
                  <object class="GtkLabel" id="label_type">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="label"
                        translatable="yes">&lt;b&gt;Oops!&lt;/b&gt;</property>
                    <property name="use_markup">True</property>
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
                    <property name="can_focus">False</property>
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
        </interface>
        """

    def __init__(self, p_display: BUI.DisplayTextMarkup, p_editor: Gtk.Entry,
                 p_type: str = '') -> None:
        """Initialize editor view contents.

        :param p_display: display for formatted text.
        :param p_editor: editor for markup text.
        :param p_type: content type of view (for example, 'Title')
        """
        builder = Gtk.Builder.new_from_string(self._UI_VIEW_MARKUP, -1)
        get_object = builder.get_object

        self._buffer = p_editor.get_buffer()
        self._button_edit = get_object('button_edit')
        _ = self._button_edit.connect('toggled', self.on_toggled)
        self._text_restore = ''
        self._ui_view = get_object('view')

        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 6
        site_display = get_object('site_display')
        site_display.pack_start(
            p_display, EXPAND_OKAY, FILL_OKAY, N_PADDING)
        p_display.show()

        label_type = get_object('label_type')
        label_type.set_label('<b>{}</b>:'.format(p_type))

        site_editor = get_object('site_editor')
        site_editor.pack_start(
            p_editor, EXPAND_OKAY, FILL_OKAY, N_PADDING)
        _ = p_editor.connect('icon-press', self.on_icon_press)
        _ = p_editor.connect(
            'activate', lambda _: self._button_edit.clicked())
        p_editor.show()

    def on_icon_press(
            self, _entry, p_icon_position, _event: Gdk.Event) -> None:
        """End edit and if user cancels edit, restore text.

        :param _entry: edit view (unused).
        :param p_icon_position: identifies icon user clicked.
        :param _event: user interface event (unused).
        """
        if Gtk.EntryIconPosition.SECONDARY == p_icon_position:
            self._buffer.set_text(self._text_restore, len(self._text_restore))
        self._button_edit.clicked()

    def on_toggled(self, _button: Gtk.Button) -> None:
        """Record restore text before edit begins and clear after edit ends.

        :param _button: edit button (unused).
        """
        if self._button_edit.get_active():
            self._text_restore = self._buffer.get_text()
        else:
            self._text_restore = ''

    @property
    def ui_view(self) -> Gtk.Box:
        """Return GTK element of markup view."""
        return self._ui_view
