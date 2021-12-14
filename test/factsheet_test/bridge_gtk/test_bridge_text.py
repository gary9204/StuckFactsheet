"""
Unit tests for GTK-based classes that implement abstract identification
information classes.  See :mod:`.bridge_text`.

.. include:: /test/refs_include_pytest.txt
"""
import gi   # type: ignore[import]
import math
import pickle
import pytest   # type: ignore[import]
import typing

from pathlib import Path

import factsheet.bridge_gtk.bridge_text as BTEXT

gi.require_version('Gtk', '3.0')
from gi.repository import GLib   # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402
from gi.repository import Pango   # type: ignore[import]    # noqa: E402


class PatchModelText(BTEXT.ModelText[typing.Any]):
    """:class:`.ModelText` subclass with stub text property.

        :param args: patch and superclass positional parameters.
        :param kwargs: patch and superclass keyword parameters.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_persist(self):
        return self._ui_model

    def _new_ui_model(self):
        self._ui_model = ''

    def _set_persist(self, p_persist):
        self._ui_model = str(p_persist)


class TestEscapeTextMarkup:
    """Unit tests for function :func:`.escape_text_markup`."""

    def test_escape_text_markup(self):
        """| Confirm markup errors escaped.
        | Case: text does not contain markup error.
        """
        # Setup
        TEXT = 'The <b>Parrot Sketch.</b>'
        TEXT_ESCAPED = TEXT
        # Test
        assert TEXT_ESCAPED == BTEXT.escape_text_markup(TEXT)

    def test_escape_text_markup_error(self):
        """| Confirm markup errors escaped.
        | Case: text contains markup error.
        """
        # Setup
        TEXT = 'The <b>Parrot </b Sketch.'
        TEXT_ESCAPED = GLib.markup_escape_text(TEXT, len(TEXT))
        # Test
        assert TEXT_ESCAPED == BTEXT.escape_text_markup(TEXT)

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
            _ = BTEXT.escape_text_markup(TEXT)
        exc = exc_info.value
        assert DOMAIN == exc.domain
        assert MESSAGE == exc.message
        assert CODE == exc.code


class TestFactoryEditorTextMarkup:
    """Unit tests for :class:`.FactoryEditorTextMarkup`."""

    def test_init(self):
        """Confirm storage initialization."""
        # Setup
        MODEL = BTEXT.ModelTextMarkup()
        # Test
        target = BTEXT.FactoryEditorTextMarkup(p_model=MODEL)
        assert target._ui_model is MODEL._ui_model

    def test_call(self):
        """Confirm return is editable view."""
        # Setup
        NAME_ICON_PRIMARY = 'emblem-default-symbolic'
        NAME_ICON_SECONDARY = 'edit-delete-symbolic'
        TOOLTIP_PRIMARY = 'Click to accept changes.'
        TOOLTIP_SECONDARY = 'Click to cancel changes.'
        N_WIDTH_EDIT = 45
        entry_buffer = BTEXT.ModelTextMarkup()
        target = BTEXT.FactoryEditorTextMarkup(p_model=entry_buffer)
        # Test
        view = target()
        assert isinstance(view, Gtk.Entry)
        assert target._ui_model is view.get_buffer()
        assert Gtk.Align.START == view.get_halign()
        assert NAME_ICON_PRIMARY == (
            view.get_icon_name(Gtk.EntryIconPosition.PRIMARY))
        assert NAME_ICON_SECONDARY == (
            view.get_icon_name(Gtk.EntryIconPosition.SECONDARY))
        assert TOOLTIP_PRIMARY == (
            view.get_icon_tooltip_markup(Gtk.EntryIconPosition.PRIMARY))
        assert TOOLTIP_SECONDARY == (
            view.get_icon_tooltip_markup(Gtk.EntryIconPosition.SECONDARY))
        assert N_WIDTH_EDIT == view.get_width_chars()


class TestFactoryDisplayTextMarkup:
    """Unit tests for :class:`.FactoryDisplayTextMarkup`."""

    def test_call(self, monkeypatch):
        """Confirm return is display-only view.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        TEXT = 'The <b>Parrot </b Sketch.'
        TEXT_ESCAPED = GLib.markup_escape_text(TEXT, len(TEXT))
        entry_buffer = BTEXT.ModelTextMarkup()
        entry_buffer._set_persist(TEXT)
        target = BTEXT.FactoryDisplayTextMarkup(p_model=entry_buffer)

        class PatchConnect:
            def __init__(self):
                self.calls = dict()

            def connect(self, p_signal, p_handler):
                self.calls[p_signal] = p_handler

        patch_label = PatchConnect()
        monkeypatch.setattr(Gtk.Label, 'connect', patch_label.connect)
        EXPECT_LABEL = {'destroy': target.on_destroy}
        patch_entry = PatchConnect()
        monkeypatch.setattr(Gtk.EntryBuffer, 'connect', patch_entry.connect)
        EXPECT_ENTRY_BUFFER = {'deleted-text': target.on_change,
                               'inserted-text': target.on_change}
        N_WIDTH_DISPLAY = 15
        XALIGN = 0.0
        # Test
        display = target()
        assert isinstance(display, Gtk.Label)
        assert TEXT_ESCAPED == display.get_label()
        assert target._displays[id(display)] is display
        assert EXPECT_LABEL == patch_label.calls
        assert EXPECT_ENTRY_BUFFER == patch_entry.calls

        assert Pango.EllipsizeMode.END is display.get_ellipsize()
        assert Gtk.Align.START == display.get_halign()
        assert display.get_selectable()
        assert display.get_use_markup()
        assert N_WIDTH_DISPLAY == display.get_width_chars()
        assert math.isclose(XALIGN, display.get_xalign())

    def test_init(self):
        """Confirm storage initialization."""
        # Setup
        MODEL = BTEXT.ModelTextMarkup()
        # Test
        target = BTEXT.FactoryDisplayTextMarkup(p_model=MODEL)
        assert target._ui_model is MODEL._ui_model
        assert isinstance(target._displays, dict)
        assert not target._displays

    def test_on_change(self):
        """| Confirm refresh of display views."""
        # Setup
        TEXT = 'The <b>Parrot </b Sketch.'
        TEXT_ESCAPED = GLib.markup_escape_text(TEXT, len(TEXT))
        entry_buffer = BTEXT.ModelTextMarkup()
        entry_buffer._set_persist(p_persist=TEXT)
        target = BTEXT.FactoryDisplayTextMarkup(p_model=entry_buffer)

        N_DISPLAYS = 3
        for _ in range(N_DISPLAYS):
            display = BTEXT.DisplayTextMarkup()
            target._displays[id(display)] = display
        # Test
        target.on_change(None, None, None)
        assert N_DISPLAYS == len(target._displays)
        for display in target._displays.values():
            assert TEXT_ESCAPED == display.get_label()

    def test_on_destroy(self):
        """| Confirm display view removal.
        | Case: display connected to model.
        """
        # Setup
        TEXT = 'The <b>Parrot Sketch.</b>'
        entry_buffer = BTEXT.ModelTextMarkup()
        entry_buffer._set_persist(p_persist=TEXT)
        target = BTEXT.FactoryDisplayTextMarkup(p_model=entry_buffer)
        N_DISPLAYS = 5
        I_DESTROY = 4
        for i in range(N_DISPLAYS):
            display = Gtk.Label()
            id_display = BTEXT.id_display(display)
            target._displays[id_display] = display
            if i == I_DESTROY:
                id_destroy = id_display
                display_destroy = display
        # Test
        target.on_destroy(display_destroy)
        assert N_DISPLAYS - 1 == len(target._displays)
        assert id_destroy not in target._displays

    def test_on_destroy_warn(self, caplog):
        """| Confirm display view removal.
        | Case: display not connected to model.

        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        TEXT = 'The <b>Parrot Sketch.</b>'
        entry_buffer = BTEXT.ModelTextMarkup()
        entry_buffer._set_persist(p_persist=TEXT)
        target = BTEXT.FactoryDisplayTextMarkup(p_model=entry_buffer)
        N_DISPLAYS = 5
        for _ in range(N_DISPLAYS):
            display = Gtk.Label()
            id_display = BTEXT.id_display(display)
            target._displays[id_display] = display
        DISPLAY_MISSING = Gtk.Label()
        N_LOGS = 1
        LAST = -1
        log_message = ('Missing display: {} (FactoryDisplayTextMarkup'
                       '.on_destroy)'.format(hex(id(DISPLAY_MISSING))))
        # Test
        target.on_destroy(DISPLAY_MISSING)
        assert N_DISPLAYS == len(target._displays)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname


class TestFactoryEditorTextStyled:
    """Unit tests for :class:`.FactoryEditorTextStyled`."""

    def test_init(self):
        """Confirm storage initialization."""
        # Setup
        MODEL = BTEXT.ModelTextStyled()
        # Test
        target = BTEXT.FactoryEditorTextStyled(p_model=MODEL)
        assert target._ui_model is MODEL._ui_model

    def test_call(self):
        """Confirm attributes of display and edit views."""
        # Setup
        MODEL = BTEXT.ModelTextStyled()
        target = BTEXT.FactoryEditorTextStyled(p_model=MODEL)
        N_MARGIN_LEFT_RIGHT = 6
        N_MARGIN_TOP_BOTTOM = 6
        WRAP_MODE = Gtk.WrapMode.WORD_CHAR
        # Test
        view = target()
        assert isinstance(view, Gtk.TextView)
        assert target._ui_model is view.get_buffer()
        assert N_MARGIN_TOP_BOTTOM == view.get_bottom_margin()
        assert N_MARGIN_LEFT_RIGHT == view.get_left_margin()
        assert N_MARGIN_LEFT_RIGHT == view.get_right_margin()
        assert N_MARGIN_TOP_BOTTOM == view.get_top_margin()
        assert view.get_vexpand()
        assert WRAP_MODE == view.get_wrap_mode()
        assert view.get_editable()


class TestFactoryDisplayTextStyled:
    """Unit tests for :class:`.FactoryDisplayTextStyled`."""

    def test_init(self):
        """Confirm storage initialization."""
        # Setup
        MODEL = BTEXT.ModelTextStyled()
        # Test
        target = BTEXT.FactoryDisplayTextStyled(p_model=MODEL)
        source = target._factory_source
        assert isinstance(source, BTEXT.FactoryEditorTextStyled)
        assert source._ui_model is MODEL._ui_model
        assert target._ui_model is MODEL._ui_model

    def test_call(self):
        """Confirm attributes of display and edit views."""
        # Setup
        MODEL = BTEXT.ModelTextStyled()
        target = BTEXT.FactoryDisplayTextStyled(p_model=MODEL)
        # Test
        view = target()
        assert isinstance(view, Gtk.TextView)
        assert not view.get_editable()


class TestIdDisplay:
    """Unit tests for :func:`.id_display`."""

    def test_id_display(self):
        """Confirm id returned."""
        # Setup
        DISPLAY = Gtk.Label()
        # Test
        assert id(DISPLAY) == BTEXT.id_display(DISPLAY)


class TestModelText:
    """Unit tests for :class:`.ModelText`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BTEXT.ModelText, '_get_persist'),
        (BTEXT.ModelText, '_new_ui_model'),
        (BTEXT.ModelText, '_set_persist'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified.

        :param CLASS: class that should be abstract.
        :param NAME_METHOD: method that should be abstract.
        """
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__

    def test_eq(self):
        """Confirm equality comparison.

        #. Case: not a text attribute.
        #. Case: different content.
        #. Case: equal
        """
        # Setup
        TEXT = 'The Parrot Sketch'
        source = PatchModelText()
        source._set_persist(TEXT)
        # Test: not a text attribute.
        assert not source.__eq__(TEXT)
        # Test: different content.
        TEXT_DIFFER = 'Something completely different.'
        target = PatchModelText()
        target._set_persist(TEXT_DIFFER)
        assert not source.__eq__(target)
        # Test: equal
        target = PatchModelText()
        target._set_persist(TEXT)
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format.

        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        source = PatchModelText()
        TEXT = 'The Parrot Sketch'
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
        """| Confirm initialization.
        | Case: non-default text.
        """
        # Setup
        TEXT = 'The Parrot Sketch'
        # Test
        target = PatchModelText(p_text=TEXT)
        assert TEXT == target.text
        assert isinstance(target._stale, bool)
        assert not target._stale

    def test_init_default(self):
        """| Confirm initialization.
        | Case: default text.
        """
        # Setup
        BLANK = ''
        # Test
        target = PatchModelText()
        assert BLANK == target.text
        assert isinstance(target._stale, bool)
        assert not target._stale

    def test_str(self):
        """Confirm return is attribute content. """
        # Setup
        TEXT = 'The Parrot Sketch'
        target = PatchModelText()
        target._set_persist(p_persist=TEXT)
        expect = '<{}: {}>'.format(type(target).__name__, TEXT)
        # Test
        assert expect == str(target)

    def test_is_fresh(self):
        """Confirm return matches state. """
        # Setup
        target = PatchModelText()
        target._stale = False
        # Test
        assert target.is_fresh()
        target._stale = True
        assert not target.is_fresh()

    def test_is_stale(self):
        """Confirm return matches state. """
        # Setup
        target = PatchModelText()
        target._stale = False
        # Test
        assert not target.is_stale()
        target._stale = True
        assert target.is_stale()

    def test_set_freah(self):
        """Confirm attribute marked fresh. """
        # Setup
        target = PatchModelText()
        target._stale = True
        # Test
        target.set_fresh()
        assert not target._stale

    def test_set_stale(self):
        """Confirm attribute marked stale. """
        # Setup
        target = PatchModelText()
        target._stale = False
        # Test
        target.set_stale()
        assert target._stale

    def test_text(self):
        """Confirm access limits of text property."""
        # Setup
        target_class = PatchModelText
        target = target_class()
        TEXT = 'The Parrot Sketch'
        target._set_persist(TEXT)
        TEXT_NEW = 'Something completely different.'
        # Test
        assert target_class.text.fget is not None
        assert TEXT == target.text
        assert target_class.text.fset is not None
        target.text = TEXT_NEW
        assert TEXT_NEW == target._get_persist()
        assert target_class.text.fdel is None


class TestModelTextMarkup:
    """Unit tests for :class:`.ModelTextMarkup`.

    :class:`.TestBridgeTextCommon` contains additional unit tests for
    :class:`.ModelTextMarkup`.
    """

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format.

        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        source = BTEXT.ModelTextMarkup()
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
        target = BTEXT.ModelTextMarkup()
        assert target._stale is not None
        assert not target._stale
        assert isinstance(target._ui_model, Gtk.EntryBuffer)
        assert BLANK == target._ui_model.get_text()

    def test_get_persist(self):
        """Confirm export to persistent form."""
        # Setup
        target = BTEXT.ModelTextMarkup()
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
        target = BTEXT.ModelTextMarkup()
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
        target = BTEXT.ModelTextMarkup()
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


class TestModelTextStyled:
    """Unit tests for :class:`.ModelTextStyled`."""

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format.

        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        source = BTEXT.ModelTextStyled()
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
        NO_HIDDEN = False
        # Test
        target = BTEXT.ModelTextStyled()
        assert target._stale is not None
        assert not target._stale
        assert isinstance(target._ui_model, Gtk.TextBuffer)
        start, end = target._ui_model.get_bounds()
        assert BLANK == target._ui_model.get_text(start, end, NO_HIDDEN)

    def test_get_persist(self):
        """Confirm export to persistent form."""
        # Setup
        target = BTEXT.ModelTextStyled()
        TEXT = 'The Parrot Sketch.'
        ALL = -1
        target._ui_model.set_text(TEXT, ALL)
        # Test
        assert TEXT == target._get_persist()

    @pytest.mark.parametrize('NAME_SIGNAL, N_DEFAULT', [
        ('changed', 0),
        ])
    def test_new_model(self, NAME_SIGNAL, N_DEFAULT):
        """Confirm GTK model with signal connections.

        :param NAME_SIGNAL: signal under test.
        :param N_DEFAULT: number of default handlers for signal.
        """
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(Gtk.TextBuffer))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        NO_SIGNAL = 0
        # Test
        target = BTEXT.ModelTextStyled()
        assert isinstance(target._ui_model, Gtk.TextBuffer)
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
        target = BTEXT.ModelTextStyled()
        target_buffer = target._ui_model
        TEXT = 'The Parrot Sketch.'
        ALL = -1
        target._ui_model.set_text(TEXT, ALL)
        target.set_fresh()
        TEXT_NEW = 'Something completely different.'
        # Test
        target._set_persist(TEXT_NEW)
        assert target._ui_model is target_buffer
        assert TEXT_NEW == target._get_persist()
        assert target.is_stale()


class TestTypes:
    """Unit tests for type hint definitions in :mod:`.bridge_text`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (BTEXT.IdDisplay.__qualname__, 'NewType.<locals>.new_type'),
        (BTEXT.IdDisplay.__dict__['__supertype__'], int),
        (BTEXT.PersistText, str),
        (BTEXT.DisplayTextMarkup, Gtk.Label),
        (BTEXT.EditorTextMarkup, Gtk.Entry),
        (BTEXT.DisplayTextStyled, Gtk.TextView),
        (BTEXT.EditorTextStyled, Gtk.TextView),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type hint definitions.

        :param TYPE_TARGET: type hint under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT
