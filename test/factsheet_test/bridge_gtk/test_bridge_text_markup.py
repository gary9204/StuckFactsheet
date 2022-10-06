"""
Unit tests for bridge classes for text with `Pango markup`_.
See :mod:`.bridge_text_markup`.

.. _Pango markup:
    https://docs.gtk.org/Pango/pango_markup.html

.. include:: /test/refs_include_pytest.txt
"""
import gi  # type: ignore[import]
import logging
import math
from pathlib import Path
import pickle
import pytest

import factsheet.bridge_gtk.bridge_text_markup as BMARKUP
import factsheet.view.ui as VUI

from gi.repository import GLib  # type: ignore[import]  # noqa: E402
from gi.repository import GObject as GO  # noqa: E402
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # noqa: E402
from gi.repository import Pango   # noqa: E402


class TestDisplayTextMarkup:
    """Unit tests for :class:`.DisplayTextMarkup`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        TEXT = '<i>The Parrot Sketch</i>'
        MODEL = BMARKUP.x_b_tm_ModelTextMarkup()
        MODEL.text = TEXT
        # Test
        target = BMARKUP.DisplayTextMarkup(p_model=MODEL)
        assert isinstance(target._ui_view, BMARKUP.UiDisplayTextMarkup)
        assert TEXT == target._ui_view.get_label()
        assert target._id_delete
        assert GO.signal_handler_is_connected(
            MODEL.ui_model, target._id_delete)
        assert target._id_insert
        assert GO.signal_handler_is_connected(
            MODEL.ui_model, target._id_insert)

    @pytest.mark.parametrize('NAME_SIGNAL, ORIGIN, N_DEFAULT', [
            ('destroy', BMARKUP.UiDisplayTextMarkup, 0),
            ])
    def test_init_signals_view(self, NAME_SIGNAL, ORIGIN, N_DEFAULT):
        """| Confirm initialization.
        | Case: signal connections to visual element.

        :param NAME_SIGNAL: name of signal to check.
        :param ORIGIN: GTK class origin of signal.
        :param N_DEFAULT: count of default signal handlers.
        """
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        MODEL = BMARKUP.x_b_tm_ModelTextMarkup()
        target = BMARKUP.DisplayTextMarkup(p_model=MODEL)
        # Test
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                target._ui_view, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(target._ui_view, id_signal)

        assert N_DEFAULT + 1 == n_handlers

    def test_on_change(self):
        """Confirm refresh of display views."""
        # Setup
        MODEL = BMARKUP.x_b_tm_ModelTextMarkup()
        target = BMARKUP.DisplayTextMarkup(p_model=MODEL)
        PATCH_MODEL = BMARKUP.x_b_tm_ModelTextMarkup()
        PATCH_TEXT = '<i>The Parrot Sketch'
        PATCH_MODEL.text = PATCH_TEXT
        PATCH_ESCAPED = GLib.markup_escape_text(PATCH_TEXT, len(PATCH_TEXT))
        # Test
        target.on_change(PATCH_MODEL.ui_model, None, None)
        assert PATCH_ESCAPED == target._ui_view.get_label()

    @pytest.mark.parametrize('ATTR_ID_HANDLER', [
        '_id_delete',
        '_id_insert',
        ])
    def test_on_destroy(self, ATTR_ID_HANDLER):
        """Confirm initialization."""
        # Setup
        TEXT = '<i>The Parrot Sketch</i>'
        MODEL = BMARKUP.x_b_tm_ModelTextMarkup()
        MODEL.text = TEXT
        target = BMARKUP.DisplayTextMarkup(p_model=MODEL)
        ui_model = MODEL.ui_model
        ui_view = target._ui_view
        id_handler = getattr(target, ATTR_ID_HANDLER)
        ID_INVALID = 0
        # Test
        target.on_destroy(ui_view, ui_model)
        assert not hasattr(target, '_ui_view')
        assert ID_INVALID == getattr(target, ATTR_ID_HANDLER)
        assert not GO.signal_handler_is_connected(ui_model, id_handler)

    @pytest.mark.parametrize('NAME_PROP, NAME_ATTR', [
        ('ui_view', '_ui_view'),
        ])
    def test_property_access(self, NAME_PROP, NAME_ATTR):
        """Confirm access limits of each property.

        :param NAME_PROP: name of property.
        :param NAME_ATTR: name of attribute for property.
        """
        # Setup
        TEXT = '<i>The Parrot Sketch</i>'
        MODEL = BMARKUP.x_b_tm_ModelTextMarkup()
        MODEL.text = TEXT
        target = BMARKUP.DisplayTextMarkup(p_model=MODEL)
        attr = getattr(target, NAME_ATTR)
        CLASS = BMARKUP.DisplayTextMarkup
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert attr == target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None

    def test_ui_definition(self):
        """Confirm visual element definition."""
        # Setup
        N_WIDTH_DISPLAY = 15
        XALIGN = 0
        get_object = VUI.GetUiElementByStr(
            p_string_ui=BMARKUP.DisplayTextMarkup._UI_DEFINITION)
        # Test
        target = get_object('ui_view')
        assert target.get_visible()
        assert Gtk.Align.START == target.get_halign()
        assert target.get_use_markup()
        assert target.get_selectable()
        assert Pango.EllipsizeMode.END == target.get_ellipsize()
        assert N_WIDTH_DISPLAY == target.get_width_chars()
        assert math.isclose(XALIGN, target.get_xalign())


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
        MODEL = BMARKUP.x_b_tm_ModelTextMarkup()
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
        MODEL = BMARKUP.x_b_tm_ModelTextMarkup()
        target = BMARKUP.EditorTextMarkup(p_model=MODEL)
        attr = getattr(target, NAME_ATTR)
        CLASS = BMARKUP.EditorTextMarkup
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert attr == target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None


class TestEscapeTextMarkup:
    """Unit tests for function :func:`.x_b_tm_escape_text_markup`."""

    def test_escape_text_markup(self):
        """| Confirm markup errors escaped.
        | Case: text does not contain markup error.
        """
        # Setup
        TEXT = 'The <b>Parrot Sketch.</b>'
        TEXT_ESCAPED = TEXT
        # Test
        assert TEXT_ESCAPED == BMARKUP.x_b_tm_escape_text_markup(TEXT)

    def test_escape_text_markup_error(self):
        """| Confirm markup errors escaped.
        | Case: text contains markup error.
        """
        # Setup
        TEXT = 'The <b>Parrot </b Sketch.'
        TEXT_ESCAPED = GLib.markup_escape_text(TEXT, len(TEXT))
        # Test
        assert TEXT_ESCAPED == BMARKUP.x_b_tm_escape_text_markup(TEXT)

    def test_escape_text_markup_except(self, monkeypatch):
        """| Confirm markup errors escaped.
        | Case: GLib error that is not a markup error.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        QUARK = GLib.unix_error_quark()
        DOMAIN = GLib.quark_to_string(QUARK)
        MESSAGE = 'Oops'
        CODE = 42

        def patch_parse(_text, _len, _marker):
            raise GLib.Error.new_literal(QUARK, MESSAGE, CODE)

        monkeypatch.setattr(Pango, 'parse_markup', patch_parse)

        TEXT = 'The <b>Parrot </b Sketch.'
        # Test
        with pytest.raises(GLib.Error) as exc_info:
            _ = BMARKUP.x_b_tm_escape_text_markup(TEXT)
        exc = exc_info.value
        assert DOMAIN == exc.domain
        assert MESSAGE == exc.message
        assert CODE == exc.code


