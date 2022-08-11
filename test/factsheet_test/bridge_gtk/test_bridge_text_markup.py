"""
Unit tests for bridge classes for text with `Pango markup`_.
See :mod:`.bridge_text_markup`.

.. _Pango markup:
    https://docs.gtk.org/Pango/pango_markup.html

.. include:: /test/refs_include_pytest.txt
"""
import gi  # type: ignore[import]
import logging
from pathlib import Path
import pickle
import pytest

import factsheet.bridge_gtk.bridge_text_markup as BMARKUP
import factsheet.view.ui as VUI

from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # noqa: E402


class TestEditorTextMarkup:
    """Unit tests for :class:`.EditorTextMarkup`."""

    def test_ui_definition(self):
        """Confirm visual element definition."""
        # Setup
        N_WIDTH_EDIT = 45
        NAME_ICON_PRIMARY = 'emblem-default-symbolic'
        TOOLTIP_PRIMARY = 'Click to accept changes.'
        NAME_ICON_SECONDARY = 'edit-delete-symbolic'
        TOOLTIP_SECONDARY = 'Click to cancel changes.'
        get_object = VUI.GetUiElementByStr(
            p_string_ui=BMARKUP.EditorTextMarkup._UI_DEFINITION)
        # Test
        target = get_object('ui_view')
        assert Gtk.Align.START == target.get_halign()
        assert N_WIDTH_EDIT == target.get_width_chars()
        assert NAME_ICON_PRIMARY == target.get_icon_name(
            Gtk.EntryIconPosition.PRIMARY)
        assert TOOLTIP_PRIMARY == target.get_icon_tooltip_markup(
            Gtk.EntryIconPosition.PRIMARY)
        assert NAME_ICON_SECONDARY == target.get_icon_name(
            Gtk.EntryIconPosition.SECONDARY)
        assert TOOLTIP_SECONDARY == target.get_icon_tooltip_markup(
            Gtk.EntryIconPosition.SECONDARY)

    def test_init(self):
        """Confirm initialization."""
        # Setup
        MODEL = BMARKUP.ModelTextMarkup()
        # Test
        target = BMARKUP.EditorTextMarkup(p_model=MODEL)
        assert isinstance(target._ui_view, BMARKUP.UiEditorTextMarkup)
        assert target._ui_view.get_buffer() is MODEL.ui_model

    @pytest.mark.parametrize('NAME_PROP, NAME_ATTR', [
        ('ui_view', '_ui_view'),
        ])
    def test_property_access(self, NAME_PROP, NAME_ATTR):
        """Confirm access limits of each property.

        :param NAME_PROP: name of property.
        :param NAME_ATTR: name of attribute for property.
        """
        # Setup
        MODEL = BMARKUP.ModelTextMarkup()
        target = BMARKUP.EditorTextMarkup(p_model=MODEL)
        attr = getattr(target, NAME_ATTR)
        CLASS = BMARKUP.EditorTextMarkup
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert attr == target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None


class TestModelTextMarkup:
    """Unit tests for :class:`.ModelTextMarkup`."""

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format.

        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        source = BMARKUP.ModelTextMarkup()
        TEXT = 'Something completely different'
        source._set_persist(TEXT)
        source._stale = True
        # Test
        with PATH.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert source._get_persist() == target._get_persist()
        assert not target._stale

    def test_init(self):
        """Confirm initialization."""
        # Setup
        BLANK = ''
        # Test
        target = BMARKUP.ModelTextMarkup()
        assert target._stale is not None
        assert not target._stale
        assert isinstance(target._ui_model, Gtk.EntryBuffer)
        assert BLANK == target._ui_model.get_text()

    def test_get_persist(self):
        """Confirm export to persistent form."""
        # Setup
        target = BMARKUP.ModelTextMarkup()
        TEXT = 'The Parrot Sketch.'
        ALL = -1
        target._ui_model.set_text(TEXT, ALL)
        # Test
        assert TEXT == target._get_persist()

    @pytest.mark.parametrize('NAME_SIGNAL, N_DEFAULT', [
        ('deleted-text', 0),
        ('inserted-text', 0),
        ])
    def test_new_model(self, NAME_SIGNAL, N_DEFAULT):
        """Confirm GTK model with signal connections.

        :param NAME_SIGNAL: signal under test.
        :param N_DEFAULT: number of default handlers for signal.
        """
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(Gtk.EntryBuffer))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        NO_SIGNAL = 0
        # Test
        target = BMARKUP.ModelTextMarkup()
        assert isinstance(target._ui_model, Gtk.EntryBuffer)
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                target._ui_model, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if NO_SIGNAL == id_signal:
                break
            n_handlers += 1
            GO.signal_handler_disconnect(target._ui_model, id_signal)
        assert (N_DEFAULT + 1) == n_handlers

    def test_set_persist(self):
        """Confirm import from persistent form."""
        # Setup
        target = BMARKUP.ModelTextMarkup()
        target_buffer = target._ui_model
        TEXT = 'The Parrot Sketch.'
        ALL = -1
        target._ui_model.set_text(TEXT, ALL)
        target.set_fresh()
        TEXT_NEW = 'Something completely different.'
        # Test
        target._set_persist(TEXT_NEW)
        assert target._ui_model is target_buffer
        assert TEXT_NEW == target._ui_model.get_text()
        assert target.is_stale()


