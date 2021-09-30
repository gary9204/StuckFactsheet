"""
Unit tests for GTK-based classes that implement abstract identification
information classes.  See :mod:`.bridge_text`.

.. include:: /test/refs_include_pytest.txt
"""
import gi   # type: ignore[import]
import logging
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


class PatchBridgeText(BTEXT.ModelGtkText[typing.Any]):
    """:class:`.ModelGtkText` subclass with stub text property."""

    def __init__(self):
        super().__init__()
        self._ui_model = 'Oops! incomplete test initialization.'

    def _get_persist(self):
        return self._ui_model

    def _set_persist(self, p_persist):
        self._ui_model = str(p_persist)


class TestBridgeText:
    """Unit tests for :class:`.ModelGtkText`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BTEXT.ModelGtkText, '_get_persist'),
        (BTEXT.ModelGtkText, '_set_persist'),
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
        source = PatchBridgeText()
        source._set_persist(TEXT)
        # Test: not a text attribute.
        assert not source.__eq__(TEXT)
        # Test: different content.
        TEXT_DIFFER = 'Something completely different.'
        target = PatchBridgeText()
        target._set_persist(TEXT_DIFFER)
        assert not source.__eq__(target)
        # Test: equal
        target = PatchBridgeText()
        target._set_persist(TEXT)
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format.

        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        source = PatchBridgeText()
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
        """Confirm initialization."""
        # Setup
        # Test
        target = PatchBridgeText()
        assert target._stale is not None
        assert not target._stale

    def test_str(self):
        """Confirm return is attribute content. """
        # Setup
        TEXT = 'The Parrot Sketch'
        target = PatchBridgeText()
        target._ui_model = TEXT
        expect = '<{}: {}>'.format(type(target).__name__, TEXT)
        # Test
        assert expect == str(target)

    def test_is_fresh(self):
        """Confirm return matches state. """
        # Setup
        target = PatchBridgeText()
        target._stale = False
        # Test
        assert target.is_fresh()
        target._stale = True
        assert not target.is_fresh()

    def test_is_stale(self):
        """Confirm return matches state. """
        # Setup
        target = PatchBridgeText()
        target._stale = False
        # Test
        assert not target.is_stale()
        target._stale = True
        assert target.is_stale()

    def test_set_freah(self):
        """Confirm attribute marked fresh. """
        # Setup
        target = PatchBridgeText()
        target._stale = True
        # Test
        target.set_fresh()
        assert not target._stale

    def test_set_stale(self):
        """Confirm attribute marked stale. """
        # Setup
        target = PatchBridgeText()
        target._stale = False
        # Test
        target.set_stale()
        assert target._stale

    def test_text(self):
        """Confirm access limits of text property."""
        # Setup
        target_class = PatchBridgeText
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
        assert target.is_stale()
        assert target_class.text.fdel is None


class TestBridgeTextCommon:
    """Unit tests common to descendants of :class:`.ModelGtkText`.

    Parameters specialize the tests for each class.  Some descendants
    may need individualized tests (for example,
    :class:`.BridgeTextStatic`).
    """

    @pytest.mark.skip
    @pytest.mark.parametrize(
        'CLASS_BRIDGE, CLASS_TEXT, NAME_SIGNAL, N_DEFAULT', [
            (BTEXT.ModelGtkTextBuffer, Gtk.TextBuffer,
                'changed', 0),
            (BTEXT.ModelGtkEntryBuffer, Gtk.EntryBuffer,
                'deleted-text', 0),
            (BTEXT.ModelGtkEntryBuffer, Gtk.EntryBuffer,
                'inserted-text', 0),
        ])
    def test_get_set_signals(self, tmp_path, CLASS_BRIDGE, CLASS_TEXT,
                             NAME_SIGNAL, N_DEFAULT):
        """Confirm reconstruction of signal connections.

        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        :param CLASS_BRIDGE: bridge class under test.
        :param CLASS_TEXT: text storage class for bridge.
        :param NAME_SIGNAL: signal under test.
        :param N_DEFAULT: number of default handlers for signal.
        """
        # Setup
        source = CLASS_BRIDGE()
        source._stale = True
        TEXT = 'The Parrot Sketch'
        source._set_persist(TEXT)
        # Warning: GO.signal_lookup fails unless there is a prior
        #    reference to CLASS_TEXT.  Reference loads GObject class.
        origin_gtype = GO.type_from_name(GO.type_name(CLASS_TEXT))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        NO_SIGNAL = 0
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        # Test
        with PATH.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)

        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                target._model, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if NO_SIGNAL == id_signal:
                break
            n_handlers += 1
            GO.signal_handler_disconnect(target._model, id_signal)
        assert (N_DEFAULT + 1) == n_handlers

    @pytest.mark.skip
    @pytest.mark.parametrize('CLASS_BRIDGE, CLASS_TEXT', [
        (BTEXT.ModelGtkTextBuffer, Gtk.TextBuffer),
        (BTEXT.ModelGtkEntryBuffer, Gtk.EntryBuffer),
        # See TestBridgeTextStatic for specialized test.
        ])
    def test_init(self, CLASS_BRIDGE, CLASS_TEXT):
        """Confirm initialization.

        :param CLASS_BRIDGE: bridge class under test.
        :param CLASS_TEXT: text storage class for bridge.
        """
        # Setup
        # Test
        target = CLASS_BRIDGE()
        assert not target._stale
        assert isinstance(target._model, CLASS_TEXT)
        assert not target._get_persist()

    @pytest.mark.parametrize(
        'CLASS_BRIDGE, CLASS_TEXT, NAME_SIGNAL, N_DEFAULT', [
            # (BTEXT.ModelGtkTextBuffer, Gtk.TextBuffer, 'changed', 0),
            # (BTEXT.ModelGtkEntryBuffer, Gtk.EntryBuffer, 'deleted-text', 0),
            # (BTEXT.ModelGtkEntryBuffer, Gtk.EntryBuffer, 'inserted-text', 0),
        ])
    def test_init_signals(
            self, CLASS_BRIDGE, CLASS_TEXT, NAME_SIGNAL, N_DEFAULT):
        """Confirm initialization of signal connections.

        :param CLASS_BRIDGE: bridge class under test.
        :param CLASS_TEXT: text storage class for bridge.
        :param NAME_SIGNAL: signal under test.
        :param N_DEFAULT: number of default handlers for signal.
        """
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(CLASS_TEXT))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        NO_SIGNAL = 0
        # Test
        target = CLASS_BRIDGE()
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                target._model, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if NO_SIGNAL == id_signal:
                break
            n_handlers += 1
            GO.signal_handler_disconnect(target._model, id_signal)
        assert (N_DEFAULT + 1) == n_handlers


class TestFactoryGtkEntry:
    """Unit tests for :class:`.FactoryGtkEntry`."""

    def test_init(self):
        """Confirm storage initialization."""
        # Setup
        MODEL = BTEXT.ModelGtkEntryBuffer()
        # Test
        target = BTEXT.FactoryGtkEntry(p_model=MODEL)
        assert target._ui_model is MODEL._ui_model

    def test_call(self):
        """Confirm return is editable view."""
        # Setup
        NAME_ICON_PRIMARY = 'emblem-default-symbolic'
        NAME_ICON_SECONDARY = 'edit-delete-symbolic'
        TOOLTIP_PRIMARY = 'Click to accept changes.'
        TOOLTIP_SECONDARY = 'Click to cancel changes.'
        N_WIDTH_EDIT = 45
        entry_buffer = BTEXT.ModelGtkEntryBuffer()
        target = BTEXT.FactoryGtkEntry(p_model=entry_buffer)
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


class TestFactoryGtkLabelBuffered:
    """Unit tests for :class:`.FactoryGtkLabelBuffered`."""

    def test_call(self, monkeypatch):
        """Confirm return is display-only view.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        TEXT = 'The <b>Parrot </b Sketch.'
        TEXT_ESCAPED = GLib.markup_escape_text(TEXT, len(TEXT))
        entry_buffer = BTEXT.ModelGtkEntryBuffer()
        entry_buffer.text = TEXT
        target = BTEXT.FactoryGtkLabelBuffered(p_model=entry_buffer)

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
        MODEL = BTEXT.ModelGtkEntryBuffer()
        # Test
        target = BTEXT.FactoryGtkLabelBuffered(p_model=MODEL)
        assert target._ui_model is MODEL._ui_model
        assert isinstance(target._displays, dict)
        assert not target._displays

    def test_on_change(self):
        """| Confirm refresh of display views."""
        # Setup
        TEXT = 'The <b>Parrot </b Sketch.'
        TEXT_ESCAPED = GLib.markup_escape_text(TEXT, len(TEXT))
        entry_buffer = BTEXT.ModelGtkEntryBuffer()
        entry_buffer.text = TEXT
        target = BTEXT.FactoryGtkLabelBuffered(p_model=entry_buffer)

        N_DISPLAYS = 3
        for _ in range(N_DISPLAYS):
            display = BTEXT.ViewTextDisplay()
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
        entry_buffer = BTEXT.ModelGtkEntryBuffer()
        entry_buffer.text = TEXT
        target = BTEXT.FactoryGtkLabelBuffered(p_model=entry_buffer)
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

    def test_on_destroy_warn(self, PatchLogger, monkeypatch):
        """| Confirm display view removal.
        | Case: display not connected to model.

        :param PatchLogger: deprecated but not yet removed.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        TEXT = 'The <b>Parrot Sketch.</b>'
        entry_buffer = BTEXT.ModelGtkEntryBuffer()
        entry_buffer.text = TEXT
        target = BTEXT.FactoryGtkLabelBuffered(p_model=entry_buffer)
        N_DISPLAYS = 5
        for _ in range(N_DISPLAYS):
            display = Gtk.Label()
            id_display = BTEXT.id_display(display)
            target._displays[id_display] = display
        DISPLAY_MISSING = Gtk.Label()

        patch_logger = PatchLogger()
        monkeypatch.setattr(logging.Logger, 'warning', patch_logger.warning)
        log_message = ('Missing display: {} (FactoryGtkLabelBuffered'
                       '.on_destroy)'.format(hex(id(DISPLAY_MISSING))))
        # Test
        target.on_destroy(DISPLAY_MISSING)
        assert N_DISPLAYS == len(target._displays)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_filter_text_markup(self):
        """| Confirm markup errors escaped.
        | Case: text does not contain markup error.
        """
        # Setup
        TEXT = 'The <b>Parrot Sketch.</b>'
        entry_buffer = BTEXT.ModelGtkEntryBuffer()
        entry_buffer.text = TEXT
        target = BTEXT.FactoryGtkLabelBuffered(p_model=entry_buffer)
        # Test
        assert TEXT == target.filter_text_markup()

    def test_filter_text_markup_error(self):
        """| Confirm markup errors escaped.
        | Case: text contains markup error.
        """
        # Setup
        TEXT = 'The <b>Parrot </b Sketch.'
        TEXT_ESCAPED = GLib.markup_escape_text(TEXT, len(TEXT))
        entry_buffer = BTEXT.ModelGtkEntryBuffer()
        entry_buffer.text = TEXT
        target = BTEXT.FactoryGtkLabelBuffered(p_model=entry_buffer)
        # Test
        assert TEXT_ESCAPED == target.filter_text_markup()

    def test_filter_text_markup_except(self, monkeypatch):
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
        entry_buffer = BTEXT.ModelGtkEntryBuffer()
        entry_buffer.text = TEXT
        target = BTEXT.FactoryGtkLabelBuffered(p_model=entry_buffer)
        # Test
        with pytest.raises(GLib.Error) as exc_info:
            _ = target.filter_text_markup()
        exc = exc_info.value
        assert DOMAIN == exc.domain
        assert MESSAGE == exc.message
        assert CODE == exc.code


class TestIdDisplay:
    """Unit tests for :func:`.id_display`."""

    def test_id_display(self):
        """Confirm id returned."""
        # Setup
        DISPLAY = Gtk.Label()
        # Test
        assert id(DISPLAY) == BTEXT.id_display(DISPLAY)


class TestModelGtkEntryBuffer:
    """Unit tests for :class:`.ModelGtkEntryBuffer`.

    :class:`.TestBridgeTextCommon` contains additional unit tests for
    :class:`.ModelGtkEntryBuffer`.
    """

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format.

        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        source = BTEXT.ModelGtkEntryBuffer()
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
        target = BTEXT.ModelGtkEntryBuffer()
        assert target._stale is not None
        assert not target._stale
        assert isinstance(target._ui_model, Gtk.EntryBuffer)
        assert BLANK == target._ui_model.get_text()

    def test_get_persist(self):
        """Confirm export to persistent form."""
        # Setup
        target = BTEXT.ModelGtkEntryBuffer()
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
        target = BTEXT.ModelGtkEntryBuffer()
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
        target = BTEXT.ModelGtkEntryBuffer()
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


class TestFactoryGtkTextView:
    """Unit tests for :class:`.FactoryGtkTextView`."""

    def test_init(self):
        """Confirm storage initialization."""
        # Setup
        MODEL = BTEXT.ModelGtkTextBuffer()
        # Test
        target = BTEXT.FactoryGtkTextView(p_model=MODEL)
        assert target._ui_model is MODEL._ui_model

    def test_call(self):
        """Confirm attributes of display and edit views."""
        # Setup
        MODEL = BTEXT.ModelGtkTextBuffer()
        target = BTEXT.FactoryGtkTextView(p_model=MODEL)
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


class TestFactoryGtkTextViewDisplay:
    """Unit tests for :class:`.FactoryGtkTextViewDisplay`."""

    pass


class TestModelGtkTextBuffer:
    """Unit tests for :class:`.ModelGtkTextBuffer`."""

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format.

        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        source = BTEXT.ModelGtkTextBuffer()
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
        target = BTEXT.ModelGtkTextBuffer()
        assert target._stale is not None
        assert not target._stale
        assert isinstance(target._ui_model, Gtk.TextBuffer)
        start, end = target._ui_model.get_bounds()
        assert BLANK == target._ui_model.get_text(start, end, NO_HIDDEN)

    def test_get_persist(self):
        """Confirm export to persistent form."""
        # Setup
        target = BTEXT.ModelGtkTextBuffer()
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
        target = BTEXT.ModelGtkTextBuffer()
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
        target = BTEXT.ModelGtkTextBuffer()
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

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (BTEXT.IdDisplay.__qualname__, 'NewType.<locals>.new_type'),
        (BTEXT.IdDisplay.__dict__['__supertype__'], int),
        # (type(BTEXT.ModelTextOpaque), typing.TypeVar),
        # (BTEXT.ModelTextOpaque.__constraints__, ()),
        # # (BTEXT.ModelTextStatic, str),
        # (BTEXT.ViewTextTagged, Gtk.TextView),
        # (BTEXT.ViewTextMarkup, Gtk.Entry),
        # (type(BTEXT.ViewTextOpaque), typing.TypeVar),
        # (BTEXT.ViewTextOpaque.__constraints__, ()),
        # (type(BTEXT.ViewTextOpaquePassive), typing.TypeVar),
        # (BTEXT.ViewTextOpaquePassive.__constraints__, ()),
        # (BTEXT.ViewTextDisplay, Gtk.Label),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions.

        :param TYPE_TARGET: type under test.
        :param TYPE_SOURCE: expected type.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
