"""
Unit tests for GTK-based classes that implement abstract identification
information classes.  See :mod:`.bridge_text`.
"""
import gi   # type: ignore[import]
import logging
import pickle
import pytest   # type: ignore[import]
import typing

from pathlib import Path

import factsheet.bridge_gtk.bridge_text as BTEXT

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class PatchBridgeText(BTEXT.BridgeText[typing.Any, typing.Any]):
    """:class:`.BridgeText` subclass with stub text property."""

    def __init__(self):
        super().__init__()

    def _get_persist(self):
        return self._model

    def _new_model(self):
        return str()

    def new_view(self):
        return str()

    def _set_persist(self, p_persist):
        self._model = str(p_persist)


class TestBridgeText:
    """Unit tests for :class:`.BridgeText`.

    See :mod:`.abc_common` for additional tests to confirm method and
    property definitions of :class:`.BridgeText`.
    """

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BTEXT.BridgeText, '_get_persist'),
        (BTEXT.BridgeText, '_new_model'),
        (BTEXT.BridgeText, 'new_view'),
        (BTEXT.BridgeText, '_set_persist'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
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
        """Confirm conversion to and from pickle format."""
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
            (BTEXT.BridgeTextFormat, BTEXT.ModelTextFormat,
                'changed', 0),
            (BTEXT.BridgeTextMarkup, BTEXT.ModelTextMarkup,
                'deleted-text', 0),
            (BTEXT.BridgeTextMarkup, BTEXT.ModelTextMarkup,
                'inserted-text', 0),
        ])
    def test_get_set_signals(self, tmp_path, CLASS_BRIDGE, CLASS_TEXT,
                             NAME_SIGNAL, N_DEFAULT):
        """Confirm reconstruction of signal connections."""
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
        (BTEXT.BridgeTextFormat, BTEXT.ModelTextFormat),
        (BTEXT.BridgeTextMarkup, BTEXT.ModelTextMarkup),
        # See TestBridgeTextStatic for specialized test.
        ])
    def test_init(self, CLASS_BRIDGE, CLASS_TEXT):
        """Confirm initialization. """
        # Setup
        # Test
        target = CLASS_BRIDGE()
        assert not target._stale
        assert isinstance(target._model, CLASS_TEXT)
        assert not target._get_persist()

    @pytest.mark.parametrize(
        'CLASS_BRIDGE, CLASS_TEXT, NAME_SIGNAL, N_DEFAULT', [
            (BTEXT.BridgeTextFormat, BTEXT.ModelTextFormat,
                'changed', 0),
            (BTEXT.BridgeTextMarkup, BTEXT.ModelTextMarkup,
                'deleted-text', 0),
            (BTEXT.BridgeTextMarkup, BTEXT.ModelTextMarkup,
             'inserted-text', 0),
        ])
    def test_init_signals(
            self, CLASS_BRIDGE, CLASS_TEXT, NAME_SIGNAL, N_DEFAULT):
        """Confirm initialization of signal connections."""
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


class TestBridgeTextFormat:
    """Unit tests for :class:`.BridgeTextFormat`.

    See :class:`.TestBridgeTextCommon` for additional unit tests for
    :class:`.BridgeTextFormat`.
    """

    def test_get_persist(self):
        """Confirm export to persistent form."""
        # Setup
        target = BTEXT.BridgeTextFormat()
        TEXT = 'The Parrot Sketch.'
        ALL = -1
        target._model.set_text(TEXT, ALL)
        # Test
        assert TEXT == target._get_persist()

    def test_new_model(self):
        """Confirm storage element."""
        # Setup
        target = BTEXT.BridgeTextFormat()
        # Test
        assert isinstance(target._model, BTEXT.ModelTextFormat)

    def test_new_view(self):
        """Confirm view element."""
        # Setup
        target = BTEXT.BridgeTextFormat()
        # Test
        view = target.new_view()
        assert isinstance(view, BTEXT.ViewTextFormat)
        assert target._model is view.get_buffer()

    def test_set_persist(self):
        """Confirm import from persistent form."""
        # Setup
        target = BTEXT.BridgeTextFormat()
        TEXT = 'The Parrot Sketch.'
        ALL = -1
        target._model.set_text(TEXT, ALL)
        target._stale = False
        TEXT_NEW = 'Something completely different.'
        # Test
        target._set_persist(TEXT_NEW)
        assert TEXT_NEW == target._get_persist()
        assert target._stale


class TestBridgeTextMarkup:
    """Unit tests for :class:`.BridgeTextMarkup`.

    :class:`.TestBridgeTextCommon` contains additional unit tests for
    :class:`.BridgeTestMarkup`.
    """

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

    def test_new_view(self):
        """Confirm view element."""
        # Setup
        target = BTEXT.BridgeTextMarkup()
        # Test
        view = target.new_view()
        assert isinstance(view, BTEXT.ViewTextMarkup)
        assert target._model is view.get_buffer()

    def test_set_persist(self):
        """Confirm import from persistent form."""
        # Setup
        target = BTEXT.BridgeTextMarkup()
        TEXT = 'The Parrot Sketch.'
        ALL = -1
        target._model.set_text(TEXT, ALL)
        target._stale = False
        TEXT_NEW = 'Something completely different.'
        # Test
        target._set_persist(TEXT_NEW)
        assert TEXT_NEW == target._get_persist()
        assert target._stale