class TestModelTextMarkup:
    """Unit tests for :class:`.x_b_tm_ModelTextMarkup`."""

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format.

        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        source = BMARKUP.x_b_tm_ModelTextMarkup()
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
        target = BMARKUP.x_b_tm_ModelTextMarkup()
        assert target._stale is not None
        assert not target._stale
        assert isinstance(target._ui_model, Gtk.EntryBuffer)
        assert BLANK == target._ui_model.get_text()

    def test_get_persist(self):
        """Confirm export to persistent form."""
        # Setup
        target = BMARKUP.x_b_tm_ModelTextMarkup()
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
        target = BMARKUP.x_b_tm_ModelTextMarkup()
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
        target = BMARKUP.x_b_tm_ModelTextMarkup()
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
        (BMARKUP.UiButtonTrigger, Gtk.MenuButton),
        (BMARKUP.UiDisplayTextMarkup, Gtk.Label),
        (BMARKUP.UiAnchor, Gtk.Widget),
        (BMARKUP.UiEditorTextMarkup, Gtk.Entry),
        (BMARKUP.UiLabel, Gtk.Label),
        (BMARKUP.UiPopoverEditorMarkup, Gtk.Popover),
        (BMARKUP.UiTextMarkup, Gtk.EntryBuffer),
        (BMARKUP.UiSite, Gtk.Box),
        (BMARKUP.UiViewDuoMarkup, Gtk.Box),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type alias definitions.

        :param TYPE_TARGET: type alias under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT


class TestPopoverEditorMarkup:
    """Unit tests for :class:`.PopupEditorMarkup`."""

    def test_ui_definition(self):
        """Confirm visual element definition."""
        # Setup
        N_SPACING = 6
        TEXT = '<b>Oops!</b>'
        get_object = VUI.GetUiElementByStr(
            p_string_ui=BMARKUP.PopupEditorMarkup._UI_DEFINITION)
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
        model = BMARKUP.x_b_tm_ModelTextMarkup()
        I_EDITOR = 1
        PACK_TYPE = int(Gtk.PackType.START)
        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 0
        # Test
        target = BMARKUP.PopupEditorMarkup(p_model=model)
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
        model = BMARKUP.x_b_tm_ModelTextMarkup()
        target = BMARKUP.PopupEditorMarkup(p_model=model)
        attr = getattr(target, NAME_ATTR)
        CLASS = BMARKUP.PopupEditorMarkup
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert attr == target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None

    def test_set_anchor(self):
        """Confirm anchor is set."""
        # Setup
        model = BMARKUP.x_b_tm_ModelTextMarkup()
        target = BMARKUP.PopupEditorMarkup(p_model=model)
        BUTTON = Gtk.MenuButton()
        # Test
        target.set_anchor(p_anchor=BUTTON)
        assert target._ui_view.get_relative_to() is BUTTON

    def test_set_label(self):
        """Confirm identifying text is set."""
        # Setup
        model = BMARKUP.x_b_tm_ModelTextMarkup()
        target = BMARKUP.PopupEditorMarkup(p_model=model)
        TEXT = '<i>The Parrot Sketch</i>'
        # Test
        target.set_label(p_text=TEXT)
        assert TEXT == target._ui_label.get_label()


