"""
Unit tests for classes to display identity information.  See
:mod:`.view_markup`.
"""
import pytest   # type: ignore[import]

import factsheet.bridge_ui as BUI
import factsheet.control.control_sheet as CSHEET
import factsheet.view.view_markup as VMARKUP

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import] # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@pytest.fixture
def setup_views_markup():
    """Fixture with teardown: return display and editor views of markup."""
    PATH = None
    control = CSHEET.g_control_app.open_factsheet(
        p_path=PATH, p_time=BUI.TIME_EVENT_CURRENT)
    display_name = control.new_display_name()
    editor_name = control.new_editor_name()
    yield display_name, editor_name
    display_name.destroy()
    editor_name.destroy()


class TestEditorMarkup:
    """Unit tests for :class:`.ViewMarkup`."""

    def test_init(self, setup_views_markup):
        """| Confirm initialization.
        | Case: view settings and attributes

        :param setup_views_markup: fixture :func:`.setup_views_markup`.
        """
        # Setup
        DISPLAY, EDITOR = setup_views_markup
        I_SITE_DISPLAY = 1
        I_DISPLAY = 0
        N_PADDING = 6
        I_BUTTON_EDIT = 0
        I_EDITOR = 0
        TYPE = 'Parrot'
        TYPE_MARKED = '<b>' + TYPE + '</b>:'
        # Test
        target = VMARKUP.ViewMarkup(
            p_display=DISPLAY, p_editor=EDITOR, p_type=TYPE)
        children_editor = target._ui_view.get_children()
        assert target._buffer is EDITOR.get_buffer()
        assert isinstance(target._button_edit, Gtk.MenuButton)
        assert '' == target._text_restore
        assert isinstance(target._ui_view, Gtk.Box)

        site_display = children_editor[I_SITE_DISPLAY]
        assert isinstance(site_display, Gtk.Box)
        assert DISPLAY is (
            site_display.get_children()[I_DISPLAY])
        expand_passive, fill_passive, padding_passive, _pack = (
            site_display.query_child_packing(DISPLAY))
        assert expand_passive
        assert fill_passive
        assert N_PADDING == padding_passive
        assert DISPLAY.get_visible()

        button_edit = children_editor[I_BUTTON_EDIT]
        popover_edit = button_edit.get_popover()
        box_popover = popover_edit.get_child()
        label_type, site_editor = box_popover.get_children()
        assert TYPE_MARKED == label_type.get_label()
        assert isinstance(site_editor, Gtk.Box)
        assert EDITOR is site_editor.get_children()[I_EDITOR]
        expand_active, fill_active, padding_active, _pack = (
            site_editor.query_child_packing(EDITOR))
        assert expand_active
        assert fill_active
        assert N_PADDING == padding_active
        assert EDITOR.get_visible()

    @pytest.mark.parametrize(
        'NAME_SIGNAL, NAME_ATTR, ORIGIN, N_DEFAULT', [
            ('toggled', '_button_edit', Gtk.MenuButton, 0),
            ])
    def test_init_signals_attr(self, setup_views_markup,
                               NAME_SIGNAL, NAME_ATTR, ORIGIN, N_DEFAULT):
        """| Confirm initialization.
        | Case: signal connections to view attributes.

        :param setup_views_markup: fixture :func:`.setup_views_markup`.
        :param NAME_SIGNAL: name of signal to check.
        :param NAME_ATTR: attribute generating signal.
        :param ORIGIN: GTK class origin of signal.
        :param N_DEFAULT: count of default signal handlers.
        """
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        DISPLAY, EDITOR = setup_views_markup
        target = VMARKUP.ViewMarkup(p_display=DISPLAY, p_editor=EDITOR)
        # Test
        attribute = getattr(target, NAME_ATTR)
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                attribute, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(attribute, id_signal)

        assert N_DEFAULT + 1 == n_handlers

    @pytest.mark.parametrize('NAME_SIGNAL, ORIGIN, N_DEFAULT', [
            ('icon_press', Gtk.Entry, 0),
            ('activate', Gtk.Entry, 0),
            ])
    def test_init_signals_editor(
            self, setup_views_markup, NAME_SIGNAL, ORIGIN, N_DEFAULT):
        """| Confirm initialization.
        | Case: signal connections to editor.

        :param setup_views_markup: fixture :func:`.setup_views_markup`.
        :param NAME_SIGNAL: name of signal to check.
        :param ORIGIN: GTK class origin of signal.
        :param N_DEFAULT: count of default signal handlers.
        """
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        DISPLAY, EDITOR = setup_views_markup
        _target = VMARKUP.ViewMarkup(p_display=DISPLAY, p_editor=EDITOR)
        # Test
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                EDITOR, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(EDITOR, id_signal)

        assert N_DEFAULT + 1 == n_handlers

    @pytest.mark.parametrize('ICON, EXPECT_TEXT', [
        (Gtk.EntryIconPosition.PRIMARY, 'Something completely different'),
        (Gtk.EntryIconPosition.SECONDARY, ''),
        ])
    def test_on_icon_press(self, setup_views_markup, ICON, EXPECT_TEXT):
        """Confirm text restored before ending edit.

        #. Case: primary icon.
        #. Case: secondary icon.

        :param setup_views_markup: fixture :func:`.setup_views_markup`.
        :param ICON: icon to check.
        :param EXPECT_TEXT: text expected in buffer.
        """
        # Setup
        DISPLAY, EDITOR = setup_views_markup
        target = VMARKUP.ViewMarkup(
            p_display=DISPLAY, p_editor=EDITOR)
        TEXT = 'Something completely different'
        target._buffer.set_text(TEXT, len(TEXT))
        target._button_edit.clicked()
        BLANK = ''
        target._text_restore = BLANK
        # Test
        target.on_icon_press(None, ICON, None)
        assert not target._button_edit.get_active()
        assert EXPECT_TEXT == target._buffer.get_text()

    def test_on_toggle(self, setup_views_markup):
        """Confirm record of restore text and clear of restore text.

        #. Case: editor changes to active
        #. Case: editor changes to not active

        :param setup_views_markup: fixture :func:`.setup_views_markup`.
        """
        # Setup
        DISPLAY, EDITOR = setup_views_markup
        target = VMARKUP.ViewMarkup(p_display=DISPLAY, p_editor=EDITOR)
        BLANK = ''
        TEXT = 'Something completely different.'
        target._buffer.set_text(TEXT, len(TEXT))
        # Test: edit button is active
        target._button_edit.clicked()
        assert TEXT == target._text_restore
        # Test: edit button is not active
        target._button_edit.clicked()
        assert BLANK == target._text_restore

    @pytest.mark.parametrize('NAME_PROP, NAME_ATTR', [
        ('ui_view', '_ui_view'),
        ])
    def test_property_access(
            self, setup_views_markup, NAME_PROP, NAME_ATTR):
        """Confirm access limits of each property.

        :param NAME_PROP: name of property.
        :param NAME_ATTR: name of attribute for property.
        """
        # Setup
        DISPLAY, EDITOR = setup_views_markup
        target = VMARKUP.ViewMarkup(p_display=DISPLAY, p_editor=EDITOR)
        attr = getattr(target, NAME_ATTR)
        CLASS = VMARKUP.ViewMarkup
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert attr == target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None
