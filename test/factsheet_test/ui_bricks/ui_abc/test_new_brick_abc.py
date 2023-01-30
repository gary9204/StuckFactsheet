"""
Unit tests for :mod:`.new_brick_abc`.
"""
import pytest
import typing

import factsheet.ui_bricks.ui_abc.new_brick_abc as NBRICKABC


class TestModule:
    """Unit tests for module-level components of :mod:`.new_brick_abc`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (type(NBRICKABC.ControlMarkupGeneric), typing.TypeVar),
        (NBRICKABC.ControlMarkupGeneric.__constraints__,  # type: ignore
            ()),
        (type(NBRICKABC.ControlMarkupTrackGeneric), typing.TypeVar),
        (NBRICKABC.ControlMarkupTrackGeneric.__constraints__,  # type: ignore
            ()),
        (type(NBRICKABC.ModelMarkupGeneric), typing.TypeVar),
        (NBRICKABC.ModelMarkupGeneric.__constraints__,  # type: ignore
            ()),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type definitions.

        :param TYPE_TARGET: type under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT


class TestNewBrickAbc:
    """Unit tests for :class:`.NewBrickAbc`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (NBRICKABC.NewBrickAbc, 'markup'),
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