class TestViewDuoMarkup:
    """Unit tests for :class:`.ViewDuoMarkup`."""

    def test_ui_definition(self):
        """Confirm visual element definition."""
        # Setup
        get_object = VUI.GetUiElementByStr(
            p_string_ui=BMARKUP.ViewDuoMarkup._UI_DEFINITION)
        N_SPACING = 6
        I_BUTTON = 0
        # Test
        ui_view = get_object('ui_view')
        assert isinstance(ui_view, BMARKUP.UiViewDuoMarkup)
        assert N_SPACING == ui_view.get_spacing()
        button = ui_view.get_children()[I_BUTTON]
        assert isinstance(button, BMARKUP.UiButtonTrigger)

    def test_init(self):
        """| Confirm initialization.
        | Case: direct attribute initialization.
        """
        # Setup
        model = BMARKUP.x_b_tm_ModelTextMarkup()
        LABEL = 'Sketch'
        BLANK = ''
        # Test
        target = BMARKUP.ViewDuoMarkup(p_model=model, p_label=LABEL)
        assert BLANK == target._text_restore
        assert isinstance(target._ui_view, BMARKUP.UiViewDuoMarkup)
        assert isinstance(target._ui_button, BMARKUP.UiButtonTrigger)
        assert isinstance(target._display, BMARKUP.DisplayTextMarkup)
        assert isinstance(target._popup, BMARKUP.PopupEditorMarkup)
        assert LABEL == target._popup.ui_label.get_label()

    @pytest.mark.parametrize('HELPER', [
        'fill_display',
        'link_popup',
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
            BMARKUP.ViewDuoMarkup, HELPER, helper)
        model = BMARKUP.x_b_tm_ModelTextMarkup()
        LABEL = 'Parrot'
        # Test
        _target = BMARKUP.ViewDuoMarkup(
            p_model=model, p_label=LABEL)
        assert called_helper

    def test_fill_display(self):
        """Confirm display populated in view duo."""
        # Setup
        model = BMARKUP.x_b_tm_ModelTextMarkup()
        LABEL = 'Sketch'
        target = BMARKUP.ViewDuoMarkup(p_model=model, p_label=LABEL)
        PATCH_UI_DISPLAY = BMARKUP.UiDisplayTextMarkup()
        target._display._ui_view = PATCH_UI_DISPLAY
        I_DISPLAY = 1
        N_PADDING = 6
        # Test
        target.fill_display()
        display = target._ui_view.get_children()[I_DISPLAY]
        assert isinstance(display, BMARKUP.UiDisplayTextMarkup)
        expand, fill, padding, pack_type = (
            target._ui_view.query_child_packing(display))
        assert expand
        assert fill
        assert N_PADDING == padding
        assert pack_type is Gtk.PackType.START
        assert display.get_visible()

    def test_link_popup(self):
        """Confirm links betwen popup editor to view duo components."""
        # Setup
        model = BMARKUP.x_b_tm_ModelTextMarkup()
        LABEL = 'Sketch'
        target = BMARKUP.ViewDuoMarkup(p_model=model, p_label=LABEL)
        PATCH_UI_BUTTON = BMARKUP.UiButtonTrigger()
        target._ui_button = PATCH_UI_BUTTON
        PATCH_POPUP = BMARKUP.PopupEditorMarkup(model)
        target._popup = PATCH_POPUP
        # Test
        target.link_popup()
        assert PATCH_UI_BUTTON.get_popover() is PATCH_POPUP.ui_view
        assert PATCH_POPUP.ui_view.get_relative_to() is PATCH_UI_BUTTON

    @pytest.mark.parametrize(
        'ORIGIN, NAME_SIGNAL, ATTRS_VIEW, N_DEFAULT', [
            (Gtk.Entry, 'activate', ['_popup', '_ui_editor'], 0),
            (Gtk.Entry, 'icon_press', ['_popup', '_ui_editor'], 0),
            (Gtk.MenuButton, 'toggled', ['_ui_button'], 0),
            ])
    def test_link_popup_signals(
            self, ORIGIN, NAME_SIGNAL, ATTRS_VIEW, N_DEFAULT):
        """| Confirm popup editor signal connection.

        :param ORIGIN: GTK class origin of signal.
        :param NAME_SIGNAL: name of signal to check.
        :param ATTRS_VIEW: list of attributes to reach visual element.
        :param N_DEFAULT: count of default signal handlers.
        """
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        model = BMARKUP.x_b_tm_ModelTextMarkup()
        LABEL = 'Sketch'
        target = BMARKUP.ViewDuoMarkup(p_model=model, p_label=LABEL)
        ui_view = target
        for attr in ATTRS_VIEW:
            ui_view = getattr(ui_view, attr)
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
        model = BMARKUP.x_b_tm_ModelTextMarkup()
        LABEL = 'Sketch'
        target = BMARKUP.ViewDuoMarkup(p_model=model, p_label=LABEL)
        target._ui_button.clicked()
        TEXT_RESTORE = 'The Parrot Sketch'
        target._text_restore = TEXT_RESTORE
        TEXT_EDITED = 'Something completely different'
        target._popup.ui_editor.set_text(TEXT_EDITED)
        EVENT = None
        # Test
        target.on_icon_press(target._popup.ui_editor, ICON, EVENT)
        assert not target._ui_button.get_active()
        assert EXPECT_TEXT == target._popup.ui_editor.get_text()

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
        model = BMARKUP.x_b_tm_ModelTextMarkup()
        LABEL = 'Parrot'
        target = BMARKUP.ViewDuoMarkup(p_model=model, p_label=LABEL)
        TEXT_RESTORE = 'Oops!'
        target._text_restore = TEXT_RESTORE
        TEXT_EDITED = 'Something completely different'
        target._popup.ui_editor.set_text(TEXT_EDITED)
        target._ui_button.set_active(ACTIVE)
        target.on_toggled(target._ui_button, target._popup.ui_editor)
        assert TEXT_EXPECT == target._text_restore

    @pytest.mark.parametrize('NAME_PROP, NAMES_ATTR', [
        ('ui_button', ['_ui_button']),
        ('ui_view', ['_ui_view']),
        ])
    def test_property_access(self, NAME_PROP, NAMES_ATTR):
        """Confirm access limits of each property.

        :param NAME_PROP: name of property.
        :param NAME_ATTR: list of names that identify attribute.
        """
        # Setup
        model = BMARKUP.x_b_tm_ModelTextMarkup()
        LABEL = 'Parrot'
        target = BMARKUP.ViewDuoMarkup(p_model=model, p_label=LABEL)
        attr = target
        for name in NAMES_ATTR:
            attr = getattr(attr, name)
        # attr = getattr(target, NAME_ATTR)
        CLASS = BMARKUP.ViewDuoMarkup
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert attr == target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None