class TestBridgeTextStatic:
    """Unit tests for :class:`.BridgeTextStatis`.

    See :class:`.TestBridgeTextCommon` for additional unit tests for
    :class:`.BridgeTestStatic`.
    """

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format."""
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        source = BTEXT.BridgeTextStatic()
        TEXT = 'Something completely different'
        source._set_persist(TEXT)
        source._stale = True
        I_ENTRY = 0
        source._views[I_ENTRY] = BTEXT.ViewTextStatic()
        # Test
        with PATH.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert source._get_persist() == target._get_persist()
        assert isinstance(target._views, dict)
        assert not target._views
        assert not target._stale

    def test_init(self):
        """Confirm initialization. """
        # Setup
        # Test
        target = BTEXT.BridgeTextStatic()
        assert not target._stale
        assert not target._views
        assert isinstance(target._model, BTEXT.ModelTextStatic)
        assert not target._get_persist()

    def test_destroy_view(self):
        """| Confirm view removal.
        | Case: model connected to view.
        """
        # Setup
        target = BTEXT.BridgeTextStatic()
        N_VIEWS = 5
        I_REMOVE = 4
        for i in range(N_VIEWS):
            view = BTEXT.ViewTextStatic()
            id_view = id(view)
            target._views[id_view] = view
            if i == I_REMOVE:
                id_remove = id_view
                view_remove = view
        # Test
        target._destroy_view(view_remove)
        assert id_remove not in target._views

    def test_destroy_view_warn(self, PatchLogger, monkeypatch):
        """| Confirm view removal.
        | Case: model not connected view.
        """
        # Setup
        target = BTEXT.BridgeTextStatic()
        N_VIEWS = 5
        for _ in range(N_VIEWS):
            view = BTEXT.ViewTextStatic()
            target._views[id(view)] = view
        VIEW_MISSING = BTEXT.ViewTextStatic()

        patch_logger = PatchLogger()
        monkeypatch.setattr(logging.Logger, 'warning', patch_logger.warning)
        log_message = ('Missing view: {} (BridgeTextStatic._destroy_view)'
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
        target = BTEXT.BridgeTextStatic()
        TEXT = 'The <b>Parrot </b>Sketch'
        target._model = TEXT
        # Test
        assert TEXT == target._get_persist()

    def test_new_model(self):
        """Confirm storage type."""
        # Setup
        target = BTEXT.BridgeTextStatic()
        # Test
        assert isinstance(target._model, BTEXT.ModelTextStatic)

    def test_new_view(self, monkeypatch):
        """Confirm view element."""
        # Setup
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
        target = BTEXT.BridgeTextStatic()
        TEXT = 'The <b>Parrot </b>Sketch'
        target._set_persist(TEXT)
        SIGNAL = 'destroy'
        HANDLER = target._destroy_view
        # Test
        view = target.new_view()
        assert isinstance(view, BTEXT.ViewTextStatic)
        assert TEXT == view.get_label()
        assert patch_connect.called
        assert SIGNAL == patch_connect.signal
        assert target._destroy_view == HANDLER
        assert target._views[id(view)] is view

    def test_set_persist(self):
        """Confirm import from persistent form."""
        # Setup
        target = BTEXT.BridgeTextStatic()
        TEXT = 'The <b>Parrot </b>Sketch.'
        target._model = TEXT
        target._stale = False
        N_VIEWS = 3
        for _ in range(N_VIEWS):
            view = BTEXT.ViewTextStatic()
            target._views[id(view)] = view
        TEXT_NEW = 'Something <i>completely </i>different.'
        # Test
        target._set_persist(TEXT_NEW)
        assert TEXT_NEW == target._get_persist()
        assert N_VIEWS == len(target._views)
        for view in target._views.values():
            assert TEXT_NEW == view.get_label()


class TestTypes:
    """Unit tests for type hint definitions in :mod:`.bridge_text`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (type(BTEXT.ModelTextOpaque), typing.TypeVar),
        (BTEXT.ModelTextFormat, Gtk.TextBuffer),
        (BTEXT.ModelTextMarkup, Gtk.EntryBuffer),
        (BTEXT.ModelTextStatic, str),
        (BTEXT.ViewTextFormat, Gtk.TextView),
        (BTEXT.ViewTextMarkup, Gtk.Entry),
        (type(BTEXT.ViewTextOpaque), typing.TypeVar),
        (BTEXT.ViewTextOpaque.__constraints__, ()),
        (BTEXT.ViewTextStatic, Gtk.Label),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
