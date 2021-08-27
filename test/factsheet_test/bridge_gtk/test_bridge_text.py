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


class PatchBridgeText(BTEXT.BridgeText[typing.Any, typing.Any, typing.Any]):
    """:class:`.BridgeText` subclass with stub text property."""

    def __init__(self):
        super().__init__()

    def _get_persist(self):
        return self._model

    def _new_model(self):
        return str()

    def new_view(self):
        return str()

    def new_view_passive(self):
        return str()

    def _set_persist(self, p_persist):
        self._model = str(p_persist)


class TestBridgeText:
    """Unit tests for :class:`.BridgeText`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BTEXT.BridgeText, '_get_persist'),
        (BTEXT.BridgeText, '_new_model'),
        (BTEXT.BridgeText, 'new_view'),
        (BTEXT.BridgeText, 'new_view_passive'),
        (BTEXT.BridgeText, '_set_persist'),
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
        assert isinstance(target._model, str)
        assert not target._model
        assert target._stale is not None
        assert not target._stale

    def test_str(self):
        """Confirm return is attribute content. """
        # Setup
        TEXT = 'The Parrot Sketch'
        target = PatchBridgeText()
        target._model = TEXT
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

    def test_set_persist(self):
        """Confirm attribute marked stale after content change."""
        # Setup
        target = PatchBridgeText()
        TEXT = 'The Parrot Sketch'
        # Test
        target._set_persist(TEXT)

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
    """Unit tests common to descendants of :class:`.BridgeText`.

    Parameters specialize the tests for each class.  Some descendants
    may need individualized tests (for example,
    :class:`.BridgeTextStatic`).
    """

    @pytest.mark.parametrize(
        'CLASS_BRIDGE, CLASS_TEXT, NAME_SIGNAL, N_DEFAULT', [
            (BTEXT.BridgeTextTagged, BTEXT.ModelTextTagged,
                'changed', 0),
            (BTEXT.BridgeTextMarkup, BTEXT.ModelTextMarkup,
                'deleted-text', 0),
            (BTEXT.BridgeTextMarkup, BTEXT.ModelTextMarkup,
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

    @pytest.mark.parametrize('CLASS_BRIDGE, CLASS_TEXT', [
        (BTEXT.BridgeTextTagged, BTEXT.ModelTextTagged),
        (BTEXT.BridgeTextMarkup, BTEXT.ModelTextMarkup),
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
            (BTEXT.BridgeTextTagged, BTEXT.ModelTextTagged,
                'changed', 0),
            (BTEXT.BridgeTextMarkup, BTEXT.ModelTextMarkup,
                'deleted-text', 0),
            (BTEXT.BridgeTextMarkup, BTEXT.ModelTextMarkup,
             'inserted-text', 0),
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


class TestBridgeTextMarkup:
    """Unit tests for :class:`.BridgeTextMarkup`.

    :class:`.TestBridgeTextCommon` contains additional unit tests for
    :class:`.BridgeTextMarkup`.
    """

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format.

        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        source = BTEXT.BridgeTextMarkup()
        TEXT = 'Something completely different'
        source._set_persist(TEXT)
        source._stale = True
        I_ENTRY = 0
        source._views[I_ENTRY] = BTEXT.ViewTextDisplay()
        # Test
        with PATH.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert source._get_persist() == target._get_persist()
        assert isinstance(target._views, dict)
        assert not target._views
        assert not target._stale

    def test_destroy_view(self):
        """| Confirm display-only view removal.
        | Case: model connected to view.
        """
        # Setup
        target = BTEXT.BridgeTextMarkup()
        N_VIEWS = 5
        I_REMOVE = 4
        for i in range(N_VIEWS):
            view = BTEXT.ViewTextDisplay()
            id_view = id(view)
            target._views[id_view] = view
            if i == I_REMOVE:
                id_remove = id_view
                view_remove = view
        # Test
        target._destroy_view(view_remove)
        assert id_remove not in target._views

    def test_destroy_view_warn(self, PatchLogger, monkeypatch):
        """| Confirm display-only view removal.
        | Case: model not connected view.

        :param PatchLogger: deprecated but not yet removed.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        target = BTEXT.BridgeTextMarkup()
        N_VIEWS = 5
        for _ in range(N_VIEWS):
            view = BTEXT.ViewTextDisplay()
            target._views[id(view)] = view
        VIEW_MISSING = BTEXT.ViewTextDisplay()

        patch_logger = PatchLogger()
        monkeypatch.setattr(logging.Logger, 'warning', patch_logger.warning)
        log_message = ('Missing view: {} (BridgeTextMarkup._destroy_view)'
                       ''.format(hex(id(VIEW_MISSING))))
        # Test
        target._destroy_view(VIEW_MISSING)
        assert N_VIEWS == len(target._views)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_get_persist(self):
        """Confirm export to persistent form."""
        # Setup
        target = BTEXT.BridgeTextMarkup()
        TEXT = 'The Parrot Sketch.'
        ALL = -1
        target._model.set_text(TEXT, ALL)
        # Test
        assert TEXT == target._get_persist()

    def test_new_model(self):
        """Confirm storage type."""
        # Setup
        target = BTEXT.BridgeTextMarkup()
        # Test
        assert isinstance(target._model, BTEXT.ModelTextMarkup)
        assert isinstance(target._views, dict)
        assert not target._views

    def test_new_view(self):
        """Confirm return is editable view."""
        # Setup
        NAME_ICON_PRIMARY = 'emblem-default-symbolic'
        NAME_ICON_SECONDARY = 'edit-delete-symbolic'
        TOOLTIP_PRIMARY = 'Click to accept changes.'
        TOOLTIP_SECONDARY = 'Click to cancel changes.'
        target = BTEXT.BridgeTextMarkup()
        # Test
        view = target.new_view()
        assert isinstance(view, BTEXT.ViewTextMarkup)
        assert target._model is view.get_buffer()
        assert not target._views
        assert Gtk.Align.START == view.get_halign()
        assert NAME_ICON_PRIMARY == (
            view.get_icon_name(Gtk.EntryIconPosition.PRIMARY))
        assert NAME_ICON_SECONDARY == (
            view.get_icon_name(Gtk.EntryIconPosition.SECONDARY))
        assert TOOLTIP_PRIMARY == (
            view.get_icon_tooltip_markup(Gtk.EntryIconPosition.PRIMARY))
        assert TOOLTIP_SECONDARY == (
            view.get_icon_tooltip_markup(Gtk.EntryIconPosition.SECONDARY))
        assert target.N_WIDTH_EDIT == view.get_width_chars()

    def test_new_view_passive(self, monkeypatch):
        """Confirm return is display-only view.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        class PatchConnect:
            def __init__(self):
                self.called = False
                self.signal = None
                self.handler = None

            def connect(self, p_signal, p_handler):
                self.called = True
                self.signal = p_signal
                self.handler = p_handler

        patch_connect = PatchConnect()
        monkeypatch.setattr(Gtk.Widget, 'connect', patch_connect.connect)
        target = BTEXT.BridgeTextMarkup()
        TEXT = 'The <b>Parrot </b>Sketch'
        target._set_persist(TEXT)
        SIGNAL = 'destroy'
        HANDLER = target._destroy_view
        N_XALIGN = 0.0
        # Test
        view = target.new_view_passive()
        assert isinstance(view, BTEXT.ViewTextDisplay)
        assert TEXT == view.get_label()
        assert patch_connect.called
        assert SIGNAL == patch_connect.signal
        assert target._destroy_view == HANDLER
        assert target._views[id(view)] is view

        assert Pango.EllipsizeMode.END is view.get_ellipsize()
        assert Gtk.Align.START == view.get_halign()
        assert view.get_selectable()
        assert view.get_use_markup()
        assert target.N_WIDTH_DISPLAY == view.get_width_chars()
        assert math.isclose(N_XALIGN, view.get_xalign())

    def test_on_change(self):
        """| Confirm refresh of display views."""
        # Setup
        target = BTEXT.BridgeTextMarkup()
        TEXT = 'The <b>Parrot </b>Sketch.'
        ALL = -1
        target._model.set_text(TEXT, ALL)
        N_VIEWS = 3
        for _ in range(N_VIEWS):
            view = BTEXT.ViewTextDisplay()
            target._views[id(view)] = view
        target.set_fresh()
        # Test
        target.on_change()
        assert target.is_stale()
        assert N_VIEWS == len(target._views)
        for view in target._views.values():
            assert TEXT == view.get_label()

    def test_set_persist(self):
        """Confirm import from persistent form."""
        # Setup
        target = BTEXT.BridgeTextMarkup()
        TEXT = 'The Parrot Sketch.'
        ALL = -1
        target._model.set_text(TEXT, ALL)
        N_VIEWS = 3
        for _ in range(N_VIEWS):
            view = BTEXT.ViewTextDisplay()
            target._views[id(view)] = view
        target.set_fresh()
        TEXT_NEW = 'Something completely different.'
        # Test
        target._set_persist(TEXT_NEW)
        assert TEXT_NEW == target._get_persist()
        assert target.is_stale()
        assert N_VIEWS == len(target._views)
        for view in target._views.values():
            assert TEXT_NEW == view.get_label()


class TestBridgeTextTagged:
    """Unit tests for :class:`.BridgeTextTagged`.

    See :class:`.TestBridgeTextCommon` for additional unit tests for
    :class:`.BridgeTextTagged`.
    """

    def test_get_persist(self):
        """Confirm export to persistent form."""
        # Setup
        target = BTEXT.BridgeTextTagged()
        TEXT = 'The Parrot Sketch.'
        ALL = -1
        target._model.set_text(TEXT, ALL)
        # Test
        assert TEXT == target._get_persist()

    def test_new_model(self):
        """Confirm storage element."""
        # Setup
        target = BTEXT.BridgeTextTagged()
        # Test
        assert isinstance(target._model, BTEXT.ModelTextTagged)

    @pytest.mark.parametrize('METHOD, EDIT_OK', [
        ('new_view', True),
        ('new_view_passive', False),
        ])
    def test_new_views(self, METHOD, EDIT_OK):
        """Confirm attributes of display and edit views.

        :param METHOD: method to test, which is ``new_view`` or
            ``new_view_passive``.
        :param EDIT_OK: whether view should be editable.
        """
        # Setup
        target = BTEXT.BridgeTextTagged()
        method_target = getattr(target, METHOD)
        N_MARGIN_LEFT_RIGHT = 6
        N_MARGIN_TOP_BOTTOM = 6
        # Test
        view = method_target()
        assert isinstance(view, BTEXT.ViewTextTagged)
        assert target._model is view.get_buffer()
        assert N_MARGIN_TOP_BOTTOM == view.get_bottom_margin()
        assert N_MARGIN_LEFT_RIGHT == view.get_left_margin()
        assert N_MARGIN_LEFT_RIGHT == view.get_right_margin()
        assert N_MARGIN_TOP_BOTTOM == view.get_top_margin()
        assert view.get_vexpand()
        assert Gtk.WrapMode.WORD_CHAR == view.get_wrap_mode()
        assert view.get_editable() is EDIT_OK

    def test_set_persist(self):
        """Confirm import from persistent form."""
        # Setup
        target = BTEXT.BridgeTextTagged()
        TEXT = 'The Parrot Sketch.'
        ALL = -1
        target._model.set_text(TEXT, ALL)
        target._stale = False
        TEXT_NEW = 'Something completely different.'
        # Test
        target._set_persist(TEXT_NEW)
        assert TEXT_NEW == target._get_persist()
        assert target._stale


class TestFilterUserMarkup:
    """Unit tests for :func:`.filter_user_markup`."""

    def test_filter_user_markup(self):
        """| Confirm markup errors escaped.
        | Case: text does not contain markup error.
        """
        # Setup
        TEXT = 'The <b>Parrot Sketch.</b>'
        # Test
        assert TEXT == BTEXT.filter_user_markup(p_markup=TEXT)

    def test_filter_user_markup_error(self):
        """| Confirm markup errors escaped.
        | Case: text contains markup error.
        """
        # Setup
        TEXT = 'The <b>Parrot </b Sketch.'
        TEXT_CLEAN = GLib.markup_escape_text(TEXT, len(TEXT))
        # Test
        assert TEXT_CLEAN == BTEXT.filter_user_markup(p_markup=TEXT)

    def test_filter_user_markup_except(self, monkeypatch):
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
            _ = BTEXT.filter_user_markup(p_markup=TEXT)
        exc = exc_info.value
        assert DOMAIN == exc.domain
        assert MESSAGE == exc.message
        assert CODE == exc.code


class TestTypes:
    """Unit tests for type hint definitions in :mod:`.bridge_text`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (type(BTEXT.ModelTextOpaque), typing.TypeVar),
        (BTEXT.ModelTextOpaque.__constraints__, ()),
        (BTEXT.ModelTextTagged, Gtk.TextBuffer),
        (BTEXT.ModelTextMarkup, Gtk.EntryBuffer),
        # (BTEXT.ModelTextStatic, str),
        (BTEXT.ViewTextTagged, Gtk.TextView),
        (BTEXT.ViewTextMarkup, Gtk.Entry),
        (type(BTEXT.ViewTextOpaque), typing.TypeVar),
        (BTEXT.ViewTextOpaque.__constraints__, ()),
        (type(BTEXT.ViewTextOpaquePassive), typing.TypeVar),
        (BTEXT.ViewTextOpaquePassive.__constraints__, ()),
        (BTEXT.ViewTextDisplay, Gtk.Label),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions.

        :param TYPE_TARGET: type under test.
        :param TYPE_SOURCE: expected type.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
