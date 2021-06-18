"""
Unit tests for classes to display identity information.  See
:mod:`.view_idcore`.
"""
import pytest   # type: ignore[import]

import factsheet.control.control_sheet as CSHEET
import factsheet.view.view_idcore as VIDCORE

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import] # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@pytest.fixture
def setup_views_markup():
    """Fixture with teardown: return passive and active views of markup."""
    PATH = None
    control = CSHEET.g_roster_factsheets.open_factsheet(p_path=PATH)
    view_passive = control.new_view_name_passive()
    view_active = control.new_view_name_active()
    yield view_passive, view_active
    view_passive.destroy()
    view_active.destroy()


class TestEditorMarkup:
    """Unit tests for :class:`.EditorMarkup`."""

    def test_init(self, setup_views_markup):
        """| Confirm initialization.
        | Case: view settings and attributes

        :param setup_views_markup: fixture :func:`.setup_views_markup`.
        """
        # Setup
        view_passive, view_active = setup_views_markup
        I_SITE_VIEW_PASSIVE = 1
        I_VIEW_PASSIVE = 0
        N_PADDING = 6
        I_BUTTON_EDIT = 0
        I_VIEW_ACTIVE = 0
        TYPE = 'Parrot'
        TYPE_MARKED = '<b>' + TYPE + '</b>:'
        # Test
        target = VIDCORE.EditorMarkup(p_view_passive=view_passive,
                                      p_view_active=view_active, p_type=TYPE)
        children_editor = target._view_editor.get_children()
        assert target._buffer is view_active.get_buffer()
        assert isinstance(target._button_edit, Gtk.MenuButton)
        assert isinstance(target._popover, Gtk.Popover)
        assert '' == target._text_restore
        assert isinstance(target._view_editor, Gtk.Box)

        site_view_passive = children_editor[I_SITE_VIEW_PASSIVE]
        assert isinstance(site_view_passive, Gtk.Box)
        assert view_passive is (
            site_view_passive.get_children()[I_VIEW_PASSIVE])
        expand_passive, fill_passive, padding_passive, _pack = (
            site_view_passive.query_child_packing(view_passive))
        assert expand_passive
        assert fill_passive
        assert N_PADDING == padding_passive
        assert view_passive.get_visible()

        button_edit = children_editor[I_BUTTON_EDIT]
        popover_edit = button_edit.get_popover()
        box_popover = popover_edit.get_child()
        label_type, site_view_active = box_popover.get_children()
        assert TYPE_MARKED == label_type.get_label()
        assert isinstance(site_view_active, Gtk.Box)
        assert view_active is (
            site_view_active.get_children()[I_VIEW_ACTIVE])
        expand_active, fill_active, padding_active, _pack = (
            site_view_active.query_child_packing(view_active))
        assert expand_active
        assert fill_active
        assert N_PADDING == padding_active
        assert view_active.get_visible()

    @pytest.mark.parametrize(
        'NAME_SIGNAL, NAME_ATTR, ORIGIN, N_DEFAULT', [
            ('toggled', '_button_edit', Gtk.MenuButton, 0),
            ])
    def test_init_signals_attr(self, setup_views_markup,
                               NAME_SIGNAL, NAME_ATTR, ORIGIN, N_DEFAULT):
        """| Confirm initialization.
        | Case: signal connections to attributes

        :param setup_views_markup: fixture :func:`.setup_views_markup`.
        :param NAME_SIGNAL: name of signal to check.
        :param NAME_ATTR: attribute generating signal.
        :param ORIGIN: GTK class origin of signal.
        :param N_DEFAULT: count of default signal handlers.
        """
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        view_passive, view_active = setup_views_markup
        target = VIDCORE.EditorMarkup(
            p_view_passive=view_passive, p_view_active=view_active)
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
    def test_init_signals_view_active(
            self, setup_views_markup, NAME_SIGNAL, ORIGIN, N_DEFAULT):
        """| Confirm initialization.
        | Case: signal connections to active view

        :param setup_views_markup: fixture :func:`.setup_views_markup`.
        :param NAME_SIGNAL: name of signal to check.
        :param ORIGIN: GTK class origin of signal.
        :param N_DEFAULT: count of default signal handlers.
        """
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        view_passive, view_active = setup_views_markup
        _target = VIDCORE.EditorMarkup(
            p_view_passive=view_passive, p_view_active=view_active)
        # Test
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                view_active, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(view_active, id_signal)

        assert N_DEFAULT + 1 == n_handlers

    @pytest.mark.parametrize('ICON, EXPECT_TEXT', [
        (Gtk.EntryIconPosition.PRIMARY, 'Something completely different'),
        (Gtk.EntryIconPosition.SECONDARY, ''),
        ])
    def test_on_icon_press(self, setup_views_markup, ICON, EXPECT_TEXT):
        """Confirm text restored before ending edit.

        #. Case: primary icon
        #. Case: secondary icon

        :param setup_views_markup: fixture :func:`.setup_views_markup`.
        :param ICON: icon to check.
        :param EXPECT_TEXT: text expected in buffer.
        """
        # Setup
        view_passive, view_active = setup_views_markup
        target = VIDCORE.EditorMarkup(
            p_view_passive=view_passive, p_view_active=view_active)
        TEXT = 'Something completely different'
        target._buffer.set_text(TEXT, len(TEXT))
        target._button_edit.clicked()
        BLANK = ''
        target._text_restore = BLANK
        # Test: primary icon
        target.on_icon_press(None, ICON, None)
        assert not target._button_edit.get_active()
        assert EXPECT_TEXT == target._buffer.get_text()

    def test_on_toggle(self, setup_views_markup):
        """Confirm record and clear of restored text.

        #. Case: edit button is active
        #. Case: edit button is not active

        :param setup_views_markup: fixture :func:`.setup_views_markup`.
        """
        # Setup
        view_passive, view_active = setup_views_markup
        target = VIDCORE.EditorMarkup(
            p_view_passive=view_passive, p_view_active=view_active)
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
        ('view_editor', '_view_editor'),
        ])
    def test_property_access(
            self, setup_views_markup, NAME_PROP, NAME_ATTR):
        """Confirm access limits of each property.

        :param NAME_PROP: name of property.
        :param NAME_ATTR: name of attribute for property.
        """
        # Setup
        view_passive, view_active = setup_views_markup
        target = VIDCORE.EditorMarkup(
            p_view_passive=view_passive, p_view_active=view_active)
        attr = getattr(target, NAME_ATTR)
        CLASS = VIDCORE.EditorMarkup
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert attr == target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None
