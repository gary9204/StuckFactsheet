"""
Unit tests for :mod:`.new_component_abc`.
"""
import pytest
import typing

import factsheet.ui_bricks.ui_abc.new_component_abc as NEWCOMPABC


class TestNewComponentAbc:
    """Unit tests for :class:`.NewComponentAbc`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (NEWCOMPABC.NewComponentAbc, 'new_control'),
        (NEWCOMPABC.NewComponentAbc, 'new_control_track'),
        (NEWCOMPABC.NewComponentAbc, 'new_model'),
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


class TestModule:
    """Unit tests for module-level components of :mod:`.new_component_abc`.
    """

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (type(NEWCOMPABC.ControlOpaque), typing.TypeVar),
        (type(NEWCOMPABC.ControlTrackOpaque), typing.TypeVar),
        (type(NEWCOMPABC.ModelOpaque), typing.TypeVar),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type definitions.

        :param TYPE_TARGET: type under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT
