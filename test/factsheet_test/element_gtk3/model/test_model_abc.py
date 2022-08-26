"""
Unit tests storage element facade base class.  See
:mod:`.element_gtk3.model.model_abc`.
"""
import gi   # type: ignore[import]
from pathlib import Path
import pickle
import pytest
import typing

import factsheet.element_gtk3.model.model_abc as EMABC

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class PatchModelAbc(EMABC.ModelAbc[typing.Any, typing.Any]):
    """Class with test stubs for abstract
    :class:`~.element_gtk3.model.model_abc.ModelAbc` methods.
    """

    MODEL_INIT = 'A Norwegian Blue'

    def get_persist(self): return self._ui_model.get_text()

    def new_ui_model(self): return Gtk.Entry(text=self.MODEL_INIT)

    def set_persist(self, p_persist): self._ui_model.set_text(p_persist)


class TestModelAbc:
    """Unit tests for :class:`~.element_gtk3.model.model_abc.ModelAbc`."""

    def test_eq(self):
        """Confirm equality comparison.

        #. Case: type difference.
        #. Case: storage element difference.
        #. Case: equivalent.
        """
        # Setup
        TEXT = 'Parrot'
        source = PatchModelAbc()
        source._ui_model.set_text(TEXT)
        # Test: type difference.
        assert not source.__eq__(TEXT)
        # Test: storage element difference.
        TEXT_DIFFER = 'Something completely different.'
        target = PatchModelAbc()
        target._ui_model.set_text(TEXT_DIFFER)
        assert not source.__eq__(target)
        # Test: equivalent.
        target = PatchModelAbc()
        target._ui_model.set_text(TEXT)
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format."""
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        TEXT = 'Parrot'
        source = PatchModelAbc()
        source._ui_model.set_text(TEXT)
        # Test
        with PATH.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert source.get_persist() == target.get_persist()
        assert not hasattr(target, 'ex_ui_model')

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = PatchModelAbc()
        assert PatchModelAbc.MODEL_INIT == target._ui_model.get_text()

    def test_str(self):
        """Confirm string representation."""
        # Setup
        TEXT = 'Parrot'
        target = PatchModelAbc()
        target._ui_model.set_text(TEXT)
        expect = '<PatchModelAbc: {}>'.format(TEXT)
        # Test
        assert expect == str(target)

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (EMABC.ModelAbc, 'get_persist'),
        (EMABC.ModelAbc, 'new_ui_model'),
        (EMABC.ModelAbc, 'set_persist'),
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

    def test_ui_model(self):
        """Confirm access limits of
        :attr:`~.element_gtk3.model.model_abc.ModelAbc.ui_model`
        property.
        """
        # Setup
        target_class = PatchModelAbc
        target = target_class()
        # Test
        assert target_class.ui_model.fget is not None
        assert target.ui_model is target._ui_model
        assert target_class.ui_model.fset is None
        assert target_class.ui_model.fdel is None


class TestModule:
    """Unit tests for module-level components of
    :mod:`~.element_gtk3.model.model_abc`.
    """

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (type(EMABC.UiModelOpaque), typing.TypeVar),
        (type(EMABC.PersistOpaque), typing.TypeVar),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type hint definitions.

        :param TYPE_TARGET: type hint under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT
