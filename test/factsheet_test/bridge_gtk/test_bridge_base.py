"""
Unit tests for base of classes that encapsulate widget toolkit classes.
See :mod:`~.bridge_base`.
"""
# import logging
from pathlib import Path
import pickle
import pytest  # type: ignore[import]
import typing

import factsheet.bridge_gtk.bridge_base as BBASE


class PatchBridgeBase(BBASE.BridgeBase[typing.Any, typing.Any, str]):
    """Class with test stubs for abstract :class:`~.BridgeBase` methods."""

    def __init__(self):
        self.called_common = False
        super().__init__()

    def _get_persist(self): return self._model

    def _init_transients(self):
        self.called_common = True

    def _new_model(self): return str()

    def new_view(self): return dict()

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
        for _ in range(N_VIEWS):
            _ = source.new_view()
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
        for _ in range(N_VIEWS):
            _ = source.new_view()
        source.called_common = False
        # Test
        with PATH.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert target.called_common
        assert not hasattr(target, 'ex_model')
        assert source._get_persist() == target._get_persist()
        # assert isinstance(target._views, dict)
        # assert not target._views

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = PatchBridgeBase()
        assert target.called_common
        assert isinstance(target._model, str)
        assert not target._model
        # assert isinstance(target._views, dict)
        # assert not target._views

    def test_str(self):
        """Confirm string representation."""
        # Setup
        target = PatchBridgeBase()
        TEXT = 'Something completely different'
        target._set_persist(TEXT)
        N_VIEWS = 3
        for _ in range(N_VIEWS):
            _ = target.new_view()
        expect = '<PatchBridgeBase: {}>'.format(TEXT)
        # Test
        assert expect == str(target)

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BBASE.BridgeBase, '_get_persist'),
        (BBASE.BridgeBase, '_new_model'),
        (BBASE.BridgeBase, 'new_view'),
        (BBASE.BridgeBase, '_set_persist'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__


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
