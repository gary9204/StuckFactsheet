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


class TestBridgeText:
    """Unit tests for :class:`.BridgeText`.

    See :mod:`.abc_common` for additional tests to confirm method and
    property definitions of :class:`.BridgeText`.
    """

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BTEXT.BridgeText, '_bind'),
        (BTEXT.BridgeText, '_get_persist'),
        (BTEXT.BridgeText, '_loose'),
        (BTEXT.BridgeText, '_new_model'),
        (BTEXT.BridgeText, '_set_persist'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__

    def test_eq(self, patch_bridge_text):
        """Confirm equality comparison.

        #. Case: not a text attribute.
        #. Case: different content.
        #. Case: equal
        """
        # Setup
        TEXT = 'The Parrot Sketch'
        source = patch_bridge_text()
        source._set_persist(TEXT)
        # Test: not a text attribute.
        assert not source.__eq__(TEXT)
        # Test: different content.
        TEXT_DIFFER = 'Something completely different.'
        target = patch_bridge_text()
        target._set_persist(TEXT_DIFFER)
        assert not source.__eq__(target)
        # Test: equal
        target = patch_bridge_text()
        target._set_persist(TEXT)
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path, patch_bridge_text):
        """Confirm conversion to and from pickle format."""
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        source = patch_bridge_text()
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

    def test_init(self, patch_bridge_text):
        """Confirm initialization."""
        # Setup
        # Test
        target = patch_bridge_text()
        assert isinstance(target._views, dict)
        assert not target._views
        assert isinstance(target._model, str)
        assert not target._model
        assert target._stale is not None
        assert not target._stale

    def test_str(self, patch_bridge_text):
        """Confirm return is attribute content. """
        # Setup
        TEXT = 'The Parrot Sketch'
        target = patch_bridge_text()
        target._model = TEXT
        expect = '<{}: {}>'.format(type(target).__name__, TEXT)
        # Test
        assert expect == str(target)

    def test_attach_view(self, patch_bridge_text):
        """| Confirm addition of view.
        | Case: view not attached initially
        """
        # Setup
        target = patch_bridge_text()
        N_VIEWS = 3
        views = [BTEXT.ViewTextStatic() for _ in range(N_VIEWS)]
        # Test
        for view in views:
            target.attach_view(view)
        assert len(views) == len(target._views)
        for view in views:
            assert target._views[id(view)] is view
        assert views == target.bound

    def test_attach_view_warn(
            self, patch_bridge_text, monkeypatch, PatchLogger):
        """| Confirm addition of view.
        | Case: view attached initially
        """
        # Setup
        target = patch_bridge_text()
        N_VIEWS = 3
        views = [BTEXT.ViewTextStatic() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        target.bound.clear()
        I_DUP = 1
        view_dup = views[I_DUP]

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Duplicate view: {} ({}.attach_view)'
            ''.format(hex(id(view_dup)), type(target).__name__))
        # Test
        target.attach_view(view_dup)
        assert len(views) == len(target._views)
        assert not target.bound
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_detach_view(self, patch_bridge_text):
        """| Confirm removal of view.
        | Case: view attached initially
        """
        # Setup
        target = patch_bridge_text()

        N_VIEWS = 3
        views = [BTEXT.ViewTextMarkup() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        N_REMOVE = 1
        view_remove = views.pop(N_REMOVE)
        # Test
        target.detach_view(view_remove)
        assert len(views) == len(target._views)
        for view in views:
            assert target._views[id(view)] is view
        assert [view_remove] == target.loosed

    def test_detach_view_warn(
            self, patch_bridge_text, monkeypatch, PatchLogger):
        """| Confirm removal of view.
        | Case: view not attached initially
        """
        # Setup
        target = patch_bridge_text()

        N_VIEWS = 3
        views = [BTEXT.ViewTextStatic() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        N_REMOVE = 1
        view_remove = views.pop(N_REMOVE)
        target.detach_view(view_remove)
        target.loosed.clear()
        assert len(views) == len(target._views)

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Missing view: {} ({}.detach_view)'
            ''.format(hex(id(view_remove)), type(target).__name__))
        # Test
        target.detach_view(view_remove)
        assert not target.loosed
        assert len(views) == len(target._views)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_is_fresh(self, patch_bridge_text):
        """Confirm return matches state. """
        # Setup
        target = patch_bridge_text()
        target._stale = False
        # Test
        assert target.is_fresh()
        target._stale = True
        assert not target.is_fresh()

    def test_is_stale(self, patch_bridge_text):
        """Confirm return matches state. """
        # Setup
        target = patch_bridge_text()
        target._stale = False
        # Test
        assert not target.is_stale()
        target._stale = True
        assert target.is_stale()

    def test_set_freah(self, patch_bridge_text):
        """Confirm attribute marked fresh. """
        # Setup
        target = patch_bridge_text()
        target._stale = True
        # Test
        target.set_fresh()
        assert not target._stale

    def test_set_stale(self, patch_bridge_text):
        """Confirm attribute marked stale. """
        # Setup
        target = patch_bridge_text()
        target._stale = False
        # Test
        target.set_stale()
        assert target._stale

    def test_text(self, patch_bridge_text):
        """Confirm access limits of each concrete property."""
        # Setup
        target_class = patch_bridge_text
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


class TestBridgeTextCommon:
    """Unit tests common common to descendants of :class:`.BridgeText`.

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
        I_ENTRY = 0
        source._views[I_ENTRY] = CLASS_TEXT()
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
        (BTEXT.BridgeTextStatic, BTEXT.ModelTextStatic),
        ])
    def test_init(self, CLASS_BRIDGE, CLASS_TEXT):
        """Confirm initialization. """
        # Setup
        # Test
        target = CLASS_BRIDGE()
        assert not target._stale
        assert not target._views
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

    :class:`.TestBridgeTextCommon` contains all unit tests for
    :class:`.BridgeTextFormat`.
    """

    def test_bind(self):
        """Confirm toolkit element association."""
        # Setup
        target = BTEXT.BridgeTextFormat()
        VIEW = BTEXT.ViewTextFormat()
        # Test
        target._bind(VIEW)
        assert target._model is VIEW.get_buffer()

    def test_get_persist(self):
        """Confirm export to persistent form."""
        # Setup
        target = BTEXT.BridgeTextFormat()
        TEXT = 'The Parrot Sketch.'
        ALL = -1
        target._model.set_text(TEXT, ALL)
        # Test
        assert TEXT == target._get_persist()

    def test_loose(self):
        """Confirm toolkit element disassociation."""
        # Setup
        target = BTEXT.BridgeTextFormat()
        VIEW = BTEXT.ViewTextFormat()
        target._bind(VIEW)
        assert target._model is VIEW.get_buffer()
        # Test
        target._loose(VIEW)
        assert target._model is not VIEW.get_buffer()

    def test_new_model(self):
        """Confirm storage element."""
        # Setup
        target = BTEXT.BridgeTextFormat()
        # Test
        assert isinstance(target._model, BTEXT.ModelTextFormat)

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

    def test_bind(self):
        """Confirm GTK binding."""
        # Setup
        target = BTEXT.BridgeTextMarkup()
        VIEW = BTEXT.ViewTextMarkup()
        # Test
        target._bind(VIEW)
        assert target._model is VIEW.get_buffer()

    def test_get_persist(self):
        """Confirm export to persistent form."""
        # Setup
        target = BTEXT.BridgeTextMarkup()
        TEXT = 'The Parrot Sketch.'
        ALL = -1
        target._model.set_text(TEXT, ALL)
        # Test
        assert TEXT == target._get_persist()

    def test_loose(self):
        """Confirm GTK binding."""
        # Setup
        target = BTEXT.BridgeTextMarkup()
        VIEW = BTEXT.ViewTextMarkup()
        target._bind(VIEW)
        assert target._model is VIEW.get_buffer()
        # Test
        target._loose(VIEW)
        assert target._model is not VIEW.get_buffer()

    def test_new_model(self):
        """Confirm storage type."""
        # Setup
        target = BTEXT.BridgeTextMarkup()
        # Test
        assert isinstance(target._model, BTEXT.ModelTextMarkup)

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

    def test_bind(self):
        """Confirm GTK binding."""
        # Setupsht
        target = BTEXT.BridgeTextStatic()
        TEXT = 'The <b>Parrot </b>Sketch'
        target._set_persist(TEXT)
        VIEW = BTEXT.ViewTextStatic()
        # Test
        target._bind(VIEW)
        assert TEXT == VIEW.get_label()

    def test_get_persist(self):
        """Confirm export to persistent form."""
        # Setup
        target = BTEXT.BridgeTextStatic()
        TEXT = 'The <b>Parrot </b>Sketch'
        target._model = TEXT
        # Test
        assert TEXT == target._get_persist()

    def test_loose(self):
        """Confirm GTK binding."""
        # Setup
        target = BTEXT.BridgeTextStatic()
        VIEW = BTEXT.ViewTextStatic()
        TEXT = 'The <b>Parrot </b>Sketch'
        VIEW.set_label(TEXT)
        BLANK = ''
        # Test
        target._loose(VIEW)
        target._bind(VIEW)
        assert BLANK == VIEW.get_label()

    def test_new_model(self):
        """Confirm storage type."""
        # Setup
        target = BTEXT.BridgeTextStatic()
        # Test
        assert isinstance(target._model, BTEXT.ModelTextStatic)

    def test_set_persist(self):
        """Confirm import from persistent form."""
        # Setup
        target = BTEXT.BridgeTextStatic()
        TEXT = 'The <b>Parrot </b>Sketch.'
        target._model = TEXT
        target._stale = False
        N_VIEWS = 3
        views = [BTEXT.ViewTextStatic() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        TEXT_NEW = 'Something <i>completely </i>different.'
        # Test
        target._set_persist(TEXT_NEW)
        assert target._stale
        assert TEXT_NEW == target._get_persist()
        for view in views:
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
