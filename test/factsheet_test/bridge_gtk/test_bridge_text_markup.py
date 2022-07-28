"""
Unit tests for bridge classes for text with `Pango markup`_.
See :mod:`.bridge_text_markup`.

.. _Pango markup:
    https://docs.gtk.org/Pango/pango_markup.html

.. include:: /test/refs_include_pytest.txt
"""
import gi  # type: ignore[import]
import logging
import pytest

import factsheet.bridge_gtk.bridge_text as BTEXT
import factsheet.bridge_gtk.bridge_text_markup as BTEXT_MARKUP
import factsheet.view.ui as VUI

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]  # noqa: E402
from gi.repository import GObject as GO  # noqa: E402


class TestModule:
    """Unit tests for module-level components of :mod:`.bridge_text_markup`."""

    def test_globals(self):
        """Confirm global definitions."""
        # Setup
        # Test
        assert isinstance(BTEXT_MARKUP.logger, logging.Logger)

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (BTEXT_MARKUP.ButtonEdit, Gtk.MenuButton),
        (BTEXT_MARKUP.DisplayTextMarkup, Gtk.Label),
        (BTEXT_MARKUP.EditorTextMarkup, Gtk.Entry),
        (BTEXT_MARKUP.UiTextMarkup, Gtk.EntryBuffer),
        (BTEXT_MARKUP.ViewDuoTextMarkup, Gtk.Box),
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
            BTEXT_MARKUP.PairViewDuoTextMarkup._DEF_VIEW_DUO, str)

    def test_init(self):
        """| Confirm initialization.
        | Case: attributes set directly.
        """
        # Setup
        model = BTEXT.ModelTextMarkup()
        LABEL = 'Parrot'
        # Test
        target = BTEXT_MARKUP.PairViewDuoTextMarkup(
            p_model=model, p_label=LABEL)
        assert target._model is model
        assert isinstance(target._ui_view, BTEXT_MARKUP.ViewDuoTextMarkup)

    @pytest.mark.parametrize('HELPER', [
        'fill_display',
        'fill_label',
        'fill_popup_editor',
        ])
    def test_init_delegate(self, HELPER, monkeypatch):
        """| Confirm initialization.
        | Case: helper method calls to set attributes.

        :param HELPER: name of helper method under test.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_
        """
        # Setup
        called_helper = False

        def helper(self, *_args, **_kwargs):
            nonlocal called_helper
            called_helper = True  # pylint: disable=unused-variable

        monkeypatch.setattr(
            BTEXT_MARKUP.PairViewDuoTextMarkup, HELPER, helper)
        model = BTEXT.ModelTextMarkup()
        LABEL = 'Parrot'
        # Test
        _target = BTEXT_MARKUP.PairViewDuoTextMarkup(
            p_model=model, p_label=LABEL)
        assert called_helper

    def test_fill_display(self):
        """Confirm display populated in view duo."""
        # Setup
        model = BTEXT.ModelTextMarkup()
        LABEL = 'Parrot'
        target = BTEXT_MARKUP.PairViewDuoTextMarkup(
            p_model=model, p_label=LABEL)
        get_object = VUI.GetUiElementByStr(
            p_string_ui=BTEXT_MARKUP.PairViewDuoTextMarkup._DEF_VIEW_DUO)
        site_display = get_object('site_display')
        FIRST = 0
        N_PADDING = 6
        # Test
        target.fill_display(get_object)
        display = site_display.get_children()[FIRST]
        assert isinstance(display, BTEXT_MARKUP.DisplayTextMarkup)
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
        model = BTEXT.ModelTextMarkup()
        LABEL = 'Parrot'
        EXPECT = '<b>' + LABEL + '</b>:'
        target = BTEXT_MARKUP.PairViewDuoTextMarkup(
            p_model=model, p_label=LABEL)
        get_object = VUI.GetUiElementByStr(
            p_string_ui=BTEXT_MARKUP.PairViewDuoTextMarkup._DEF_VIEW_DUO)
        # Test
        target.fill_label(get_object, LABEL)
        label_duo = get_object('label_duo')
        assert EXPECT == label_duo.get_label()

    def test_fill_popup_editor(self):
        """Confirm editor popup populated in view duo."""
        # Setup
        model = BTEXT.ModelTextMarkup()
        LABEL = 'Parrot'
        target = BTEXT_MARKUP.PairViewDuoTextMarkup(
            p_model=model, p_label=LABEL)
        get_object = VUI.GetUiElementByStr(
            p_string_ui=BTEXT_MARKUP.PairViewDuoTextMarkup._DEF_VIEW_DUO)
        site_editor = get_object('site_editor')
        FIRST = 0
        N_PADDING = 6
        # Test
        target.fill_popup_editor(get_object)
        editor = site_editor.get_children()[FIRST]
        assert isinstance(editor, BTEXT_MARKUP.EditorTextMarkup)
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
        model = BTEXT.ModelTextMarkup()
        LABEL = 'Parrot'
        target = BTEXT_MARKUP.PairViewDuoTextMarkup(
            p_model=model, p_label=LABEL)
        get_object = VUI.GetUiElementByStr(
            p_string_ui=BTEXT_MARKUP.PairViewDuoTextMarkup._DEF_VIEW_DUO)
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
        model = BTEXT.ModelTextMarkup()
        LABEL = 'Parrot'
        target = BTEXT_MARKUP.PairViewDuoTextMarkup(
            p_model=model, p_label=LABEL)
        TEXT_RESTORE = 'The Parrot Sketch'
        target._text_restore = TEXT_RESTORE
        TEXT_EDITED = 'Something completely different'
        editor = Gtk.Entry(text=TEXT_EDITED)
        EVENT = None
        button_edit = BTEXT_MARKUP.ButtonEdit()
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
        model = BTEXT.ModelTextMarkup()
        LABEL = 'Parrot'
        target = BTEXT_MARKUP.PairViewDuoTextMarkup(
            p_model=model, p_label=LABEL)
        TEXT_RESTORE = 'Oops!'
        target._text_restore = TEXT_RESTORE
        TEXT_EDITED = 'Something completely different'
        editor = Gtk.Entry(text=TEXT_EDITED)
        editor.set_text(TEXT_EDITED)
        button_edit = BTEXT_MARKUP.ButtonEdit()
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
        model = BTEXT.ModelTextMarkup()
        LABEL = 'Parrot'
        target = BTEXT_MARKUP.PairViewDuoTextMarkup(
            p_model=model, p_label=LABEL)
        attr = getattr(target, NAME_ATTR)
        CLASS = BTEXT_MARKUP.PairViewDuoTextMarkup
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert attr == target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None
