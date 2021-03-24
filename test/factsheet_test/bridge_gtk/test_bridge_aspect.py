"""
Unit tests for GTK-based classes that encapsulate fact aspect classes.
See :mod:`~.bridge_aspect`.
"""
import gi   # type: ignore[import]
import pytest   # type: ignore[import]
import typing

import factsheet.bridge_gtk.bridge_aspect as BASPECT

from factsheet.bridge_gtk.bridge_aspect import ViewAspectOpaque

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class PatchBridgeAspect(BASPECT.BridgeAspect[
        typing.Any, typing.Any, typing.Any, typing.Any]):
    """Class with test stubs for abstract :class:`~.BridgeAbxtract` methods."""

    def _bind(self, p_view):
        p_view.set_label(self._model)

    def _get_persist(self):
        return self._model

    def _loose(self, p_view):
        p_view.set_label('')

    def _new_model(self):
        return str()

    def new_view(self):
        return BASPECT.ViewAspectPlain()

    def _set_persist(self, p_persist):
        self._model = p_persist
        for view in self._views.values():
            view.set_label(self._model)

    def transcribe(self, p_source):
        persist = ''
        if p_source is not None:
            persist = str(p_source)
        return persist


class TestBridgeAspect:
    """Unit tests for :class:`~.BridgeAspect`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BASPECT.BridgeAspect, '_bind'),
        (BASPECT.BridgeAspect, '_get_persist'),
        (BASPECT.BridgeAspect, '_loose'),
        (BASPECT.BridgeAspect, '_new_model'),
        (BASPECT.BridgeAspect, 'new_view'),
        (BASPECT.BridgeAspect, '_set_persist'),
        (BASPECT.BridgeAspect, 'transcribe'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__

    def test_refresh(self):
        """| Confirm storage and view elements are set from source.
        | Case: source is not None.
        """
        # Setup
        target = PatchBridgeAspect()
        N_VIEWS = 3
        views = [target.attach_view() for _ in range(N_VIEWS)]
        SOURCE = 42
        model = str(SOURCE)
        # Test
        target.refresh(SOURCE)
        assert model == target._model
        for view in views:
            assert target._views[id(view)] is view
            assert model == view.get_label()

    def test_refresh_none(self):
        """| Confirm storage and view elements are set from source.
        | Case: source is not None.
        """
        # Setup
        target = PatchBridgeAspect()
        N_VIEWS = 3
        views = [target.attach_view() for _ in range(N_VIEWS)]
        SOURCE = 42
        target.refresh(SOURCE)
        BLANK = ''
        # Test
        target.refresh(None)
        assert BLANK == target._model
        for view in views:
            assert target._views[id(view)] is view
            assert BLANK == view.get_label()


class TestBridgeAspectPlain:
    """Unit tests for :class:`.AspectPlain`.

    See :class:`.TestAspectCommon` for additional unit tests for
    :class:`.AspectPlain.
    """

    def test_init(self):
        """Confirm initialization."""
        # Setup
        BLANK = ''
        # Test
        target = BASPECT.BridgeAspectPlain[typing.Any]()
        assert BLANK == target._model
        assert isinstance(target._views, dict)

    def test_bind(self):
        """Confirm widget association."""
        # Setupsht
        target = BASPECT.BridgeAspectPlain[typing.Any]()
        TEXT = 'The <b>Parrot </b>Sketch'
        target._set_persist(TEXT)
        VIEW = BASPECT.ViewAspectPlain()
        # Test
        target._bind(VIEW)
        assert TEXT == VIEW.get_label()

    def test_get_persist(self):
        """Confirm export to persistent form."""
        # Setup
        target = BASPECT.BridgeAspectPlain[typing.Any]()
        TEXT = 'The <b>Parrot </b>Sketch'
        target._model = TEXT
        # Test
        assert TEXT == target._get_persist()

    def test_loose(self):
        """Confirm widget disassociation."""
        # Setup
        target = BASPECT.BridgeAspectPlain[typing.Any]()
        VIEW = BASPECT.ViewAspectPlain()
        TEXT = 'The <b>Parrot </b>Sketch'
        VIEW.set_label(TEXT)
        BLANK = ''
        # Test
        target._loose(VIEW)
        assert BLANK == VIEW.get_label()

    def test_new_model(self):
        """Confirm storage element."""
        # Setup
        target = BASPECT.BridgeAspectPlain[typing.Any]()
        # Test
        model = target._new_model()
        assert isinstance(model, BASPECT.ModelAspectPlain)

    def test_new_view(self):
        """Confirm view element."""
        # Setup
        target = BASPECT.BridgeAspectPlain[typing.Any]()
        # Test
        view = target.new_view()
        assert isinstance(view, BASPECT.ViewAspectPlain)

    def test_refresh(self):
        """| Confirm storage and view elements are set from source.
        | Case: source is not None.
        """
        # Setup
        target = BASPECT.BridgeAspectPlain[typing.Any]()
        N_VIEWS = 3
        views = [target.attach_view() for _ in range(N_VIEWS)]
        SOURCE = 42
        model = str(SOURCE)
        # Test
        target.refresh(SOURCE)
        assert model == target._model
        for view in views:
            assert target._views[id(view)] is view
            assert model == view.get_label()

    def test_refresh_none(self):
        """| Confirm storage and view elements are set from source.
        | Case: source is not None.
        """
        # Setup
        target = BASPECT.BridgeAspectPlain[typing.Any]()
        N_VIEWS = 3
        views = [target.attach_view() for _ in range(N_VIEWS)]
        SOURCE = 42
        target.refresh(SOURCE)
        BLANK = ''
        # Test
        target.refresh(None)
        assert BLANK == target._model
        for view in views:
            assert target._views[id(view)] is view
            assert BLANK == view.get_label()

    def test_set_persist(self):
        """Confirm import from persistent form."""
        # Setup
        target = BASPECT.BridgeAspectPlain[typing.Any]()
        TEXT = 'The <b>Parrot </b>Sketch.'
        target._model = TEXT
        N_VIEWS = 3
        views = [target.attach_view() for _ in range(N_VIEWS)]
        TEXT_NEW = 'Something <i>completely </i>different.'
        # Test
        target._set_persist(TEXT_NEW)
        assert TEXT_NEW == target._get_persist()
        for view in views:
            assert TEXT == view.get_label()

    def test_transcribe(self):
        """| Confirm transcription from source to persist form.
        | Case: source is not None.
        """
        # Setup
        target = BASPECT.BridgeAspectPlain[typing.Any]()
        N_VIEWS = 3
        _views = [target.attach_view() for _ in range(N_VIEWS)]
        SOURCE = 42
        text = str(SOURCE)
        # Test
        assert text == target.transcribe(SOURCE)

    def test_transcribe_none(self):
        """| Confirm transcription from source to persist form.
        | Case: source is None.
        """
        # Setup
        target = BASPECT.BridgeAspectPlain[typing.Any]()
        N_VIEWS = 3
        _views = [target.attach_view() for _ in range(N_VIEWS)]
        SOURCE = None
        BLANK = ''
        # Test
        assert BLANK == target.transcribe(SOURCE)

    def test_update_views(self):
        """Confirm manual update of views."""
        # Setup
        target = BASPECT.BridgeAspectPlain[typing.Any]()
        N_VIEWS = 3
        views = [target.attach_view() for _ in range(N_VIEWS)]
        SOURCE = 42
        model = str(SOURCE)
        target._model = model
        # Test
        target._update_views()
        for view in views:
            assert target._views[id(view)] is view
            assert model == view.get_label()


class TestBridgeAspectMissing:
    """Unit tests for :class:`~.BridgeAspectMissing`."""

    def test_transcribe(self):
        """Confirm warning for missing aspect."""
        # Setup
        target = BASPECT.BridgeAspectMissing()
        N_VIEWS = 3
        _views = [target.attach_view() for _ in range(N_VIEWS)]
        SOURCE = 'Dinsdale'
        text = ('Aspect \'{}\' not found. Please report omission.'
                ''.format(SOURCE))
        # Test
        assert text == target.transcribe(SOURCE)


class TestTypes:
    """Unit tests for type hint definitions in :mod:`.bridge_aspect`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (type(BASPECT.ModelAspectOpaque), typing.TypeVar),
        (BASPECT.ModelAspectOpaque.__constraints__, ()),
        (BASPECT.ModelAspectPlain, str),
        (type(BASPECT.PersistAspectOpaque), typing.TypeVar),
        (BASPECT.PersistAspectOpaque.__constraints__, ()),
        (BASPECT.PersistAspectPlain, str),
        (type(BASPECT.SourceOpaque), typing.TypeVar),
        (BASPECT.SourceOpaque.__constraints__, ()),
        (BASPECT.ViewAspectAny, Gtk.Widget),
        (BASPECT.ViewAspectMissing, Gtk.Label),
        (type(ViewAspectOpaque), typing.TypeVar),
        (BASPECT.ViewAspectOpaque.__constraints__, ()),
        (BASPECT.ViewAspectPlain, Gtk.Label),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