class TestModule:
    """Unit tests for module-level components of :mod:`.bridge_text_markup`."""

    def test_globals(self):
        """Confirm global definitions."""
        # Setup
        # Test
        assert isinstance(BMARKUP.logger, logging.Logger)

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (BMARKUP.ButtonEdit, Gtk.MenuButton),
        (BMARKUP.DisplayTextMarkup, Gtk.Label),
        (BMARKUP.UiAnchor, Gtk.Widget),
        (BMARKUP.UiEditorTextMarkup, Gtk.Entry),
        (BMARKUP.UiLabel, Gtk.Label),
        (BMARKUP.UiPopoverEditorMarkup, Gtk.Popover),
        (BMARKUP.UiTextMarkup, Gtk.EntryBuffer),
        (BMARKUP.UiSite, Gtk.Box),
        (BMARKUP.ViewDuoTextMarkup, Gtk.Box),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type alias definitions.

        :param TYPE_TARGET: type alias under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT


class TestPairViewDuoTextMarkup:
    """Unit tests for :class:`.PairViewDuoTextMarkup`."""

    def test_constants(self):
        """Confirm constant definitions."""
        # Setup
        # Test
        assert isinstance(
            BMARKUP.PairViewDuoTextMarkup._DEF_VIEW_DUO, str)

    def test_init(self):
        """| Confirm initialization.
        | Case: direct attribute initialization.
        """
        # Setup
        model = BMARKUP.ModelTextMarkup()
        LABEL = 'Parrot'
        # Test
        target = BMARKUP.PairViewDuoTextMarkup(
            p_model=model, p_label=LABEL)
        assert target._model is model
        assert isinstance(target._ui_view, BMARKUP.ViewDuoTextMarkup)

    @pytest.mark.parametrize('HELPER', [
        'fill_display',
        'fill_label',
        'fill_popup_editor',
        ])
    def test_init_delegate(self, HELPER, monkeypatch):
        """| Confirm initialization.
        | Case: delegated attribute initialization calls.

        :param HELPER: name of helper method under test.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        called_helper = False

        def helper(self, *_args, **_kwargs):
            nonlocal called_helper
            called_helper = True  # pylint: disable=unused-variable

        monkeypatch.setattr(
            BMARKUP.PairViewDuoTextMarkup, HELPER, helper)
        model = BMARKUP.ModelTextMarkup()
        LABEL = 'Parrot'
        # Test
        _target = BMARKUP.PairViewDuoTextMarkup(
            p_model=model, p_label=LABEL)
        assert called_helper

    def test_fill_display(self):
        """Confirm display populated in view duo."""
        # Setup
        model = BMARKUP.ModelTextMarkup()
        LABEL = 'Parrot'
        target = BMARKUP.PairViewDuoTextMarkup(
            p_model=model, p_label=LABEL)
        get_object = VUI.GetUiElementByStr(
            p_string_ui=BMARKUP.PairViewDuoTextMarkup._DEF_VIEW_DUO)
        site_display = get_object('site_display')
        FIRST = 0
        N_PADDING = 6
        # Test
        target.fill_display(get_object)
        display = site_display.get_children()[FIRST]
        assert isinstance(display, BMARKUP.DisplayTextMarkup)
        expand, fill, padding, pack_type = (
            site_display.query_child_packing(display))
        assert expand
        assert fill
        assert N_PADDING == padding
        assert pack_type is Gtk.PackType.START
        assert display.get_visible()

    def test_fill_label(self):
        """Confirm label populated in view duo."""
        # Setup
        model = BMARKUP.ModelTextMarkup()
        LABEL = 'Parrot'
        EXPECT = '<b>' + LABEL + '</b>:'
        target = BMARKUP.PairViewDuoTextMarkup(
            p_model=model, p_label=LABEL)
        get_object = VUI.GetUiElementByStr(
            p_string_ui=BMARKUP.PairViewDuoTextMarkup._DEF_VIEW_DUO)
        # Test
        target.fill_label(get_object, LABEL)
        label_duo = get_object('label_duo')
        assert EXPECT == label_duo.get_label()

    @pytest.mark.skip(reason='Adding EditorTExtMarkup')
    def test_fill_popup_editor(self):
        """Confirm editor popup populated in view duo."""
        # Setup
        model = BMARKUP.ModelTextMarkup()
        LABEL = 'Parrot'
        target = BMARKUP.PairViewDuoTextMarkup(
            p_model=model, p_label=LABEL)
        get_object = VUI.GetUiElementByStr(
            p_string_ui=BMARKUP.PairViewDuoTextMarkup._DEF_VIEW_DUO)
        site_editor = get_object('site_editor')
        FIRST = 0
        N_PADDING = 6
        # Test
        target.fill_popup_editor(get_object)
        editor = site_editor.get_children()[FIRST]
        assert isinstance(editor, BMARKUP.EditorTextMarkup)
        expand, fill, padding, pack_type = (
            site_editor.query_child_packing(editor))
        assert expand
        assert fill
        assert N_PADDING == padding
        assert pack_type is Gtk.PackType.START
        assert editor.get_visible()

    @pytest.mark.parametrize(
        'ORIGIN, NAME_SIGNAL, LOCATION, IS_SITE, N_DEFAULT', [
            (Gtk.Entry, 'activate', 'site_editor', True, 0),
            (Gtk.Entry, 'icon_press', 'site_editor', True, 0),
            (Gtk.MenuButton, 'toggled', 'button_edit', False, 0),
            ])
    def test_fill_popup_editor_signals(
            self, ORIGIN, NAME_SIGNAL, LOCATION, IS_SITE, N_DEFAULT):
        """| Confirm popup editor signal connection.

        :param ORIGIN: GTK class origin of signal.
        :param NAME_SIGNAL: name of signal to check.
        :param LOCATION: location of object in builder.
        :param IS_SITE: True when location is site containing object.
        :param N_DEFAULT: count of default signal handlers.
        """
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        model = BMARKUP.ModelTextMarkup()
        LABEL = 'Parrot'
        target = BMARKUP.PairViewDuoTextMarkup(
            p_model=model, p_label=LABEL)
        get_object = VUI.GetUiElementByStr(
            p_string_ui=BMARKUP.PairViewDuoTextMarkup._DEF_VIEW_DUO)
        target.fill_popup_editor(get_object)
        if IS_SITE:
            site = get_object(LOCATION)
            FIRST = 0
            ui_view = site.get_children()[FIRST]
        else:
            ui_view = get_object(LOCATION)
        # Test
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                ui_view, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(ui_view, id_signal)

        assert N_DEFAULT + 1 == n_handlers

    @pytest.mark.parametrize('ICON, EXPECT_TEXT', [
        (Gtk.EntryIconPosition.SECONDARY, 'The Parrot Sketch'),
        (Gtk.EntryIconPosition.PRIMARY, 'Something completely different'),
        ])
    def test_on_icon_press(self, ICON, EXPECT_TEXT):
        """Confirm text restored before ending edit.

        Cases cover primary icon (accept edits) and secondary icon
        (cancel edits).

        :param ICON: icon under test.
        :param EXPECT_TEXT: text expected in editor.
        """
        # Setup
        model = BMARKUP.ModelTextMarkup()
        LABEL = 'Parrot'
        target = BMARKUP.PairViewDuoTextMarkup(
            p_model=model, p_label=LABEL)
        TEXT_RESTORE = 'The Parrot Sketch'
        target._text_restore = TEXT_RESTORE
        TEXT_EDITED = 'Something completely different'
        editor = Gtk.Entry(text=TEXT_EDITED)
        EVENT = None
        button_edit = BMARKUP.ButtonEdit()
        button_edit.clicked()
        # Test
        target.on_icon_press(editor, ICON, EVENT, button_edit)
        assert not button_edit.get_active()
        assert EXPECT_TEXT == editor.get_text()

    @pytest.mark.parametrize('ACTIVE, TEXT_EXPECT', [
        (True, 'Something completely different'),
        (False, ''),
        ])
    def test_on_toggle(self, ACTIVE, TEXT_EXPECT):
        """Confirm record of restore text and clear of restore text.

        :param ACTIVE: whether edit button is active.
        :param TEXT_EXPECT: expected restore text.
        """
        # Setup
        model = BMARKUP.ModelTextMarkup()
        LABEL = 'Parrot'
        target = BMARKUP.PairViewDuoTextMarkup(
            p_model=model, p_label=LABEL)
        TEXT_RESTORE = 'Oops!'
        target._text_restore = TEXT_RESTORE
        TEXT_EDITED = 'Something completely different'
        editor = Gtk.Entry(text=TEXT_EDITED)
        editor.set_text(TEXT_EDITED)
        button_edit = BMARKUP.ButtonEdit()
        button_edit.set_active(ACTIVE)
        # Test
        target.on_toggled(button_edit, editor)
        assert TEXT_EXPECT == target._text_restore

    @pytest.mark.parametrize('NAME_PROP, NAME_ATTR', [
        ('model', '_model'),
        ('ui_view', '_ui_view'),
        ])
    def test_property_access(self, NAME_PROP, NAME_ATTR):
        """Confirm access limits of each property.

        :param NAME_PROP: name of property.
        :param NAME_ATTR: name of attribute for property.
        """
        # Setup
        model = BMARKUP.ModelTextMarkup()
        LABEL = 'Parrot'
        target = BMARKUP.PairViewDuoTextMarkup(
            p_model=model, p_label=LABEL)
        attr = getattr(target, NAME_ATTR)
        CLASS = BMARKUP.PairViewDuoTextMarkup
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert attr == target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None


class TestPopoverEditorMarkup:
    """Unit tests for :class:`.PopoverEditorMarkup`."""

    def test_ui_definition(self):
        """Confirm visual element definition."""
        # Setup
        N_SPACING = 6
        TEXT = '<b>Oops!</b>'
        get_object = VUI.GetUiElementByStr(
            p_string_ui=BMARKUP.PopoverEditorMarkup._UI_DEFINITION)
        # Test
        ui_view = get_object('ui_view')
        assert isinstance(ui_view, BMARKUP.UiPopoverEditorMarkup)
        site_editor = get_object('site_editor')
        assert isinstance(site_editor, BMARKUP.UiSite)
        assert N_SPACING == site_editor.get_spacing()
        ui_label = get_object('ui_label')
        assert isinstance(ui_label, BMARKUP.UiLabel)
        assert TEXT == ui_label.get_label()
        assert ui_label.get_use_markup()

    def test_init(self):
        """Confirm initialization."""
        # Setup
        model = BMARKUP.ModelTextMarkup()
        I_EDITOR = 1
        PACK_TYPE = int(Gtk.PackType.START)
        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 0
        # Test
        target = BMARKUP.PopoverEditorMarkup(p_model=model)
        assert isinstance(target._ui_view, BMARKUP.UiPopoverEditorMarkup)
        assert isinstance(target._ui_editor, BMARKUP.UiEditorTextMarkup)
        assert target._ui_editor.get_buffer() is model.ui_model
        site_editor = target._ui_view.get_child()
        editor = site_editor.get_children()[I_EDITOR]
        pack_type, expand, fill, padding = site_editor.child_get(
            editor, 'pack-type', 'expand', 'fill', 'padding')
        assert pack_type is PACK_TYPE
        assert expand is EXPAND_OKAY
        assert fill is FILL_OKAY
        assert N_PADDING == padding
        assert target._ui_editor is editor
        assert isinstance(target._ui_label, BMARKUP.UiLabel)

    @pytest.mark.parametrize('NAME_PROP, NAME_ATTR', [
        ('ui_editor', '_ui_editor'),
        ('ui_label', '_ui_label'),
        ('ui_view', '_ui_view'),
        ])
    def test_property_access(self, NAME_PROP, NAME_ATTR):
        """Confirm access limits of each property.

        :param NAME_PROP: name of property.
        :param NAME_ATTR: name of attribute for property.
        """
        # Setup
        model = BMARKUP.ModelTextMarkup()
        target = BMARKUP.PopoverEditorMarkup(p_model=model)
        attr = getattr(target, NAME_ATTR)
        CLASS = BMARKUP.PopoverEditorMarkup
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert attr == target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None

    def test_set_anchor(self):
        """Confirm anchor is set."""
        # Setup
        model = BMARKUP.ModelTextMarkup()
        target = BMARKUP.PopoverEditorMarkup(p_model=model)
        BUTTON = Gtk.MenuButton()
        # Test
        target.set_anchor(p_anchor=BUTTON)
        assert target._ui_view.get_relative_to() is BUTTON

    def test_set_label(self):
        """Confirm identifying text is set."""
        # Setup
        model = BMARKUP.ModelTextMarkup()
        target = BMARKUP.PopoverEditorMarkup(p_model=model)
        TEXT = '<i>The Parrot Sketch</i>'
        # Test
        target.set_label(p_text=TEXT)
        assert TEXT == target._ui_label.get_label()
