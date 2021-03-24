"""
Unit tests for GTK-based classes that implement abstract identification
information classes.  See :mod:`.bridge_text`.
"""
import gi   # type: ignore[import]
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
        self.bound = []
        self.loosed = []

    # def _bind(self, p_view):
    #     self.bound.append(p_view)

    def _get_persist(self):
        return self._model

    # def _loose(self, p_view):
    #     self.loosed = [p_view]

    def _new_model(self):
        return str()

    def new_view(self):
        return str()

    def _set_persist(self, p_persist):
        super()._set_persist(p_persist)
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
        # Test
        target = PatchBridgeText()
        # assert isinstance(target._views, dict)
        # assert not target._views
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
        """TBD"""
        # Setup
        target = PatchBridgeText()
        TEXT = 'The Parrot Sketch'
        # Test
        target._set_persist(TEXT)
        assert target.is_stale()

    def test_set_stale(self):
        """Confirm attribute marked stale. """
        # Setup
        target = PatchBridgeText()
        target._stale = False
        # Test
        target.set_stale()
        assert target._stale

    def test_text(self):
        """Confirm access limits of each concrete property."""
        # Setup
        # class PatchUpdate:
        #     def __init__(self): self.called = False

        #     def _update_views(self): self.called = True

        target_class = PatchBridgeText
        # patch_update = PatchUpdate()
        # monkeypatch.setattr(
        #     target_class, '_update_views', patch_update._update_views)

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
        # assert patch_update.called


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
        # I_ENTRY = 0
        # source._views[I_ENTRY] = CLASS_TEXT()
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
        # (BTEXT.BridgeTextStatic, BTEXT.ModelTextStatic),
        ])
    def test_init(self, CLASS_BRIDGE, CLASS_TEXT):
        """Confirm initialization. """
        # Setup
        # Test
        target = CLASS_BRIDGE()
        assert not target._stale
        # assert not target._views
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

    # def test_bind(self):
    #     """Confirm toolkit element association."""
    #     # Setup
    #     target = BTEXT.BridgeTextFormat()
    #     VIEW = BTEXT.ViewTextFormat()
    #     # Test
    #     target._bind(VIEW)
    #     assert target._model is VIEW.get_buffer()

    def test_get_persist(self):
        """Confirm export to persistent form."""
        # Setup
        target = BTEXT.BridgeTextFormat()
        TEXT = 'The Parrot Sketch.'
        ALL = -1
        target._model.set_text(TEXT, ALL)
        # Test
        assert TEXT == target._get_persist()

    # def test_loose(self):
    #     """Confirm toolkit element disassociation."""
    #     # Setup
    #     target = BTEXT.BridgeTextFormat()
    #     VIEW = BTEXT.ViewTextFormat()
    #     target._bind(VIEW)
    #     assert target._model is VIEW.get_buffer()
    #     # Test
    #     target._loose(VIEW)
    #     assert target._model is not VIEW.get_buffer()

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

    # def test_bind(self):
    #     """Confirm widget association."""
    #     # Setup
    #     target = BTEXT.BridgeTextMarkup()
    #     VIEW = BTEXT.ViewTextMarkup()
    #     # Test
    #     target._bind(VIEW)
    #     assert target._model is VIEW.get_buffer()

    def test_get_persist(self):
        """Confirm export to persistent form."""
        # Setup
        target = BTEXT.BridgeTextMarkup()
        TEXT = 'The Parrot Sketch.'
        ALL = -1
        target._model.set_text(TEXT, ALL)
        # Test
        assert TEXT == target._get_persist()

    # def test_loose(self):
    #     """Confirm widget disassociation."""
    #     # Setup
    #     target = BTEXT.BridgeTextMarkup()
    #     VIEW = BTEXT.ViewTextMarkup()
    #     target._bind(VIEW)
    #     assert target._model is VIEW.get_buffer()
    #     # Test
    #     target._loose(VIEW)
    #     assert target._model is not VIEW.get_buffer()

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
        # (BTEXT.BridgeTextStatic, BTEXT.ModelTextStatic),
        # Test
        target = BTEXT.BridgeTextStatic()
        assert not target._stale
        assert not target._views
        assert isinstance(target._model, BTEXT.ModelTextStatic)
        assert not target._get_persist()

    # def test_bind(self):
    #     """Confirm widget association."""
    #     # Setupsht
    #     target = BTEXT.BridgeTextStatic()
    #     TEXT = 'The <b>Parrot </b>Sketch'
    #     target._set_persist(TEXT)
    #     VIEW = BTEXT.ViewTextStatic()
    #     # Test
    #     target._bind(VIEW)
    #     assert TEXT == VIEW.get_label()

    def test_get_persist(self):
        """Confirm export to persistent form."""
        # Setup
        target = BTEXT.BridgeTextStatic()
        TEXT = 'The <b>Parrot </b>Sketch'
        target._model = TEXT
        # Test
        assert TEXT == target._get_persist()

    # def test_loose(self):
    #     """Confirm widget disassociation."""
    #     # Setup
    #     target = BTEXT.BridgeTextStatic()
    #     VIEW = BTEXT.ViewTextStatic()
    #     TEXT = 'The <b>Parrot </b>Sketch'
    #     VIEW.set_label(TEXT)
    #     BLANK = ''
    #     # Test
    #     target._loose(VIEW)
    #     assert BLANK == VIEW.get_label()

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

    # def test_bind(self):
    #     """Confirm widget association."""
    #     # Setupsht
    #     target = BTEXT.BridgeTextStatic()
    #     TEXT = 'The <b>Parrot </b>Sketch'
    #     target._set_persist(TEXT)
    #     VIEW = BTEXT.ViewTextStatic()
    #     # Test
    #     target._bind(VIEW)
    #     assert TEXT == VIEW.get_label()

    @pytest.mark.skip
    def test_set_persist(self):
        """Confirm import from persistent form."""
        # Setup
        target = BTEXT.BridgeTextStatic()
        TEXT = 'The <b>Parrot </b>Sketch.'
        target._model = TEXT
        target._stale = False
        N_VIEWS = 3
        _views = [target.new_view() for _ in range(N_VIEWS)]
        TEXT_NEW = 'Something <i>completely </i>different.'
        # Test
        target._set_persist(TEXT_NEW)
        assert target._stale
        assert TEXT_NEW == target._get_persist()

    def test_text_setter(self):
        """Confirm extension of text property setter."""
        # Setup
        target = BTEXT.BridgeTextStatic()
        TEXT = 'The Parrot Sketch'
        target._set_persist(TEXT)
        TEXT_NEW = 'Something completely different.'
        N_VIEWS = 3
        views = [target.new_view() for _ in range(N_VIEWS)]
        # view = target.new_view()
        # Test
        target.text = TEXT_NEW
        assert TEXT_NEW == target._get_persist()
        for view in views:
            assert TEXT_NEW == view.get_label()
        # assert TEXT_NEW == view.get_label()

    # def test_update_views(self):
    #     """Confirm views match persistent form."""
    #     # Setup
    #     target = BTEXT.BridgeTextStatic()
    #     TEXT = 'The <b>Parrot </b>Sketch.'
    #     target._model = TEXT
    #     target._stale = False
    #     N_VIEWS = 3
    #     views = [target.new_view() for _ in range(N_VIEWS)]
    #     TEXT_NEW = 'Something <i>completely </i>different.'
    #     target._set_persist(TEXT_NEW)
    #     # Test
    #     target._update_views()
    #     for view in views:
    #         assert TEXT_NEW == view.get_label()


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
