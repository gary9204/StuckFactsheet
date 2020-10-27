"""
Unit tests for base of model classes that encapsulate widget toolkit
classes.  See :mod:`~.bridge_base`.
"""
import logging
from pathlib import Path
import pickle
import pytest  # type: ignore[import]
import typing

import factsheet.bridge_gtk.bridge_base as BBASE


class PatchBridgeBase(BBASE.BridgeBase[typing.Any, typing.Any, str]):
    """Class with test stubs for abstract :class:`~.BridgeBase` methods."""

    def __init__(self):
        super().__init__()
        self.bound = []
        self.loosed = []

    def _bind(self, p_view): self.bound.append(p_view)

    def _get_persist(self): return self._model

    def _loose(self, p_view): self.loosed.append(p_view)

    def _new_model(self): return str()

    def _set_persist(self, p_persist): self._model = p_persist


class TestBridgeBase:
    """Unit tests for :class:`~.BridgeBase`."""

    def test_eq(self):
        """Confirm equality comparison.

        #. Case: type difference.
        #. Case: storage element difference.
        #. Case: equivalent.
        """
        # Setup
        source = PatchBridgeBase()
        TEXT = 'Something completely different'
        source._set_persist(TEXT)
        N_VIEWS = 3
        views = [[i] for i in range(N_VIEWS)]
        for view in views:
            source.attach_view(view)
        source.bound.clear()
        # Test: type difference.
        assert not source.__eq__(TEXT)
        # Test: storage element difference.
        target = PatchBridgeBase()
        TEXT_DIFFER = 'Something completely different.'
        target._set_persist(TEXT_DIFFER)
        assert not source.__eq__(target)
        # Test: equivalent.
        target = PatchBridgeBase()
        target._set_persist(TEXT)
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format."""
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        source = PatchBridgeBase()
        TEXT = 'Something completely different'
        source._set_persist(TEXT)
        N_VIEWS = 3
        views = [[i] for i in range(N_VIEWS)]
        for view in views:
            source.attach_view(view)
        source.bound.clear()
        # Test
        with PATH.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert not hasattr(target, 'ex_model')
        assert source._get_persist() == target._get_persist()
        assert isinstance(target._views, dict)
        assert not target._views

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = PatchBridgeBase()
        assert isinstance(target._model, str)
        assert not target._model
        assert isinstance(target._views, dict)
        assert not target._views

    def test_iter(self):
        """Confirm iterator over views."""
        # Setup
        target = PatchBridgeBase()
        TEXT = 'Something completely different'
        target._set_persist(TEXT)
        N_VIEWS = 3
        views = [[i] for i in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        target.bound.clear()
        # Test
        assert views == list(target)

    def test_str(self):
        """Confirm string representation."""
        # Setup
        target = PatchBridgeBase()
        TEXT = 'Something completely different'
        target._set_persist(TEXT)
        N_VIEWS = 3
        views = [[i] for i in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        target.bound.clear()
        expect = '<PatchBridgeBase: {}>'.format(TEXT)
        # Test
        assert expect == str(target)

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BBASE.BridgeBase, '_bind'),
        (BBASE.BridgeBase, '_get_persist'),
        (BBASE.BridgeBase, '_loose'),
        (BBASE.BridgeBase, '_new_model'),
        (BBASE.BridgeBase, '_set_persist'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__

    def test_attach_view(self):
        """| Confirm view element association.
        | Case: view not associated initially
        """
        # Setup
        target = PatchBridgeBase()
        N_VIEWS = 3
        views = [[i] for i in range(N_VIEWS)]
        # Test
        for view in views:
            target.attach_view(view)
        assert len(views) == len(target._views)
        for view in views:
            assert target._views[id(view)] is view
        assert views == target.bound

    def test_attach_view_warn(self, monkeypatch, PatchLogger):
        """| Confirm view element association.
        | Case: view assocaited initially
        """
        # Setup
        target = PatchBridgeBase()
        N_VIEWS = 3
        views = [[i] for i in range(N_VIEWS)]
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

    def test_detach_all(self):
        """Confirm separation of all view elements."""
        # Setup
        target = PatchBridgeBase()
        N_VIEWS = 3
        views = [[i] for i in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        target.bound.clear()
        # Test
        target.detach_all()
        assert not target._views
        assert views == target.loosed

    def test_detach_view(self):
        """| Confirm view element separation.
        | Case: view assocated initially
        """
        # Setup
        target = PatchBridgeBase()
        N_VIEWS = 3
        views = [[i] for i in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        target.bound.clear()
        N_REMOVE = 1
        view_remove = views.pop(N_REMOVE)
        # Test
        target.detach_view(view_remove)
        assert len(views) == len(target._views)
        for view in views:
            assert target._views[id(view)] is view
        assert [view_remove] == target.loosed

    def test_detach_view_warn(self, monkeypatch, PatchLogger):
        """| Confirm view element separation.
        | Case: view not associated initially
        """
        # Setup
        target = PatchBridgeBase()
        N_VIEWS = 3
        views = [[i] for i in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        target.bound.clear()
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


class TestBridgeTypes:
    """Unit tests for type hint definitions in :mod:`.bridge_base`.
    """

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (type(BBASE.ModelOpaque), typing.TypeVar),
        (type(BBASE.PersistOpaque), typing.TypeVar),
        (type(BBASE.ViewOpaque), typing.TypeVar),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
