"""
Unit tests for base of classes that encapsulate widget toolkit classes.
See :mod:`~.bridge_base`.
"""
import gi   # type: ignore[import]
# import logging
from pathlib import Path
import pickle
import pytest  # type: ignore[import]
import typing

import factsheet.bridge_gtk.bridge_base as BBASE

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk   # type: ignore[import]    # noqa: E402


class PatchBridgeBase(BBASE.BridgeBase[typing.Any, typing.Any]):
    """Class with test stubs for abstract :class:`~.BridgeBase` methods."""

    def __init__(self):
        super().__init__()
        self._ui_model = 'Oops! incomplete test initialization.'

    def _get_persist(self): return self._ui_model

    def _set_persist(self, p_persist): self._ui_model = p_persist


class TestBridgeBase:
    """Unit tests for :class:`~.BridgeBase`."""

    def test_eq(self):
        """Confirm equality comparison.

        #. Case: type difference.
        #. Case: storage element difference.
        #. Case: equivalent.
        """
        # Setup
        TEXT = 'Parrot'
        source = PatchBridgeBase()
        source._ui_model = TEXT
        # Test: type difference.
        assert not source.__eq__(TEXT)
        # Test: storage element difference.
        TEXT_DIFFER = 'Something completely different.'
        target = PatchBridgeBase()
        target._ui_model = TEXT_DIFFER
        assert not source.__eq__(target)
        # Test: equivalent.
        target = PatchBridgeBase()
        target._ui_model = TEXT
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format."""
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        TEXT = 'Parrot'
        source = PatchBridgeBase()
        source._ui_model = TEXT
        # Test
        with PATH.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert not hasattr(target, 'ex_ui_model')
        assert source._get_persist() == target._get_persist()

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        _target = PatchBridgeBase()
        # Successful call makes no state change.

    def test_str(self):
        """Confirm string representation."""
        # Setup
        TEXT = 'Parrot'
        target = PatchBridgeBase()
        target._ui_model = TEXT
        expect = '<PatchBridgeBase: {}>'.format(TEXT)
        # Test
        assert expect == str(target)

    def test_ui_model(self):
        """Confirm access limits of ui_model property."""
        # Setup
        target_class = PatchBridgeBase
        target = target_class()
        # Test
        assert target_class.ui_model.fget is not None
        assert target.ui_model is target._ui_model
        assert target_class.ui_model.fset is None
        assert target_class.ui_model.fdel is None

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BBASE.BridgeBase, '_get_persist'),
        (BBASE.BridgeBase, '_set_persist'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__


class TestBridgeTypes:
    """Unit tests for :class:`~.FactoryUiViewAbstract`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (type(BBASE.ModelUiOpaque), typing.TypeVar),
        (type(BBASE.PersistUiOpaque), typing.TypeVar),
        # (BBASE.ViewAny, Gtk.Widget),
        (type(BBASE.ViewUiOpaque), typing.TypeVar),
        (BBASE.TimeEvent, int),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type hint definitions.

        :param TYPE_TARGET: type hint as defined.
        :param TYPE_EXPECT: expected type hint.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT


class TestFactoryGtkViewAbstract:
    """Unit tests for `.FactoryUiViewAbstract`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BBASE.FactoryUiViewAbstract, '__call__'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__


class TestTimeEvent:
    """Unit tests for time constant in :mod:`.bridge_base`."""

    def test_time_current(self):
        """Confirm value of constant :data:`.TIME_EVENT_CURRENT`."""
        # Setup
        # Test
        assert Gdk.CURRENT_TIME == BBASE.TIME_EVENT_CURRENT
