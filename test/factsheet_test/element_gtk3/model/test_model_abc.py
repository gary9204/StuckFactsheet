"""
Unit tests for storage element facade base class.  See
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


class PatchModelGtk3(EMABC.ModelGtk3[typing.Any, typing.Any]):
    """Class with test stubs for abstract
    :class:`~.element_gtk3.model.model_abc.ModelGtk3` methods.
    """

    MODEL_INIT = 'A Norwegian Blue'

    def new_ui_model(self):
        """Stub method."""
        return Gtk.Entry(text=self.MODEL_INIT)

    def set_internal(self, p_persist):
        """Stub method."""
        self._ui_model.set_text(p_persist)

    def to_external(self):
        """Stub method."""
        return self._ui_model.get_text()


class TestChangeMarkAbc:
    """Unit tests for :class:`~.element_gtk3.model.model_abc.ChangeMarkAbc`."""

    class TrackerStub(EMABC.ChangeMarkAbc[int]):
        """Subclass with stub for abstract methods."""

        def __init__(self, p_model: int) -> None:
            """Stub: pass through to super class.."""
            super().__init__(p_model)

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (EMABC.ChangeMarkAbc, '__init__'),
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

    def test_init(self):
        """Confirm mark initialized as unchanged."""
        # Setup
        MODEL = 42
        UNCHANGED = False
        # Test
        target = self.TrackerStub(p_model=MODEL)
        assert target._changed is UNCHANGED

    @pytest.mark.parametrize('CHANGED', [
        True,
        False,
        ])
    def test_has_changed(self, CHANGED):
        """Confirm report of mark is correct.

        :param CHANGED: expected mark.
        """
        # Setup
        MODEL = 42
        target = self.TrackerStub(p_model=MODEL)
        target._changed = CHANGED
        # Test
        assert target.has_changed() is CHANGED

    @pytest.mark.parametrize('CHANGED', [
        True,
        False,
        ])
    def test_set(self, CHANGED):
        """Confirm mark is set correctly.

        :param CHANGED: expected mark.
        """
        # Setup
        MODEL = 42
        target = self.TrackerStub(p_model=MODEL)
        target._changed = not CHANGED
        # Test
        target.set(CHANGED)
        assert target._changed is CHANGED


# class TestConsistency:
#     """Unit tests for :class:`~.element_gtk3.model.model_abc.Consistency`."""
#
#     @pytest.mark.parametrize('CLASS, NAME_METHOD', [
#         (EMABC.Consistency, 'alike'),
#         (EMABC.Consistency, 'differ'),
#         (EMABC.Consistency, 'set_alike'),
#         (EMABC.Consistency, 'set_differ'),
#         ])
#     def test_method_abstract(self, CLASS, NAME_METHOD):
#         """Confirm each abstract method is specified.
#
#         :param CLASS: class that should be abstract.
#         :param NAME_METHOD: method that should be abstract.
#         """
#         # Setup
#         # Test
#         assert hasattr(CLASS, '__abstractmethods__')
#         assert NAME_METHOD in CLASS.__abstractmethods__


class TestConversion:
    """Unit tests for :class:`~.element_gtk3.model.model_abc.Conversion`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (EMABC.Conversion, 'set_internal'),
        (EMABC.Conversion, 'to_external'),
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


class TestModelAbc:
    """Unit tests for :class:`~.element_gtk3.model.model_abc.ModelAbc`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (EMABC.ModelAbc, 'new_ui_model'),
        (EMABC.ModelAbc, 'ui_model'),
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
        target_class = EMABC.ModelAbc
        # Test
        assert target_class.ui_model.fget is not None
        assert target_class.ui_model.fset is None
        assert target_class.ui_model.fdel is None


class TestModelGtk3:
    """Unit tests for :class:`~.element_gtk3.model.model_abc.ModelGtk3`."""

    def test_eq(self):
        """Confirm equality comparison.

        #. Case: type difference.
        #. Case: storage element difference.
        #. Case: equivalent.
        """
        # Setup
        TEXT = 'Parrot'
        source = PatchModelGtk3()
        source._ui_model.set_text(TEXT)
        # Test: type difference.
        assert not source.__eq__(TEXT)
        # Test: storage element difference.
        TEXT_DIFFER = 'Something completely different.'
        target = PatchModelGtk3()
        target._ui_model.set_text(TEXT_DIFFER)
        assert not source.__eq__(target)
        # Test: equivalent.
        target = PatchModelGtk3()
        target._ui_model.set_text(TEXT)
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format."""
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        TEXT = 'Parrot'
        source = PatchModelGtk3()
        source._ui_model.set_text(TEXT)
        # Test
        with PATH.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert source.to_external() == target.to_external()
        assert not hasattr(target, 'ex_ui_model')

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = PatchModelGtk3()
        assert PatchModelGtk3.MODEL_INIT == target._ui_model.get_text()

    def test_str(self):
        """Confirm string representation."""
        # Setup
        TEXT = 'Parrot'
        target = PatchModelGtk3()
        target._ui_model.set_text(TEXT)
        expect = '<PatchModelGtk3: {}>'.format(TEXT)
        # Test
        assert expect == str(target)

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (EMABC.ModelGtk3, 'to_external'),
        (EMABC.ModelGtk3, 'new_ui_model'),
        (EMABC.ModelGtk3, 'set_internal'),
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
        :attr:`~.element_gtk3.model.model_abc.ModelGtk3.ui_model`
        property.
        """
        # Setup
        target_class = PatchModelGtk3
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
        (type(EMABC.ExternalOpaque), typing.TypeVar),
        (type(EMABC.ModelOpaque), typing.TypeVar),
        (type(EMABC.UiModelOpaque), typing.TypeVar),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type hint definitions.

        :param TYPE_TARGET: type hint under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT
